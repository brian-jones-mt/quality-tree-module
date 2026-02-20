# GEMINI.md

## Project Overview

This project is a training module on "Quality Trees," a process for defining and measuring software quality attributes. The target audience includes senior engineers, tech leads, and architects.

The repository contains Markdown files that are used to generate a series of static HTML slide decks. The generation process is handled by a Python script (`generate_slides.py`) that uses a Vue.js template for the slide presentation.

The main technologies used are:
-   **Python:** For the slide generation script.
-   **Markdown:** As the source format for the slide content.
-   **HTML/CSS/JavaScript (Vue.js):** For the generated slide decks.
-   **SASS:** For styling the slides.
-   **Mermaid:** for diagrams.
-   **uv:** For environment and package management.
-   **GitHub Actions:** For CI/CD to GitHub Pages.


Check and adhere to `agents.md` also

## Building and Running

### 1. Install Dependencies

This project uses `uv` for environment and package management. To install the required dependencies, run:

```bash
uv pip install .
```

The slide generation script also has dependencies on `sass` and `@mermaid-js/mermaid-cli` which can be installed via `npm`. The script will attempt to install these globally if they are not found.

### 2. Generate the Slides

To generate the HTML slide decks from the Markdown source files, run:

```bash
uv run python3 generate_slides.py
```

This command executes the `generate_slides.py` script, which will:
1.  Compile `styles/main.scss` to `styles/main.css`.
2.  Compile any `.mmd` or `.mermaid` files into PNG images.
3.  Copy all image assets to the `dist` directory.
4.  Find all `slides.md` files in the `docs/` directory.
5.  Generate an `index.html` file for each module in the `dist/` directory.
6.  Create a main `dist/index.html` file that links to all the modules.

### 3. Preview the Slides

After generating the slides, you can preview them by opening the `dist/index.html` file in your web browser:

```bash
open dist/index.html
```

## Development Conventions

-   **Content:** All slide content is written in Markdown files named `slides.md` located in subdirectories under `docs/`. Each subdirectory represents a module.
-   **Slides:** Individual slides within a `slides.md` file are separated by `---`.
-   **Styling:** The visual style of the slides is defined in `styles/main.scss`. Changes to this file will be compiled to `styles/main.css` during the build process.
-   **Templates:** The HTML structure of the slides is defined in a hardcoded Vue.js template within `generate_slides.py`.
-   **Diagrams:** Mermaid is used for diagrams. Files with `.mmd` or `.mermaid` extensions are automatically compiled to PNG images and placed in the output directory, maintaining their relative path.
-   **Deployment:** The project is automatically deployed to GitHub Pages on every push to the `main` branch, as configured in `.github/workflows/deploy.yml`.

To create a new module, you would:
1.  Create a new subdirectory in the `docs/` directory (e.g., `docs/Mod 6 - New Module/`).
2.  Create a `slides.md` file within that new directory.
3.  Add your slide content in Markdown, separating slides with `---`.
4.  Run `uv run python3 generate_slides.py` to generate the new slide deck.
