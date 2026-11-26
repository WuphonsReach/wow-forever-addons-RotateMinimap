"""Extract the outline of capital N from several fonts into glyphs.json (font units, y up)."""
import json
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = [
    ("cinzel", sys.argv[1] + "/Cinzel.ttf", {"wght": 800}),
    ("marcellus", sys.argv[1] + "/Marcellus.ttf", None),
    ("dejavu", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", None),
    ("freeserif", "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf", None),
]
out = {}
for key, path, axes in FONTS:
    font = TTFont(path)
    if axes:
        font = instancer.instantiateVariableFont(font, axes)
    gs = font.getGlyphSet()
    name = font.getBestCmap()[ord("N")]
    pen = SVGPathPen(gs)
    gs[name].draw(pen)
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    out[key] = {"d": pen.getCommands(), "bounds": bp.bounds}
json.dump(out, open(sys.argv[2], "w"))
print({k: v["bounds"] for k, v in out.items()})
