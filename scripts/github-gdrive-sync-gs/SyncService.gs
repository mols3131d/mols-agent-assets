function splitGithubTree(tree, ignoreRules = CONFIG.IGNORE_RULES) {
  if (!Array.isArray(tree)) {
    throw new Error("GitHub tree 처리 오류: tree는 배열이어야 합니다.");
  }

  const filteredTree = tree.filter((item) => {
    return item && item.path && !isIgnoredPath(item.path, ignoreRules);
  });

  const folders = filteredTree
    .filter((item) => item.type === "tree")
    .sort((a, b) => a.path.localeCompare(b.path));

  const files = filteredTree.filter((item) => item.type === "blob");

  return {
    folders,
    files,
    filePaths: new Set(files.map((file) => file.path)),
  };
}

function syncFoldersToDrive(drive, folders) {
  folders.forEach((folder) => {
    drive.ensureFolder(folder.path);
  });
}

function syncFilesToDrive(github, drive, files, branch) {
  files.forEach((file) => {
    syncSingleFileToDrive(github, drive, file, branch);
  });
}

function syncSingleFileToDrive(github, drive, file, branch) {
  const { parentPath, filename } = splitFilePath(file.path);

  const parentFolder = drive.ensureFolder(parentPath);

  const existingFile = drive.getFileSha(parentFolder, filename);

  if (existingFile && existingFile.sha === file.sha) {
    drive.trashDuplicateFiles(parentFolder, filename, existingFile.id);

    Logger.log(`스킵됨 (변경 없음): ${file.path}`);

    return;
  }

  const fileBlob = github.downloadFileBlob(file.path, branch, filename);

  drive.saveFile(parentFolder, filename, fileBlob, file.sha);

  if (existingFile) {
    Logger.log(`업데이트 완료 (변경 감지): ${file.path}`);
  } else {
    Logger.log(`신규 파일 저장 완료: ${file.path}`);
  }
}
