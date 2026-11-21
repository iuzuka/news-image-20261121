#!/usr/bin/env python3
"""Compose the 21 November 2026 newspaper front page (entry.png).

Fresh implementation: PIL composites the two generated press-style
illustrations in assets/ with programmatic typesetting (no AI text).

Run:  python3 draw_news21.py   -> writes entry.png (1024x1024, < 1 MiB)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
W, H = 1024, 1024
MARGIN = 20

PAPER = (247, 242, 231)
NAVY = (28, 36, 64)
GOLD = (201, 162, 39)
RED = (176, 58, 46)
INK = (18, 18, 18)
FRAME = (30, 30, 30)
WHITE = (255, 255, 255)

SERIF = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
SERIF_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SANS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
SANS_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

_font_cache = {}


def font(paths, size):
    """First usable font from the candidate list, cached per size."""
    key = (tuple(paths), size)
    if key in _font_cache:
        return _font_cache[key]
    for path in paths:
        try:
            found = ImageFont.truetype(path, size)
            _font_cache[key] = found
            return found
        except (OSError, IOError):
            continue
    found = ImageFont.load_default()
    _font_cache[key] = found
    return found


def fit(paths, text, start, width, minimum=10):
    """Largest font size (<= start) at which text fits inside width."""
    size = start
    while size > minimum:
        candidate = font(paths, size)
        if candidate.getlength(text) <= width:
            return candidate
        size -= 1
    return font(paths, minimum)


def tracked_width(f, text, tracking):
    return sum(f.getlength(ch) for ch in text) + tracking * max(0, len(text) - 1)


def draw_tracked(d, cx, y, text, f, fill, tracking):
    """Draw text centred on cx with extra space between letters."""
    total = tracked_width(f, text, tracking)
    x = cx - total / 2
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking


def cover(img, w, h, fx=0.5, fy=0.5):
    """Scale the image to cover w x h, then crop around the focus point."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    cx = min(max(fx * nw, w / 2), nw - w / 2)
    cy = min(max(fy * nh, h / 2), nh - h / 2)
    return img.crop((round(cx - w / 2), round(cy - h / 2),
                     round(cx + w / 2), round(cy + h / 2)))


def place_photo(page, box, path, focus=(0.5, 0.5)):
    """Paste an illustration into box, cover-cropped, with a thin frame."""
    x0, y0, x1, y1 = box
    with Image.open(path) as im:
        im = cover(im.convert("RGB"), x1 - x0, y1 - y0, *focus)
    page.paste(im, (x0, y0))
    d = ImageDraw.Draw(page)
    d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=FRAME, width=2)


def headline(d, lines, x, y, width, start, leading):
    """Bold serif headline; size shrinks until the widest line fits."""
    probe = font(SERIF_BOLD, start)
    widest = max(lines, key=lambda s: probe.getlength(s))
    f = fit(SERIF_BOLD, widest, start, width)
    for line in lines:
        d.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def body_lines(d, lines, x, y, width, size, leading):
    """Regular serif paragraph from pre-broken lines (each autofit)."""
    for line in lines:
        f = font(SERIF, size)
        if f.getlength(line) > width:
            f = fit(SERIF, line, size, width)
        d.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def kicker(d, text, x, y, size=21):
    f = font(SANS_BOLD, size)
    d.text((x, y), text, font=f, fill=RED)
    return y


def rule(d, y, x0=MARGIN, x1=W - MARGIN, width=2):
    d.rectangle([x0, y, x1 - 1, y + width - 1], fill=INK)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # --- masthead ---
    d.rectangle([0, 0, W - 1, 107], fill=NAVY)
    d.rectangle([0, 108, W - 1, 113], fill=RED)
    gold = font(SANS_BOLD, 27)
    draw_tracked(d, W // 2, 14, "THE WORLD IN ONE PAGE", gold, GOLD, 7)
    date_text = "SATURDAY, 21 NOVEMBER 2026"
    date_f = fit(SERIF_BOLD, date_text, 58, W - 2 * MARGIN)
    date_w = date_f.getlength(date_text)
    d.text(((W - date_w) / 2, 46), date_text, font=date_f, fill=WHITE)

    # --- lead story: Poland ---
    place_photo(page, (20, 122, 1004, 330),
                BASE / "assets" / "media-generation-poland-dawn-0-f03972f8-b11b-40e8-9a68-f937f0d83824.webp",
                focus=(0.5, 0.48))
    kicker(d, "POLAND \u2022 LEAD STORY", 20, 340)
    headline(d, ["RUSSIAN MISSILES LAND IN POLAND"], 20, 366, 984, 56, 60)
    body_lines(d, [
        "Two cruise missiles and a drone came down in south-east Poland during Russia's massive",
        "overnight attack on Ukraine. PM Donald Tusk calls it a deliberate provocation; NATO chief",
        "Mark Rutte is due in Warsaw on Saturday.",
    ], 20, 420, 984, 20, 27)
    rule(d, 503)

    # --- second story: Shenzhen summit ---
    kicker(d, "SUMMIT \u2022 SHENZHEN", 20, 518, size=20)
    headline(d, ["TRUMP, XI AND PUTIN ISSUE JOINT", "DECLARATION"],
             20, 544, 640, 40, 44)
    body_lines(d, [
        "The first-ever trilateral meeting at the APEC summit ends",
        "with a four-point joint declaration on peace and security \u2014 but no",
        "deal on Ukraine or Iran.",
    ], 20, 634, 640, 19, 26)
    place_photo(page, (682, 518, 1004, 700),
                BASE / "assets" / "media-generation-shenzhen-dusk-0-6ab2ed24-4f73-4426-be4b-20a1bf6cb004.webp")
    rule(d, 714)

    # --- bottom columns: markets and Asia ---
    kicker(d, "MARKETS", 20, 726, size=20)
    kicker(d, "ASIA", 522, 726, size=20)
    headline(d, ["WALL STREET SLUMPS INTO", "CORRECTION"], 20, 752, 482, 36, 40)
    headline(d, ["INDONESIA'S VP SEAT STILL", "VACANT"], 522, 752, 482, 36, 40)
    body_lines(d, [
        "The S&P 500 falls about 3.7% as AI shares sell",
        "off, pushing US stocks into correction territory.",
    ], 20, 830, 482, 18, 23)
    body_lines(d, [
        "Nine days after Gibran Rakabuming quit, the",
        "MPR waits for President Prabowo's two names;",
        "the vote is set for 2 December.",
    ], 522, 830, 482, 18, 23)

    # --- ticker ---
    d.rectangle([0, 896, W - 1, H - 1], fill=NAVY)
    ticker_lines = [
        "ALSO: Mongolia's president quits \u2022 ICJ genocide verdict reverberates \u2022 UK and EU sign trade deals \u2022",
        "Trump pardons Pete Rose \u2022 At least 11 killed in Kyiv strikes",
    ]
    for i, line in enumerate(ticker_lines):
        f = font(SANS_BOLD, 18)
        if f.getlength(line) > 984:
            f = fit(SANS_BOLD, line, 18, 984)
        d.text((20, 912 + i * 34), line, font=f, fill=WHITE)

    out = BASE / "entry.png"
    page.save(out, format="PNG", optimize=True)
    size = out.stat().st_size
    print(f"wrote {out} {page.size[0]}x{page.size[1]} {size} bytes")
    if size >= 1024 * 1024:
        print("WARNING: entry.png is 1 MiB or larger")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
