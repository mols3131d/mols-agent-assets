class GithubApiError extends Error {
  constructor(message, context = {}) {
    super(message);
    this.name = 'GithubApiError';
    this.context = context;
  }
}

class GithubClient {
  constructor(options) {
    if (!options || !options.owner || !options.repo) {
      throw new Error('GithubClient 설정 오류: owner와 repo는 필수입니다.');
    }

    this.owner = options.owner;
    this.repo = options.repo;
    this.token = options.token || '';
    this.fetcher = options.fetcher || UrlFetchApp;
    this.baseUrl = `https://api.github.com/repos/${this.owner}/${this.repo}`;
  }

  getHeaders(accept) {
    const headers = {
      'User-Agent': 'GAS-Sync-Script',
      'Accept': accept || 'application/vnd.github.v3+json'
    };

    if (this.token) {
      headers['Authorization'] = `token ${this.token}`;
    }

    return headers;
  }

  encodePath(path) {
    return String(path)
      .split('/')
      .map(encodeURIComponent)
      .join('/');
  }

  buildTreeUrl(branch) {
    const encodedBranch = encodeURIComponent(branch);
    return `${this.baseUrl}/git/trees/${encodedBranch}?recursive=1`;
  }

  buildContentsUrl(path, branch) {
    const encodedPath = this.encodePath(path);
    const encodedBranch = encodeURIComponent(branch);
    return `${this.baseUrl}/contents/${encodedPath}?ref=${encodedBranch}`;
  }

  fetchJson(url, options = {}) {
    const response = this.fetcher.fetch(url, {
      headers: options.headers || this.getHeaders(),
      muteHttpExceptions: true
    });

    const status = response.getResponseCode();
    const body = response.getContentText();

    if (status < 200 || status >= 300) {
      throw new GithubApiError(`GitHub API error: HTTP ${status}`, {
        url,
        status,
        body
      });
    }

    try {
      return JSON.parse(body);
    } catch (error) {
      throw new GithubApiError('GitHub API error: JSON 파싱 실패', {
        url,
        status,
        body
      });
    }
  }

  fetchBlob(url, filename, options = {}) {
    const response = this.fetcher.fetch(url, {
      headers: options.headers || this.getHeaders('application/vnd.github.v3.raw'),
      muteHttpExceptions: true
    });

    const status = response.getResponseCode();

    if (status < 200 || status >= 300) {
      throw new GithubApiError(`GitHub 파일 다운로드 실패: HTTP ${status}`, {
        url,
        status,
        body: response.getContentText()
      });
    }

    return response.getBlob().setName(filename);
  }

  getTree(branch) {
    if (!branch) {
      throw new Error('GithubClient 오류: branch는 필수입니다.');
    }

    const url = this.buildTreeUrl(branch);
    const payload = this.fetchJson(url);

    if (!payload.tree || !Array.isArray(payload.tree)) {
      throw new GithubApiError('GitHub API error: tree 응답이 올바르지 않습니다.', {
        url,
        payload
      });
    }

    if (payload.truncated) {
      throw new GithubApiError(
        'GitHub API error: tree 응답이 truncated 상태입니다. 일부 파일만 반환되어 삭제 동기화를 중단합니다.',
        { url }
      );
    }

    return payload.tree;
  }

  downloadFileBlob(path, branch, filename) {
    if (!path) {
      throw new Error('GithubClient 오류: path는 필수입니다.');
    }

    if (!branch) {
      throw new Error('GithubClient 오류: branch는 필수입니다.');
    }

    if (!filename) {
      throw new Error('GithubClient 오류: filename은 필수입니다.');
    }

    const url = this.buildContentsUrl(path, branch);

    return this.fetchBlob(url, filename, {
      headers: this.getHeaders('application/vnd.github.v3.raw')
    });
  }
}