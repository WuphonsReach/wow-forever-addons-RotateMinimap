# Icon concepts

These scripts drew the icon options that came before the final icon. They are kept for reference only. To change the icon, use [tools/make_icon.py](../../tools/make_icon.py).

The final icon is option G (a navy compass face with a gold player arrow), with the N from the Grenze typeface at 50 degrees.

## The scripts

Each script writes 512×512 SVG files into the folder that you give it.

| Script | What it draws |
| --- | --- |
| `gen_icons.py` | The first 12 concepts, with more detail. Some are for a large icon only. |
| `gen_small.py` | Round 1 for the AddOn List, options A to F: bold, with a gold rim and one gold shape. It imports `gen_icons.py`. |
| `gen_small2.py` | Round 2, options G to L: variations on Tilted N (C) and Compass star (E). It imports `gen_icons.py` and `gen_small.py`. |
| `gen_final.py` | Option G with an N drawn from three lines, and its detailed version. |
| `extract_n.py`, `extract_n2.py` | Copy the outline of the capital N from font files into `glyphs.json` and `glyphs2.json`. |
| `gen_n.py` | Option G with an N from a typeface. It reads `glyphs.json`, or the file that the `GLYPHS` variable names. |

## Run them

Run the scripts from this folder:

```bash
python3 gen_icons.py out
python3 gen_small.py out/small
python3 gen_small2.py out/small2
```

Notes:

- `gen_icons.py` reads its output folder when another script imports it. Give a folder argument to every script.
- `extract_n.py` and `extract_n2.py` need fontTools (`pip install fonttools`). They also need the font files, in the folder that you give as the first argument. The fonts are not in the repo. Get them from the [Google Fonts repo](https://github.com/google/fonts/tree/main/ofl).
- To see a result at its real size, convert it: `rsvg-convert -w 64 -h 64 file.svg -o file.png`.

Git ignores `out/` and `glyphs*.json`, so the results do not go into the repo by accident.
