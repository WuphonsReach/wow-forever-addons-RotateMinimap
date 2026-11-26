"""In-game AddOn List icon candidates: bold, full-bleed, gold rim, one gold glyph."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_icons import P, f, arc_arrow, rose_point, svg  # noqa: E402

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
INK = "#2A1804"


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
    y = lambda v: cy + v + 0.1 * s  # noqa: E731
    tip, rgt, notch, lft = (cx, y(-s)), (cx + 0.74 * s, y(0.8 * s)), (cx, y(0.36 * s)), (cx - 0.74 * s, y(0.8 * s))
    return (f'<path d="M{f(tip)} L{f(rgt)} L{f(notch)} L{f(lft)} Z" fill="{INK}" stroke="{INK}" '
            f'stroke-width="{outline * 2}" stroke-linejoin="round"/>'
            f'<path d="M{f(tip)} L{f(notch)} L{f(lft)} Z" fill="#FFE7A0"/>'
            f'<path d="M{f(tip)} L{f(rgt)} L{f(notch)} Z" fill="#C88A26"/>')


def gold_arrow(r, a0, a1, w, p, head=1.4):
    return (arc_arrow(r, a0, a1, w, INK, INK, 22, head=head)
            + arc_arrow(r, a0, a1, w, f"url(#{p}gold)", head=head))


SMALL = []


def small(slug, name, note):
    def deco(fn):
        SMALL.append((slug, name, note, fn))
        return fn
    return deco


@small("s1-navy-turn", "Navy turn",
       "Gold player arrow inside one turn arrow, on a navy face in a gold rim.")
def s1(p):
    return svg(round_frame(p, f"url(#{p}navy)") + gold_arrow(146, 30, 296, 46, p) + bevel_chevron(72, p),
               gold_defs(p))


@small("s2-teal-turn", "Teal turn",
       "The same idea on a teal face, with two turn arrows. Close to the colours of OneForAll.")
def s2(p):
    return svg(round_frame(p, f"url(#{p}teal)") + gold_arrow(148, 18, 138, 42, p)
               + gold_arrow(148, 198, 318, 42, p) + bevel_chevron(64, p), gold_defs(p))


@small("s3-tilted-n", "Tilted N",
       "Fixed player arrow with the N swung off to the side. The N is the clue that the map turns.")
def s3(p):
    n = P(128, 34)
    hw, h = 30, 82
    nd = f"M{n[0]-hw:.1f},{n[1]+h/2:.1f} V{n[1]-h/2:.1f} L{n[0]+hw:.1f},{n[1]+h/2:.1f} V{n[1]-h/2:.1f}"
    rot = f'transform="rotate(34 {n[0]:.1f} {n[1]:.1f})"'
    letter = (f'<path d="{nd}" fill="none" stroke="{INK}" stroke-width="44" stroke-miterlimit="1.6" {rot}/>'
              f'<path d="{nd}" fill="none" stroke="#F0614A" stroke-width="24" stroke-miterlimit="1.6" {rot}/>')
    ticks = "".join(
        f'<line x1="{P(168, a)[0]:.1f}" y1="{P(168, a)[1]:.1f}" x2="{P(194, a)[0]:.1f}" y2="{P(194, a)[1]:.1f}" '
        f'stroke="#9FB6CC" stroke-width="12"/>' for a in range(34 + 45, 34 + 360, 45))
    return svg(round_frame(p, f"url(#{p}navy)") + ticks + letter + bevel_chevron(84, p, cy=270), gold_defs(p))


@small("s4-map-window", "Map window",
       "A simple turned map (land, lake, river) in the gold rim, with a red N gem. The small version of option 01.")
def s4(p):
    defs = gold_defs(p) + f'<clipPath id="{p}c"><circle cx="256" cy="256" r="196"/></clipPath>'
    gem = P(220, -34)
    terrain = f"""<g clip-path="url(#{p}c)"><g transform="rotate(-34 256 256)">
<rect width="512" height="512" fill="#4F7F3D"/>
<path d="M0,320 C120,290 200,360 300,330 C380,305 440,260 512,260 V512 H0Z" fill="#679A4C"/>
<ellipse cx="350" cy="170" rx="80" ry="54" fill="#3C8CB4"/>
<path d="M-10,200 C90,230 150,170 230,230 C300,280 360,300 520,360" fill="none" stroke="#3C8CB4" stroke-width="36" stroke-linecap="round"/>
<circle cx="150" cy="140" r="34" fill="#2E5A2B"/><circle cx="310" cy="390" r="34" fill="#2E5A2B"/></g></g>"""
    body = (round_frame(p, "#4F7F3D") + terrain
            + f'<circle cx="256" cy="256" r="192" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="10"/>'
            + bevel_chevron(76, p)
            + f'<circle cx="{gem[0]:.1f}" cy="{gem[1]:.1f}" r="40" fill="{INK}"/>'
            + f'<circle cx="{gem[0]:.1f}" cy="{gem[1]:.1f}" r="31" fill="#D23A22"/>'
            + f'<circle cx="{gem[0]-9:.1f}" cy="{gem[1]-10:.1f}" r="10" fill="#FF9A7A"/>')
    return svg(body, defs)


@small("s5-compass-star", "Compass star",
       "A four-point gold star turned 30 degrees, with a red north point. Matches the star shape in the Spoken icons.")
def s5(p):
    star = "".join(rose_point(176, 44, a, "#FFE7A0", "#C88A26") for a in (120, 210, 300))
    star += rose_point(176, 44, 30, "#FF7A5E", "#B32E18")
    outline = "".join(
        f'<path d="M256,256 L{f(P(176, a))} L{f(P(44, a + 45))} Z" fill="{INK}" stroke="{INK}" stroke-width="22" '
        f'stroke-linejoin="round"/>' for a in (30, 120, 210, 300))
    outline += "".join(
        f'<path d="M256,256 L{f(P(176, a))} L{f(P(44, a - 45))} Z" fill="{INK}" stroke="{INK}" stroke-width="22" '
        f'stroke-linejoin="round"/>' for a in (30, 120, 210, 300))
    hub = f'<circle cx="256" cy="256" r="22" fill="#FFE7A0" stroke="{INK}" stroke-width="8"/>'
    return svg(round_frame(p, f"url(#{p}navy)") + outline + star + hub, gold_defs(p))


@small("s6-arrow-rim", "Arrow rim",
       "No closed rim: the gold ring itself is the turn arrow, around the player arrow.")
def s6(p):
    face = (f'<circle cx="256" cy="256" r="232" fill="{INK}"/>'
            f'<circle cx="256" cy="256" r="222" fill="url(#{p}navy)"/>')
    return svg(face + gold_arrow(176, 28, 300, 64, p, head=1.25) + bevel_chevron(82, p), gold_defs(p))


if __name__ == "__main__":
    meta = []
    for slug, name, note, fn in SMALL:
        with open(os.path.join(OUT, f"{slug}.svg"), "w") as fh:
            fh.write(fn(slug[:2] + "_"))
        meta.append({"slug": slug, "name": name, "note": note})
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    print(f"wrote {len(meta)} icons")
