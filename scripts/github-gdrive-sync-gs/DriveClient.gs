class DriveClient {
  constructor(options) {
    if (!options || !options.targetFolderId) {
      throw new Error('DriveClient 설정 오류: targetFolderId는 필수입니다.');
    }

    this.driveApp = options.driveApp || DriveApp;
    this.urlFetchApp = options.urlFetchApp || UrlFetchApp;
    this.scriptApp = options.scriptApp || ScriptApp;
    this.config = options.config || CONFIG;
    this.isIgnoredPath = options.isIgnoredPath || isIgnoredPath;
    this.logger = options.logger || Logger;

    this.rootFolder = this.driveApp.getFolderById(options.targetFolderId);
    this.folderCache = {
      '': this.rootFolder
    };
  }

  ensureFolder(path) {
    const normalizedPath = this.normalizePath(path);

    if (!normalizedPath) {
      return this.rootFolder;
    }

    if (this.folderCache[normalizedPath]) {
      return this.folderCache[normalizedPath];
    }

    const parts = normalizedPath.split('/');
    const folderName = parts.pop();
    const parentPath = parts.join('/');
    const parentFolder = this.ensureFolder(parentPath);

    let folder = this.getSubFolder(parentFolder, folderName);

    if (!folder) {
      folder = parentFolder.createFolder(folderName);
      this.logger.log(`폴더 생성 완료: ${normalizedPath}`);
    }

    this.folderCache[normalizedPath] = folder;

    return folder;
  }

  getSubFolder(parentFolder, name) {
    const folders = parentFolder.getFoldersByName(name);
    return folders.hasNext() ? folders.next() : null;
  }

  getFileSha(parentFolder, filename) {
    const file = this.getFirstFileByName(parentFolder, filename);

    if (!file) {
      return null;
    }

    return {
      id: file.getId(),
      sha: file.getDescription()
    };
  }

  getFirstFileByName(parentFolder, filename) {
    const files = parentFolder.getFilesByName(filename);
    return files.hasNext() ? files.next() : null;
  }

  trashDuplicateFiles(parentFolder, filename, keepFileId) {
    const files = parentFolder.getFilesByName(filename);
    let trashedCount = 0;

    while (files.hasNext()) {
      const file = files.next();

      if (file.getId() !== keepFileId) {
        file.setTrashed(true);
        trashedCount += 1;
        this.logger.log(`중복 파일 제거됨: ${filename}`);
      }
    }

    return trashedCount;
  }

  saveFile(parentFolder, filename, fileBlob, sha) {
    if (!parentFolder) {
      throw new Error('DriveClient 오류: parentFolder는 필수입니다.');
    }

    if (!filename) {
      throw new Error('DriveClient 오류: filename은 필수입니다.');
    }

    if (!fileBlob) {
      throw new Error('DriveClient 오류: fileBlob은 필수입니다.');
    }

    if (!sha) {
      throw new Error('DriveClient 오류: sha는 필수입니다.');
    }

    const existingFile = this.getFirstFileByName(parentFolder, filename);

    if (existingFile) {
      this.updateFileContent(existingFile, filename, fileBlob);
      existingFile.setDescription(sha);

      this.trashDuplicateFiles(
        parentFolder,
        filename,
        existingFile.getId()
      );

      this.logger.log(`기존 파일 내용 덮어쓰기 완료: ${filename}`);

      return existingFile;
    }

    const file = parentFolder.createFile(fileBlob);
    file.setDescription(sha);

    this.logger.log(`신규 파일 생성 완료: ${filename}`);

    return file;
  }

  updateFileContent(file, filename, fileBlob) {
    const uploadUrl = this.buildUploadUrl(file.getId());

    const response = this.urlFetchApp.fetch(uploadUrl, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${this.scriptApp.getOAuthToken()}`
      },
      payload: fileBlob,
      muteHttpExceptions: true
    });

    const status = response.getResponseCode();

    if (status < 200 || status >= 300) {
      throw new Error(
        `파일 본문 업데이트 실패 (${filename}): HTTP ${status} / ${response.getContentText()}`
      );
    }

    return response;
  }

  buildUploadUrl(fileId) {
    if (!fileId) {
      throw new Error('DriveClient 오류: fileId는 필수입니다.');
    }

    return `https://www.googleapis.com/upload/drive/v3/files/${encodeURIComponent(fileId)}?uploadType=media`;
  }

  validateSyncMarker() {
    const markerName = this.config.SYNC_MARKER_FILENAME;

    if (!markerName) {
      throw new Error('설정 오류: SYNC_MARKER_FILENAME이 설정되지 않았습니다.');
    }

    const marker = this.getFirstFileByName(this.rootFolder, markerName);

    if (!marker) {
      throw new Error(
        `안전 중단: Drive 대상 폴더에 marker 파일이 없습니다. ` +
        `대상 폴더 root에 "${markerName}" 파일을 생성하세요.`
      );
    }

    this.logger.log(`Drive marker 확인 완료: ${markerName}`);

    return marker;
  }

  listFilesRecursive(folder = this.rootFolder, basePath = '') {
    const results = [];
    const normalizedBasePath = this.normalizePath(basePath);

    const files = folder.getFiles();

    while (files.hasNext()) {
      const file = files.next();

      const path = normalizedBasePath
        ? `${normalizedBasePath}/${file.getName()}`
        : file.getName();

      results.push({
        type: 'file',
        path,
        file
      });
    }

    const folders = folder.getFolders();

    while (folders.hasNext()) {
      const childFolder = folders.next();

      const folderPath = normalizedBasePath
        ? `${normalizedBasePath}/${childFolder.getName()}`
        : childFolder.getName();

      results.push(
        ...this.listFilesRecursive(childFolder, folderPath)
      );
    }

    return results;
  }

  getDeleteTargets(validFilePaths) {
    this.validateManifest(validFilePaths);

    const markerFilename = this.config.SYNC_MARKER_FILENAME;

    return this.listFilesRecursive().filter(item => {
      if (item.type !== 'file') {
        return false;
      }

      if (markerFilename && item.path === markerFilename) {
        return false;
      }

      return this.isIgnoredPath(item.path) || !validFilePaths.has(item.path);
    });
  }

  trashFilesNotInManifest(validFilePaths) {
    const deleteTargets = this.getDeleteTargets(validFilePaths);

    this.validateDeleteLimit(deleteTargets);

    deleteTargets.forEach(item => {
      if (this.config.DRY_RUN_DELETE) {
        this.logger.log(`[DRY-RUN] 삭제 예정 GitHub에 없음: ${item.path}`);
        return;
      }

      item.file.setTrashed(true);
      this.logger.log(`Drive에서 삭제됨 GitHub에 없음: ${item.path}`);
    });

    this.logger.log(`삭제 동기화 검사 완료: 삭제 대상 ${deleteTargets.length}개`);

    return deleteTargets;
  }

  validateManifest(validFilePaths) {
    if (!(validFilePaths instanceof Set)) {
      throw new Error('삭제 동기화 오류: validFilePaths는 Set이어야 합니다.');
    }

    if (validFilePaths.size < this.config.MIN_EXPECTED_GITHUB_FILES) {
      throw new Error(
        `안전 중단: GitHub 파일 manifest가 너무 작습니다. ` +
        `현재 ${validFilePaths.size}개`
      );
    }
  }

  validateDeleteLimit(deleteTargets) {
    if (deleteTargets.length > this.config.MAX_DELETE_PER_RUN) {
      throw new Error(
        `안전 중단: 삭제 예정 파일이 ${deleteTargets.length}개입니다. ` +
        `상한 ${this.config.MAX_DELETE_PER_RUN}개를 초과했습니다.`
      );
    }
  }

  normalizePath(path) {
    return String(path || '')
      .replace(/^\/+/, '')
      .replace(/\/+$/, '');
  }
}