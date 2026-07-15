from src.scripts import sync_github_files


def test_download_uses_raw_github_url(monkeypatch):
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b"remote-content"

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(sync_github_files.urllib.request, "urlopen", fake_urlopen)

    content = sync_github_files.download(
        "https://github.com/owner/repo/blob/main/src/rules/sample.md"
    )

    assert content == b"remote-content"
    assert captured["timeout"] == 30
    assert captured["url"] == (
        "https://raw.githubusercontent.com/owner/repo/main/src/rules/sample.md"
    )
