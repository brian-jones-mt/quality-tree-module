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


import subprocess

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


def _process_module_slides(slides_file: Path, out_root_dir: Path, styles_output_dir: Path):
    """
    Processes a single slides.md file, generates its HTML, and writes it to the output directory.
    """
    rel_path = slides_file.relative_to(SRC)
    module_dir = slides_file.parent
    module_name = module_dir.name
    
    markdown_content = slides_file.read_text(encoding='utf-8')
    
    html_slides, slides_json = generate_slides_html(module_name, markdown_content)
    
    out_module_dir = out_root_dir / module_name
    out_module_dir.mkdir(parents=True, exist_ok=True)
    
    css_rel = os.path.relpath(styles_output_dir / 'main.css', start=out_module_dir)

    html_output = VUE_TEMPLATE.format(
      title=module_name,
      slides_json=slides_json,
      css_path=css_rel.replace('\\\\', '/')
    )
    
    out_file = out_module_dir / "index.html"
    out_file.write_text(html_output, encoding='utf-8')
    print(f"Generated {out_file}")



def _generate_index_page(overview_file: Path, slides_files: list[Path], out_root_dir: Path):
    """
    Generates the central index page from overview.md.
    """
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

        index_out = out_root_dir / 'index.html'
        index_out.write_text(INDEX_TEMPLATE, encoding='utf-8')
        print(f"Generated central index at {index_out}")
    else:
        print("No overview.md found; skipping central index generation.")


def _compile_mermaid_diagrams(src_dir: Path, out_dir: Path):
    """
    Finds Mermaid files in src_dir, compiles them to PNG, and places them in out_dir.
    """
    mermaid_extensions = ('.mmd', '.mermaid')
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(mermaid_extensions):
                src_path = Path(root) / file
                # Construct relative path from src_dir
                relative_path = src_path.relative_to(src_dir)
                # Change extension to .png
                dest_file_name = file.rsplit('.', 1)[0] + '.png'
                dest_path = out_dir / relative_path.parent / dest_file_name
                
                # Create parent directories if they don't exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                command = [
                    'npx', '-p', '@mermaid-js/mermaid-cli', 'mmdc',
                    '-i', str(src_path),
                    '-o', str(dest_path)
                ]
                print(f"Compiling Mermaid: {' '.join(command)}")
                try:
                    # Capture output to prevent printing to stdout by run_shell_command
                    result = subprocess.run(command, check=True, capture_output=True, text=True)
                    print(f"Successfully compiled {src_path} to {dest_path}")
                    if result.stdout:
                        print(f"Mermaid-cli stdout: {result.stdout}")
                    if result.stderr:
                        print(f"Mermaid-cli stderr: {result.stderr}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to compile {src_path}: {e}")
                    print(f"Mermaid-cli stdout: {e.stdout}")
                    print(f"Mermaid-cli stderr: {e.stderr}")
                    raise SystemExit(1)


def _copy_images_to_output(src_dir: Path, out_dir: Path):
    """
    Copies image files from the source directory to the output directory,
    maintaining the relative directory structure.
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                src_path = Path(root) / file
                # Construct relative path from src_dir
                relative_path = src_path.relative_to(src_dir)
                # Construct destination path in out_dir
                dest_path = out_dir / relative_path
                
                # Create parent directories if they don't exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(src_path, dest_path)
                print(f"Copied image: {src_path} to {dest_path}")


def main():
    compile_sass()
    
    out_styles = _setup_output_directories(SRC, OUTDIR, ROOT / 'styles')
    _compile_mermaid_diagrams(SRC, OUTDIR)
    _copy_images_to_output(SRC, OUTDIR)

    slides_files = list(SRC.glob('**/slides.md'))
    
    if not slides_files:
        print("No slides.md files found in docs directory.")
        raise SystemExit(1)

    for slides_file in sorted(slides_files):
        _process_module_slides(slides_file, OUTDIR, out_styles)

    _generate_index_page(SRC / 'overview.md', slides_files, OUTDIR)



if __name__ == '__main__':
    main()
