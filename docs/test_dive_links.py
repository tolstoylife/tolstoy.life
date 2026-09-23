"""Self-check for serve.py's dive cross-link resolver.

The 2026-07 folder move relocated dives into nested subcats; serve.py rewrites the
flat-era `../<slug>/…` links to their real location at render time. Run after
touching resolve_dive_links / _dive_alias:  python3 docs/test_dive_links.py
"""
import serve


def check():
    alias = serve._dive_alias()

    # A flat `../<slug>/` link to a nested work dive resolves to its real path, computed from the same alias rather than a hard-coded slug.
    slug, real = next((s, p) for s, p in alias.items() if p.startswith("research/works/"))
    out = serve.resolve_dive_links(f'<a href="../{slug}/index.html">x</a>')
    assert f'href="/{real}/index.html"' in out, f"{slug} should resolve to /{real}/"

    # A URL fragment survives the rewrite.
    frag = serve.resolve_dive_links(f'<a href="../{slug}/index.html#s5">x</a>')
    assert f'/{real}/index.html#s5"' in frag, "fragment should be preserved"

    # An out-of-docs website/ pointer is left exactly as authored; rewriting it would only invent a wrong path.
    src = '<a href="../../../website/src/posts/notes/x.md">x</a>'
    assert serve.resolve_dive_links(src) == src, "website link must be left as-is"

    print(f"dive-link resolver OK (sample: ../{slug}/ -> /{real}/)")


if __name__ == "__main__":
    check()
