from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


authoring = load_module("sle_authoring", ROOT / "scripts" / "sle_authoring.py")
figures = load_module("generate_sle_figures", ROOT / "scripts" / "generate_sle_figures.py")


class SleAuthoringTests(unittest.TestCase):
    def test_production_contracts_pass(self) -> None:
        report = authoring.validate()
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(report["metrics"]["chapters"], 18)
        self.assertEqual(report["metrics"]["question_bridges"], 17)
        self.assertEqual(report["metrics"]["contracts"], 23)

    def test_curriculum_question_chain_is_exact(self) -> None:
        production = json.loads(
            (ROOT / "sle-critical-phenomena" / "authoring" / "production.json").read_text(encoding="utf-8")
        )
        chapters = production["curriculum"]
        for previous, current in zip(chapters, chapters[1:]):
            self.assertEqual(previous["exit_question"], current["entry_question"])

    def test_fixture_has_no_unresolved_stop_point(self) -> None:
        contract = json.loads(
            (ROOT / "sle-critical-phenomena" / "authoring" / "contracts" / "00-production-fixture.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("unresolved", {item["resolution"] for item in contract["reader_stop_points"]})
        self.assertGreaterEqual(len(contract["new_concepts"]), 2)
        self.assertGreaterEqual(len(contract["derivations"]), 2)

    def test_figures_are_deterministic_and_have_accessibility_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_paths = figures.generate(Path(first))
            second_paths = figures.generate(Path(second))
            self.assertEqual([path.name for path in first_paths], [path.name for path in second_paths])
            for first_path, second_path in zip(first_paths, second_paths):
                self.assertEqual(first_path.read_bytes(), second_path.read_bytes())
                text = first_path.read_text(encoding="utf-8")
                self.assertIn("role=\"img\"", text)
                self.assertIn("<title", text)
                self.assertIn("<desc", text)

    def test_context_is_scoped_to_the_contract(self) -> None:
        context = authoring.context_markdown("fixture-00")
        self.assertIn('"chapter_id": "fixture-00"', context)
        self.assertIn('"id": "fig-slit-map"', context)
        self.assertNotIn('"id": "fig-kappa-phases"', context)


if __name__ == "__main__":
    unittest.main()
