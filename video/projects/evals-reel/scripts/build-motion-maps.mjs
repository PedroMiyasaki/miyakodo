import fs from "node:fs";
import path from "node:path";

const projectDir = path.resolve(import.meta.dirname, "..");
const framesDir = path.join(projectDir, "compositions", "frames");
const scenes = JSON.parse(fs.readFileSync(path.join(framesDir, "scenes.json"), "utf8"));
const ids = new Set(scenes.map((scene) => scene.id));

for (const file of fs.readdirSync(framesDir)) {
  if (file.endsWith(".motion.json") && !ids.has(file.replace(".motion.json", ""))) {
    fs.unlinkSync(path.join(framesDir, file));
  }
}

for (const scene of scenes) {
  fs.writeFileSync(
    path.join(framesDir, `${scene.id}.motion.json`),
    `${JSON.stringify(
      {
        duration: scene.duration,
        assertions: [
          { kind: "appearsBy", selector: scene.hero, bySec: scene.bySec },
          { kind: "staysInFrame", selector: scene.hero },
        ],
      },
      null,
      2,
    )}\n`,
  );
}

fs.writeFileSync(
  path.join(projectDir, "index.motion.json"),
  `${JSON.stringify(
    {
      duration: 202.18,
      assertions: [
        { kind: "appearsBy", selector: "#handle", bySec: 0.9 },
        { kind: "staysInFrame", selector: "#handle" },
      ],
    },
    null,
    2,
  )}\n`,
);

console.log(`Wrote ${scenes.length + 1} motion maps.`);
