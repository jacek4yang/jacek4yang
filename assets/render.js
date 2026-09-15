// Render the assets/*.svg sources to PNG via @resvg/resvg-js.
// Usage: node assets/render.js
const { Resvg } = require("@resvg/resvg-js");
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname);

const jobs = [
  ["hero.svg", "hero.png", 1600],
  ["avatar-source.svg", "avatar-1024.png", 1024],
  ["avatar-source.svg", "avatar-512.png", 512],
  ["avatar-source.svg", "avatar-256.png", 256],
  ["avatar-source.svg", "avatar-64.png", 64],
  ["favicon.svg", "favicon.png", 32],
  ["og-image.svg", "og-image.png", 1200],
];

for (const [src, out, width] of jobs) {
  const svg = fs.readFileSync(path.join(dir, src), "utf8");
  const r = new Resvg(svg, {
    fitTo: { mode: "width", value: width },
    font: { loadSystemFonts: true },
  });
  fs.writeFileSync(path.join(dir, out), r.render().asPng());
  console.log("wrote", out, width + "px");
}
