# Taglish Corpus

Taglish compound words (a Tagalog affix on an English or other foreign root) spelled by
the KWF rules, built from the **Taglish Compound Corpus** tab of the CA-Spell sheet
(Google Sheets ID `1gGco3XDYv_wElCWL-UnRG24AuL4a-N_cB_sP8AnYZHQ`, tab gid `258714167`).
Snapshot taken 2026-11-27, after every row of the sheet was reviewed.

## Files

| File | Contents |
|---|---|
| `taglish_corpus.txt` | The corpus: 1,546 standardized entries, one per line, A–Z. Multiword roots keep their spaces (`nag-dark mode`). |
| `taglish_tokens.txt` | The same entries cut to the Taglish word itself (`nag-dark`), one per line. Use this as a spell-checker word list. |
| `taglish_corpus.csv` | Each entry with total frequency, affix, root word, morphological pattern, aspect/POS, KWF status, the KWF basis, and the source spellings merged into it. Sorted by frequency. |
| `variant_map.csv` | 299 source spellings that needed fixing, mapped to their entry (`nagreply` → `nag-reply`, `tinry` → `ni-try`, `na-cancelled` → `na-cancel`). Useful for spell-check suggestions. |
| `excluded.csv` | 17 rows left out: 11 with a Tagalog root, 6 numerals. |
| `data/taglish_compound_corpus_sheet.csv` | The sheet tab the files are built from. |
| `build_corpus.py` | Rebuilds every file above from the snapshot. |

Rebuild after editing the sheet (standard-library Python, no installs):

```bash
python build_corpus.py --download   # fetch the sheet tab, then build
python build_corpus.py              # build from the saved snapshot
```

The build stops if any row in the sheet still has a blank **Corpus Inclusion**.

## KWF rules applied

From the *Manwal sa Masinop na Pagsulat* (KWF):

- **11.3 / 12.40.** A hyphen separates a Tagalog affix from a foreign word kept in its
  original spelling (*mag-shake, nag-makeup, pa-cute, maki-computer*) and from a proper
  noun, which keeps its capital (*pa-Mandaluyong, naka-Gucci*). So `nagreply`,
  `nag reply` → `nag-reply`, and `nag-gcash` → `nag-GCash`.
- **11.3.** A loanword respelled in Filipino is written solid (*pakyut, ipakrimeyt*):
  `mag-seselpon` → `magseselpon`, `na-eksayt` → `naeksayt`.
- **11.3.** A consonant-final syllable before a vowel takes a hyphen (*mag-isa*):
  `nag-a-analyze`, `mag-e-exam`.

KWF has no rule for the cases below, so the sheet's existing conventions are used:

- **-in- inside an English root** is written `ni-` + hyphen: `tinry` → `ni-try`,
  `sinend` → `ni-send`. With reduplication the infixed syllable is kept: `dine-define`.
- **Reduplication** joins the copied syllable to the affix, hyphen before the root:
  `nagte-text`, `magco-color`, `nag-u-update`. The syllable is kept as the respondent
  spelled it; only a missing vowel is restored (`nag-ccheck` → `nagche-check`).
- **A Tagalog suffix on an English root** follows a hyphen: `ni-react-an`, `video-han`.
- **English -ed** that repeats the aspect the affix already marks is dropped:
  `na-cancelled` → `na-cancel`. Adjectives stay as they are (`na-tired`, `na-outdated`).
- **Misspelled roots** are corrected: `na-dissapoint` → `na-disappoint`.
- **Multiword roots** cut off by the extraction are completed from the source sentence:
  `nag-dark` → `nag-dark mode`, `nag-q` → `nag-Q&A`, `pa-sta` → `pa-Sta. Mesa`.

## Sheet columns

| Column | Values |
|---|---|
| KWF Orthography Status | **Standard (KWF-Compliant)**: the source spelling already follows the rules (1,290 rows). **Needs Standardization**: it breaks one, and the entry shows the fix (250). **Non-Standard / Informal**: a pattern KWF does not cover (infix inside an English root, English root + suffix, colloquial *nakaka-*), spelled by the conventions above (49). **Exclude (Not Taglish)** (17). |
| Corpus Inclusion | Include in Corpus (1,589), Exclude - Pure Tagalog (11), Exclude - Numeral (6). No row is pending. |
| Aspect / POS Trigger | By affix: *i-, mag-, ma-, pa-, paki-, maka-* → VERB-CONTEMPLATED / IMPERATIVE; with reduplication → VERB-FUTURE (Contemplated); *nag-, um-, nagpa-, napa-* → VERB-PAST (Completed); *na-, ni-, in-, pina-* → VERB-PAST (Passive/Completed); *nag-, na-, ni-* with reduplication, *ina-, ine-* → VERB-PRESENT (Progressive); *pag-, ka-* → NOUN / VERB-NOMINAL; *naka-, napaka-, pang-, nakaka-* → ADJ / STATIVE. |
| KWF Basis / Notes | The rule and any fix behind each row's entry. |

## Counts

- Sheet rows: 1,606 compounds, 1,831 occurrences
- Included: 1,589 rows → 1,546 entries (1,813 occurrences). Spellings that standardize
  to the same entry are merged and their frequencies added (`nag-reply` + `nagreply`).
- Excluded: 17 rows. Pending review: 0.

Files are UTF-8. The CSVs include a BOM so Excel opens them correctly.
