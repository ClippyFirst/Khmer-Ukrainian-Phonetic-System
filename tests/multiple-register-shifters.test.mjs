import assert from "node:assert/strict";
import { parseSyllable } from "../src/khmer-engine-core.js";

// Multiple register shifters are structurally ambiguous; do not guess a register.
const result = parseSyllable("ប៉៊");
assert.equal(result.status, "EVIDENCE_LIMITED");
assert.equal(result.register_rule, "MULTIPLE_REGISTER_SHIFTERS");
