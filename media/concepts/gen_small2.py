"""Round 2 of in-game icons: variations on Tilted N (C) and Compass star (E), navy and gold."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_icons import P, f, svg  # noqa: E402
from gen_small import INK, gold_defs, round_frame, bevel_chevron  # noqa: E402

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
RED_L, RED_D = "#FF7A5E", "#B32E18"
GOLD_L, GOLD_D = "#FFE7A0", "#C88A26"
STEEL_L, STEEL_D = "#A9BCD3", "#5F7592"


def n_letter(cx, cy, h, color, w, rot, outline=20):
    hw = h * 0.36
    d = f"M{cx-hw:.1f},{cy+h/2:.1f} V{cy-h/2:.1f} L{cx+hw:.1f},{cy+h/2:.1f} V{cy-h/2:.1f}"
    t = f'transform="rotate({rot} {cx:.1f} {cy:.1f})"'
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + outline}" stroke-miterlimit="1.6" {t}/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-miterlimit="1.6" {t}/>')


def gold_ticks(r1, r2, rot, n=8, w=14, color="#E2B455", skip=None):
    out = []
    for i in range(n):
        a = rot + i * 360 / n
        if skip is not None and i in skip:
            continue
        out.append(f'<line x1="{P(r1, a)[0]:.1f}" y1="{P(r1, a)[1]:.1f}" x2="{P(r2, a)[0]:.1f}" '
                   f'y2="{P(r2, a)[1]:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
    return "".join(out)


def star(R, rin, rot, north=(RED_L, RED_D), body=(GOLD_L, GOLD_D), outline=22, points=(0, 90, 180, 270)):
    """Four-point star; the point at offset 0 is north."""
    sh, fill = [], []
    for off in points:
        a = rot + off
        tip, l, r = P(R, a), P(rin, a - 45), P(rin, a + 45)
        sh.append(f'<path d="M256,256 L{f(tip)} L{f(l)} L{f(r)} Z" fill="{INK}" stroke="{INK}" '
                  f'stroke-width="{outline}" stroke-linejoin="round"/>')
        lt, dk = north if off == 0 else body
        fill.append(f'<path d="M256,256 L{f(tip)} L{f(l)} Z" fill="{lt}"/>'
                    f'<path d="M256,256 L{f(tip)} L{f(r)} Z" fill="{dk}"/>')
    return "".join(sh), "".join(fill)


def hub(r=22):
    return f'<circle cx="256" cy="256" r="{r}" fill="{GOLD_L}" stroke="{INK}" stroke-width="8"/>'


def index_notch(p):
    a, b, c = P(198, 0), P(160, -11), P(160, 11)
    return (f'<path d="M{f(a)} L{f(b)} L{f(c)} Z" fill="url(#{p}gold)" stroke="{INK}" stroke-width="10" '
            f'stroke-linejoin="round"/>')


SMALL = []


def small(slug, name, note):
    def deco(fn):
        SMALL.append((slug, name, note, fn))
        return fn
    return deco


ROT = 32


@small("g-tilted-n-gold", "Tilted N, gold ticks",
       "C with gold ticks in place of the blue ones, and a larger N and arrow.")
def g(p):
    n = P(126, ROT)
    body = (round_frame(p, f"url(#{p}navy)") + gold_ticks(170, 190, ROT, skip={0})
            + n_letter(n[0], n[1], 90, "#F0614A", 26, ROT) + bevel_chevron(88, p, cy=272))
    return svg(body, gold_defs(p))


@small("h-tilted-n-bezel", "Tilted N, notch",
       "C with a fixed gold notch at the top. The N has turned away from the notch, so the map has turned.")
def h(p):
    n = P(126, ROT)
    body = (round_frame(p, f"url(#{p}navy)") + gold_ticks(176, 192, ROT, n=8, w=12, skip={0})
            + n_letter(n[0], n[1], 84, "#F0614A", 24, ROT) + index_notch(p) + bevel_chevron(80, p, cy=280))
    return svg(body, gold_defs(p))


@small("i-compass-star", "Compass star, larger",
       "E with a bigger star that almost touches the rim, and a smaller hub.")
def i(p):
    sh, fill = star(186, 46, 30)
    return svg(round_frame(p, f"url(#{p}navy)") + sh + fill + hub(18), gold_defs(p))


@small("j-eight-point-rose", "Eight-point rose",
       "E with four short steel-blue points between the gold ones. More like a real compass rose.")
def j(p):
    sh2, fill2 = star(118, 34, 75, north=(STEEL_L, STEEL_D), body=(STEEL_L, STEEL_D), outline=18)
    sh, fill = star(186, 44, 30)
    return svg(round_frame(p, f"url(#{p}navy)") + sh2 + fill2 + sh + fill + hub(18), gold_defs(p))


@small("k-star-and-arrow", "Star under arrow",
       "C and E together: a turned steel star with a red north point, under a fixed gold player arrow.")
def k(p):
    sh, fill = star(186, 40, ROT, north=(RED_L, RED_D), body=(STEEL_L, STEEL_D), outline=18)
    return svg(round_frame(p, f"url(#{p}navy)") + sh + fill + bevel_chevron(70, p, outline=14), gold_defs(p))


@small("l-compass-needle", "Compass needle",
       "A two-tone needle, red north and gold south, turned away from a fixed gold notch.")
def l_(p):
    sh, fill = star(184, 40, ROT, points=(0, 180), body=(GOLD_L, GOLD_D))
    body = (round_frame(p, f"url(#{p}navy)") + gold_ticks(178, 192, ROT, n=8, w=10, skip={0, 4})
            + index_notch(p) + sh + fill + hub(20))
    return svg(body, gold_defs(p))


if __name__ == "__main__":
    meta = []
    for slug, name, note, fn in SMALL:
        with open(os.path.join(OUT, f"{slug}.svg"), "w") as fh:
            fh.write(fn(slug[:1] + "2_"))
        meta.append({"slug": slug, "name": name, "note": note})
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    print(f"wrote {len(meta)} icons")
