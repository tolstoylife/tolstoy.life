import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # docs/
import serve

def test_critic_deletion_renders_del():
    html = serve.render_body("a {--cut here--} b")
    assert "<del" in html and "cut here" in html

def test_critic_substitution_renders_old_and_new():
    html = serve.render_body("x {~~springs from~>is connected with~~} y")
    assert "springs from" in html and "is connected with" in html

def test_critic_comment_renders_note():
    html = serve.render_body("x {>>Chertkov softened this<<} y")
    assert "Chertkov softened this" in html

def test_footnote_renders():
    html = serve.render_body("Body text[^1]\n\n[^1]: the footnote")
    assert "the footnote" in html and ("footnote" in html)

def test_wikilink_renders_link():
    html = serve.render_body("the single tax that [[Henry George]] proposed")
    assert "Henry George" in html and "wikilink" in html


def test_front_page_credits_tolstoydigital_licence():
    html = serve.build_index(serve.merge_doc_files(serve.collect_md_files(), serve.collect_orphan_html_files()))
    assert "tolstoydigital" in html and "CC BY-SA 4.0" in html


def test_front_page_leads_with_reading():
    html = serve.build_index(serve.merge_doc_files(serve.collect_md_files(), serve.collect_orphan_html_files()))
    read_at = html.index("Read and listen")
    assert read_at < html.index('<iframe class="viz-frame"'), "the reading section comes before the timeline chart"
    assert read_at < html.index('<h2>Notes</h2>'), "the reading section comes before the dated notes"
    assert "/reader/non-fiction/personal-papers/confession/" in html
