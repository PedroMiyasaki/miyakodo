import fs from "node:fs";
import path from "node:path";

const framesDir = path.resolve(import.meta.dirname, "../compositions/frames");

const font = `@font-face {
      font-family: "Bricolage Grotesque";
      src: url("node_modules/@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-wght-normal.woff2") format("woff2");
      font-weight: 200 800;
    }`;

const base = `#root {
      position: relative;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #0A0A0A;
      color: #FFFFFF;
      font-family: "Bricolage Grotesque", sans-serif;
    }
    #root > * { position: absolute; }
    #root::before {
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 4;
      opacity: 0.14;
      background-image: radial-gradient(#FFFFFF 0.6px, transparent 0.7px);
      background-size: 4px 4px;
    }
    .label {
      position: absolute;
      font-weight: 800;
      letter-spacing: -0.05em;
      line-height: 0.9;
    }
    .off { opacity: 0; }
    .sheet {
      position: absolute;
      border: 7px solid #FFFFFF;
      background: #0A0A0A;
      box-sizing: border-box;
    }
    .fold {
      position: absolute;
      top: -1px;
      right: -1px;
      width: 0;
      height: 0;
      border-style: solid;
      border-width: 0 42px 42px 0;
      border-color: transparent #FFFFFF transparent transparent;
    }
    .rule {
      height: 8px;
      margin: 22px 22px 0;
      background: #FFFFFF;
      transform-origin: left center;
      transform: scaleX(0);
    }
    .rule.short { width: 58%; }
    .draw {
      transform-origin: left center;
      transform: scaleX(0);
    }
    svg .ink {
      fill: none;
      stroke: #FFFFFF;
      stroke-width: 7;
      stroke-linecap: square;
      stroke-linejoin: miter;
    }`;

const wrap = (id, duration, css, body, motion) => `<template>
  <style>
    ${font}
    ${base}
    ${css}
  </style>
  <div id="root" data-composition-id="${id}" data-width="1080" data-height="1920" data-duration="${duration}">
${body}
  </div>
  <script>
    const timeline = gsap.timeline({ paused: true });
    const byId = (name) => document.getElementById(name);
${motion}
    window.__timelines = window.__timelines || {};
    window.__timelines["${id}"] = timeline;
  </script>
</template>
`;

const scenes = [];

scenes.push({
  id: "a-contratos",
  duration: 11.3,
  hero: "#a-doc0",
  bySec: 0.8,
  css: `#a-title { left: 72px; top: 200px; font-size: 64px; }
 .a-paper { position: absolute; left: 120px; width: 210px; height: 270px; padding: 28px 22px; border: 6px solid #FFFFFF; background: #0A0A0A; box-sizing: border-box; }
 #a-doc0 { top: 390px; } #a-doc1 { top: 710px; } #a-doc2 { top: 1030px; }
 .a-paper b { font-size: 40px; } .a-line { height: 7px; margin-top: 24px; background: #FFFFFF; } .a-line:nth-child(3) { width: 70%; }
 .a-scan { position: absolute; left: -14px; top: 56px; width: 226px; height: 10px; background: #FFFFFF; box-shadow: 0 0 0 6px rgba(255,255,255,.12); opacity: 0; }
 #a-flow { position: absolute; left: 356px; top: 450px; }
 #a-output { left: 640px; top: 710px; width: 360px; height: 320px; padding: 26px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 #a-output-title { left: 640px; top: 560px; width: 360px; font-size: 46px; line-height: 1.1; }
 .a-clause { height: 16px; margin-top: 32px; background: #FFFFFF; transform-origin: left center; opacity: 0; }
 #a-clause1 { width: 82%; } #a-clause2 { width: 65%; }`,
  body: `    <div id="a-title" class="label off">CONTRATOS → CLÁUSULAS</div>
    <div id="a-doc0" class="a-paper off"><b>01</b><div class="a-line"></div><div class="a-line"></div><div class="a-line"></div><div id="a-scan0" class="a-scan"></div></div>
    <div id="a-doc1" class="a-paper off"><b>02</b><div class="a-line"></div><div class="a-line"></div><div class="a-line"></div><div id="a-scan1" class="a-scan"></div></div>
    <div id="a-doc2" class="a-paper off"><b>03</b><div class="a-line"></div><div class="a-line"></div><div class="a-line"></div><div id="a-scan2" class="a-scan"></div></div>
    <svg id="a-flow" class="off" width="256" height="760" viewBox="0 0 256 760"><path class="ink" d="M0 60 C150 60 50 380 220 380 M0 380 H220 M0 700 C150 700 50 380 220 380"></path><polyline class="ink" points="190,352 224,380 190,408"></polyline></svg>
    <div id="a-output-title" class="label off">CLÁUSULAS MAIS CRÍTICAS</div>
    <div id="a-output" class="off"><div id="a-clause0" class="a-clause"></div><div id="a-clause1" class="a-clause"></div><div id="a-clause2" class="a-clause"></div></div>`,
  motion: `    timeline.fromTo('#a-title', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, .1);
    timeline.fromTo('.a-paper', { opacity: 0, x: -28 }, { opacity: 1, x: 0, duration: .45, stagger: .5, ease: 'power3.out' }, .2);
    [0,1,2].forEach((i) => {
      timeline.fromTo('#a-scan'+i, { opacity: 0, y: 0 }, { opacity: 1, y: 145, duration: .95, ease: 'power1.inOut' }, 2.7+i*1.1);
      timeline.to('#a-scan'+i, { opacity: 0, duration: .15 }, 3.65+i*1.1);
    });
    timeline.fromTo('#a-flow', { opacity: 0 }, { opacity: 1, duration: .4 }, 6.1);
    timeline.fromTo('#a-output, #a-output-title', { opacity: 0, x: 22 }, { opacity: 1, x: 0, duration: .45 }, 6.8);
    timeline.fromTo('.a-clause', { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .45, stagger: .6, ease: 'power2.out' }, 7.35);`,
});

scenes.push({
  id: "b-clausula",
  duration: 4.3,
  hero: "#contract",
  bySec: 0.7,
  css: `#contract { left: 120px; top: 280px; width: 520px; height: 700px; }
    #contract .rule { height: 12px; margin-top: 36px; }
    #hot { position: absolute; left: 168px; top: 468px; width: 400px; height: 26px; background: #FFFFFF; }
    #ring { position: absolute; left: 148px; top: 440px; }
    #link { position: absolute; left: 660px; top: 456px; }
    #tag { left: 700px; top: 300px; font-size: 64px; padding: 14px 18px 10px; background: #FFFFFF; color: #0A0A0A; }`,
  body: `    <div id="contract" class="sheet off"><div class="fold"></div><div class="rule"></div><div class="rule short"></div><div class="rule"></div><div class="rule"></div><div class="rule short"></div><div class="rule"></div><div class="rule short"></div></div>
    <div id="hot" class="draw off"></div>
    <svg id="ring" class="off" width="460" height="90" viewBox="0 0 460 90"><rect class="ink" id="ring-path" x="8" y="8" width="444" height="74" stroke-dasharray="1040" stroke-dashoffset="1040"></rect></svg>
    <svg id="link" class="off" width="280" height="40" viewBox="0 0 280 40"><line class="ink" x1="0" y1="20" x2="250" y2="20"></line><polyline class="ink" points="230,4 262,20 230,36"></polyline></svg>
    <div id="tag" class="label off">CRÍTICA</div>`,
  motion: `    timeline.fromTo(byId("contract"), { opacity: 0, y: 40, rotation: -2 }, { opacity: 1, y: 0, rotation: -1, duration: 0.45, ease: "power3.out" }, 0.1);
    timeline.fromTo("#contract .rule", { scaleX: 0 }, { scaleX: 1, duration: 0.25, stagger: 0.08, ease: "power2.out" }, 0.45);
    timeline.fromTo(byId("hot"), { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.35, ease: "power2.out" }, 1.7);
    timeline.fromTo(byId("ring"), { opacity: 0 }, { opacity: 1, duration: 0.1 }, 2.1);
    timeline.fromTo("#ring-path", { strokeDashoffset: 1040 }, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, 2.1);
    timeline.fromTo(byId("link"), { opacity: 0 }, { opacity: 1, duration: 0.15 }, 2.55);
    timeline.fromTo(byId("tag"), { opacity: 0, scale: 1.4, rotation: 8 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.35, ease: "back.out(1.7)" }, 2.9);`,
});

scenes.push({
  id: "c-prompt",
  duration: 12.84,
  hero: "#c-agent",
  bySec: 0.7,
  css: `#c-title { left: 72px; top: 240px; font-size: 72px; }
 #c-agent { left: 72px; top: 600px; width: 320px; height: 470px; padding: 28px 24px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 #c-agent-name { font-size: 50px; font-weight: 800; }
 #c-prompt { position: absolute; left: 20px; right: 20px; top: 134px; height: 280px; border: 3px solid #FFFFFF; padding: 22px 18px; box-sizing: border-box; }
 #c-prompt b { font-size: 40px; } .c-copy { height: 9px; margin-top: 24px; background: #FFFFFF; transform-origin: left center; }
 .c-copy:nth-last-child(2) { width: 75%; }
 #c-contract { left: 494px; top: 680px; width: 190px; height: 300px; padding: 22px 18px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 #c-contract-name { left: 450px; top: 600px; width: 280px; font-size: 40px; text-align: center; }
 #c-out { left: 804px; top: 680px; width: 204px; height: 300px; padding: 20px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 #c-out-name { left: 752px; top: 550px; width: 280px; font-size: 40px; line-height: 1.1; }
 .c-red { height: 9px; margin-top: 26px; background: #FF6B6B; transform-origin: left center; opacity: 0; }
 #c-arrow1 { left: 407px; top: 800px; } #c-arrow2 { left: 706px; top: 800px; }
 .c-arrow { position: absolute; }`,
  body: `    <div id="c-title" class="label off">DO PROMPT À RESPOSTA</div>
    <div id="c-agent" class="off"><div id="c-agent-name">AGENTE</div><div id="c-prompt" class="off"><b>PROMPT</b><div class="c-copy"></div><div class="c-copy"></div><div class="c-copy"></div><div class="c-copy"></div></div></div>
    <svg id="c-arrow1" class="c-arrow off" width="68" height="50" viewBox="0 0 68 50"><path class="ink" d="M0 25 H58 M40 7 L60 25 L40 43"></path></svg>
    <div id="c-contract-name" class="label off">CONTRATO</div><div id="c-contract" class="off"><div class="c-copy"></div><div class="c-copy"></div><div class="c-copy"></div><div class="c-copy"></div><div class="c-copy"></div></div>
    <svg id="c-arrow2" class="c-arrow off" width="76" height="50" viewBox="0 0 76 50"><path class="ink" d="M0 25 H66 M46 7 L68 25 L46 43"></path></svg>
    <div id="c-out-name" class="label off">CLÁUSULAS IMPORTANTES</div><div id="c-out" class="off"><div class="c-red"></div><div class="c-red"></div><div class="c-red"></div><div class="c-red"></div><div class="c-red"></div></div>`,
  motion: `    timeline.fromTo('#c-title, #c-agent', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .4, stagger: .12 }, .1);
    timeline.fromTo('#c-prompt', { opacity: 0 }, { opacity: 1, duration: .3 }, 1.05);
    timeline.fromTo('#c-prompt .c-copy', { scaleX: 0 }, { scaleX: 1, duration: .3, stagger: .32 }, 1.45);
    timeline.fromTo('#c-arrow1', { opacity: 0 }, { opacity: 1, duration: .3 }, 6.5);
    timeline.fromTo('#c-contract, #c-contract-name', { opacity: 0, x: 18 }, { opacity: 1, x: 0, duration: .35 }, 7.05);
    timeline.fromTo('#c-arrow2', { opacity: 0 }, { opacity: 1, duration: .3 }, 9.0);
    timeline.fromTo('#c-out, #c-out-name', { opacity: 0 }, { opacity: 1, duration: .35 }, 9.4);
    timeline.fromTo('.c-red', { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .25, stagger: .2, ease: 'power2.out' }, 9.75);`,
});

scenes.push({
  id: "d-resposta",
  duration: 4.6,
  hero: "#mini",
  bySec: 0.7,
  css: `#mini { left: 90px; top: 520px; width: 250px; height: 330px; }
    #to-q { position: absolute; left: 360px; top: 650px; }
    #bubble { position: absolute; left: 560px; top: 430px; }
    #mark { position: absolute; left: 655px; top: 560px; width: 220px; text-align: center; font-size: 220px; font-weight: 800; line-height: 1; }`,
  body: `    <div id="mini" class="sheet off"><div class="fold"></div><div class="rule"></div><div class="rule short"></div><div class="rule"></div><div class="rule short"></div><div class="rule"></div></div>
    <svg id="to-q" class="off" width="200" height="40" viewBox="0 0 200 40"><line class="ink" x1="0" y1="20" x2="168" y2="20"></line><polyline class="ink" points="148,4 176,20 148,36"></polyline></svg>
    <svg id="bubble" class="off" width="420" height="420" viewBox="0 0 420 420"><circle class="ink" id="bubble-path" cx="210" cy="210" r="180" stroke-dasharray="1140" stroke-dashoffset="1140"></circle></svg>
    <div id="mark" class="label off">?</div>`,
  motion: `    timeline.fromTo(byId("mini"), { opacity: 0, y: 36, rotation: -4 }, { opacity: 1, y: 0, rotation: -2, duration: 0.4, ease: "power3.out" }, 0.12);
    timeline.fromTo("#mini .rule", { scaleX: 0 }, { scaleX: 1, duration: 0.22, stagger: 0.06 }, 0.4);
    timeline.fromTo(byId("to-q"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0.85);
    timeline.fromTo(byId("bubble"), { opacity: 0 }, { opacity: 1, duration: 0.1 }, 1.15);
    timeline.fromTo("#bubble-path", { strokeDashoffset: 1140 }, { strokeDashoffset: 0, duration: 0.55, ease: "power2.out" }, 1.15);
    timeline.fromTo(byId("mark"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, 1.7);
    timeline.to(byId("mark"), { rotation: 4, duration: 0.1, yoyo: true, repeat: 5, ease: "power1.inOut" }, 2.3);`,
});

scenes.push({
  id: "e-demais",
  duration: 4.8,
  hero: "#e-valid",
  bySec: 0.6,
  css: `#e-title { left: 72px; top: 220px; font-size: 72px; }
 #e-valid { left: 170px; top: 430px; width: 740px; height: 320px; border: 6px solid #5BD6A2; box-sizing: border-box; }
 #e-valid-name { left: 205px; top: 455px; font-size: 40px; }
 .e-bar { position: absolute; left: 215px; width: 650px; height: 24px; transform-origin: left center; }
 #e-good0 { top: 545px; background: #5BD6A2; } #e-good1 { top: 615px; width: 480px; background: #5BD6A2; } #e-good2 { top: 685px; width: 580px; background: #5BD6A2; }
 #e-limit { position: absolute; left: 150px; top: 778px; width: 780px; border-top: 6px dashed #FF6B6B; }
 #e-extra0 { top: 845px; background: #FF6B6B; } #e-extra1 { top: 915px; width: 550px; background: #FF6B6B; } #e-extra2 { top: 985px; width: 420px; background: #FF6B6B; }
 #e-excess { left: 215px; top: 1090px; color: #FF6B6B; font-size: 88px; }`,
  body: `    <div id="e-title" class="label off">SAÍDA DO AGENTE</div>
    <div id="e-valid" class="off"></div><div id="e-valid-name" class="label off">CLÁUSULAS RELEVANTES</div>
    <div id="e-good0" class="e-bar off"></div><div id="e-good1" class="e-bar off"></div><div id="e-good2" class="e-bar off"></div>
    <div id="e-limit" class="off"></div>
    <div id="e-extra0" class="e-bar off"></div><div id="e-extra1" class="e-bar off"></div><div id="e-extra2" class="e-bar off"></div>
    <div id="e-excess" class="label off">DEMAIS</div>`,
  motion: `    timeline.fromTo('#e-title, #e-valid, #e-valid-name', { opacity: 0 }, { opacity: 1, duration: .3, stagger: .08 }, .1);
    timeline.fromTo('#e-good0, #e-good1, #e-good2', { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .3, stagger: .3, ease: 'power2.out' }, .6);
    timeline.fromTo('#e-limit', { opacity: 0 }, { opacity: 1, duration: .25 }, 1.8);
    timeline.fromTo('#e-extra0, #e-extra1, #e-extra2', { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .3, stagger: .35, ease: 'power2.out' }, 2.15);
    timeline.fromTo('#e-excess', { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: .35 }, 3.45);`,
});

scenes.push({
  id: "e-rele",
  duration: 3,
  hero: "#er-result",
  bySec: 0.2,
  css: `#er-result { left: 220px; top: 300px; width: 640px; height: 290px; border: 6px solid #FFFFFF; padding: 32px; box-sizing: border-box; }
 .er-line { height: 16px; margin-bottom: 35px; background: #5BD6A2; }
 .er-line:last-child { background: #FF6B6B; width: 80%; }
 #er-loop { position: absolute; left: 360px; top: 740px; }
 #er-label { left: 160px; top: 1190px; width: 760px; font-size: 80px; text-align: center; }`,
  body: `    <div id="er-result"><div class="er-line"></div><div class="er-line"></div><div class="er-line"></div><div class="er-line"></div></div>
    <svg id="er-loop" class="off" width="360" height="360" viewBox="0 0 360 360"><defs><marker id="er-head" markerWidth="44" markerHeight="44" refX="30" refY="22" viewBox="0 0 44 44" markerUnits="userSpaceOnUse" orient="auto"><path id="er-arrowhead" fill="#FFFFFF" opacity="0" d="M2 2 L42 22 L2 42 Z"></path></marker></defs><path class="ink" id="er-loop-path" d="M180 45 A135 135 0 1 1 65 109" stroke-dasharray="790" stroke-dashoffset="790" marker-end="url(#er-head)"></path></svg>
    <div id="er-label" class="label off">RE-TRABALHO</div>`,
  motion: `    timeline.fromTo('#er-loop', { opacity: 0 }, { opacity: 1, duration: .2 }, .15);
    timeline.fromTo('#er-loop-path', { strokeDashoffset: 790 }, { strokeDashoffset: 0, duration: 1.15, ease: 'power1.inOut' }, .2);
    timeline.to('#er-arrowhead', { opacity: 1, duration: .15 }, 1.2);
    timeline.fromTo('#er-label', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .3 }, 1.4);`,
});

scenes.push({
  id: "f-faltou",
  duration: 7.2,
  hero: "#f-expected",
  bySec: 0.8,
  css: `#f-title { left: 72px; top: 220px; font-size: 72px; }
 #f-left-name { left: 92px; top: 460px; font-size: 44px; } #f-right-name { left: 630px; top: 460px; font-size: 44px; }
 .f-paper { position: absolute; top: 550px; width: 340px; height: 540px; padding: 44px 24px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 #f-expected { left: 92px; } #f-answer { left: 630px; }
 .f-row { position: absolute; left: 24px; right: 24px; height: 90px; display: flex; align-items: center; font-size: 40px; font-weight: 800; border-bottom: 4px solid #FFFFFF; box-sizing: border-box; opacity: 0; }
 .f-row:nth-child(1) { top: 55px; } .f-row:nth-child(2) { top: 215px; } .f-row:nth-child(3) { top: 375px; }
 #f-gap { color: #FF6B6B; border: 5px dashed #FF6B6B; justify-content: center; font-size: 40px; }
 #f-source2 { color: #FF6B6B; }
 #f-arrow { left: 457px; top: 786px; position: absolute; }
 #f-missing { left: 92px; top: 1170px; width: 880px; text-align: center; font-size: 64px; color: #FF6B6B; }
 #f-again { left: 92px; top: 1320px; width: 880px; text-align: center; font-size: 44px; line-height: 1.2; }`,
  body: `    <div id="f-title" class="label off">O QUE FICOU DE FORA?</div>
    <div id="f-left-name" class="label off">GABARITO</div><div id="f-right-name" class="label off">RESPOSTA DO AGENTE</div>
    <div id="f-expected" class="f-paper off"><div class="f-row">CLÁUSULA 01</div><div id="f-source2" class="f-row">CLÁUSULA 02</div><div class="f-row">CLÁUSULA 03</div></div>
    <svg id="f-arrow" class="off" width="144" height="56" viewBox="0 0 144 56"><path class="ink" d="M0 28 H126 M104 6 L132 28 L104 50"></path></svg>
    <div id="f-answer" class="f-paper off"><div id="f-answer1" class="f-row">CLÁUSULA 01</div><div id="f-gap" class="f-row">AUSENTE</div><div id="f-answer3" class="f-row">CLÁUSULA 03</div></div>
    <div id="f-missing" class="label off">FALTOU A CLÁUSULA 02</div>
    <div id="f-again" class="label off">O TIME PRECISA CONFERIR O CONTRATO INTEIRO.</div>`,
  motion: `    timeline.fromTo('#f-title, #f-left-name, #f-right-name, .f-paper', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .35, stagger: .08 }, .1);
    timeline.fromTo('#f-expected .f-row', { opacity: 0, x: -12 }, { opacity: 1, x: 0, duration: .3, stagger: .25 }, .75);
    timeline.fromTo('#f-arrow', { opacity: 0 }, { opacity: 1, duration: .25 }, 1.55);
    timeline.fromTo('#f-answer1, #f-answer3', { opacity: 0, x: -12 }, { opacity: 1, x: 0, duration: .3, stagger: .35 }, 1.9);
    timeline.fromTo('#f-gap', { opacity: 0 }, { opacity: 1, duration: .35 }, 3.0);
    timeline.fromTo('#f-missing', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, 3.55);
    timeline.fromTo('#f-again', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, 4.9);`,
});

scenes.push({
  id: "g-fix",
  duration: 7.9,
  hero: "#g-agent",
  bySec: 0.6,
  css: `#g-title { left: 72px; top: 200px; width: 936px; font-size: 64px; line-height: 1.1; }
 #g-agent { left: 250px; top: 380px; width: 580px; height: 250px; border: 6px solid #FFFFFF; box-sizing: border-box; padding: 28px; }
 #g-agent-name { font-size: 48px; font-weight: 800; }
 .g-prompt { position: absolute; left: 28px; top: 118px; width: 512px; padding: 22px 0; border-top: 3px solid #FFFFFF; font-size: 48px; font-weight: 800; text-align: center; }
 #g-prompt2 { background: #FFFFFF; color: #0A0A0A; }
 #g-branch { left: 168px; top: 664px; position: absolute; }
 #g-cases { position: absolute; left: 82px; top: 850px; display: flex; gap: 28px; }
 .g-case { position: relative; width: 208px; height: 260px; border: 5px solid #FFFFFF; box-sizing: border-box; text-align: center; padding-top: 25px; }
 .g-name { font-size: 40px; font-weight: 800; } .g-state { position: absolute; left: 0; top: 104px; width: 100%; font-size: 110px; font-weight: 800; line-height: 1; }
 .g-ok { color: #5BD6A2; } .g-bad { color: #FF6B6B; }
 #g-fixed { left: 82px; top: 1160px; width: 208px; text-align: center; font-size: 40px; color: #5BD6A2; }
 #g-regressed { left: 320px; top: 1160px; width: 680px; text-align: center; font-size: 48px; line-height: 1.15; color: #FF6B6B; }`,
  body: `    <div id="g-title" class="label off">UMA MUDANÇA NO SISTEMA</div>
    <div id="g-agent" class="off"><div id="g-agent-name">AGENTE</div><div id="g-prompt1" class="g-prompt">PROMPT V1</div><div id="g-prompt2" class="g-prompt off">PROMPT V2</div></div>
    <svg id="g-branch" class="off" width="744" height="154" viewBox="0 0 744 154"><path class="ink" d="M372 0 V45 M0 45 H744 M12 45 V135 M252 45 V135 M492 45 V135 M732 45 V135 M0 117 L12 138 L24 117 M240 117 L252 138 L264 117 M480 117 L492 138 L504 117 M720 117 L732 138 L744 117"></path></svg>
    <div id="g-cases" class="off">
      <div class="g-case"><div class="g-name">CASO 01</div><div id="g-first-bad" class="g-state g-bad">×</div><div id="g-first-ok" class="g-state g-ok off">✓</div></div>
      <div class="g-case"><div class="g-name">CASO 02</div><div class="g-state g-ok g-previous">✓</div><div class="g-state g-bad g-broken off">×</div></div>
      <div class="g-case"><div class="g-name">CASO 03</div><div class="g-state g-ok g-previous">✓</div><div class="g-state g-bad g-broken off">×</div></div>
      <div class="g-case"><div class="g-name">CASO 04</div><div class="g-state g-ok g-previous">✓</div><div class="g-state g-bad g-broken off">×</div></div>
    </div>
    <div id="g-fixed" class="label off">CORRIGIU</div><div id="g-regressed" class="label off">MAS OS OUTROS REGREDIRAM</div>`,
  motion: `    timeline.fromTo('#g-title, #g-agent, #g-branch, #g-cases', { opacity: 0 }, { opacity: 1, duration: .35, stagger: .1 }, .1);
    timeline.to('#g-prompt1', { opacity: 0, duration: .2 }, 1.15);
    timeline.fromTo('#g-prompt2', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .3 }, 1.35);
    timeline.to('#g-first-bad', { opacity: 0, duration: .2 }, 2.65);
    timeline.fromTo('#g-first-ok, #g-fixed', { opacity: 0 }, { opacity: 1, duration: .3 }, 2.85);
    timeline.to('.g-previous', { opacity: 0, duration: .18, stagger: .4 }, 4.2);
    timeline.fromTo('.g-broken', { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .25, stagger: .4, ease: 'power3.out' }, 4.4);
    timeline.fromTo('#g-regressed', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, 5.7);`,
});

scenes.push({
  id: "g-quebra",
  duration: 3.4,
  hero: "#kept",
  bySec: 0.2,
  css: `#kept { left: 80px; top: 200px; width: 460px; height: 140px; display: flex; align-items: center; justify-content: space-between; padding: 0 28px; font-size: 48px; font-weight: 800; }
    #kept b { font-size: 72px; }
    #down { position: absolute; left: 280px; top: 370px; }
    #cases { position: absolute; left: 70px; top: 560px; display: flex; gap: 22px; }
    .case { position: relative; width: 210px; height: 210px; border: 7px solid #FFFFFF; }
    .case span { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 110px; font-weight: 800; }
    .bad { opacity: 0; }
    #broke { left: 80px; top: 860px; font-size: 88px; }`,
  body: `    <div id="kept" class="sheet">ESSE CASO<b>✓</b></div>
    <svg id="down" width="40" height="140" viewBox="0 0 40 140"><line class="ink" x1="20" y1="0" x2="20" y2="110"></line><polyline class="ink" points="4,96 20,128 36,96"></polyline></svg>
    <div id="cases">
      <div class="case" id="case-a"><span class="ok">✓</span><span class="bad">×</span></div>
      <div class="case" id="case-b"><span class="ok">✓</span><span class="bad">×</span></div>
      <div class="case" id="case-c"><span class="ok">✓</span><span class="bad">×</span></div>
      <div class="case" id="case-d"><span class="ok">✓</span><span class="bad">×</span></div>
    </div>
    <div id="broke" class="label off">QUEBROU</div>`,
  motion: `    timeline.fromTo("#cases .bad", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.28, stagger: 0.22, ease: "back.out(1.7)" }, 0.35);
    timeline.to("#cases .ok", { opacity: 0, duration: 0.18, stagger: 0.22 }, 0.35);
    timeline.fromTo(byId("broke"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.3 }, 1.5);`,
});

scenes.push({
  id: "h-marcada",
  duration: 6,
  hero: "#h-doc0",
  bySec: 0.7,
  css: `#h-title { left: 72px; top: 190px; width: 936px; font-size: 64px; line-height: 1.1; }
 .h-row { position: absolute; left: 150px; width: 800px; height: 220px; }
 #h-row0 { top: 450px; } #h-row1 { top: 705px; } #h-row2 { top: 960px; } #h-row3 { top: 1215px; }
 .h-contract { position: absolute; left: 0; width: 380px; height: 220px; padding: 24px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 .h-contract b { font-size: 40px; } .h-copy { height: 8px; margin-top: 22px; background: #FFFFFF; } .h-copy:last-child { width: 70%; }
 .h-arrow { position: absolute; left: 415px; top: 76px; }
 .h-check { position: absolute; left: 610px; top: 22px; width: 180px; height: 180px; border: 6px solid #5BD6A2; display: flex; align-items: center; justify-content: center; font-size: 112px; color: #5BD6A2; font-weight: 800; box-sizing: border-box; opacity: 0; }`,
  body: `    <div id="h-title" class="label off">DATASET COM RESPOSTA MARCADA</div>
    <div id="h-row0" class="h-row"><div id="h-doc0" class="h-contract off"><b>CONTRATO 01</b><div class="h-copy"></div><div class="h-copy"></div><div class="h-copy"></div></div><svg id="h-arrow0" class="h-arrow off" width="170" height="56" viewBox="0 0 170 56"><path class="ink" d="M0 28 H146 M122 6 L154 28 L122 50"></path></svg><div id="h-check0" class="h-check">✓</div></div>
    <div id="h-row1" class="h-row"><div id="h-doc1" class="h-contract off"><b>CONTRATO 02</b><div class="h-copy"></div><div class="h-copy"></div><div class="h-copy"></div></div><svg id="h-arrow1" class="h-arrow off" width="170" height="56" viewBox="0 0 170 56"><path class="ink" d="M0 28 H146 M122 6 L154 28 L122 50"></path></svg><div id="h-check1" class="h-check">✓</div></div>
    <div id="h-row2" class="h-row"><div id="h-doc2" class="h-contract off"><b>CONTRATO 03</b><div class="h-copy"></div><div class="h-copy"></div><div class="h-copy"></div></div><svg id="h-arrow2" class="h-arrow off" width="170" height="56" viewBox="0 0 170 56"><path class="ink" d="M0 28 H146 M122 6 L154 28 L122 50"></path></svg><div id="h-check2" class="h-check">✓</div></div>
    <div id="h-row3" class="h-row"><div id="h-doc3" class="h-contract off"><b>CONTRATO 04</b><div class="h-copy"></div><div class="h-copy"></div><div class="h-copy"></div></div><svg id="h-arrow3" class="h-arrow off" width="170" height="56" viewBox="0 0 170 56"><path class="ink" d="M0 28 H146 M122 6 L154 28 L122 50"></path></svg><div id="h-check3" class="h-check">✓</div></div>`,
  motion: `    timeline.fromTo('#h-title', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, .1);
    [0,1,2,3].forEach((i) => {
      timeline.fromTo('#h-doc'+i, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: .35 }, .2+i*.65);
      timeline.fromTo('#h-arrow'+i, { opacity: 0 }, { opacity: 1, duration: .25 }, 1.2+i*.65);
      timeline.fromTo('#h-check'+i, { opacity: 0, scale: .8 }, { opacity: 1, scale: 1, duration: .35, ease: 'power3.out' }, 1.6+i*.65);
    });`,
});

const docs = Array.from({ length: 50 }, (_, index) => `<b id="doc-${index}"></b>`).join("");

scenes.push({
  id: "i-cinquenta",
  duration: 5.2,
  hero: "#fifty",
  bySec: 0.7,
  css: `#fifty { left: 80px; top: 160px; font-size: 200px; }
    #grid { position: absolute; left: 80px; top: 460px; width: 920px; display: grid; grid-template-columns: repeat(10, 1fr); gap: 12px; }
    #grid b { height: 72px; border: 4px solid #FFFFFF; opacity: 0; }`,
  body: `    <div id="fifty" class="label off">50</div>
    <div id="grid">${docs}</div>`,
  motion: `    timeline.fromTo(byId("fifty"), { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 0.12);
    timeline.fromTo("#grid b", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.22, stagger: 0.028, ease: "power2.out" }, 0.65);`,
});

scenes.push({
  id: "i-golden",
  duration: 2.2,
  hero: "#grid",
  bySec: 0.2,
  css: `#fifty { left: 80px; top: 150px; font-size: 140px; }
    #grid { position: absolute; left: 80px; top: 380px; width: 920px; display: grid; grid-template-columns: repeat(10, 1fr); gap: 12px; }
    #grid b { height: 64px; border: 4px solid #FFFFFF; }
    #golden { left: 80px; top: 980px; font-size: 72px; padding: 14px 18px 10px; background: #FFFFFF; color: #0A0A0A; }`,
  body: `    <div id="fifty" class="label">50</div>
    <div id="grid">${docs}</div>
    <div id="golden" class="label off">DATASET DE EVALS</div>`,
  motion: `    timeline.fromTo(byId("golden"), { opacity: 0, scale: 1.35, rotation: 6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.5)" }, 0.35);`,
});

scenes.push({
  id: "j-muda",
  duration: 14.6,
  hero: "#j-prompt",
  bySec: 0.7,
  css: `#j-title { left: 72px; top: 200px; width: 936px; font-size: 72px; }
 .j-config { position: absolute; top: 410px; width: 390px; height: 136px; border: 5px solid #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 48px; font-weight: 800; box-sizing: border-box; }
 #j-prompt { left: 100px; } #j-tools { left: 590px; }
 #j-loop { position: absolute; left: 430px; top: 625px; }
 #j-rerun { left: 72px; top: 890px; width: 936px; text-align: center; font-size: 60px; }
 #j-table { position: absolute; left: 130px; top: 1030px; width: 820px; }
 .j-row { display: grid; grid-template-columns: 240px 290px 290px; height: 72px; align-items: center; border-bottom: 3px solid #FFFFFF; font-size: 40px; font-weight: 800; text-align: center; }
 .j-row.j-head { height: 64px; font-size: 40px; }
 .j-answer { opacity: 0; color: #5BD6A2; font-size: 52px; }
 #j-stable { left: 130px; top: 1450px; width: 820px; text-align: center; font-size: 52px; color: #5BD6A2; }`,
  body: `    <div id="j-title" class="label off">MUDOU O SISTEMA?</div>
    <div id="j-prompt" class="j-config off">PROMPT</div><div id="j-tools" class="j-config off">TOOLS</div>
    <svg id="j-loop" class="off" width="220" height="220" viewBox="0 0 220 220"><path class="ink" id="j-loop-path" d="M110 30 A80 80 0 1 1 42 68" stroke-dasharray="470" stroke-dashoffset="470"></path><polygon fill="#FFFFFF" points="19,84 42,68 40,106"></polygon></svg>
    <div id="j-rerun" class="label off">RODAR EVALS DE NOVO</div>
    <div id="j-table" class="off"><div class="j-row j-head"><span>CASO</span><span>GABARITO</span><span>AGENTE</span></div><div class="j-row"><span>01</span><span>✓</span><span id="j-answer1" class="j-answer">✓</span></div><div class="j-row"><span>02</span><span>✓</span><span id="j-answer2" class="j-answer">✓</span></div><div class="j-row"><span>03</span><span>✓</span><span id="j-answer3" class="j-answer">✓</span></div><div class="j-row"><span>04</span><span>✓</span><span id="j-answer4" class="j-answer">✓</span></div></div>
    <div id="j-stable" class="label off">MESMAS RESPOSTAS. ESTÁVEL.</div>`,
  motion: `    timeline.fromTo('#j-title, #j-prompt', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35, stagger: .12 }, .1);
    timeline.to('#j-prompt', { backgroundColor: '#FFFFFF', color: '#0A0A0A', duration: .25 }, .9);
    timeline.fromTo('#j-tools', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, 2.0);
    timeline.to('#j-tools', { backgroundColor: '#FFFFFF', color: '#0A0A0A', duration: .25 }, 2.8);
    timeline.fromTo('#j-loop', { opacity: 0 }, { opacity: 1, duration: .2 }, 4.05);
    timeline.fromTo('#j-loop-path', { strokeDashoffset: 470 }, { strokeDashoffset: 0, duration: 1.15, ease: 'power1.inOut' }, 4.15);
    timeline.fromTo('#j-rerun', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .35 }, 5.25);
    timeline.fromTo('#j-table', { opacity: 0 }, { opacity: 1, duration: .35 }, 6.0);
    timeline.fromTo('.j-answer', { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .3, stagger: .65, ease: 'power3.out' }, 7.0);
    timeline.fromTo('#j-stable', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .35 }, 10.4);`,
});

const checks = Array.from({ length: 8 }, (_, index) => `<i id="check-${index}">✓</i>`).join("");

scenes.push({
  id: "j-roda",
  duration: 3.9,
  hero: "#changed-prompt",
  bySec: 0.2,
  css: `#changed-prompt, #changed-tools { width: 300px; height: 120px; display: flex; align-items: center; justify-content: center; font-size: 42px; font-weight: 800; }
    #changed-prompt { left: 80px; top: 180px; }
    #changed-tools { left: 420px; top: 180px; }
    #loop { position: absolute; left: 760px; top: 170px; }
    #rerun { left: 80px; top: 420px; font-size: 92px; }
    #checks { position: absolute; left: 80px; top: 620px; display: flex; gap: 16px; }
    #checks i { width: 88px; height: 88px; border: 5px solid #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 42px; font-weight: 800; opacity: 0; }
    #stable { left: 80px; top: 800px; width: 760px; height: 150px; display: flex; align-items: center; justify-content: space-between; padding: 0 28px; font-size: 72px; font-weight: 800; }
    #stable b { width: 90px; height: 90px; background: #FFFFFF; color: #0A0A0A; display: flex; align-items: center; justify-content: center; font-size: 60px; }`,
  body: `    <div id="changed-prompt" class="sheet">PROMPT</div>
    <div id="changed-tools" class="sheet">TOOLS</div>
    <svg id="loop" class="off" width="140" height="140" viewBox="0 0 140 140"><path class="ink" id="loop-path" d="M70 24 A 46 46 0 1 1 40 36" stroke-dasharray="280" stroke-dashoffset="280"></path><polyline class="ink" points="28,18 40,42 62,24"></polyline></svg>
    <div id="rerun" class="label off">RODA DE NOVO</div>
    <div id="checks">${checks}</div>
    <div id="stable" class="sheet off">ESTÁVEL<b>✓</b></div>`,
  motion: `    timeline.fromTo(byId("loop"), { opacity: 0 }, { opacity: 1, duration: 0.1 }, 0.15);
    timeline.fromTo("#loop-path", { strokeDashoffset: 280 }, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, 0.15);
    timeline.fromTo(byId("rerun"), { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 0.3 }, 0.55);
    timeline.fromTo("#checks i", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.2, stagger: 0.08, ease: "back.out(1.5)" }, 1.15);
    timeline.fromTo(byId("stable"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 2.85);`,
});

scenes.push({
  id: "k-metrica",
  duration: 3.2,
  hero: "#k1-card",
  bySec: 0.5,
  css: `#k1-card { left: 120px; top: 680px; width: 840px; height: 190px; border: 6px solid #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 64px; font-weight: 800; box-sizing: border-box; }`,
  body: `    <div id="k1-card" class="off">1. Métrica Objetiva</div>`,
  motion: `    timeline.fromTo('#k1-card', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .35, ease: 'power3.out' }, .1);`,
});

scenes.push({
  id: "k-direcao",
  duration: 8.4,
  hero: "#k2-card",
  bySec: 0.5,
  css: `#k2-card { left: 250px; top: 680px; width: 580px; height: 190px; border: 6px solid #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 64px; font-weight: 800; box-sizing: border-box; }
 #k2-chart { position: absolute; left: 110px; top: 620px; }
 #k2-higher { left: 110px; top: 1340px; width: 860px; text-align: center; font-size: 52px; }`,
  body: `    <div id="k2-card" class="off">2. Direção</div>
    <svg id="k2-chart" class="off" width="860" height="640" viewBox="0 0 860 640"><path class="ink" d="M70 30 V570 H820"></path><polyline class="ink" id="k2-trend" points="110,510 330,390 550,270 760,100" stroke-dasharray="840" stroke-dashoffset="840"></polyline><circle id="k2-p0" class="off" cx="110" cy="510" r="13" fill="#FFFFFF"></circle><circle id="k2-p1" class="off" cx="330" cy="390" r="13" fill="#FFFFFF"></circle><circle id="k2-p2" class="off" cx="550" cy="270" r="13" fill="#FFFFFF"></circle><circle id="k2-p3" class="off" cx="760" cy="100" r="13" fill="#FFFFFF"></circle></svg>
    <div id="k2-higher" class="label off">NOTAS CADA VEZ MAIS ALTAS</div>`,
  motion: `    timeline.fromTo('#k2-card', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .35, ease: 'power3.out' }, .1);
    timeline.to('#k2-card', { y: -340, duration: .65, ease: 'power2.inOut' }, 2.25);
    timeline.fromTo('#k2-chart', { opacity: 0 }, { opacity: 1, duration: .3 }, 3.05);
    timeline.fromTo('#k2-trend', { strokeDashoffset: 840 }, { strokeDashoffset: 0, duration: 2.0, ease: 'power1.inOut' }, 4.35);
    timeline.fromTo('#k2-p0, #k2-p1, #k2-p2, #k2-p3', { opacity: 0 }, { opacity: 1, duration: .2, stagger: .6 }, 4.5);
    timeline.fromTo('#k2-higher', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .35 }, 6.4);`,
});

scenes.push({
  id: "l-xyz",
  duration: 4.2,
  hero: "#l-rule",
  bySec: 0.6,
  css: `#l-title { left: 72px; top: 200px; width: 936px; font-size: 72px; }
 #l-rule { left: 220px; top: 400px; width: 640px; height: 170px; border: 6px solid #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 52px; font-weight: 800; box-sizing: border-box; }
 #l-branch { position: absolute; left: 185px; top: 620px; }
 .l-case { position: absolute; top: 840px; width: 190px; height: 280px; padding: 26px 18px; border: 6px solid #FFFFFF; box-sizing: border-box; }
 #l-x { left: 112px; } #l-y { left: 434px; } #l-z { left: 756px; }
 .l-case b { font-size: 44px; } .l-copy { height: 8px; margin-top: 24px; background: #FFFFFF; } .l-copy:last-child { width: 70%; }
 .l-broken { position: absolute; top: 910px; width: 70px; font-size: 104px; color: #FF6B6B; font-weight: 800; line-height: 1; }
 #l-bad-x { left: 318px; } #l-bad-y { left: 640px; } #l-bad-z { left: 962px; }
 #l-label { left: 112px; top: 1250px; width: 856px; font-size: 60px; text-align: center; color: #FF6B6B; }`,
  body: `    <div id="l-title" class="label off">ESSA REGRA ESTÁ CERTA?</div><div id="l-rule" class="off">REGRA DE NEGÓCIO</div>
    <svg id="l-branch" class="off" width="688" height="174" viewBox="0 0 688 174"><path class="ink" d="M344 0 V50 M22 50 H666 M22 50 V150 M344 50 V150 M666 50 V150 M2 138 L22 158 L42 138 M324 138 L344 158 L364 138 M646 138 L666 158 L686 138"></path></svg>
    <div id="l-x" class="l-case off"><b>CASO X</b><div class="l-copy"></div><div class="l-copy"></div><div class="l-copy"></div></div><div id="l-bad-x" class="l-broken off">×</div>
    <div id="l-y" class="l-case off"><b>CASO Y</b><div class="l-copy"></div><div class="l-copy"></div><div class="l-copy"></div></div><div id="l-bad-y" class="l-broken off">×</div>
    <div id="l-z" class="l-case off"><b>CASO Z</b><div class="l-copy"></div><div class="l-copy"></div><div class="l-copy"></div></div><div id="l-bad-z" class="l-broken off">×</div>
    <div id="l-label" class="label off">QUEBROU X, Y E Z</div>`,
  motion: `    timeline.fromTo('#l-title, #l-rule', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35, stagger: .1 }, .1);
    timeline.fromTo('#l-branch', { opacity: 0 }, { opacity: 1, duration: .25 }, .75);
    timeline.fromTo('.l-case', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .3, stagger: .3 }, 1.15);
    timeline.fromTo('.l-broken', { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .25, stagger: .3, ease: 'power3.out' }, 1.6);
    timeline.fromTo('#l-label', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .3 }, 2.65);`,
});

scenes.push({
  id: "m-sub",
  duration: 8.2,
  hero: "#m-subjective",
  bySec: 0.7,
  css: `#m-title { left: 72px; top: 200px; width: 936px; font-size: 64px; }
 .m-before { position: absolute; top: 420px; width: 420px; height: 170px; border: 5px solid #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 52px; font-weight: 800; box-sizing: border-box; }
 #m-subjective { left: 72px; } #m-reactive { left: 588px; }
 #m-converge { position: absolute; left: 280px; top: 620px; }
 #m-evals { left: 380px; top: 830px; width: 320px; height: 140px; background: #FFFFFF; color: #0A0A0A; display: flex; align-items: center; justify-content: center; font-size: 64px; font-weight: 800; }
 #m-route { position: absolute; left: 130px; top: 1090px; }
 .m-pass { position: absolute; width: 76px; height: 76px; border: 5px solid #5BD6A2; background: #0A0A0A; color: #5BD6A2; display: flex; align-items: center; justify-content: center; font-size: 48px; font-weight: 800; box-sizing: border-box; }
 #m-pass0 { left: 175px; top: 1180px; } #m-pass1 { left: 405px; top: 1130px; } #m-pass2 { left: 635px; top: 1080px; }
 #m-direction { left: 72px; top: 1330px; width: 936px; text-align: center; font-size: 80px; }
 #m-method { left: 72px; top: 1450px; width: 936px; text-align: center; font-size: 44px; }`,
  body: `    <div id="m-title" class="label off">DE REAGIR A EVOLUIR</div>
    <div id="m-subjective" class="m-before off">SUBJETIVO</div><div id="m-reactive" class="m-before off">REATIVO</div>
    <svg id="m-converge" class="off" width="520" height="174" viewBox="0 0 520 174"><path class="ink" d="M0 0 L260 115 L520 0 M260 115 V160 M240 142 L260 166 L280 142"></path></svg>
    <div id="m-evals" class="label off">EVALS</div>
    <svg id="m-route" class="off" width="820" height="220" viewBox="0 0 820 220"><path class="ink" id="m-road" d="M80 130 L310 80 L540 30 L770 30" stroke-dasharray="760" stroke-dashoffset="760"></path><polyline class="ink" points="738,8 775,30 738,52"></polyline></svg>
    <div id="m-pass0" class="m-pass off">✓</div><div id="m-pass1" class="m-pass off">✓</div><div id="m-pass2" class="m-pass off">✓</div>
    <div id="m-direction" class="label off">DIREÇÃO PARA EVOLUIR</div><div id="m-method" class="label off">TESTAR. MEDIR. MELHORAR.</div>`,
  motion: `    timeline.fromTo('#m-title, #m-subjective', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35, stagger: .1 }, .1);
    timeline.fromTo('#m-reactive', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .35 }, 2.9);
    timeline.fromTo('#m-converge', { opacity: 0 }, { opacity: 1, duration: .25 }, 3.45);
    timeline.fromTo('#m-evals', { opacity: 0, scale: .8 }, { opacity: 1, scale: 1, duration: .35, ease: 'power3.out' }, 3.9);
    timeline.fromTo('#m-route', { opacity: 0 }, { opacity: 1, duration: .2 }, 4.45);
    timeline.fromTo('#m-road', { strokeDashoffset: 760 }, { strokeDashoffset: 0, duration: 1.5, ease: 'power1.inOut' }, 4.5);
    timeline.fromTo('.m-pass', { opacity: 0 }, { opacity: 1, duration: .2, stagger: .45 }, 4.65);
    timeline.fromTo('#m-direction, #m-method', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .3, stagger: .2 }, 6.1);`,
});

scenes.push({
  id: "m-direcao",
  duration: 2.0,
  hero: "#subjective",
  bySec: 0.2,
  css: `#subjective { left: 80px; top: 280px; font-size: 80px; }
    #cut { position: absolute; left: 80px; top: 312px; width: 500px; height: 10px; background: #FFFFFF; }
    #to-direction { position: absolute; left: 80px; top: 480px; }
    #objective { left: 80px; top: 620px; font-size: 140px; }`,
  body: `    <div id="subjective" class="label">SUBJETIVO</div>
    <div id="cut"></div>
    <svg id="to-direction" class="off" width="520" height="40" viewBox="0 0 520 40"><line class="ink" id="dir-path" x1="0" y1="20" x2="470" y2="20" stroke-dasharray="480" stroke-dashoffset="480"></line><polyline class="ink" points="448,4 490,20 448,36"></polyline></svg>
    <div id="objective" class="label off">DIREÇÃO</div>`,
  motion: `    timeline.fromTo(byId("to-direction"), { opacity: 0 }, { opacity: 1, duration: 0.1 }, 0.15);
    timeline.fromTo("#dir-path", { strokeDashoffset: 480 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, 0.15);
    timeline.fromTo(byId("objective"), { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 0.55);`,
});

for (const scene of scenes) {
  fs.writeFileSync(
    path.join(framesDir, `${scene.id}.html`),
    wrap(scene.id, scene.duration, scene.css, scene.body, scene.motion),
  );
}

const obsolete = fs.readdirSync(framesDir).filter((file) => /^\d\d-/.test(file));
for (const file of obsolete) fs.unlinkSync(path.join(framesDir, file));

fs.writeFileSync(
  path.join(framesDir, "scenes.json"),
  `${JSON.stringify(scenes.map(({ id, duration, hero, bySec }) => ({ id, duration, hero, bySec })), null, 2)}\n`,
);

console.log(`Wrote ${scenes.length} drawn scenes. Removed ${obsolete.length} old frames.`);
