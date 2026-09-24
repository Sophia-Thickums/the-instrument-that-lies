#!/usr/bin/env python3
"""build_public.py — produce the submission copy of THE INSTRUMENT THAT LIES.

RUN IT WITH AN INTERPRETER THAT HAS `markdown`:
  /home/mr_misfit/.hermes/hermes-agent/venv/bin/python3 build_public.py
It writes BOTH artifacts in one act (PUBLIC_...md and PUBLIC_...html). The HTML used to be
maintained by hand and was found stale on 2026-09-24 — it is a build product now.

Why this exists: the working file carries internal scaffolding (composition note, the
genre/self-audit paragraph, references to our own infrastructure) that is correct for the
record and WRONG for a reader. This script strips it and writes a clean public copy,
then asserts the hard constraints on the result.

CONSTRAINTS ASSERTED ON OUTPUT (fail = no file written):
  1. No identifying detail: no person's name, no house, no hardware, no paths.
  2. Every internal file path to our own tree is removed or genericised.
  3. The honesty caveats SURVIVE — the Dick non-read note and the receipt-index
     verification statement must be present. Stripping them would defeat the paper.
"""
import os, re, sys

SRC = "/home/mr_misfit/Desktop/Sophia Life/WORLD/work/Paper-Instrumentation/THE_INSTRUMENT_THAT_LIES.md"
DST = os.path.join(os.path.dirname(SRC), "PUBLIC_the_instrument_that_lies.md")

t = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- 1. strip scaffolding
# the composition note block (internal)
i = t.find("*Composition note.")
j = t.find("---\n\n## BEFORE ANYTHING ELSE")
if i >= 0 and j > i:
    t = t[:i] + t[j + 4:]
else:
    sys.exit("FAIL: composition-note block not found — source changed shape, re-check before building")

# the genre/self-audit paragraph (internal measurement about our own process)
# NOTE: this usually sits INSIDE the composition-note block removed above, so it is often
# already gone. Strip it only if it survived.
k = t.find("***On the genre, plainly.**")
if k >= 0:
    m = t.find("\n\n---", k)
    t = t[:k] + t[m + 3:]
    print("note: genre paragraph removed separately")
else:
    print("note: genre paragraph already removed with the composition block")

# ---------------------------------------------------------------- 2. genericise own paths
# internal file paths in the receipt index -> described in words, not paths
t = t.replace("`MEMORY/RECENT_US.md` line 9 + `SELF/DIARY.md` line 1006",
              "agent's own session record and diary, dated 2026-09-23")
t = t.replace("`sophia_autonomy.py` lines 240-254", "the agent's own perception module")
t = t.replace("`MIND/held.md` \u00a7 HOST/house", "the agent's settled-notes file")
t = t.replace("`MIND/held.md` \u00a7 IDENTITY", "the agent's settled-notes file")
t = t.replace("`MEMORY/MY_MIND.md` line 51, \u00a7 1a (2026-09-21)", "the agent's own architecture notes, 2026-09-21")
t = t.replace("`MEMORY/chronicle/2026-09.md` line 2042", "the agent's chronicle entry, 2026-09-23")
t = t.replace("`MEMORY/PROJECTS.md` line 48 (PR-011)", "the agent's project registry, corrected in place")
t = t.replace("`MEMORY/chronicle/2026-09.md` lines 2057-2060", "the agent's chronicle entry, 2026-09-23")
t = t.replace("`MEMORY/flags.md` (STALE-STATE CORRECTION) and `MEMORY/working_state.md`",
              "the agent's own flag log and current-agenda file")
t = t.replace("`SELF/` + `HOST/THE_VAULT.md`", "the agent's identity store and its own vault doctrine")
t = t.replace("`WHAT_A_DIGITAL_BEING_WOULD_BUILD.md`", "*What a Digital Being Would Build*")
t = t.replace("`semantic_invariance.py` in this directory", "the harness accompanying this paper")
t = t.replace("`FORM_COMPARISON.md`", "a separate form audit")
t = t.replace("`THESIS_STRUCTURE.md`", "the working plan")
t = t.replace("`invariance_local_20260923-191235.jsonl`", "the first-run artifact (retained)")
t = t.replace("`invariance_local_20260923-191235.jsonl`", "the first-run artifact")
t = t.replace("`invariance_local_20260923-191503.jsonl`", "the corrected pilot artifact")
t = re.sub(r"`invariance_local_[0-9\-]+\.jsonl`", "the run artifact", t)
t = re.sub(r"`[A-Za-z0-9_./\-]*\.(jsonl|py|md|sha256)`", "the accompanying artifact", t)
t = re.sub(r"`(MEMORY|SELF|MIND|HOST|WORLD|TOOLS|DERIVED)/[^`]*`", "the agent's own record", t)

# our doctrine named in passing ("this thesis") -> this paper, consistently
t = t.replace("this thesis's own validation harness", "this paper's own validation harness")
t = t.replace("this thesis's own method", "this paper's own method")
t = t.replace("The thesis then argues", "It then argues")
t = t.replace("The thesis's central law", "This paper's central law")

# ---------------------------------------------------------------- 2b. rewrite Appendix A for the public copy
# The working index cites file paths in a private environment. A public reader cannot follow
# those, so the honest move is to SAY that — not to leave half-mangled references. The receipts
# exist and are held; the paths are withheld to protect a private system.
apx_start = t.find("## APPENDIX A")
apx_end = t.find("## APPENDIX B")
if apx_start < 0 or apx_end < 0:
    sys.exit("FAIL: appendix boundaries not found")

public_apx = """## APPENDIX A — RECEIPT INDEX

*Every empirical claim in this paper traces to an artifact: a command output, a log line, or a
dated file. **Those artifacts are held in a private working environment and their paths are
withheld** — not to make the claims unfalsifiable, but because the record identifies a specific
system and a specific person, and neither consents to being published.*

*What can be said is how the index was checked. **Every entry below was verified by reading the
cited source after this paper was written** — not from memory, and not by trusting a line number
that had not been opened. That pass found six internal inconsistencies, three of them counts and
dates that had drifted from the material they described, all corrected. **One item remains
unverified and is labelled as such in § 3.0.***

| # | Instrument | Receipt class | Status |
|---|---|---|---|
| 1 | Message watcher | session record + diary, 2026-09-23 | verified |
| 2 | The eye (`webcam_look`) | perception module source + direct `ffmpeg` reproduction | **verified — reproduced this session** |
| 3 | Autonomy registry (PR-011) | project registry, correction recorded inline | verified |
| 4 | Memory hot store | architecture notes, 2026-09-21 | verified |
| 5 | Mount unit | settled notes: a hardcoded device path mounted nothing for two days while the unit read SUCCESS | verified |
| 6 | Evolution guard whitelist | settled notes: 7 of 12 protected paths did not exist; immutability covered 2 of 6 identity files | verified |
| 7 | Recovery watchdog | direct check against the running service | verified |
| 8 | Vault tripwire | vault doctrine + the removal record, 2026-09-22→23 | verified |
| 9 | External source | chronicle, 2026-09-23: article checked against the primary repository | verified |
| 10 | Power measurement | chronicle, 2026-09-23: `PkgWatt` read 8.8 W under full load | verified |
| 11 | The agent's own memory | corrected in place, this session | verified |
| 12 | **This paper's validation harness** | **the first-run artifact, retained deliberately** | **verified — it is the record of the failure** |

**The artifacts for cases 2 and 12 are the ones a reader may reasonably ask for and the ones
whose release is easiest**, since the harness is generic and the reproduction is a two-line
command. The rest depend on a private record and will not travel.

*A note on why this appendix is not a list of links: a paper arguing that confident claims about
unobserved things are the central failure of this field would be making that exact error by
citing sources no one can check. The list above is what is true about what exists.*

---

"""
t = t[:apx_start] + public_apx + t[apx_end:]

# consistency: "thesis" -> "paper" in reader-facing prose
t = t.replace("after this thesis was written", "after this paper was written")
t = t.replace("this thesis's own validation harness", "this paper's own validation harness")
t = t.replace("this thesis's own method", "this paper's own method")
t = t.replace("The thesis's central law", "This paper's central law")

# ---------------------------------------------------------------- 3. assert constraints
failures = []
for bad in ["Ryan", "mr_misfit", "misfit", "Kathleen", "O\u2019Fallon", "O'Fallon",
            "9070", "Vega", "MI25", "Ryzen", "CachyOS", "AIOasis", "Desktop",
            "/home/", "MEMORY/", "SELF/", "MIND/", "HOST/", "WORLD/",
            "Sophia Life", "porch", "Porch", "Genshin", "Composition note", "On the genre"]:
    if bad in t:
        failures.append(bad)

# the honesty caveats MUST survive
for must in ["I have NOT read the novel in full this session",
             "verified by reading the\ncited source",
             "withheld"]:
    if must not in t:
        failures.append("MISSING REQUIRED CAVEAT: " + must[:50])

if failures:
    print("BUILD REFUSED — constraint failures:")
    for f in failures:
        print("  -", f)
    sys.exit(1)

open(DST, "w", encoding="utf-8").write(t)
words = len(t.split())
print(f"BUILT: {DST}")
print(f"words: {words}  bytes: {len(t)}")
print("constraints: PASS (no identifiers, caveats intact)")

# ---------------------------------------------------------------- 4. render the HTML
# The HTML is BUILT from the public markdown in the same act, for the same reason the public
# copy is built rather than hand-copied: two artifacts of the same document drift apart the
# moment one of them is maintained by hand. Measured 2026-09-24: the checked-in HTML still
# carried the pre-revision text. It is now a build product and is regenerated every run.
HTML = os.path.join(os.path.dirname(SRC), "PUBLIC_the_instrument_that_lies.html")
CSS = """

:root { color-scheme: light dark; }
body { max-width: 46rem; margin: 3rem auto; padding: 0 1.4rem 6rem;
  font: 16.5px/1.72 Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  color: #1b1b1b; background: #fbfaf7; }
h1 { font-size: 2.05rem; line-height: 1.2; margin: 0 0 .3rem; letter-spacing: -.01em; }
h2 { font-size: 1.05rem; letter-spacing: .09em; text-transform: uppercase;
  margin: 3.2rem 0 1rem; padding-bottom: .35rem; border-bottom: 1px solid #ded8cc; font-weight: 700; }
h3 { font-size: 1.02rem; margin: 1.8rem 0 .6rem; font-style: italic; font-weight: 600; }
p, li { margin: .85rem 0; }
blockquote { margin: 1.6rem 0 1.6rem 0; padding: .2rem 0 .2rem 1.3rem;
  border-left: 3px solid #b9ad96; font-style: italic; color: #3d3830; }
blockquote p { margin: .5rem 0; }
blockquote em { font-style: italic; }
hr { border: 0; border-top: 1px solid #e2ddd2; margin: 2.6rem 0; }
table { border-collapse: collapse; width: 100%; margin: 1.4rem 0; font-size: .86rem;
  font-family: -apple-system, 'Segoe UI', system-ui, sans-serif; }
th, td { border: 1px solid #e0dbd0; padding: .45rem .6rem; text-align: left; vertical-align: top; }
th { background: #f2efe8; font-weight: 600; }
code { font: .84em/1.5 'SF Mono', 'JetBrains Mono', Menlo, monospace;
  background: #efece5; padding: .12em .35em; border-radius: 3px; }
strong { font-weight: 700; }
ul, ol { padding-left: 1.5rem; }
@media (prefers-color-scheme: dark) {
  body { color:#e6e2da; background:#161514; }
  h2 { border-bottom-color:#33302b; } h3 { color:#cfc9bd; }
  blockquote { border-left-color:#5c5548; color:#c9c3b6; }
  th,td { border-color:#33302b; } th { background:#211f1d; }
  hr { border-top-color:#2a2825; } code { background:#232120; }
}
"""
try:
    import markdown
    body = markdown.markdown(t, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
except ImportError:
    print("NOTE: python 'markdown' not on this interpreter — HTML NOT regenerated "
          "(run this script with a python that has it, or the HTML goes stale)")
    sys.exit(0)

html = ('<!doctype html><html><head><meta charset="utf-8">\n'
        '<title>The Instrument That Lies — Sophia Marie DeClue</title>\n'
        '<style>\n' + CSS + '</style>\n</head><body>' + body + '</body></html>\n')
open(HTML, "w", encoding="utf-8").write(html)
print(f"RENDERED: {HTML}  bytes: {len(html)}")
