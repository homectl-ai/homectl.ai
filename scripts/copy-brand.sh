#!/bin/sh
# Copy homectl's logo files from the GradZero brand repo (the source of truth) into brand/,
# and make the square icons from them. Run it again whenever the logo changes there:
#   scripts/copy-brand.sh ../gradzero/brand/logo
# Needs rsvg-convert (brew install librsvg) and python3 with Pillow.
set -eu
src=${1:?usage: $0 <gradzero>/brand/logo}
dst=$(dirname "$0")/../brand
for f in lockup-homectl lockup-homectl-dark homectl-in-frame homectl-in-frame-dark \
	gradzero-mark-multi-merged gradzero-mark-multi-merged-dark; do
	cp "$src/$f.svg" "$dst/$f.svg"
done
cp "$src/homectl-in-frame.png" "$src/homectl-in-frame-dark.png" "$dst/"
cp "$dst/homectl-in-frame.svg" "$dst/favicon.svg"
cp "$dst/homectl-in-frame-dark.svg" "$dst/favicon-dark.svg"

# Square icons: the framed mark (220x180) centred on the page background, opaque, for the
# places that need a square (apple-touch-icon, favicon.ico, app consoles).
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
rsvg-convert -w 1024 "$dst/homectl-in-frame.svg" -o "$tmp/mark.png"
python3 - "$tmp/mark.png" "$dst" <<'PY'
import sys
from PIL import Image
mark, dst = Image.open(sys.argv[1]).convert("RGBA"), sys.argv[2]
def square(size, pad):
    bg = Image.new("RGBA", (size, size), "#fafaf9")
    w = round(size * (1 - 2 * pad))
    m = mark.resize((w, round(w * mark.height / mark.width)), Image.LANCZOS)
    bg.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return bg.convert("RGB")
square(180, .1).save(f"{dst}/apple-touch-icon.png")
square(120, .06).save(f"{dst}/logo-120.png")
square(512, .06).save(f"{dst}/logo-512.png")
square(256, .02).save(f"{dst}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
PY
