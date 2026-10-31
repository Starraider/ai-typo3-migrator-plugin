#!/usr/bin/env python3
"""Generate the synthetic handoff fixtures and the contract templates.

Run from the repository root:  python3 tests/handoff/build_fixtures.py

Writes sealed example artifacts to tests/handoff/fixtures/bundle-valid/ and copies
the same examples to docs/contracts/handoff-v1/templates/ (the authoring source).
The data is synthetic and does not copy upstream assets.
"""
import copy
import importlib.util
import json
import os
import shutil

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CONTRACT = os.path.join(ROOT, "docs", "contracts", "handoff-v1")
FIXTURES = os.path.join(ROOT, "tests", "handoff", "fixtures", "bundle-valid")

spec = importlib.util.spec_from_file_location("validate_handoff", os.path.join(CONTRACT, "scripts", "validate_handoff.py"))
vh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vh)

SRC_DIGEST = "sha256:" + "a" * 64


def seal(doc):
    for d in doc["decisions"]:
        if d["status"] == "answered" and d["effect"] == "binding" and not d.get("bindingDigest") and d["appliesTo"] == doc["artifactId"]:
            d["bindingDigest"] = vh.payload_digest(doc)
    doc["payloadDigest"] = vh.payload_digest(doc)
    doc["revision"] = vh.compute_revision(doc)
    return doc


def dep(doc, ref):
    return {"artifactType": doc["artifactType"], "artifactId": doc["artifactId"],
            "schemaVersion": doc["schemaVersion"], "revision": doc["revision"], "ref": ref}


def envelope(atype, aid, payload, **kw):
    return {
        "schemaVersion": "1.0.0", "artifactType": atype, "artifactId": aid,
        "revision": "sha256:" + "0" * 64, "payloadDigest": "sha256:" + "0" * 64,
        "generatedAt": "2026-10-31T00:00:00Z",
        "readiness": kw.get("readiness", "ready"),
        "sources": kw.get("sources", [{"kind": "react-source", "locator": "mockup/src", "identityStatus": "known", "digest": SRC_DIGEST}]),
        "dependencies": kw.get("dependencies", []),
        "target": kw.get("target", {"versionsKnown": True, "typo3": "14.3.1", "php": "8.3.12", "astryx": "1.0.0", "styleXConnector": "1.1.2", "conflicts": []}),
        "evidence": kw.get("evidence", [{"id": "ev-1", "class": "observed", "kind": "source", "locator": "mockup/src/index.css"}]),
        "verification": kw.get("verification", []),
        "decisions": kw.get("decisions", []),
        "unresolved": kw.get("unresolved", []),
        "payload": payload,
    }


def design_system():
    payload = {
        "mode": "implementation",
        "tokens": [
            {"id": "color.accent", "tier": "semantic", "role": "accent", "value": "#0b5fff", "renderedValue": "rgb(11, 95, 255)",
             "sourceLocation": "mockup/src/index.css:12", "confidence": "observed", "scope": ":root",
             "mapping": {"status": "mapped", "targetProperty": "--astryx-color-accent", "rationale": "same semantic role in installed tokens.stylex.js"}},
            {"id": "space.section", "tier": "primitive", "role": "section spacing", "value": "clamp(3rem, 6vw, 6rem)", "confidence": "observed", "scope": ":root",
             "mapping": {"status": "project-token", "targetProperty": "--brand-space-section", "rationale": "fluid value has no Astryx equivalent"}},
        ],
        "fonts": [{"family": "Example Sans", "weights": ["400", "700"], "status": "available", "files": ["Resources/Public/Fonts/example-sans.woff2"]}],
        "assets": [{"id": "logo", "source": "mockup/public/logo.svg", "checksum": SRC_DIGEST, "mediaType": "image/svg+xml", "ownership": "site-package", "rights": "client-supplied", "destination": "Resources/Public/Images/logo.svg", "status": "available"}],
        "themes": [{"name": "default", "selector": ":root", "mode": "light", "selectable": "verified"}],
        "breakpoints": [{"name": "md", "query": "(min-width: 48rem)", "confidence": "observed"}],
        "globalStyles": [{"selector": "body", "summary": "Example Sans 16px/1.6, accent link color"}],
        "targetCompatibility": {"status": "supported", "checks": [{"name": "typo3 14.3.x", "result": "ok"}, {"name": "fluid_styled_content absent", "result": "ok"}]},
        "foundation": {"status": "verified", "assetMode": "consuming-project-vite", "entrypoints": ["Resources/Private/JavaScript/main.js"], "manifests": ["Resources/Public/.vite/manifest.json", "Resources/Public/stylex-manifest.json"]},
    }
    return envelope("design-system", "acme-site", payload, verification=[
        {"id": "v-css-manifest", "status": "passed", "reason": "CSS hash matches style manifest", "command": "npm run build"},
        {"id": "v-render", "status": "passed", "reason": "computed styles match reference at 3 widths"}])


def card_spec(ds):
    payload = {
        "component": {"id": "card", "name": "Card", "sourceLocator": "mockup/src/components/Card.tsx", "renderedLocation": "/#cards"},
        "scope": "single", "children": [],
        "structure": [{"part": "media", "role": "image"}, {"part": "body", "role": "title, badge, text, actions"}],
        "variants": [{"name": "vertical", "evidence": "source"}, {"name": "horizontal", "evidence": "source", "condition": "md and up"}],
        "contentModel": [
            {"name": "title", "kind": "editorial", "cardinality": "1", "validation": "max 80 characters"},
            {"name": "badge", "kind": "editorial", "cardinality": "0..1"},
            {"name": "actions", "kind": "editorial", "cardinality": "0..3"},
            {"name": "hover", "kind": "interaction-state", "cardinality": "n/a"}],
        "assets": [{"id": "card-image", "role": "media", "ownership": "fal-editorial", "aspectRatio": "16:9", "altRequired": True, "status": "available"}],
        "responsive": [{"condition": "min-width 48rem", "rule": "image moves beside text", "evidence": "source"}],
        "interactions": [{"name": "focus", "behavior": "visible focus ring on actions", "evidence": "source", "keyboard": "tab order follows DOM"}],
        "referenceCaptures": [{"ref": "references/card-768.png", "viewport": "768x900", "state": "default", "conditions": "Example Sans loaded, DPR 1"}],
        "candidateNotes": [{"candidate": "Astryx Card", "gaps": ["no badge field"], "advisory": True}],
        "verificationCriteria": [{"id": "vc-1", "criterion": "box geometry within 1px", "viewport": "768x900", "state": "default"}],
        "targetHypothesis": {"placementClass": "content-element", "placeable": True, "proposedFields": ["header", "image", "badge", "links"]},
    }
    return envelope("component-spec", "card", payload, dependencies=[dep(ds, "../../design-system.json")],
                    decisions=[{"id": "d-scope-card", "question": "Analysis granularity for the card section?", "options": ["single", "parent-with-children"],
                                "status": "answered", "answer": "parent-with-children", "answerWording": "one spec for the card, reused", "date": "2026-10-31",
                                "appliesTo": "card", "effect": "run-only"}])


def grid_spec(ds, card):
    payload = {
        "component": {"id": "card-grid", "name": "Card grid section", "sourceLocator": "mockup/src/sections/CardGrid.tsx"},
        "scope": "parent-with-children",
        "children": [{"componentId": "card", "ref": "../card/component-spec.json", "count": 3}],
        "structure": [{"part": "section", "role": "full-width background", "children": ["column"]}],
        "variants": [], "contentModel": [{"name": "cards", "kind": "editorial", "cardinality": "3..6"}],
        "assets": [], "responsive": [{"condition": "below 48rem", "rule": "single column", "evidence": "source"}],
        "interactions": [], "referenceCaptures": [], "candidateNotes": [], "verificationCriteria": [{"id": "vc-g1", "criterion": "three columns at desktop"}],
        "targetHypothesis": {"placementClass": "nested-container", "placeable": True,
                             "container": {"columns": [{"colPos": 101, "name": "Cards", "allowedChildren": ["astryx_card"], "min": 3, "max": 6}]}},
    }
    return envelope("component-spec", "card-grid", payload,
                    dependencies=[dep(ds, "../../design-system.json"), dep(card, "../card/component-spec.json")])


def build_report(ds, card):
    payload = {
        "component": {"id": "card", "specRef": "component-spec.json"},
        "completion": "verified", "disposition": "extend",
        "hypothesis": {"outcome": "adopted"},
        "candidates": [{"name": "Astryx Card", "path": "vendor/skom/typo3-astryx/ContentBlocks/ContentElements/card", "installedVersion": "1.0.0",
                        "fields": ["header", "image", "links"], "slots": ["default", "media"], "recipes": ["vertical"], "fit": "partial", "gaps": ["no badge field"], "selected": True}],
        "rejectedAlternatives": [{"option": "new block", "reason": "extension covers the badge gap"}],
        "preflight": {"status": "passed", "fscConflict": False, "details": ["TYPO3 14.3.1", "PHP 8.3.12"]},
        "changes": [{"path": "packages/site/ContentBlocks/ContentElements/card-extension/config.yaml", "kind": "created"}],
        "extensionPoints": ["site-package Content Block extension"],
        "assets": [{"id": "card-image", "disposition": "FAL editorial"}],
        "checks": [
            {"id": "c-style-768", "kind": "computed-style", "gate": "hard", "status": "passed", "viewport": "768x900", "state": "default"},
            {"id": "c-layout-768", "kind": "layout", "gate": "hard", "status": "passed", "viewport": "768x900", "state": "default"},
            {"id": "c-shot-768", "kind": "screenshot", "gate": "advisory", "status": "passed", "viewport": "768x900"}],
        "differences": [{"id": "diff-aa", "description": "anti-aliasing noise", "disposition": "noise"}],
        "acceptedDeviations": [],
    }
    return envelope("build-report", "card-build", payload,
                    dependencies=[dep(ds, "../../design-system.json"), dep(card, "component-spec.json")],
                    verification=[{"id": "v-editor", "status": "passed", "reason": "backend edit with long title checked"}])


def write(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main():
    if os.path.isdir(FIXTURES):
        shutil.rmtree(FIXTURES)
    ds = seal(design_system())
    card = card_spec(ds)
    card = seal(card)
    grid = seal(grid_spec(ds, card))
    report = seal(build_report(ds, card))
    layout = {
        "design-system.json": ds,
        "components/card/component-spec.json": card,
        "components/card-grid/component-spec.json": grid,
        "components/card/build-report.json": report,
    }
    for rel, doc in layout.items():
        write(os.path.join(FIXTURES, rel), doc)
    templates = os.path.join(CONTRACT, "templates")
    os.makedirs(templates, exist_ok=True)
    write(os.path.join(templates, "design-system.example.json"), ds)
    write(os.path.join(templates, "component-spec.example.json"), card)
    write(os.path.join(templates, "component-spec-parent.example.json"), grid)
    write(os.path.join(templates, "build-report.example.json"), report)
    print("fixtures and templates written")


if __name__ == "__main__":
    main()

