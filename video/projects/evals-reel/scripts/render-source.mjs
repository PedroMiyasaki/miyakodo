import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const projectDir = path.resolve(import.meta.dirname, "..");
const repoDir = path.resolve(projectDir, "..", "..", "..");
const input = path.join(
  repoDir,
  "video",
  "inputs",
  "se-voce-desenvolve-qualquer-projeto-de-ia-precisa-de-evals.MP4",
);
const output = path.join(projectDir, "assets", "evals-cut-sdr.mp4");
const audioOutput = path.join(projectDir, "assets", "evals-cut-audio.m4a");
const plan = JSON.parse(
  fs.readFileSync(path.join(projectDir, "edit-plan.json"), "utf8"),
);

const filters = [];
const concatInputs = [];
plan.segments.forEach((segment, index) => {
  filters.push(
    `[0:v]trim=start=${segment.sourceStart}:end=${segment.sourceEnd},setpts=PTS-STARTPTS[v${index}]`,
    `[0:a]atrim=start=${segment.sourceStart}:end=${segment.sourceEnd},asetpts=PTS-STARTPTS[a${index}]`,
  );
  concatInputs.push(`[v${index}][a${index}]`);
});

filters.push(
  `${concatInputs.join("")}concat=n=${plan.segments.length}:v=1:a=1[vcat][acat]`,
  "[vcat]zscale=transfer=linear:npl=100,tonemap=tonemap=hable:desat=0,zscale=primaries=bt709:transfer=bt709:matrix=bt709:range=limited,format=yuv420p[vout]",
);

const render = spawnSync(
  "ffmpeg",
  [
    "-hide_banner",
    "-y",
    "-i",
    input,
    "-filter_complex",
    filters.join(";"),
    "-map",
    "[vout]",
    "-map",
    "[acat]",
    "-c:v",
    "libx264",
    "-preset",
    "medium",
    "-crf",
    "18",
    "-profile:v",
    "high",
    "-level:v",
    "4.2",
    "-r",
    "60",
    "-c:a",
    "aac",
    "-b:a",
    "192k",
    "-ar",
    "44100",
    "-color_primaries",
    "bt709",
    "-color_trc",
    "bt709",
    "-colorspace",
    "bt709",
    "-movflags",
    "+faststart",
    output,
  ],
  { stdio: "inherit" },
);

if (render.status !== 0) {
  process.exit(render.status ?? 1);
}

const extractAudio = spawnSync(
  "ffmpeg",
  [
    "-hide_banner",
    "-y",
    "-i",
    output,
    "-vn",
    "-c:a",
    "copy",
    audioOutput,
  ],
  { stdio: "inherit" },
);

process.exit(extractAudio.status ?? 1);
