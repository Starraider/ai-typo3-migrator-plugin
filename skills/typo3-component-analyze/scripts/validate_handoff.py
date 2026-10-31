#!/usr/bin/env python3
"""Validate, hash and seal TYPO3 design-migration handoff artifacts (contract v1).

Dependencies: Python 3.8+ standard library only. No provider connection, network
access, or TYPO3 installation is needed, so the same command runs locally and in CI.

Commands:
  validate FILE   Check structure, readiness rules, decisions, references and freshness.
  revision FILE   Print the recomputed payloadDigest and revision (no writes).
  seal FILE       Recompute payloadDigest and revision and write them into FILE.

Exit codes (validate):
  0  valid and fresh
  1  invalid (at least one error finding)
  2  structurally valid but not provably current (stale or unknown freshness)
  64 usage or I/O problem

Run `validate_handoff.py validate --json FILE` for machine-readable results.
"""
import argparse
import hashlib
import json
import os
import re
import sys

SUPPORTED_MAJOR = 1
TYPES = ("design-system", "component-spec", "build-report")
ERROR, STALE = "error", "stale"


# --------------------------------------------------------------------------- hashing

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def binding_payload(doc):
    """Payload used for hashing: the non-binding targetHypothesis is excluded."""
    payload = doc.get("payload")
    if not isinstance(payload, dict):
        return payload
    return {k: v for k, v in payload.items() if k != "targetHypothesis"}


def payload_digest(doc):
    return digest(binding_payload(doc))


def revision_input(doc):
    sources = [
        {k: s.get(k) for k in ("kind", "locator", "selector", "identityStatus", "digest", "revision")}
        for s in doc.get("sources", []) if isinstance(s, dict)
    ]
    deps = [
        {k: d.get(k) for k in ("artifactType", "artifactId", "schemaVersion", "revision")}
        for d in doc.get("dependencies", []) if isinstance(d, dict)
    ]
    decisions = [
        {k: d.get(k) for k in ("id", "appliesTo", "answer", "effect", "bindingDigest")}
        for d in doc.get("decisions", [])
        if isinstance(d, dict) and d.get("status") == "answered" and d.get("effect") == "binding"
    ]
    return {
        "schemaVersion": doc.get("schemaVersion"),
        "artifactType": doc.get("artifactType"),
        "artifactId": doc.get("artifactId"),
        "payload": binding_payload(doc),
        "sources": sorted(sources, key=canonical),
        "dependencies": sorted(deps, key=canonical),
        "decisions": sorted(decisions, key=lambda d: str(d["id"])),
    }


def compute_revision(doc):
    return digest(revision_input(doc))


# --------------------------------------------------------------- mini JSON Schema

class Schema:
    """Small interpreter for the JSON Schema subset used by the shipped schemas."""

    def __init__(self, root):
        self.root = root

    def resolve(self, ref):
        node = self.root
        for part in ref.lstrip("#/").split("/"):
            node = node[part]
        return node

    def check(self, value, schema, path, out):
        if "$ref" in schema:
            return self.check(value, self.resolve(schema["$ref"]), path, out)
        if "enum" in schema and value not in schema["enum"]:
            out.append(("bad-enum", path, "must be one of %s, got %r" % (schema["enum"], value)))
            return
        if "type" in schema and not self._type_ok(value, schema["type"]):
            out.append(("bad-type", path, "expected %s, got %s" % (schema["type"], type(value).__name__)))
            return
        if isinstance(value, str):
            if "minLength" in schema and len(value) < schema["minLength"]:
                out.append(("bad-value", path, "must not be empty"))
            if "pattern" in schema and not re.search(schema["pattern"], value):
                out.append(("bad-value", path, "does not match pattern %s" % schema["pattern"]))
        if isinstance(value, dict):
            for key in schema.get("required", []):
                if key not in value:
                    out.append(("missing-field", path + "/" + key if path else key, "required field is missing"))
            for key, sub in schema.get("properties", {}).items():
                if key in value:
                    self.check(value[key], sub, (path + "/" + key) if path else key, out)
        if isinstance(value, list):
            if "minItems" in schema and len(value) < schema["minItems"]:
                out.append(("bad-value", path, "needs at least %d item(s)" % schema["minItems"]))
            if "items" in schema:
                for i, item in enumerate(value):
                    self.check(item, schema["items"], "%s[%d]" % (path, i), out)

    @staticmethod
    def _type_ok(value, expected):
        names = expected if isinstance(expected, list) else [expected]
        for name in names:
            if name == "object" and isinstance(value, dict):
                return True
            if name == "array" and isinstance(value, list):
                return True
            if name == "string" and isinstance(value, str):
                return True
            if name == "boolean" and isinstance(value, bool):
                return True
            if name == "integer" and isinstance(value, int) and not isinstance(value, bool):
                return True
            if name == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
                return True
        return False


def schema_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.join(here, "..", "references", "schemas"), os.path.join(here, "..", "schemas")):
        if os.path.isfile(os.path.join(candidate, "envelope.schema.json")):
            return os.path.normpath(candidate)
    raise FileNotFoundError("handoff schemas not found next to this script")


def load_schema(name):
    with open(os.path.join(schema_dir(), name), encoding="utf-8") as fh:
        return Schema(json.load(fh))


# ------------------------------------------------------------------- validation

class Findings:
    def __init__(self):
        self.items = []

    def add(self, code, path, message, severity=ERROR):
        self.items.append({"code": code, "severity": severity, "path": path, "message": message})

    def errors(self):
        return [f for f in self.items if f["severity"] == ERROR]

    def stale(self):
        return [f for f in self.items if f["severity"] == STALE]


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def find_bundle_root(artifact_path):
    cur = os.path.dirname(os.path.realpath(artifact_path))
    parent_dir = os.path.dirname(cur)
    if os.path.basename(parent_dir) == "components" and not os.path.isfile(os.path.join(cur, "design-system.json")):
        return os.path.dirname(parent_dir)
    probe = cur
    while True:
        if os.path.isfile(os.path.join(probe, "design-system.json")):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            return cur
        probe = parent


def resolve_ref(ref, artifact_dir, bundle_root, findings, path):
    """Return the absolute path for a relative reference, or None when it is invalid."""
    if (not isinstance(ref, str) or not ref or os.path.isabs(ref) or "\\" in ref
            or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", ref) or ref.startswith("//")):
        findings.add("invalid-reference", path, "reference must be a relative POSIX path inside the bundle: %r" % (ref,))
        return None
    target = os.path.normpath(os.path.join(artifact_dir, ref))
    real_root = os.path.realpath(bundle_root)
    real_target = os.path.realpath(target)
    if os.path.commonpath([real_root, real_target]) != real_root:
        findings.add("escaping-reference", path, "reference escapes the bundle root: %r" % ref)
        return None
    return target


def check_decisions(doc, findings, artifact_dir, bundle_root, dep_docs):
    decisions = doc.get("decisions", [])
    unresolved_ids = {u.get("id") for u in doc.get("unresolved", []) if isinstance(u, dict)}
    seen = set()
    own_payload = payload_digest(doc)
    for i, d in enumerate(decisions):
        if not isinstance(d, dict):
            continue
        path = "decisions[%d]" % i
        if d.get("id") in seen:
            findings.add("decision-invalid", path, "duplicate decision id %r" % d.get("id"))
        seen.add(d.get("id"))
        if d.get("status") == "unanswered":
            if d.get("answer"):
                findings.add("decision-invalid", path, "unanswered decision must not carry an answer")
            if d.get("id") not in unresolved_ids:
                findings.add("decision-invalid", path, "unanswered decision %r must appear in unresolved" % d.get("id"))
            if doc.get("readiness") == "ready":
                findings.add("readiness-inconsistent", "readiness", "unanswered decision %r prevents ready" % d.get("id"))
            continue
        if d.get("status") != "answered":
            continue
        for key in ("answer", "answerWording", "date"):
            if not d.get(key):
                findings.add("decision-invalid", path + "/" + key, "answered decision requires %s" % key)
        if d.get("answer") and d.get("options") and d["answer"] not in d["options"]:
            findings.add("decision-invalid", path + "/answer", "answer %r is not one of the offered options" % d["answer"])
        if d.get("effect") != "binding":
            continue
        if not d.get("bindingDigest"):
            findings.add("decision-invalid", path + "/bindingDigest", "binding decision requires bindingDigest")
            continue
        applies = d.get("appliesTo")
        current = None
        if applies == doc.get("artifactId"):
            current = own_payload
        elif applies in dep_docs:
            current = payload_digest(dep_docs[applies])
        if current is not None and current != d["bindingDigest"]:
            findings.add("decision-stale", path,
                         "binding requirements of %r changed after decision %r was answered; ask again" % (applies, d.get("id")),
                         STALE)


def check_readiness(doc, findings):
    readiness = doc.get("readiness")
    unresolved = [u for u in doc.get("unresolved", []) if isinstance(u, dict)]
    if readiness == "ready" and unresolved:
        findings.add("readiness-inconsistent", "readiness", "ready is not allowed while unresolved entries exist")
    if readiness == "incomplete" and any(u.get("readinessEffect") == "blocked" for u in unresolved):
        findings.add("readiness-inconsistent", "readiness", "a blocking unresolved entry requires readiness blocked")
    if readiness == "ready" and any(v.get("status") == "failed" for v in doc.get("verification", []) if isinstance(v, dict)):
        findings.add("readiness-inconsistent", "readiness", "ready is not allowed with a failed verification entry")


def check_type_rules(doc, findings, artifact_dir, bundle_root, dep_docs):
    payload = doc.get("payload", {})
    verification = [v for v in doc.get("verification", []) if isinstance(v, dict)]
    unqualified = [v["id"] for v in verification if v.get("status") in ("failed", "not-run")]
    atype = doc.get("artifactType")
    if atype == "design-system":
        foundation = payload.get("foundation", {})
        if foundation.get("status") == "verified" and unqualified:
            findings.add("unqualified-verified", "payload/foundation/status",
                         "foundation cannot be verified while checks are failed or not-run: %s" % ", ".join(unqualified))
        compat = payload.get("targetCompatibility", {})
        if payload.get("mode") == "implementation" and compat.get("status") not in ("supported",):
            if foundation.get("status") in ("implemented", "verified"):
                findings.add("readiness-inconsistent", "payload/foundation/status",
                             "implementation requires targetCompatibility.status supported")
    elif atype == "component-spec":
        children = payload.get("children", [])
        if payload.get("scope") == "parent-with-children" and not children:
            findings.add("readiness-inconsistent", "payload/children", "parent-with-children scope needs child references")
        if payload.get("scope") == "single" and children:
            findings.add("readiness-inconsistent", "payload/children", "single scope must not reference child specifications")
        deps_by_ref = {d.get("ref"): d for d in doc.get("dependencies", []) if isinstance(d, dict)}
        for i, child in enumerate(children):
            if not isinstance(child, dict):
                continue
            cpath = "payload/children[%d]" % i
            target = resolve_ref(child.get("ref"), artifact_dir, bundle_root, findings, cpath + "/ref")
            dep = deps_by_ref.get(child.get("ref"))
            problem = None
            if target is None:
                problem = "invalid child reference"
            elif dep is None:
                problem = "child is not listed in dependencies"
                findings.add("child-dependency-missing", cpath, problem)
            elif not os.path.isfile(target):
                problem = "child specification is missing"
            else:
                try:
                    child_rev = compute_revision(read_json(target))
                    if child_rev != dep.get("revision"):
                        problem = "child specification is stale"
                except (ValueError, OSError):
                    problem = "child specification is unreadable"
            if problem and doc.get("readiness") == "ready":
                findings.add("readiness-inconsistent", cpath, "parent cannot be ready: %s" % problem)
        hyp = payload.get("targetHypothesis", {})
        if hyp.get("placementClass") == "native-component" and hyp.get("placeable"):
            findings.add("bad-value", "payload/targetHypothesis/placeable", "an embedded native component is not placeable")
        for ci, col in enumerate(hyp.get("container", {}).get("columns", [])):
            if isinstance(col, dict) and col.get("min", 0) > col.get("max", 0):
                findings.add("bad-value", "payload/targetHypothesis/container/columns[%d]" % ci, "min exceeds max")
    elif atype == "build-report":
        decisions = {d.get("id"): d for d in doc.get("decisions", []) if isinstance(d, dict)}
        for i, dev in enumerate(payload.get("acceptedDeviations", [])):
            ref = decisions.get(dev.get("decisionId")) if isinstance(dev, dict) else None
            if not ref or ref.get("status") != "answered":
                findings.add("decision-invalid", "payload/acceptedDeviations[%d]" % i,
                             "accepted deviation needs an answered decision")
            elif ref.get("effect") != "binding":
                findings.add("decision-invalid", "payload/acceptedDeviations[%d]" % i,
                             "accepted deviation decision must be binding")
        for i, diff in enumerate(payload.get("differences", [])):
            if isinstance(diff, dict) and diff.get("disposition") == "accepted" and not diff.get("decisionId"):
                findings.add("decision-invalid", "payload/differences[%d]" % i, "accepted difference needs decisionId")
        if payload.get("completion") == "verified":
            checks = payload.get("checks", [])
            bad = [c.get("id") for c in checks if isinstance(c, dict) and c.get("gate") == "hard" and c.get("status") != "passed"]
            advisory_only = not any(isinstance(c, dict) and c.get("gate") == "hard" and c.get("status") == "passed" for c in checks)
            open_diffs = [d.get("id") for d in payload.get("differences", []) if isinstance(d, dict) and d.get("disposition") == "open"]
            if unqualified or bad or open_diffs or advisory_only:
                reasons = []
                if unqualified:
                    reasons.append("verification failed/not-run: " + ", ".join(unqualified))
                if bad:
                    reasons.append("hard checks not passed: " + ", ".join(bad))
                if advisory_only:
                    reasons.append("no passed hard (computed style/layout) check")
                if open_diffs:
                    reasons.append("open differences: " + ", ".join(open_diffs))
                findings.add("unqualified-verified", "payload/completion", "; ".join(reasons))
        if payload.get("completion") == "blocked" and doc.get("readiness") == "ready":
            findings.add("readiness-inconsistent", "readiness", "blocked completion cannot be ready")
        if payload.get("preflight", {}).get("fscConflict") and payload.get("changes"):
            findings.add("readiness-inconsistent", "payload/changes", "target edits recorded despite a Fluid Styled Content conflict")


def validate_file(path, bundle_root=None):
    findings = Findings()
    result = {"file": path, "artifactType": None, "artifactId": None, "revision": None,
              "payloadDigest": None, "fresh": None, "ok": False, "findings": findings.items}
    try:
        doc = read_json(path)
    except (OSError, ValueError) as exc:
        findings.add("unreadable", "", "cannot read JSON: %s" % exc)
        return result, findings
    if not isinstance(doc, dict):
        findings.add("bad-type", "", "top level must be an object")
        return result, findings
    result["artifactType"], result["artifactId"] = doc.get("artifactType"), doc.get("artifactId")

    version = doc.get("schemaVersion")
    if isinstance(version, str) and re.match(r"^[0-9]+\.", version):
        if int(version.split(".")[0]) != SUPPORTED_MAJOR:
            findings.add("unsupported-schema-major", "schemaVersion",
                         "schema major %s is not supported (supported: %d)" % (version.split(".")[0], SUPPORTED_MAJOR))
            return result, findings

    raw = []
    load_schema("envelope.schema.json").check(doc, load_schema("envelope.schema.json").root, "", raw)
    if doc.get("artifactType") in TYPES and isinstance(doc.get("payload"), dict):
        pschema = load_schema("%s.payload.schema.json" % doc["artifactType"])
        pschema.check(doc["payload"], pschema.root, "payload", raw)
    for code, p, msg in raw:
        findings.add(code, p, msg)
    if findings.errors():
        return result, findings

    artifact_path = os.path.realpath(path)
    artifact_dir = os.path.dirname(artifact_path)
    root = os.path.realpath(bundle_root) if bundle_root else find_bundle_root(path)

    result["payloadDigest"] = payload_digest(doc)
    result["revision"] = compute_revision(doc)
    if result["payloadDigest"] != doc["payloadDigest"]:
        findings.add("payload-digest-mismatch", "payloadDigest",
                     "payload changed without resealing (recorded %s, computed %s)" % (doc["payloadDigest"], result["payloadDigest"]))
    elif result["revision"] != doc["revision"]:
        findings.add("revision-mismatch", "revision",
                     "revision does not match sources, dependencies or decisions (recorded %s, computed %s)" % (doc["revision"], result["revision"]))

    unknown = False
    for i, s in enumerate(doc["sources"]):
        if s["identityStatus"] == "known" and not (s.get("digest") or s.get("revision")):
            findings.add("bad-value", "sources[%d]" % i, "known source identity needs digest or revision")
        if s["identityStatus"] == "unavailable":
            unknown = True
            findings.add("unknown-freshness", "sources[%d]" % i,
                         "source identity unavailable (%s); freshness cannot be established" % s["locator"], STALE)

    dep_docs = {}
    for i, dep in enumerate(doc["dependencies"]):
        dpath = "dependencies[%d]" % i
        target = resolve_ref(dep["ref"], artifact_dir, root, findings, dpath + "/ref")
        if target is None:
            continue
        if not os.path.isfile(target):
            unknown = True
            findings.add("unknown-freshness", dpath, "dependency file not found: %s" % dep["ref"], STALE)
            continue
        try:
            dep_doc = read_json(target)
        except (OSError, ValueError) as exc:
            findings.add("unresolved-reference", dpath, "dependency unreadable: %s" % exc)
            continue
        dver = str(dep_doc.get("schemaVersion", ""))
        if not re.match(r"^[0-9]+\.", dver) or int(dver.split(".")[0]) != SUPPORTED_MAJOR:
            findings.add("unsupported-schema-major", dpath, "dependency uses unsupported schemaVersion %r" % dver)
            continue
        if dep_doc.get("artifactType") != dep["artifactType"] or dep_doc.get("artifactId") != dep["artifactId"]:
            findings.add("unresolved-reference", dpath, "dependency file identity differs from the recorded dependency")
            continue
        dep_docs[dep["artifactId"]] = dep_doc
        current = compute_revision(dep_doc)
        if current != dep["revision"]:
            findings.add("stale-dependency", dpath,
                         "%s '%s' changed (recorded %s, current %s); reassess before reuse" %
                         (dep["artifactType"], dep["artifactId"], dep["revision"], current), STALE)

    check_decisions(doc, findings, artifact_dir, root, dep_docs)
    check_readiness(doc, findings)
    check_type_rules(doc, findings, artifact_dir, root, dep_docs)

    result["fresh"] = False if findings.stale() else ("unknown" if unknown else True)
    if unknown and not any(f["code"] == "stale-dependency" for f in findings.items):
        result["fresh"] = "unknown"
    result["ok"] = not findings.errors() and not findings.stale()
    return result, findings


# ------------------------------------------------------------------------- CLI

def cmd_validate(args):
    result, findings = validate_file(args.file, args.bundle_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("%s: %s" % (args.file, "OK" if result["ok"] else "NOT OK"))
        for f in findings.items:
            print("  [%s] %s %s: %s" % (f["severity"], f["code"], f["path"], f["message"]))
        if result["ok"]:
            print("  revision %s (fresh)" % result["revision"])
    if findings.errors():
        return 1
    if findings.stale():
        return 2
    return 0


def cmd_revision(args):
    doc = read_json(args.file)
    print(json.dumps({"payloadDigest": payload_digest(doc), "revision": compute_revision(doc)}, indent=2))
    return 0


def cmd_seal(args):
    doc = read_json(args.file)
    for d in doc.get("decisions", []):
        if (isinstance(d, dict) and d.get("status") == "answered" and d.get("effect") == "binding"
                and not d.get("bindingDigest") and d.get("appliesTo") == doc.get("artifactId")):
            d["bindingDigest"] = payload_digest(doc)
    doc["payloadDigest"] = payload_digest(doc)
    doc["revision"] = compute_revision(doc)
    with open(args.file, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps({"file": args.file, "payloadDigest": doc["payloadDigest"], "revision": doc["revision"]}))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=__doc__.split("\n\n", 1)[1])
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validate a handoff JSON file")
    v.add_argument("file")
    v.add_argument("--bundle-root", help="bundle root that bounds relative references (default: nearest ancestor with design-system.json)")
    v.add_argument("--json", action="store_true", help="print machine-readable results")
    v.set_defaults(func=cmd_validate)
    r = sub.add_parser("revision", help="print recomputed digest and revision")
    r.add_argument("file")
    r.set_defaults(func=cmd_revision)
    s = sub.add_parser("seal", help="write recomputed digest and revision into the file")
    s.add_argument("file")
    s.set_defaults(func=cmd_seal)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 64


if __name__ == "__main__":
    sys.exit(main())
