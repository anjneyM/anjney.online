#!/usr/bin/env python3
"""Generate card.png (1200x630) — the Open Graph / Twitter card for anjney.online.

Usage: python3 tools/make-card.py
Requires: pip install pillow
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

# palette (mirrors index.html dark theme)
BG = (5, 5, 5)
INK = (244, 241, 232)
BODY = (201, 198, 187)
DIM = (139, 136, 125)
LINE = (35, 34, 29)
ACCENT = (84, 201, 140)

ROOT = Path(__file__).resolve().parent.parent

# fonts (macOS system fonts)
SERIF = "/System/Library/Fonts/Supplemental/Charter.ttc"
F_NAME = lambda: ImageFont.truetype(SERIF, 104)
F_TAG = lambda: ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 36)
F_ROLE = lambda: ImageFont.truetype(SERIF, 42)
F_EDU = lambda: ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 26)
F_SANS = lambda: ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 24)
F_DOMAIN = lambda: ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 22)


def draw_asterisk(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color, width: int):
    for k in range(3):
        a = math.radians(k * 60 + 90)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line([(cx - r * math.cos(a), cy - r * math.sin(a)), (x2, y2)], fill=color, width=width)


def draw_spaced(d: ImageDraw.ImageDraw, text: str, cx: int, y: int, font, color, spacing: int):
    """Center text with extra letter-spacing, using a manual character walk."""
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=color, anchor="la")
        x += w + spacing


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # hairline frame, inset — gives it the "card" feel
    m = 44
    d.rectangle([m, m, W - m - 1, H - m - 1], outline=LINE, width=1)

    # corner accents
    cr = 12
    for cx, cy in [(m + 26, m + 26), (W - m - 26, m + 26), (m + 26, H - m - 26), (W - m - 26, H - m - 26)]:
        draw_asterisk(d, cx, cy, cr, ACCENT, 2)

    cx = W // 2

    # top: green asterisk, echoes the site's rotating badge
    draw_asterisk(d, cx, 96, 34, ACCENT, 6)

    # name
    d.text((cx, 158), "Anjney Mital", font=F_NAME(), fill=INK, anchor="ma")

    # tagline
    d.text((cx, 292), "Tech policy, law & advocacy", font=F_TAG(), fill=BODY, anchor="ma")

    # divider
    d.line([(cx - 330, 348), (cx + 330, 348)], fill=LINE, width=1)

    # open to
    d.text((cx, 384), "OPEN TO", font=F_SANS(), fill=ACCENT, anchor="ma")
    draw_spaced(d, "TECH POLICY   ·   COMPLIANCE   ·   RESEARCH   ·   DATA PRIVACY", cx, 418, F_SANS(), DIM, 2)

    # divider
    d.line([(cx - 330, 496), (cx + 330, 496)], fill=LINE, width=1)

    # education
    d.text((cx, 522), "B.A. LL.B. — Symbiosis Law School, Hyderabad · 2021–2026", font=F_EDU(), fill=BODY, anchor="ma")

    # domain
    d.text((cx, 560), "anjney.online", font=F_DOMAIN(), fill=DIM, anchor="ma")

    out = ROOT / "card.png"
    img.save(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
