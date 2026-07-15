from src.scripts.sync_github_files import classify_state


def test_classify_missing():
    assert (
        classify_state(
            dest_exists=False,
            synced_hash="old",
            remote_hash="new",
            local_hash=None,
        )
        == "missing"
    )


def test_classify_adopted_when_hash_empty_and_local_matches_remote():
    assert (
        classify_state(
            dest_exists=True,
            synced_hash="",
            remote_hash="abc",
            local_hash="abc",
        )
        == "adopted"
    )


def test_classify_untracked_local_when_hash_empty_and_local_differs():
    assert (
        classify_state(
            dest_exists=True,
            synced_hash="",
            remote_hash="abc",
            local_hash="local",
        )
        == "untracked-local"
    )


def test_classify_unchanged():
    assert (
        classify_state(
            dest_exists=True,
            synced_hash="abc",
            remote_hash="abc",
            local_hash="abc",
        )
        == "unchanged"
    )


def test_classify_remote_changed():
    assert (
        classify_state(
            dest_exists=True,
            synced_hash="abc",
            remote_hash="remote",
            local_hash="abc",
        )
        == "remote-changed"
    )


def test_classify_local_modified():
    assert (
        classify_state(
            dest_exists=True,
            synced_hash="abc",
            remote_hash="abc",
            local_hash="local",
        )
        == "local-modified"
    )


def test_classify_conflict():
    assert (
        classify_state(
            dest_exists=True,
            synced_hash="abc",
            remote_hash="remote",
            local_hash="local",
        )
        == "conflict"
    )
