"""Rebuild master.ass for the gpt-6 Reel: breath-grouped blocks, varied reveal
steps, hand-picked EMPH. Replaces the generator's uniform 6-word / 3-step rule.
Idempotent: rerun to regenerate from words_out.txt + the header below."""
import json
from pathlib import Path

E = Path('edit/gpt-6-is-great-not-as-good-as-they-said')
EMPH = {48, 145, 184, 218, 298, 305, 386, 403, 440, 471}
LINE_CHARS, HOLD_MAX, MIN_STEP = 16, 0.6, 0.25
B = chr(92)
CLAUSE = {'mas','então','porque','se','aí','e','ou','que','onde','quando','de'}

rows = [l.rstrip('\n').split('\t') for l in (E/'words_out.txt').read_text(encoding='utf-8').splitlines()]
W = [(int(a), float(b), float(c), float(d), e) for a, b, c, d, e in rows]

edl = json.loads((E/'edl.json').read_text(encoding='utf-8'))
bounds, off = [], 0.0
for r in edl['ranges']:
    off += float(r['end']) - float(r['start'])
    bounds.append(round(off, 2))

# --- blocks: break on breath, sentence end, comma, or 6-word cap -------------
blocks, cur = [], []
for w in W:
    if cur:
        prev = cur[-1][4]
        head = w[4].strip('.,!?').lower()
        brk = (w[3] >= 0.26
               or prev.endswith(('.', '?', '!'))
               or (prev.endswith(',') and len(cur) >= 3)
               or (head in CLAUSE and len(cur) >= 4)
               or len(cur) >= 5)
        if brk:
            blocks.append(cur); cur = []
    cur.append(w)
if cur: blocks.append(cur)

def wrap(words):
    lines, ln = [], ''
    for t in words:
        cand = (ln + ' ' + t).strip()
        if ln and len(cand) > LINE_CHARS:
            lines.append(ln); ln = t
        else:
            ln = cand
    if ln: lines.append(ln)
    return lines

def markup(words, idxs):
    """Render tokens, wrapping EMPH ones; pad only when not starting a line."""
    lines, cursor, out = wrap([t for _, t in zip(idxs, words)]), 0, []
    flat = []
    for li, line in enumerate(lines):
        toks = line.split(' ')
        rendered = []
        for ti, tok in enumerate(toks):
            gi = idxs[cursor]; cursor += 1
            if gi in EMPH:
                core = tok.rstrip('.,!?'); tail = tok[len(core):]
                pre = '' if ti == 0 else '\\h\\h'
                rendered.append(pre + '{' + B + 'rEMPH}' + core + '{' + B + 'r}' + tail)
            else:
                rendered.append(tok)
        flat.append(' '.join(rendered))
    return '\\N'.join(flat)

def ts(t):
    t = max(0.0, t); h = int(t//3600); m = int(t % 3600//60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

cues = []
for bi, b in enumerate(blocks):
    n = len(b); dur = b[-1][2] - b[0][1]
    commas = sum(1 for x in b if x[4].endswith(','))
    if commas >= 2 and n >= 3:      steps = [[x] for x in b]          # a list: one per beat
    elif dur < 0.85 or n <= 2:      steps = [b]                        # fast: arrives whole
    elif n <= 4:                    steps = [b[:2], b[2:]]
    else:                           steps = [b[:2], b[2:4], b[4:]]
    steps = [s for s in steps if s]
    # merge steps shorter than MIN_STEP into the previous one
    merged = []
    for s in steps:
        if merged and (s[0][1] - merged[-1][0][1]) < MIN_STEP:
            merged[-1] = merged[-1] + s
        else:
            merged.append(s)
    steps = merged

    nxt = blocks[bi+1][0][1] if bi+1 < len(blocks) else None
    seg_end = next((x for x in bounds if x >= b[-1][2] - 0.01), b[-1][2])

    def block_end():
        caps = [seg_end] + ([nxt - 0.02] if nxt is not None else [])
        e = min([b[-1][2] + HOLD_MAX] + caps)
        return max(e, min([b[-1][2] + 0.05] + caps))   # floor never outruns a cap

    # the closing cue must also breathe: fold it back rather than flash it
    while len(steps) > 1 and block_end() - steps[-1][0][1] < MIN_STEP:
        steps = steps[:-2] + [steps[-2] + steps[-1]]

    shown = []
    for si, s in enumerate(steps):
        shown += s
        start = s[0][1]
        if si+1 < len(steps):
            end = steps[si+1][0][1]
        else:
            end = b[-1][2] + HOLD_MAX
            if nxt is not None: end = min(end, nxt - 0.02)
            end = min(end, seg_end)
            end = max(end, b[-1][2] + 0.05)
        txt = markup([x[4] for x in shown], [x[0] for x in shown])
        cues.append([start, end, txt])

# no two cues may be on screen at once - libass would stack them
cues.sort(key=lambda c: c[0])
for i in range(len(cues) - 1):
    cues[i][1] = min(cues[i][1], cues[i+1][0])
cues = [f"Dialogue: 0,{ts(a)},{ts(b)},BODY,,0,0,0,,{t}" for a, b, t in cues if b - a >= 0.05]

header = (E/'master.ass').read_text(encoding='utf-8').split('[Events]')[0]
fmt = "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
(E/'master.ass').write_text(header + fmt + '\n'.join(cues) + '\n', encoding='utf-8')
print(f"blocks {len(blocks)}  cues {len(cues)}  emph {len(EMPH)}")
from collections import Counter
print("block sizes:", sorted(Counter(len(b) for b in blocks).items()))
