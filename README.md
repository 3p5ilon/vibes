# vibes

A personal image moodboard — scattered images, organized by year.

Inspired by [Guzey](https://guzey.com/vibes/) and [Sophia](https://girl.surgery/website_vibes/). Based on the approach from [sophiawisdom's gist](https://gist.github.com/sophiawisdom/c1b16fcaca017d1aec2358c6fb619697).

## Structure

```
vibes/
├── index.html       — home page
├── lister.py        — run whenever you add images
├── images.json      — auto-generated, do not edit
├── 2025/            — images go directly in year folders
└── 2024/
```

`lister.py` scans all `YYYY/` folders, URL-encodes filenames, and writes `images.json`. `index.html` reads it on load and renders the scattered layout client-side. adding a new year (e.g. `2027/`) automatically makes it the default.

## Setup

requires python 3!

```bash
python3 -m venv venv
source venv/bin/activate
pip install pillow pillow-heif
deactivate
```

### Adding images

drop images into the correct year folder, then regenerate `images.json`:

```bash
source venv/bin/activate
python3 lister.py  # regenerates images.json
deactivate

python3 -m http.server 8000  # preview at localhost:8000
```

## License

MIT
