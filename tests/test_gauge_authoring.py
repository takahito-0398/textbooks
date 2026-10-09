from __future__ import annotations

import importlib.util
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_gauge_authoring.py"
SPEC = importlib.util.spec_from_file_location("validate_gauge_authoring", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class GaugeAuthoringValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = validator.load_json(validator.MANIFEST_PATH)
        self.contracts = [validator.load_json(path) for path in sorted(validator.CONTRACT_DIR.glob("*.json"))]

    def test_repository_contracts_are_valid(self) -> None:
        self.assertEqual([], validator.validate_all(self.manifest, self.contracts))

    def test_forward_mathematical_dependency_is_rejected(self) -> None:
        broken = deepcopy(self.manifest)
        broken["curriculum"][0]["mathematical_dependencies"] = ["ch-02"]
        errors = validator.validate_manifest(broken)
        self.assertTrue(any("must point backward" in error for error in errors))

    def test_unresolved_reader_stop_point_is_rejected(self) -> None:
        broken = deepcopy(self.contracts[0])
        broken["reader_stop_points"][0]["resolution"] = "unresolved"
        errors = validator.validate_contract(broken, self.manifest, Path("00-production-fixture.json"))
        self.assertTrue(any("unresolved Reader Stop-Point" in error for error in errors))

    def test_uncontracted_black_box_is_rejected(self) -> None:
        broken = deepcopy(self.contracts[0])
        broken["black_boxes"] = ["bb-does-not-exist"]
        errors = validator.validate_contract(broken, self.manifest, Path("00-production-fixture.json"))
        self.assertTrue(any("unknown black-box" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

