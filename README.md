# Targeting Neuroimmune Interfaces in Depression with Engineered Autologous Immune Cells

Leon Sandler, Independent Researcher — sandler.leon@gmail.com

Conceptual figures, reference-verification code, and manuscript for
*"Targeting Neuroimmune Interfaces in Depression with Engineered Autologous
Immune Cells: A Falsifiable Preclinical Framework,"* prepared for submission to
Wiley's **Advanced Immunology**.

## Summary

This is a hypothesis paper, not a report of experimental results. It proposes
an immunotherapy design paradigm — engineered autologous immune cells directed
at the **CNS border compartments** (meningeal and dural sinus spaces, choroid
plexus) rather than at the brain parenchyma — and specifies the immunological
mechanism such a framework would require, the evidence status of each link in
that chain, and the preclinical programme capable of refuting it.

Two points of scope are stated explicitly in the manuscript and repeated here:

- **Dopamine is not proposed as a delivery mechanism.** Dopamine does not cross
  the blood–brain barrier in physiologically meaningful quantities, and
  peripherally produced catecholamines have no established route to central
  dopaminergic circuits. The framework acts through immune signalling at CNS
  borders, not neurotransmitter delivery. Engineered immune-cell dopaminergic
  signalling appears only as an explicitly-labelled Tier 3 exploratory module.
- **No construct exists and no animal or human study has been performed.** The
  four depression-associated phenotypes discussed (postpartum, chronic
  treatment-resistant, post-deployment, perimenopausal) are treated as *test
  cases* for whether partially overlapping immune states can be identified and
  manipulated — not as conditions asserted to share one common signature.

## Contents

```
manuscript/   Neuroimmune_Interfaces_Depression_v3.docx   (CC BY 4.0)
code/         generate_figures.py        (MIT) — regenerates Figures 1–2
              figure1_framework.png      framework with evidence-status colour coding
              figure2_falsification.png  falsification decision architecture
              verify_references.py       (MIT) — Crossref reference verification
```

### Figures

`generate_figures.py` regenerates both manuscript figures. They are **schematic
diagrams, not data plots** — no simulation or dataset underlies them. The script
exists so the figures are reproducible and version-controlled rather than static
images.

```bash
pip install matplotlib
python code/generate_figures.py
```

### Reference verification

`verify_references.py` checks every reference in the manuscript against the
[Crossref](https://www.crossref.org/) REST API, comparing title-word overlap,
year, journal, volume, and first page against what is cited, and reports any
mismatch. It was used to audit all 68 references prior to submission.

```bash
pip install requests python-docx
python code/verify_references.py
```

Note that Crossref reports the *online-first* date in its `issued` field, so
references citing a later print-issue year are flagged for review rather than
treated as errors; each such flag was checked manually against
`published-print`.

## License

- Manuscript text and figures: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see `manuscript/LICENSE`
- Code: MIT — see `LICENSE` at repository root
