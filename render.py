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

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (16, 38, 63)
NAVY2 = (24, 56, 90)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
TEAL = (14, 77, 92)
TEAL_DK = (9, 52, 64)
GRAY = (88, 88, 88)
SKY = (223, 232, 238)
WHITE = (255, 255, 255)
ORANGE = (232, 120, 30)
YELLOW = (245, 196, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, fill, maxw, lh):
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def burst(d, cx, cy, r_outer, r_inner, n, fill):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def hline(d, x0, x1, y, fill, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_gulf(d, x, y, w, h):
    """Night sky over the Gulf: drones, a Patriot battery, an intercept."""
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int((8 + 14 * t)) if k == 0 else
                  int((18 + 26 * t)) if k == 1 else
                  int((38 + 36 * t)) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    # stars (fixed positions; kept clear of the label at top-left)
    for sx, sy, sr in [(360, 20, 2), (420, 44, 1), (480, 18, 2),
                       (520, 60, 1), (300, 84, 1), (500, 78, 2),
                       (210, 52, 1), (120, 70, 1), (90, 44, 1),
                       (260, 60, 2), (180, 80, 1), (540, 30, 1)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(220, 225, 235))
    # moon
    d.ellipse([x + w - 78, y + 14, x + w - 40, y + 52], fill=(240, 230, 190))
    # ground: desert strip
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(38, 32, 26))
    # Patriot launcher: truck base + angled tubes
    bx, by = x + 48, y + h - 34
    d.rectangle([bx, by - 26, bx + 120, by], fill=(52, 54, 60))
    d.rectangle([bx + 8, by - 34, bx + 112, by - 26], fill=(40, 42, 48))
    for i in range(4):
        tx = bx + 22 + i * 24
        d.line([(tx, by - 34), (tx + 26, by - 78)], fill=(120, 124, 132),
               width=5)
    # radar dish
    d.arc([bx + 128, by - 62, bx + 168, by - 22], 180, 360,
          fill=(150, 154, 162), width=3)
    d.line([(bx + 148, by - 42), (bx + 148, by - 26)], fill=(150, 154, 162),
           width=3)
    # drones: pale diamonds with red lights
    for dx, dy in [(x + 300, y + 40), (x + 360, y + 66), (x + 430, y + 34),
                   (x + 500, y + 58)]:
        d.polygon([(dx, dy - 6), (dx + 7, dy), (dx, dy + 6), (dx - 7, dy)],
                  fill=(190, 194, 204))
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(220, 60, 50))
    # intercept burst
    ex, ey = x + 330, y + 108
    burst(d, ex, ey, 46, 20, 10, ORANGE)
    burst(d, ex, ey, 26, 11, 10, YELLOW)
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(255, 240, 180))
    for sx, sy, sr in [(ex - 56, ey - 26, 17), (ex + 50, ey - 34, 20),
                       (ex + 70, ey - 2, 14)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 115, 122))
    # label
    d.text((x + 12, y + 12), "GULF SKIES — BAHRAIN & KUWAIT",
           font=SANS_B(17), fill=WHITE)


def draw_bridge(d, x, y, w, h):
    """A suspension bridge under a drone sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 140, 160))
    for wy in (y + h - 18, y + h - 8):
        for wx in range(x + 6, x + w - 24, 38):
            d.arc([wx, wy, wx + 28, wy + 10], 180, 360, fill=(220, 235, 240),
                  width=2)
    # towers
    for tx in (x + 90, x + w - 118):
        d.rectangle([tx, y + 12, tx + 22, y + h - 26], fill=(60, 60, 66))
    # deck + cables
    d.rectangle([x, y + h - 52, x + w, y + h - 44], fill=(40, 40, 46))
    for cx in range(x + 10, x + w - 10, 34):
        d.line([(x + 101, y + 14), (cx, y + h - 50)], fill=(110, 110, 116),
               width=1)
        d.line([(x + w - 107, y + 14), (cx, y + h - 50)], fill=(110, 110, 116),
               width=1)
    # drones: small dark diamonds
    for dx, dy in [(x + 30, y + 16), (x + 70, y + 30), (x + 170, y + 12),
                   (x + 300, y + 22), (x + 380, y + 10), (x + 430, y + 32)]:
        d.polygon([(dx, dy - 5), (dx + 5, dy), (dx, dy + 5), (dx - 5, dy)],
                  fill=(30, 30, 34))
    # blast on the deck
    bx, by = x + w // 2, y + h - 58
    burst(d, bx, by, 26, 11, 8, ORANGE)
    burst(d, bx, by, 14, 6, 8, YELLOW)


def draw_skyline(d, x, y, w, h):
    """Shenzhen at dusk: skyline silhouettes and a low sun."""
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int((250 - 60 * t)) if k == 0 else
                  int((190 - 90 * t)) if k == 1 else
                  int((120 + 40 * t)) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    d.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=(245, 196, 60))
    heights = [34, 52, 40, 62, 46, 56, 38, 50]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, y + h - bh, bx + bw - 2, y + h], fill=(40, 36, 54))
        for wy in range(y + h - bh + 6, y + h - 6, 12):
            for wx in range(bx + 6, bx + bw - 8, 12):
                if (wx + wy) % 24 < 12:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 210, 90))


def draw_chart(d, x, y, w, h):
    """A falling market line."""
    pts = [(x + i * w / 9, y + h * (0.15 + 0.75 * i / 9) +
            (6 if i % 3 else -6)) for i in range(10)]
    d.line(pts, fill=GOLD_LT, width=4, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 14, pts[-1][1] - 16),
               (pts[-1][0] - 2, pts[-1][1] - 2)], fill=(220, 60, 50))
    d.text((x, y - 2), "", font=SANS_B(10), fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 10), "THE WORLD IN ONE DAY", font=SERIF_B(54),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 74), "WEDNESDAY  ·  18 NOVEMBER 2026", font=SANS_B(28),
           fill=GOLD_LT, anchor="ma")
    hline(d, 0, W, 118, GOLD, 4)

    # ---- lead story ----------------------------------------------------
    d.text((40, 134), "THE GULF  —  DRONES OVER BAHRAIN AND KUWAIT",
           font=SANS_B(21), fill=RED)
    d.text((40, 160), "IRAN HITS BAHRAIN AND KUWAIT", font=SANS_B(40),
           fill=INK)
    d.text((40, 202), "AS A US CARRIER SAILS IN", font=SANS_B(40), fill=INK)
    draw_gulf(d, 40, 248, 560, 216)
    lx = 624
    y = para(d, lx, 252,
             "Iranian drones hit Bahrain and Kuwait before dawn, aimed "
             "at US Patriot systems at Ali Al-Salem base, Tehran said.",
             SANS(19), INK, 360, 24)
    y = para(d, lx, y + 8,
             "Bahrain said its defences shot down several drones, "
             "another attack after Tuesday's.",
             SANS(19), INK, 360, 24)
    para(d, lx, y + 8,
         "The US confirmed its jets hit a missile site on Qeshm "
         "Island.",
         SANS(19), INK, 360, 24)
    hline(d, 40, 984, 480, (200, 192, 170), 2)

    # ---- middle row: Ukraine + Shenzhen --------------------------------
    # Ukraine, left column
    draw_bridge(d, 40, 494, 452, 74)
    d.text((40, 578), "UKRAINE", font=SANS_B(20), fill=RED)
    d.text((40, 602), "KERCH BRIDGE SPAN FALLS", font=SANS_B(26), fill=INK)
    d.text((40, 632), "INTO THE STRAIT", font=SANS_B(26), fill=INK)
    para(d, 40, 666,
         "Ukraine hit the Crimea bridge for a second day; part of its "
         "road span fell into the water. Russia struck two bridges "
         "in Kyiv in reply.", SANS(18), (60, 60, 60), 452, 22)
    # Shenzhen, right column
    draw_skyline(d, 532, 494, 452, 74)
    d.text((532, 578), "SHENZHEN  —  APEC", font=SANS_B(20), fill=RED)
    d.text((532, 602), "XI, PUTIN AND TRUMP", font=SANS_B(26), fill=INK)
    d.text((532, 632), "TO MEET IN SHENZHEN", font=SANS_B(26), fill=INK)
    para(d, 532, 666,
         "Putin flew in for the APEC summit, a day before the first "
         "three-way meeting with Xi and Trump. Trump was in Manila "
         "for the Quad first.", SANS(18), (60, 60, 60), 452, 22)
    hline(d, 40, 984, 732, (200, 192, 170), 2)

    # ---- markets strip ---------------------------------------------------
    d.rectangle([0, 742, W, 832], fill=NAVY)
    d.text((40, 754), "MARKETS SLIDE", font=SANS_B(26), fill=GOLD_LT)
    draw_chart(d, 330, 752, 180, 66)
    d.text((530, 754),
           "Dow −1.6% · S&P −1.0% · Nasdaq −0.7%",
           font=SANS_B(20), fill=WHITE)
    d.text((530, 788),
           "Brent −0.7% to $92.53  ·  Gold −1.4% to $3,796",
           font=SANS(19), fill=(200, 210, 220))
    d.text((40, 782), "S&P at lowest since July", font=SANS(19),
           fill=(200, 210, 220))

    # ---- bottom row: four short stories ---------------------------------
    cards = [
        ("EBOLA — DR CONGO", RED,
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
        d.text((cx, 860), kicker, font=SANS_B(17), fill=color)
        para(d, cx, 884, head, SANS_B(20), INK, 226, 25)
        cx += 238
    hline(d, 40, 984, 972, (200, 192, 170), 2)

    # ---- footer ----------------------------------------------------------
    d.text((W // 2, 984),
           "ALSO: Nvidia beats, up 4%  ·  Dhoni retires from the IPL  ·  "
           "Russian plane crash kills 19  ·  US loses measles-free status",
           font=SANS(16), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
