#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Newspaper front page, 1024x1024 PNG, drawn entirely with PIL and
DejaVu fonts. No network, no photos, no copied artwork.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 245, 238)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (22, 35, 63)
GREY = (96, 94, 86)
SKY = (52, 84, 138)
GOLD = (232, 178, 74)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF_I = FD + "DejaVuSerif-Italic.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
MONO_B = FD + "DejaVuSansMono-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(SANS, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, weight=2, fill=INK):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)
    return y + weight


def kicker_head_body(draw, x, y, width, kicker, headline, body,
                     head_size=25, body_size=15, head_font=None):
    y = para(draw, x, y, [kicker], font(SANS_B, 14), fill=RED,
             leading=18)
    y += 3
    hf = head_font or font(SERIF_B, head_size)
    lines = wrap(draw, headline, hf, width)
    y = para(draw, x, y, lines, hf, leading=int(head_size * 1.12))
    y += 4
    bf = font(SANS, body_size)
    blines = wrap(draw, body, bf, width)
    y = para(draw, x, y, blines, bf,
             leading=int(body_size * 1.3))
    return y


def draw_lead_picture(draw, x, y, w, h):
    """Night sky over a skyline, two missile streaks, one burst."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    for sx, sy in [(18, 14), (52, 30), (96, 10), (150, 26), (205, 12),
                   (250, 34), (300, 16), (120, 44), (180, 52), (268, 52),
                   (36, 56), (225, 66)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(220, 225, 235))
    # moon
    draw.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(238, 232, 210))
    # missile streaks (head dot + fading trail)
    for (x0, y0, x1, y1) in [(30, 118, 150, 52), (120, 126, 235, 66)]:
        for i in range(5):
            t = i / 4.0
            px = x + x0 + (x1 - x0) * t
            py = y + y0 + (y1 - y0) * t
            r = 4 - i * 0.6
            draw.ellipse([px - r, py - r, px + r, py + r], fill=GOLD)
        draw.line([x + x0, y + y0, x + x1, y + y1], fill=GOLD, width=2)
    # burst at end of first streak
    bx, by = x + 150, y + 52
    for dx, dy in [(0, -11), (8, -8), (11, 0), (8, 8), (0, 11),
                   (-8, 8), (-11, 0), (-8, -8)]:
        draw.line([bx, by, bx + dx, by + dy], fill=(255, 196, 90), width=2)
    draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 220, 140))
    # skyline silhouette
    base = y + h
    heights = [46, 30, 58, 38, 66, 28, 50, 36, 60, 30]
    bw = w / len(heights)
    for i, bh in enumerate(heights):
        draw.rectangle([x + i * bw, base - bh, x + (i + 1) * bw - 2, base],
                       fill=(10, 16, 32))
        for wy in range(int(base - bh) + 8, base - 6, 14):
            draw.rectangle([x + i * bw + 5, wy, x + i * bw + 9, wy + 5],
                           fill=(255, 214, 120))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_market_chart(draw, x, y, w, h):
    """Small falling-line chart inside a thin frame."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=(255, 255, 255))
    pts = [(8, 50), (50, 44), (95, 48), (140, 34), (185, 38),
           (230, 24), (275, 26), (320, 14), (360, 16), (400, 6)]
    pts = [(x + px, y + h - 8 - py) for px, py in pts]
    draw.line(pts, fill=RED, width=3)
    draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                 fill=RED)
    draw.text((x + 8, y + 4), "S&P 500  -3.70%  THIS WEEK",
              font=font(SANS_B, 11), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34                      # side margin
    cw = W - 2 * mx              # content width

    # ---- masthead ----
    y = 22
    name = "THE WORLD IN ONE DAY"
    nf = font(SERIF_B, 57)
    tw = d.textlength(name, font=nf)
    d.text(((W - tw) / 2, y), name, font=nf, fill=INK)
    y += 72
    y = rule(d, mx, y, cw, 4)
    y = rule(d, mx, y + 2, cw, 1)
    y += 8
    df = font(SANS_B, 18)
    d.text((mx, y), "SATURDAY \u00b7 21 NOVEMBER 2026", font=df, fill=INK)
    rf = font(SANS, 13)
    right = "ALL THE WORLD'S NEWS \u00b7 IN ONE PAGE"
    d.text((W - mx - d.textlength(right, font=rf), y + 3), right,
           font=rf, fill=GREY)
    y += 26
    y = rule(d, mx, y, cw, 2)
    y += 10

    # ---- lead story ----
    y = para(d, mx, y, ["WAR IN EUROPE \u00b7 NATO ON ALERT"],
             font(SANS_B, 15), fill=RED, leading=19)
    y += 2
    hf = font(SERIF_B, 44)
    hl = wrap(d, "RUSSIAN MISSILES LAND IN POLAND", hf, cw)
    y = para(d, mx, y, hl, hf, leading=50)
    y += 6
    text_w = 600
    pic_x = mx + text_w + 26
    pic_w = W - mx - pic_x
    deck = ("Two missiles and a suspected drone came down in the east "
            "during the huge overnight barrage on Ukraine. Warsaw calls "
            "it a deliberate provocation; NATO calls it a grave violation.")
    body = ("A Kh-101 cruise missile was found near Nowy Lipowiec, about "
            "60 km from the Ukrainian border. No one was hurt in Poland. "
            "Warsaw has opened an investigation, and Swedish Gripen jets "
            "joined the response. NATO chief Mark Rutte is due in Warsaw "
            "today. The barrage fired more than 400 drones and 110 "
            "missiles at Ukraine, killing at least eight people.")
    ty = y
    ty = para(d, mx, ty, wrap(d, deck, font(SERIF_I, 17), text_w),
              font(SERIF_I, 17), leading=22)
    ty += 6
    ty = para(d, mx, ty, wrap(d, body, font(SANS, 15), text_w),
              font(SANS, 15), leading=20)
    draw_lead_picture(d, pic_x, y, pic_w, 140)
    cy = y + 140 + 6
    cy = para(d, pic_x, cy,
              wrap(d, "Missiles crossed into Poland during the night "
                      "attack on Ukraine. (Illustration)",
                   font(SERIF_I, 12), pic_w),
              font(SERIF_I, 12), leading=15)
    y = max(ty, cy) + 4
    y = rule(d, mx, y, cw, 2)
    y += 10

    # ---- row 2: COP31 | markets ----
    col_w = (cw - 30) // 2
    x2 = mx + col_w + 30
    y2 = y
    y2 = kicker_head_body(
        d, mx, y2, col_w,
        "CLIMATE \u00b7 ANTALYA",
        "COP31 RUNS INTO OVERTIME AS FOSSIL-FUEL DEAL FAILS",
        "Delegates rejected two draft deals in Antalya on Saturday, and "
        "the talks ran into overtime. The latest text drops any mention "
        "of phasing out fossil fuels and drops a proposed $120bn-a-year "
        "target for adaptation finance. The EU warns the draft is \u201ca "
        "substantial step backwards\u201d. The presidency worked "
        "overnight on a third text.",
        head_size=25, body_size=15)
    y3 = y
    y3 = para(d, x2, y3, ["MARKETS \u00b7 WALL STREET"],
              font(SANS_B, 14), fill=RED, leading=18)
    y3 += 3
    hf2 = font(SERIF_B, 25)
    y3 = para(d, x2, y3,
              wrap(d, "S&P 500 AND DOW SLIDE INTO CORRECTION", hf2, col_w),
              hf2, leading=28)
    y3 += 6
    draw_market_chart(d, x2, y3, col_w, 46)
    y3 += 46 + 8
    y3 = para(d, x2, y3,
              wrap(d, "The AI sell-off deepened on Friday. The S&P 500 "
                      "fell 3.70% to 6,910.39 and the Dow joined it in "
                      "correction territory; the Nasdaq lost 5.28%. "
                      "Tokyo's Nikkei fell 5.06% and Seoul's Kospi "
                      "5.21%. Anthropic slid after its debut.",
                   font(SANS, 15), col_w),
              font(SANS, 15), leading=20)
    y = max(y2, y3) + 4
    y = rule(d, mx, y, cw, 2)
    y += 10

    # ---- row 3: three short stories ----
    col3 = (cw - 2 * 24) // 3
    x3b = mx + col3 + 24
    x3c = x3b + col3 + 24
    ya = kicker_head_body(
        d, mx, y, col3,
        "CYBER \u00b7 UNITED STATES",
        "FBI DATABASE HACKED AS US OUTAGES GO ON",
        "The FBI and the Agriculture Department were hit by cyberattacks "
        "amid wider US computer outages, separate from the Outlook and "
        "aviation outages.",
        head_size=21, body_size=13)
    yb = kicker_head_body(
        d, x3b, y, col3,
        "COURTS \u00b7 MISSOURI",
        "BAYER'S $7.25BN ROUNDUP DEAL APPROVED",
        "A Missouri judge approved one of the largest mass-tort "
        "settlements in history, covering people who say Roundup made "
        "them ill. Bayer denies it causes cancer.",
        head_size=21, body_size=13)
    yc = kicker_head_body(
        d, x3c, y, col3,
        "CULTURE \u00b7 GAMES",
        "GTA VI TAKES $3.79BN IN A DAY",
        "Rockstar says it took $3.79bn in retail sales in its first 24 "
        "hours \u2014 the biggest entertainment launch ever. It sold "
        "32.5m units; Metacritic: 99.",
        head_size=21, body_size=13)
    y = max(ya, yb, yc) + 4
    y = rule(d, mx, y, cw, 2)
    y += 8

    # ---- in brief ----
    y = para(d, mx, y, ["IN BRIEF"], font(SANS_B, 15), fill=RED,
             leading=18)
    y += 2
    briefs = [
        ("WASHINGTON", "A US court rules 9\u20138 the House passed a "
         "$1.7tn bill unconstitutionally."),
        ("HORMUZ", "Iran says it shot down a US MQ-9 drone over the "
         "strait."),
        ("PERU", "A 6.9 quake shakes the Andes; no damage reported at "
         "first."),
        ("IRAQ", "A fire at a Basra power plant kills at least four."),
        ("HEALTH", "A cancer pill makes tumours undetectable in 1 in 12 "
         "patients."),
        ("RIYADH", "Houthi missiles fired at the capital; three "
         "intercepted."),
    ]
    bw = (cw - 2 * 24) // 3
    bx = [mx, mx + bw + 24, mx + 2 * (bw + 24)]
    bf = font(SANS, 12)
    bfb = font(SANS_B, 12)
    row_y = y
    for row in range(2):
        max_h = 0
        for col in range(3):
            label, text = briefs[row * 3 + col]
            x = bx[col]
            lab = label + " \u2014 "
            lab_w = d.textlength(lab, font=bfb)
            lines = wrap(d, text, bf, bw - lab_w)
            yy = row_y
            # first line: body text offset by the label width, label in bold
            d.text((x + lab_w, yy), lines[0], font=bf, fill=INK)
            d.text((x, yy), lab, font=bfb, fill=INK)
            yy += 15
            for ln in lines[1:]:
                d.text((x, yy), ln, font=bf, fill=INK)
                yy += 15
            max_h = max(max_h, yy - row_y)
        row_y += max_h + 4
    y = row_y + 2
    y = rule(d, mx, y, cw, 2)
    y += 8

    # ---- ticker ----
    tick = ("S&P 500  6,910.39  \u25bc3.70%    NASDAQ  22,617.73  "
            "\u25bc5.28%    NIKKEI  56,436.65  \u25bc5.06%    GOLD  $3,515.40  "
            "\u25bc4.62%    BRENT  $89.95  \u25bc2.21%")
    tf = font(MONO_B, 14)
    tw = d.textlength(tick, font=tf)
    while tw > cw - 16 and tf.size > 11:
        tf = font(MONO_B, tf.size - 1)
        tw = d.textlength(tick, font=tf)
    d.rectangle([mx, y, mx + cw, y + 34], fill=INK)
    d.text((mx + (cw - tw) / 2, y + 9), tick, font=tf, fill=(255, 255, 255))
    y += 34
    print("final y:", y)

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
