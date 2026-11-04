#!/usr/bin/env bash
# Rebuild the paper's figures and its three builds from paper/main.md and paper/refs.bib:
#
#   figures/fig*.svg            from results/ (paper/figures/make_figures.py, standard library only;
#                               every plotted number is parsed and asserted against main.md)
#   build/figures/fig*.pdf|png  the SVGs rendered by headless Chrome (pdflatex cannot read SVG)
#   build/main.tex              standalone LaTeX for arXiv (pdflatex), bibliography rendered inline
#                               by citeproc, so no BibTeX run; upload with build/figures/*.pdf
#   build/main.html             standalone HTML, figures and CSS embedded
#   build/main.pdf              main.html printed by headless Chrome
#
# Needs python3, pandoc >= 3 (citeproc built in) and Google Chrome or Chromium for the figure
# PDFs/PNGs and main.pdf (set CHROME=/path/to/chrome to choose one). No LaTeX is needed or run.
# Usage: paper/build.sh   (from any directory)

set -euo pipefail
cd "$(dirname "$0")"
PAPER_DIR=$(pwd)
OUT="$PAPER_DIR/build"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/paper-build.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT/figures"

say() { printf '%s\n' "$*"; }
die() { printf 'build.sh: %s\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null || die "python3 not found"
command -v pandoc >/dev/null || die "pandoc not found"
pandoc_major=$(pandoc --version | sed -n '1s/^pandoc[^0-9]*\([0-9]*\).*/\1/p')
[ "${pandoc_major:-0}" -ge 3 ] || die "pandoc >= 3 required (found $(pandoc --version | head -1))"

find_chrome() {
  if [ -n "${CHROME:-}" ] && [ -x "$CHROME" ]; then printf '%s' "$CHROME"; return; fi
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    [ -x "$c" ] && { printf '%s' "$c"; return; }
  done
  for c in google-chrome google-chrome-stable chromium chromium-browser; do
    command -v "$c" >/dev/null && { command -v "$c"; return; }
  done
}
CHROME_BIN=$(find_chrome || true)
# A throwaway profile, so the user's own Chrome session is never touched.
CHROME_FLAGS=(--headless --disable-gpu --no-first-run --no-default-browser-check --disable-extensions
              --hide-scrollbars --user-data-dir="$TMP/chrome-profile")
chrome() { "$CHROME_BIN" "${CHROME_FLAGS[@]}" "$@" >"$TMP/chrome.log" 2>&1; }

# 1. Figures (SVG) from the result files.
say "== figures"
python3 figures/make_figures.py

# 2. SVG -> PDF (vector, for pdflatex) and PNG (2x raster fallback) with headless Chrome.
if [ -n "$CHROME_BIN" ]; then
  for svg in figures/fig*.svg; do
    name=$(basename "$svg" .svg)
    vb=$(sed -n 's/.*viewBox="0 0 \([0-9.]*\) \([0-9.]*\)".*/\1 \2/p' "$svg" | head -1)
    w=${vb% *}; h=${vb#* }
    [ -n "$w" ] && [ -n "$h" ] || die "$svg: no viewBox"
    page="$TMP/$name.html"
    {
      printf '<!doctype html><html><head><meta charset="utf-8"><style>'
      printf '@page{size:%spx %spx;margin:0}html,body{margin:0;padding:0;background:#fff;overflow:hidden}' "$w" "$h"
      printf 'svg{display:block;width:%spx;height:%spx}</style></head><body>' "$w" "$h"
      cat "$svg"
      printf '</body></html>\n'
    } > "$page"
    chrome --no-pdf-header-footer --print-to-pdf="$TMP/$name.pdf" "file://$page"
    chrome --force-device-scale-factor=2 --window-size="${w%.*},${h%.*}" --screenshot="$TMP/$name.png" "file://$page"
    pages=$(LC_ALL=C grep -a -o '/Count [0-9]*' "$TMP/$name.pdf" | head -1 | tr -dc '0-9' || true)
    [ "$pages" = "1" ] || die "$name.pdf has ${pages:-no} page count, expected 1"
    mv "$TMP/$name.pdf" "$OUT/figures/$name.pdf"
    mv "$TMP/$name.png" "$OUT/figures/$name.png"
  done
else
  say "WARNING: Google Chrome/Chromium not found: build/figures/*.pdf|png and build/main.pdf not built"
fi

# 3. Pandoc filter: structured author entries (name, affiliation, note) become one line per
#    author; for LaTeX the figure sources switch from .svg to the Chrome-rendered .pdf.
cat > "$TMP/paper.lua" <<'LUA'
local function inlines(v) return pandoc.Inlines(v) end
local function latex_of(ils)
  return (pandoc.write(pandoc.Pandoc({pandoc.Plain(ils)}), 'latex'):gsub('%s+$', ''))
end
function Meta(meta)
  if not meta.author then return nil end
  local list = pandoc.List()
  for _, a in ipairs(meta.author) do
    if pandoc.utils.type(a) == 'table' and a.name then
      local out = pandoc.Inlines(inlines(a.name))
      local extra = pandoc.List()
      if a.affiliation then extra:insert(inlines(a.affiliation)) end
      if a.note then extra:insert(inlines(a.note)) end
      if FORMAT:match('latex') then
        local parts = {}
        for _, e in ipairs(extra) do table.insert(parts, latex_of(e)) end
        if #parts > 0 then
          out:insert(pandoc.RawInline('latex', '\\thanks{' .. table.concat(parts, '. ') .. '}'))
        end
      else
        for i, e in ipairs(extra) do
          out:insert(pandoc.LineBreak())
          out:insert(pandoc.Span(e, {class = (i == 1 and a.affiliation) and 'affiliation' or 'author-note'}))
        end
      end
      list:insert(pandoc.MetaInlines(out))
    else
      list:insert(a)
    end
  end
  meta.author = list
  return meta
end
function Image(img)
  if FORMAT:match('latex') and img.src:match('%.svg$') then
    img.src = img.src:gsub('%.svg$', '.pdf')
    return img
  end
end
LUA

# LaTeX preamble additions: tolerate graphicx versions without the `alt` key; tidy floats.
cat > "$TMP/header.tex" <<'TEX'
\makeatletter
\@ifundefined{KV@Gin@alt}{\define@key{Gin}{alt}{}}{}
\makeatother
\renewcommand{\topfraction}{0.9}
\renewcommand{\textfraction}{0.1}
\renewcommand{\floatpagefraction}{0.8}
TEX

check_pandoc_log() {
  if grep -q '\[WARNING\]' "$1"; then cat "$1" >&2; die "pandoc warnings in $2 (see above)"; fi
}

# 4. arXiv LaTeX.
say "== build/main.tex"
pandoc main.md --citeproc --lua-filter="$TMP/paper.lua" --standalone --to=latex \
  --include-in-header="$TMP/header.tex" \
  -V documentclass=article -V fontsize=11pt -V geometry:margin=1in -V colorlinks=true \
  -o "$TMP/body.tex" 2>"$TMP/pandoc-tex.log" || { cat "$TMP/pandoc-tex.log" >&2; die "pandoc failed (main.tex)"; }
check_pandoc_log "$TMP/pandoc-tex.log" main.tex
# arXiv: \pdfoutput=1 in the first lines selects pdflatex for PDF figures.
{ printf '\\pdfoutput=1\n'; cat "$TMP/body.tex"; } > "$TMP/main.tex"
mv "$TMP/main.tex" "$OUT/main.tex"

# 5. Standalone HTML.
say "== build/main.html"
cat > "$TMP/paper.css" <<'CSS'
:root { --ink: #1d1d1b; --muted: #5c5c58; --rule: #dcdcd6; --accent: #0b5cad; --tint: #f5f5f2; }
html { font-size: 17px; }
body {
  max-width: 44rem; margin: 2.5rem auto 4rem; padding: 0 1.25rem; color: var(--ink); background: #fff;
  font-family: Charter, "Bitstream Charter", "Iowan Old Style", Georgia, Cambria, "Times New Roman", serif;
  line-height: 1.55; hyphens: auto; -webkit-hyphens: auto; text-rendering: optimizeLegibility;
  font-kerning: normal;
}
h1, h2, h3, .title, .author, .date, .abstract-title, table, figcaption {
  font-family: "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif;
}
header#title-block-header { margin: 0 0 2rem; }
h1.title { font-size: 1.55rem; line-height: 1.25; font-weight: 650; margin: 0 0 1rem; border: 0; padding: 0; }
p.author { margin: 0.2rem 0; font-size: 0.98rem; font-weight: 600; }
p.author .affiliation, p.author .author-note { font-weight: 400; color: var(--muted); font-size: 0.9rem; }
p.date { margin: 0.3rem 0 0; color: var(--muted); font-size: 0.9rem; }
.abstract { margin: 1.6rem 0 0; padding: 1rem 1.25rem; background: var(--tint); border-left: 3px solid var(--rule);
  font-size: 0.93rem; }
.abstract-title { font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted);
  font-weight: 600; margin-bottom: 0.4rem; text-align: left; }
h1 { font-size: 1.3rem; line-height: 1.3; margin: 2.6rem 0 0.8rem; padding-top: 0.5rem; border-top: 1px solid var(--rule); }
h2 { font-size: 1.07rem; line-height: 1.3; margin: 1.9rem 0 0.6rem; }
p { margin: 0 0 0.9rem; }
ul, ol { padding-left: 1.3rem; } li { margin-bottom: 0.45rem; }
a { color: var(--accent); text-decoration: none; } a:hover { text-decoration: underline; }
code { font-family: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 0.82em;
  background: var(--tint); padding: 0.02em 0.1em; border-radius: 2px; overflow-wrap: anywhere; }
table { border-collapse: collapse; width: 100%; margin: 1.2rem 0 1.4rem; font-size: 0.72rem; line-height: 1.35;
  font-variant-numeric: tabular-nums; }
th, td { padding: 0.3rem 0.4rem; border-bottom: 1px solid #e4e4df; vertical-align: top; text-align: left; }
thead th { border-bottom: 1.5px solid #8a8a85; font-weight: 600; }
figure { margin: 2rem 0; counter-increment: figure; }
figure img, figure svg { display: block; width: 100%; max-width: 600px; height: auto; margin: 0 auto; }
figcaption { font-size: 0.84rem; line-height: 1.45; color: #3b3b38; margin: 0.7rem auto 0; max-width: 600px; }
figcaption::before { content: "Figure " counter(figure) ". "; font-weight: 600; color: var(--ink); }
#refs { font-size: 0.86rem; }
.csl-entry { margin-bottom: 0.55rem; padding-left: 1.5em; text-indent: -1.5em; overflow-wrap: anywhere; }
@media screen and (max-width: 720px) { table { display: block; overflow-x: auto; } }
@page { size: A4; margin: 17mm 16mm 19mm;
  @bottom-center { content: counter(page); font: 9pt "Helvetica Neue", Helvetica, Arial, sans-serif; color: #777; } }
@media print {
  html { font-size: 10.5pt; }
  body { max-width: none; margin: 0; padding: 0; }
  h1, h2 { break-after: avoid; }
  figure, tr, .abstract { break-inside: avoid; }
  table { font-size: 7.4pt; }
  figure img, figure svg { max-width: 15.5cm; }
  a { color: inherit; }
}
CSS
pandoc main.md --citeproc --lua-filter="$TMP/paper.lua" --standalone --to=html5 --embed-resources \
  --css="$TMP/paper.css" -M lang=en -o "$TMP/main.html" 2>"$TMP/pandoc-html.log" \
  || { cat "$TMP/pandoc-html.log" >&2; die "pandoc failed (main.html)"; }
check_pandoc_log "$TMP/pandoc-html.log" main.html
mv "$TMP/main.html" "$OUT/main.html"

# 6. PDF from the HTML.
if [ -n "$CHROME_BIN" ]; then
  say "== build/main.pdf"
  chrome --no-pdf-header-footer --print-to-pdf="$TMP/main.pdf" "file://$OUT/main.html"
  [ -s "$TMP/main.pdf" ] || { cat "$TMP/chrome.log" >&2; die "Chrome produced no main.pdf"; }
  mv "$TMP/main.pdf" "$OUT/main.pdf"
fi

# 7. Checks on the outputs.
say "== checks"
python3 - "$OUT" <<'PY'
import re, sys
from pathlib import Path
out = Path(sys.argv[1])
html = (out / "main.html").read_text(encoding="utf-8")
tex = (out / "main.tex").read_text(encoding="utf-8")
problems = []
# Exactly one [CHECK] marker, the known PSD3/PSR item.
tex_plain = tex.replace("{[}", "[").replace("{]}", "]").replace("\\ ", " ")
for name, text in (("main.html", html), ("main.tex", tex_plain)):
    marks = re.findall(r"\[CHECK[^\]]*\]", text)
    if len(marks) != 1 or "PSD3/PSR" not in marks[0]:
        problems.append(f"{name}: [CHECK] markers {marks}")
# Three figures, each with a caption and an id that the text links to.
figs = re.findall(r'<figure id="(fig:[a-z]+)"', html)
if figs != ["fig:evidence", "fig:gate", "fig:tradeoff"]:
    problems.append(f"main.html figures {figs}")
if len(re.findall(r"<figcaption", html)) != 3:
    problems.append("main.html: expected 3 figcaptions")
for f in figs:
    if f'href="#{f}"' not in html:
        problems.append(f"main.html: no link to {f}")
    if f"\\label{{{f}}}" not in tex or f"\\hyperref[{f}]" not in tex:
        problems.append(f"main.tex: label or reference for {f} missing")
for g in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", tex):
    if not g.endswith(".pdf") or not (out / g).is_file():
        problems.append(f"main.tex: graphic {g} missing or not PDF")
# Every internal link resolves; every citation rendered (no '???' or bare @keys).
ids = set(re.findall(r'\bid="([^"]+)"', html))
for h in sorted(set(re.findall(r'href="#([^"]+)"', html))):
    if h not in ids:
        problems.append(f"main.html: dangling link #{h}")
cites = set(re.findall(r'href="#ref-([^"]+)"', html))
entries = set(re.findall(r'id="ref-([^"]+)"', html))
if not cites or cites - entries:
    problems.append(f"main.html: citations without entry {sorted(cites - entries)}")
if re.search(r"\?\?\?|\(@\w|\[@\w", html):
    problems.append("main.html: unresolved citation text")
links = set(re.findall(r'href="#([^"]+)"', html))
print(f"figures {len(figs)}, internal links {len(links)}, "
      f"references {len(entries)} (all cited entries present), [CHECK] markers 1 (PSD3/PSR)")
if problems:
    print("\n".join(problems), file=sys.stderr)
    sys.exit(1)
PY

# Body words (Sections 1 to 7, figure captions excluded), the paper's 9,000-word limit.
words=$(awk '/^# 1\. Introduction/{f=1} /^# Appendix A\./{f=0} f' main.md | grep -v '^!\[' | wc -w | tr -d ' ')
say "body words (Sections 1-7, captions excluded): $words"
[ "$words" -le 9000 ] || die "body is $words words, over 9,000"

say "== outputs"
( cd "$OUT" && ls -l main.tex main.html main.pdf figures/* 2>/dev/null | awk '{printf "%10s  %s\n", $5, $NF}' )
[ -n "$CHROME_BIN" ] || say "NOTE: Chrome not found; figure PDFs/PNGs and main.pdf were not built."
