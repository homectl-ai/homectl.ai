# homectl.ai

The homectl.ai site (GitHub Pages) and the Go vanity import pages for `homectl.ai/homectl` and
`homectl.ai/homectl-net`. Pages needs the repo public on the free plan, or a paid plan for private repos.

## Logo
The logo comes from the GradZero brand repo (`brand/logo/` there is the source of truth); `brand/` here holds
copies, so the site doesn't depend on it. When the logo changes, regenerate it there and run
`scripts/copy-brand.sh <gradzero>/brand/logo`. Each file has a `-dark` twin, picked by `prefers-color-scheme`:
`lockup-homectl` (the wordmark, header), `homectl-in-frame` (the icon; also `favicon.svg`/`favicon-dark.svg`)
and `gradzero-mark-multi-merged` (the "by GradZero AI" footer). The script also makes the square, opaque icons:
`apple-touch-icon.png`, `favicon.ico`, `logo-120.png` (for app consoles such as Google's consent screen) and
`logo-512.png`.
