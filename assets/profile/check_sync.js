// SMIL timeline sanity check for the typing strip: verifies each line's
// animations exist, begin times are staggered, and caret x-sync values
// match the clip widths (caret rides the sweep).
const fs = require("fs");

const svg = fs.readFileSync("assets/profile/typing-dark.svg", "utf8");
const clips = [...svg.matchAll(/<clipPath id="clip-dark-(\d)"><rect[^>]*>\s*<animate[^>]*values="([^"]+)"[^>]*begin="([\d.]+)s"/g)];
const carets = [...svg.matchAll(/<rect x="([\d.]+)" y="16"[^>]*>\s*<animate attributeName="x" values="([^"]+)"/g)];
const texts = [...svg.matchAll(/clip-path="url\(#clip-dark-(\d)\)"/g)];

console.log("lines with clips:", clips.length);
console.log("lines with text:", texts.length);
console.log("carets:", carets.length);

let ok = true;
clips.forEach(([, idx, values, begin]) => {
  const caret = carets[Number(idx)];
  if (!caret) { console.log(`FAIL: no caret for line ${idx}`); ok = false; return; }
  const clipMax = Math.max(...values.split(";").map(Number));
  const caretVals = caret[2].split(";").map(Number);
  // caret end position + 8px caret width should reach the clip's max width
  const caretMax = Math.max(...caretVals) + 8;
  if (Math.abs(caretMax - clipMax) > 2) {
    console.log(`FAIL: line ${idx} caret max ${caretMax} != clip max ${clipMax}`);
    ok = false;
  }
});
// begin times strictly increasing
const begins = clips.map((c) => Number(c[3]));
for (let i = 1; i < begins.length; i++) {
  if (begins[i] <= begins[i - 1]) { console.log("FAIL: begins not staggered"); ok = false; }
}
console.log(ok ? "ALL SYNC CHECKS PASS" : "CHECKS FAILED");
process.exit(ok ? 0 : 1);
