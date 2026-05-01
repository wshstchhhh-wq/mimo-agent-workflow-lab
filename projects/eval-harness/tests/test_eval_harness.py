from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eval_harness import ModelResponse, PromptCase, average_by_model, evaluate, render_markdown, write_outputs


class EvalHarnessTests(unittest.TestCase):
    def sample_prompt(self) -> PromptCase:
        return PromptCase(
            id="case",
            title="Case",
            prompt="Explain CSV report flow",
            required_terms=["CSV", "Markdown", "token"],
        )

    def test_evaluate_scores_required_term_coverage(self) -> None:
        scores = evaluate(
            [self.sample_prompt()],
            [ModelResponse("model-a", "case", "读取 CSV，生成 Markdown，并记录 token。")],
        )

        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0].coverage, 100.0)
        self.assertGreater(scores[0].total, 70)

    def test_average_by_model(self) -> None:
        scores = evaluate(
            [self.sample_prompt()],
            [
                ModelResponse("model-a", "case", "CSV Markdown token"),
                ModelResponse("model-a", "case", "CSV"),
            ],
        )

        self.assertIn("model-a", average_by_model(scores))

    def test_write_outputs(self) -> None:
        scores = evaluate([self.sample_prompt()], [ModelResponse("model-a", "case", "CSV Markdown token")])
        with tempfile.TemporaryDirectory() as tmp:
            report, csv_path = write_outputs(scores, Path(tmp))

            self.assertTrue(report.exists())
            self.assertTrue(csv_path.exists())
            self.assertIn("评测报告", render_markdown(scores))


if __name__ == "__main__":
    unittest.main()
