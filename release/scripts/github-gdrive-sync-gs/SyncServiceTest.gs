function SyncServiceTest_createFakeGithub() {
  return {
    downloaded: [],

    downloadFileBlob(path, branch, filename) {
      this.downloaded.push({
        path,
        branch,
        filename,
      });

      return Utilities.newBlob(`content:${path}`).setName(filename);
    },
  };
}

function SyncServiceTest_createFakeDrive(existingFilesByName = {}) {
  return {
    ensuredFolders: [],
    savedFiles: [],
    trashedDuplicates: [],
    existingFilesByName,

    ensureFolder(path) {
      this.ensuredFolders.push(path);

      return {
        path,
      };
    },

    getFileSha(parentFolder, filename) {
      return this.existingFilesByName[filename] || null;
    },

    trashDuplicateFiles(parentFolder, filename, keepFileId) {
      this.trashedDuplicates.push({
        parentFolder,
        filename,
        keepFileId,
      });

      return 0;
    },

    saveFile(parentFolder, filename, fileBlob, sha) {
      this.savedFiles.push({
        parentFolder,
        filename,
        fileBlob,
        sha,
      });

      return {
        id: `saved-${filename}`,
        sha,
      };
    },
  };
}

function SyncServiceTest_splitGithubTree_success() {
  TestRunner.run("SyncService.splitGithubTree success", () => {
    const tree = [
      {
        path: "z-folder",
        type: "tree",
      },
      {
        path: "a-folder",
        type: "tree",
      },
      {
        path: "src/index.js",
        type: "blob",
        sha: "sha-1",
      },
      {
        path: "dist/app.js",
        type: "blob",
        sha: "sha-ignored",
      },
      {
        path: "README.md",
        type: "blob",
        sha: "sha-2",
      },
    ];

    const manifest = splitGithubTree(tree, ["dist/**"]);

    assertEqual(
      manifest.folders.length,
      2,
      "should include two folders",
    );

    assertEqual(
      manifest.folders[0].path,
      "a-folder",
      "folders should be sorted",
    );

    assertEqual(
      manifest.files.length,
      2,
      "ignored file should be excluded",
    );

    assertTrue(
      manifest.filePaths.has("src/index.js"),
      "manifest should include src/index.js",
    );

    assertTrue(
      manifest.filePaths.has("README.md"),
      "manifest should include README.md",
    );

    assertFalse(
      manifest.filePaths.has("dist/app.js"),
      "manifest should exclude ignored file",
    );
  });
}

function SyncServiceTest_splitGithubTree_rejectsNonArray() {
  TestRunner.run("SyncService.splitGithubTree rejects non-array", () => {
    assertThrows(() => {
      splitGithubTree(null, []);
    }, "non-array tree should throw");
  });
}

function SyncServiceTest_syncFoldersToDrive() {
  TestRunner.run("SyncService.syncFoldersToDrive", () => {
    const drive = SyncServiceTest_createFakeDrive();

    syncFoldersToDrive(drive, [
      {
        path: "src",
      },
      {
        path: "src/app",
      },
    ]);

    assertEqual(
      drive.ensuredFolders.length,
      2,
      "should ensure two folders",
    );

    assertEqual(
      drive.ensuredFolders[0],
      "src",
      "first ensured folder should match",
    );

    assertEqual(
      drive.ensuredFolders[1],
      "src/app",
      "second ensured folder should match",
    );
  });
}

function SyncServiceTest_syncSingleFileToDrive_newFile() {
  TestRunner.run("SyncService.syncSingleFileToDrive new file", () => {
    const github = SyncServiceTest_createFakeGithub();
    const drive = SyncServiceTest_createFakeDrive();

    syncSingleFileToDrive(
      github,
      drive,
      {
        path: "src/index.js",
        sha: "sha-new",
      },
      "main",
    );

    assertEqual(
      drive.ensuredFolders[0],
      "src",
      "parent folder should be ensured",
    );

    assertEqual(
      github.downloaded.length,
      1,
      "file should be downloaded",
    );

    assertEqual(
      github.downloaded[0].path,
      "src/index.js",
      "download path should match",
    );

    assertEqual(
      github.downloaded[0].branch,
      "main",
      "download branch should match",
    );

    assertEqual(
      github.downloaded[0].filename,
      "index.js",
      "download filename should match",
    );

    assertEqual(
      drive.savedFiles.length,
      1,
      "file should be saved",
    );

    assertEqual(
      drive.savedFiles[0].sha,
      "sha-new",
      "saved sha should match",
    );
  });
}

function SyncServiceTest_syncSingleFileToDrive_existingSameSha() {
  TestRunner.run(
    "SyncService.syncSingleFileToDrive existing same sha",
    () => {
      const github = SyncServiceTest_createFakeGithub();

      const drive = SyncServiceTest_createFakeDrive({
        "index.js": {
          id: "drive-file-id",
          sha: "same-sha",
        },
      });

      syncSingleFileToDrive(
        github,
        drive,
        {
          path: "src/index.js",
          sha: "same-sha",
        },
        "main",
      );

      assertEqual(
        github.downloaded.length,
        0,
        "same SHA file should not be downloaded",
      );

      assertEqual(
        drive.savedFiles.length,
        0,
        "same SHA file should not be saved",
      );

      assertEqual(
        drive.trashedDuplicates.length,
        1,
        "duplicates should be cleaned",
      );

      assertEqual(
        drive.trashedDuplicates[0].keepFileId,
        "drive-file-id",
        "keepFileId should match existing file id",
      );
    },
  );
}

function SyncServiceTest_syncSingleFileToDrive_existingDifferentSha() {
  TestRunner.run(
    "SyncService.syncSingleFileToDrive existing different sha",
    () => {
      const github = SyncServiceTest_createFakeGithub();

      const drive = SyncServiceTest_createFakeDrive({
        "index.js": {
          id: "drive-file-id",
          sha: "old-sha",
        },
      });

      syncSingleFileToDrive(
        github,
        drive,
        {
          path: "src/index.js",
          sha: "new-sha",
        },
        "main",
      );

      assertEqual(
        github.downloaded.length,
        1,
        "changed file should be downloaded",
      );

      assertEqual(
        drive.savedFiles.length,
        1,
        "changed file should be saved",
      );

      assertEqual(
        drive.savedFiles[0].sha,
        "new-sha",
        "new sha should be saved",
      );
    },
  );
}

function SyncServiceTest_syncFilesToDrive() {
  TestRunner.run("SyncService.syncFilesToDrive", () => {
    const github = SyncServiceTest_createFakeGithub();
    const drive = SyncServiceTest_createFakeDrive();

    syncFilesToDrive(
      github,
      drive,
      [
        {
          path: "a.txt",
          sha: "sha-a",
        },
        {
          path: "src/b.txt",
          sha: "sha-b",
        },
      ],
      "main",
    );

    assertEqual(
      github.downloaded.length,
      2,
      "two files should be downloaded",
    );

    assertEqual(
      drive.savedFiles.length,
      2,
      "two files should be saved",
    );
  });
}

function SyncServiceTest_all() {
  SyncServiceTest_splitGithubTree_success();
  SyncServiceTest_splitGithubTree_rejectsNonArray();

  SyncServiceTest_syncFoldersToDrive();
  SyncServiceTest_syncSingleFileToDrive_newFile();
  SyncServiceTest_syncSingleFileToDrive_existingSameSha();
  SyncServiceTest_syncSingleFileToDrive_existingDifferentSha();
  SyncServiceTest_syncFilesToDrive();
}
