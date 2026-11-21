#!/usr/bin/env python3
"""Compose the 21 November 2026 world-news front page (1024x1024).

Layout (my own design for this edition): a navy masthead naming the day,
a wide lead photograph with headline and deck, a second story with its
picture on the right and text on the left, two short panels side by side,
and a navy ticker footer. Two text-free press illustrations live in
assets/ (a Polish air-defence radar vehicle at dawn; the Shenzhen
convention centre at dusk). Every word is set here with PIL so the text
stays crisp. Deterministic: fixed inputs, no clock, no randomness.
Writes entry.png next to this file; if the PNG would pass 1 MiB it
writes JPEG bytes instead (same filename).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
MARGIN = 20
INNER = W - 2 * MARGIN

PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (15, 30, 51)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def fit(draw, text, path, size, max_width):
    """Largest size at or below `size` that fits `max_width`."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_width:
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        elif cur:
            lines.append(cur)
            cur = word
        else:
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover(image, width, height):
    sw, sh = image.size
    scale = max(width / sw, height / sh)
    big = image.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    left = (big.width - width) // 2
    top = (big.height - height) // 2
    return big.crop((left, top, left + width, top + height))


def kicker(draw, x, y, text, size=21):
    draw.text((x, y), text, font=font(SANS_BOLD, size), fill=RED)


def head(draw, x, y, text, size, width, leading, fill=INK):
    fnt = font(SERIF_BOLD, size)
    return para(draw, x, y, wrap(draw, text, fnt, width), fnt, fill, leading)


def deck(draw, x, y, text, size, width, leading):
    fnt = font(SANS, size)
    return para(draw, x, y, wrap(draw, text, fnt, width), fnt, GREY, leading)


def build():
    poland = Image.open(os.path.join(
        ASSETS,
        "media-generation-poland-dawn-0-f03972f8-b11b-40e8-9a68-f937f0d83824.webp"))
    shenzhen = Image.open(os.path.join(
        ASSETS,
        "media-generation-shenzhen-dusk-0-6ab2ed24-4f73-4426-be4b-20a1bf6cb004.webp"))

    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # Masthead.
    d.rectangle([4, 4, W - 5, 108], fill=NAVY)
    tag = "T H E   W O R L D   I N   O N E   P A G E"
    tag_font = font(SANS_BOLD, 23)
    d.text(((W - d.textlength(tag, font=tag_font)) / 2, 16),
           tag, font=tag_font, fill=GOLD)
    date = "SATURDAY, 21 NOVEMBER 2026"
    date_font = fit(d, date, SERIF_BOLD, 56, INNER - 10)
    d.text(((W - d.textlength(date, font=date_font)) / 2, 46),
           date, font=date_font, fill=WHITE)
    d.rectangle([4, 108, W - 5, 114], fill=RED)

    # Lead: Poland photograph, headline, deck.
    page.paste(cover(poland, INNER, 230), (MARGIN, 126))
    d.rectangle([MARGIN, 126, MARGIN + INNER - 1, 126 + 230 - 1],
                outline=INK, width=2)
    y = 368
    kicker(d, MARGIN, y, "POLAND  •  LEAD STORY")
    y = head(d, MARGIN, 394, "RUSSIAN MISSILES LAND IN POLAND",
             44, INNER, 50)
    y += 6
    deck(d, MARGIN, y,
         "Two cruise missiles and a drone came down in south-east Poland "
         "during Russia's massive overnight attack on Ukraine. PM Donald "
         "Tusk calls it a deliberate provocation; NATO chief Mark Rutte "
         "is due in Warsaw on Saturday.",
         21, INNER, 27)

    d.line([(MARGIN, 556), (MARGIN + INNER, 556)], fill=INK, width=2)

    # Second row: Shenzhen story, text left, picture right.
    y0 = 570
    tw = 640
    kicker(d, MARGIN, y0, "SUMMIT  •  SHENZHEN", size=19)
    y = head(d, MARGIN, y0 + 26,
             "TRUMP, XI AND PUTIN ISSUE JOINT DECLARATION",
             30, tw, 36)
    deck(d, MARGIN, y + 4,
         "The first-ever trilateral meeting at the APEC summit ends with "
         "a four-point declaration on peace and security — but no deal "
         "on Ukraine or Iran.",
         21, tw, 27)
    ix = MARGIN + tw + 24
    page.paste(cover(shenzhen, INNER - tw - 24, 170), (ix, y0))
    d.rectangle([ix, y0, ix + (INNER - tw - 24) - 1, y0 + 170 - 1],
                outline=INK, width=2)

    d.line([(MARGIN, 754), (MARGIN + INNER, 754)], fill=INK, width=2)

    # Third row: two panels.
    col = (INNER - 24) // 2
    y0 = 768
    kicker(d, MARGIN, y0, "MARKETS", size=19)
    y = head(d, MARGIN, y0 + 26, "WALL STREET SLUMPS INTO CORRECTION",
             26, col, 31)
    deck(d, MARGIN, y + 4,
         "The S&P 500 falls about 3.7% as AI shares sell off, pushing "
         "US stocks into correction territory.",
         20, col, 26)

    rx = MARGIN + col + 24
    kicker(d, rx, y0, "ASIA", size=19)
    y = head(d, rx, y0 + 26, "INDONESIA'S VP SEAT STILL VACANT",
             26, col, 31)
    deck(d, rx, y + 4,
         "Nine days after Gibran Rakabuming quit, the MPR waits for "
         "President Prabowo's two names; the vote is set for 2 December.",
         20, col, 26)

    # Footer ticker.
    d.rectangle([4, 952, W - 5, 1020], fill=NAVY)
    foot_font = font(SANS, 19)
    ticker = ("ALSO:  Mongolia's president quits  •  ICJ genocide verdict "
              "reverberates  •  UK and EU sign trade deals  •  Trump "
              "pardons Pete Rose  •  At least 11 killed in Kyiv strikes")
    y = 962
    for line in wrap(d, ticker, foot_font, INNER - 16):
        d.text((MARGIN + 8, y), line, font=foot_font, fill=WHITE)
        y += 23

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    if os.path.getsize(out) > 1048576:
        page.save(out, format="JPEG", quality=88, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
