#!/usr/bin/env python3
"""Generate static Vue.js-based slide decks from slides.md files in docs directory."""
import json
import re
import os
import shutil
import markdown
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "docs"
OUTDIR = ROOT / "dist"

# Vue.js template for rendering slides
VUE_TEMPLATE = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
    <link rel="stylesheet" href="{css_path}">
  </head>
  <body>
    <div id="app">
      <div class="slide-container">
        <div class="slide-content" v-html="currentSlide"></div>
        <div class="slide-control">
          <button @click="previousSlide" :disabled="currentIndex === 0">← Previous</button>
          <span class="slide-number">{{{{ currentIndex + 1 }}}} / {{{{ slides.length }}}}</span>
          <button @click="nextSlide" :disabled="currentIndex === slides.length - 1">Next →</button>
        </div>
      </div>
      <div class="keyboard-hint">Use arrow keys to navigate</div>
    </div>

    <script>
      const {{ createApp }} = Vue;
      
      const slides = {slides_json};
      
      createApp({{
        data() {{
          return {{
            slides: slides,
            currentIndex: 0
          }};
        }},
        computed: {{
          currentSlide() {{
            return this.slides[this.currentIndex];
          }}
        }},
        methods: {{
          nextSlide() {{
            if (this.currentIndex < this.slides.length - 1) {{
              this.currentIndex++;
            }}
          }},
          previousSlide() {{
            if (this.currentIndex > 0) {{
              this.currentIndex--;
            }}
          }},
          handleKeydown(event) {{
            if (event.key === 'ArrowRight') {{
              this.nextSlide();
            }} else if (event.key === 'ArrowLeft') {{
              this.previousSlide();
            }}
          }}
        }},
        mounted() {{
          window.addEventListener('keydown', this.handleKeydown);
        }},
        unmounted() {{
          window.removeEventListener('keydown', this.handleKeydown);
        }}
      }}).mount('#app');
    </script>
  </body>
</html>
'''


def parse_markdown_to_html(markdown_text):
    """Convert markdown text to HTML using the markdown library."""
    html = markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])
    return html


def extract_slides(markdown_text):
    """Split markdown text by --- to extract individual slides."""
    slides = markdown_text.split('---')
    return [slide.strip() for slide in slides if slide.strip()]


def generate_slides_html(title, slides_text):
    """Convert slides markdown to HTML format."""
    raw_slides = extract_slides(slides_text)
    html_slides = [parse_markdown_to_html(slide) for slide in raw_slides]
    return html_slides, json.dumps(html_slides)


def main():
    if not SRC.exists():
        print(f"Source {SRC} not found.")
        raise SystemExit(1)

    OUTDIR.mkdir(parents=True, exist_ok=True)

    # Copy styles into output so pages can reference a ready-made stylesheet
    src_styles = ROOT / 'styles'
    out_styles = OUTDIR / 'styles'
    if src_styles.exists():
        try:
            shutil.copytree(src_styles, out_styles, dirs_exist_ok=True)
        except Exception:
            # fallback: copy files individually
            out_styles.mkdir(parents=True, exist_ok=True)
            for p in src_styles.glob('*'):
                if p.is_file():
                    shutil.copy2(p, out_styles / p.name)

    # Find all slides.md files
    slides_files = list(SRC.glob('**/slides.md'))
    
    if not slides_files:
        print("No slides.md files found in docs directory.")
        raise SystemExit(1)

    for slides_file in sorted(slides_files):
        # Get relative path and module folder
        rel_path = slides_file.relative_to(SRC)
        module_dir = slides_file.parent
        module_name = module_dir.name
        
        # Read slides
        markdown_content = slides_file.read_text(encoding='utf-8')
        
        # Parse and convert to HTML
        html_slides, slides_json = generate_slides_html(module_name, markdown_content)
        
        # Create output directory
        out_module_dir = OUTDIR / module_name
        out_module_dir.mkdir(parents=True, exist_ok=True)
        
        # Compute CSS path relative to this module output directory
        css_rel = os.path.relpath(out_styles / 'main.css', start=out_module_dir)

        # Generate HTML file
        html_output = VUE_TEMPLATE.format(
          title=module_name,
          slides_json=slides_json,
          css_path=css_rel.replace('\\\\', '/')
        )
        
        out_file = out_module_dir / "index.html"
        out_file.write_text(html_output, encoding='utf-8')
        print(f"Generated {out_file}")

    # Generate central index page from overview.md
    overview_file = SRC / 'overview.md'
    if overview_file.exists():
        overview_md = overview_file.read_text(encoding='utf-8')
        overview_html = parse_markdown_to_html(overview_md)

        # Build module links from generated module dirs
        module_links = []
        for slides_file in sorted(slides_files):
            module_dir = slides_file.parent
            module_name = module_dir.name
            # link to module_name/index.html (URL-encode spaces)
            href = f"{module_name.replace(' ', '%20')}/index.html"
            module_links.append(f'<li><a href="{href}">{module_name}</a></li>')

        links_html = '<ul>\n' + '\n'.join(module_links) + '\n</ul>' if module_links else ''

        INDEX_TEMPLATE = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Tree — Overview</title>
    <link rel="stylesheet" href="styles/main.css">
  </head>
  <body>
    <div id="app">
      <div class="slide-container">
        <main style="padding:40px; max-width:980px; margin:auto;">
          {overview_html}
          <h2 style="margin-top:24px;">Modules</h2>
          {links_html}
        </main>
      </div>
    </div>
  </body>
</html>
'''

        index_out = OUTDIR / 'index.html'
        index_out.write_text(INDEX_TEMPLATE, encoding='utf-8')
        print(f"Generated central index at {index_out}")
    else:
        print("No overview.md found; skipping central index generation.")


if __name__ == '__main__':
    main()
