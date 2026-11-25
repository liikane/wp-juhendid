import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_links import check_links


class CheckLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_relative_markdown_and_unicode_html_anchors(self):
        self.write(
            "README.md",
            "# Juhend\n\n[HTML](docs/cheat.html#r%C3%B5hutused)\n"
            "[Markdown](docs/guide.md#määrang)\n[Inline code](docs/guide.md#koodinäide)",
        )
        self.write("docs/cheat.html", '<h2 id="rõhutused">Rõhutused</h2>')
        self.write("docs/guide.md", "# Määrang\n\n## `Koodinäide`")

        self.assertEqual(check_links(self.root), [])

    def test_reports_missing_files_and_anchors(self):
        self.write("README.md", "[Puuduv](nope.md)\n[Ankur](guide.md#puudub)")
        self.write("guide.md", "# Olemas")

        errors = check_links(self.root)

        self.assertEqual(len(errors), 2)
        self.assertIn("missing target", errors[0])
        self.assertIn("missing anchor", errors[1])

    def test_ignores_code_examples_and_external_links(self):
        self.write(
            "README.md",
            "# Näidis\n"
            "[Välislink](https://example.com)\n"
            "`[inline](missing.md)`\n"
            "```md\n[code](also-missing.md)\n# fake-anchor\n```\n"
            "<a href=\"https://example.org\">Välislink</a>\n",
        )

        self.assertEqual(check_links(self.root), [])

    def test_checks_html_hrefs_and_srcs(self):
        self.write(
            "index.html",
            '<a href="missing.md">Link</a><img src="absent.png">'
            '<pre><code><a href="ignored.md" id="fake">Näidis</a></code></pre>',
        )

        errors = check_links(self.root)

        self.assertEqual(len(errors), 2)
        self.assertTrue(all("missing target" in error for error in errors))

    def test_checks_reference_style_markdown_destinations(self):
        self.write("README.md", "[guide]: docs/guide.md\n[guide]\n")
        self.write("docs/guide.md", "# Juhend")

        self.assertEqual(check_links(self.root), [])


if __name__ == "__main__":
    unittest.main()
