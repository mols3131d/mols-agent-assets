// --- Mock Factories ---

function GithubClientTest_createFakeResponse({ status = 200, body = "{}", blob = null } = {}) {
  return {
    getResponseCode() { return status; },
    getContentText() { return body; },
    getBlob() { return blob || Utilities.newBlob("test"); }
  };
}

function GithubClientTest_createFakeFetcher(response) {
  return { fetch(url, options) { return response; } };
}

// --- Common Setup Helper ---

function GithubClientTest_setup(optionsOverrides = {}) {
  const defaults = {
    owner: "owner",
    repo: "repo",
    token: "token123"
  };
  return new GithubClient(Object.assign(defaults, optionsOverrides));
}

// --- Test Suites ---

function GithubClientTest_constructor() {
  TestRunner.run("GithubClient.constructor", () => {
    // 1. Success construction
    const client = GithubClientTest_setup();
    assertEqual(client.owner, "owner", "owner should be assigned");
    assertEqual(client.repo, "repo", "repo should be assigned");
    assertEqual(client.token, "token123", "token should be assigned");
    assertEqual(client.baseUrl, "https://api.github.com/repos/owner/repo", "baseUrl should be generated correctly");

    // 2. Failure: missing owner
    assertThrows(() => {
      new GithubClient({ repo: "repo" });
    }, "owner is required");

    // 3. Failure: missing repo
    assertThrows(() => {
      new GithubClient({ owner: "owner" });
    }, "repo is required");
  });
}

function GithubClientTest_headers() {
  TestRunner.run("GithubClient.headers", () => {
    // 1. Without token
    const clientNoToken = GithubClientTest_setup({ token: "" });
    const headersNoToken = clientNoToken.getHeaders();
    assertEqual(headersNoToken["User-Agent"], "GAS-Sync-Script", "User-Agent should exist");
    assertEqual(headersNoToken["Accept"], "application/vnd.github.v3+json", "Accept header should exist");
    assertFalse("Authorization" in headersNoToken, "Authorization should not exist");

    // 2. With token
    const clientWithToken = GithubClientTest_setup({ token: "secret-token" });
    const headersWithToken = clientWithToken.getHeaders();
    assertEqual(headersWithToken.Authorization, "token secret-token", "Authorization header should exist");
  });
}

function GithubClientTest_urlBuilders() {
  TestRunner.run("GithubClient.urlBuilders", () => {
    const client = GithubClientTest_setup();

    // encodePath
    const encoded = client.encodePath("folder name/한글 file.txt");
    assertEqual(encoded, "folder%20name/%ED%95%9C%EA%B8%80%20file.txt", "path should be encoded segment-by-segment");

    // buildTreeUrl
    const treeUrl = client.buildTreeUrl("feature/test branch");
    assertEqual(treeUrl, "https://api.github.com/repos/owner/repo/git/trees/feature%2Ftest%20branch?recursive=1", "tree url should be encoded");

    // buildContentsUrl
    const contentsUrl = client.buildContentsUrl("folder name/test.txt", "feature/test branch");
    assertEqual(contentsUrl, "https://api.github.com/repos/owner/repo/contents/folder%20name/test.txt?ref=feature%2Ftest%20branch", "contents url should be encoded");
  });
}

function GithubClientTest_getTree() {
  TestRunner.run("GithubClient.getTree scenarios", () => {
    // 1. Success case
    const successRes = GithubClientTest_createFakeResponse({
      status: 200,
      body: JSON.stringify({
        truncated: false,
        tree: [{ path: "src/index.js", type: "blob" }]
      })
    });
    const successClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(successRes) });
    const tree = successClient.getTree("main");
    assertEqual(tree.length, 1, "tree should contain one item");
    assertEqual(tree[0].path, "src/index.js", "tree path should match");

    // 2. Error case: 404 http error
    const errRes = GithubClientTest_createFakeResponse({ status: 404, body: '{"message":"Not Found"}' });
    const errClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(errRes) });
    assertThrows(() => { errClient.getTree("main"); }, "404 should throw");

    // 3. Error case: invalid tree structure (missing tree field)
    const invalidTreeRes = GithubClientTest_createFakeResponse({ status: 200, body: JSON.stringify({ truncated: false }) });
    const invalidTreeClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(invalidTreeRes) });
    assertThrows(() => { invalidTreeClient.getTree("main"); }, "missing tree should throw");

    // 4. Error case: truncated response
    const truncatedRes = GithubClientTest_createFakeResponse({ status: 200, body: JSON.stringify({ truncated: true, tree: [] }) });
    const truncatedClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(truncatedRes) });
    assertThrows(() => { truncatedClient.getTree("main"); }, "truncated should throw");

    // 5. Error case: invalid JSON body
    const invalidJsonRes = GithubClientTest_createFakeResponse({ status: 200, body: "{invalid json" });
    const invalidJsonClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(invalidJsonRes) });
    assertThrows(() => { invalidJsonClient.getTree("main"); }, "invalid json should throw");

    // 6. Error case: empty branch validation
    const valClient = GithubClientTest_setup();
    assertThrows(() => { valClient.getTree(""); }, "branch is required");
  });
}

function GithubClientTest_downloadFileBlob() {
  TestRunner.run("GithubClient.downloadFileBlob scenarios", () => {
    // 1. Success case
    const successRes = GithubClientTest_createFakeResponse({ status: 200, blob: Utilities.newBlob("hello world") });
    const successClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(successRes) });
    const blob = successClient.downloadFileBlob("src/index.js", "main", "index.js");
    assertEqual(blob.getName(), "index.js", "blob name should match filename");

    // 2. Error case: 500 server error
    const errRes = GithubClientTest_createFakeResponse({ status: 500, body: "server error" });
    const errClient = GithubClientTest_setup({ fetcher: GithubClientTest_createFakeFetcher(errRes) });
    assertThrows(() => { errClient.downloadFileBlob("src/index.js", "main", "index.js"); }, "500 should throw");

    // 3. Error case: validation checks
    const valClient = GithubClientTest_setup();
    assertThrows(() => { valClient.downloadFileBlob("", "main", "a.txt"); }, "path is required");
    assertThrows(() => { valClient.downloadFileBlob("a.txt", "", "a.txt"); }, "branch is required");
    assertThrows(() => { valClient.downloadFileBlob("a.txt", "main", ""); }, "filename is required");
  });
}

// --- Suite Runner ---

function GithubClientTest_all() {
  GithubClientTest_constructor();
  GithubClientTest_headers();
  GithubClientTest_urlBuilders();
  GithubClientTest_getTree();
  GithubClientTest_downloadFileBlob();
}
