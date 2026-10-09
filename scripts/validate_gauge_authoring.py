"""Validate the 4D gauge-theory authoring contracts and emit audit evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "gauge-theory-smooth-topology"
MANIFEST_PATH = BOOK / "production" / "manifest.json"
CONTRACT_DIR = BOOK / "contracts"
SCHEMA_PATH = BOOK / "authoring" / "chapter-contract.schema.json"
AUDIT_INGESTION_PATH = BOOK / "production" / "audit-ingestion.md"
FINAL_REPORT_PATH = BOOK / "production" / "PRODUCTION_BOOTSTRAP_REPORT.md"
REQUIRED_CONTRACT_FIELDS = {
    "chapter_id", "source", "central_question", "reader_starting_state",
    "prerequisites", "new_concepts", "main_derivations", "results",
    "proof_depth", "black_boxes", "rigor_statuses", "reader_stop_points",
    "required_bridges", "figures", "sources", "previous_connection",
    "next_question", "unresolved_stop_points",
}
STOP_RESOLUTIONS = {"body", "appendix", "black_box", "unresolved"}
RIGOR_STATUSES = {
    "definition", "theorem", "proposition", "lemma", "heuristic",
    "physical_intuition", "conjecture", "numerical_evidence",
    "expected_behavior", "open_problem", "black_box_theorem",
}
VAGUE_PHRASES = ("well known", "one can show", "よく知られている", "容易に分かる", "standard")
PLACEHOLDERS = re.compile(r"\b(?:TODO|TBD|FIXME)\b|要確認|後で書く", re.IGNORECASE)
CITATION_RE = re.compile(r"@([A-Za-z][A-Za-z0-9_:.+-]*)")
BIB_KEY_RE = re.compile(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", re.IGNORECASE)
QUARTO_XREF_PREFIXES = ("fig-", "eq-", "sec-", "tbl-", "lst-", "thm-", "lem-", "prp-", "cor-")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ids(items: list[dict]) -> set[str]:
    return {item["id"] for item in items}


def duplicate_ids(items: list[dict]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = item.get("id")
        if item_id in seen:
            duplicates.add(str(item_id))
        seen.add(item_id)
    return duplicates


def graph_has_cycle(nodes: list[str], edges: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dependency in edges.get(node, []):
            if visit(dependency):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    for key in ("book", "curriculum", "registries", "production_stop_conditions"):
        if key not in manifest:
            errors.append(f"manifest missing top-level key: {key}")
    if errors:
        return errors

    curriculum = manifest["curriculum"]
    chapter_ids = [chapter.get("id") for chapter in curriculum]
    chapter_id_set = set(chapter_ids)
    if len(chapter_ids) != len(chapter_id_set):
        errors.append("curriculum contains duplicate chapter ids")
    positions = {chapter_id: index for index, chapter_id in enumerate(chapter_ids)}
    for index, chapter in enumerate(curriculum):
        expected_previous = chapter_ids[index - 1] if index else None
        expected_next = chapter_ids[index + 1] if index + 1 < len(chapter_ids) else None
        if chapter.get("previous") != expected_previous:
            errors.append(f"{chapter['id']}: previous must be {expected_previous!r}")
        if chapter.get("next") != expected_next:
            errors.append(f"{chapter['id']}: next must be {expected_next!r}")
        for dependency_kind in ("mathematical_dependencies", "pedagogical_dependencies"):
            dependencies = chapter.get(dependency_kind, [])
            for dependency in dependencies:
                if dependency not in chapter_id_set:
                    errors.append(f"{chapter['id']}: unknown {dependency_kind} id {dependency}")
                elif positions[dependency] >= index:
                    errors.append(f"{chapter['id']}: {dependency_kind} must point backward: {dependency}")
        if not chapter.get("central_question", "").strip().endswith(("。", "？")):
            errors.append(f"{chapter['id']}: central_question must be a complete sentence")

    for dependency_kind in ("mathematical_dependencies", "pedagogical_dependencies"):
        edges = {chapter["id"]: chapter.get(dependency_kind, []) for chapter in curriculum}
        if graph_has_cycle(chapter_ids, edges):
            errors.append(f"curriculum {dependency_kind} contains a cycle")

    registries = manifest["registries"]
    required_registries = {
        "notation", "conventions", "assumptions", "sources", "theorems",
        "black_boxes", "figures", "reader_questions", "moduli_lifecycle", "quality_gates",
    }
    missing_registries = required_registries - set(registries)
    if missing_registries:
        errors.append(f"missing registries: {sorted(missing_registries)}")
        return errors

    for name in required_registries - {"moduli_lifecycle", "quality_gates"}:
        duplicates = duplicate_ids(registries[name])
        if duplicates:
            errors.append(f"{name} contains duplicate ids: {sorted(duplicates)}")

    assumption_ids = ids(registries["assumptions"])
    convention_ids = ids(registries["conventions"])
    source_ids = ids(registries["sources"])
    theorem_ids = ids(registries["theorems"])
    for theorem in registries["theorems"]:
        if theorem.get("proof_depth") not in manifest.get("proof_depth_levels", {}):
            errors.append(f"{theorem['id']}: invalid proof depth")
        for assumption in theorem.get("assumptions", []):
            if assumption not in assumption_ids | convention_ids:
                errors.append(f"{theorem['id']}: unknown assumption/convention {assumption}")
        for source in theorem.get("sources", []):
            if source not in source_ids:
                errors.append(f"{theorem['id']}: unknown source {source}")
        for chapter in theorem.get("used_by", []):
            if chapter not in chapter_id_set:
                errors.append(f"{theorem['id']}: unknown downstream chapter {chapter}")

    for black_box in registries["black_boxes"]:
        if black_box.get("theorem") not in theorem_ids:
            errors.append(f"{black_box['id']}: unknown theorem {black_box.get('theorem')}")
        for field in ("why_needed", "input", "output", "difficulty", "downstream"):
            if not black_box.get(field):
                errors.append(f"{black_box['id']}: missing black-box contract field {field}")

    for figure in registries["figures"]:
        for field in ("objective", "concept", "type", "generator", "license", "alt", "mobile", "dark_mode", "status"):
            if field not in figure or figure[field] in (None, ""):
                errors.append(f"{figure['id']}: missing figure field {field}")
        if figure.get("status") == "generated":
            asset = figure.get("asset")
            if not asset or not (BOOK / asset).is_file():
                errors.append(f"{figure['id']}: generated asset is missing: {asset}")

    expected_lifecycle = ["equation", "symmetry", "linearization", "complex", "index", "regularity", "orientation", "compactification", "count"]
    if registries["moduli_lifecycle"] != expected_lifecycle:
        errors.append("moduli lifecycle is incomplete or out of order")
    expected_gates = {"architecture", "mathematics", "explanation", "continuity", "sources", "rendering", "independent_audit"}
    if set(registries["quality_gates"]) != expected_gates:
        errors.append("quality gates must contain Gates 1-7 exactly")
    unresolved_stops = [item["id"] for item in manifest["production_stop_conditions"] if not item.get("resolved")]
    if unresolved_stops:
        errors.append(f"production stop conditions remain unresolved: {unresolved_stops}")
    return errors


def validate_contract(contract: dict, manifest: dict, path: Path) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_CONTRACT_FIELDS - set(contract)
    extra = set(contract) - REQUIRED_CONTRACT_FIELDS
    if missing:
        errors.append(f"{path.name}: missing fields {sorted(missing)}")
    if extra:
        errors.append(f"{path.name}: unexpected fields {sorted(extra)}")
    if missing:
        return errors

    registries = manifest["registries"]
    concept_ids = ids(registries["notation"]) | ids(registries["conventions"]) | ids(registries["assumptions"])
    theorem_ids = ids(registries["theorems"])
    black_box_ids = ids(registries["black_boxes"])
    figure_ids = ids(registries["figures"])
    source_ids = ids(registries["sources"])
    for field in ("prerequisites", "new_concepts"):
        for item in contract[field]:
            if item not in concept_ids:
                errors.append(f"{path.name}: unknown {field} id {item}")
    for item in contract["results"]:
        if item not in theorem_ids:
            errors.append(f"{path.name}: unknown theorem id {item}")
    for item in contract["black_boxes"]:
        if item not in black_box_ids:
            errors.append(f"{path.name}: unknown black-box id {item}")
    for item in contract["figures"]:
        if item not in figure_ids:
            errors.append(f"{path.name}: unknown figure id {item}")
    for item in contract["sources"]:
        if item not in source_ids:
            errors.append(f"{path.name}: unknown source id {item}")
    if contract["proof_depth"] not in manifest["proof_depth_levels"]:
        errors.append(f"{path.name}: invalid proof depth {contract['proof_depth']}")
    invalid_statuses = set(contract["rigor_statuses"]) - RIGOR_STATUSES
    if invalid_statuses:
        errors.append(f"{path.name}: invalid rigor statuses {sorted(invalid_statuses)}")
    if len(contract["required_bridges"]) < 2:
        errors.append(f"{path.name}: at least two bridges are required")
    if contract["unresolved_stop_points"]:
        errors.append(f"{path.name}: unresolved Reader Stop-Points remain")
    for stop_point in contract["reader_stop_points"]:
        missing_stop_fields = {"question", "resolution", "location"} - set(stop_point)
        if missing_stop_fields:
            errors.append(f"{path.name}: Reader Stop-Point missing {sorted(missing_stop_fields)}")
        elif stop_point["resolution"] not in STOP_RESOLUTIONS:
            errors.append(f"{path.name}: invalid Reader Stop-Point resolution")
        elif stop_point["resolution"] == "unresolved":
            errors.append(f"{path.name}: unresolved Reader Stop-Point: {stop_point['question']}")

    source_path = BOOK / contract["source"]
    if not source_path.is_file():
        errors.append(f"{path.name}: source does not exist: {contract['source']}")
        return errors
    text = source_path.read_text(encoding="utf-8")
    if f"<!-- contract: contracts/{path.name} -->" not in text:
        errors.append(f"{path.name}: source does not declare its contract")
    if PLACEHOLDERS.search(text):
        errors.append(f"{path.name}: source contains a placeholder marker")
    lower_text = text.lower()
    for phrase in VAGUE_PHRASES:
        if phrase.lower() in lower_text and "<!-- reviewed-vague -->" not in text:
            errors.append(f"{path.name}: unexplained vague phrase: {phrase}")
    return errors


def validate_citations(manifest: dict, contracts: list[dict]) -> list[str]:
    errors: list[str] = []
    bib_path = BOOK / "references.bib"
    bib_keys = set(BIB_KEY_RE.findall(bib_path.read_text(encoding="utf-8")))
    source_by_id = {source["id"]: source for source in manifest["registries"]["sources"]}
    for source in source_by_id.values():
        if source["citation_key"] not in bib_keys:
            errors.append(f"source {source['id']}: missing bibliography key {source['citation_key']}")
    for contract in contracts:
        text = (BOOK / contract["source"]).read_text(encoding="utf-8")
        cited = {key for key in CITATION_RE.findall(text) if not key.startswith(QUARTO_XREF_PREFIXES)}
        missing = cited - bib_keys
        if missing:
            errors.append(f"{contract['source']}: unknown citation keys {sorted(missing)}")
        declared_keys = {source_by_id[source_id]["citation_key"] for source_id in contract["sources"] if source_id in source_by_id}
        undeclared = cited - declared_keys
        if undeclared:
            errors.append(f"{contract['source']}: citations not declared by contract {sorted(undeclared)}")
    return errors


def validate_all(manifest: dict | None = None, contracts: list[dict] | None = None) -> list[str]:
    manifest = deepcopy(manifest) if manifest is not None else load_json(MANIFEST_PATH)
    contract_paths = sorted(CONTRACT_DIR.glob("*.json"))
    contracts = deepcopy(contracts) if contracts is not None else [load_json(path) for path in contract_paths]
    errors = validate_manifest(manifest)
    if contracts is not None:
        paths = contract_paths if len(contract_paths) == len(contracts) else [Path(f"contract-{index}.json") for index in range(len(contracts))]
        for contract, path in zip(contracts, paths):
            errors.extend(validate_contract(contract, manifest, path))
        errors.extend(validate_citations(manifest, contracts))
    if not SCHEMA_PATH.is_file():
        errors.append("chapter contract schema is missing")
    if not AUDIT_INGESTION_PATH.is_file():
        errors.append("audit ingestion report is missing")
    if not FINAL_REPORT_PATH.is_file():
        errors.append("production bootstrap final report is missing")
    return errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def write_audit_bundle(output_dir: Path, errors: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_paths = [MANIFEST_PATH, SCHEMA_PATH, AUDIT_INGESTION_PATH, FINAL_REPORT_PATH, *sorted(CONTRACT_DIR.glob("*.json"))]
    evidence = {str(path.relative_to(ROOT)): sha256(path) for path in evidence_paths}
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "book": "gauge-theory-smooth-topology",
        "validator": "scripts/validate_gauge_authoring.py",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "evidence_sha256": evidence,
    }
    (output_dir / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    snapshot = output_dir / "evidence"
    snapshot.mkdir(exist_ok=True)
    for path in evidence_paths:
        destination = snapshot / path.relative_to(BOOK)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-bundle", type=Path)
    args = parser.parse_args()
    errors = validate_all()
    if args.audit_bundle:
        write_audit_bundle(args.audit_bundle, errors)
    if errors:
        print("Gauge authoring validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("Gauge authoring validation passed: curriculum, registries, chapter contracts, citations, assets, and quality gates are consistent.")


if __name__ == "__main__":
    main()
