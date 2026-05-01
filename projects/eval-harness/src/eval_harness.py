from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PromptCase:
    id: str
    title: str
    prompt: str
    required_terms: list[str]


@dataclass(frozen=True)
class ModelResponse:
    model: str
    prompt_id: str
    response: str


@dataclass(frozen=True)
class Score:
    model: str
    prompt_id: str
    prompt_title: str
    coverage: float
    structure: float
    specificity: float

    @property
    def total(self) -> float:
        return round(self.coverage * 0.6 + self.structure * 0.2 + self.specificity * 0.2, 2)


def load_prompts(path: Path) -> list[PromptCase]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        PromptCase(
            id=item["id"],
            title=item["title"],
            prompt=item["prompt"],
            required_terms=list(item["required_terms"]),
        )
        for item in raw
    ]


def load_responses(path: Path) -> list[ModelResponse]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        ModelResponse(
            model=item["model"],
            prompt_id=item["prompt_id"],
            response=item["response"],
        )
        for item in raw
    ]


def score_response(prompt: PromptCase, response: ModelResponse) -> Score:
    text = response.response
    lowered = text.lower()
    matched = sum(1 for term in prompt.required_terms if term.lower() in lowered)
    coverage = round(matched / max(len(prompt.required_terms), 1) * 100, 2)

    structure_markers = len(re.findall(r"(1[.、]|2[.、]|3[.、]|步骤|流程|先|再|最后|;|；)", text))
    structure = min(100.0, 35.0 + structure_markers * 13.0)

    concrete_markers = len(re.findall(r"(\d+|CSV|JSON|Markdown|SVG|token|diff|prompt|路径|命令|测试)", text, flags=re.I))
    specificity = min(100.0, 30.0 + concrete_markers * 10.0)

    return Score(
        model=response.model,
        prompt_id=response.prompt_id,
        prompt_title=prompt.title,
        coverage=coverage,
        structure=round(structure, 2),
        specificity=round(specificity, 2),
    )


def evaluate(prompts: list[PromptCase], responses: list[ModelResponse]) -> list[Score]:
    prompt_by_id = {prompt.id: prompt for prompt in prompts}
    scores = []
    for response in responses:
        prompt = prompt_by_id.get(response.prompt_id)
        if prompt is None:
            raise ValueError(f"Unknown prompt_id: {response.prompt_id}")
        scores.append(score_response(prompt, response))
    return scores


def average_by_model(scores: list[Score]) -> dict[str, float]:
    grouped: dict[str, list[float]] = {}
    for score in scores:
        grouped.setdefault(score.model, []).append(score.total)
    return {model: round(sum(values) / len(values), 2) for model, values in grouped.items()}


def render_markdown(scores: list[Score]) -> str:
    averages = average_by_model(scores)
    lines = [
        "# MiMo Agent Workflow Lab 评测报告",
        "",
        "## 模型平均分",
        "",
        "| 模型 | 平均分 |",
        "| --- | ---: |",
    ]
    for model, value in sorted(averages.items(), key=lambda item: item[1], reverse=True):
        lines.append(f"| {model} | {value:.2f} |")

    lines.extend(
        [
            "",
            "## 明细",
            "",
            "| Prompt | 模型 | 术语覆盖 | 结构化 | 具体性 | 总分 |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for score in sorted(scores, key=lambda item: (item.prompt_id, -item.total)):
        lines.append(
            f"| {score.prompt_title} | {score.model} | {score.coverage:.2f} | {score.structure:.2f} | {score.specificity:.2f} | {score.total:.2f} |"
        )

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "该报告用于记录同题 prompt 下不同模型输出的可解释评分，后续可接入 MiMo API，把真实响应写入 `runs/` 后重新生成报告。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(scores: list[Score], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "evaluation_report.md"
    csv_path = out_dir / "score_summary.csv"
    report_path.write_text(render_markdown(scores), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["prompt_id", "prompt_title", "model", "coverage", "structure", "specificity", "total"])
        for score in scores:
            writer.writerow(
                [
                    score.prompt_id,
                    score.prompt_title,
                    score.model,
                    f"{score.coverage:.2f}",
                    f"{score.structure:.2f}",
                    f"{score.specificity:.2f}",
                    f"{score.total:.2f}",
                ]
            )
    return report_path, csv_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate model responses for MiMo Orbit workflow cases.")
    parser.add_argument("--prompts", type=Path, required=True, help="Prompt suite JSON.")
    parser.add_argument("--responses", type=Path, required=True, help="Model responses JSON.")
    parser.add_argument("--out", type=Path, required=True, help="Output directory.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    prompts = load_prompts(args.prompts)
    responses = load_responses(args.responses)
    scores = evaluate(prompts, responses)
    report_path, csv_path = write_outputs(scores, args.out)
    print(f"Generated {report_path}")
    print(f"Generated {csv_path}")
    for model, value in sorted(average_by_model(scores).items(), key=lambda item: item[1], reverse=True):
        print(f"{model}: {value:.2f}")


if __name__ == "__main__":
    main()
