from src.scripts.sync_github_files import sha256_bytes


def test_sha256_bytes():
    assert (
        sha256_bytes(b"hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e730"
        "43362938b9824"
    )
