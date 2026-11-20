"""Protect the live section from incorrect statuses and accidental rewrites."""

import unittest

from update_profile import END, START, escape_cell, render, replace_section


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
        self.assertIn("🟢&nbsp;Open", output)
        self.assertIn("🟣&nbsp;Merged", output)
        self.assertIn("⚪&nbsp;Closed", output)

    def test_own_repositories_are_not_upstream_contributions(self):
        output = render([pr(owner="ritesh17RB"), pr(2)])
        self.assertNotIn("ritesh17RB", output)
        self.assertIn("#2", output)

    def test_latest_four_are_preserved_in_api_order(self):
        output = render([pr(number) for number in range(1, 7)])
        self.assertIn("#4", output)
        self.assertNotIn("#5", output)

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
