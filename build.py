#!/usr/bin/env python3
"""Stitches content/*.html + templates/*.html into the static site.

Add a chapter:
  1. Write content/0N-slug.html (see README for the expected shape).
  2. Add an entry to manifest.json.
  3. Run `python3 build.py`, then commit the generated output.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SECTION_OPEN_RE = re.compile(r'<section\b([^>]*)>', re.DOTALL)
H2_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.DOTALL)
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')
TAG_RE = re.compile(r'<[^>]+>')


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, text):
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def extract_sections(content_html):
    """Returns [{id, group, badge, heading}] in document order, by reading
    each <section>'s own attributes and the first <h2> that follows it."""
    sections = []
    for m in SECTION_OPEN_RE.finditer(content_html):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        if "id" not in attrs:
            continue
        h2 = H2_RE.search(content_html, m.end())
        heading = TAG_RE.sub("", h2.group(1)).strip() if h2 else attrs["id"]
        sections.append({
            "id": attrs["id"],
            "group": attrs.get("data-group", ""),
            "badge": attrs.get("data-badge", ""),
            "heading": heading,
        })
    return sections


def render_section_nav(sections):
    out = []
    last_group = None
    for s in sections:
        if s["group"] and s["group"] != last_group:
            out.append(f'    <div class="grp">{s["group"]}</div>')
            last_group = s["group"]
        out.append(
            f'    <a href="#{s["id"]}"><span class="n">{s["badge"]}</span>'
            f'<span>{s["heading"]}</span></a>'
        )
    return "\n".join(out)


def render_chapter_nav(manifest, active_file):
    out = []
    for ch in manifest:
        cls = ' class="active"' if ch["file"] == active_file else ""
        out.append(f'    <a{cls} href="{ch["file"]}">'
                    f'<span class="n">{ch["id"]}</span><span>{ch["title"]}</span></a>')
    return "\n".join(out)


def render_index_cards(manifest):
    out = []
    for ch in manifest:
        out.append(
            '  <a class="card" href="chapters/{file}">\n'
            '    <span class="n">{id}</span>\n'
            '    <div>\n'
            '      <span class="eyebrow">{eyebrow}</span>\n'
            '      <h2>{title}</h2>\n'
            '      <p>{description}</p>\n'
            '    </div>\n'
            '  </a>'.format(**ch)
        )
    return "\n".join(out)


def fill(template, values):
    for key, val in values.items():
        template = template.replace("{{" + key + "}}", val)
    return template


def build():
    manifest = json.loads(read("manifest.json"))
    page_template = read("templates/page.html")

    for ch in manifest:
        content = read(f"content/{ch['file']}")
        sections = extract_sections(content)
        page = fill(page_template, {
            "TITLE": ch["title"],
            "DESCRIPTION": ch["description"],
            "CHAPTER_NAV": render_chapter_nav(manifest, ch["file"]),
            "SECTION_NAV": render_section_nav(sections),
            "CONTENT": content,
        })
        write(f"chapters/{ch['file']}", page)
        print(f"built chapters/{ch['file']}")

    index_template = read("templates/index.html")
    index = fill(index_template, {"CHAPTERS": render_index_cards(manifest)})
    write("index.html", index)
    print("built index.html")


if __name__ == "__main__":
    build()
