"""Dependency-free checks for the public static site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / name for name in ("index.html", "privacy.html", "contact.html")]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.duplicate_ids = set()
        self.has_title = False
        self.has_description = False
        self.has_main = False
        self.has_lang = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get("id"):
            if data["id"] in self.ids:
                self.duplicate_ids.add(data["id"])
            self.ids.add(data["id"])
        if tag == "html":
            self.has_lang = bool(data.get("lang"))
        if tag == "title":
            self.has_title = True
        if tag == "main":
            self.has_main = True
        if tag == "meta" and data.get("name") == "description":
            self.has_description = bool(data.get("content"))
        for attr in ("href", "src"):
            if data.get(attr):
                self.links.append(data[attr])


def main():
    errors = []
    parsed = {}
    for page in PAGES:
        if not page.is_file():
            errors.append(f"Missing page: {page.name}")
            continue
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed[page] = parser
        for label, present in (("lang", parser.has_lang), ("title", parser.has_title),
                               ("description", parser.has_description), ("main", parser.has_main)):
            if not present:
                errors.append(f"{page.name}: missing {label}")
        for duplicate in parser.duplicate_ids:
            errors.append(f"{page.name}: duplicate id {duplicate}")
    for page, parser in parsed.items():
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith("mailto:"):
                continue
            target = ROOT / unquote(url.path) if url.path else page
            if url.path.startswith("/"):
                errors.append(f"{page.name}: root-relative link {link}")
                continue
            if url.path and not target.is_file():
                errors.append(f"{page.name}: missing target {link}")
            elif url.fragment and target in parsed and url.fragment not in parsed[target].ids:
                errors.append(f"{page.name}: missing fragment {link}")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    if css.count("{") != css.count("}"):
        errors.append("styles.css: unbalanced braces")
    if "prefers-reduced-motion" not in css:
        errors.append("styles.css: reduced-motion rule missing")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(parsed)} pages; structure and internal links valid")


if __name__ == "__main__":
    main()
