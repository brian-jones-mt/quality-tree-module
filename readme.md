# Quality Tree Training

This repository contains a reusable training package to aid understanding of the quality tree process.  The Target audience is senior and lead engineers, Tech Leads, and aspiring architects.

The output of this is a series of slide decks and resources for use in training.

How to generate and preview the slide deck
----------------------------------------

- Generate the HTML slide deck from the `overview.md` source:

```bash
python3 generate_slides.py
```

- Open the generated slides locally:

```bash
open docs/index.html
```

Notes:
- The repository is configured with a GitHub Actions workflow `.github/workflows/deploy.yml` that runs `generate_slides.py` on push and deploys the `docs/` folder to GitHub Pages.
- If you want a different theme, edit `docs/index.html` or update `generate_slides.py` template to change the Reveal.js theme.