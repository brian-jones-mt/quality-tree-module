#!/usr/bin/env python3
"""Generate static Vue.js-based slide decks from slides.md files in docs directory."""
import json
import os
import shutil
import markdown
import subprocess
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
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{
        startOnLoad: true,
        querySelector: '.slide-content code.language-mermaid',
      }});
    </script>
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
    html = markdown.markdown(markdown_text, extensions=['extra', 'codehilite', 'sane_lists'])
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

def compile_sass():
    """Compile SCSS to CSS using the sass compiler. If sass is not found, attempt to install it."""
    try:
        # Check if sass is available
        subprocess.run(['sass', '--version'], check=True, capture_output=True)
    except FileNotFoundError:
        print("SASS compiler not found. Attempting to install 'sass' globally using npm...")
        try:
            subprocess.run(['npm', 'install', '-g', 'sass'], check=True)
            print("SASS installed successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to install SASS: {e}")
            print("Please ensure npm is installed and accessible in your PATH, or install sass manually (e.g., 'npm install -g sass').")
            raise SystemExit(1)
    except subprocess.CalledProcessError as e:
        print(f"SASS --version command failed: {e.stderr.decode().strip()}")
        raise SystemExit(1)

    try:
        subprocess.run(['sass', 'styles/main.scss', 'styles/main.css'], check=True)
        print("SASS compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling SASS: {e.stderr.decode().strip()}")
        raise SystemExit(1)

def _setup_output_directories(src_path: Path, out_path: Path, styles_path: Path):
    """
    Sets up output directories and copies static assets like styles.
    """
    if not src_path.exists():
        print(f"Source {src_path} not found.")
        raise SystemExit(1)

    out_path.mkdir(parents=True, exist_ok=True)

    out_styles = out_path / 'styles'
    if styles_path.exists():
        try:
            shutil.copytree(styles_path, out_styles, dirs_exist_ok=True)
        except Exception:
            # fallback: copy files individually
            out_styles.mkdir(parents=True, exist_ok=True)
            for p in styles_path.glob('*'):
                if p.is_file():
                    shutil.copy2(p, out_styles / p.name)
    return out_styles

def _compile_mermaid_diagrams(src_dir: Path, out_dir: Path):
    """
    Finds Mermaid files in src_dir, compiles them to SVG, and places them in out_dir.
    Attempts to install `@mermaid-js/mermaid-cli` globally if `mmdc` command is not found.
    """
    mermaid_extensions = ('.mmd', '.mermaid')

    # Check if mmdc is available
    try:
        subprocess.run(['mmdc', '--version'], check=True, capture_output=True)
    except FileNotFoundError:
        print("Mermaid CLI (mmdc) not found. Attempting to install '@mermaid-js/mermaid-cli' globally using npm...")
        try:
            subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'], check=True)
            print("Mermaid CLI installed successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to install Mermaid CLI: {e}")
            print("Please ensure npm is installed and accessible in your PATH, or install '@mermaid-js/mermaid-cli' manually (e.g., 'npm install -g @mermaid-js/mermaid-cli').")
            raise SystemExit(1)

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(mermaid_extensions):
                src_path = Path(root) / file
                relative_path = src_path.relative_to(src_dir)
                dest_file_name = file.rsplit('.', 1)[0] + '.svg'
                dest_path = out_dir / relative_path.parent / dest_file_name
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                command = [
                    'mmdc',
                    '-i', str(src_path),
                    '-o', str(dest_path)
]

                try:
                    subprocess.run(command, check=True)
                    print(f"Compiled Mermaid: {src_path} -> {dest_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error compiling Mermaid diagram {src_path}: {e}")
                    raise SystemExit(1)

                try:
                    subprocess.run(command, check=True)
                    print(f"Compiled Mermaid: {src_path} -> {dest_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error compiling Mermaid diagram {src_path}: {e}")
                    raise SystemExit(1)


def _compile_plantuml_diagrams(src_dir: Path, out_dir: Path):
    """
    Finds PlantUML files in src_dir, compiles them to SVG, and places them in out_dir.
    Supported extensions: .puml, .plantuml, .uml, .iuml
    Prefers the local `plantuml` CLI if available; falls back to Kroki cloud rendering otherwise.
    To force local JAR usage, set env var PLANTUML_JAR to a path to plantuml.jar.
    """
    import shutil as _shutil
    import urllib.request
    import urllib.error

    exts = ('.puml', '.plantuml', '.uml', '.iuml')

    def _have(cmd: str) -> bool:
        return _shutil.which(cmd) is not None

    plantuml_cli = None
    plantuml_jar = os.environ.get('PLANTUML_JAR')

    if plantuml_jar and Path(plantuml_jar).exists():
        plantuml_cli = ('java', '-jar', plantuml_jar)
    elif _have('plantuml'):
        plantuml_cli = ('plantuml',)

    for root, _, files in os.walk(src_dir):
        for file in files:
            if not file.lower().endswith(exts):
                continue
            src_path = Path(root) / file
            relative_path = src_path.relative_to(src_dir)
            dest_file_name = file.rsplit('.', 1)[0] + '.svg'
            dest_path = out_dir / relative_path.parent / dest_file_name
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            if plantuml_cli:
                # Use local PlantUML to render SVG directly to our destination
                try:
                    # Many plantuml CLIs support: -tsvg -pipe. We'll use -pipe to control output path.
                    proc = subprocess.run(
                        list(plantuml_cli) + ['-tsvg', '-pipe'],
                        check=True,
                        input=src_path.read_text(encoding='utf-8').encode('utf-8'),
                        capture_output=True
                    )
                    dest_path.write_bytes(proc.stdout)
                    print(f"Compiled PlantUML (local): {src_path} -> {dest_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error compiling PlantUML diagram {src_path} with local CLI: {e}")
                    raise SystemExit(1)
            else:
                # Fallback to Kroki cloud rendering
                try:
                    req = urllib.request.Request(
                        url='https://kroki.io/plantuml/svg',
                        data=src_path.read_text(encoding='utf-8').encode('utf-8'),
                        headers={'Content-Type': 'text/plain; charset=utf-8'},
                        method='POST'
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        svg = resp.read()
                        dest_path.write_bytes(svg)
                        print(f"Compiled PlantUML (kroki): {src_path} -> {dest_path}")
                except (urllib.error.URLError, urllib.error.HTTPError) as e:
                    print(f"Failed to render PlantUML via Kroki for {src_path}: {e}")
                    print("Consider installing PlantUML locally or setting PLANTUML_JAR.")
                    raise SystemExit(1)



def _build_all():
    # 1) Compile styles
    styles_src = ROOT / 'styles'
    compile_sass()

    # 2) Prepare output directories and copy styles
    out_styles = _setup_output_directories(SRC, OUTDIR, styles_src)

    # 3) Precompile diagrams (Mermaid + PlantUML) into OUTDIR mirror
    _compile_mermaid_diagrams(SRC, OUTDIR)
    _compile_plantuml_diagrams(SRC, OUTDIR)

    # 4) Generate slides for each module (each docs/*/slides.md)
    index_entries = []
    for module_dir in sorted(SRC.iterdir()):
        if not module_dir.is_dir():
            continue
        slides_md = module_dir / 'slides.md'
        if not slides_md.exists():
            # allow nested subfolders containing slides
            for sub in module_dir.rglob('slides.md'):
                rel = sub.relative_to(SRC).parent
                title = f"{rel}"
                _emit_module(slides_path=sub, module_rel_dir=rel, title=str(title))
                index_entries.append((str(rel), f"{OUTDIR}/{rel}/index.html"))
            continue
        rel = slides_md.parent.relative_to(SRC)
        title = f"{rel}"
        _emit_module(slides_path=slides_md, module_rel_dir=rel, title=str(title))
        index_entries.append((str(rel), f"{OUTDIR}/{rel}/index.html"))

    _emit_index(index_entries)


def _emit_module(slides_path: Path, module_rel_dir: Path, title: str):
    out_module_dir = OUTDIR / module_rel_dir
    out_module_dir.mkdir(parents=True, exist_ok=True)

    slides_text = slides_path.read_text(encoding='utf-8')
    html_slides, slides_json = generate_slides_html(title, slides_text)

    # Determine CSS path relative to module dir
    css_rel_path = Path('..') / 'styles' / 'main.css'
    html = VUE_TEMPLATE.format(title=title, slides_json=slides_json, css_path=str(css_rel_path))

    (out_module_dir / 'index.html').write_text(html, encoding='utf-8')


def _emit_index(entries):
    index_html = [
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <title>Quality Tree Slides</title>',
        f'  <link rel="stylesheet" href="styles/main.css">',
        '</head>',
        '<body>',
        '  <div class="index">',
        '    <h1>Quality Tree Module Slides</h1>',
        '    <ul>'
    ]
    for name, href in sorted(entries):
        rel = Path(href).relative_to(OUTDIR)
        index_html.append(f'      <li><a href="{rel}">{name}</a></li>')
    index_html += [
        '    </ul>',
        '  </div>',
        '</body>',
        '</html>'
    ]
    (OUTDIR / 'index.html').write_text('\n'.join(index_html), encoding='utf-8')


if __name__ == '__main__':
    _build_all()
