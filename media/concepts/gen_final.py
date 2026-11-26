"""Option G (Tilted N, gold ticks): the in-game icon and a detailed CurseForge version."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_icons import P, f, svg  # noqa: E402
from gen_small import INK, gold_defs, round_frame, bevel_chevron  # noqa: E402
from gen_small2 import n_letter, gold_ticks  # noqa: E402

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def ingame(angle, p="g_", lrot=None):
    lrot = angle if lrot is None else lrot
    n = P(126, angle)
    body = (round_frame(p, f"url(#{p}navy)") + gold_ticks(170, 190, angle, skip={0})
            + n_letter(n[0], n[1], 90, "#F0614A", 26, lrot) + bevel_chevron(88, p, cy=264))
    return svg(body, gold_defs(p))


def detailed(angle, p="cf_", lrot=None, letter_svg=None):
    lrot = angle if lrot is None else lrot
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
    # Faint map that turns with the N (contours and a river), clipped to the face.
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
    # N: gold-edged red enamel.
    hw, h = 90 * 0.36, 90
    nd = f"M{n[0]-hw:.1f},{n[1]+h/2:.1f} V{n[1]-h/2:.1f} L{n[0]+hw:.1f},{n[1]+h/2:.1f} V{n[1]-h/2:.1f}"
    t = f'stroke-miterlimit="1.6" fill="none" transform="rotate({lrot} {n[0]:.1f} {n[1]:.1f})"'
    letter = (f'<path d="{nd}" stroke="{INK}" stroke-width="50" {t}/>'
              f'<path d="{nd}" stroke="url(#{p}gold)" stroke-width="40" {t}/>'
              f'<path d="{nd}" stroke="#D63A22" stroke-width="24" {t}/>'
              f'<path d="{nd}" stroke="#FF8A6E" stroke-width="8" opacity=".55" {t}/>')
    if letter_svg:
        letter = letter_svg
    # Chevron with a highlight on its lit edge.
    s, cy = 90, 264
    y = lambda v: cy + v + 0.1 * s  # noqa: E731
    tip, lft, notch = (256, y(-s)), (256 - 0.74 * s, y(0.8 * s)), (256, y(0.36 * s))
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


if __name__ == "__main__":
    for tag, lr in (("upright", 0), ("half", 30)):
        open(os.path.join(OUT, f"ingame-60-{tag}.svg"), "w").write(ingame(60, lrot=lr))
        open(os.path.join(OUT, f"curseforge-60-{tag}.svg"), "w").write(detailed(60, lrot=lr))
    print("ok")
