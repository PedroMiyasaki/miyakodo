import fs from "node:fs";
import path from "node:path";

const projectDir = path.resolve(import.meta.dirname, "..");
const transcript = JSON.parse(
  fs.readFileSync(path.join(projectDir, "transcript.json"), "utf8"),
);

const sourceStart = 0.18;
const sourceEnd = 209.36;
const defaultPause = 0.18;
const intentionalPauses = [
  { from: 5.78, to: 6.3, keep: 0.52, label: "hook" },
  { from: 92.02, to: 92.94, keep: 0.62, label: "evals-reveal" },
];

const rounded = (value) => Math.round(value * 1000) / 1000;
const overlaps = (a0, a1, b0, b1) => Math.max(a0, b0) < Math.min(a1, b1);

const cutIntervals = [];
for (let i = 0; i < transcript.words.length - 1; i += 1) {
  const current = transcript.words[i];
  const next = transcript.words[i + 1];
  const gap = next.start - current.end;
  if (gap <= 0.35) continue;

  const intentional = intentionalPauses.find((pause) =>
    overlaps(current.end, next.start, pause.from, pause.to),
  );
  const keep = intentional?.keep ?? defaultPause;
  if (gap <= keep + 0.02) continue;

  const leftKeep = keep * 0.5;
  cutIntervals.push({
    from: rounded(current.end + leftKeep),
    to: rounded(next.start - (keep - leftKeep)),
    originalGap: rounded(gap),
    keptGap: keep,
    label: intentional?.label ?? "pause",
  });
}

const segments = [];
let cursor = sourceStart;
for (const cut of cutIntervals) {
  if (cut.from <= cursor || cut.from >= sourceEnd) continue;
  segments.push({
    sourceStart: rounded(cursor),
    sourceEnd: rounded(Math.min(cut.from, sourceEnd)),
  });
  cursor = Math.max(cursor, cut.to);
}
if (cursor < sourceEnd) {
  segments.push({ sourceStart: rounded(cursor), sourceEnd: sourceEnd });
}

let editedCursor = 0;
for (const segment of segments) {
  segment.start = rounded(editedCursor);
  segment.duration = rounded(segment.sourceEnd - segment.sourceStart);
  editedCursor += segment.duration;
  segment.end = rounded(editedCursor);
}

function sourceToEdited(sourceTime) {
  let removed = sourceStart;
  for (const cut of cutIntervals) {
    if (sourceTime <= cut.from) break;
    removed += Math.min(sourceTime, cut.to) - cut.from;
  }
  return rounded(sourceTime - removed);
}

const words = transcript.words
  .filter((word) => word.end >= sourceStart && word.start <= sourceEnd)
  .map((word) => ({
    ...word,
    start: sourceToEdited(word.start),
    end: sourceToEdited(word.end),
  }));

for (let i = 0; i < words.length; i += 1) {
  words[i].text = words[i].text
    .replace(/^AI(?=\W|$)/i, "IA")
    .replace(/^EVALS(?=\W|$)/i, "evals")
    .replace(/^Antropic(?=\W|$)/i, "Anthropic");
}

for (let i = 0; i < words.length - 5; i += 1) {
  const sequence = words
    .slice(i, i + 6)
    .map((word) => word.text.toLowerCase().replace(/[.,?!]/g, ""))
    .join(" ");
  if (sequence === "para a gente como que ele") {
    words[i + 1].text = "o";
    words[i + 2].text = "agente";
  }
}

for (let i = 0; i < words.length - 6; i += 1) {
  const sequence = words
    .slice(i, i + 7)
    .map((word) => word.text.toLowerCase().replace(/[.,?!]/g, ""))
    .join(" ");
  if (sequence === "para a gente ou a gente ia") {
    words[i + 1].text = "o";
    words[i + 2].text = "agente";
    words[i + 4].text = "o";
    words[i + 5].text = "agente";
  }
}

const captions = [];
let group = [];
for (const word of words) {
  const candidate = [...group, word];
  const candidateText = candidate.map((item) => item.text).join(" ");
  const duration = candidate.at(-1).end - candidate[0].start;
  const previousEndsSentence = group.at(-1)?.text.match(/[.!?]$/);
  const shouldBreak =
    group.length > 0 &&
    (candidate.length > 6 ||
      candidateText.length > 36 ||
      duration > 2.7 ||
      previousEndsSentence);

  if (shouldBreak) {
    captions.push({
      start: group[0].start,
      end: group.at(-1).end,
      words: group,
    });
    group = [word];
  } else {
    group = candidate;
  }
}
if (group.length) {
  captions.push({
    start: group[0].start,
    end: group.at(-1).end,
    words: group,
  });
}

for (const caption of captions) {
  caption.text = caption.words.map((word) => word.text).join(" ");
}

const chapterBoundaries = [
  ["01-nome", 0.18],
  ["02-tecnico-negocio", 6.3],
  ["03-contratos", 20.08],
  ["04-sem-evals", 36.12],
  ["05-dois-erros", 52.32],
  ["06-regressao", 77.85],
  ["07-gabarito", 96.2],
  ["08-rodar-de-novo", 121.94],
  ["09-metrica-direcao", 139.52],
  ["10-regra-testada", 156.98],
  ["11-direcao", 180.98],
  ["12-guia", 193.44],
  ["end", sourceEnd],
];

const chapters = chapterBoundaries.slice(0, -1).map(([id, source], index) => {
  const nextSource = chapterBoundaries[index + 1][1];
  const start = sourceToEdited(source);
  const end = sourceToEdited(nextSource);
  return {
    id,
    sourceStart: source,
    sourceEnd: nextSource,
    start,
    end,
    duration: rounded(end - start),
  };
});

const editPlan = {
  sourceStart,
  sourceEnd,
  duration: rounded(editedCursor),
  removed: rounded(sourceEnd - sourceStart - editedCursor),
  cutIntervals,
  segments,
  chapters,
};

fs.writeFileSync(
  path.join(projectDir, "edit-plan.json"),
  `${JSON.stringify(editPlan, null, 2)}\n`,
);
fs.writeFileSync(
  path.join(projectDir, "transcript-edited.json"),
  `${JSON.stringify({ duration: editPlan.duration, words, captions }, null, 2)}\n`,
);

console.log(
  JSON.stringify(
    {
      duration: editPlan.duration,
      removed: editPlan.removed,
      cuts: cutIntervals.length,
      captions: captions.length,
      chapters,
    },
    null,
    2,
  ),
);
