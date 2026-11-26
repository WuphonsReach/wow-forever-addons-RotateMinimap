"""Draw the addon icon: media/icon.svg (the AddOn List icon) and media/icon-curseforge.svg (the detailed version).

    python3 tools/make_icon.py            # write the two SVGs
    python3 tools/make_icon.py --render   # also write icon.tga (64x64) and media/icon-curseforge-400.png

Writing the SVGs needs only Python. --render also needs rsvg-convert (librsvg) and ImageMagick 7 (`magick`).

The design: a gold rim around a navy compass face. The gold player arrow points up and stays fixed. The red N
and the tick marks are turned ANGLE degrees clockwise, as on a turning minimap. The N is the capital N of the
Grenze typeface (SIL Open Font License 1.1), stored below as an outline path, so the SVGs need no font file.
The early concepts and the scripts that made them are in media/concepts/.
"""

import math
import shutil
import subprocess
import sys

from addon import ROOT

ANGLE = 50  # where the N sits, in degrees clockwise from the top
C = 256  # the centre of the 512x512 drawing
INK = "#2A1804"  # the dark outline colour

# Capital N from Grenze (wght 700), in font units with y up: (path, (xmin, ymin, xmax, ymax)).
GRENZE_N = ((
    'M408.999267578125 -10.599853515625Q407.5992431640625 -10.599853515625 400.79931640625 -6.69989013671'
    '875Q393.9993896484375 -2.7999267578125 388.199462890625 0.4000244140625L276.19921875 233.80249023437'
    '5Q262.5994873046875 260.6021728515625 248.99951171875 293.20220947265625Q235.3995361328125 325.80224'
    '609375 224.2994384765625 357.00250244140625Q213.1993408203125 388.2027587890625 205.7991943359375 41'
    '0.403076171875H196.999267578125L206.3992919921875 123.5989990234375V88.198974609375L274.799194335937'
    '5 65.1990966796875V0H28.800537109375V58.399169921875L89.6005859375 81.3990478515625V527.000732421875'
    'L28.800537109375 550.0006103515625V608.3997802734375H262.5985107421875L392.3988037109375 332.7973632'
    '8125Q400.9986572265625 315.5975341796875 410.898681640625 288.79736328125Q420.7987060546875 261.9971'
    '923828125 430.1988525390625 234.29681396484375Q439.5989990234375 206.596435546875 445.9991455078125 '
    '184.7960205078125H455.1990966796875L445.799072265625 487.6007080078125V520.2008056640625L377.9991455'
    '078125 543.20068359375V608.3997802734375H623.3978271484375V550.0006103515625L562.5977783203125 527.0'
    '00732421875V6.4000244140625Q533.7982177734375 2.800048828125 498.49853515625 -1.09991455078125Q463.1'
    '988525390625 -4.9998779296875 437.4990234375 -7.79986572265625Q411.7991943359375 -10.599853515625 40'
    '8.999267578125 -10.599853515625Z'
), (28.800537109375, -10.599853515625, 623.3978271484375, 608.3997802734375))


# ---------- geometry (angle 0 is up, positive is clockwise) ----------

def P(r, a, cx=C, cy=C):
    t = math.radians(a)
    return (cx + r * math.sin(t), cy - r * math.cos(t))


def f(pt):
    return f"{pt[0]:.1f},{pt[1]:.1f}"


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
            f'<defs>{defs}</defs>{body}</svg>\n')


# ---------- shared parts ----------

def gold_defs(p):
    return f"""
<linearGradient id="{p}gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFEBA8"/><stop offset=".45" stop-color="#E2A93C"/><stop offset="1" stop-color="#8C5A12"/></linearGradient>
<linearGradient id="{p}rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE39A"/><stop offset=".5" stop-color="#C98E2A"/><stop offset="1" stop-color="#6E440C"/></linearGradient>
<radialGradient id="{p}navy" cx=".4" cy=".35"><stop offset="0" stop-color="#26365A"/><stop offset="1" stop-color="#0C1222"/></radialGradient>
<radialGradient id="{p}teal" cx=".4" cy=".35"><stop offset="0" stop-color="#2A9AA8"/><stop offset="1" stop-color="#0B4450"/></radialGradient>"""


def round_frame(p, face, inner=196):
    return f"""
<circle cx="256" cy="256" r="254" fill="{INK}"/>
<circle cx="256" cy="256" r="244" fill="url(#{p}rim)"/>
<circle cx="256" cy="256" r="{inner + 6}" fill="{INK}"/>
<circle cx="256" cy="256" r="{inner}" fill="{face}"/>
<circle cx="256" cy="256" r="{inner - 4}" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="10"/>"""


def bevel_chevron(s, p, cx=256, cy=256, outline=12):
    """The player arrow: a light left half and a dark right half, with a dark outline."""
    y = lambda v: cy + v + 0.1 * s  # noqa: E731
    tip, rgt, notch, lft = (cx, y(-s)), (cx + 0.74 * s, y(0.8 * s)), (cx, y(0.36 * s)), (cx - 0.74 * s, y(0.8 * s))
    return (f'<path d="M{f(tip)} L{f(rgt)} L{f(notch)} L{f(lft)} Z" fill="{INK}" stroke="{INK}" '
            f'stroke-width="{outline * 2}" stroke-linejoin="round"/>'
            f'<path d="M{f(tip)} L{f(notch)} L{f(lft)} Z" fill="#FFE7A0"/>'
            f'<path d="M{f(tip)} L{f(rgt)} L{f(notch)} Z" fill="#C88A26"/>')


def gold_ticks(r1, r2, rot, n=8, w=14, color="#E2B455", skip=None):
    out = []
    for i in range(n):
        a = rot + i * 360 / n
        if skip is not None and i in skip:
            continue
        out.append(f'<line x1="{P(r1, a)[0]:.1f}" y1="{P(r1, a)[1]:.1f}" x2="{P(r2, a)[0]:.1f}" '
                   f'y2="{P(r2, a)[1]:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
    return "".join(out)


def n_glyph(cx, cy, h, rot, fill="#F0614A", outline=8, edge=None, edge_w=0):
    """The Grenze N, centred on (cx, cy), h pixels tall, turned rot degrees, with a dark outline."""
    d, (x0, y0, x1, y1) = GRENZE_N
    k = h / (y1 - y0)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    t = f'transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({k:.5f} {-k:.5f}) translate({-mx:.1f} {-my:.1f})"'
    out = f'<path d="{d}" fill="{INK}" stroke="{INK}" stroke-width="{outline * 2 / k:.1f}" stroke-linejoin="round" {t}/>'
    if edge:
        out += f'<path d="{d}" fill="{edge}" stroke="{edge}" stroke-width="{edge_w * 2 / k:.1f}" stroke-linejoin="round" {t}/>'
    out += f'<path d="{d}" fill="{fill}" {t}/>'
    return out


# ---------- the two icons ----------

def ingame(angle=ANGLE, p="n_"):
    """Bold and simple, for about 35 px in the AddOn List."""
    n = P(124, angle)
    body = (round_frame(p, f"url(#{p}navy)") + gold_ticks(170, 190, angle, skip={0})
            + n_glyph(n[0], n[1], 100, angle) + bevel_chevron(88, p, cy=264))
    return svg(body, gold_defs(p))


def detailed(angle=ANGLE, p="cf_"):
    """The same layout with more detail, for the CurseForge avatar (400x400)."""
    n = P(124, angle)
    defs = gold_defs(p) + f"""
<radialGradient id="{p}face" cx=".42" cy=".36" r=".7"><stop offset="0" stop-color="#2C406A"/><stop offset=".7" stop-color="#14203A"/><stop offset="1" stop-color="#080D18"/></radialGradient>
<linearGradient id="{p}rim2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF0BE"/><stop offset=".3" stop-color="#E6B04A"/><stop offset=".65" stop-color="#A9711C"/><stop offset="1" stop-color="#5E3A08"/></linearGradient>
<linearGradient id="{p}rimin" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFE39A"/><stop offset=".5" stop-color="#B07A22"/><stop offset="1" stop-color="#5E3A08"/></linearGradient>
<linearGradient id="{p}sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".16"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>
<radialGradient id="{p}edge"><stop offset=".78" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<clipPath id="{p}clip"><circle cx="256" cy="256" r="200"/></clipPath>"""
    studs = "".join(
        f'<circle cx="{P(229, a)[0]:.1f}" cy="{P(229, a)[1]:.1f}" r="7.5" fill="url(#{p}rim2)" stroke="{INK}" stroke-width="2.5"/>'
        for a in range(0, 360, 45))
    # A faint map (contours, a river, a road) that turns with the N, clipped to the face.
    contours = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({r} {cx} {cy})" fill="none" '
        f'stroke="#4A6A98" stroke-width="3" opacity=".45"/>'
        for cx, cy, rx, ry, r in [(170, 170, 70, 44, 20), (170, 170, 44, 26, 25), (170, 170, 20, 12, 30),
                                  (350, 340, 80, 52, -15), (350, 340, 52, 32, -10), (350, 340, 26, 15, -5),
                                  (380, 150, 40, 28, 40)])
    river = ('<path d="M40,300 C120,280 160,330 230,300 C300,270 300,200 380,210 C430,216 460,190 480,170" '
             'fill="none" stroke="#2F5A8E" stroke-width="12" stroke-linecap="round" opacity=".7"/>')
    road = ('<path d="M120,470 C160,400 220,390 250,340 C280,290 260,230 300,180 C330,140 330,90 320,40" '
            'fill="none" stroke="#5E7699" stroke-width="5" stroke-dasharray="14 10" stroke-linecap="round" opacity=".55"/>')
    face_map = f'<g clip-path="url(#{p}clip)"><g transform="rotate({angle} 256 256)">{contours}{river}{road}</g></g>'
    minor = "".join(
        f'<line x1="{P(188, a)[0]:.1f}" y1="{P(188, a)[1]:.1f}" x2="{P(198, a)[0]:.1f}" y2="{P(198, a)[1]:.1f}" '
        f'stroke="#D9B260" stroke-width="2.5" opacity=".75"/>'
        for a in [angle + i * 5 for i in range(72)] if round((a - angle) % 45) != 0)
    major = gold_ticks(172, 198, angle, w=9, skip={0}, color="#F0C766")
    letter = n_glyph(n[0], n[1], 100, angle, fill="#D63A22", outline=9, edge=f"url(#{p}gold)", edge_w=5)
    # The player arrow, with a highlight on its lit edge.
    s, cy = 90, 264
    y = lambda v: cy + v + 0.1 * s  # noqa: E731
    tip, lft = (256, y(-s)), (256 - 0.74 * s, y(0.8 * s))
    glint = (f'<path d="M{f((tip[0] - 6, tip[1] + 22))} L{f((lft[0] + 18, lft[1] - 12))}" stroke="#FFF8DC" '
             f'stroke-width="5" stroke-linecap="round" opacity=".8"/>')
    body = f"""
<circle cx="256" cy="256" r="255" fill="{INK}"/>
<circle cx="256" cy="256" r="247" fill="url(#{p}rim2)"/>
<circle cx="256" cy="256" r="240" fill="none" stroke="#FFF4CC" stroke-width="2" opacity=".6"/>
<circle cx="256" cy="256" r="218" fill="none" stroke="{INK}" stroke-width="3" opacity=".55"/>
{studs}
<circle cx="256" cy="256" r="212" fill="{INK}"/>
<circle cx="256" cy="256" r="208" fill="url(#{p}rimin)"/>
<circle cx="256" cy="256" r="200" fill="url(#{p}face)"/>
{face_map}
{minor}{major}
<circle cx="256" cy="256" r="200" fill="url(#{p}edge)"/>
{letter}
{bevel_chevron(s, p, cy=cy, outline=12)}
{glint}
<g clip-path="url(#{p}clip)"><ellipse cx="200" cy="120" rx="210" ry="120" transform="rotate(-25 200 120)" fill="url(#{p}sheen)"/></g>"""
    return svg(body, defs)


def render():
    """icon.tga: 64x64, 32-bit, uncompressed, rows stored from the bottom (as the other Forever addons use).
    Without -flip, the game shows the icon upside down: -orient only sets the header flag."""
    for tool in ("rsvg-convert", "magick"):
        if not shutil.which(tool):
            sys.exit(f"--render needs {tool}")
    png = subprocess.run(["rsvg-convert", "-w", "64", "-h", "64", str(ROOT / "media/icon.svg")],
                         check=True, capture_output=True).stdout
    subprocess.run(["magick", "-", "-flip", "-compress", "none", "-type", "TrueColorAlpha", "-orient", "BottomLeft",
                    str(ROOT / "icon.tga")], input=png, check=True)
    subprocess.run(["rsvg-convert", "-w", "400", "-h", "400", "-o", str(ROOT / "media/icon-curseforge-400.png"),
                    str(ROOT / "media/icon-curseforge.svg")], check=True)
    print("wrote icon.tga and media/icon-curseforge-400.png")


def main():
    if sys.argv[1:] not in ([], ["--render"]):
        sys.exit("usage: make_icon.py [--render]")
    (ROOT / "media").mkdir(exist_ok=True)
    (ROOT / "media/icon.svg").write_text(ingame(), encoding="utf-8")
    (ROOT / "media/icon-curseforge.svg").write_text(detailed(), encoding="utf-8")
    print("wrote media/icon.svg and media/icon-curseforge.svg")
    if sys.argv[1:] == ["--render"]:
        render()


if __name__ == "__main__":
    main()
