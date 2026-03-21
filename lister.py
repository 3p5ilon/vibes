import json
import os

try:
    from PIL import Image
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("Run: pip install pillow pillow-heif")
    raise SystemExit

# scan all YEAR/ folders (any folder whose name is a 4-digit number)
data = {}
for entry in os.scandir("."):
    if not entry.is_dir() or not entry.name.isdigit():
        continue
    year, images = entry.name, []
    for file in sorted(os.listdir(year)):
        try:
            im = Image.open(f"{year}/{file}")
            # store as "YEAR/file.jpg" — no leading slash
            # root page uses this as-is, year pages prepend "../"
            images.append([f"{year}/{file}", [im.width, im.height]])
        except:
            continue  # skip .DS_Store, non-images
    if images:
        data[year] = images
        print(f"{year}: {len(images)} images")

if not data:
    print("No year folders found. Create a 2026/ folder and put images in it.")
    raise SystemExit

years = sorted(data.keys(), reverse=True)

# one flat JSON — each page fetches this and filters by year
json.dump([img for y in years for img in data[y]], open("images.json", "w"))


def year_href(current_year, y):
    if current_year == years[0]:
        return f"{y}/"          # root → 2025/
    return f"../" if y == years[0] else f"../{y}/"  # year page → back to root or sibling


def make_page(current_year, json_path, img_prefix):
    # img_prefix: "" for root page, "../" for year subpages
    nav_links = " ".join(
        f'<a href="{year_href(current_year, y)}">{y}</a>'
        for y in years if y != current_year
    )
    img_count = len(data[current_year])

    return f"""<!DOCTYPE html>
<html>
<head>
<title>{current_year} vibes</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📷</text></svg>">
</head>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box }}

  :root {{
    --bg: #111210;
    --text: #ddd8d0;
    --link: #3d3d3a;
    --link-hover: #a8a49c;
    --border: rgba(255,255,255,0.07);
    --fname-bg: rgba(20,20,18,0.70);
    --lb-bg: rgba(10,10,9,0.94);
    --lb-name: #555;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{
      --bg: #f2f0eb;
      --text: #111;
      --link: #bbb;
      --link-hover: #444;
      --border: rgba(0,0,0,0.09);
      --fname-bg: rgba(250,249,246,0.80);
      --lb-bg: rgba(235,233,228,0.96);
      --lb-name: #aaa;
    }}
  }}

  body {{ background: var(--bg); min-height: 100vh }}

  #header {{
    padding: 1.6rem 2rem 1.4rem;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    position: relative;
    z-index: 10;
  }}

  #left {{ display: flex; align-items: baseline; gap: 1.1rem; flex-wrap: wrap }}

  h1 {{
    font: italic normal 20px/1 Georgia, serif;
    color: var(--text);
    white-space: nowrap;
    letter-spacing: .01em;
  }}

  #nav {{ display: flex; gap: .8rem; align-items: baseline; flex-wrap: wrap }}

  #nav a {{
    font: italic normal 14px/1 Georgia, serif;
    color: var(--link);
    text-decoration: none;
    letter-spacing: .01em;
    transition: color .15s;
  }}
  #nav a:hover {{ color: var(--link-hover) }}

  #count {{
    font: italic normal 14px/1 Georgia, serif;
    color: var(--link);
    letter-spacing: .01em;
    white-space: nowrap;
  }}

  #container {{ position: relative; width: 100%; min-height: 100vh }}

  .w {{
    position: absolute; cursor: zoom-in;
    border-radius: 5px; overflow: hidden;
    border: 1px solid var(--border);
  }}
  .w img {{ display: block; transition: opacity .15s }}
  .w:hover img {{ opacity: .88 }}

  .w .n {{
    display: none; position: absolute;
    bottom: 0; left: 0; right: 0;
    background: rgba(0,0,0,.82); color: #f0f0f0;
    font: 10px/1.4 monospace; padding: 4px 6px;
    white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis; pointer-events: none;
  }}
  .w:hover .n {{ display: block }}

  #lb {{
    display: none; position: fixed; inset: 0;
    background: var(--lb-bg); z-index: 9999;
    align-items: center; justify-content: center; flex-direction: column;
  }}
  #lb.open {{ display: flex }}
  #lb img {{ max-width: 90vw; max-height: 85vh; object-fit: contain; cursor: zoom-out; border-radius: 4px }}
  #lb-n {{ color: var(--lb-name); font: 11px monospace; margin-top: 12px; letter-spacing: .05em }}
</style>

<div id="header">
  <div id="left">
    <h1>{current_year} vibes</h1>
    <div id="nav">{nav_links}</div>
  </div>
  <div id="count">{img_count} images</div>
</div>

<div id="container"></div>

<div id="lb" onclick="if(event.target===this||event.target.tagName==='IMG')closeLb()">
  <img id="lb-img" src="" alt="">
  <div id="lb-n"></div>
</div>

<script>
const C   = document.getElementById('container');
const lb  = document.getElementById('lb');
const lbi = document.getElementById('lb-img');
const lbn = document.getElementById('lb-n');
let imgs = [], idx = 0;

const openLb  = i => {{ idx=i; lbi.src=imgs[i].s; lbn.textContent=imgs[i].l; lb.classList.add('open') }};
const closeLb = ()  => lb.classList.remove('open');

document.addEventListener('keydown', e => {{
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape')     closeLb();
  if (e.key === 'ArrowRight') {{ idx=(idx+1)%imgs.length; lbi.src=imgs[idx].s; lbn.textContent=imgs[idx].l }}
  if (e.key === 'ArrowLeft')  {{ idx=(idx-1+imgs.length)%imgs.length; lbi.src=imgs[idx].s; lbn.textContent=imgs[idx].l }}
}});

function shuffle(a) {{
  for (let i=a.length-1; i>0; i--) {{
    const j = Math.floor(Math.random()*(i+1));
    [a[i],a[j]] = [a[j],a[i]];
  }}
  return a;
}}

const PREFIX = '{img_prefix}';  // "" for root, "../" for year subpages

fetch("{json_path}")
  .then(r => r.json())
  .then(all => {{
    // filter this year's images, prepend prefix so paths are relative to this page
    const kv = shuffle(
      all
        .filter(([p]) => p.startsWith('{current_year}/'))
        .map(([p, dims]) => [PREFIX + p, dims])
    );
    const sw = C.getBoundingClientRect().width;

    const pairs = kv.map(([k,[w,h]]) => {{
      const r = (w*h)/(500*300);
      return [
        Math.min(parseInt(r>16 ? w/8 : r>4 ? w/4 : w/2), sw-10),
        parseInt(r>16 ? h/8 : r>4 ? h/4 : h/2)
      ];
    }});

    let pos=[], i=0;

    const iv = setInterval(() => {{
      let H=600;
      const [w,h] = pairs[i];

      outer: while (true) {{
        for (let _=0; _<50; _++) {{
          const al=Math.random()*(sw-w), at=Math.random()*(H-h);
          let hit=false;
          for (let j=0; j<pos.length; j++) {{
            const [bl,bt]=pos[j];
            if (al<bl+pairs[j][0] && al+w>bl && at<bt+pairs[j][1] && at+h>bt) {{ hit=true; break }}
          }}
          if (!hit) {{ pos.push([parseInt(al),parseInt(at)]); break outer }}
        }}
        H += 50;
      }}

      const fp=kv[i][0], label=fp.split('/').pop(), ii=imgs.length;
      imgs.push({{s:fp, l:label}});

      const wrap = document.createElement('div');
      wrap.className = 'w';
      wrap.style.cssText = `top:${{pos[i][1]}}px;left:${{pos[i][0]}}px;width:${{pairs[i][0]}}px;height:${{pairs[i][1]}}px`;
      wrap.onclick = () => openLb(ii);

      const img = document.createElement('img');
      img.src=fp; img.loading='lazy';
      img.style.cssText = `width:${{pairs[i][0]}}px;height:${{pairs[i][1]}}px`;

      const n = document.createElement('div');
      n.className='n'; n.textContent=label;

      wrap.appendChild(img); wrap.appendChild(n); C.appendChild(wrap);
      i++; if (i===kv.length) clearInterval(iv);
    }}, 100);
  }});
</script>
</html>"""


# root index.html — images are at "2026/file.jpg" relative to root
open("index.html", "w").write(make_page(years[0], "images.json", img_prefix=""))
print(f"\nGenerated → index.html ({years[0]} vibes)")

# YEAR/index.html — images are at "../2025/file.jpg" relative to the year subfolder
for year in years[1:]:
    os.makedirs(year, exist_ok=True)
    open(f"{year}/index.html", "w").write(make_page(year, "../images.json", img_prefix="../"))
    print(f"Generated → {year}/index.html")

print("\nDone. Run: python3 -m http.server 8000")
