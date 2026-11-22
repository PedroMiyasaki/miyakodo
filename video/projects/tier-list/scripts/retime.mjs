import fs from 'node:fs';
import assert from 'node:assert/strict';

// Apply once to the approved Studio sources, preserving the manual edits.
const rate = 1.1;
const scale = value => Number((Number(value) / rate).toFixed(9));
const root = fs.readFileSync('index.html', 'utf8');
assert(!root.includes('data-playback-rate='), 'This edit has already been retimed.');
const files = ['index.html', ...new Set([...root.matchAll(/data-composition-src="([^"]+)"/g)].map(match => match[1]))];
const originalDuration = JSON.parse(fs.readFileSync('transcript-edited.json', 'utf8')).duration;
const duration = scale(originalDuration);
const updates = new Map();

for (const file of files) {
  const before = fs.readFileSync(file, 'utf8');
  let after = before.replace(/\bdata-(start|duration)="([\d.]+)"/g, (_, key, value) => `data-${key}="${scale(value)}"`);
  after = after.replace(/data-automation="([^"]+)"/g, (_, encoded) => {
    const automation = JSON.parse(encoded.replaceAll('&quot;', '"').replaceAll('&amp;', '&'));
    for (const lane of automation.lanes) for (const point of lane.points) point.t = scale(point.t);
    return `data-automation="${JSON.stringify(automation).replaceAll('&', '&amp;').replaceAll('"', '&quot;')}"`;
  });
  after = after.replace(/<(video|audio)\b[^>]*>/g, tag => tag.replace(/>$/, ` data-playback-rate="${rate}">`));
  after = after.replace(/<script>([\s\S]*?)<\/script>/g, (_, script) => `<script>${script
    .replace(/\bduration\s*:\s*([\d.]+)/g, (_, value) => `duration:${scale(value)}`)
    .replace(/,\s*([\d.]+)\s*\);/g, (_, value) => `,${scale(value)});`)}</script>`);
  if (file === 'index.html') after = after.replace(/(data-composition-id="main"[^>]*data-duration=")[^"]+/, `$1${duration}`);
  assert.deepEqual([...after.matchAll(/data-media-start="([^"]+)"/g)].map(m => m[1]), [...before.matchAll(/data-media-start="([^"]+)"/g)].map(m => m[1]));
  assert.deepEqual([...after.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]), [...before.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]));
  assert.deepEqual(after.replace(/<script>[\s\S]*?<\/script>/g, '').match(/>[^<]+</g), before.replace(/<script>[\s\S]*?<\/script>/g, '').match(/>[^<]+</g));
  updates.set(file, after);
}

assert.equal((updates.get('index.html').match(/data-playback-rate="1.1"/g) || []).length, 10);
const compress = (object, keys) => { for (const key of keys) if (typeof object[key] === 'number') object[key] = scale(object[key]); };
const transcript = JSON.parse(fs.readFileSync('transcript-edited.json', 'utf8'));
compress(transcript, ['duration']);
transcript.playbackRate = rate;
for (const word of transcript.words) compress(word, ['start', 'end']);
for (const caption of transcript.captions) {
  compress(caption, ['start', 'end', 'visibleEnd']);
  for (const word of caption.words) compress(word, ['start', 'end']);
}
const plan = JSON.parse(fs.readFileSync('edit-plan.json', 'utf8'));
compress(plan, ['duration']);
plan.playbackRate = rate;
for (const item of plan.items) {
  item.voiceSourceDuration = item.voiceDuration;
  compress(item, ['start', 'duration', 'end', 'speechAt', 'ratingAt', 'voiceAt', 'voiceDuration']);
}
const timeline = JSON.parse(fs.readFileSync('timeline-plan.json', 'utf8'));
compress(timeline, ['duration']);
timeline.playbackRate = rate;
timeline.ratings = timeline.ratings.filter(rating => root.includes(`id="slot-${rating.id}"`));
for (const rating of timeline.ratings) {
  const tag = root.match(new RegExp(`<div[^>]*id="slot-${rating.id}"[^>]*>`))[0];
  rating.start = scale(tag.match(/data-start="([^"]+)"/)[1]);
  compress(rating, ['duration']);
}
for (const voice of timeline.voices) compress(voice, ['start', 'end', 'pedroStarts']);
assert(Math.abs(duration * rate - originalDuration) < 1e-7);
for (const [file, data] of [['transcript-edited.json', transcript], ['edit-plan.json', plan], ['timeline-plan.json', timeline]]) updates.set(file, JSON.stringify(data, null, 2) + '\n');
for (const [file, contents] of updates) fs.writeFileSync(file, contents);
console.log(JSON.stringify({playbackRate: rate, duration, htmlFiles: files.length, mediaClips: 10}));
