function MainTest_createValidConfig(overrides = {}) {
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

function MainTest_createGithubClient() {
  TestRunner.run("Main.createGithubClient", () => {
    const client = createGithubClient(
      MainTest_createValidConfig({
        GITHUB_OWNER: "test-owner",
        GITHUB_REPO: "test-repo",
        GITHUB_TOKEN: "test-token",
      }),
    );

    assertEqual(
      client.owner,
      "test-owner",
      "GithubClient owner should match config",
    );

    assertEqual(
      client.repo,
      "test-repo",
      "GithubClient repo should match config",
    );

    assertEqual(
      client.token,
      "test-token",
      "GithubClient token should match config",
    );
  });
}

function MainTest_all() {
  MainTest_createGithubClient();
}
