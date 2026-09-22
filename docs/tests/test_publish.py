import pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # docs/
import publish


def test_publishable_keeps_tracked_generated_and_audio_only(tmp_path):
    def put(rel):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")

    for rel in ["a.md", "tool.py", "tests/t.md", "reader/w/overview.md"]:
        put(rel)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    for rel in [
        "a.html", "reader/w/overview.html", "reader/w/index.html",  # generated from tracked .md
        "stale.html",                                               # no tracked source — another branch's leftover
        "research/d/visuals/p.jpg",                                 # dive image, rights unclear
        "reader/w/build/audio/s.m4a", "reader/w/build/timing.json",
        "reader/w/build/_audition/a.wav", "reader/w/build/audio/.DS_Store",
    ]:
        put(rel)

    got = {p.as_posix() for p in publish.publishable(tmp_path)}

    assert got == {
        "a.md", "a.html",
        "reader/w/overview.md", "reader/w/overview.html", "reader/w/index.html",
        "reader/w/build/audio/s.m4a", "reader/w/build/timing.json",
    }
