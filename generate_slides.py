#!/usr/bin/env python3
"""Generate a Reveal.js-based slide deck at docs/index.html from overview.md."""
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "overview.md"
OUTDIR = ROOT / "docs"
OUT = OUTDIR / "index.html"

TEMPLATE = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Tree — Intro</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/black.css" id="theme">
  </head>
  <body>
    <div class="reveal">
      <div class="slides">
        <section data-markdown>
          <textarea data-template>
{markdown}
          </textarea>
        </section>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/markdown/markdown.esm.js"></script>
    <script>
      const deck = new Reveal({
        plugins: [ RevealMarkdown ]
      });
      deck.initialize();
    </script>
  </body>
</html>
'''


def main():
    if not SRC.exists():
        print(f"Source {SRC} not found. Please create an overview.md in the repo root.")
        raise SystemExit(1)

    md = SRC.read_text(encoding='utf-8')

    # Ensure output dir
    OUTDIR.mkdir(parents=True, exist_ok=True)

    html = TEMPLATE.format(markdown=md)
    OUT.write_text(html, encoding='utf-8')
    print(f"Wrote {OUT}")


if __name__ == '__main__':
    main()
