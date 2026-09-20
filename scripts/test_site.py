"""Check the public demo, source fidelity, links and skill download package."""
import importlib.util
import json
import re
import struct
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("build_site", Path(__file__).with_name("build-site.py"))
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.metas = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        for name in ("href", "src"):
            if attributes.get(name):
                self.links.append(attributes[name])
        if tag == "meta":
            self.metas[attributes.get("property", attributes.get("name"))] = attributes.get("content")


class SiteTests(unittest.TestCase):
    def test_share_image_is_real_png_with_expected_dimensions(self):
        data = (BUILDER.OUTPUT / "assets/social-preview.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", data[16:24]), (1280, 640))
        self.assertLess(len(data), 1_000_000)

    def test_examples_keep_declared_facts_and_numbers(self):
        examples = BUILDER.validate_examples(BUILDER.skill_metadata())
        self.assertEqual(len(examples), 7)
        self.assertEqual(sum(item.get("kind") == "question" for item in examples), 1)

    def test_catalog_is_derived_from_the_skill(self):
        actual = json.loads((BUILDER.OUTPUT / "assets/rules.json").read_text(encoding="utf-8"))
        self.assertEqual(actual, BUILDER.skill_metadata())

    def test_zip_contains_exact_canonical_files(self):
        with zipfile.ZipFile(BUILDER.OUTPUT / "downloads/jusmanizer.zip") as package:
            self.assertEqual(set(package.namelist()), {f"jusmanizer/{name}" for name in BUILDER.PACKAGE_FILES})
            for name in BUILDER.PACKAGE_FILES:
                self.assertEqual(package.read(f"jusmanizer/{name}"), (BUILDER.ROOT / name).read_bytes())
        self.assertEqual((BUILDER.OUTPUT / "downloads/SKILL.md").read_bytes(), (BUILDER.ROOT / "SKILL.md").read_bytes())

    def test_page_links_and_share_metadata(self):
        parser = PageParser()
        parser.feed((BUILDER.OUTPUT / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for link in parser.links:
            if link.startswith("#") and link != "#":
                self.assertIn(link[1:], parser.ids)
            elif not re.match(r"https?://", link) and not link.startswith("#"):
                self.assertTrue((BUILDER.OUTPUT / link).is_file(), link)
        self.assertEqual(parser.metas["og:image"], "https://brunoflma.github.io/jusmanizer/assets/social-preview.png")
        self.assertEqual(parser.metas["twitter:card"], "summary_large_image")


if __name__ == "__main__":
    unittest.main()
