//! The `grust` participants: Grust's own kernels over `GraphProjection`, direct,
//! with no procedure layer, no Cypher and no storage backend.
//!
//! One source, two builds. `grust/Cargo.toml` builds it against the published
//! release, v0.22.0; `grust-next/Cargo.toml` builds the same file against the
//! commit under test with the `accounting-api` feature, which is what that
//! commit added and the release does not have: `GraphProjection::prepare_incoming`,
//! `ExecutionContext::with_accounting`, and `WorkCount` in place of a `usize`
//! work total. A harness that edited this file per commit would be timing two
//! participants; this way the only difference between the columns is Grust.
//!
//! The budget is deliberately unbounded here. Charging is part of what these
//! kernels do and stays on by default, but a limit that could fire would make
//! the column a measurement of a policy rather than of a kernel; the resources
//! it did charge are reported beside the result instead. Whether charging
//! happens at all is `--accounting`, and every output line names the mode.
//!
//! Where the transpose is built is the correction this participant carries.
//! B3 built Grust's incoming adjacency lazily, inside the first kernel that
//! needed it, so it was timed in `kernel_ms`; grustcat builds both adjacencies
//! in its constructor, inside `build_ms`. With `accounting-api` the transpose is
//! built by `prepare_incoming` inside the build timer and its share is reported
//! as `incoming_ms`. The release has no such method, so every build runs the
//! kernel twice on the same projection and reports both calls: the first is
//! what B3 published, the second has the transpose already cached.
//!
//! B4 prepared it for every algorithm, including the three kernels that never
//! read in-arcs, and that was a harness artifact rather than a measurement:
//! building and freeing a transpose no kernel reads leaves the process's
//! allocator in a different state, and the first call after it took about 112
//! to 128 more minor page faults. `--prepare-incoming needed`, the default
//! here, prepares it only for a kernel that reads it — PageRank's pull kernel,
//! and no other kernel in this matrix. `--prepare-incoming always` keeps B4's
//! behaviour available as its own labelled row, so the correction can be shown
//! rather than asserted. Minor page faults are reported beside every call, read
//! outside every timer, because that is the quantity the artifact moved.

use std::time::Instant;

#[cfg(feature = "accounting-api")]
use grust_algorithms::Accounting;
use grust_algorithms::{
    ExecutionContext, ExecutionLimits, GraphProjection, Orientation, PageRankOptions,
    ProjectionEdge, SnapshotIdentity, TriangleOptions, bfs, pagerank, triangles,
    weakly_connected_components,
};

/// `struct rusage` on Linux: two timevals, then fourteen longs. `ru_minflt` is
/// the fifth of those longs, so index 8 of eighteen words.
#[repr(C)]
struct Rusage {
    words: [i64; 18],
}

unsafe extern "C" {
    fn getrusage(who: i32, usage: *mut Rusage) -> i32;
}

/// Minor page faults taken by this process and all its threads so far.
///
/// Read outside every timer, never inside one. This is the quantity the B4
/// allocator artifact moved: a transpose built and freed before a kernel that
/// never reads it raises glibc's dynamic mmap threshold, and the next call's
/// large allocations come from a different place. A time that changed while
/// this did not is not that effect; a time that changed with it may be.
fn minflt() -> i64 {
    let mut usage = Rusage { words: [0; 18] };
    // SAFETY: `getrusage` fills a `struct rusage`, whose Linux layout `Rusage`
    // reproduces; RUSAGE_SELF is 0 and covers every thread of this process.
    let code = unsafe { getrusage(0, &mut usage) };
    assert_eq!(code, 0, "getrusage(RUSAGE_SELF)");
    usage.words[8]
}

/// Whether the kernel this invocation will run reads the incoming adjacency.
///
/// PageRank's pull kernel is the only kernel in this matrix that does, and it
/// is selected only when a concurrency was requested and the work clears the
/// sequential floor in `grust-algorithms/src/parallel.rs`; below that floor
/// PageRank takes the push loop, which reads out-arcs alone. WCC, BFS and
/// triangles never read in-arcs at any width — checked in the kernels, not
/// inferred from their names — and triangles runs on an undirected projection,
/// whose rows already mirror, so there is nothing to build there in any case.
fn reads_incoming(algorithm: &str, concurrency: Option<usize>, nodes: usize, edges: usize) -> bool {
    algorithm == "pagerank"
        && concurrency.is_some()
        && nodes.saturating_add(edges).saturating_mul(2) >= 1 << 14
}

/// The binary's name without the `bench-` prefix: `grust` or `grust-next`.
fn participant() -> &'static str {
    env!("CARGO_BIN_NAME").strip_prefix("bench-").unwrap_or(env!("CARGO_BIN_NAME"))
}

/// The Grust commit this binary was linked against, passed in by the image
/// build. Both commits call themselves 0.22.0, so the version cannot say which.
fn grust_commit() -> &'static str {
    option_env!("GRUST_COMMIT").unwrap_or("unknown")
}

/// FNV-1a over each score's IEEE-754 bits, little-endian, in node order.
///
/// Bit identity is what licenses comparing two kernels' times, and a sum or a
/// maximum can agree while the vector does not. `parity.py` computes the same
/// function over the reference's scores, so the comparison is of every bit of
/// every score and not of a summary.
fn digest(values: &[f64]) -> String {
    let mut hash: u64 = 0xcbf2_9ce4_8422_2325;
    for value in values {
        for byte in value.to_bits().to_le_bytes() {
            hash ^= u64::from(byte);
            hash = hash.wrapping_mul(0x0000_0100_0000_01b3);
        }
    }
    format!("{hash:016x}")
}

fn read(path: &str) -> (usize, Vec<(usize, usize)>) {
    let text = std::fs::read_to_string(path).expect("fixture");
    let mut lines = text.lines();
    let mut header = lines.next().expect("header").split_whitespace();
    let nodes: usize = header.next().expect("nodes").parse().expect("nodes");
    let declared: usize = header.next().expect("edges").parse().expect("edges");
    let edges: Vec<(usize, usize)> = lines
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            let mut parts = line.split_whitespace();
            (parts.next().expect("source").parse().expect("source"),
             parts.next().expect("target").parse().expect("target"))
        })
        .collect();
    assert_eq!(edges.len(), declared, "fixture header disagrees with its body");
    (nodes, edges)
}

fn flag(args: &[String], name: &str) -> Option<String> {
    args.iter().position(|a| a == name).map(|i| args[i + 1].clone())
}

/// The accounting mode requested, and the label every output line carries.
#[cfg(feature = "accounting-api")]
fn accounting(args: &[String]) -> (Accounting, &'static str) {
    let mode = match flag(args, "--accounting").as_deref().unwrap_or("counted") {
        "counted" => Accounting::COUNTED,
        "work-uncounted" => Accounting::WORK_UNCOUNTED,
        "unchecked" => Accounting::UNCHECKED,
        other => panic!("unknown --accounting {other}: counted, work-uncounted or unchecked"),
    };
    (mode, mode.label())
}

/// The release has no opt-out: it always counts work and observes
/// cancellation, which is what the later commit calls `counted`. It accepts
/// `counted` and refuses anything else, rather than running counted under
/// another mode's name.
#[cfg(not(feature = "accounting-api"))]
fn accounting(args: &[String]) -> ((), &'static str) {
    match flag(args, "--accounting").as_deref().unwrap_or("counted") {
        "counted" => ((), "counted"),
        other => panic!("--accounting {other}: this Grust has no accounting opt-out, so only counted runs"),
    }
}

fn context(limits: ExecutionLimits, args: &[String]) -> ExecutionContext {
    #[cfg(feature = "accounting-api")]
    return ExecutionContext::with_accounting(limits, accounting(args).0).expect("execution context");
    #[cfg(not(feature = "accounting-api"))]
    {
        accounting(args);
        ExecutionContext::new(limits).expect("execution context")
    }
}

/// Counted work, or `null` where the mode did not count it. A zero would say
/// the kernel did nothing, which is a different claim.
fn work_units(context: &ExecutionContext) -> String {
    let usage = context.usage().expect("usage");
    #[cfg(feature = "accounting-api")]
    return usage.work_units.counted().map(|units| units.to_string()).unwrap_or_else(|| "null".into());
    #[cfg(not(feature = "accounting-api"))]
    usage.work_units.to_string()
}

/// Build the transpose now, inside the build timer, where grustcat's
/// constructor builds its own. Returns the milliseconds it took, or `None`
/// where this Grust cannot build it outside a kernel or was not asked to.
#[cfg(feature = "accounting-api")]
fn prepare_incoming(projection: &GraphProjection, wanted: bool) -> Option<f64> {
    if !wanted {
        return None;
    }
    let started = Instant::now();
    projection.prepare_incoming().expect("prepare_incoming");
    Some(started.elapsed().as_secs_f64() * 1e3)
}

/// The release has no `prepare_incoming`: its pull kernel builds the transpose
/// inside the first call that reads it, and nothing else builds one at all.
#[cfg(not(feature = "accounting-api"))]
fn prepare_incoming(_projection: &GraphProjection, _wanted: bool) -> Option<f64> {
    None
}

/// `--prepare-incoming needed` (the default) builds the transpose inside the
/// build timer only for a kernel that reads it; `always` builds it for every
/// algorithm, which is what B4 did and what this row exists to show.
///
/// The release cannot honour `always`, having no method to call, so it refuses
/// it rather than producing a row that silently means something else.
fn prepare_policy(args: &[String]) -> &'static str {
    match flag(args, "--prepare-incoming").as_deref().unwrap_or("needed") {
        "needed" => "needed",
        "always" if cfg!(feature = "accounting-api") => "always",
        "always" => panic!("--prepare-incoming always: this Grust has no prepare_incoming, so it \
                            cannot build the transpose outside a kernel"),
        other => panic!("unknown --prepare-incoming {other}: needed or always"),
    }
}

/// One kernel call: its time, the fields that identify its result, and a
/// value compared between the first and second call on the same projection.
struct Call {
    kernel_ms: f64,
    /// Minor page faults taken across the kernel call, read outside the timer.
    minflt: i64,
    fields: String,
    identity: String,
    materialise_ms: f64,
    /// PageRank's scores, kept only when `--scores-out` asks for them.
    scores: Option<Vec<f64>>,
}

/// `--scores-out PATH`: write every PageRank score's bits, one hex word per
/// line in node order, after both calls and outside every timer. Parity uses it
/// to compare each score with the reference's rather than a digest or a sum;
/// timed runs never pass it.
fn write_scores(path: &str, scores: &[f64]) {
    use std::fmt::Write as _;
    let mut text = String::with_capacity(scores.len() * 17);
    for score in scores {
        writeln!(text, "{:016x}", score.to_bits()).expect("format");
    }
    std::fs::write(path, text).expect("--scores-out");
}

fn call(projection: &GraphProjection, algorithm: &str, tolerance: f64, max_iterations: usize, keep: bool) -> Call {
    // Read before the timer starts and again after it stops: the counter is
    // reported beside the time, never inside it.
    let faults = minflt();
    let started = Instant::now();
    match algorithm {
        "pagerank" => {
            // `..Default::default()` because the later commit adds a `variant`
            // field whose default is PageRank; the release has no such field.
            #[allow(clippy::needless_update)]
            let options = PageRankOptions {
                damping: 0.85, tolerance, max_iterations, personalization: None,
                ..Default::default()
            };
            let result = pagerank(projection, options).expect("pagerank");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let faults = minflt() - faults;
            let started = Instant::now();
            let scores = result.values();
            let sum: f64 = scores.iter().sum();
            let (argmax, max) = scores.iter().enumerate()
                .fold((0usize, f64::MIN), |(bi, bv), (i, v)| if *v > bv { (i, *v) } else { (bi, bv) });
            let bits = digest(scores);
            Call {
                kernel_ms,
                minflt: faults,
                fields: format!("\"iterations\":{},\"residual\":{},\"converged\":{},\"sum\":{sum},\
                                 \"max\":{max},\"argmax\":{argmax},\"scores_digest\":\"{bits}\"",
                                result.iterations(), result.residual(), result.converged()),
                identity: format!("{bits}/{}", result.iterations()),
                materialise_ms: started.elapsed().as_secs_f64() * 1e3,
                scores: keep.then(|| scores.to_vec()),
            }
        }
        "wcc" => {
            let result = weakly_connected_components(projection).expect("wcc");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let faults = minflt() - faults;
            let started = Instant::now();
            let labels = result.values();
            let distinct: std::collections::HashSet<_> = labels.iter().collect();
            let identity = format!("{:?}", labels);
            Call {
                kernel_ms,
                minflt: faults,
                fields: format!("\"count\":{},\"probe_label\":{}", distinct.len(), labels[0]),
                identity,
                materialise_ms: started.elapsed().as_secs_f64() * 1e3,
                scores: None,
            }
        }
        "bfs" => {
            let result = bfs(projection, "0").expect("bfs");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let faults = minflt() - faults;
            let started = Instant::now();
            // Unreachable nodes carry positive infinity here and -1 in the
            // reference; both mean the same thing and neither enters the sum.
            let distances = result.values();
            let reached = distances.iter().filter(|hops| hops.is_finite()).count();
            let total: f64 = distances.iter().filter(|hops| hops.is_finite()).sum();
            Call {
                kernel_ms,
                minflt: faults,
                fields: format!("\"reached\":{reached},\"distance_sum\":{total}"),
                identity: digest(distances),
                materialise_ms: started.elapsed().as_secs_f64() * 1e3,
                scores: None,
            }
        }
        "triangles" => {
            let result = triangles(projection, TriangleOptions { max_degree: None }).expect("triangles");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let faults = minflt() - faults;
            Call {
                kernel_ms,
                minflt: faults,
                fields: format!("\"triangles\":{}", result.triangle_count()),
                identity: result.triangle_count().to_string(),
                materialise_ms: 0.0,
                scores: None,
            }
        }
        other => panic!("unknown algorithm {other}"),
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let (_, mode) = accounting(&args);
    let participant = participant();
    if args.iter().any(|a| a == "--receipt") {
        println!(
            "{{\"participant\":\"{participant}\",\"version\":\"{}\",\"commit\":\"{}\",\
              \"grust_commit\":\"{}\",\"precision\":\"f64\",\
              \"algorithms\":[\"pagerank\",\"wcc\",\"bfs\",\"triangles\"],\
              \"parallel\":\"sequential unless with_concurrency is requested\",\"width_capable\":true,\
              \"accounting\":\"{mode}\",\"accounting_selectable\":{},\"prepares_incoming\":{},\
              \"prepare_incoming_selectable\":{},\"minflt\":true,\"scores_out\":true}}",
            env!("CARGO_PKG_VERSION"), option_env!("BENCH_COMMIT").unwrap_or("unknown"), grust_commit(),
            cfg!(feature = "accounting-api"), cfg!(feature = "accounting-api"),
            cfg!(feature = "accounting-api"));
        return;
    }
    let fixture = flag(&args, "--fixture").expect("--fixture");
    let algorithm = flag(&args, "--algorithm").expect("--algorithm");
    let max_iterations: usize = flag(&args, "--max-iterations")
        .map(|v| v.parse().expect("--max-iterations")).unwrap_or(100);
    let tolerance: f64 = flag(&args, "--tolerance")
        .map(|v| v.parse().expect("--tolerance")).unwrap_or(1e-10);

    let started = Instant::now();
    let (nodes, edges) = read(&fixture);
    let parse_ms = started.elapsed().as_secs_f64() * 1e3;

    // Two distinct things could be called "sequential": concurrency unset, where
    // PageRank takes the push loop kept as the parallel path's oracle, and
    // concurrency 1, where it takes the pull kernel on one thread. They are
    // different algorithms, so the flag is explicit and the output records which.
    let concurrency: Option<usize> = flag(&args, "--concurrency").map(|v| v.parse().expect("--concurrency"));
    let prepare = prepare_policy(&args);
    let mut context = context(ExecutionLimits {
        memory_bytes: usize::MAX,
        work_units: usize::MAX,
        batch_rows: 1 << 16,
        deadline: None,
    }, &args);
    if let Some(workers) = concurrency {
        context = context.with_concurrency(workers).expect("concurrency");
    }

    let minflt_start = minflt();
    let started = Instant::now();
    let orientation = if algorithm == "triangles" { Orientation::Undirected } else { Orientation::Outgoing };
    let projection = GraphProjection::from_topology(
        SnapshotIdentity::new("fixture".into(), "r1".into(), "reader".into()).expect("identity"),
        (0..nodes).map(|node| format!("{node}").into()).collect(),
        edges.iter().enumerate()
            .map(|(ordinal, &(source, target))| ProjectionEdge { source, target, ordinal, id: None })
            .collect(),
        None,
        orientation,
        &context,
    )
    .expect("projection");
    // Inside the build timer, where grustcat's constructor builds its own, and
    // only for a kernel that reads it. B4 built it for every algorithm so that
    // the build column would be the same work as grustcat's constructor; what
    // that bought was a transpose WCC and BFS never read, built and freed just
    // before their first call, and an allocator in a state their v0.22.0 column
    // was not measured in. Matching a constructor is not worth measuring a
    // different process. `incoming_ms` says how much of `build_ms` it was; a
    // row that built nothing reports null and says so in `prepare_incoming`.
    let wanted = prepare == "always" || reads_incoming(&algorithm, concurrency, nodes, edges.len());
    let incoming_ms = prepare_incoming(&projection, wanted);
    let build_ms = started.elapsed().as_secs_f64() * 1e3;
    let minflt_build = minflt() - minflt_start;

    let scores_out = flag(&args, "--scores-out");
    let first = call(&projection, &algorithm, tolerance, max_iterations, scores_out.is_some());
    // Read after the first call, as B3 read it after its only call.
    let work = work_units(&context);
    let second = call(&projection, &algorithm, tolerance, max_iterations, false);
    // The second call is only a timing of the same computation if it is the
    // same computation. A difference is a defect, and exits non-zero so parity
    // records an error and the cell is never timed.
    assert_eq!(first.identity, second.identity, "second call on the same projection returned a different result");
    let peak_bytes = context.usage().expect("usage").peak_bytes;
    if let (Some(path), Some(scores)) = (&scores_out, &first.scores) {
        write_scores(path, scores);
    }

    println!("{{\"participant\":\"{participant}\",\"grust_commit\":\"{}\",\"accounting\":\"{mode}\",\
               \"algorithm\":\"{algorithm}\",\"fixture\":\"{fixture}\",\
               \"nodes\":{nodes},\"edges\":{},\"parse_ms\":{parse_ms},\"build_ms\":{build_ms},\
               \"incoming_ms\":{},\"prepare_incoming\":\"{prepare}\",\"reads_incoming\":{},\
               \"minflt_build\":{minflt_build},\"minflt_first\":{},\"minflt_second\":{},\
               \"kernel_ms\":{},\"kernel_second_ms\":{},\"second_identical\":true,{},\
               \"materialise_ms\":{},\"work_units\":{work},\"peak_bytes\":{peak_bytes},\"concurrency\":{}}}",
             grust_commit(), edges.len(),
             incoming_ms.map(|ms| ms.to_string()).unwrap_or_else(|| "null".into()),
             reads_incoming(&algorithm, concurrency, nodes, edges.len()),
             first.minflt, second.minflt,
             first.kernel_ms, second.kernel_ms, first.fields, first.materialise_ms,
             concurrency.map(|w| w.to_string()).unwrap_or_else(|| "null".into()));
}
