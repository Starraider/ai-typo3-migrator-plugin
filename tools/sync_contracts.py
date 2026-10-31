#!/usr/bin/env python3
"""Copy the handoff contract authoring source into each distributed skill.

  python3 tools/sync_contracts.py          copy files
  python3 tools/sync_contracts.py --check  fail (exit 1) when any copy differs

Skill layout produced:
  references/handoff-contract.md
  references/schemas/*.json
  scripts/validate_handoff.py
  templates/*.json
Skills carry independent copies so each installs standalone; there are no runtime
references into sibling skill directories.
"""
import argparse
import os
import shutil
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "docs", "contracts", "handoff-v1")
SKILLS = ["typo3-design-system-extract", "typo3-component-analyze", "typo3-component-build"]


def mapping():
    pairs = [("handoff-contract.md", "references/handoff-contract.md"),
             ("scripts/validate_handoff.py", "scripts/validate_handoff.py")]
    for sub, dest in (("schemas", "references/schemas"), ("templates", "templates")):
        for name in sorted(os.listdir(os.path.join(SRC, sub))):
            if name.endswith(".json"):
                pairs.append((sub + "/" + name, dest + "/" + name))
    return pairs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = []
    for skill in SKILLS:
        for src_rel, dest_rel in mapping():
            src = os.path.join(SRC, src_rel)
            dest = os.path.join(ROOT, "skills", skill, dest_rel)
            same = os.path.isfile(dest) and open(src, "rb").read() == open(dest, "rb").read()
            if same:
                continue
            if args.check:
                drift.append(os.path.relpath(dest, ROOT))
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(src, dest)
                os.chmod(dest, os.stat(src).st_mode)
    if args.check:
        if drift:
            print("contract drift:\n  " + "\n  ".join(drift))
            return 1
        print("contract copies are identical")
    else:
        print("contracts synced")
    return 0


if __name__ == "__main__":
    sys.exit(main())

