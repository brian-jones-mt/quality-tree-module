# Quality Tree Training

This repository contains a reusable training package to aid understanding of the quality tree process. The target audience is senior and lead engineers, Tech Leads, and aspiring architects.

The output of this is a series of slide decks and resources for use in training, generated from Markdown files in the `docs` directory.

How to generate and preview the slide decks
-----------------------------------------

### 1. Install Dependencies

This project uses `uv` for environment and package management. Install the required dependencies:

```bash
uv pip install -r requirements.txt
```
*(Note: If `requirements.txt` does not exist, you may need to install them manually: `uv pip install markdown python-markdown-math Pygments`)*

### 2. Generate the Slides

Generate the HTML slide decks from the `slides.md` files in the `docs` directory:

```bash
uv run python3 generate_slides.py
```

This will create a `dist` directory containing the generated HTML files, organized by module.

### 3. Preview the Slides

Open the main index file to see the list of modules:

```bash
open dist/index.html
```

Or open a specific module directly:

```bash
open "dist/Mod 1 - Anatomy of Quality/index.html"
```

Notes:
- The repository is configured with a GitHub Actions workflow `.github/workflows/deploy.yml` that runs `generate_slides.py` on push and deploys the `dist/` folder to GitHub Pages.
- The slides are built using a Vue.js template in `generate_slides.py`. You can edit the template there to change the layout or style of the slides.