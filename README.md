# Taglish Corpus List

Built from the **CA-Spell: Taglish Compound Corpus & Frequency Directory** sheet
(Google Sheets ID `1gGco3XDYv_wElCWL-UnRG24AuL4a-N_cB_sP8AnYZHQ`, tab gid `258714167`),
exported 2026-11-26.

## Files

| File | Contents |
|---|---|
| `taglish_corpus.txt` | The corpus list: 283 standardized Taglish entries, one per line, A–Z. |
| `taglish_corpus.csv` | The same 283 entries with total frequency, affix, root word, morphological pattern, aspect/POS, KWF orthography status and the source spellings merged into each entry. Sorted by frequency. |
| `variant_map.csv` | 68 non-standard or variant spellings mapped to their standardized entry (e.g. `nagreply` → `nag-reply`, `tinry` → `ni-try`). Useful for spell-check suggestions. |
| `pending_review.csv` | 1,262 compounds the sheet marks as still pending review (all frequency 1). They are **not** in the corpus list. |
| `excluded.csv` | 1 entry excluded as pure Tagalog (`mag-isa`). |

## How the list was built

- Only rows marked **Include in Corpus** (292 rows) go into the corpus.
- The **Standardized Corpus Entry** column is used as the word. When several source
  spellings standardize to the same entry (e.g. `i-submit` and `issubmit`), they are
  merged into one entry and their frequencies are added together. This is why 292 rows
  become 283 entries.
- For merged entries, the metadata comes from the row already written in standard form.
- Entries are kept exactly as the sheet gives them. Nothing was respelled.

## Counts (match the sheet's summary)

- Total unique compounds: 1,555
- Total occurrences: 1,779
- Approved for corpus: 292 rows → 283 entries (515 occurrences)
- Pending review: 1,262
- Excluded: 1

Files are UTF-8. The CSVs include a BOM so Excel opens them correctly.
