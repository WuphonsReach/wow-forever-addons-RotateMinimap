"""Extract capital N from the narrower candidate fonts into glyphs2.json (font units, y up)."""
import json
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

D = sys.argv[1]
FONTS = [
    ("cinzel", D + "/Cinzel.ttf", {"wght": 900}),
    ("grenze", D + "/Grenze.ttf", {"wght": 700}),
    ("robotoserif", D + "/RobotoSerif.ttf", {"wght": 800, "wdth": 50, "opsz": 8, "GRAD": 0}),
    ("notoserif", D + "/NotoSerif.ttf", {"wght": 800, "wdth": 62.5}),
    ("rokkitt", D + "/Rokkitt.ttf", {"wght": 800}),
    ("oswald", D + "/Oswald.ttf", {"wght": 700}),
    ("medievalsharp", D + "/MedievalSharp.ttf", None),
    ("dejavu", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", None),
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
    x0, y0, x1, y1 = bp.bounds
    out[key] = {"d": pen.getCommands(), "bounds": bp.bounds}
    print(f"{key:14s} width/height = {(x1 - x0) / (y1 - y0):.2f}")
json.dump(out, open(sys.argv[2], "w"))
