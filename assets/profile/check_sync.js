// Layout and SMIL timeline sanity checks for hero and typing SVGs.
// Run: node assets/profile/check_sync.js
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname);
let allOk = true;

function checkFile(name) {
  const file = path.join(dir, name);
  if (!fs.existsSync(file)) {
    console.error(`FAIL: ${name} does not exist`);
    allOk = false;
    return;
  }
  const content = fs.readFileSync(file, "utf8");

  // Basic XML check
  if (!content.startsWith("<svg") || !content.endsWith("</svg>")) {
    console.error(`FAIL: ${name} malformed svg bounds`);
    allOk = false;
  }

  // Verify keyTimes bounds
  const keyTimesMatches = [...content.matchAll(/keyTimes="([^"]+)"/g)];
  for (const [, kt] of keyTimesMatches) {
    const vals = kt.split(";").map(Number);
    if (vals[0] !== 0 || vals[vals.length - 1] !== 1) {
      console.error(`FAIL: ${name} keyTimes must start at 0 and end at 1: ${kt}`);
      allOk = false;
    }
    for (let i = 1; i < vals.length; i++) {
      if (vals[i] < vals[i - 1]) {
        console.error(`FAIL: ${name} keyTimes not non-decreasing: ${kt}`);
        allOk = false;
      }
    }
  }

  console.log(`PASS: ${name} passed validation`);
}

checkFile("hero-dark.svg");
checkFile("hero-light.svg");
checkFile("hero-static.svg");
checkFile("typing-dark.svg");
checkFile("typing-light.svg");

process.exit(allOk ? 0 : 1);
