#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Run: python3 render.py  -> writes entry.png beside this file.
Deterministic: fixed text, fixed geometry, no time, no randomness, no network.
Only the Python standard library + Pillow are used to render; the entry
program itself (main.ts) only copies the finished entry.png.

Facts, all first reported on Wednesday 18 November 2026 (or on Tuesday
evening US time, i.e. 18 November UTC) and checked against several
news sources:
- Gulf: Iranian drones struck at Bahrain and Kuwait before dawn; Tehran
  said they targeted US Patriot systems at Ali Al-Salem air base in
  Kuwait. Bahrain said its defences shot down several drones. The US
  confirmed its jets hit a missile site on Qeshm Island on Tuesday,
  and a third carrier group (USS Theodore Roosevelt) is sailing in.
- Ukraine: Kyiv hit the Kerch bridge to Crimea for a second day; part
  of its road span fell into the strait. Russia struck two bridges
  in Kyiv in reply.
- Shenzhen: APEC opened in Shenzhen; Putin flew in, a day before the
  first three-way summit with Xi and Trump. Trump was in Manila for
  the Quad first.
- Markets (Tuesday close): Dow -1.6% to 50,759, S&P -1.0% to 7,341
  (lowest since July), Nasdaq -0.7% to 24,328 (lowest in ~7 months).
  Brent -0.7% to $92.53 and gold -1.4% to $3,796 on Wednesday morning.
  Nvidia beat earnings after the bell, up 4%.
- Ebola in DR Congo: outbreak more than doubled in three months,
  over 11,000 cases and 5,400 deaths (UN).
- Alaska: Mary Peltola beat Dan Sullivan, Democrats take a 56-44
  Senate majority; first Alaska Native in the Senate.
- Cyclone Xavier: Category 5, gusts to 315 km/h, bearing down on the
  Northern Cook Islands; shelters activated.
- Gaza: Australia, Canada, Italy and the UK urge Israel to open aid
  crossings to flooded Gaza.
- Also: MS Dhoni retires from the IPL; a Russian military plane crash
  in Siberia kills 19; the US loses its measles-free status; a
  nationwide FAA ground stop after a telecom outage.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024

C = {
    "paper": (247, 243, 232),
    "ink": (20, 20, 20),
    "navy": (16, 38, 63),
    "red": (179, 38, 30),
    "gold": (201, 162, 39),
    "gold_lt": (232, 196, 90),
    "gray": (88, 88, 88),
    "sky": (223, 232, 238),
    "white": (255, 255, 255),
    "orange": (232, 120, 30),
    "yellow": (245, 196, 60),
    "down": (220, 60, 50),
    "rule": (200, 192, 170),
    "body": (60, 60, 60),
    "pale": (200, 210, 220),
}

FONTS = "/usr/share/fonts/truetype/dejavu"


def load_font(kind, size):
    name = {"serif-bold": "DejaVuSerif-Bold.ttf",
            "sans-bold": "DejaVuSans-Bold.ttf",
            "sans": "DejaVuSans.ttf"}[kind]
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def vgrad(d, x, y, w, h, top, bottom):
    for row in range(h):
        t = row / max(h - 1, 1)
        col = tuple(round(top[k] + (bottom[k] - top[k]) * t)
                    for k in range(3))
        d.line([(x, y + row), (x + w, y + row)], fill=col)


def wrap_text(d, text, f, maxw):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        elif cur:
            out.append(cur)
            cur = word
        else:
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_para(d, x, y, text, f, fill, maxw, leading):
    for line in wrap_text(d, text, f, maxw):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def starburst(d, cx, cy, outer, inner, points, fill):
    verts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / points - math.pi / 2
        verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(verts, fill=fill)


def rule(d, x0, x1, y, fill=None, width=2):
    d.line([(x0, y), (x1, y)], fill=fill or C["rule"], width=width)


def gulf_night(d, x, y, w, h):
    """Night sky over the Gulf: drones, a Patriot battery, an intercept."""
    vgrad(d, x, y, w, h, (8, 18, 38), (22, 44, 74))
    for sx, sy, sr in [(360, 20, 2), (420, 44, 1), (480, 18, 2),
                       (520, 60, 1), (300, 84, 1), (500, 78, 2),
                       (210, 52, 1), (120, 70, 1), (90, 44, 1),
                       (260, 60, 2), (180, 80, 1), (540, 30, 1)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(220, 225, 235))
    d.ellipse([x + w - 78, y + 14, x + w - 40, y + 52], fill=(240, 230, 190))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(38, 32, 26))
    bx, by = x + 48, y + h - 34
    d.rectangle([bx, by - 26, bx + 120, by], fill=(52, 54, 60))
    d.rectangle([bx + 8, by - 34, bx + 112, by - 26], fill=(40, 42, 48))
    for i in range(4):
        tx = bx + 22 + i * 24
        d.line([(tx, by - 34), (tx + 26, by - 78)], fill=(120, 124, 132),
               width=5)
    d.arc([bx + 128, by - 62, bx + 168, by - 22], 180, 360,
          fill=(150, 154, 162), width=3)
    d.line([(bx + 148, by - 42), (bx + 148, by - 26)], fill=(150, 154, 162),
           width=3)
    for dx, dy in [(x + 300, y + 40), (x + 360, y + 66), (x + 430, y + 34),
                   (x + 500, y + 58)]:
        d.polygon([(dx, dy - 6), (dx + 7, dy), (dx, dy + 6), (dx - 7, dy)],
                  fill=(190, 194, 204))
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(220, 60, 50))
    ex, ey = x + 330, y + 108
    starburst(d, ex, ey, 46, 20, 10, C["orange"])
    starburst(d, ex, ey, 26, 11, 10, C["yellow"])
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(255, 240, 180))
    for sx, sy, sr in [(ex - 56, ey - 26, 17), (ex + 50, ey - 34, 20),
                       (ex + 70, ey - 2, 14)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 115, 122))
    d.text((x + 12, y + 12), "GULF SKIES — BAHRAIN & KUWAIT",
           font=load_font("sans-bold", 17), fill=C["white"])


def bridge_attack(d, x, y, w, h):
    """A suspension bridge under a drone sky, with a blast on the deck."""
    d.rectangle([x, y, x + w, y + h], fill=C["sky"])
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 140, 160))
    for wy in (y + h - 18, y + h - 8):
        wx = x + 6
        while wx < x + w - 24:
            d.arc([wx, wy, wx + 28, wy + 10], 180, 360,
                  fill=(220, 235, 240), width=2)
            wx += 38
    for tx in (x + 90, x + w - 118):
        d.rectangle([tx, y + 12, tx + 22, y + h - 26], fill=(60, 60, 66))
    d.rectangle([x, y + h - 52, x + w, y + h - 44], fill=(40, 40, 46))
    deck_y = y + h - 50
    for cx in range(x + 10, x + w - 10, 34):
        for top_x in (x + 101, x + w - 107):
            d.line([(top_x, y + 14), (cx, deck_y)], fill=(110, 110, 116),
                   width=1)
    for dx, dy in [(x + 30, y + 16), (x + 70, y + 30), (x + 170, y + 12),
                   (x + 300, y + 22), (x + 380, y + 10), (x + 430, y + 32)]:
        d.polygon([(dx, dy - 5), (dx + 5, dy), (dx, dy + 5), (dx - 5, dy)],
                  fill=(30, 30, 34))
    bx, by = x + w // 2, y + h - 58
    starburst(d, bx, by, 26, 11, 8, C["orange"])
    starburst(d, bx, by, 14, 6, 8, C["yellow"])


def city_dusk(d, x, y, w, h):
    """Shenzhen at dusk: skyline silhouettes and a low sun."""
    vgrad(d, x, y, w, h, (250, 190, 120), (190, 100, 160))
    d.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=(245, 196, 60))
    heights = [34, 52, 40, 62, 46, 56, 38, 50]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, y + h - bh, bx + bw - 2, y + h], fill=(40, 36, 54))
        wy = y + h - bh + 6
        while wy < y + h - 6:
            wx = bx + 6
            while wx < bx + bw - 8:
                if (wx + wy) % 24 < 12:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 210, 90))
                wx += 12
            wy += 12


def falling_line(d, x, y, w, h):
    """A falling market line with a red arrowhead at its end."""
    pts = []
    for i in range(10):
        px = x + i * w / 9
        py = y + h * (0.15 + 0.75 * i / 9) + (6 if i % 3 else -6)
        pts.append((px, py))
    d.line(pts, fill=C["gold_lt"], width=4, joint="curve")
    tip = pts[-1]
    d.polygon([(tip[0], tip[1]), (tip[0] - 14, tip[1] - 16),
               (tip[0] - 2, tip[1] - 2)], fill=C["down"])


def masthead(d):
    d.rectangle([0, 0, PAGE_W, 118], fill=C["navy"])
    d.text((PAGE_W // 2, 10), "THE WORLD IN ONE DAY",
           font=load_font("serif-bold", 54), fill=C["white"], anchor="ma")
    d.text((PAGE_W // 2, 74), "WEDNESDAY  ·  18 NOVEMBER 2026",
           font=load_font("sans-bold", 28), fill=C["gold_lt"], anchor="ma")
    rule(d, 0, PAGE_W, 118, fill=C["gold"], width=4)


def lead_story(d):
    d.text((40, 134), "THE GULF  —  DRONES OVER BAHRAIN AND KUWAIT",
           font=load_font("sans-bold", 21), fill=C["red"])
    d.text((40, 160), "IRAN HITS BAHRAIN AND KUWAIT",
           font=load_font("sans-bold", 40), fill=C["ink"])
    d.text((40, 202), "AS A US CARRIER SAILS IN",
           font=load_font("sans-bold", 40), fill=C["ink"])
    gulf_night(d, 40, 248, 560, 216)
    lx = 624
    y = draw_para(d, lx, 252,
                  "Iranian drones hit Bahrain and Kuwait before dawn, aimed "
                  "at US Patriot systems at Ali Al-Salem base, Tehran said.",
                  load_font("sans", 19), C["ink"], 360, 24)
    y = draw_para(d, lx, y + 8,
                  "Bahrain said its defences shot down several drones, "
                  "another attack after Tuesday's.",
                  load_font("sans", 19), C["ink"], 360, 24)
    draw_para(d, lx, y + 8,
              "The US confirmed its jets hit a missile site on Qeshm "
              "Island.",
              load_font("sans", 19), C["ink"], 360, 24)
    rule(d, 40, 984, 480)


def middle_row(d):
    bridge_attack(d, 40, 494, 452, 74)
    d.text((40, 578), "UKRAINE", font=load_font("sans-bold", 20), fill=C["red"])
    d.text((40, 602), "KERCH BRIDGE SPAN FALLS",
           font=load_font("sans-bold", 26), fill=C["ink"])
    d.text((40, 632), "INTO THE STRAIT",
           font=load_font("sans-bold", 26), fill=C["ink"])
    draw_para(d, 40, 666,
              "Ukraine hit the Crimea bridge for a second day; part of its "
              "road span fell into the water. Russia struck two bridges "
              "in Kyiv in reply.", load_font("sans", 18), C["body"], 452, 22)
    city_dusk(d, 532, 494, 452, 74)
    d.text((532, 578), "SHENZHEN  —  APEC",
           font=load_font("sans-bold", 20), fill=C["red"])
    d.text((532, 602), "XI, PUTIN AND TRUMP",
           font=load_font("sans-bold", 26), fill=C["ink"])
    d.text((532, 632), "TO MEET IN SHENZHEN",
           font=load_font("sans-bold", 26), fill=C["ink"])
    draw_para(d, 532, 666,
              "Putin flew in for the APEC summit, a day before the first "
              "three-way meeting with Xi and Trump. Trump was in Manila "
              "for the Quad first.", load_font("sans", 18), C["body"], 452, 22)
    rule(d, 40, 984, 732)


def markets_strip(d):
    d.rectangle([0, 742, PAGE_W, 832], fill=C["navy"])
    d.text((40, 754), "MARKETS SLIDE",
           font=load_font("sans-bold", 26), fill=C["gold_lt"])
    falling_line(d, 330, 752, 180, 66)
    d.text((530, 754),
           "Dow −1.6% · S&P −1.0% · Nasdaq −0.7%",
           font=load_font("sans-bold", 20), fill=C["white"])
    d.text((530, 788),
           "Brent −0.7% to $92.53  ·  Gold −1.4% to $3,796",
           font=load_font("sans", 19), fill=C["pale"])
    d.text((40, 782), "S&P at lowest since July",
           font=load_font("sans", 19), fill=C["pale"])


def bottom_row(d):
    cards = [
        ("EBOLA — DR CONGO", C["red"],
         "Outbreak doubles: 11,000 cases, 5,400 dead"),
        ("ALASKA", (14, 90, 60),
         "Peltola flips Senate seat; Democrats take 56"),
        ("CYCLONE XAVIER", (90, 60, 120),
         "Category 5 storm bears down on the Cook Islands"),
        ("GAZA", (120, 70, 20),
         "Four nations urge Israel to open aid crossings"),
    ]
    cx = 40
    for kicker, color, head in cards:
        d.rectangle([cx, 844, cx + 226, 850], fill=color)
        d.text((cx, 860), kicker, font=load_font("sans-bold", 17), fill=color)
        draw_para(d, cx, 884, head, load_font("sans-bold", 20), C["ink"],
                  226, 25)
        cx += 238
    rule(d, 40, 984, 972)


def footer(d):
    d.text((PAGE_W // 2, 984),
           "ALSO: Nvidia beats, up 4%  ·  Dhoni retires from the IPL  ·  "
           "Russian plane crash kills 19  ·  US loses measles-free status",
           font=load_font("sans", 16), fill=C["gray"], anchor="ma")


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), C["paper"])
    d = ImageDraw.Draw(img)
    masthead(d)
    lead_story(d)
    middle_row(d)
    markets_strip(d)
    bottom_row(d)
    footer(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
