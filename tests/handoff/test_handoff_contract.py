"""Focused tests for the handoff contract v1 helper, fixtures and contract copies.

Run: python3 -m unittest discover -s tests/handoff -v
No provider connection or TYPO3 installation is needed.
"""
import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
VALIDATOR = os.path.join(ROOT, "docs", "contracts", "handoff-v1", "scripts", "validate_handoff.py")
FIXTURES = os.path.join(HERE, "fixtures", "bundle-valid")

spec = importlib.util.spec_from_file_location("validate_handoff", VALIDATOR)
vh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vh)

DS = "design-system.json"
CARD = "components/card/component-spec.json"
GRID = "components/card-grid/component-spec.json"
REPORT = "components/card/build-report.json"


class BundleCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "bundle")
        shutil.copytree(FIXTURES, self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def path(self, rel):
        return os.path.join(self.root, rel)

    def load(self, rel):
        with open(self.path(rel), encoding="utf-8") as fh:
            return json.load(fh)

    def save(self, rel, doc, seal=False):
        if seal:
            for d in doc["decisions"]:
                if d["status"] == "answered" and d["effect"] == "binding" and not d.get("bindingDigest") and d["appliesTo"] == doc["artifactId"]:
                    d["bindingDigest"] = vh.payload_digest(doc)
            doc["payloadDigest"] = vh.payload_digest(doc)
            doc["revision"] = vh.compute_revision(doc)
        with open(self.path(rel), "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2)

    def check(self, rel):
        result, findings = vh.validate_file(self.path(rel))
        return result, {f["code"] for f in findings.items}

    def codes(self, rel):
        return self.check(rel)[1]


class ValidFixtures(BundleCase):
    def test_all_valid_fixtures_pass_and_are_fresh(self):
        for rel in (DS, CARD, GRID, REPORT):
            result, codes = self.check(rel)
            self.assertTrue(result["ok"], (rel, result["findings"]))
            self.assertIs(result["fresh"], True)

    def test_cli_exit_codes_and_json(self):
        out = subprocess.run([sys.executable, VALIDATOR, "validate", "--json", self.path(CARD)], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(json.loads(out.stdout)["ok"])
        doc = self.load(CARD)
        doc["schemaVersion"] = "2.0.0"
        self.save(CARD, doc)
        out = subprocess.run([sys.executable, VALIDATOR, "validate", self.path(CARD)], capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertEqual(subprocess.run([sys.executable, VALIDATOR, "--help"], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run([sys.executable, VALIDATOR, "validate", self.path("nope.json")], capture_output=True).returncode, 1)


class RevisionStability(BundleCase):
    def test_same_input_same_revision_and_key_order_irrelevant(self):
        doc = self.load(CARD)
        shuffled = json.loads(json.dumps(doc, sort_keys=True))
        self.assertEqual(vh.compute_revision(doc), vh.compute_revision(shuffled))

    def test_timestamp_verification_evidence_and_hypothesis_do_not_change_revision(self):
        doc = self.load(CARD)
        base = vh.compute_revision(doc)
        doc["generatedAt"] = "2030-01-01T00:00:00Z"
        doc["verification"].append({"id": "x", "status": "not-run", "reason": "later"})
        doc["evidence"].append({"id": "ev-9", "class": "unknown", "kind": "note"})
        doc["payload"]["targetHypothesis"]["proposedFields"] = ["different"]
        doc["decisions"][0]["effect"] = "run-only"
        self.assertEqual(vh.compute_revision(doc), base)
        self.assertEqual(vh.payload_digest(doc), self.load(CARD)["payloadDigest"])

    def test_hypothesis_change_keeps_spec_current(self):
        doc = self.load(CARD)
        doc["payload"]["targetHypothesis"]["placementClass"] = "native-component"
        doc["payload"]["targetHypothesis"]["placeable"] = False
        self.save(CARD, doc)  # not resealed on purpose
        self.assertNotIn("payload-digest-mismatch", self.codes(CARD))
        self.assertNotIn("revision-mismatch", self.codes(CARD))
        self.assertNotIn("stale-dependency", self.codes(REPORT))

    def test_binding_payload_source_and_dependency_changes_alter_revision(self):
        doc = self.load(CARD)
        base = vh.compute_revision(doc)
        changed = copy.deepcopy(doc)
        changed["payload"]["contentModel"][0]["cardinality"] = "2"
        self.assertNotEqual(vh.compute_revision(changed), base)
        changed = copy.deepcopy(doc)
        changed["sources"][0]["digest"] = "sha256:" + "b" * 64
        self.assertNotEqual(vh.compute_revision(changed), base)
        changed = copy.deepcopy(doc)
        changed["dependencies"][0]["revision"] = "sha256:" + "c" * 64
        self.assertNotEqual(vh.compute_revision(changed), base)


class Invalidation(BundleCase):
    def test_token_change_makes_dependents_stale_but_not_invalid(self):
        ds = self.load(DS)
        ds["payload"]["tokens"][0]["value"] = "#ff0000"
        self.save(DS, ds, seal=True)
        for rel in (CARD, GRID, REPORT):
            result, codes = self.check(rel)
            self.assertIn("stale-dependency", codes, rel)
            self.assertFalse(result["ok"])
            self.assertIs(result["fresh"], False)
        proc = subprocess.run([sys.executable, VALIDATOR, "validate", self.path(CARD)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)

    def test_source_revision_change_propagates(self):
        ds = self.load(DS)
        ds["sources"][0]["digest"] = "sha256:" + "d" * 64
        self.save(DS, ds, seal=True)
        self.assertIn("stale-dependency", self.codes(CARD))

    def test_unsealed_payload_edit_is_payload_digest_mismatch(self):
        doc = self.load(CARD)
        doc["payload"]["component"]["name"] = "Edited"
        self.save(CARD, doc)
        codes = self.codes(CARD)
        self.assertIn("payload-digest-mismatch", codes)
        self.assertNotIn("revision-mismatch", codes)

    def test_unsealed_source_edit_is_revision_mismatch(self):
        doc = self.load(CARD)
        doc["sources"][0]["digest"] = "sha256:" + "e" * 64
        self.save(CARD, doc)
        codes = self.codes(CARD)
        self.assertIn("revision-mismatch", codes)
        self.assertNotIn("payload-digest-mismatch", codes)

    def test_unknown_freshness_for_unavailable_source_and_missing_dependency(self):
        doc = self.load(CARD)
        doc["sources"][0] = {"kind": "screenshot", "locator": "shot.png", "identityStatus": "unavailable"}
        self.save(CARD, doc, seal=True)
        result, codes = self.check(CARD)
        self.assertIn("unknown-freshness", codes)
        self.assertEqual(result["fresh"], "unknown")
        os.remove(self.path(DS))
        self.assertIn("unknown-freshness", self.codes(GRID))

    def test_unsupported_schema_major_distinguished(self):
        doc = self.load(CARD)
        doc["schemaVersion"] = "2.1.0"
        self.save(CARD, doc)
        self.assertEqual(self.codes(CARD), {"unsupported-schema-major"})
        ds = self.load(DS)
        ds["schemaVersion"] = "2.0.0"
        self.save(DS, ds)
        self.assertIn("unsupported-schema-major", self.codes(GRID))

    def test_malformed_fields(self):
        doc = self.load(CARD)
        del doc["decisions"]
        doc["readiness"] = "done"
        doc["payload"]["scope"] = "many"
        doc["sources"][0]["locator"] = 5
        self.save(CARD, doc)
        result, codes = self.check(CARD)
        self.assertTrue({"missing-field", "bad-enum", "bad-type"} <= codes)
        self.assertFalse(result["ok"])

    def test_known_source_requires_digest_or_revision(self):
        doc = self.load(CARD)
        del doc["sources"][0]["digest"]
        self.save(CARD, doc, seal=True)
        self.assertIn("bad-value", self.codes(CARD))


class References(BundleCase):
    def test_escaping_absolute_and_url_refs_rejected(self):
        for bad, code in (("../../../outside.json", "escaping-reference"), ("/etc/passwd", "invalid-reference"),
                          ("https://example.com/x.json", "invalid-reference"), ("a\\b.json", "invalid-reference")):
            doc = self.load(CARD)
            doc["dependencies"][0]["ref"] = bad
            self.save(CARD, doc, seal=True)
            self.assertIn(code, self.codes(CARD), bad)

    def test_symlink_escape_rejected(self):
        outside = os.path.join(self.tmp, "outside")
        os.makedirs(outside)
        link = os.path.join(self.root, "components", "card", "link")
        os.symlink(outside, link)
        doc = self.load(CARD)
        doc["dependencies"][0]["ref"] = "link/design-system.json"
        self.save(CARD, doc, seal=True)
        self.assertIn("escaping-reference", self.codes(CARD))

    def test_missing_or_stale_child_makes_parent_not_ready(self):
        os.remove(self.path(CARD))
        self.assertIn("readiness-inconsistent", self.codes(GRID))
        grid = self.load(GRID)
        grid["readiness"] = "incomplete"
        grid["unresolved"] = [{"id": "child", "description": "card spec missing", "readinessEffect": "incomplete"}]
        self.save(GRID, grid, seal=True)
        self.assertNotIn("readiness-inconsistent", self.codes(GRID))

    def test_child_must_be_a_dependency(self):
        grid = self.load(GRID)
        grid["dependencies"] = [d for d in grid["dependencies"] if d["artifactType"] != "component-spec"]
        self.save(GRID, grid, seal=True)
        self.assertIn("child-dependency-missing", self.codes(GRID))


class Decisions(BundleCase):
    def decision(self, **over):
        d = {"id": "d-1", "question": "Accept nearest recipe?", "options": ["deviation", "blocked"], "status": "answered",
             "answer": "deviation", "answerWording": "yes, accept it", "date": "2026-10-31", "appliesTo": "card", "effect": "binding"}
        d.update(over)
        return d

    def with_decision(self, d):
        spec_doc = self.load(CARD)
        self.save(CARD, spec_doc, seal=True)
        doc = self.load(REPORT)
        doc["decisions"] = [d]
        self.save(REPORT, doc, seal=True)
        return doc

    def test_valid_binding_decision_bound_to_current_spec(self):
        digest = self.load(CARD)["payloadDigest"]
        self.with_decision(self.decision(bindingDigest=digest))
        self.assertNotIn("decision-invalid", self.codes(REPORT))
        self.assertNotIn("decision-stale", self.codes(REPORT))

    def test_decision_becomes_stale_when_binding_requirements_change(self):
        digest = self.load(CARD)["payloadDigest"]
        self.with_decision(self.decision(bindingDigest=digest))
        spec_doc = self.load(CARD)
        spec_doc["payload"]["contentModel"][0]["cardinality"] = "2"
        self.save(CARD, spec_doc, seal=True)
        # refresh the report's dependency so only the decision is stale
        report = self.load(REPORT)
        for dep in report["dependencies"]:
            if dep["artifactId"] == "card":
                dep["revision"] = self.load(CARD)["revision"]
        self.save(REPORT, report, seal=True)
        result, codes = self.check(REPORT)
        self.assertIn("decision-stale", codes)
        self.assertNotIn("stale-dependency", codes)

    def test_hypothesis_only_change_does_not_stale_decision(self):
        digest = self.load(CARD)["payloadDigest"]
        self.with_decision(self.decision(bindingDigest=digest))
        spec_doc = self.load(CARD)
        spec_doc["payload"]["targetHypothesis"]["proposedFields"] = ["x"]
        self.save(CARD, spec_doc, seal=True)
        self.assertNotIn("decision-stale", self.codes(REPORT))

    def test_decision_field_rules(self):
        self.with_decision(self.decision(answerWording="", answer="maybe", bindingDigest="sha256:" + "0" * 64))
        self.assertIn("decision-invalid", self.codes(REPORT))
        self.with_decision(self.decision())  # binding without bindingDigest
        self.assertIn("decision-invalid", self.codes(REPORT))

    def test_binding_decision_changes_revision_run_only_does_not(self):
        doc = self.load(CARD)
        base = vh.compute_revision(doc)
        doc["decisions"].append(self.decision(bindingDigest=doc["payloadDigest"]))
        self.assertNotEqual(vh.compute_revision(doc), base)
        doc["decisions"][-1]["effect"] = "run-only"
        self.assertEqual(vh.compute_revision(doc), base)

    def test_unanswered_decision_must_be_unresolved_and_blocks_ready(self):
        d = self.decision(status="unanswered")
        for key in ("answer", "answerWording", "date"):
            d.pop(key)
        doc = self.load(CARD)
        doc["decisions"] = [d]
        self.save(CARD, doc, seal=True)
        codes = self.codes(CARD)
        self.assertIn("decision-invalid", codes)
        self.assertIn("readiness-inconsistent", codes)
        doc["readiness"] = "blocked"
        doc["unresolved"] = [{"id": "d-1", "description": "scope not answered", "readinessEffect": "blocked"}]
        self.save(CARD, doc, seal=True)
        self.assertEqual(self.codes(CARD), set())


class VerificationAndReadiness(BundleCase):
    def test_failed_or_not_run_cannot_be_verified(self):
        doc = self.load(REPORT)
        doc["verification"].append({"id": "v-mobile", "status": "failed", "reason": "image order wrong at 390px"})
        self.save(REPORT, doc, seal=True)
        codes = self.codes(REPORT)
        self.assertIn("unqualified-verified", codes)
        self.assertIn("readiness-inconsistent", codes)
        doc = self.load(REPORT)
        doc["verification"][-1]["status"] = "not-run"
        self.save(REPORT, doc, seal=True)
        self.assertIn("unqualified-verified", self.codes(REPORT))
        doc["payload"]["completion"] = "qualified"
        self.save(REPORT, doc, seal=True)
        self.assertNotIn("unqualified-verified", self.codes(REPORT))

    def test_screenshot_alone_cannot_verify(self):
        doc = self.load(REPORT)
        doc["payload"]["checks"] = [c for c in doc["payload"]["checks"] if c["gate"] == "advisory"]
        self.save(REPORT, doc, seal=True)
        self.assertIn("unqualified-verified", self.codes(REPORT))

    def test_failed_hard_check_blocks_verified(self):
        doc = self.load(REPORT)
        doc["payload"]["checks"][0]["status"] = "failed"
        self.save(REPORT, doc, seal=True)
        self.assertIn("unqualified-verified", self.codes(REPORT))

    def test_accepted_deviation_needs_answered_binding_decision(self):
        doc = self.load(REPORT)
        doc["payload"]["acceptedDeviations"] = [{"requirement": "pill recipe", "reason": "no clean adaptation", "approver": "pm", "decisionId": "missing"}]
        self.save(REPORT, doc, seal=True)
        self.assertIn("decision-invalid", self.codes(REPORT))

    def test_fsc_conflict_with_target_edits_is_inconsistent(self):
        doc = self.load(REPORT)
        doc["payload"]["preflight"] = {"status": "blocked", "fscConflict": True}
        self.save(REPORT, doc, seal=True)
        self.assertIn("readiness-inconsistent", self.codes(REPORT))

    def test_embedded_component_is_not_placeable(self):
        doc = self.load(CARD)
        doc["payload"]["targetHypothesis"].update({"placementClass": "native-component", "placeable": True})
        self.save(CARD, doc, seal=True)
        self.assertIn("bad-value", self.codes(CARD))

    def test_unresolved_blocks_ready(self):
        doc = self.load(CARD)
        doc["unresolved"] = [{"id": "u", "description": "carousel loop unknown", "readinessEffect": "incomplete"}]
        self.save(CARD, doc, seal=True)
        self.assertIn("readiness-inconsistent", self.codes(CARD))


class ContractCopies(unittest.TestCase):
    def test_skill_copies_match_authoring_source(self):
        proc = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "sync_contracts.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_templates_equal_fixtures(self):
        tpl = os.path.join(ROOT, "docs", "contracts", "handoff-v1", "templates")
        pairs = {"design-system.example.json": DS, "component-spec.example.json": CARD,
                 "component-spec-parent.example.json": GRID, "build-report.example.json": REPORT}
        for name, rel in pairs.items():
            with open(os.path.join(tpl, name), "rb") as a, open(os.path.join(FIXTURES, rel), "rb") as b:
                self.assertEqual(a.read(), b.read(), name)

    def test_contract_is_standalone_in_skills(self):
        for skill in ("typo3-design-system-extract", "typo3-component-analyze", "typo3-component-build"):
            base = os.path.join(ROOT, "skills", skill)
            if not os.path.isdir(base):
                continue
            tmp = tempfile.mkdtemp()
            try:
                dest = os.path.join(tmp, skill)
                shutil.copytree(base, dest)
                proc = subprocess.run([sys.executable, os.path.join(dest, "scripts", "validate_handoff.py"), "validate",
                                       os.path.join(FIXTURES, DS)], capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            finally:
                shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
