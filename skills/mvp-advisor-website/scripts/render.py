"""Render neutral MVP GHL snippets without external writes or dependencies."""
import argparse
import csv
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

TOKEN = re.compile(r"\{\{custom_values\.([a-z0-9_]+)\}\}")


def normalize_css(code):
    css = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", code, re.S | re.I))
    css = re.sub(r"#[0-9a-fA-F]{3,8}\b", "COLOR", css)
    return re.sub(r"\d+\s*,\s*\d+\s*,\s*\d+(?=\s*,)", "RGB", css)


def render(values_path, output, include_legacy=False):
    data = json.loads(Path(values_path).read_text(encoding="utf-8-sig"))
    values = dict(data.get("values", {}))
    if not isinstance(values.get("advisor_name"), str) or not values["advisor_name"].strip():
        raise ValueError("values.advisor_name is required")
    for key, value in values.items():
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value:
            continue
        if key.startswith("theme_"):
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
                raise ValueError(f"{key} must be a six-digit hex color")
        elif key.startswith("webprez_"):
            url = urlparse(value)
            if url.scheme != "https" or url.hostname != "smartmoney.talk":
                raise ValueError(f"{key} requires the collected HTTPS WebPrez viewing link")
        elif key.startswith("video_") and not key.endswith("_thumbnail"):
            url = urlparse(value)
            if url.scheme != "https" or url.hostname != "player.vimeo.com" or "/rendition/720p/" not in url.path or "signature=" not in url.query:
                raise ValueError(f"{key} requires the exact signed Vimeo 720p file URL")
        elif key.endswith("_url") or key.endswith("_thumbnail"):
            if urlparse(value).scheme != "https":
                raise ValueError(f"{key} requires a public HTTPS URL")
    bios = {}
    for role, key in (("home", "advisor_home_bio_html"), ("about", "advisor_about_bio_html")):
        paragraphs = data.get("bios", {}).get(role, [])
        if not isinstance(paragraphs, list) or any(not isinstance(p, str) for p in paragraphs):
            raise ValueError(f"bios.{role} must be a paragraph array")
        if paragraphs:
            bios[key] = "\n\n".join("<p>" + html.escape(p) + "</p>" for p in paragraphs)
    if any(key.endswith("_html") for key in values):
        raise ValueError("Use bios paragraph arrays instead of raw HTML values")
    folder = Path(__file__).resolve().parents[1] / "assets" / "template"
    output = Path(output).resolve()
    if output == folder.resolve() or folder.resolve() in output.parents:
        raise ValueError("Output must be outside installed template assets")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Use a new/empty output directory to preserve existing work")
    output.mkdir(parents=True, exist_ok=True)
    sections, checks, missing = [], [], set()
    primary = values.get("theme_primary") or "#8e9897"
    hover = values.get("theme_hover") or "#a3adac"
    light = values.get("theme_light") or "#d4dcdb"
    rgb = ",".join(str(int(primary[i:i+2], 16)) for i in (1, 3, 5))
    for number in range(1, 10 if include_legacy else 9):
        source_name = f"section-{number:02d}.html" if number < 9 else "legacy-optional.html"
        original = (folder / source_name).read_text(encoding="utf-8-sig")

        def replace(match):
            key = match[1]
            if key in bios:
                return bios[key]
            value = values.get(key)
            if value:
                return html.escape(value, quote=True)
            missing.add(key)
            return match[0]

        code = TOKEN.sub(replace, original)
        # Apply branding inside style blocks only; preserve all URLs and prose.
        def theme(match):
            css = match[0].replace("#8e9897", primary).replace("#a3adac", hover).replace("#d4dcdb", light)
            return css.replace("142,152,151,", rgb + ",")
        code = re.sub(r"<style\b[^>]*>.*?</style>", theme, code, flags=re.S | re.I)
        scripts = lambda text: re.findall(r"<script\b[^>]*>.*?</script>", text, re.S | re.I)
        if normalize_css(original) != normalize_css(code) or scripts(original) != scripts(code):
            raise ValueError(f"Layout or script changed in {source_name}")
        (output / f"section-{number:02d}.html").write_text(code, encoding="utf-8")
        sections.append(code)
        checks.append({"section": number, "cssGeometryPreserved": True, "scriptsPreserved": True})
    combined = "\n\n".join(sections)
    (output / "all-sections.html").write_text(combined, encoding="utf-8")
    preview = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + html.escape(values["advisor_name"]) + '</title><style>body{margin:0}</style></head><body>' + combined + '</body></html>'
    (output / "preview.html").write_text(preview, encoding="utf-8")
    with (output / "missing-values.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["key", "status"])
        writer.writerows((key, "needs_source_value") for key in sorted(missing))
    report = {"advisor": values["advisor_name"], "sourceChecks": checks, "missing": sorted(missing), "renderedVerified": False, "playbackVerified": False, "published": False}
    (output / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (output / "source-manifest.json").write_text(json.dumps(data.get("sources", {}), indent=2), encoding="utf-8")
    print(f"Rendered {len(sections)} sections; {len(missing)} unresolved values. Output: {output}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--values", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--include-legacy", action="store_true")
    args = parser.parse_args()
    render(args.values, args.output, args.include_legacy)
