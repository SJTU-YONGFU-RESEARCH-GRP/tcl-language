# Third-party runtime and notices

Wacl upstream: https://github.com/ecky-l/wacl

Precompiled distribution: https://ecky-l.github.io/wacl/releases/wacl.zip (2017-05-29 files). It contains a Tcl 8.6 interpreter and bundled Tcl library/extensions. `wacl.wasm`, `wacl-library.data`, and `wacl-custom.data` are copied unmodified. The upstream zip SHA-256 and the local asset hashes are recorded below and in `SHA256.json`.

`wacl.js` has one compatibility change: replace `delete window.Module;` with `if(typeof window!=="undefined")delete window.Module;` to permit execution in a Web Worker. The application uses the exported Tcl C API instead of upstream's string-concatenating Eval wrapper. No claim is made that this is the latest Tcl release.

- Wacl: BSD-3-Clause, see `WACL-LICENSE`.
- Tcl and upstream components: see `TCL-LICENSE` and notices embedded in the Tcl library data; upstream source and build recipes are linked above.
- RequireJS 2.3.3: MIT, copyright and license URL are preserved at the start of `require.js`; https://github.com/requirejs/requirejs.
- Wacl's bundled extensions include tDOM, rl_json and selected Tcllib modules. They retain their upstream licenses and authorship; see https://github.com/ecky-l/wacl/tree/master/ext and the accompanying upstream license terms. The original author credits are not replaced by this project's MIT license.

All runtime files are hosted locally with the course; learners do not depend on a third-party CDN for execution. Update the runtime only after rerunning all native and WASM checks.
50d4ecb40c4db0448942332f9562c3cedc8bea38fa89d95ca5e5b9afcc5afb23  wacl.zip
