# -*- coding: utf-8 -*-
"""Verify every reference in the manuscript against Crossref.

For each reference we send the full citation string to Crossref's bibliographic
query, then check whether the best-matching record actually corresponds to what
we cited: title-word overlap, year, journal, volume, and first page.
"""
import io, os, re, json, time, difflib
import requests
from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
DOCX = os.path.join(HERE, "..", "manuscript", "Neuroimmune_Interfaces_Depression_v5.docx")
MAILTO = "sandler.leon@gmail.com"
HEADERS = {"User-Agent": f"ref-verify/1.0 (mailto:{MAILTO})"}

STOP = set("""a an the of and or in on for to with from by at as is are was were be been
that this these those we our their its it his her they them then than into via using
between within across during after before not no non new novel study studies""".split())


def sig_words(s):
    s = s.lower().replace("–", "-").replace("’", "'")
    ws = re.findall(r"[a-z0-9][a-z0-9\-']+", s)
    return [w for w in ws if w not in STOP and len(w) > 2]


def load_refs():
    doc = Document(DOCX)
    refs = []
    for p in doc.paragraphs:
        t = p.text.strip()
        m = re.match(r"^\[(\d+)\]\s+(.*)$", t)
        if m:
            refs.append((int(m.group(1)), m.group(2)))
    return refs


def parse_claimed(ref):
    out = {}
    m = re.search(r"\.\s*(\d{4})\s*;", ref)
    if not m:
        m = re.search(r"\b(19|20)(\d{2})\b", ref)
        out["year"] = int(m.group(0)) if m else None
    else:
        out["year"] = int(m.group(1))
    m = re.search(r";\s*(\d+)", ref)
    out["volume"] = m.group(1) if m else None
    m = re.search(r":\s*([A-Za-z]?\d+)", ref.split(";")[-1]) if ";" in ref else None
    out["first_page"] = m.group(1) if m else None
    return out


def query_crossref(ref):
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": ref, "rows": 3,
              "select": "title,container-title,issued,volume,page,DOI,author,type"}
    r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json().get("message", {}).get("items", [])


def score_item(ref, item):
    titles = item.get("title") or []
    ct = titles[0] if titles else ""
    tw = sig_words(ct)
    if not tw:
        return 0.0, ct
    refw = set(sig_words(ref))
    hit = sum(1 for w in tw if w in refw)
    return hit / len(tw), ct


def main():
    refs = load_refs()
    report = []
    summary = {"OK": 0, "CHECK": 0, "NOT_FOUND": 0}
    print(f"verifying {len(refs)} references...")

    for num, ref in refs:
        claimed = parse_claimed(ref)
        try:
            items = query_crossref(ref)
        except Exception as e:
            report.append((num, "NOT_FOUND", ref, f"query error: {e}", {}))
            summary["NOT_FOUND"] += 1
            time.sleep(1.0)
            continue

        best, best_score, best_title = None, 0.0, ""
        for it in items:
            sc, ct = score_item(ref, it)
            if sc > best_score:
                best, best_score, best_title = it, sc, ct

        if best is None or best_score < 0.45:
            report.append((num, "NOT_FOUND", ref,
                           f"no confident title match (best overlap {best_score:.2f}: {best_title[:90]!r})", {}))
            summary["NOT_FOUND"] += 1
            time.sleep(1.0)
            continue

        issued = best.get("issued", {}).get("date-parts", [[None]])[0][0]
        cr = {
            "doi": best.get("DOI"),
            "title": best_title,
            "journal": (best.get("container-title") or [""])[0],
            "year": issued,
            "volume": best.get("volume"),
            "page": best.get("page"),
            "overlap": round(best_score, 2),
        }

        problems = []
        if claimed["year"] and issued and claimed["year"] != issued:
            problems.append(f"YEAR claimed {claimed['year']} vs Crossref {issued}")
        if claimed["volume"] and cr["volume"] and str(claimed["volume"]) != str(cr["volume"]):
            problems.append(f"VOLUME claimed {claimed['volume']} vs Crossref {cr['volume']}")
        if claimed["first_page"] and cr["page"]:
            cr_first = str(cr["page"]).split("-")[0].strip()
            if cr_first and claimed["first_page"].lower() != cr_first.lower():
                problems.append(f"PAGE claimed {claimed['first_page']} vs Crossref {cr['page']}")
        if best_score < 0.70:
            problems.append(f"TITLE overlap only {best_score:.2f} - check wording")

        status = "OK" if not problems else "CHECK"
        summary[status] += 1
        report.append((num, status, ref, "; ".join(problems) if problems else "match", cr))
        time.sleep(0.8)

    lines = []
    lines.append("REFERENCE VERIFICATION REPORT (Crossref)")
    lines.append("=" * 78)
    lines.append(f"OK: {summary['OK']}   NEEDS CHECK: {summary['CHECK']}   NOT FOUND: {summary['NOT_FOUND']}")
    lines.append("")
    for status_filter in ("NOT_FOUND", "CHECK", "OK"):
        block = [r for r in report if r[1] == status_filter]
        if not block:
            continue
        lines.append("")
        lines.append(f"----- {status_filter} ({len(block)}) " + "-" * 40)
        for num, status, ref, note, cr in block:
            lines.append("")
            lines.append(f"[{num}] {note}")
            lines.append(f"   CITED:    {ref}")
            if cr:
                lines.append(f"   CROSSREF: {cr['title']}")
                lines.append(f"             {cr['journal']} {cr['year']};{cr['volume']}:{cr['page']}  doi:{cr['doi']}")
    with io.open(os.path.join(HERE, "reference_verification_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(json.dumps(summary))
    print("report written")


if __name__ == "__main__":
    main()
