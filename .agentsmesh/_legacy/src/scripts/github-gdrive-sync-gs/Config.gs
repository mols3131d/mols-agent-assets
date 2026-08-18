const CONFIG = {
  GITHUB_OWNER: "mols3131d",
  GITHUB_REPO: "mols-agent-assets",
  BRANCH: "src-only",

  TARGET_FOLDER_ID:
    PropertiesService.getScriptProperties().getProperty("TARGET_FOLDER_ID"),
  GITHUB_TOKEN:
    PropertiesService.getScriptProperties().getProperty("GITHUB_TOKEN"),

  SYNC_INTERVAL_DAYS: 7,
  SYNC_RUN_HOUR: 4,

  IGNORE_RULES: ["**/scripts/**", "**/*.py", "**/*.sh"],

  DRY_RUN_DELETE: true,
  MAX_DELETE_PER_RUN: 20,
  MIN_EXPECTED_GITHUB_FILES: 1,
  SYNC_MARKER_FILENAME: ".github-drive-sync-marker",
};
