function syncGithubToGDrive() {
  Logger.log("동기화 프로세스 시작...");

  try {
    validateConfig();

    const config = CONFIG;

    const github = createGithubClient(config);
    const drive = createDriveClient(config);

    drive.validateSyncMarker();

    const tree = github.getTree(config.BRANCH);

    const manifest = splitGithubTree(tree, config.IGNORE_RULES);

    syncFoldersToDrive(drive, manifest.folders);

    syncFilesToDrive(github, drive, manifest.files, config.BRANCH);

    drive.trashFilesNotInManifest(manifest.filePaths);

    Logger.log("동기화 프로세스가 성공적으로 완료되었습니다.");
  } catch (error) {
    Logger.log(`동기화 프로세스 실패: ${error.message}`);
    if (error.context) {
      Logger.log(`에러 컨텍스트: ${JSON.stringify(error.context)}`);
    }
    throw error;
  }
}

function createGithubClient(config = CONFIG) {
  return new GithubClient({
    owner: config.GITHUB_OWNER,
    repo: config.GITHUB_REPO,
    token: config.GITHUB_TOKEN,
  });
}

function createDriveClient(config = CONFIG) {
  return new DriveClient({
    targetFolderId: config.TARGET_FOLDER_ID,
    config,
    isIgnoredPath,
  });
}

function setupTrigger() {
  Logger.log("설정 검사 중...");
  validateConfig();

  Logger.log("트리거 설정 시작...");

  deleteExistingSyncTriggers();

  const days = Number(CONFIG.SYNC_INTERVAL_DAYS);
  const hour = Number(CONFIG.SYNC_RUN_HOUR);
  const nextHour = (hour + 1) % 24;

  ScriptApp.newTrigger("syncGithubToGDrive")
    .timeBased()
    .everyDays(days)
    .atHour(hour)
    .create();

  Logger.log(
    `트리거 등록 완료: [${days}일]마다 [${hour}시 ~ ${nextHour}시 사이]에 자동 실행됩니다.`,
  );
}

function deleteExistingSyncTriggers() {
  const triggers = ScriptApp.getProjectTriggers();

  triggers.forEach((trigger) => {
    if (trigger.getHandlerFunction() === "syncGithubToGDrive") {
      ScriptApp.deleteTrigger(trigger);
      Logger.log("기존 트리거 제거 완료.");
    }
  });
}
