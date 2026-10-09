"""Validate and package the SLE textbook authoring contract using only stdlib."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "sle-critical-phenomena"
AUTHORING = BOOK / "authoring"
SPEC_PATH = AUTHORING / "production.json"
CONTRACT_DIR = AUTHORING / "contracts"
SHORTCUT_PHRASES = ("明らか", "容易", "自明", "よく知られている", "one can show", "it is clear")
REQUIRED_SPEC_KEYS = {
    "schema_version", "book", "scope", "proof_depth_policy", "status_vocabulary",
    "normalizations", "domain_conventions", "terminology", "convergence_topologies",
    "prerequisites", "theorems", "black_boxes", "correspondences", "sources",
    "figures", "simulation_policy", "curriculum", "quality_gates", "audit_provenance",
}
REQUIRED_CONTRACT_KEYS = {
    "chapter_id", "source", "central_question", "reader_starting_state",
    "mathematical_prerequisites", "pedagogical_prerequisites", "previous_connection",
    "failed_approach", "new_concepts", "derivations", "results", "proof_depth",
    "black_boxes", "reader_stop_points", "required_bridges", "figures", "sources",
    "next_question", "quality_budget",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def duplicate_ids(items: list[dict], key: str = "id") -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = item.get(key)
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    return duplicates


def bib_keys() -> set[str]:
    text = (BOOK / "references.bib").read_text(encoding="utf-8")
    return set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", text))


def qmd_citations(text: str) -> set[str]:
    labels = set(re.findall(r"@([A-Za-z][A-Za-z0-9_:-]+)", text))
    return {label for label in labels if not label.startswith(("eq-", "fig-", "tbl-", "sec-"))}


def validate_contract(contract_path: Path, spec: dict, errors: list[str], warnings: list[str]) -> None:
    contract = load_json(contract_path)
    missing = REQUIRED_CONTRACT_KEYS - set(contract)
    extra = set(contract) - REQUIRED_CONTRACT_KEYS
    if missing:
        errors.append(f"{contract_path.relative_to(ROOT)}: missing keys {sorted(missing)}")
    if extra:
        errors.append(f"{contract_path.relative_to(ROOT)}: unknown keys {sorted(extra)}")
    if missing:
        return

    if not re.fullmatch(r"(?:ch|app|fixture)-\d{2}", contract["chapter_id"]):
        errors.append(f"{contract_path.relative_to(ROOT)}: invalid chapter_id")
    if contract["proof_depth"] not in spec["proof_depth_policy"]:
        errors.append(f"{contract_path.relative_to(ROOT)}: unknown proof depth")
    if len(contract["required_bridges"]) < 2:
        errors.append(f"{contract_path.relative_to(ROOT)}: at least two bridges are required")

    source_ids = {item["id"] for item in spec["sources"]}
    theorem_ids = {item["id"] for item in spec["theorems"]}
    black_box_ids = {item["id"] for item in spec["black_boxes"]}
    figure_ids = {item["id"] for item in spec["figures"]}
    for source_id in contract["sources"]:
        if source_id not in source_ids:
            errors.append(f"{contract_path.relative_to(ROOT)}: unknown source {source_id}")
    for black_box_id in contract["black_boxes"]:
        if black_box_id not in black_box_ids:
            errors.append(f"{contract_path.relative_to(ROOT)}: unknown black box {black_box_id}")
    for figure_id in contract["figures"]:
        if figure_id not in figure_ids:
            errors.append(f"{contract_path.relative_to(ROOT)}: unknown figure {figure_id}")

    concept_ids = set()
    for concept in contract["new_concepts"]:
        required = {"id", "need", "introduced_after"}
        if set(concept) != required or len(concept.get("need", "")) < 12:
            errors.append(f"{contract_path.relative_to(ROOT)}: incomplete concept motivation")
        if concept.get("id") in concept_ids:
            errors.append(f"{contract_path.relative_to(ROOT)}: duplicate concept {concept.get('id')}")
        concept_ids.add(concept.get("id"))

    for derivation in contract["derivations"]:
        required = {"id", "inputs", "assumptions", "steps_promised", "sanity_check"}
        if set(derivation) != required or not derivation.get("inputs") or derivation.get("steps_promised", 0) < 2:
            errors.append(f"{contract_path.relative_to(ROOT)}: incomplete derivation contract")

    for result in contract["results"]:
        if result.get("status") not in spec["status_vocabulary"]:
            errors.append(f"{contract_path.relative_to(ROOT)}: unknown status {result.get('status')}")
        theorem_id = result.get("theorem_id")
        if theorem_id is not None and theorem_id not in theorem_ids:
            errors.append(f"{contract_path.relative_to(ROOT)}: unknown theorem {theorem_id}")

    unresolved = [p for p in contract["reader_stop_points"] if p.get("resolution") == "unresolved"]
    if unresolved:
        errors.append(f"{contract_path.relative_to(ROOT)}: unresolved Reader Stop-Points remain")
    valid_resolutions = {"body", "appendix", "black_box", "unresolved"}
    for point in contract["reader_stop_points"]:
        if set(point) != {"question", "resolution", "location"} or point.get("resolution") not in valid_resolutions:
            errors.append(f"{contract_path.relative_to(ROOT)}: invalid Reader Stop-Point")

    budget = contract["quality_budget"]
    if set(budget) != {"motivations", "worked_derivations", "interpretations", "explicit_limits"}:
        errors.append(f"{contract_path.relative_to(ROOT)}: invalid quality budget")
    elif any(not isinstance(value, int) or value < 1 for value in budget.values()):
        errors.append(f"{contract_path.relative_to(ROOT)}: quality budget cannot be zero")

    source_path = BOOK / contract["source"]
    if not source_path.is_file():
        errors.append(f"{contract_path.relative_to(ROOT)}: missing QMD {contract['source']}")
        return
    text = source_path.read_text(encoding="utf-8")
    relative_contract = contract_path.relative_to(BOOK).as_posix()
    if f"<!-- contract: {relative_contract} -->" not in text:
        errors.append(f"{source_path.relative_to(ROOT)}: contract backlink is missing")
    if contract["chapter_id"].startswith("fixture-") and "<!-- synthetic-fixture: true -->" not in text:
        errors.append(f"{source_path.relative_to(ROOT)}: fixture marker is missing")
    for phrase in SHORTCUT_PHRASES:
        if phrase.casefold() in text.casefold():
            errors.append(f"{source_path.relative_to(ROOT)}: explanation shortcut phrase '{phrase}'")
    for citation in qmd_citations(text):
        if citation not in bib_keys():
            errors.append(f"{source_path.relative_to(ROOT)}: unknown citation @{citation}")
    if text.count("STATUS:") < 2:
        errors.append(f"{source_path.relative_to(ROOT)}: theorem/assumption status is not visible enough")
    if "証明していない" not in text:
        warnings.append(f"{source_path.relative_to(ROOT)}: explicit limit section was not detected")


def validate() -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if not SPEC_PATH.is_file():
        return {"ok": False, "errors": ["production.json is missing"], "warnings": [], "metrics": {}}
    spec = load_json(SPEC_PATH)
    missing = REQUIRED_SPEC_KEYS - set(spec)
    if missing:
        errors.append(f"production.json: missing keys {sorted(missing)}")
    if spec.get("book", {}).get("stage") == "production-complete":
        if spec.get("book", {}).get("formal_prose_started") is not True:
            errors.append("production.json: completed production must contain formal prose")
    elif spec.get("book", {}).get("formal_prose_started") is not False:
        errors.append("production.json: bootstrap must not claim formal prose")

    for registry in ("normalizations", "domain_conventions", "prerequisites", "theorems", "black_boxes", "sources", "figures", "curriculum", "quality_gates"):
        duplicates = duplicate_ids(spec.get(registry, []))
        if duplicates:
            errors.append(f"production.json: duplicate ids in {registry}: {sorted(duplicates)}")

    source_ids = {item["id"] for item in spec.get("sources", [])}
    citation_keys = bib_keys() if (BOOK / "references.bib").is_file() else set()
    for source in spec.get("sources", []):
        if source.get("citation") not in citation_keys:
            errors.append(f"production.json: BibTeX key missing for source {source.get('id')}")
    for theorem in spec.get("theorems", []):
        if theorem.get("depth") not in spec.get("proof_depth_policy", {}):
            errors.append(f"production.json: theorem {theorem.get('id')} has invalid depth")
        if theorem.get("status") not in spec.get("status_vocabulary", []):
            errors.append(f"production.json: theorem {theorem.get('id')} has invalid status")
        for source_id in theorem.get("sources", []):
            if source_id not in source_ids:
                errors.append(f"production.json: theorem {theorem.get('id')} references {source_id}")
    for black_box in spec.get("black_boxes", []):
        if black_box.get("source") not in source_ids:
            errors.append(f"production.json: black box {black_box.get('id')} has unknown source")
        if not all(black_box.get(field) for field in ("input", "output", "difficulty", "used_by")):
            errors.append(f"production.json: black box {black_box.get('id')} lacks its teaching contract")
    for item in spec.get("correspondences", []):
        if item.get("source") not in source_ids:
            errors.append(f"production.json: correspondence {item.get('model')} has unknown source")

    curriculum = spec.get("curriculum", [])
    curriculum_ids = {item["id"] for item in curriculum}
    prerequisite_ids = {item["id"] for item in spec.get("prerequisites", [])}
    for index, chapter in enumerate(curriculum):
        for dependency in chapter.get("math_dependencies", []) + chapter.get("pedagogical_dependencies", []):
            if dependency not in curriculum_ids | prerequisite_ids:
                errors.append(f"production.json: {chapter.get('id')} has unknown dependency {dependency}")
        if index and curriculum[index - 1]["exit_question"] != chapter["entry_question"]:
            errors.append(f"production.json: question chain breaks before {chapter.get('id')}")
    if len(curriculum) != 18:
        errors.append(f"production.json: expected 18 chapters, found {len(curriculum)}")

    normalization_text = "\n".join(item.get("statement", "") for item in spec.get("normalizations", []))
    for invariant in ("2t/z", "hcap(K_t)=2t", "1+4/kappa", "min(2,1+kappa/8)", "(3kappa-8)(6-kappa)"):
        if invariant not in normalization_text:
            errors.append(f"production.json: missing SLE invariant {invariant}")
    if "U_t=sqrt(kappa) B_t" not in normalization_text:
        errors.append("production.json: Brown driving normalization is missing")

    for figure in spec.get("figures", []):
        for field in ("objective", "type", "generator", "asset", "alt", "mobile", "dark_mode", "status"):
            if not figure.get(field):
                errors.append(f"production.json: figure {figure.get('id')} lacks {field}")
        if figure.get("status") == "implemented":
            asset = BOOK / figure["asset"]
            if not asset.is_file() or asset.stat().st_size == 0:
                errors.append(f"production.json: implemented figure missing: {figure['asset']}")
            fallback = figure.get("print_fallback")
            if fallback and not (BOOK / fallback).is_file():
                errors.append(f"production.json: print fallback missing: {fallback}")

    for provenance in spec.get("audit_provenance", []):
        if provenance.get("sha256") in (None, "", "pending"):
            errors.append(f"production.json: audit hash missing for {provenance.get('file')}")

    quarto_config = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    portal = (ROOT / "index.qmd").read_text(encoding="utf-8")
    if '"sle-critical-phenomena/**/*.qmd"' not in quarto_config:
        errors.append("_quarto.yml: SLE render glob is missing")
    if "id: sle-critical-phenomena" not in quarto_config:
        errors.append("_quarto.yml: SLE sidebar is missing")
    if "sle-critical-phenomena/" not in portal:
        errors.append("index.qmd: SLE portal card is missing")
    custom_css = (ROOT / "shared" / "styles" / "custom.css").read_text(encoding="utf-8")
    for css_contract in (".math.display", "overflow-x: auto", "@media (max-width: 991.98px)", "color-scheme: dark"):
        if css_contract not in custom_css:
            errors.append(f"shared/styles/custom.css: missing rendering contract {css_contract}")

    contract_paths = sorted(CONTRACT_DIR.glob("*.json"))
    if not contract_paths:
        errors.append("authoring/contracts: at least one contract fixture is required")
    for contract_path in contract_paths:
        validate_contract(contract_path, spec, errors, warnings)
    if spec.get("book", {}).get("stage") == "production-complete":
        formal_contracts = [
            load_json(path) for path in contract_paths
            if load_json(path).get("chapter_id", "").startswith("ch-")
        ]
        formal_ids = {contract["chapter_id"] for contract in formal_contracts}
        curriculum_ids = {chapter["id"] for chapter in curriculum}
        if formal_ids != curriculum_ids:
            errors.append(
                "authoring/contracts: formal chapter contracts do not match curriculum: "
                + f"missing={sorted(curriculum_ids - formal_ids)}, extra={sorted(formal_ids - curriculum_ids)}"
            )

    metrics = {
        "chapters": len(curriculum),
        "theorems": len(spec.get("theorems", [])),
        "black_boxes": len(spec.get("black_boxes", [])),
        "sources": len(spec.get("sources", [])),
        "figures": len(spec.get("figures", [])),
        "contracts": len(contract_paths),
        "question_bridges": max(0, len(curriculum) - 1),
    }
    return {"ok": not errors, "errors": errors, "warnings": warnings, "metrics": metrics}


def find_contract(chapter_id: str) -> tuple[Path, dict]:
    for path in CONTRACT_DIR.glob("*.json"):
        contract = load_json(path)
        if contract.get("chapter_id") == chapter_id:
            return path, contract
    raise SystemExit(f"Unknown chapter contract: {chapter_id}")


def write_output(path: Path, content: str) -> None:
    output = path if path.is_absolute() else ROOT / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")
    print(output)


def context_markdown(chapter_id: str) -> str:
    _, contract = find_contract(chapter_id)
    spec = load_json(SPEC_PATH)
    figure_ids = set(contract["figures"])
    source_ids = set(contract["sources"])
    black_box_ids = set(contract["black_boxes"])
    relevant = {
        "global": spec["book"],
        "scope": spec["scope"],
        "proof_depth_policy": spec["proof_depth_policy"],
        "normalizations": spec["normalizations"],
        "domain_conventions": spec["domain_conventions"],
        "terminology": spec["terminology"],
        "contract": contract,
        "black_boxes": [item for item in spec["black_boxes"] if item["id"] in black_box_ids],
        "figures": [item for item in spec["figures"] if item["id"] in figure_ids],
        "sources": [item for item in spec["sources"] if item["id"] in source_ids],
        "review_order": [gate["name"] for gate in spec["quality_gates"]],
    }
    return "# Authoring context: " + chapter_id + "\n\n```json\n" + json.dumps(relevant, ensure_ascii=False, indent=2) + "\n```\n"


def review_markdown(chapter_id: str) -> str:
    _, contract = find_contract(chapter_id)
    stop_points = "\n".join(
        f"- [ ] {item['question']} → {item['resolution']} / {item['location']}"
        for item in contract["reader_stop_points"]
    )
    return f"""# Review sheet: {chapter_id}

## 1. Missing Explanation First

- [ ] motivation
- [ ] bridge
- [ ] derivation and allowed operations
- [ ] assumption and definition
- [ ] distinction and interpretation
- [ ] example or counterexample
- [ ] proof idea or black-box contract
- [ ] previous/next chapter connection

## 2. Reader Stop-Points

{stop_points}

## 3. Mathematics

- [ ] Normalization, signs, coefficients, boundary cases
- [ ] Every claim has an epistemic status
- [ ] curve / trace / hull / driving object are not conflated
- [ ] classification and lattice convergence are separated

## 4. Continuity and sources

- [ ] Previous connection: {contract['previous_connection']}
- [ ] Next question: {contract['next_question']}
- [ ] Deep claims resolve to registered primary or standard sources

## 5. Rendering

- [ ] Desktop dark mode
- [ ] 375px viewport and math horizontal scroll
- [ ] Static figure and animation fallback
- [ ] PDF equations, references, captions, and links

## Gate 7

- Reviewer:
- Date:
- Decision: PASS / REVISE / FAIL
- Evidence:
"""


def print_report(report: dict) -> None:
    print(json.dumps(report, ensure_ascii=False, indent=2))


def create_audit_bundle(output: Path) -> None:
    report = validate()
    if not report["ok"]:
        print_report(report)
        raise SystemExit(1)
    target = output if output.is_absolute() else ROOT / output
    try:
        target.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit("Audit output must remain inside the repository") from exc
    if target.exists():
        raise SystemExit(f"Audit output already exists: {target}")
    target.mkdir(parents=True)
    shutil.copy2(SPEC_PATH, target / "production.json")
    shutil.copy2(AUTHORING / "chapter-contract.schema.json", target / "chapter-contract.schema.json")
    shutil.copytree(CONTRACT_DIR, target / "contracts")
    (target / "validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    tracked = [
        path for path in BOOK.rglob("*") if path.is_file()
    ] + [ROOT / "_quarto.yml", ROOT / "index.qmd", ROOT / "shared" / "styles" / "custom.css"]
    hashes = {
        path.relative_to(ROOT).as_posix(): sha256(path)
        for path in sorted(set(tracked))
        if target not in path.parents
    }
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "book_id": "sle-critical-phenomena",
        "gate_7": "requires independent human sign-off",
        "files": hashes,
    }
    (target / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(target)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    context_parser = subparsers.add_parser("context")
    context_parser.add_argument("chapter_id")
    context_parser.add_argument("--output", type=Path, required=True)
    review_parser = subparsers.add_parser("review")
    review_parser.add_argument("chapter_id")
    review_parser.add_argument("--output", type=Path, required=True)
    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "validate":
        report = validate()
        print_report(report)
        raise SystemExit(0 if report["ok"] else 1)
    if args.command == "context":
        write_output(args.output, context_markdown(args.chapter_id))
        return
    if args.command == "review":
        write_output(args.output, review_markdown(args.chapter_id))
        return
    if args.command == "audit":
        create_audit_bundle(args.output)


if __name__ == "__main__":
    main()
