"""Build the Taglish corpus from the CA-Spell "Taglish Compound Corpus" sheet.

    python build_corpus.py              # build from data/taglish_compound_corpus_sheet.csv
    python build_corpus.py --download   # refresh that snapshot from Google Sheets first

Every row of the sheet must already be reviewed (no blank "Corpus Inclusion");
the build stops otherwise. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import sys
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "data" / "taglish_compound_corpus_sheet.csv"
SHEET_URL = ("https://docs.google.com/spreadsheets/d/1gGco3XDYv_wElCWL-UnRG24AuL4a-N_cB_sP8AnYZHQ"
             "/export?format=csv&gid=258714167")

COLUMNS = ["source_form", "frequency", "affix", "root_word", "morphological_pattern",
           "aspect_pos", "kwf_status", "corpus_entry", "inclusion", "kwf_basis"]
INCLUDE = "Include in Corpus"
STANDARD = "Standard (KWF-Compliant)"


def load(path: Path) -> list[dict]:
    rows = list(csv.reader(path.open(encoding="utf-8-sig")))
    header = next(i for i, r in enumerate(rows) if r and r[0].startswith("Compound Word"))
    out = []
    for n, r in enumerate(rows[header + 1:], start=header + 2):
        if not any(c.strip() for c in r):
            continue
        r = (r + [""] * len(COLUMNS))[:len(COLUMNS)]
        row = dict(zip(COLUMNS, (c.strip() for c in r)))
        row["sheet_row"] = n
        row["frequency"] = int(row["frequency"].replace(",", "") or 0)
        out.append(row)
    return out


def write_csv(name: str, fields: list[str], items: list[dict]) -> None:
    with (ROOT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(items)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--download", action="store_true", help="refresh the sheet snapshot first")
    args = ap.parse_args()
    if args.download:
        SNAPSHOT.parent.mkdir(exist_ok=True)
        with urllib.request.urlopen(SHEET_URL, timeout=60) as r:
            SNAPSHOT.write_bytes(r.read())
        print(f"downloaded {SNAPSHOT.relative_to(ROOT)}")

    rows = load(SNAPSHOT)
    pending = [r for r in rows if not r["inclusion"]]
    if pending:
        print(f"{len(pending)} row(s) still pending review, e.g. sheet row {pending[0]['sheet_row']} "
              f"({pending[0]['source_form']}). Review them in the sheet first.", file=sys.stderr)
        return 1
    included = [r for r in rows if r["inclusion"] == INCLUDE]
    excluded = [r for r in rows if r["inclusion"] != INCLUDE]

    # One corpus entry per standardized form; spellings that standardize to the
    # same entry are merged and their frequencies added.
    groups: dict[str, list[dict]] = {}
    for r in included:
        groups.setdefault(r["corpus_entry"].lower(), []).append(r)
    corpus = []
    for members in groups.values():
        main_row = sorted(members, key=lambda r: (r["kwf_status"] != STANDARD, -r["frequency"],
                                                  r["sheet_row"]))[0]
        corpus.append({
            **main_row,
            "total_frequency": sum(r["frequency"] for r in members),
            "source_forms": "; ".join(f"{r['source_form']} ({r['frequency']})" for r in
                                      sorted(members, key=lambda r: (-r["frequency"], r["source_form"]))),
        })
    corpus.sort(key=lambda c: (-c["total_frequency"], c["corpus_entry"].lower()))

    entries = sorted((c["corpus_entry"] for c in corpus), key=str.lower)
    (ROOT / "taglish_corpus.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")

    # Token list for spell checkers: the Taglish word itself (first word of a
    # multiword entry such as "nag-dark mode").
    tokens = sorted({e.split(" ")[0].rstrip(".") for e in entries}, key=str.lower)
    (ROOT / "taglish_tokens.txt").write_text("\n".join(tokens) + "\n", encoding="utf-8")

    write_csv("taglish_corpus.csv",
              ["corpus_entry", "total_frequency", "affix", "root_word", "morphological_pattern",
               "aspect_pos", "kwf_status", "kwf_basis", "source_forms"], corpus)

    variants = sorted((r for r in included if r["kwf_status"] != STANDARD),
                      key=lambda r: r["source_form"].lower())
    write_csv("variant_map.csv", ["source_form", "corpus_entry", "kwf_status", "frequency",
                                  "kwf_basis"], variants)
    write_csv("excluded.csv", ["source_form", "frequency", "inclusion", "corpus_entry", "kwf_basis"],
              sorted(excluded, key=lambda r: (r["inclusion"], r["source_form"])))

    status = Counter(r["kwf_status"] for r in rows)
    print(f"sheet rows {len(rows)} (occurrences {sum(r['frequency'] for r in rows)}), "
          f"included {len(included)}, excluded {len(excluded)}, pending 0")
    print(f"corpus entries {len(corpus)} (occurrences {sum(c['total_frequency'] for c in corpus)}), "
          f"tokens {len(tokens)}, variant spellings {len(variants)}")
    for k, v in status.most_common():
        print(f"  {k}: {v}")
    for k, v in Counter(r["inclusion"] for r in excluded).most_common():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
