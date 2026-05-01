from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "proof" / "screenshots"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_to_width(draw: ImageDraw.ImageDraw, line: str, max_width: int, active_font) -> list[str]:
    parts = []
    token = ""
    for ch in line:
        if ch.isascii() and (ch.isalnum() or ch in "/._+-"):
            token += ch
        else:
            if token:
                parts.append(token)
                token = ""
            parts.append(ch)
    if token:
        parts.append(token)

    lines = []
    current = ""
    for part in parts:
        probe = current + part
        if draw.textbbox((0, 0), probe, font=active_font)[2] <= max_width:
            current = probe
        else:
            if current:
                lines.append(current)
            current = part
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, max_width: int, body_font, fill) -> int:
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            y += 18
            continue
        if line.startswith("# "):
            draw.text((x, y), line[2:], font=font(36, True), fill=(23, 32, 31))
            y += 52
            continue
        if line.startswith("## "):
            draw.text((x, y), line[3:], font=font(27, True), fill=(8, 127, 140))
            y += 40
            continue

        for wrapped in wrap_to_width(draw, line, max_width, body_font):
            draw.text((x, y), wrapped, font=body_font, fill=fill)
            y += 31
    return y


def render_card(title: str, subtitle: str, source: Path, out: Path) -> None:
    text = source.read_text(encoding="utf-8")
    width = 1400
    body_font = font(22)
    temp = Image.new("RGB", (width, 2000), (246, 247, 251))
    temp_draw = ImageDraw.Draw(temp)
    content_bottom = draw_text_block(temp_draw, text, 72, 190, width - 150, body_font, (49, 58, 56))
    height = max(860, content_bottom + 80)

    img = Image.new("RGB", (width, height), (246, 247, 251))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((44, 42, width - 44, height - 42), radius=8, fill=(255, 255, 255), outline=(217, 226, 223), width=2)
    draw.text((72, 72), title, font=font(44, True), fill=(23, 32, 31))
    draw.text((72, 128), subtitle, font=font(22), fill=(102, 113, 111))
    draw.line((72, 170, width - 72, 170), fill=(217, 226, 223), width=2)
    draw_text_block(draw, text, 72, 200, width - 150, body_font, (49, 58, 56))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=95)
    print(out)


def main() -> None:
    render_card(
        "Data Report Agent 输出证明",
        "由 projects/data-report-agent 从 CSV 生成的 Markdown 报告",
        ROOT / "proof" / "data-report-demo" / "report.md",
        SCREENSHOTS / "data-report-output.png",
    )
    render_card(
        "Eval Harness 输出证明",
        "由 projects/eval-harness 从 prompt suite 和 responses 生成的评测报告",
        ROOT / "proof" / "eval-demo" / "evaluation_report.md",
        SCREENSHOTS / "eval-report-output.png",
    )


if __name__ == "__main__":
    main()
