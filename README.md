# Taglish Corpus

Taglish compound words (a Tagalog affix on an English or other foreign root) spelled by
the KWF rules and cross-checked against the validators' gold standard. Built from the
**Taglish Compound Corpus** tab of the CA-Spell sheet (Google Sheets ID
`1gGco3XDYv_wElCWL-UnRG24AuL4a-N_cB_sP8AnYZHQ`, tab gid `258714167`), after every row was
reviewed and checked against the sheet's **Validator View** tab. Snapshot taken 2026-11-27.

## Files

| File | Contents |
|---|---|
| `taglish_corpus.txt` | The corpus: 1,548 standardized entries, one per line, A–Z. Entries the validators wrote as two words keep the space (`nag-back up`). |
| `taglish_tokens.txt` | The entries cut to the Taglish word itself (`nag-back`), one per line. Use this as a spell-checker word list. |
| `taglish_corpus.csv` | Each entry with total frequency, affix, root word, morphological pattern, aspect/POS, KWF status, the KWF basis, and the source spellings merged into it. Sorted by frequency. |
| `variant_map.csv` | 307 source spellings that needed fixing, mapped to their entry (`nagreply` → `nag-reply`, `nag-backup` → `nag-back up`, `tinry` → `ni-try`). Useful for spell-check suggestions. |
| `excluded.csv` | 17 rows left out: 11 with a Tagalog root, 6 numerals. |
| `taglish_sentences.txt` | The sentence corpus: 588 gold-standard sentences from the 60% corpus partition, one per line. |
| `taglish_sentences.csv` | All 591 sentences of the partition with sentence ID, gold sentence, where the gold form comes from, the original sentence, the validators' verdicts and remarks, and the detected compound words. |
| `data/*.csv` | Snapshots of the three sheet tabs the files are built from: Taglish Compound Corpus, Processed Sentences, Validator View. |
| `build_corpus.py` | Rebuilds every file above from the snapshots. |

Rebuild after editing the sheet (standard-library Python, no installs):

```bash
python build_corpus.py --download   # fetch the sheet tab, then build
python build_corpus.py              # build from the saved snapshot
```

The build stops if any row in the sheet still has a blank **Corpus Inclusion**.

## Sentence corpus

The Processed Sentences tab splits the 985 eligible sentences 60/30/10. The sentence
corpus is the **60% - Correct Taglish Corpus** partition (591 sentences), each in its
gold-standard form from the Validator View:

- **Validator revision** (208): the validators' revised sentence, e.g.
  *Natry mo na ba…* → *Na-try mo na ba…*
- **Original** (380): sentences the validators marked Acceptable, kept as written.
- **Pending** (3), left out of `taglish_sentences.txt` until the Validator View has a
  complete revision:
  - S0125: the revision column holds only "ang cellphone";
  - S0249: Needs Revision, no revision; the remark says *Na-update* is possibly meant;
  - S0342: Needs Revision, no revision or remark (orthography marked Correct).

The 300 Testing Data and 94 Dev Validation sentences are deliberately not in the
sentence corpus, so CA-Spell is never evaluated on sentences it was built from.

The gold sentences are the validators' text, so a few words differ from the word list
where the corpus convention was kept (e.g. *tinry* in S0002, `ni-try` in the word list).

## Validator View cross-check

The Validator View holds the lead evaluators' verdict on each of the 985 sentences: the
KWF orthography of its compounds, a gold-standard sentence, and remarks such as
`nag-backup → nag-back up`. Every corpus entry was checked against it:

1. **A validator fix wins** (281 rows): `nag-backup` → `nag-back up`,
   `magcocolor` → `magko-color`, `na-cancelled` → `na-cancel`, `kinancel` → `ni-cancel`.
2. **A word the validators accepted as written keeps that spelling** (`na-scared`,
   `nag-silog`), and the entry is the word itself, not a longer phrase (`nag-cash`, not
   `nag-cash in`; the phrase is noted in column J of the sheet).
3. **The corpus convention is kept** where the validators deferred a form or accepted it
   as written but the corpus view had already decided otherwise (39 entries):
   - infixed English roots stay `ni-` + root (`tinry` → `ni-try`, `chineck` → `ni-check`).
     The validators asked for a reference spelling first and themselves used this
     convention for `kinancel` → `ni-cancel` "alinsunod sa convention ng corpus";
   - `ie-evaluate`, `ii-implement`, `io-organize`, `drawing-an`, `in-apply-an`,
     `in-configure` keep the corpus view's earlier entries;
   - flagged for the validators: `naghost` → `nag-ghost`, `mag-eenjoy` → `mag-e-enjoy`,
     `mag-gro-grocery` → `maggro-grocery`, `na-eksayt` → `naeksayt`, `videohan` →
     `video-han`, and the infixed `tinest`, `tinext`, `tinransfer`, `tinype`, `sinave`,
     `sineason`, `sinimulate`, `pinush`, `minodify`. The validators accepted these as
     written, but their own fixes elsewhere (`na-eexperience` → `na-e-experience`,
     `mag-seselpon` → `magseselpon`, `nagreply` → `nag-reply`) follow the convention.

Column J of the sheet cites the validator sentence behind each fix or convention
(e.g. *Validator View fix (S0058)*).

## KWF rules applied

From the *Manwal sa Masinop na Pagsulat* (KWF):

- **11.3 / 12.40.** A hyphen separates a Tagalog affix from a foreign word kept in its
  original spelling (*mag-shake, nag-makeup, pa-cute, maki-computer*) and from a proper
  noun, which keeps its capital (*pa-Mandaluyong, naka-Gucci*). So `nagreply`,
  `nag reply` → `nag-reply`, and `nag-gcash` → `nag-GCash`.
- **11.3.** A loanword respelled in Filipino is written solid (*pakyut, ipakrimeyt*):
  `mag-seselpon` → `magseselpon`.
- **11.3.** A consonant-final syllable before a vowel takes a hyphen (*mag-isa*):
  `nag-a-analyze`, `mag-e-exam`, and, as the validators wrote it, `na-e-experience`.

KWF has no rule for the cases below; the corpus and validator conventions are used:

- **-in- inside an English root** is written `ni-` + hyphen (`ni-try`). With
  reduplication the infixed syllable is kept (`dine-define`).
- **Reduplication** joins the copied syllable to the affix, hyphen before the root, with
  the syllable spelled as the validators wrote it (`nagte-text`, `magko-color`,
  `nagfi-freeze`).
- **A Tagalog suffix on an English root** follows a hyphen: `ni-react-an`, `video-han`.
- **English -ed** is dropped where it repeats the aspect the affix marks
  (`na-cancelled` → `na-cancel`) and kept where the validators accepted it
  (`na-scared`, `na-touched`).
- **English phrasal verbs** are written as two words, as the validators did
  (`nag-log in`, `na-burn out`).

## Sheet columns

| Column | Values |
|---|---|
| KWF Orthography Status | **Standard (KWF-Compliant)**: the source spelling already follows the rules (1,282 rows). **Needs Standardization**: it breaks one, and the entry shows the fix (258). **Non-Standard / Informal**: a pattern KWF does not cover (infix inside an English root, English root + suffix, colloquial *nakaka-*), spelled by the conventions above (49). **Exclude (Not Taglish)** (17). |
| Corpus Inclusion | Include in Corpus (1,589), Exclude - Pure Tagalog (11), Exclude - Numeral (6). No row is pending. |
| Aspect / POS Trigger | By affix: *i-, mag-, ma-, pa-, paki-, maka-* → VERB-CONTEMPLATED / IMPERATIVE; with reduplication → VERB-FUTURE (Contemplated); *nag-, um-, nagpa-, napa-* → VERB-PAST (Completed); *na-, ni-, in-, pina-* → VERB-PAST (Passive/Completed); *nag-, na-, ni-* with reduplication, *ina-, ine-* → VERB-PRESENT (Progressive); *pag-, ka-* → NOUN / VERB-NOMINAL; *naka-, napaka-, pang-, nakaka-* → ADJ / STATIVE. |
| KWF Basis / Notes | The rule and any fix behind each row's entry, the multiword expression the word belongs to, and the Validator View sentence behind a fix or convention. |

## Counts

- Sheet rows: 1,606 compounds, 1,831 occurrences
- Included: 1,589 rows → 1,548 entries (1,813 occurrences). Spellings that standardize
  to the same entry are merged and their frequencies added (`nag-reply` + `nagreply`).
- Excluded: 17 rows. Pending review: 0.

Files are UTF-8. The CSVs include a BOM so Excel opens them correctly.
