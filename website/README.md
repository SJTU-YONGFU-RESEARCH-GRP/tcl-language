# Lesson website

Static site built from `lessons/*/lesson_{en,zh}.md` with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Local

```bash
make site-install   # once
make site           # → website/site/
make site-serve     # http://127.0.0.1:8000
```

## Publish

Push to `main` triggers [.github/workflows/pages.yml](../.github/workflows/pages.yml).  
Live URL (after Pages is enabled): https://sjtu-yongfu-research-grp.github.io/tcl-language/

Generated files (`docs/`, `mkdocs.yml`, `site/`) are produced by `scripts/build_website.py` and are gitignored except `requirements.txt` and this README.
