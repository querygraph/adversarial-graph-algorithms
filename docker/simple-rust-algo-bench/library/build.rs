//! Record the dependency versions the binary was actually linked against.
fn main() {
    let lock = std::fs::read_to_string("Cargo.lock")
        .or_else(|_| std::fs::read_to_string("../../../Cargo.lock"))
        .unwrap_or_default();
    for (crate_name, variable) in [("graph", "GRAPH_VERSION"), ("graph_builder", "GRAPH_BUILDER_VERSION")] {
        let needle = format!("name = \"{crate_name}\"\nversion = \"");
        let found = lock.split(&needle).nth(1)
            .and_then(|rest| rest.split('"').next()).unwrap_or("unknown").to_string();
        println!("cargo:rustc-env={variable}={found}");
    }
    println!("cargo:rerun-if-changed=Cargo.lock");
}
