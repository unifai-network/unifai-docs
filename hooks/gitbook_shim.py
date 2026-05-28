"""MkDocs hook to mimic GitBook's article header:
  - an UPPERCASE section "eyebrow" above the H1 (the top-level nav section)
  - the page `description` rendered as a gray subtitle below the H1
Both are things GitBook renders that Material does not.
"""
import re
import html as _html

_H1 = re.compile(r"<h1[^>]*>.*?</h1>", re.S | re.I)


def _top_section_title(page):
    """Walk up the nav parents to the outermost section title."""
    node = getattr(page, "parent", None)
    top = None
    while node is not None:
        top = node
        node = getattr(node, "parent", None)
    return getattr(top, "title", None) if top else None


def on_page_content(html, page=None, config=None, files=None, **kwargs):
    if page is None or not html:
        return html
    m = _H1.search(html)
    if not m:
        return html

    eyebrow = _top_section_title(page)
    desc = (getattr(page, "meta", None) or {}).get("description")

    pre = (
        '<p class="gb-eyebrow">%s</p>' % _html.escape(str(eyebrow))
        if eyebrow
        else ""
    )
    post = (
        '<p class="gb-subtitle">%s</p>' % _html.escape(" ".join(str(desc).split()))
        if desc
        else ""
    )
    if not pre and not post:
        return html

    return html[: m.start()] + pre + m.group(0) + post + html[m.end():]
