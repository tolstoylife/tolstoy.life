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


def test_held_back_covers_the_working_papers():
    import pathlib
    held = [
        "research/themes/crisis/annotations.md",
        "research/themes/crisis/annotations.html",
        "research/works/x/annotations.thorium-export.json",
        "superpowers/plans/2026-09-22-research-site-soft-launch.md",
        "research/works/x/_verifier-report.md",
        "research/works/x/extracts/_sweep_diaries.md",
        "research/themes/y/visuals/_visuals-sweep.md",
        "research/themes/y/_witness_sweep.md",
        "research/_meta/z/session-log.md",
        "research/_meta/z/handoff-2026-05-28.md",
        "research/_meta/_handoff-held-quote-corrections-2026-06-07.md",
        "research/works/x/_scholarship-sweep.html",
    ]
    kept = [
        "research/themes/crisis/index.md",
        "reader/non-fiction/personal-papers/confession/overview.md",
        "research/works/x/dossier.yaml",
        "editorial/editorial.md",
        "reader/assets/annotations.js",
        "research/works/x/extracts/_scholarship.md",
    ]
    for rel in held:
        assert publish.held_back(pathlib.PurePosixPath(rel)), rel
    for rel in kept:
        assert not publish.held_back(pathlib.PurePosixPath(rel)), rel
