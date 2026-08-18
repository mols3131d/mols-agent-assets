// --- Mock Factories ---

function DriveClientTest_createFakeFile(
  id,
  name,
  description = "",
  contentBlob = null,
) {
  let trashed = false;
  return {
    id,
    name,
    description,
    trashed,
    contentBlob,
    getId() {
      return this.id;
    },
    getName() {
      return this.name;
    },
    getDescription() {
      return this.description;
    },
    setDescription(desc) {
      this.description = desc;
    },
    setTrashed(val) {
      this.trashed = val;
    },
    isTrashed() {
      return this.trashed;
    },
    getBlob() {
      return this.contentBlob;
    },
  };
}

function DriveClientTest_createFakeFolder(id, name) {
  const folders = [];
  const files = [];
  let trashed = false;
  return {
    id,
    name,
    folders,
    files,
    trashed,
    getId() {
      return this.id;
    },
    getName() {
      return this.name;
    },
    isTrashed() {
      return this.trashed;
    },
    setTrashed(val) {
      this.trashed = val;
    },
    getFoldersByName(folderName) {
      const matched = this.folders.filter(
        (f) => f.getName() === folderName && !f.isTrashed(),
      );
      return DriveClientTest_createIterator(matched);
    },
    getFilesByName(fileName) {
      const matched = this.files.filter(
        (f) => f.getName() === fileName && !f.isTrashed(),
      );
      return DriveClientTest_createIterator(matched);
    },
    createFolder(folderName) {
      const newFolder = DriveClientTest_createFakeFolder(
        `folder-${folderName}-${Math.random()}`,
        folderName,
      );
      this.folders.push(newFolder);
      return newFolder;
    },
    createFile(fileBlob) {
      const newFile = DriveClientTest_createFakeFile(
        `file-${fileBlob.getName()}-${Math.random()}`,
        fileBlob.getName(),
        "",
        fileBlob,
      );
      this.files.push(newFile);
      return newFile;
    },
    getFiles() {
      return DriveClientTest_createIterator(
        this.files.filter((f) => !f.isTrashed()),
      );
    },
    getFolders() {
      return DriveClientTest_createIterator(
        this.folders.filter((f) => !f.isTrashed()),
      );
    },
  };
}

function DriveClientTest_createIterator(items) {
  let index = 0;
  return {
    hasNext() {
      return index < items.length;
    },
    next() {
      if (index >= items.length) throw new Error("No more items in iterator");
      return items[index++];
    },
  };
}

function DriveClientTest_createValidConfig(overrides = {}) {
  return Object.assign(
    {
      DRY_RUN_DELETE: false,
      MAX_DELETE_PER_RUN: 5,
      MIN_EXPECTED_GITHUB_FILES: 1,
      SYNC_MARKER_FILENAME: ".github-drive-sync-marker",
    },
    overrides,
  );
}

function DriveClientTest_createFakeResponse({
  status = 200,
  body = "{}",
} = {}) {
  return {
    getResponseCode() {
      return status;
    },
    getContentText() {
      return body;
    },
  };
}

function DriveClientTest_createFakeScriptApp(token = "dummy-token") {
  return {
    getOAuthToken() {
      return token;
    },
  };
}

function DriveClientTest_createFakeUrlFetchApp(response) {
  const fetches = [];
  return {
    fetch(url, options) {
      fetches.push({ url, options });
      return response;
    },
    getFetches() {
      return fetches;
    },
  };
}

// --- Common Setup Helper ---

function DriveClientTest_setup(
  configOverrides = {},
  isIgnoredPath = () => false,
) {
  const rootFolder = DriveClientTest_createFakeFolder("root-id", "root");
  const driveAppMock = {
    getFolderById(id) {
      assertEqual(id, "root-id", "should request correct folder ID");
      return rootFolder;
    },
  };
  const successResponse = DriveClientTest_createFakeResponse({
    status: 200,
    body: '{"id": "file-id"}',
  });
  const urlFetchMock = DriveClientTest_createFakeUrlFetchApp(successResponse);
  const scriptAppMock = DriveClientTest_createFakeScriptApp("token-123");

  const client = new DriveClient({
    targetFolderId: "root-id",
    driveApp: driveAppMock,
    urlFetchApp: urlFetchMock,
    scriptApp: scriptAppMock,
    config: DriveClientTest_createValidConfig(configOverrides),
    isIgnoredPath,
  });
  return { client, rootFolder, driveAppMock, urlFetchMock, scriptAppMock };
}

// --- Test Suites ---

function DriveClientTest_constructor() {
  TestRunner.run("DriveClient.constructor", () => {
    // 1. Invalid instantiation checks
    assertThrows(() => {
      new DriveClient({});
    }, "targetFolderId is required");
    assertThrows(() => {
      new DriveClient(null);
    }, "options is required");

    // 2. Valid instantiation check
    const { client, rootFolder } = DriveClientTest_setup();
    assertEqual(
      client.rootFolder,
      rootFolder,
      "rootFolder should be initialized",
    );
    assertEqual(
      client.folderCache[""],
      rootFolder,
      "rootFolder should be cached",
    );
  });
}

function DriveClientTest_normalizePath() {
  TestRunner.run("DriveClient.normalizePath", () => {
    const { client } = DriveClientTest_setup();
    assertEqual(
      client.normalizePath("/foo/bar/"),
      "foo/bar",
      "should strip outer slashes",
    );
    assertEqual(
      client.normalizePath("///a///b///"),
      "a///b",
      "should strip outer slashes completely",
    );
    assertEqual(client.normalizePath(""), "", "should handle empty path");
    assertEqual(client.normalizePath(null), "", "should handle null path");
  });
}

function DriveClientTest_folderOperations() {
  TestRunner.run(
    "DriveClient.folderOperations (ensureFolder & getSubFolder)",
    () => {
      const { client, rootFolder } = DriveClientTest_setup();

      // ensureFolder root
      const root = client.ensureFolder("");
      assertEqual(root, rootFolder, "empty path yields root");

      // ensureFolder nested path creation
      const child = client.ensureFolder("src/utils");
      const srcFolder = rootFolder.folders[0];
      assertEqual(srcFolder.getName(), "src", "src folder should be created");
      assertEqual(
        srcFolder.folders[0],
        child,
        "utils folder should be created under src",
      );

      // getSubFolder check
      const found = client.getSubFolder(rootFolder, "src");
      assertEqual(found, srcFolder, "getSubFolder returns matched folder");
      const notFound = client.getSubFolder(rootFolder, "invalid");
      assertEqual(notFound, null, "getSubFolder returns null for unmatched");
    },
  );
}

function DriveClientTest_fileQueries() {
  TestRunner.run(
    "DriveClient.fileQueries (getFileSha & getFirstFileByName)",
    () => {
      const { client, rootFolder } = DriveClientTest_setup();
      const fileBlob = Utilities.newBlob("content").setName("a.txt");
      const newFile = rootFolder.createFile(fileBlob);
      newFile.setDescription("some-sha-value");

      // getFirstFileByName
      const found = client.getFirstFileByName(rootFolder, "a.txt");
      assertEqual(found, newFile, "should find file by name");
      const notFound = client.getFirstFileByName(rootFolder, "b.txt");
      assertEqual(notFound, null, "should return null for non-existing");

      // getFileSha
      const shaData = client.getFileSha(rootFolder, "a.txt");
      assertEqual(shaData.id, newFile.getId(), "should return file id");
      assertEqual(
        shaData.sha,
        "some-sha-value",
        "should return sha from description",
      );

      const noShaData = client.getFileSha(rootFolder, "b.txt");
      assertEqual(noShaData, null, "should return null sha if file not found");
    },
  );
}

function DriveClientTest_trashDuplicateFiles() {
  TestRunner.run("DriveClient.trashDuplicateFiles", () => {
    const { client, rootFolder } = DriveClientTest_setup();
    const blob = Utilities.newBlob("x");
    const file1 = rootFolder.createFile(blob);
    file1.name = "dup.txt";
    const file2 = rootFolder.createFile(blob);
    file2.name = "dup.txt";
    const file3 = rootFolder.createFile(blob);
    file3.name = "dup.txt";

    const count = client.trashDuplicateFiles(
      rootFolder,
      "dup.txt",
      file2.getId(),
    );
    assertEqual(count, 2, "should trash 2 duplicate files");
    assertTrue(file1.isTrashed(), "file1 should be trashed");
    assertFalse(file2.isTrashed(), "file2 should not be trashed (keepFileId)");
    assertTrue(file3.isTrashed(), "file3 should be trashed");
  });
}

function DriveClientTest_saveFile() {
  TestRunner.run("DriveClient.saveFile (new file & existing file)", () => {
    const { client, rootFolder } = DriveClientTest_setup();
    const blob = Utilities.newBlob("content").setName("a.txt");

    // 1. Save new file
    const resNew = client.saveFile(rootFolder, "a.txt", blob, "sha123");
    const savedFile = rootFolder.files[0];
    assertEqual(
      resNew.getId(),
      savedFile.getId(),
      "should return saved file id",
    );
    assertEqual(resNew.getDescription(), "sha123", "should return saved sha");
    assertEqual(
      savedFile.getDescription(),
      "sha123",
      "should write sha in description",
    );

    // 2. Save existing file (update scenario)
    const newBlob = Utilities.newBlob("new-content").setName("a.txt");
    const resExist = client.saveFile(rootFolder, "a.txt", newBlob, "sha456");
    assertEqual(
      resExist.getId(),
      savedFile.getId(),
      "should keep same file id",
    );
    assertEqual(
      resExist.getDescription(),
      "sha456",
      "should update sha to sha456",
    );
    assertEqual(
      savedFile.getDescription(),
      "sha456",
      "should write updated sha in description",
    );
  });
}

function DriveClientTest_updateFileContent() {
  TestRunner.run("DriveClient.updateFileContent (success & error)", () => {
    const successResponse = DriveClientTest_createFakeResponse({
      status: 200,
      body: '{"id": "file-id"}',
    });
    const urlFetchMock = DriveClientTest_createFakeUrlFetchApp(successResponse);
    const scriptAppMock = DriveClientTest_createFakeScriptApp("token-123");

    const client = new DriveClient({
      targetFolderId: "root-id",
      driveApp: {
        getFolderById: () =>
          DriveClientTest_createFakeFolder("root-id", "root"),
      },
      urlFetchApp: urlFetchMock,
      scriptApp: scriptAppMock,
      config: DriveClientTest_createValidConfig(),
    });

    const fileBlob = Utilities.newBlob("updated-data").setName("a.txt");
    const fakeFile = DriveClientTest_createFakeFile("file-id", "a.txt");

    // Success call
    client.updateFileContent(fakeFile, "a.txt", fileBlob);
    const fetches = urlFetchMock.getFetches();
    assertEqual(fetches.length, 1, "should make 1 fetch call");
    assertEqual(
      fetches[0].url,
      "https://www.googleapis.com/upload/drive/v3/files/file-id?uploadType=media",
      "should use correct API url",
    );
    assertEqual(
      fetches[0].options.headers["Authorization"],
      "Bearer token-123",
      "should inject OAuth token",
    );

    // Error call
    const errorResponse = DriveClientTest_createFakeResponse({
      status: 500,
      body: "Internal Server Error",
    });
    const errUrlFetch = DriveClientTest_createFakeUrlFetchApp(errorResponse);
    const errClient = new DriveClient({
      targetFolderId: "root-id",
      driveApp: {
        getFolderById: () =>
          DriveClientTest_createFakeFolder("root-id", "root"),
      },
      urlFetchApp: errUrlFetch,
      scriptApp: scriptAppMock,
      config: DriveClientTest_createValidConfig(),
    });
    const errFakeFile = DriveClientTest_createFakeFile("file-id", "a.txt");

    assertThrows(() => {
      errClient.updateFileContent(errFakeFile, "a.txt", fileBlob);
    }, "should throw on HTTP error response");
  });
}

function DriveClientTest_validateSyncMarker() {
  TestRunner.run("DriveClient.validateSyncMarker (success & error)", () => {
    // 1. Success case: marker exists
    const { client, rootFolder } = DriveClientTest_setup({
      SYNC_MARKER_FILENAME: "marker.txt",
    });
    rootFolder.createFile(Utilities.newBlob("").setName("marker.txt"));
    client.validateSyncMarker(); // Should not throw

    // 2. Error case 1: target folder empty or marker missing
    const { client: errClient } = DriveClientTest_setup({
      SYNC_MARKER_FILENAME: "marker.txt",
    });
    assertThrows(() => {
      errClient.validateSyncMarker();
    }, "should throw safety exception");

    // 3. Error case 2: marker filename config missing
    const { client: errClientConfig } = DriveClientTest_setup({
      SYNC_MARKER_FILENAME: "",
    });
    assertThrows(() => {
      errClientConfig.validateSyncMarker();
    }, "should throw on empty marker config");
  });
}

function DriveClientTest_deleteOperations() {
  TestRunner.run(
    "DriveClient.deleteOperations (listFilesRecursive, getDeleteTargets & trashFilesNotInManifest)",
    () => {
      const { client, rootFolder } = DriveClientTest_setup({
        DRY_RUN_DELETE: false,
        MAX_DELETE_PER_RUN: 1,
        MIN_EXPECTED_GITHUB_FILES: 1,
      });

      // Setup nested files
      const f1 = rootFolder.createFile(
        Utilities.newBlob("1").setName("file1.txt"),
      );
      const src = rootFolder.createFolder("src");
      const f2 = src.createFile(Utilities.newBlob("2").setName("file2.txt"));

      // 1. listFilesRecursive
      const allFiles = client.listFilesRecursive();
      assertEqual(allFiles.length, 2, "should find 2 files recursively");
      assertTrue(
        allFiles.some((f) => f.path === "file1.txt" && f.file === f1),
        "should find root file",
      );
      assertTrue(
        allFiles.some((f) => f.path === "src/file2.txt" && f.file === f2),
        "should find nested file",
      );

      // 2. getDeleteTargets
      const manifest = new Set(["file1.txt"]); // src/file2.txt should be deleted
      const targets = client.getDeleteTargets(manifest);
      assertEqual(targets.length, 1, "should find 1 delete target");
      assertEqual(
        targets[0].path,
        "src/file2.txt",
        "delete target path matches",
      );

      // 3. trashFilesNotInManifest - limit exceeded
      assertThrows(() => {
        // Setup another deleted file to exceed limit (MAX_DELETE_PER_RUN = 1)
        rootFolder.createFile(Utilities.newBlob("3").setName("file3.txt"));
        client.trashFilesNotInManifest(manifest);
      }, "should throw since 2 deletions exceed limit of 1");

      // 4. trashFilesNotInManifest - dry-run check
      const { client: dryClient, rootFolder: dryRoot } = DriveClientTest_setup({
        DRY_RUN_DELETE: true,
        MAX_DELETE_PER_RUN: 5,
        MIN_EXPECTED_GITHUB_FILES: 1,
      });
      const df1 = dryRoot.createFile(Utilities.newBlob("").setName("a.txt"));
      const df2 = dryRoot.createFile(Utilities.newBlob("").setName("b.txt"));
      const dryManifest = new Set(["a.txt"]);

      const dryRes = dryClient.trashFilesNotInManifest(dryManifest);
      assertEqual(dryRes.length, 1, "dry-run identifies 1 target");
      assertFalse(df2.isTrashed(), "file should not be trashed under dry-run");

      // 5. trashFilesNotInManifest - success check
      const { client: runClient, rootFolder: runRoot } = DriveClientTest_setup({
        DRY_RUN_DELETE: false,
        MAX_DELETE_PER_RUN: 5,
        MIN_EXPECTED_GITHUB_FILES: 1,
      });
      const rf1 = runRoot.createFile(Utilities.newBlob("").setName("a.txt"));
      const rf2 = runRoot.createFile(Utilities.newBlob("").setName("b.txt"));

      const runRes = runClient.trashFilesNotInManifest(dryManifest);
      assertEqual(runRes.length, 1, "should delete 1 file");
      assertTrue(rf2.isTrashed(), "file b.txt should be trashed");
      assertFalse(rf1.isTrashed(), "file a.txt should remain");

      // 6. trashFilesNotInManifest - ignore rules check (newly added)
      const { client: ignoreClient, rootFolder: ignoreRoot } = DriveClientTest_setup(
        {
          DRY_RUN_DELETE: false,
          MAX_DELETE_PER_RUN: 5,
          MIN_EXPECTED_GITHUB_FILES: 1,
        },
        (path) => path.endsWith(".py") // .py 파일들을 무시 규칙으로 가정
      );

      const fPy = ignoreRoot.createFile(Utilities.newBlob("").setName("test.py"));
      const fTxt = ignoreRoot.createFile(Utilities.newBlob("").setName("test.txt"));
      const ignoreManifest = new Set(["test.py", "test.txt"]);

      const ignoreRes = ignoreClient.trashFilesNotInManifest(ignoreManifest);
      assertEqual(ignoreRes.length, 1, "ignored file should be deleted");
      assertEqual(ignoreRes[0].path, "test.py", "deleted file path matches");
      assertTrue(fPy.isTrashed(), "test.py should be trashed");
      assertFalse(fTxt.isTrashed(), "test.txt should not be trashed");

      // 7. trashFilesNotInManifest - sync marker protection check (newly added)
      const { client: markerClient, rootFolder: markerRoot } = DriveClientTest_setup({
        DRY_RUN_DELETE: false,
        MAX_DELETE_PER_RUN: 5,
        MIN_EXPECTED_GITHUB_FILES: 1,
        SYNC_MARKER_FILENAME: ".github-drive-sync-marker"
      });

      const fMarker = markerRoot.createFile(Utilities.newBlob("").setName(".github-drive-sync-marker"));
      const markerManifest = new Set(["test.txt"]);

      const markerRes = markerClient.trashFilesNotInManifest(markerManifest);
      assertFalse(fMarker.isTrashed(), "sync marker file should NOT be trashed");
    },
  );
}

// --- Suite Runner ---

function DriveClientTest_all() {
  DriveClientTest_constructor();
  DriveClientTest_normalizePath();
  DriveClientTest_folderOperations();
  DriveClientTest_fileQueries();
  DriveClientTest_trashDuplicateFiles();
  DriveClientTest_saveFile();
  DriveClientTest_updateFileContent();
  DriveClientTest_validateSyncMarker();
  DriveClientTest_deleteOperations();
}
