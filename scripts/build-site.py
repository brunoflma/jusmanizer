"""Prepare the static Pages site and downloads from the canonical skill files."""
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
OUTPUT = ROOT / ".site-build"
PACKAGE_FILES = ("SKILL.md", "LICENSE", "scripts/jusmanizer.py")


def skill_metadata():
    source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    groups = []
    for line in source.splitlines():
        group = re.match(r"^## ([A-F])\. (.+)$", line)
        rule = re.match(r"^### (J\d{2}) (.+)$", line)
        if group:
            groups.append({"id": group[1], "name": group[2], "rules": []})
        elif rule:
            if not groups:
                raise ValueError("Rule found before a group")
            groups[-1]["rules"].append({"id": rule[1], "name": rule[2]})
    ids = [rule["id"] for group in groups for rule in group["rules"]]
    if ids != [f"J{i:02}" for i in range(1, 33)] or len(groups) != 6:
        raise ValueError("The website expects the canonical 32 rules in six groups")
    return {"ruleCount": len(ids), "groupCount": len(groups), "groups": groups}


def validate_examples(metadata):
    examples = json.loads((SITE / "assets/examples.json").read_text(encoding="utf-8"))
    known = {rule["id"] for group in metadata["groups"] for rule in group["rules"]}
    if len(examples) != 7 or len({item["id"] for item in examples}) != 7:
        raise ValueError("Expected seven distinct illustrative examples")
    for item in examples:
        for field in ("before", "after", "prompt", "title", "context"):
            if not item.get(field):
                raise ValueError(f"Missing {field} in {item['id']}")
        if not set(item["rules"]) <= known:
            raise ValueError(f"Unknown rule in {item['id']}")
        for fact in item["facts"]:
            if fact.casefold() not in item["before"].casefold() or fact.casefold() not in item["after"].casefold():
                raise ValueError(f"Protected fact changed in {item['id']}: {fact}")
        if item.get("kind") != "question":
            before_numbers = re.findall(r"\d+(?:[.,/:]\d+)*", item["before"])
            after_numbers = re.findall(r"\d+(?:[.,/:]\d+)*", item["after"])
            if sorted(before_numbers) != sorted(after_numbers):
                raise ValueError(f"Numbers changed in {item['id']}")
    return examples


def build():
    metadata = skill_metadata()
    validate_examples(metadata)
    if OUTPUT.resolve().parent != ROOT or OUTPUT.name != ".site-build":
        raise ValueError("Build output must stay inside the project")
    shutil.copytree(SITE, OUTPUT, dirs_exist_ok=True)
    (OUTPUT / "assets/rules.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    downloads = OUTPUT / "downloads"
    downloads.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "SKILL.md", downloads / "SKILL.md")
    with zipfile.ZipFile(downloads / "jusmanizer.zip", "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name in PACKAGE_FILES:
            package.write(ROOT / name, arcname=f"jusmanizer/{name}")
    (OUTPUT / ".nojekyll").touch()
    print("Site built: 7 examples, 32 rules, 6 groups, canonical ZIP and SKILL.md downloads.")


if __name__ == "__main__":
    build()
