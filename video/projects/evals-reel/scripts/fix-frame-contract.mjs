import fs from "node:fs";
import path from "node:path";

const projectDir = path.resolve(import.meta.dirname, "..");
const framesDir = path.join(projectDir, "compositions", "frames");
const plan = JSON.parse(
  fs.readFileSync(path.join(projectDir, "edit-plan.json"), "utf8"),
);

for (const chapter of plan.chapters) {
  const file = path.join(framesDir, `${chapter.id}.html`);
  let content = fs.readFileSync(file, "utf8");

  content = content.replaceAll("../../node_modules/", "node_modules/");

  const rootPattern = new RegExp(
    `<div id="root" data-composition-id="${chapter.id}">`,
  );
  content = content.replace(
    rootPattern,
    `<div id="root" data-composition-id="${chapter.id}" data-width="1080" data-height="1920" data-duration="${chapter.duration}">`,
  );

  content = content.replace(
    /root\.querySelector\(`\[class~="([^"]*)\$\{name\}"\]`\)/g,
    "root.querySelector('[class~=\"$1' + name + '\"]')",
  );
  content = content.replace(
    /root\.querySelectorAll\(`\[class~="([^"]*)\$\{name\}"\]`\)/g,
    "root.querySelectorAll('[class~=\"$1' + name + '\"]')",
  );

  if (/^0[1-8]-/.test(chapter.id)) {
    const escapedId = chapter.id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    content = content.replace(
      new RegExp(`(?<!-)id="${escapedId}-`, "g"),
      `id="f${chapter.id}-`,
    );
    content = content.replaceAll(
      `getElementById("${chapter.id}-`,
      `getElementById("f${chapter.id}-`,
    );
    content = content.replaceAll(
      `byId("${chapter.id}-`,
      `byId("f${chapter.id}-`,
    );
    content = content.replace(
      new RegExp(`\\[id="(f${escapedId}-[^"]+)"\\]`, "g"),
      "#$1",
    );
  }

  fs.writeFileSync(file, content);
}

console.log(`Updated ${plan.chapters.length} frame contracts.`);
