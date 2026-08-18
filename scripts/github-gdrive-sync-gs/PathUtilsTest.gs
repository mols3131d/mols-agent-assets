function PathUtilsTest_normalizePath() {
  TestRunner.run("PathUtils.normalizePath", () => {
    assertEqual(
      normalizePath("/src/index.js/"),
      "src/index.js",
      "should trim leading and trailing slashes",
    );

    assertEqual(
      normalizePath(""),
      "",
      "empty path should remain empty",
    );

    assertEqual(
      normalizePath(null),
      "",
      "null path should become empty string",
    );
  });
}

function PathUtilsTest_splitFilePath() {
  TestRunner.run("PathUtils.splitFilePath", () => {
    const nested = splitFilePath("/src/app/index.js");

    assertEqual(
      nested.filename,
      "index.js",
      "filename should be extracted",
    );

    assertEqual(
      nested.parentPath,
      "src/app",
      "parentPath should be extracted",
    );

    const root = splitFilePath("README.md");

    assertEqual(
      root.filename,
      "README.md",
      "root filename should be extracted",
    );

    assertEqual(
      root.parentPath,
      "",
      "root parentPath should be empty",
    );
  });
}

function PathUtilsTest_globToRegex() {
  TestRunner.run("PathUtils.globToRegex", () => {
    const rootLogRegex = globToRegex("*.log");

    assertTrue(
      rootLogRegex.test("error.log"),
      "*.log should match root log file",
    );

    assertFalse(
      rootLogRegex.test("logs/error.log"),
      "*.log should not match nested log file",
    );

    const nestedLogRegex = globToRegex("**/*.log");

    assertTrue(
      nestedLogRegex.test("logs/error.log"),
      "**/*.log should match nested log file",
    );

    assertFalse(
      nestedLogRegex.test("error.log"),
      "**/*.log does not match root log file in this matcher",
    );
  });
}

function PathUtilsTest_isIgnoredPath() {
  TestRunner.run("PathUtils.isIgnoredPath", () => {
    const rules = [
      ".github-drive-sync-marker",
      ".github/**",
      "node_modules/**",
      "dist/**",
      "*.log",
      "**/*.log",
      ".DS_Store",
      "**/.DS_Store",
    ];

    assertTrue(
      isIgnoredPath(".github-drive-sync-marker", rules),
      "marker file should be ignored",
    );

    assertTrue(
      isIgnoredPath(".github/workflows/deploy.yml", rules),
      ".github/** should be ignored",
    );

    assertTrue(
      isIgnoredPath("node_modules/pkg/index.js", rules),
      "node_modules/** should be ignored",
    );

    assertTrue(
      isIgnoredPath("dist/app.js", rules),
      "dist/** should be ignored",
    );

    assertTrue(
      isIgnoredPath("error.log", rules),
      "*.log should match root log file",
    );

    assertTrue(
      isIgnoredPath("logs/error.log", rules),
      "**/*.log should match nested log file",
    );

    assertTrue(
      isIgnoredPath(".DS_Store", rules),
      ".DS_Store should match root file",
    );

    assertTrue(
      isIgnoredPath("src/.DS_Store", rules),
      "**/.DS_Store should match nested file",
    );

    assertFalse(
      isIgnoredPath("src/index.js", rules),
      "normal source file should not be ignored",
    );
  });
}

function PathUtilsTest_all() {
  PathUtilsTest_normalizePath();
  PathUtilsTest_splitFilePath();
  PathUtilsTest_globToRegex();
  PathUtilsTest_isIgnoredPath();
}
