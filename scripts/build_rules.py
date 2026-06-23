from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


CATEGORIES = ("douyin", "doubao", "volcengine")
EXTRA_SUFFIXES = {"vlabstatic.com"}


def parse_file(path: Path, follow_includes: bool) -> tuple[set[str], set[str]]:
    suffixes: set[str] = set()
    exact: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        value = line.split()[0]
        if value.startswith("include:"):
            if follow_includes:
                raise ValueError(f"Unexpected include rule in {path.name}: {value}")
        elif value.startswith("full:"):
            exact.add(value.removeprefix("full:").lower())
        elif value.startswith("regexp:"):
            raise ValueError(f"Unsupported regexp rule: {value}")
        else:
            suffixes.add(value.lower())
    return suffixes, exact


def write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path, help="domain-list-community data directory")
    parser.add_argument("--repo", type=Path, help="domain-list-community repository")
    args = parser.parse_args()

    suffixes, exact = parse_file(args.data / "bytedance", follow_includes=False)
    for category in CATEGORIES:
        category_suffixes, category_exact = parse_file(
            args.data / category, follow_includes=True
        )
        suffixes |= category_suffixes
        exact |= category_exact
    suffixes |= EXTRA_SUFFIXES

    commit = "unknown"
    if args.repo:
        commit = subprocess.check_output(
            ["git", "-C", str(args.repo), "rev-parse", "HEAD"], text=True
        ).strip()

    total = len(suffixes) + len(exact)
    header = [
        "# NAME: ByteDanceCN",
        "# AUTHOR: DDcat2025",
        "# REPO: https://github.com/DDcat2025/douyin-bytedance-shadowrocket-rules",
        "# SOURCE: https://github.com/v2fly/domain-list-community",
        f"# SOURCE-COMMIT: {commit}",
        "# INCLUDED: bytedance-base, doubao, douyin, volcengine, jimeng dependencies",
        f"# DOMAIN-SUFFIX: {len(suffixes)}",
        f"# DOMAIN: {len(exact)}",
        f"# TOTAL: {total}",
    ]

    rules = (
        [f"DOMAIN-SUFFIX,{domain}" for domain in sorted(suffixes)]
        + [f"DOMAIN,{domain}" for domain in sorted(exact)]
    )
    shadow = Path("rule/Shadowrocket/ByteDanceCN")
    write(shadow / "ByteDanceCN.list", header + rules)
    write(
        shadow / "ByteDanceCN_Domain.list",
        header + [f".{domain}" for domain in sorted(suffixes | exact)],
    )
    write(
        Path("rule/Mihomo/ByteDanceCN/ByteDanceCN.yaml"),
        header + ["payload:"] + [f"  - {rule}" for rule in rules],
    )
    write(
        Path("data/bytedance-cn-domains.txt"),
        header + sorted(suffixes | exact),
    )


if __name__ == "__main__":
    main()

