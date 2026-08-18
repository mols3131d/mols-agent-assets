function ValidationTest_createValidConfig(overrides = {}) {
  return Object.assign(
    {
      TARGET_FOLDER_ID: "drive-folder-id",
      GITHUB_OWNER: "owner",
      GITHUB_REPO: "repo",
      GITHUB_TOKEN: "token",
      BRANCH: "main",
      SYNC_INTERVAL_DAYS: 7,
      SYNC_RUN_HOUR: 4,
      IGNORE_RULES: [
        ".github-drive-sync-marker",
        ".git/**",
        ".github/**",
        "node_modules/**",
        "dist/**",
        "build/**",
        "*.log",
        "**/*.log",
        ".DS_Store",
        "**/.DS_Store",
      ],
      DRY_RUN_DELETE: true,
      MAX_DELETE_PER_RUN: 20,
      MIN_EXPECTED_GITHUB_FILES: 1,
      SYNC_MARKER_FILENAME: ".github-drive-sync-marker",
    },
    overrides,
  );
}

function ValidationTest_validateConfig_success() {
  TestRunner.run("Validation.validateConfig success", () => {
    validateConfig(ValidationTest_createValidConfig());
  });
}

function ValidationTest_validateConfig_requiredFields() {
  TestRunner.run("Validation.validateConfig required fields", () => {
    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          TARGET_FOLDER_ID: "",
        }),
      );
    }, "empty TARGET_FOLDER_ID should throw");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          GITHUB_OWNER: "",
        }),
      );
    }, "empty GITHUB_OWNER should throw");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          GITHUB_REPO: "",
        }),
      );
    }, "empty GITHUB_REPO should throw");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          BRANCH: "",
        }),
      );
    }, "empty BRANCH should throw");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          SYNC_MARKER_FILENAME: "",
        }),
      );
    }, "empty SYNC_MARKER_FILENAME should throw");
  });
}

function ValidationTest_validateConfig_numericFields() {
  TestRunner.run("Validation.validateConfig numeric fields", () => {
    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          SYNC_INTERVAL_DAYS: 0,
        }),
      );
    }, "SYNC_INTERVAL_DAYS must be positive");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          SYNC_RUN_HOUR: 24,
        }),
      );
    }, "SYNC_RUN_HOUR must be <= 23");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          MAX_DELETE_PER_RUN: -1,
        }),
      );
    }, "MAX_DELETE_PER_RUN must be non-negative");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          MIN_EXPECTED_GITHUB_FILES: 0,
        }),
      );
    }, "MIN_EXPECTED_GITHUB_FILES must be positive");
  });
}

function ValidationTest_validateConfig_typeFields() {
  TestRunner.run("Validation.validateConfig type fields", () => {
    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          IGNORE_RULES: "not-array",
        }),
      );
    }, "IGNORE_RULES must be array");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          DRY_RUN_DELETE: "true",
        }),
      );
    }, "DRY_RUN_DELETE must be boolean");

    assertThrows(() => {
      validateConfig(
        ValidationTest_createValidConfig({
          TARGET_FOLDER_ID: "YOUR_GOOGLE_DRIVE_FOLDER_ID",
        }),
      );
    }, "placeholder TARGET_FOLDER_ID should throw");
  });
}

function ValidationTest_all() {
  ValidationTest_validateConfig_success();
  ValidationTest_validateConfig_requiredFields();
  ValidationTest_validateConfig_numericFields();
  ValidationTest_validateConfig_typeFields();
}
