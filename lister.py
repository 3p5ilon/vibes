import json
import os
from urllib.parse import quote

try:
    from PIL import Image
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    print("Run: pip install pillow pillow-heif")
    raise SystemExit

data = {}
for entry in os.scandir("."):
    if not entry.is_dir() or not entry.name.isdigit():
        continue
    year, images = entry.name, []
    for file in sorted(os.listdir(year)):
        try:
            im = Image.open(f"{year}/{file}")
            images.append([f"{year}/{quote(file)}", [im.width, im.height]])
        except:
            continue  # skip .DS_Store, non-images
    if images:
        data[year] = images
        print(f"{year}: {len(images)} images")

if not data:
    print("No year folders found. Create a 20YY/ folder and put images in it.")
    raise SystemExit

years = sorted(data.keys(), reverse=True)

out = {"years": years, "images": [img for y in years for img in data[y]]}
with open("images.json", "w") as f:
    f.write("{\n")
    f.write(f'  "years": {json.dumps(years)},\n')
    f.write('  "images": [\n')
    images = out["images"]
    for i, img in enumerate(images):
        comma = "," if i < len(images) - 1 else ""
        f.write(f"    {json.dumps(img)}{comma}\n")
    f.write("  ]\n}")


print(f"\nDone. Years: {years}")
print("Run: python3 -m http.server 8000")
