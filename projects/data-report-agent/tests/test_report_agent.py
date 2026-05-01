from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from report_agent import WorkflowRecord, render_markdown, render_svg_chart, summarize, write_outputs


class ReportAgentTests(unittest.TestCase):
    def sample_records(self) -> list[WorkflowRecord]:
        return [
            WorkflowRecord("A", "数据分析", 2, 100, 50, 0.5, 2, True),
            WorkflowRecord("B", "模型评测", 1, 200, 100, 0.0, 1, False),
        ]

    def test_summarize_counts_tokens_and_public_outputs(self) -> None:
        summary = summarize(self.sample_records())

        self.assertEqual(summary["cases"], 3)
        self.assertEqual(summary["public_outputs"], 1)
        self.assertGreater(summary["total_tokens"], 0)

    def test_render_markdown_contains_application_context(self) -> None:
        markdown = render_markdown(self.sample_records())

        self.assertIn("MiMo Agent Workflow Lab", markdown)
        self.assertIn("预计 token", markdown)
        self.assertIn("| A |", markdown)

    def test_write_outputs_creates_report_and_chart(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, chart = write_outputs(self.sample_records(), Path(tmp))

            self.assertTrue(report.exists())
            self.assertTrue(chart.exists())
            self.assertIn("<svg", render_svg_chart(self.sample_records()))


if __name__ == "__main__":
    unittest.main()
