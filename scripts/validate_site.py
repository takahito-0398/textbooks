from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}
SECRET_PATTERNS = [
    re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
    re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}'),
]
LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')

errors: list[str] = []

def is_external(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {'http', 'https', 'mailto'} or target.startswith('#')

for path in ROOT.rglob('*'):
    if any(part in {'.git', '.quarto', '_site', 'dist', 'tmp'} for part in path.parts) or path.is_dir():
        continue
    if path.name == 'quarto.zip':
        continue
    if path.suffix.lower() in {'.qmd', '.md', '.yml', '.yaml', '.css', '.scss', '.py'}:
        text = path.read_text(encoding='utf-8', errors='ignore')
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                errors.append(f'possible secret pattern in {path.relative_to(ROOT)}')
        for match in LINK_RE.finditer(text):
            raw = match.group(1).split()[0]
            if raw.startswith('\\'):
                continue
            target = raw.split('#', 1)[0]
            if not target or is_external(target):
                continue
            if target.startswith('/'):
                errors.append(f'root-relative local link in {path.relative_to(ROOT)}: {raw}')
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f'local link escapes repo in {path.relative_to(ROOT)}: {raw}')
                continue
            if candidate.suffix == '':
                qmd_candidate = candidate.with_suffix('.qmd')
                html_candidate = candidate.with_suffix('.html')
                if not candidate.exists() and not qmd_candidate.exists() and not html_candidate.exists():
                    errors.append(f'missing local link in {path.relative_to(ROOT)}: {raw}')
            elif not candidate.exists():
                errors.append(f'missing local link in {path.relative_to(ROOT)}: {raw}')
            elif candidate.suffix.lower() in IMAGE_EXTS and candidate.stat().st_size == 0:
                errors.append(f'empty image asset: {candidate.relative_to(ROOT)}')

if errors:
    print('Validation failed:')
    for err in errors:
        print(f'- {err}')
    sys.exit(1)
print('Validation passed: local links/assets and basic secret scan are clean.')
