#!/usr/bin/env python3
"""Check the catalog and plugin files against the Claude Code and Codex formats.

Offline and standard library only. Run from anywhere:

    python3 scripts/validate.py            # structure checks
    python3 scripts/validate.py --links    # also check every https link answers

The Codex limits come from https://developers.openai.com/codex/plugins/build and
https://developers.openai.com/plugins/deploy/submission (read 23 Nov 2026).
Exit code 0 means every check passed.
"""
import json
import re
import struct
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
checked = 0

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".svg"}


def check(cond, msg):
    global checked
    checked += 1
    if not cond:
        errors.append(msg)
    return cond


def load(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        check(False, f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        check(False, f"bad JSON in {path.relative_to(ROOT)}: {e}")
    return None


def https(value, where, limit=2048):
    check(isinstance(value, str) and value.startswith("https://") and len(value) <= limit,
          f"{where}: must be an https URL of at most {limit} characters")


def text(value, where, limit, required=True):
    if value is None and not required:
        return
    check(isinstance(value, str) and value.strip() and len(value) <= limit,
          f"{where}: must be text of 1 to {limit} characters (got {len(value) if isinstance(value, str) else value!r})")


def rel_path(base, value, where):
    """A ./ path that stays inside base. Returns the resolved Path or None."""
    if not check(isinstance(value, str) and value.startswith("./"), f"{where}: path must start with ./"):
        return None
    p = (base / value).resolve()
    if not check(p == base.resolve() or base.resolve() in p.parents, f"{where}: path leaves {base.name}/"):
        return None
    check(p.exists(), f"{where}: {value} does not exist")
    return p


def image_size(p):
    data = p.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if p.suffix == ".svg":
        m = re.search(r'viewBox="[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', data.decode("utf-8", "ignore"))
        if m:
            return float(m.group(1)), float(m.group(2))
    return None


def check_image(plugin_dir, value, where):
    p = rel_path(plugin_dir, value, where)
    if not p or not p.exists():
        return
    check(p.suffix.lower() in IMAGE_EXT, f"{where}: must be PNG, JPEG, WebP or SVG")
    check(p.stat().st_size <= 5 * 1024 * 1024, f"{where}: larger than 5 MiB")
    size = image_size(p)
    if p.suffix.lower() in {".png", ".svg"}:
        if check(size is not None, f"{where}: could not read the image size"):
            w, h = size
            check(w == h, f"{where}: must be square (is {w}x{h})")
            check(w >= 48, f"{where}: must be at least 48x48 (is {w}x{h})")
            check(w <= 4096, f"{where}: must be at most 4096 px a side")


def frontmatter(path):
    t = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def check_skills(skills_dir, where):
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    check(skill_files, f"{where}: no skills/<name>/SKILL.md found")
    for sf in skill_files:
        w = f"{sf.relative_to(ROOT)}"
        fm = frontmatter(sf)
        if not check(fm is not None, f"{w}: needs YAML frontmatter between --- lines"):
            continue
        name = fm.get("name", "")
        check(NAME_RE.match(name) and len(name) <= 64, f"{w}: name must be lowercase-with-hyphens, at most 64")
        check(name == sf.parent.name, f"{w}: name '{name}' must match its folder '{sf.parent.name}'")
        text(fm.get("description"), f"{w}: description", 1024)
    return [sf.parent.name for sf in skill_files]


# ---- Claude Code ---------------------------------------------------------

def check_claude():
    mp = load(ROOT / ".claude-plugin/marketplace.json")
    if not mp:
        return {}
    w = ".claude-plugin/marketplace.json"
    check(NAME_RE.match(mp.get("name", "")), f"{w}: name must be lowercase-with-hyphens")
    text((mp.get("owner") or {}).get("name"), f"{w}: owner.name", 120)
    plugins = {}
    for i, entry in enumerate(mp.get("plugins") or []):
        pw = f"{w}: plugins[{i}]"
        d = rel_path(ROOT, entry.get("source"), f"{pw}.source")
        if not d:
            continue
        man = load(d / ".claude-plugin/plugin.json")
        if not man:
            continue
        mw = str((d / ".claude-plugin/plugin.json").relative_to(ROOT))
        check(man.get("name") == entry.get("name"), f"{mw}: name must match the catalog entry '{entry.get('name')}'")
        check(SEMVER_RE.match(man.get("version", "")), f"{mw}: version must be semver")
        text(man.get("description"), f"{mw}: description", 4000)
        plugins[man.get("name")] = (d, man)
    check(plugins, f"{w}: lists no plugins")
    return plugins


# ---- Codex ---------------------------------------------------------------

def check_codex():
    mp = load(ROOT / ".agents/plugins/marketplace.json")
    if not mp:
        return {}
    w = ".agents/plugins/marketplace.json"
    check(NAME_RE.match(mp.get("name", "")), f"{w}: name must be lowercase-with-hyphens")
    text((mp.get("interface") or {}).get("displayName"), f"{w}: interface.displayName", 80)
    plugins = {}
    for i, entry in enumerate(mp.get("plugins") or []):
        pw = f"{w}: plugins[{i}]"
        src = entry.get("source")
        if isinstance(src, dict):
            check(src.get("source") == "local", f"{pw}.source.source: this repo only uses local sources")
            src = src.get("path")
        d = rel_path(ROOT, src, f"{pw}.source")
        pol = entry.get("policy") or {}
        check(pol.get("installation") in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"},
              f"{pw}.policy.installation: must be AVAILABLE, INSTALLED_BY_DEFAULT or NOT_AVAILABLE")
        check(bool(pol.get("authentication")), f"{pw}.policy.authentication: required")
        check(bool(entry.get("category")), f"{pw}.category: required")
        if not d:
            continue
        mpath = d / ".codex-plugin/plugin.json"
        man = load(mpath)
        if not man:
            continue
        mw = str(mpath.relative_to(ROOT))
        check(man.get("name") == entry.get("name"), f"{mw}: name must match the catalog entry '{entry.get('name')}'")
        check(NAME_RE.match(man.get("name", "")) and len(man["name"]) <= 64, f"{mw}: name must be lowercase-with-hyphens, at most 64")
        check(SEMVER_RE.match(man.get("version", "")), f"{mw}: version must be semver")
        text(man.get("description"), f"{mw}: description", 4000)
        author = man.get("author") or {}
        text(author.get("name"), f"{mw}: author.name", 120)
        if "url" in author:
            https(author["url"], f"{mw}: author.url")
        if "homepage" in man:
            https(man["homepage"], f"{mw}: homepage")
        check("$schema" not in man, f"{mw}: leave out $schema in the .codex-plugin format")
        check("hooks" not in man and not (d / "hooks").exists(), f"{mw}: lifecycle hooks can't go to OpenAI's directory")
        check("apps" not in man and not (d / ".app.json").exists(), f"{mw}: apps can't go to OpenAI's directory")
        skills = rel_path(d, man.get("skills"), f"{mw}: skills")
        if skills and skills.exists():
            check_skills(skills, mw)
        ui = man.get("interface")
        if check(isinstance(ui, dict), f"{mw}: interface is required for Codex"):
            text(ui.get("displayName"), f"{mw}: interface.displayName", 30)
            text(ui.get("shortDescription"), f"{mw}: interface.shortDescription", 30)
            text(ui.get("longDescription"), f"{mw}: interface.longDescription", 4000)
            text(ui.get("developerName"), f"{mw}: interface.developerName", 80)
            text(ui.get("category"), f"{mw}: interface.category", 80)
            caps = ui.get("capabilities")
            check(isinstance(caps, list) and len(caps) <= 20 and all(isinstance(c, str) and len(c) <= 120 for c in caps),
                  f"{mw}: interface.capabilities must be a list of at most 20 items of at most 120 characters")
            prompts = ui.get("defaultPrompt", [])
            check(isinstance(prompts, list) and len(prompts) <= 3 and len(set(prompts)) == len(prompts)
                  and all(isinstance(p, str) and 0 < len(p) <= 128 and "@" not in p for p in prompts),
                  f"{mw}: interface.defaultPrompt must be up to 3 unique prompts of at most 128 characters, no @mentions")
            for k in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
                if k in ui:
                    https(ui[k], f"{mw}: interface.{k}", 1024)
            for k in ("brandColor", "brandColorDark"):
                if k in ui:
                    check(re.match(r"^#[0-9A-Fa-f]{6}$", ui[k] or ""), f"{mw}: interface.{k} must be #RRGGBB")
            for k in ("composerIcon", "logo"):
                check(k in ui, f"{mw}: interface.{k} is required for Codex")
            for k in ("composerIcon", "composerIconDark", "logo", "logoDark"):
                if k in ui:
                    check_image(d, ui[k], f"{mw}: interface.{k}")
        plugins[man.get("name")] = (d, man)
    check(plugins, f"{w}: lists no plugins")
    return plugins


def check_links():
    urls = set()
    for f in [ROOT / "README.md", *ROOT.glob("plugins/*/skills/*/SKILL.md")]:
        urls |= set(re.findall(r"https://[^\s)`'\"<>]+", f.read_text()))
    for u in sorted(urls):
        u = u.rstrip(".,")
        try:
            req = urllib.request.Request(u, method="GET", headers={"User-Agent": "catalex-plugins-validate"})
            code = urllib.request.urlopen(req, timeout=20).status
        except Exception as e:  # noqa: BLE001
            code = getattr(e, "code", str(e))
        check(code == 200, f"link {u} answered {code}")


def main():
    claude = check_claude()
    codex = check_codex()
    for name in set(claude) | set(codex):
        check(name in claude and name in codex, f"plugin '{name}' must be in both catalogs")
        if name in claude and name in codex:
            (cd, cm), (xd, xm) = claude[name], codex[name]
            check(cd == xd, f"plugin '{name}': both catalogs must point at the same folder")
            check(cm.get("version") == xm.get("version"),
                  f"plugin '{name}': Claude Code version {cm.get('version')} and Codex version {xm.get('version')} differ")
            names = check_skills(cd / "skills", name)
            print(f"plugin {name} {cm.get('version')}: skills {', '.join(names)}")
    if "--links" in sys.argv:
        check_links()
    for e in errors:
        print(f"FAIL {e}")
    print(f"{checked - len(errors)}/{checked} checks passed")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
