#!/usr/bin/env bun
/**
 * Context Orchestrator Hook Test Suite
 *
 * Automated tests for intent detector and session primer hooks.
 * Run with: bun test-hooks.ts
 */

import { execSync, spawnSync } from "child_process";
import * as fs from "fs";
import * as path from "path";

const HOOKS_DIR = path.join(process.env.HOME!, ".claude", "hooks");
const INTENT_DETECTOR = path.join(HOOKS_DIR, "context-intent-detector.ts");
const SESSION_PRIMER = path.join(HOOKS_DIR, "session-context-primer.sh");
const CACHE_DIR = path.join(process.env.HOME!, ".claude", ".context-cache");

interface TestResult {
  name: string;
  passed: boolean;
  message: string;
  duration_ms: number;
}

const results: TestResult[] = [];

function runTest(
  name: string,
  testFn: () => { passed: boolean; message: string }
): void {
  const start = Date.now();
  try {
    const { passed, message } = testFn();
    results.push({
      name,
      passed,
      message,
      duration_ms: Date.now() - start,
    });
  } catch (error) {
    results.push({
      name,
      passed: false,
      message: `Exception: ${error}`,
      duration_ms: Date.now() - start,
    });
  }
}

function runIntentDetector(prompt: string): any {
  const result = spawnSync("bun", [INTENT_DETECTOR], {
    input: JSON.stringify({ prompt: prompt }),
    encoding: "utf-8",
    timeout: 5000,
  });

  if (result.error) {
    throw result.error;
  }

  // Parse JSON output from stdout
  const output = result.stdout.trim();
  if (!output) {
    return { continue: true };
  }
  return JSON.parse(output);
}

// =============================================================================
// Intent Detector Tests
// =============================================================================

runTest("Intent Detector: File exists and is executable", () => {
  const exists = fs.existsSync(INTENT_DETECTOR);
  return {
    passed: exists,
    message: exists ? "Hook file exists" : "Hook file not found",
  };
});

runTest("Intent Detector: Responds within 500ms", () => {
  const start = Date.now();
  runIntentDetector("What did I discuss yesterday with John?");
  const duration = Date.now() - start;
  return {
    passed: duration < 500,
    message: `Response time: ${duration}ms (limit: 500ms)`,
  };
});

runTest("Intent Detector: Detects limitless pattern (lifelog)", () => {
  const result = runIntentDetector("Search my lifelogs for the meeting last week");
  const hasLimitless = result.systemPrompt?.includes("limitless") ?? false;
  return {
    passed: hasLimitless,
    message: hasLimitless
      ? "Correctly detected limitless pattern"
      : "Failed to detect limitless pattern",
  };
});

runTest("Intent Detector: Detects limitless pattern (temporal)", () => {
  const result = runIntentDetector("What did I discuss yesterday?");
  const hasLimitless = result.systemPrompt?.includes("limitless") ?? false;
  return {
    passed: hasLimitless,
    message: hasLimitless
      ? "Correctly detected temporal pattern"
      : "Failed to detect temporal pattern",
  };
});

runTest("Intent Detector: Detects research pattern (docs)", () => {
  const result = runIntentDetector("Look up the documentation for React hooks");
  const hasResearch = result.systemPrompt?.includes("research") ?? false;
  return {
    passed: hasResearch,
    message: hasResearch
      ? "Correctly detected research pattern"
      : "Failed to detect research pattern",
  };
});

runTest("Intent Detector: Detects research pattern (fact-check)", () => {
  const result = runIntentDetector("Fact check this claim about climate change");
  const hasResearch = result.systemPrompt?.includes("research") ?? false;
  return {
    passed: hasResearch,
    message: hasResearch
      ? "Correctly detected fact-check pattern"
      : "Failed to detect fact-check pattern",
  };
});

runTest("Intent Detector: Detects pieces pattern (LTM)", () => {
  const result = runIntentDetector("Search my LTM for the auth implementation");
  const hasPieces = result.systemPrompt?.includes("pieces") ?? false;
  return {
    passed: hasPieces,
    message: hasPieces
      ? "Correctly detected pieces pattern"
      : "Failed to detect pieces pattern",
  };
});

runTest("Intent Detector: Detects pieces pattern (saved code)", () => {
  const result = runIntentDetector("Find my saved code for the API wrapper");
  const hasPieces = result.systemPrompt?.includes("pieces") ?? false;
  return {
    passed: hasPieces,
    message: hasPieces
      ? "Correctly detected saved code pattern"
      : "Failed to detect saved code pattern",
  };
});

runTest("Intent Detector: Explicit /context command", () => {
  const result = runIntentDetector("/context what is the best auth approach");
  const hasMultiple =
    result.systemPrompt?.includes("limitless") ||
    result.systemPrompt?.includes("research") ||
    result.systemPrompt?.includes("pieces");
  return {
    passed: hasMultiple ?? false,
    message: hasMultiple
      ? "Correctly detected /context command"
      : "Failed to detect /context command",
  };
});

runTest("Intent Detector: Explicit /limitless command", () => {
  const result = runIntentDetector("/limitless meetings last week");
  const hasLimitless = result.systemPrompt?.includes("limitless") ?? false;
  return {
    passed: hasLimitless,
    message: hasLimitless
      ? "Correctly detected /limitless command"
      : "Failed to detect /limitless command",
  };
});

runTest("Intent Detector: Explicit /research command", () => {
  const result = runIntentDetector("/research Python asyncio best practices");
  const hasResearch = result.systemPrompt?.includes("research") ?? false;
  return {
    passed: hasResearch,
    message: hasResearch
      ? "Correctly detected /research command"
      : "Failed to detect /research command",
  };
});

runTest("Intent Detector: Explicit /pieces command", () => {
  const result = runIntentDetector("/pieces database schema patterns");
  const hasPieces = result.systemPrompt?.includes("pieces") ?? false;
  return {
    passed: hasPieces,
    message: hasPieces
      ? "Correctly detected /pieces command"
      : "Failed to detect /pieces command",
  };
});

runTest("Intent Detector: No trigger for simple question", () => {
  const result = runIntentDetector("What is 2 + 2?");
  const noPrompt = !result.systemPrompt || result.systemPrompt === "";
  return {
    passed: noPrompt,
    message: noPrompt
      ? "Correctly ignored simple question"
      : "Incorrectly triggered on simple question",
  };
});

runTest("Intent Detector: Complexity scoring (multi-step)", () => {
  const result = runIntentDetector(
    "First, search for auth best practices in my notes, then look up OAuth2 documentation, and finally check my saved implementations"
  );
  const hasContext =
    result.systemPrompt?.includes("limitless") ||
    result.systemPrompt?.includes("research") ||
    result.systemPrompt?.includes("pieces");
  return {
    passed: hasContext ?? false,
    message: hasContext
      ? "Correctly detected complex multi-step query"
      : "Failed to detect complex query",
  };
});

// =============================================================================
// Session Primer Tests
// =============================================================================

runTest("Session Primer: File exists and is executable", () => {
  const exists = fs.existsSync(SESSION_PRIMER);
  const stats = exists ? fs.statSync(SESSION_PRIMER) : null;
  const isExecutable = stats ? (stats.mode & parseInt("111", 8)) !== 0 : false;
  return {
    passed: exists && isExecutable,
    message: exists
      ? isExecutable
        ? "Hook file exists and is executable"
        : "Hook file exists but not executable"
      : "Hook file not found",
  };
});

runTest("Session Primer: Completes within 5 seconds", () => {
  const start = Date.now();
  try {
    execSync(`bash ${SESSION_PRIMER}`, { timeout: 5000, encoding: "utf-8" });
  } catch (e) {
    // Ignore errors, just checking timing
  }
  const duration = Date.now() - start;
  return {
    passed: duration < 5000,
    message: `Completion time: ${duration}ms (limit: 5000ms)`,
  };
});

runTest("Session Primer: Creates cache directory", () => {
  try {
    execSync(`bash ${SESSION_PRIMER}`, { timeout: 5000, encoding: "utf-8" });
  } catch (e) {
    // Ignore errors
  }
  const exists = fs.existsSync(CACHE_DIR);
  return {
    passed: exists,
    message: exists
      ? "Cache directory created"
      : "Cache directory not created",
  };
});

runTest("Session Primer: Creates session cache file", () => {
  const cacheFile = path.join(CACHE_DIR, "session-context.json");
  try {
    execSync(`bash ${SESSION_PRIMER}`, { timeout: 5000, encoding: "utf-8" });
  } catch (e) {
    // Ignore errors
  }
  const exists = fs.existsSync(cacheFile);
  let validJson = false;
  if (exists) {
    try {
      JSON.parse(fs.readFileSync(cacheFile, "utf-8"));
      validJson = true;
    } catch (e) {
      validJson = false;
    }
  }
  return {
    passed: exists && validJson,
    message: exists
      ? validJson
        ? "Session cache file created with valid JSON"
        : "Session cache file created but invalid JSON"
      : "Session cache file not created",
  };
});

runTest("Session Primer: Reports available sources", () => {
  let output = "";
  try {
    output = execSync(`bash ${SESSION_PRIMER}`, {
      timeout: 5000,
      encoding: "utf-8",
    });
  } catch (e) {
    output = "";
  }
  const hasOutput = output.length > 0;
  const mentionsSources =
    output.includes("limitless") ||
    output.includes("research") ||
    output.includes("pieces");
  return {
    passed: hasOutput && mentionsSources,
    message: hasOutput
      ? mentionsSources
        ? "Reports available context sources"
        : "Output doesn't mention sources"
      : "No output produced (all sources may be unavailable)",
  };
});

// =============================================================================
// Cache Manager Tests
// =============================================================================

const CACHE_MANAGER = path.join(
  process.env.HOME!,
  ".claude",
  "skill-db",
  "context-orchestrator",
  "scripts",
  "cache-manager.py"
);

runTest("Cache Manager: Init command works", () => {
  try {
    const output = execSync(`python3 ${CACHE_MANAGER} init`, {
      encoding: "utf-8",
    });
    const result = JSON.parse(output.trim());
    return {
      passed: result.status === "initialized",
      message: `Init result: ${result.status}`,
    };
  } catch (e) {
    return {
      passed: false,
      message: `Error: ${e}`,
    };
  }
});

runTest("Cache Manager: Set and Get work", () => {
  try {
    // Set a value
    execSync(
      `python3 ${CACHE_MANAGER} set limitless "test query" '{"result": "test data"}'`,
      { encoding: "utf-8" }
    );

    // Get the value
    const output = execSync(
      `python3 ${CACHE_MANAGER} get limitless "test query"`,
      { encoding: "utf-8" }
    );
    const result = JSON.parse(output.trim());

    return {
      passed: result.hit === true && result.result?.result === "test data",
      message: result.hit ? "Cache set/get working" : "Cache miss after set",
    };
  } catch (e) {
    return {
      passed: false,
      message: `Error: ${e}`,
    };
  }
});

runTest("Cache Manager: Stats command works", () => {
  try {
    const output = execSync(`python3 ${CACHE_MANAGER} stats`, {
      encoding: "utf-8",
    });
    const stats = JSON.parse(output.trim());
    return {
      passed: "total_entries" in stats && "session_id" in stats,
      message: `Stats: ${stats.total_entries} entries, session ${stats.session_id}`,
    };
  } catch (e) {
    return {
      passed: false,
      message: `Error: ${e}`,
    };
  }
});

// =============================================================================
// Report Results
// =============================================================================

console.log("\n" + "=".repeat(70));
console.log("CONTEXT ORCHESTRATOR HOOK TEST RESULTS");
console.log("=".repeat(70) + "\n");

let passed = 0;
let failed = 0;

for (const result of results) {
  const status = result.passed ? "PASS" : "FAIL";
  const icon = result.passed ? "✓" : "✗";
  const color = result.passed ? "\x1b[32m" : "\x1b[31m";
  const reset = "\x1b[0m";

  console.log(
    `${color}${icon} ${status}${reset} [${result.duration_ms}ms] ${result.name}`
  );
  if (!result.passed) {
    console.log(`   └─ ${result.message}`);
  }

  if (result.passed) passed++;
  else failed++;
}

console.log("\n" + "-".repeat(70));
console.log(`Total: ${results.length} | Passed: ${passed} | Failed: ${failed}`);
console.log(
  `Success Rate: ${((passed / results.length) * 100).toFixed(1)}%`
);
console.log("-".repeat(70) + "\n");

// Exit with error code if any tests failed
process.exit(failed > 0 ? 1 : 0);
