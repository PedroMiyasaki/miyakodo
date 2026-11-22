import fs from "node:fs";
import path from "node:path";

const projectDir = path.resolve(import.meta.dirname, "..");
const plan = JSON.parse(
  fs.readFileSync(path.join(projectDir, "edit-plan.json"), "utf8"),
);
const transcript = JSON.parse(
  fs.readFileSync(path.join(projectDir, "transcript-edited.json"), "utf8"),
);

const escapeHtml = (value) =>
  value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

const explanatoryScenes = [
  { id: "a-contratos", start: 22.6, duration: 11.3 },
  { id: "c-prompt", start: 36.16, duration: 12.84 },
  { id: "e-demais", start: 54.8, duration: 4.8 },
  { id: "e-rele", start: 62.6, duration: 3.0 },
  { id: "f-faltou", start: 67.6, duration: 7.2 },
  { id: "g-fix", start: 82, duration: 7.9 },
  { id: "h-marcada", start: 95.8, duration: 6.0 },
  { id: "i-cinquenta", start: 103.2, duration: 5.2 },
  { id: "i-golden", start: 110.2, duration: 2.2 },
  { id: "j-muda", start: 119.8, duration: 14.6 },
  { id: "k-metrica", start: 137.12, duration: 3.2 },
  { id: "k-direcao", start: 142.82, duration: 8.4 },
  { id: "l-xyz", start: 167.0, duration: 4.2 },
  { id: "m-sub", start: 178.2, duration: 8.2 },
];

const sceneHosts = explanatoryScenes
  .map(
    (scene) => `      <div
        id="slot-${scene.id}"
        class="clip scene-host"
        data-composition-id="${scene.id}"
        data-composition-src="compositions/frames/${scene.id}.html"
        data-start="${scene.start}"
        data-duration="${scene.duration}"
        data-track-index="5"
      ></div>`,
  )
  .join("\n\n");

const captionDir = path.join(projectDir, "compositions", "captions");
fs.mkdirSync(captionDir, { recursive: true });

const captionHosts = plan.chapters
  .map((chapter, chapterIndex) => {
    const compositionId = `captions-${String(chapterIndex + 1).padStart(2, "0")}`;
    const chapterCaptions = transcript.captions
      .map((caption, captionIndex) => ({ caption, captionIndex }))
      .filter(
        ({ caption }) =>
          caption.start >= chapter.start && caption.start < chapter.end,
      );

    const clips = chapterCaptions
      .map(({ caption, captionIndex }, localIndex) => {
        const next = transcript.captions[captionIndex + 1];
        const displayEnd = next
          ? Math.max(caption.end, next.start - 0.025)
          : caption.end + 0.12;
        const localStart = Math.round((caption.start - chapter.start) * 1000) / 1000;
        const localEnd = Math.min(chapter.duration, displayEnd - chapter.start);
        const duration =
          Math.round(Math.max(0.12, localEnd - localStart) * 1000) / 1000;
        const words = caption.words
          .map(
            (word, wordIndex) =>
              `<span id="${compositionId}-caption-${localIndex}-word-${wordIndex}" class="caption-word">${escapeHtml(word.text)}</span>`,
          )
          .join(" ");

        return `    <div
      id="${compositionId}-caption-${localIndex}"
      class="clip caption-box"
      data-start="${localStart}"
      data-duration="${duration}"
      data-track-index="0"
      data-layout-allow-caption-zone
    >${words}</div>`;
      })
      .join("\n");

    const wordTimeline = chapterCaptions
      .flatMap(({ caption }, localIndex) =>
        caption.words.flatMap((word, wordIndex) => {
          const selector = `#${compositionId}-caption-${localIndex}-word-${wordIndex}`;
          const start =
            Math.round((word.start - chapter.start) * 1000) / 1000;
          const end = Math.round((word.end - chapter.start) * 1000) / 1000;
          return [
            `    timeline.set("${selector}", { color: "#0A0A0A", backgroundColor: "#FFFFFF" }, ${start});`,
            `    timeline.set("${selector}", { color: "#FFFFFF", backgroundColor: "transparent" }, ${end});`,
          ];
        }),
      )
      .join("\n");

    const captionComposition = `<template>
  <style>
    @font-face {
      font-family: "Inter";
      src: url("node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2") format("woff2");
      font-style: normal;
      font-weight: 100 900;
    }

    #root {
      position: relative;
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: "Inter", sans-serif;
      pointer-events: none;
    }

    .caption-box {
      position: absolute;
      inset: auto 72px 238px;
      width: max-content;
      max-width: 936px;
      margin: 0 auto;
      padding: 18px 24px 15px;
      border: 4px solid #FFFFFF;
      background: #0A0A0A;
      box-shadow: 9px 9px 0 rgba(10, 10, 10, 0.8);
      color: #FFFFFF;
      font-size: 48px;
      font-weight: 650;
      letter-spacing: -0.025em;
      line-height: 1.12;
      text-align: center;
      text-wrap: balance;
    }

    .caption-word {
      display: inline;
      padding: 1px 2px 0;
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
    }
  </style>

  <div
    id="root"
    data-composition-id="${compositionId}"
    data-width="1080"
    data-height="1920"
    data-duration="${chapter.duration}"
  >
${clips}
  </div>

  <script>
    const timeline = gsap.timeline({ paused: true });
${wordTimeline}
    window.__timelines["${compositionId}"] = timeline;
  </script>
</template>
`;

    fs.writeFileSync(
      path.join(captionDir, `${compositionId}.html`),
      captionComposition,
    );

    return `      <div
        id="slot-${compositionId}"
        class="clip caption-host"
        data-composition-id="${compositionId}"
        data-composition-src="compositions/captions/${compositionId}.html"
        data-start="${chapter.start}"
        data-duration="${chapter.duration}"
        data-track-index="20"
        data-track-kind="captions"
      ></div>`;
  })
  .join("\n\n");

const html = `<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="./node_modules/gsap/dist/gsap.min.js"></script>
    <style>
      @font-face {
        font-family: "Bricolage Grotesque";
        src: url("./node_modules/@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-wght-normal.woff2") format("woff2");
        font-style: normal;
        font-weight: 200 800;
      }

      @font-face {
        font-family: "Inter";
        src: url("./node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2") format("woff2");
        font-style: normal;
        font-weight: 100 900;
      }

      * {
        box-sizing: border-box;
      }

      html,
      body {
        width: 1080px;
        height: 1920px;
        margin: 0;
        overflow: hidden;
        background: #0A0A0A;
      }

      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #0A0A0A;
        font-family: "Inter", sans-serif;
      }

      .clip,
      .scene-host {
        position: absolute;
        inset: 0;
      }

      #video-shell {
        position: absolute;
        inset: 0;
        z-index: 0;
        overflow: hidden;
      }

      #base-video {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .scene-host {
        z-index: 5;
        pointer-events: none;
      }

      #handle {
        position: absolute;
        inset: auto auto auto 48px;
        top: 56px;
        z-index: 16;
        width: max-content;
        padding: 10px 14px 8px;
        border: 3px solid #FFFFFF;
        background: #0A0A0A;
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 740;
        letter-spacing: 0.02em;
        line-height: 1;
        pointer-events: none;
      }

      .caption-host {
        z-index: 20;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-width="1080"
      data-height="1920"
      data-duration="${plan.duration}"
      data-fps="60"
    >
      <div id="video-shell">
        <video
          id="base-video"
          src="assets/evals-cut-sdr.mp4"
          data-start="0"
          data-duration="${plan.duration}"
          data-track-index="0"
          muted
          playsinline
        ></video>
      </div>

      <audio
        id="voice-audio"
        src="assets/evals-cut-audio.m4a"
        data-start="0"
        data-duration="${plan.duration}"
        data-track-index="30"
        data-volume="1"
      ></audio>

${sceneHosts}

${captionHosts}

      <div
        id="slot-business-disclaimer"
        class="clip scene-host"
        data-composition-id="business-disclaimer"
        data-composition-src="compositions/ui/business-disclaimer.html"
        data-start="151.86"
        data-duration="4"
        data-track-index="17"
      ></div>

      <div
        id="slot-comment-evals"
        class="clip scene-host"
        data-composition-id="comment-evals"
        data-composition-src="compositions/ui/comment-evals.html"
        data-start="199.85"
        data-duration="2.33"
        data-track-index="17"
      ></div>

      <div
        id="handle"
        class="clip"
        data-start="0.2"
        data-duration="${plan.duration - 0.2}"
        data-track-index="16"
      >@pedro.miyasaki.ia</div>
    </div>

    <script>
      const timeline = gsap.timeline({ paused: true });
      timeline.set("#video-shell", { opacity: 1 }, ${plan.duration});

      window.__timelines["main"] = timeline;
    </script>
  </body>
</html>
`;

fs.writeFileSync(path.join(projectDir, "index.html"), html);
console.log(
  `Assembled ${explanatoryScenes.length} explanatory frames and ${transcript.captions.length} caption clips (${plan.duration}s).`,
);
