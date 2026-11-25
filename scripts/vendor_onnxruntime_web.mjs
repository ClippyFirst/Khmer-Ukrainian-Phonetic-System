#!/usr/bin/env node
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const version = "1.23.2";
const expectedIntegrity = "sha512-T09JUtMn+CZLk3mFwqiH0lgQf+4S7+oYHHtk6uhaYAAJI95bTcKi5bOOZYwORXfS/RLZCjDDEXGWIuOCAFlEjg==";
const root = path.resolve(process.argv[2] ?? "public/vendor/onnxruntime-web");
const temp = mkdtempSync(path.join(os.tmpdir(), "ort-web-"));
try {
  const packed = JSON.parse(execFileSync("npm", [
    "pack", "onnxruntime-web@" + version, "--json", "--pack-destination", temp,
  ], { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"] }));
  assert.equal(packed.length, 1);
  assert.equal(packed[0].integrity, expectedIntegrity, "onnxruntime-web tarball integrity changed");
  const archive = path.join(temp, packed[0].filename);
  execFileSync("tar", ["-xzf", archive, "-C", temp]);
  const dist = path.join(temp, "package", "dist");
  mkdirSync(root, { recursive: true });
  for (const filename of [
    "ort.wasm.min.mjs",
    "ort-wasm-simd-threaded.mjs",
    "ort-wasm-simd-threaded.wasm",
  ]) {
    copyFileSync(path.join(dist, filename), path.join(root, filename));
  }
  copyFileSync(path.join(temp, "package", "LICENSE"), path.join(root, "LICENSE"));
  const manifest = {
    package: "onnxruntime-web",
    version,
    integrity: expectedIntegrity,
    license: "MIT",
    files: ["ort.wasm.min.mjs", "ort-wasm-simd-threaded.mjs", "ort-wasm-simd-threaded.wasm", "LICENSE"],
  };
  await import("node:fs/promises").then(({ writeFile }) =>
    writeFile(path.join(root, "vendor-manifest.json"), JSON.stringify(manifest, null, 2) + "\n"));
  console.log("Vendored integrity-verified ONNX Runtime Web", version, "to", root);
} finally {
  rmSync(temp, { recursive: true, force: true });
}
