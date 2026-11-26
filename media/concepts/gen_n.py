"""Option G with a typeface N (outline paths from glyphs.json), at several angles."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_icons import P, svg  # noqa: E402
from gen_small import INK, gold_defs, round_frame, bevel_chevron  # noqa: E402
from gen_small2 import gold_ticks  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
GLYPHS = json.load(open(os.path.join(HERE, os.environ.get("GLYPHS", "glyphs.json"))))
FONTS = {"cinzel": "Cinzel", "marcellus": "Marcellus", "dejavu": "DejaVu Serif Bold", "freeserif": "FreeSerif Bold"}


def n_glyph(font, cx, cy, h, rot, fill="#F0614A", outline=8, edge=None, edge_w=0):
    g = GLYPHS[font]
    x0, y0, x1, y1 = g["bounds"]
    k = h / (y1 - y0)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    t = f'transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({k:.5f} {-k:.5f}) translate({-mx:.1f} {-my:.1f})"'
    out = f'<path d="{g["d"]}" fill="{INK}" stroke="{INK}" stroke-width="{outline * 2 / k:.1f}" stroke-linejoin="round" {t}/>'
    if edge:
        out += f'<path d="{g["d"]}" fill="{edge}" stroke="{edge}" stroke-width="{edge_w * 2 / k:.1f}" stroke-linejoin="round" {t}/>'
    out += f'<path d="{g["d"]}" fill="{fill}" {t}/>'
    return out


def ingame(font, angle, p="n_", r=124, h=96):
    n = P(r, angle)
    body = (round_frame(p, f"url(#{p}navy)") + gold_ticks(170, 190, angle, skip={0})
            + n_glyph(font, n[0], n[1], h, angle) + bevel_chevron(88, p, cy=264))
    return svg(body, gold_defs(p))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for font in FONTS:
        for ang in (50, 60, 70):
            open(os.path.join(out, f"{font}-{ang}.svg"), "w").write(ingame(font, ang))
    print("ok")
