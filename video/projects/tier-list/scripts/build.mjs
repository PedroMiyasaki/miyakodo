import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const project = path.resolve(import.meta.dirname, "..");
const repo = path.resolve(project, "../../..");
const input = path.join(repo, "video/inputs/tier_list");
const fps = 60;
const round = (n) => Math.round(n * 1e9) / 1e9;
const floorFrame = (n) => Math.floor(n * fps + 1e-7) / fps;
const ceilFrame = (n) => Math.ceil(n * fps - 1e-7) / fps;
const read = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const save = (file, value) => fs.writeFileSync(path.join(project, file), value, "utf8");
const json = (file, value) => save(file, `${JSON.stringify(value, null, 2)}\n`);
const escape = (value) => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll('"', "&quot;");

for (const dir of ["assets/fonts", "assets/voices", "compositions/ratings"]) {
  fs.mkdirSync(path.join(project, dir), { recursive: true });
}
for (const [name, source] of [
  ["inter.woff2", "video/projects/evals-reel/node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2"],
  ["bricolage.woff2", "video/projects/evals-reel/node_modules/@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-wght-normal.woff2"],
]) fs.copyFileSync(path.join(repo, source), path.join(project, "assets/fonts", name));

const main = read(path.join(input, "edit/transcripts/tier_list.json"));
const originalWords = main.words.filter((w) => w.type === "word");
const items = [
  { id: "whatsapp", label: "Bot no WhatsApp", grade: "D", speech: 4, last: 42.54, rating: 4.3, recording: "14.45.37" },
  { id: "conteudo", label: "Conteúdo nas redes", grade: "C", speech: 46.32, last: 73.4, rating: 46.72, recording: "14.46.04" },
  { id: "reunioes", label: "Reuniões de vendas", grade: "C", speech: 77.84, last: 88.78, rating: 78.16, recording: "14.46.20" },
  { id: "rag", label: "RAG Enterprise", grade: "B", speech: 94, last: 127.8, rating: 94.64, recording: "14.46.42" },
  { id: "especialistas", label: "Copiloto para especialistas", grade: "S", speech: 131.22, last: 185.66, rating: 132.24, recording: "14.47.07" },
];

let cursor = 0;
const editedWords = [];
for (const [index, item] of items.entries()) {
  const stem = `WhatsApp Ptt 2026-10-12 at ${item.recording}`;
  const transcript = read(path.join(input, `audios_esposa/edit/transcripts/${stem}.json`));
  const wifeWords = transcript.words.filter((w) => w.type === "word");
  const probe = JSON.parse(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "json", path.join(input, `audios_esposa/${stem}.ogg`)], { encoding: "utf8" }));
  item.voiceIn = round(Math.max(0, wifeWords[0].start - 0.08));
  item.voiceOut = round(Math.min(Number(probe.format.duration), wifeWords.at(-1).end + 0.12));
  item.voiceDuration = round(item.voiceOut - item.voiceIn);
  item.sourceStart = floorFrame(item.speech - item.voiceDuration - 0.33);
  item.sourceEnd = ceilFrame(item.last + (index === 4 ? 0.3 : 0.16));
  item.start = round(cursor);
  item.duration = round(item.sourceEnd - item.sourceStart);
  item.end = round(item.start + item.duration);
  item.speechAt = round(item.speech - item.sourceStart);
  item.ratingAt = round(item.rating - item.sourceStart);
  item.voiceAt = round(item.speechAt - 0.18 - item.voiceDuration);
  item.voicePath = `assets/voices/${item.id}.wav`;
  assert(item.voiceAt >= 0.14 && item.voiceAt + item.voiceDuration <= item.speechAt - 0.179);
  if (index) assert(items[index - 1].sourceEnd < item.sourceStart);

  if (!fs.existsSync(path.join(project, item.voicePath))) {
    execFileSync("ffmpeg", ["-hide_banner", "-y", "-i", path.join(input, `audios_esposa/${stem}.ogg`), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", path.join(project, item.voicePath)], { stdio: "ignore" });
  }
  for (const w of wifeWords) {
    let text = w.text;
    if (item.id === "rag") text = text.replace(/^Reg\b/i, "RAG");
    if (item.id === "especialistas" && text === "A") text = "IA";
    editedWords.push({ text, start: round(item.start + item.voiceAt + w.start - item.voiceIn), end: round(item.start + item.voiceAt + w.end - item.voiceIn), speaker: "esposa", chapter: index });
  }
  for (const w of originalWords.filter((w) => w.start >= item.sourceStart && w.end <= item.sourceEnd)) {
    editedWords.push({ text: w.text.replace(/^m-muito/, "muito").replace(/--$/, "..."), start: round(item.start + w.start - item.sourceStart), end: round(item.start + w.end - item.sourceStart), speaker: "pedro", chapter: index, sourceStart: w.start });
  }
  cursor = item.end;
}
const duration = round(cursor);
assert.equal(editedWords.filter((w) => w.speaker === "pedro").length, originalWords.length, "Alguma fala de Pedro foi cortada");
assert.equal(Math.round(duration * fps), Math.round(items.reduce((n, item) => n + item.duration, 0) * fps));
for (let i = 0; i < editedWords.length; i++) {
  assert(editedWords[i].start >= 0 && editedWords[i].end <= duration && editedWords[i].start <= editedWords[i].end);
  if (i) assert(editedWords[i - 1].end <= editedWords[i].start + 0.001, "Vozes sobrepostas");
}
json("edit-plan.json", { duration, fps, sourceDuration: 186.95, removed: round(186.95 - duration), items });

const captions = [];
let words = [];
const flush = () => { if (words.length) captions.push({ words, start: words[0].start, end: words.at(-1).end }); words = []; };
for (const w of editedWords) {
  const proposed = [...words, w];
  const previous = words.at(-1);
  if (words.length && (proposed.length > 6 || proposed.map((v) => v.text).join(" ").length > 36 || w.end - words[0].start > 2.7 || previous.speaker !== w.speaker || previous.chapter !== w.chapter || w.start - previous.end > 0.5 || /[.!?]$/.test(previous.text))) flush();
  words.push(w);
}
flush();
for (const [index, caption] of captions.entries()) {
  const next = captions[index + 1];
  caption.visibleEnd = round(Math.min(duration, caption.end + 0.12, next ? next.start - 0.025 : duration));
  assert(caption.visibleEnd > caption.start);
}
assert.equal(captions.flatMap((c) => c.words).length, editedWords.length);
json("transcript-edited.json", { duration, words: editedWords, captions });

const fonts = (prefix) => `@font-face{font-family:Inter;src:url('${prefix}assets/fonts/inter.woff2') format('woff2');font-weight:100 900;font-style:normal}@font-face{font-family:'Bricolage Grotesque';src:url('${prefix}assets/fonts/bricolage.woff2') format('woff2');font-weight:200 800;font-style:normal}`;
const sub = (id, seconds, css, markup, script, prefix = "../../") => `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"></head><body><template><style>${fonts(prefix)}*{box-sizing:border-box}#root{position:absolute;inset:0;width:100%;height:100%;font-family:Inter;color:#FFFFFF}${css}</style><div id="root" data-composition-id="${id}" data-width="1080" data-height="1920" data-duration="${seconds}" data-fps="60">${markup}</div><script>const tl=gsap.timeline({paused:true});${script}window.__timelines['${id}']=tl;</script></template></body></html>`;

const capCss = `.caption-group{position:absolute;inset:0}.caption-box{position:absolute;inset:auto 72px 238px;margin:0 auto;width:max-content;max-width:936px;padding:18px 24px 15px;border:4px solid #FFFFFF;background:#0A0A0A;color:#FFFFFF;box-shadow:9px 9px 0 rgba(10,10,10,.8);font-size:48px;font-weight:650;letter-spacing:-.025em;line-height:1.12;text-align:center;text-wrap:balance}.caption-word{display:inline;padding:1px 2px 0;box-decoration-break:clone;-webkit-box-decoration-break:clone}`;
let capMarkup = "", capScript = "";
let wordId = 0;
for (const [index, caption] of captions.entries()) {
  const spans = caption.words.map((w) => {
    const id = `caption-word-${wordId++}`;
    capScript += `tl.set('#${id}',{color:'#0A0A0A',backgroundColor:'#FFFFFF'},${w.start});tl.set('#${id}',{color:'#FFFFFF',backgroundColor:'transparent'},${w.end});`;
    return `<span id="${id}" class="caption-word">${escape(w.text)}</span>`;
  }).join(" ");
  capMarkup += `<div id="caption-group-${index}" class="clip caption-group" data-start="${caption.start}" data-duration="${round(caption.visibleEnd - caption.start)}" data-track-index="0"><div class="caption-box">${spans}</div></div>`;
}
save("compositions/captions.html", sub("captions", duration, capCss, capMarkup, capScript, "../"));

const grades = ["S", "A", "B", "C", "D"];
const boardCss = `.tier-board{position:absolute;top:1040px;left:108px;width:864px;padding:16px;border:4px solid #FFFFFF;background:#0A0A0A;box-shadow:9px 9px 0 rgba(10,10,10,.8)}.tier-title{margin:0 0 12px;font-size:28px;line-height:34px;font-weight:740;letter-spacing:.02em}.tier-rows{display:flex;flex-direction:column;gap:5px}.tier-row{display:flex;align-items:center;gap:14px;height:72px;border-top:1px solid rgba(255,255,255,.35)}.tier-rank{display:flex;align-items:center;justify-content:center;width:60px;height:64px;flex:none;font-family:'Bricolage Grotesque';font-size:50px;font-weight:800}.tier-rank.current{background:#FFFFFF;color:#0A0A0A}.tier-track{position:relative;height:72px;flex:1;overflow:hidden}.tier-item{position:absolute;top:1px;width:340px;height:70px;padding:2px 8px;border:3px solid #FFFFFF;background:#0A0A0A;color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:30px;line-height:1;font-weight:650;text-align:center;text-wrap:balance;transform-origin:50% 50%;will-change:transform,opacity}.tier-item.current{background:#FFFFFF;color:#0A0A0A}`;
const ratings = [];
function boardScene(id, start, seconds, included, current, cue) {
  let markup = `<div id="${id}-board" class="tier-board"><p class="tier-title">MINHA TIER LIST</p><div class="tier-rows">`;
  for (const grade of grades) {
    const cards = included.filter((item) => item.grade === grade);
    markup += `<div class="tier-row"><div class="tier-rank${current?.grade === grade ? " current" : ""}">${grade}</div><div class="tier-track">`;
    for (const [column, item] of cards.entries()) markup += `<div id="${id}-${item.id}" class="tier-item${item.id === current?.id ? " current" : ""}" style="left:${column * 352}px">${escape(item.label)}</div>`;
    markup += "</div></div>";
  }
  markup += "</div></div>";
  let script = `tl.fromTo('#${id}-board',{opacity:0,y:24},{opacity:1,y:0,duration:.22,ease:'power3.out'},0);`;
  if (current) {
    // grid-card-assemble: explicit arrival into the authored slot, no overshoot.
    script += `tl.fromTo('#${id}-${current.id}',{opacity:0,x:128,scale:.94},{opacity:1,x:0,scale:1,duration:.48,ease:'power3.out'},${cue});`;
  }
  script += `tl.to('#${id}-board',{opacity:0,y:12,duration:.22,ease:'power2.in'},${round(seconds - 0.22)});`;
  save(`compositions/ratings/${id}.html`, sub(id, seconds, boardCss, markup, script));
  ratings.push({ id, start: round(start), duration: seconds });
}
for (const [index, item] of items.entries()) {
  const start = item.start + item.ratingAt - 0.18;
  boardScene(`rating-${item.id}`, start, 6.6, items.slice(0, index + 1), item, 0.18);
}
const last = items.at(-1);
boardScene("rating-recap", last.start + 169.2 - last.sourceStart, 5.2, items, null, 0);

let media = "";
for (const item of items) {
  const automation = JSON.stringify({ version: 1, lanes: [{ target: "volume", points: [{ t: 0, v: 0.08 }, { t: round(item.speechAt - 0.14), v: 0.08 }, { t: round(item.speechAt - 0.025), v: 1 }, { t: round(item.duration - 0.025), v: 1 }, { t: item.duration, v: 0 }] }] });
  media += `<video id="video-${item.id}" class="clip base-video" src="assets/tier-list-sdr.mp4" data-start="${item.start}" data-duration="${item.duration}" data-media-start="${round(item.sourceStart)}" data-track-index="0" data-has-audio="true" data-automation='${automation}' playsinline></video>`;
  const voiceAutomation = JSON.stringify({ version: 1, lanes: [{ target: "volume", points: [{ t: 0, v: 0 }, { t: 0.025, v: 1 }, { t: round(item.voiceDuration - 0.025), v: 1 }, { t: item.voiceDuration, v: 0 }] }] });
  media += `<audio id="voice-${item.id}" class="clip" src="${item.voicePath}" data-start="${round(item.start + item.voiceAt)}" data-duration="${item.voiceDuration}" data-media-start="${item.voiceIn}" data-track-index="10" data-volume="1" data-automation='${voiceAutomation}'></audio>`;
}
const hosts = ratings.map((r) => `<div id="slot-${r.id}" class="clip graphic-host" data-composition-id="${r.id}" data-composition-src="compositions/ratings/${r.id}.html" data-start="${r.start}" data-duration="${r.duration}" data-width="1080" data-height="1920" data-track-index="5" data-track-kind="graphics"></div>`).join("");
const rootCss = `*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0A0A0A}#root{position:relative;width:100%;height:100%;overflow:hidden;background:#0A0A0A;font-family:Inter}.clip{position:absolute;inset:0}.base-video{width:100%;height:100%;object-fit:cover;z-index:0}.graphic-host{z-index:5;pointer-events:none}#handle{position:absolute;inset:auto auto auto 48px;top:56px;z-index:16;width:max-content;padding:10px 14px 8px;border:3px solid #FFFFFF;background:#0A0A0A;color:#FFFFFF;font-size:22px;font-weight:740;letter-spacing:.02em;line-height:1;pointer-events:none}.caption-host{z-index:20;pointer-events:none}`;
save("index.html", `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><script src="./node_modules/gsap/dist/gsap.min.js"></script><style>${fonts("./")}${rootCss}</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="${duration}" data-fps="60">${media}${hosts}<div id="handle" class="clip" data-start="0" data-duration="${duration}" data-track-index="16" data-track-kind="graphics">@pedro.miyasaki.ia</div><div id="slot-captions" class="clip caption-host" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="${duration}" data-width="1080" data-height="1920" data-track-index="20" data-track-kind="captions"></div></div><script>const tl=gsap.timeline({paused:true});tl.to({},{duration:${duration},ease:'none'},0);window.__timelines['main']=tl;</script></body></html>`);
json("timeline-plan.json", { duration, ratings, voices: items.map((item) => ({ id: item.id, start: round(item.start + item.voiceAt), end: round(item.start + item.voiceAt + item.voiceDuration), pedroStarts: round(item.start + item.speechAt) })) });
console.log(JSON.stringify({ duration, removed: round(186.95 - duration), originalWords: originalWords.length, allPedroWordsPreserved: true, wifeWords: editedWords.filter((w) => w.speaker === "esposa").length, captions: captions.length, ratings }, null, 2));
