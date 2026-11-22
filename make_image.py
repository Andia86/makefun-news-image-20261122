#!/usr/bin/env python3
"""Draw the front page for news-image-20261122: one image summing up the
world news of Sunday 22 November 2026.

Layout follows the classic broadsheet formula for this contest series:
a masthead naming the day, 11 illustrated story cards, a dot world map
with a pin for every card, and the remaining 29 stories as a dense
numbered brief list. 40 stories in all.

Deterministic: fixed data, fixed fonts, no clock, no randomness, no
network. Two runs write byte-identical entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968

CREAM = (247, 241, 227)
PAPER = (252, 249, 240)
INK = (24, 28, 38)
NAVY = (27, 42, 74)
RED = (176, 48, 38)
GREY = (92, 96, 104)
RULE = (27, 42, 74)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
CARD_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# Each card: number, band colour, region tag, headline, one-line summary,
# icon name. Every story happened, or was first reported, on 22 Nov 2026;
# sources are listed in NEWS_SOURCES.md.

CARDS = [
    (1, (20, 102, 107), "TÜRKIYE · CLIMATE",
     "COP31 runs into a second day of overtime",
     "New draft deal in Antalya still omits fossil fuels by name; "
     "nearly 200 nations seek consensus.", "leaf"),
    (2, (176, 48, 38), "MIDDLE EAST · HORMUZ",
     "Bahrain: Iran struck site as tankers hit",
     "Tehran says the strait could reopen if the US accepts "
     "\u201creasonable\u201d terms.", "ship"),
    (3, (70, 80, 140), "UKRAINE · WAR",
     "Ukraine strikes the Crimean Bridge again",
     "Zelenskyy calls the strikes a \u201cfair response\u201d "
     "to Russia's war.", "bridge"),
    (4, (146, 96, 24), "MEXICO · CRIME",
     "Cartel boss \u201cEl Chapo Isidro\u201d captured",
     "FBI most-wanted kingpin seized in Sinaloa; the shoot-out "
     "leaves 11 dead.", "badge"),
    (5, (178, 84, 32), "INDONESIA · DISASTER",
     "Factory fire kills 3, dozens missing",
     "Blaze at a confectionery factory near Jakarta; 36 workers "
     "unaccounted for.", "flame"),
    (6, (52, 62, 84), "UNITED STATES · CYBER",
     "FBI probes hack of criminal database",
     "Apparent breach of the NCIC system; a USDA breach is "
     "also reported.", "shield"),
    (7, (38, 92, 128), "UNITED STATES · BORDERS",
     "Arrests at Seattle airport delay flight",
     "Immigration officers make arrests in the terminal; passengers "
     "call the scene distressing.", "plane"),
    (8, (86, 60, 128), "SPACE · SCIENCE",
     "Two spacecraft reach Mercury",
     "A pair of orbiters loop in around the little planet \u2014 "
     "its first visitors in years.", "planet"),
    (9, (30, 110, 76), "SPORT · FORMULA 1",
     "Verstappen wins wild Las Vegas GP",
     "34 lead changes and a collision between the Ferraris "
     "in a classic night race.", "car"),
    (10, (160, 60, 84), "JAPAN · CULTURE",
     "Shuri Castle's main hall rises again",
     "The Okinawa landmark is restored seven years after fire "
     "gutted it.", "castle"),
    (11, (24, 84, 110), "NIGERIA · DISASTER",
     "Funeral boat capsizes, at least 24 dead",
     "A vessel carrying mourners overturns in Nigeria; the search "
     "goes on.", "boat"),
]

# Briefs 12-40: number, text (region prefix first). Headlines only, each
# checked against the sources in NEWS_SOURCES.md.
BRIEFS = [
    (12, "S. Korea education chief quits over AI cheating scandal"),
    (13, "France: sixth weekend of living-cost protests"),
    (14, "France: officers sentenced over Zecler beating"),
    (15, "Houthis strike Riyadh after Saudi coalition operation"),
    (16, "New Senate Democrats face leadership-vote test"),
    (17, "Trump vows 10% cap on credit-card interest rates"),
    (18, "May \u201caghast\u201d at Burnham EU plans: \u201cBrexit is done\u201d"),
    (19, "Zelenskyy: Putin a \u201ckiller\u201d, after Trump \u201cfriend\u201d line"),
    (20, "Denmark: Russia plotted to kill US-Ukrainian rapper"),
    (21, "Russia-bound ship droned in Gulf of Finland"),
    (22, "Man convicted of starting LA's Palisades fire"),
    (23, "Nigeria youth voter sign-ups fall before election"),
    (24, "ANC fights to hold key cities after poll setback"),
    (25, "Jeweller Paolo Bulgari dies at 89"),
    (26, "Italy ex-police chief takes own life amid mafia probe"),
    (27, "Croatia outrage over hospital patient's death"),
    (28, "Bangladesh: nearly 30 Awami League homes torched"),
    (29, "China warns US over telecom phone-number ban"),
    (30, "\u201cBlack Saturn\u201d: black hole inside a black hole"),
    (31, "Princess Aiko returns from Singapore visit"),
    (32, "Australia faults US budget office on AUKUS"),
    (33, "England beat All Blacks; Rennie under pressure"),
    (34, "Leeds win at Chelsea, first time since 1999"),
    (35, "Wembanyama hits 50 in Spurs win over Pelicans"),
    (36, "UN talks pledge \u201ckiller robot\u201d rules by 2028"),
    (37, "Judge OKs $7.25bn Roundup cancer settlement"),
    (38, "Mamdani plans to close Rikers jail by 2032"),
    (39, "Spitting Image co-creator Peter Fluck dies, 85"),
    (40, "Lock of Washington's hair sells for $4,000"),
]


# ---------------------------------------------------------------- helpers

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, max_w, max_lines, min_size=9):
    """Wrap text, shrinking the font until it fits max_lines."""
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, size)
    return fnt, wrap(draw, text, fnt, max_w)


# ------------------------------------------------------------------- icons
# Small white pictograms drawn inside each card's colour band, centred on
# (cx, cy) inside a box of about 30x22 px. Flat shapes only.

def icon(draw, name, cx, cy, col=(255, 255, 255)):
    if name == "leaf":  # globe with a leaf: climate talks
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=col, width=2)
        draw.line([cx - 10, cy, cx + 10, cy], fill=col, width=1)
        draw.line([cx, cy - 10, cx, cy + 10], fill=col, width=1)
        draw.pieslice([cx - 2, cy - 13, cx + 12, cy + 1], 270, 360, fill=col)
    elif name == "ship":  # tanker on waves
        draw.polygon([(cx - 13, cy + 2), (cx + 13, cy + 2), (cx + 9, cy + 8),
                      (cx - 9, cy + 8)], fill=col)
        draw.rectangle([cx - 8, cy - 4, cx + 2, cy + 2], fill=col)
        draw.rectangle([cx + 5, cy - 8, cx + 9, cy + 2], fill=col)
        draw.arc([cx - 14, cy + 6, cx - 2, cy + 14], 0, 180, fill=col, width=2)
        draw.arc([cx + 2, cy + 6, cx + 14, cy + 14], 0, 180, fill=col, width=2)
    elif name == "bridge":  # suspension bridge deck and towers
        draw.line([cx - 14, cy + 7, cx + 14, cy + 7], fill=col, width=2)
        draw.line([cx - 10, cy - 8, cx - 10, cy + 7], fill=col, width=2)
        draw.line([cx + 10, cy - 8, cx + 10, cy + 7], fill=col, width=2)
        draw.line([cx - 10, cy - 8, cx, cy - 1, cx + 10, cy - 8], fill=col, width=1)
        draw.line([cx - 14, cy + 7, cx - 10, cy - 8], fill=col, width=1)
        draw.line([cx + 10, cy - 8, cx + 14, cy + 7], fill=col, width=1)
    elif name == "badge":  # star badge: a most-wanted capture
        pts = []
        import math
        for i in range(10):
            r = 11 if i % 2 == 0 else 4.6
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, fill=col)
    elif name == "flame":  # factory + flame
        draw.rectangle([cx - 14, cy - 2, cx + 2, cy + 9], fill=col)
        draw.polygon([(cx - 14, cy - 2), (cx - 6, cy - 8), (cx - 6, cy - 2)], fill=col)
        draw.polygon([(cx - 4, cy - 2), (cx + 4, cy - 8), (cx + 4, cy - 2)], fill=col)
        draw.polygon([(cx + 8, cy + 9), (cx + 4, cy - 2), (cx + 8, cy - 8),
                      (cx + 13, cy - 1), (cx + 12, cy + 9)], fill=(255, 205, 90))
    elif name == "shield":  # shield with a crack of light: a breach
        draw.polygon([(cx, cy - 11), (cx + 10, cy - 7), (cx + 10, cy + 2),
                      (cx, cy + 11), (cx - 10, cy + 2), (cx - 10, cy - 7)], fill=col)
        draw.line([cx, cy - 8, cx - 2, cy - 1, cx + 1, cy + 2, cx - 1, cy + 8],
                  fill=(52, 62, 84), width=2)
    elif name == "plane":  # airliner
        draw.polygon([(cx - 14, cy + 1), (cx + 12, cy - 3), (cx + 14, cy - 1),
                      (cx + 12, cy + 2), (cx - 12, cy + 4)], fill=col)
        draw.polygon([(cx - 2, cy + 2), (cx - 8, cy + 10), (cx - 3, cy + 10),
                      (cx + 3, cy + 2)], fill=col)
        draw.polygon([(cx - 12, cy + 2), (cx - 15, cy - 6), (cx - 11, cy - 6),
                      (cx - 8, cy + 1)], fill=col)
    elif name == "planet":  # Mercury with two orbiters
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=col)
        draw.ellipse([cx - 16, cy - 4, cx + 16, cy + 5], outline=col, width=2)
        draw.ellipse([cx + 10, cy - 11, cx + 14, cy - 7], fill=(255, 205, 90))
        draw.ellipse([cx - 15, cy + 5, cx - 11, cy + 9], fill=(255, 205, 90))
    elif name == "car":  # chequered flag: a race decided
        draw.line([cx - 10, cy - 10, cx - 10, cy + 10], fill=col, width=2)
        for r in range(3):
            for c in range(4):
                if (r + c) % 2 == 0:
                    draw.rectangle([cx - 8 + c * 5, cy - 10 + r * 4,
                                    cx - 4 + c * 5, cy - 7 + r * 4], fill=col)
    elif name == "castle":  # tiered castle roofs
        draw.polygon([(cx - 13, cy - 2), (cx, cy - 10), (cx + 13, cy - 2),
                      (cx + 9, cy - 2), (cx - 9, cy - 2)], fill=col)
        draw.rectangle([cx - 9, cy - 2, cx + 9, cy + 3], fill=col)
        draw.polygon([(cx - 10, cy + 3), (cx, cy - 3), (cx + 10, cy + 3),
                      (cx + 7, cy + 3), (cx - 7, cy + 3)], fill=col)
        draw.rectangle([cx - 7, cy + 3, cx + 7, cy + 10], fill=col)
    elif name == "boat":  # boat on heavy water
        draw.polygon([(cx - 12, cy - 1), (cx + 12, cy - 1), (cx + 7, cy + 6),
                      (cx - 8, cy + 6)], fill=col)
        draw.rectangle([cx - 2, cy - 8, cx + 1, cy - 1], fill=col)
        draw.polygon([(cx + 1, cy - 8), (cx + 9, cy - 1), (cx + 1, cy - 1)], fill=col)
        draw.arc([cx - 15, cy + 4, cx - 3, cy + 12], 0, 180, fill=col, width=2)
        draw.arc([cx + 1, cy + 4, cx + 13, cy + 12], 0, 180, fill=col, width=2)


# --------------------------------------------------------------- world map
# Coarse land grid, 46 cols x 21 rows, '#' is land. Stylised, for a dot map.
LAND = [
    "..............................................",
    "..#####.......................................",
    ".########..###....####........................",
    "..#############..########......##.............",
    "...##########...##########...#########........",
    "....########.....########...#############.....",
    ".....######.......######....############......",
    "......####.........####......##########.......",
    ".......##....##....####.......########........",
    ".......###..####...#####.......######.........",
    "........########...######.......####..........",
    "........#######....########.....#####.........",
    ".........#####......######.....################",
    ".........####........####......################",
    ".........###..........##.........############...",
    ".........##........................########.....",
    ".........##.........................######......",
    ".........#...........................##.........",
    "..............................................",
    "..............................................",
    "..............................................",
]

# Pins for the terrestrial cards: card number -> (grid col, grid row).
PINS = {
    1: (24.5, 5.5),    # Antalya, Türkiye
    2: (28.5, 7.0),    # Strait of Hormuz
    3: (25.5, 3.8),    # Crimea
    4: (5.0, 8.5),     # Sinaloa, Mexico
    5: (38.5, 12.5),   # Jakarta, Indonesia
    6: (11.4, 4.9),    # Washington DC
    7: (2.7, 3.5),     # Seattle
    9: (4.0, 6.1),     # Las Vegas
    10: (43.5, 6.0),   # Okinawa, Japan
    11: (23.0, 9.8),   # Nigeria
}


# ----------------------------------------------------------------- layout

def draw_masthead(d):
    kick = font(SANS_B, 19)
    t = "THE DAY IN WORLD NEWS"
    d.text(((W - d.textlength(t, font=kick)) / 2, 20), t, font=kick, fill=NAVY)
    date_f = font(SERIF_B, 58)
    t = "Sunday 22 November 2026"
    d.text(((W - d.textlength(t, font=date_f)) / 2, 46), t, font=date_f, fill=INK)
    sub = font(SANS_B, 17)
    t = "40 STORIES · 5 CONTINENTS · ONE PAGE"
    d.text(((W - d.textlength(t, font=sub)) / 2, 116), t, font=sub, fill=RED)
    d.line([MARGIN, 142, W - MARGIN, 142], fill=RULE, width=3)
    d.line([MARGIN, 148, W - MARGIN, 148], fill=RULE, width=1)


def draw_card(d, card, x, y, w, h):
    num, band, tag, head, summ, ic = card
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=(200, 192, 168), width=1)
    d.rectangle([x, y, x + w, y + 30], fill=band)
    # number chip
    d.ellipse([x + 6, y + 5, x + 26, y + 25], fill=(255, 255, 255))
    nf = font(SANS_B, 13)
    ns = str(num)
    d.text((x + 16 - d.textlength(ns, font=nf) / 2, y + 8), ns, font=nf, fill=band)
    tf = font(SANS_B, 11)
    d.text((x + 33, y + 9), tag, font=tf, fill=(255, 255, 255))
    icon(d, ic, x + w - 22, y + 15)
    # headline + summary, shrunk to fit if needed
    tx, tw = x + 9, w - 18
    hf, hl = fit_lines(d, head, CARD_SERIF_B, 16, tw, 3)
    yy = y + 38
    for ln in hl:
        d.text((tx, yy), ln, font=hf, fill=INK)
        yy += 20
    sf, sl = fit_lines(d, summ, SANS, 11, tw, 3)
    yy += 2
    for ln in sl:
        d.text((tx, yy), ln, font=sf, fill=(58, 62, 72))
        yy += 15


def draw_map_cell(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=(200, 192, 168), width=1)
    d.rectangle([x, y, x + w, y + 30], fill=NAVY)
    tf = font(SANS_B, 11)
    d.text((x + 10, y + 9), "WHERE IT HAPPENED", font=tf, fill=(255, 255, 255))
    gx, gy = x + 10, y + 40
    gw, gh = w - 20, h - 78
    cols, rows = len(LAND[0]), len(LAND)
    dx, dy = gw / cols, gh / rows
    for r, row in enumerate(LAND):
        for c, ch in enumerate(row):
            if ch == "#":
                cxp = gx + c * dx + dx / 2
                cyp = gy + r * dy + dy / 2
                d.ellipse([cxp - 1.6, cyp - 1.6, cxp + 1.6, cyp + 1.6],
                          fill=(120, 140, 170))
    pf = font(SANS_B, 9)
    for num, (gc, gr) in PINS.items():
        cxp = gx + gc * dx
        cyp = gy + gr * dy
        d.ellipse([cxp - 7, cyp - 7, cxp + 7, cyp + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        ns = str(num)
        d.text((cxp - d.textlength(ns, font=pf) / 2, cyp - 5), ns,
               font=pf, fill=(255, 255, 255))
    nf = font(SANS, 10)
    d.text((x + 10, y + h - 30), "Card 8 is off the map:", font=nf, fill=GREY)
    d.text((x + 10, y + h - 16), "two spacecraft at Mercury.", font=nf, fill=GREY)


def draw_briefs(d, y0):
    lab = font(SANS_B, 15)
    t = "— AND THE REST OF THE DAY: 29 MORE STORIES —"
    d.text(((W - d.textlength(t, font=lab)) / 2, y0), t, font=lab, fill=NAVY)
    y = y0 + 30
    col_w = (CW - 2 * 14) / 3
    nf = font(SANS_B, 11)
    bf = font(SANS, 11)
    per = 10
    for ci in range(3):
        cx = MARGIN + ci * (col_w + 14)
        yy = y
        for num, text in BRIEFS[ci * per:(ci + 1) * per]:
            ns = f"{num}."
            d.text((cx, yy), ns, font=nf, fill=RED)
            off = d.textlength(ns, font=nf) + 5
            lines = wrap(d, text, bf, col_w - off)
            for j, ln in enumerate(lines):
                d.text((cx + off if j == 0 else cx + off, yy), ln, font=bf, fill=INK)
                yy += 14
            yy += 5


def draw_footer(d):
    d.line([MARGIN, 986, W - MARGIN, 986], fill=RULE, width=1)
    ff = font(SANS, 10)
    t = ("Every story was reported on Sunday 22 November 2026; disputed claims are "
         "attributed. Sources: AP · Reuters · AFP · BBC · Al Jazeera · CNA · "
         "Japan Times · SCMP. Original drawings.")
    d.text(((W - d.textlength(t, font=ff)) / 2, 994), t, font=ff, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    # cards: 3 rows; rows 1-2 hold 4 cards, row 3 holds 3 cards + the map
    gap = 10
    cw4 = (CW - 3 * gap) / 4
    ch = 158
    y = 160
    idx = 0
    for row in range(2):
        for col in range(4):
            draw_card(d, CARDS[idx], MARGIN + col * (cw4 + gap), y, cw4, ch)
            idx += 1
        y += ch + gap
    for col in range(3):
        draw_card(d, CARDS[idx], MARGIN + col * (cw4 + gap), y, cw4, ch)
        idx += 1
    draw_map_cell(d, MARGIN + 3 * (cw4 + gap), y, cw4, ch)
    draw_briefs(d, y + ch + 16)
    draw_footer(d)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
