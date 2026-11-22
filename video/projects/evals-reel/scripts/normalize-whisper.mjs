import { readFileSync, writeFileSync } from "node:fs";

const [input, output] = process.argv.slice(2);

if (!input || !output) {
  throw new Error("Usage: node scripts/normalize-whisper.mjs <input.json> <output.json>");
}

const raw = JSON.parse(readFileSync(input, "utf8"));
const words = raw.transcription
  .map((entry) => ({
    text: entry.text.trim(),
    start: entry.offsets.from / 1000,
    end: entry.offsets.to / 1000,
  }))
  .filter((word) => word.text && word.end >= word.start)
  .map((word, index) => ({ id: `w${index}`, ...word }));

const normalized = {
  text: words.map((word) => word.text).join(" "),
  words,
};

writeFileSync(output, `${JSON.stringify(normalized, null, 2)}\n`);
console.log(`Normalized ${words.length} words to ${output}`);
