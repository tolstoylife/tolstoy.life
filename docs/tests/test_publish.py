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


def test_site_carries_a_not_found_page():
    import pathlib, inspect
    docs = pathlib.Path(__file__).resolve().parents[1]
    assert (docs / "404.md").exists(), "404.md is the page Netlify serves for a link that leads nowhere"
    assert '"404.html"' in inspect.getsource(publish.main), "publish.py builds 404.html into _site/"


def test_only_recorded_free_images_are_cleared(tmp_path):
    dive = tmp_path / "research" / "themes" / "d"
    (dive / "visuals").mkdir(parents=True)
    for name in ["free.jpg", "restricted.jpg", "unrecorded.jpg", "museum.jpg", "met-a.jpg", "met-b.jpg"]:
        (dive / "visuals" / name).write_bytes(b"x")
    (dive / "dossier.yaml").write_text(
        "visuals:\n"
        "  - id: V01\n    licence: PD\n    localPath: visuals/free.jpg\n"
        "  - id: V02\n    licence: CC-BY-SA\n    localPath: visuals/restricted.jpg\n"
        "  - id: V03\n    licence: PD for 1899 text; museum copy rights-reserved\n    localPath: visuals/museum.jpg\n"
        "  - id: V04\n    licence: CC0\n    localPath: visuals/met-*.jpg (2 files)\n")

    cleared = publish.cleared_images(tmp_path)

    assert (dive / "visuals" / "free.jpg").resolve() in cleared
    assert (dive / "visuals" / "restricted.jpg").resolve() not in cleared
    assert (dive / "visuals" / "unrecorded.jpg").resolve() not in cleared
    assert (dive / "visuals" / "museum.jpg").resolve() not in cleared
    assert (dive / "visuals" / "met-b.jpg").resolve() in cleared


def test_withheld_images_become_a_note(tmp_path):
    dive = tmp_path / "research" / "themes" / "d"
    (dive / "visuals").mkdir(parents=True)
    free = dive / "visuals" / "free.jpg"
    free.write_bytes(b"x")
    html = ('<figure><img src="visuals/free.jpg" alt="kept"><img src="visuals/restricted.jpg" alt="gone">'
            '<img src="https://example.org/remote.jpg" alt="remote"></figure>')

    out = publish.hide_withheld_images(html, dive, {free.resolve()})

    assert '<img src="visuals/free.jpg" alt="kept">' in out
    assert 'visuals/restricted.jpg' not in out
    assert "Image not shown — rights unclear" in out
    assert 'https://example.org/remote.jpg' in out


def test_links_to_held_back_pages_are_dropped(tmp_path):
    html = ('<ul><li><a href="/research/x/index.html">The corpus dive</a></li>'
            '<li><a href="/research/x/annotations.html">Reading annotations</a></li>'
            '<li><a href="../../research/y/annotations.html">Reading annotations</a></li></ul>')
    page_dir = publish.DOCS / "reader" / "w"

    out = publish.drop_held_links(html, page_dir)

    assert "The corpus dive" in out
    assert "annotations.html" not in out


def test_missing_wikilinks_become_plain_text():
    html = ('<a class="wikilink" href="/research/wiki/Henry%20George.html">Henry George</a> and '
            '<a class="wikilink wikilink-missing" title="No page yet" href="/research/wiki/1905%20Revolution.html">1905 Revolution</a>')

    out = publish.unlink_missing_wikilinks(html)

    assert "Henry%20George.html" in out
    assert out.endswith(" and 1905 Revolution")


def test_unpublished_sources_link_to_github():
    docs = publish.DOCS
    page_dir = docs / "research" / "themes" / "d"
    script, note = docs / "research" / "lib" / "extract_tei.py", docs.parent / "website" / "src" / "wiki" / "A B.md"
    held = page_dir / "annotations.md"
    html = ('<a href="/research/lib/extract_tei.py">x</a> <a href="../../../../website/src/wiki/A%20B.md">y</a> '
            '<a href="annotations.md">z</a> <a href="/research/index.html">w</a>')

    out = publish.link_sources_to_github(html, page_dir, {docs / "research" / "index.html"}, {script, note, held})

    assert 'href="https://github.com/tolstoylife/tolstoy.life/blob/main/docs/research/lib/extract_tei.py"' in out
    assert 'href="https://github.com/tolstoylife/website/blob/main/src/wiki/A%20B.md"' in out
    assert 'href="annotations.md"' in out  # a held-back working paper keeps its dead link
    assert 'href="/research/index.html"' in out
    assert 'href="https://github.com/tolstoylife/tolstoy.life/tree/main/docs/research/lib"' in publish.link_sources_to_github(
        '<a href="/research/lib/">f</a>', page_dir, set(), {script})


def test_sitemap_lists_only_pages_as_full_addresses():
    import pathlib
    out = publish.sitemap([pathlib.PurePosixPath(p) for p in ["INDEX.html", "research/wiki/Henry George.html", "a.md", "x.css"]])

    assert "<loc>https://research.tolstoy.life/INDEX.html</loc>" in out
    assert "<loc>https://research.tolstoy.life/research/wiki/Henry%20George.html</loc>" in out
    assert ".md<" not in out and ".css<" not in out
    assert "Sitemap: https://research.tolstoy.life/sitemap.xml" in publish.ROBOTS
