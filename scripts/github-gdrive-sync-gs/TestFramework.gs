const TestRunner = {
  currentSuite: "",
  results: [], // Array of { suite, name, status, elapsed, error }
  warnings: [], // Array of { suite, message }

  startSuite(suiteName) {
    this.currentSuite = suiteName;
    Logger.log("");
    Logger.log("========================================");
    Logger.log(`TEST SUITE START: ${suiteName}`);
    Logger.log("========================================");
  },

  run(testName, fn) {
    Logger.log(`TEST START: ${testName}`);
    const start = Date.now();
    try {
      fn();
      const elapsed = (Date.now() - start) / 1000;
      Logger.log(`TEST PASS: ${testName} (${elapsed.toFixed(3)}s)`);
      this.results.push({
        suite: this.currentSuite,
        name: testName,
        status: "PASS",
        elapsed: elapsed,
      });
    } catch (error) {
      const elapsed = (Date.now() - start) / 1000;
      Logger.log(`TEST FAIL: ${testName} / ${error.message}`);
      this.results.push({
        suite: this.currentSuite,
        name: testName,
        status: "FAIL",
        elapsed: elapsed,
        error: error,
      });
    }
  },

  warn(message) {
    Logger.log(`TEST WARN: ${message}`);
    this.warnings.push({
      suite: this.currentSuite,
      message: message,
    });
  },

  printSummary() {
    const total = this.results.length;
    const passed = this.results.filter((r) => r.status === "PASS").length;
    const failed = this.results.filter((r) => r.status === "FAIL");
    const warnings = this.warnings.length;

    Logger.log("");
    Logger.log("########################################");
    Logger.log("TEST RUN RESULTS SUMMARY");
    Logger.log("########################################");

    // Group by suite
    const suites = {};
    this.results.forEach((r) => {
      if (!suites[r.suite]) suites[r.suite] = [];
      suites[r.suite].push(r);
    });

    Object.keys(suites).forEach((suiteName) => {
      Logger.log(`\n[Suite] ${suiteName}`);
      suites[suiteName].forEach((r) => {
        const statusSymbol = r.status === "PASS" ? "✓" : "✗";
        Logger.log(
          `  ${statusSymbol} [${r.status}] ${r.name} (${r.elapsed.toFixed(3)}s)`,
        );
        if (r.error) {
          Logger.log(`      Error: ${r.error.message}`);
          if (r.error.stack) {
            Logger.log(`      Stack: ${r.error.stack}`);
          }
        }
      });
    });

    if (this.warnings.length > 0) {
      Logger.log("\n[Warnings]");
      this.warnings.forEach((w) => {
        Logger.log(`  ! [WARN] (${w.suite}) ${w.message}`);
      });
    }

    const totalTime = this.results.reduce((sum, r) => sum + r.elapsed, 0);

    Logger.log("");
    Logger.log("----------------------------------------");
    Logger.log(
      `Suites: ${Object.keys(suites).length} | Tests: ${total} | Passed: ${passed} | Failed: ${failed.length} | Warnings: ${warnings}`,
    );
    Logger.log(`Total Time: ${totalTime.toFixed(3)}s`);
    Logger.log("########################################");
    Logger.log("");

    if (failed.length > 0) {
      const failedNames = failed.map((f) => `${f.suite}.${f.name}`).join(", ");
      throw new Error(`일부 테스트 케이스가 실패했습니다: ${failedNames}`);
    }
  },
};

// --- Global Assertion Helpers ---

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(
      `ASSERT_EQUAL_FAILED: ${message}\nexpected=${expected}\nactual=${actual}`,
    );
  }
}

function assertTrue(condition, message) {
  if (!condition) {
    throw new Error(`ASSERT_TRUE_FAILED: ${message}`);
  }
}

function assertFalse(condition, message) {
  if (condition) {
    throw new Error(`ASSERT_FALSE_FAILED: ${message}`);
  }
}

function assertThrows(fn, message) {
  let thrown = false;
  try {
    fn();
  } catch (error) {
    thrown = true;
    Logger.log(`Expected error caught: ${error.message}`);
  }
  if (!thrown) {
    throw new Error(`ASSERT_THROWS_FAILED: ${message}`);
  }
}
