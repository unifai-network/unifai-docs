#!/usr/bin/env python3
"""
Convert GitBook-flavored markdown -> MkDocs Material.
Non-destructive: reads existing GitBook content at repo root, writes a parallel
copy into docs/. Existing GitBook files are left untouched.
"""
import os, re, shutil, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

# GitBook hint styles -> Material admonition types
HINT_MAP = {"info": "info", "warning": "warning", "danger": "danger",
            "success": "success", "note": "note", "tip": "tip"}

# Source markdown files (relative paths) taken from SUMMARY.md structure.
MD_FILES = [
    "README.md",
    "getting-started/transaction-fee-and-reward-system.md",
    "getting-started/guide-tutorials/README.md",
    "getting-started/guide-tutorials/publish-your-docs.md",
    "getting-started/guide-tutorials/how-to-copy-a-strategy.md",
    "getting-started/faq/README.md",
    "getting-started/faq/faq-defi-users.md",
    "getting-started/faq/faq-polymarket-strategies.md",
    "for-developers/getting-started.md",
    "for-developers/editor.md",
    "for-developers/understanding-tool-types.md",
    "for-developers/markdown.md",
    "for-developers/creating-toolkits.md",
    "for-developers/agent-documentation.md",
    "for-developers/faq-developers.md",
    "resources/social-and-community-links.md",
    "resources/branding-guidelines.md",
    "resources/our-community-voices.md",
    "tokenomics/distribution-and-vesting.md",
    "tokenomics/token-utility.md",
]

re_tabs      = re.compile(r'^\s*\{%\s*tabs\s*%\}\s*$')
re_endtabs   = re.compile(r'^\s*\{%\s*endtabs\s*%\}\s*$')
re_tab       = re.compile(r'^\s*\{%\s*tab\s+title="(.*?)"\s*%\}\s*$')
re_endtab    = re.compile(r'^\s*\{%\s*endtab\s*%\}\s*$')
re_hint      = re.compile(r'^\s*\{%\s*hint\s+style="(.*?)"\s*%\}\s*$')
re_endhint   = re.compile(r'^\s*\{%\s*endhint\s*%\}\s*$')
re_file      = re.compile(r'^\s*\{%\s*file\s+src="(.*?)"\s*%\}\s*$')
re_embed     = re.compile(r'^\s*\{%\s*embed\s+url="(.*?)"\s*%\}\s*$')


def strip_gitbook_frontmatter_keys(text):
    """Remove GitBook-only frontmatter keys (e.g. `icon:`) that Material would
    misinterpret as Material icon names and fail to resolve."""
    if not text.startswith('---'):
        return text
    parts = text.split('\n')
    # find closing '---' of the frontmatter block
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == '---':
            end = i
            break
    if end is None:
        return text
    fm = [ln for ln in parts[1:end] if not re.match(r'^\s*icon\s*:', ln)]
    return '\n'.join(['---'] + fm + ['---'] + parts[end + 1:])


# GitBook page slugs (as they appear in absolute docs.unifai.network links)
# mapped to their local MkDocs paths. GitBook slugs are not the file paths.
GITBOOK_SLUG_TO_LOCAL = {
    "agent": "/for-developers/agent-documentation/",
    "creating-toolkits": "/for-developers/creating-toolkits/",
}
_LIVE_LINK = re.compile(
    r'https://docs\.unifai\.network/(?P<slug>[A-Za-z0-9\-_/]+)(?P<frag>#[A-Za-z0-9\-_]+)?'
)


def _relpath_to_local(rel):
    """Map a source .md path to its built MkDocs URL (use_directory_urls)."""
    if rel == "README.md":
        return "/"
    p = rel[:-3] if rel.endswith(".md") else rel
    if p.endswith("/README"):
        p = p[: -len("README")]
    p = p.strip("/")
    return "/" + p + "/" if p else "/"


def fix_linebreaks(text):
    """GitBook uses a trailing backslash for a hard line break; Python-Markdown
    renders that backslash literally (visible '\\'). Convert prose `foo\\` ->
    `foo  ` (Markdown hard break). Fenced code blocks are left untouched."""
    out, in_code = [], False
    for line in text.split('\n'):
        s = line.lstrip()
        if s.startswith('```') or s.startswith('~~~'):
            in_code = not in_code
            out.append(line)
            continue
        if not in_code:
            r = line.rstrip()
            if r.endswith('\\') and not r.endswith('\\\\'):
                line = r[:-1] + '  '
        out.append(line)
    return '\n'.join(out)


def rewrite_live_links(text, rel):
    """Rewrite absolute docs.unifai.network links to local ones so they don't
    bounce users back to the old GitBook site. Same-page links collapse to a
    bare #anchor; cross-page links point to the local page."""
    cur = _relpath_to_local(rel)

    def repl(m):
        slug, frag = m.group("slug").strip("/"), m.group("frag") or ""
        local = GITBOOK_SLUG_TO_LOCAL.get(slug)
        if local is None:
            print("  WARN: unmapped docs.unifai.network link in %s: %s" % (rel, m.group(0)))
            return m.group(0)
        if local == cur and frag:
            return frag                      # same page -> in-page anchor
        return local + frag                  # cross-page -> local path

    return _LIVE_LINK.sub(repl, text)


def transform(text, relpath):
    text = strip_gitbook_frontmatter_keys(text)
    # 1) Rewrite relative .gitbook asset paths to root-absolute (raw HTML-safe).
    #    Target a non-dot dir because MkDocs excludes dot-directories from the build.
    text = re.sub(r'(?:\.\./)+\.gitbook/', '/gitbook/', text)
    # 1b) Rewrite absolute docs.unifai.network links to local paths/anchors.
    text = rewrite_live_links(text, relpath)
    # 1c) Strip GitBook "broken-reference" links (these are broken on GitBook
    #     too) down to plain text so we don't ship a dead link.
    text, n_broken = re.subn(r'\[([^\]]+)\]\(broken-reference\)', r'\1', text)
    if n_broken:
        print("  NOTE: %s had %d broken-reference link(s) -> stripped to text "
              "(needs a real URL)" % (relpath, n_broken))
    # 2) Let markdown inside <details> render (md_in_html).
    text = text.replace('<details>', '<details markdown="1">')

    out, indent = [], 0
    for line in text.split('\n'):
        if re_tabs.match(line) or re_endtabs.match(line):
            continue
        if re_endtab.match(line) or re_endhint.match(line):
            indent = max(0, indent - 4)
            continue
        m = re_tab.match(line)
        if m:
            out.append(' ' * indent + '=== "%s"' % m.group(1))
            out.append('')
            indent += 4
            continue
        m = re_hint.match(line)
        if m:
            out.append(' ' * indent + '!!! ' + HINT_MAP.get(m.group(1), 'note'))
            out.append('')
            indent += 4
            continue
        m = re_file.match(line)
        if m:
            p = m.group(1)
            enc = urllib.parse.quote(p, safe="/")
            out.append(' ' * indent + '[⬇️ %s](%s){:download}' %
                       (os.path.basename(p), enc))
            out.append('')
            continue
        m = re_embed.match(line)
        if m:
            u = m.group(1)
            if "x.com" in u or "twitter.com" in u:
                # Real X/Twitter embed — widgets.js (loaded via extra_javascript)
                # upgrades this blockquote into a rendered tweet card.
                out.append(' ' * indent +
                           '<blockquote class="twitter-tweet" data-dnt="true" '
                           'data-conversation="none"><a href="%s"></a></blockquote>' % u)
            else:
                out.append(' ' * indent + '[Open link →](%s)' % u)
            out.append('')
            continue
        # Default: indent content while inside a tab/hint block.
        if indent and line.strip():
            out.append(' ' * indent + line)
        else:
            out.append(line if line.strip() else '')

    if indent != 0:
        print("  WARNING: unbalanced tab/hint blocks in %s (indent=%d)" % (relpath, indent))
    return fix_linebreaks('\n'.join(out))


EXTRA_CSS = """/* Tuned to match the live GitBook site (docs.unifai.network).
   Text colors flow through Material's scheme-aware --md-* tokens (so dark mode
   stays readable); only the token VALUES are pinned per scheme. Light-mode
   values were measured from the live DOM. */

/* ---- Light scheme: pinned to measured GitBook values ---- */
[data-md-color-scheme="default"] {
  --md-primary-fg-color:        #ffffff;   /* white header background */
  --md-primary-bg-color:        #1d1d1f;   /* dark text/icons on the header */
  --md-accent-fg-color:         #7b8af5;   /* GitBook periwinkle accent */
  --md-typeset-a-color:         #7b8af5;   /* content links (measured) */
  --md-default-fg-color:        #1d1d1f;   /* body text (measured) */
  --md-default-fg-color--light: #6c6e76;   /* subtitle / TOC / inactive tabs (measured) */

  /* GitBook has no dark footer band — make the footer light */
  --md-footer-bg-color:        #ffffff;
  --md-footer-bg-color--dark:  #fafafa;
  --md-footer-fg-color:        #1d1d1f;
  --md-footer-fg-color--light: #6c6e76;
  --md-footer-fg-color--lighter: #9aa0a6;
}

/* ---- Dark scheme: on-brand near-black + brighter periwinkle (text/fg stay
   Material's light slate defaults so everything remains readable) ---- */
[data-md-color-scheme="slate"] {
  --md-primary-fg-color: #0C0C0E;
  --md-accent-fg-color:  #8b9cff;
  --md-typeset-a-color:  #8b9cff;
  --md-default-bg-color: #0C0C0E;
}

/* ---- Structure (scheme-agnostic): borders use the adaptive --lightest token ---- */
.md-header { box-shadow: none; border-bottom: 1px solid var(--md-default-fg-color--lightest); }
.md-footer-meta { border-top: 1px solid var(--md-default-fg-color--lightest); }

/* Headings: bold + full-strength text color (Material defaults to light-300 gray) */
.md-typeset h1 {
  font-size: 2.25rem;      /* 36px */
  line-height: 1.25;       /* ~45px */
  font-weight: 700;
  color: var(--md-default-fg-color);
  letter-spacing: 0;
}
.md-typeset h2 { font-weight: 700; color: var(--md-default-fg-color); }
.md-typeset h3 { font-weight: 600; color: var(--md-default-fg-color); }

/* GitBook article header: section eyebrow above H1 + description subtitle below
   (both injected by hooks/gitbook_shim.py) */
.md-typeset .gb-eyebrow {
  text-transform: uppercase; font-size: 12px; font-weight: 700;
  letter-spacing: .04em; color: var(--md-accent-fg-color); margin: 0 0 .5rem;
}
.md-typeset .gb-subtitle {
  font-size: 18px; line-height: 1.55; color: var(--md-default-fg-color--light); margin: .4rem 0 1.6rem;
}

/* Left sidebar section labels — measured: uppercase 12px / 600 */
.md-nav--primary .md-nav__item--section > .md-nav__link,
.md-nav--primary .md-nav__item--section > label {
  text-transform: uppercase; font-size: 12px; font-weight: 600;
  letter-spacing: .3px; color: var(--md-default-fg-color);
}
.md-nav__link--active,
.md-nav__link--active:hover,
.md-nav--secondary .md-nav__link--active { color: var(--md-accent-fg-color); }

/* Right TOC title — measured: sentence case 14px / 400 */
.md-nav--secondary .md-nav__title {
  text-transform: none; font-size: 14px; font-weight: 400;
  letter-spacing: normal; color: var(--md-default-fg-color--light);
}

/* Tabs — measured: gray inactive / strong active, weight 500, 14px, NO underline */
.md-typeset .tabbed-labels > label { color: var(--md-default-fg-color--light); font-weight: 500; font-size: 14px; }
.md-typeset .tabbed-set > input:checked + label { color: var(--md-default-fg-color); font-weight: 500; }
.md-typeset .tabbed-labels::before { display: none; }   /* GitBook active tab has no underline */

/* Content column width — measured: GitBook text column ~768px (Material default is narrower) */
.md-grid { max-width: 66rem; }

/* GitBook-style floating theme switcher (bottom-right); Material's header toggle is hidden */
.md-header [data-md-component="palette"] { display: none; }
.gb-theme-toggle {
  position: fixed; right: 1.5rem; bottom: 1.5rem; z-index: 6;
  display: flex; gap: .15rem; padding: .25rem;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 999px; box-shadow: 0 2px 8px rgba(0,0,0,.12);
}
.gb-theme-toggle button {
  width: 1.9rem; height: 1.9rem; border: 0; border-radius: 999px; cursor: pointer;
  background: transparent; color: var(--md-default-fg-color--light);
  font-size: .95rem; line-height: 1; display: inline-flex; align-items: center; justify-content: center;
}
.gb-theme-toggle button:hover { color: var(--md-default-fg-color); }
.gb-theme-toggle button.active { background: var(--md-accent-fg-color); color: #fff; }

/* Search: centered rounded pill with a Cmd-K hint (desktop), like GitBook */
@media screen and (min-width: 76.25em) {
  .md-header__inner { position: relative; }
  .md-search { position: absolute; left: 50%; transform: translateX(-50%); }
  .md-search__form { width: 460px; height: 40px; border-radius: 22px; box-shadow: none; }
  [data-md-color-scheme="default"] .md-search__form { background-color: #ffffff; border: 1px solid #e5e7eb; }
  [data-md-color-scheme="slate"]   .md-search__form { background-color: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.16); }
  .md-search__input::placeholder { color: #9aa0a6; }
  .md-search__form::after {
    content: "\\2318 K"; position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
    font-size: 11px; line-height: 1; color: #9aa0a6; background: rgba(127,127,127,.14);
    border: 1px solid rgba(127,127,127,.30); border-radius: 6px; padding: 3px 6px; pointer-events: none;
  }
  .md-search__form:focus-within::after { display: none; }
}

/* FAQ <details> clean accordion */
.md-typeset details { border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; box-shadow: none; }
.md-typeset details > summary { font-weight: 600; }

/* Figures */
.md-typeset figure img, .md-typeset p > img { border-radius: 8px; max-width: 100%; }
"""


JS_TOGGLE = """// GitBook-style floating theme switcher. Reuses Material's own palette radio
// inputs (#__palette_0 light / #__palette_1 dark) so scheme switching and
// localStorage persistence stay handled by Material.
document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector(".gb-theme-toggle")) return;
  var wrap = document.createElement("div");
  wrap.className = "gb-theme-toggle";
  wrap.innerHTML =
    '<button type="button" data-scheme="default" aria-label="Light mode">\\u2600</button>' +
    '<button type="button" data-scheme="slate" aria-label="Dark mode">\\u263e</button>';
  document.body.appendChild(wrap);
  var btns = wrap.querySelectorAll("button");
  function sync() {
    var s = document.body.getAttribute("data-md-color-scheme");
    btns.forEach(function (b) { b.classList.toggle("active", b.dataset.scheme === s); });
  }
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      var input = document.getElementById("__palette_" + (b.dataset.scheme === "slate" ? "1" : "0"));
      if (input) { input.click(); }
      else { document.body.setAttribute("data-md-color-scheme", b.dataset.scheme); }
    });
  });
  sync();
  new MutationObserver(sync).observe(document.body, {
    attributes: true, attributeFilter: ["data-md-color-scheme"],
  });
});
"""


def main():
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

    for rel in MD_FILES:
        src = os.path.join(ROOT, rel)
        if not os.path.exists(src):
            print("  MISSING:", rel)
            continue
        dst_rel = "index.md" if rel == "README.md" else rel
        dst = os.path.join(DOCS, dst_rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(src, encoding="utf-8") as f:
            text = f.read()
        with open(dst, "w", encoding="utf-8") as f:
            f.write(transform(text, rel))
        print("  ok:", rel, "->", dst_rel)

    # Copy assets to a non-dot dir so /gitbook/ paths resolve under the built site.
    src_assets = os.path.join(ROOT, ".gitbook", "assets")
    dst_assets = os.path.join(DOCS, "gitbook", "assets")
    if os.path.isdir(src_assets):
        shutil.copytree(src_assets, dst_assets)
        print("  assets copied:", dst_assets)
        # No-spaces alias used as the theme logo/favicon.
        single = os.path.join(dst_assets, "unifai logo single.png")
        if os.path.exists(single):
            shutil.copyfile(single, os.path.join(dst_assets, "logo-single.png"))
            print("  logo alias: gitbook/assets/logo-single.png")

    # Brand stylesheet (referenced by mkdocs.yml -> extra_css).
    css_dir = os.path.join(DOCS, "stylesheets")
    os.makedirs(css_dir, exist_ok=True)
    with open(os.path.join(css_dir, "extra.css"), "w", encoding="utf-8") as f:
        f.write(EXTRA_CSS)
    print("  wrote stylesheets/extra.css")

    js_dir = os.path.join(DOCS, "js")
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, "theme-toggle.js"), "w", encoding="utf-8") as f:
        f.write(JS_TOGGLE)
    print("  wrote js/theme-toggle.js")

    print("Done. %d files." % len(MD_FILES))


if __name__ == "__main__":
    main()
