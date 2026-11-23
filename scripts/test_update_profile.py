"""Protect the live section from incorrect statuses and accidental rewrites."""

import unittest

from update_profile import END, START, escape_cell, render, render_projects, replace_section
from render_artwork import hero, project_card
import xml.etree.ElementTree as ET


def pr(number=1, owner="upstream", state="open", merged=False, title="Fix a bug"):
    return {
        "html_url": f"https://github.com/{owner}/project/pull/{number}",
        "title": title,
        "state": state,
        "pull_request": {"merged_at": "2026-11-20T00:00:00Z" if merged else None},
    }


class ProfileTests(unittest.TestCase):
    def test_merged_open_and_closed_are_distinct(self):
        output = render([pr(), pr(2, state="closed", merged=True), pr(3, state="closed")])
        self.assertIn("| Open |", output)
        self.assertIn("| Merged |", output)
        self.assertIn("| Closed |", output)

    def test_own_repositories_are_not_upstream_contributions(self):
        output = render([pr(owner="ritesh17RB"), pr(2)])
        self.assertNotIn("ritesh17RB", output)
        self.assertIn("#2", output)

    def test_latest_six_are_preserved_in_api_order(self):
        output = render([pr(number) for number in range(1, 8)])
        self.assertIn("#6", output)
        self.assertNotIn("#7", output)

    def test_recent_open_work_does_not_hide_merged_contributions(self):
        output = render([pr(n) for n in range(1, 9)] + [pr(20, state="closed", merged=True)])
        self.assertLess(output.index("#20"), output.index("#1"))
        self.assertIn("#5", output)
        self.assertNotIn("#6", output)

    def test_duplicate_pull_requests_are_only_shown_once(self):
        output = render([pr(), pr()])
        self.assertEqual(output.count("#1"), 1)

    def test_generated_artwork_escapes_repository_text(self):
        project = {"name": "tool & helpers", "description": 'Compare <schema> & "types"', "language": "C++"}
        for dark in (True, False):
            for mobile in (True, False):
                root = ET.fromstring(project_card(project, dark, mobile))
                self.assertIn('Compare <schema> & "types"', ''.join(root.itertext()))
                ET.fromstring(hero({"merged_count": 7, "open_count": 2, "updated_at": "23 Nov 2026"}, dark, mobile))

    def test_project_cards_reject_unexpected_repositories(self):
        with self.assertRaises(ValueError):
            render_projects([{"name": "../unexpected", "url": "https://example.com"}])

    def test_titles_cannot_break_table_or_link_markup(self):
        self.assertEqual(escape_cell("[fix] | <b>\nnext"), r"\[fix\] &#124; &lt;b&gt; next")

    def test_non_github_urls_are_rejected(self):
        item = pr()
        item["html_url"] = "https://example.com/owner/project/pull/1"
        with self.assertRaises(ValueError):
            render([item])

    def test_empty_response_keeps_existing_content(self):
        with self.assertRaises(ValueError):
            render([])

    def test_only_managed_section_changes_and_refresh_is_idempotent(self):
        original = f"Personal introduction\n{START}\nold\n{END}\nHandwritten projects\n"
        updated = replace_section(original, render([pr()]))
        self.assertTrue(updated.startswith("Personal introduction\n"))
        self.assertTrue(updated.endswith("\nHandwritten projects\n"))
        self.assertEqual(updated, replace_section(updated, render([pr()])))

    def test_missing_duplicate_or_reversed_markers_are_rejected(self):
        for template in ("no markers", f"{START}{START}{END}", f"{END}{START}"):
            with self.subTest(template=template), self.assertRaises(ValueError):
                replace_section(template, "new")


if __name__ == "__main__":
    unittest.main()
