"use strict";

const data = JSON.parse(document.getElementById("scenario-data").textContent);
const explorer = document.getElementById("interactive");
const timeline = document.getElementById("timeline");
const slider = document.getElementById("boundary");
const previous = document.getElementById("previous");
const next = document.getElementById("next");
let scenario = data.scenarios[0];
let boundary = scenario.focus_boundary;

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function eventLabel(event) {
  if (!event) return "Initial state";
  const instruction = event.instruction;
  const actor = event.actor === 0 ? "Producer" : "Consumer";
  const value = instruction.value === null ? "" : ` ${instruction.value}`;
  return `${actor}: ${instruction.kind} ${instruction.target}${value}`;
}

function renderTimeline() {
  timeline.replaceChildren(...scenario.checkpoints.map((checkpoint) => {
    const item = element("li");
    const button = element("button", eventLabel(checkpoint.event));
    button.type = "button";
    button.addEventListener("click", () => { boundary = checkpoint.boundary; render(); });
    item.append(button);
    return item;
  }));
}

function render() {
  const point = scenario.checkpoints[boundary];
  slider.max = scenario.checkpoints.length - 1;
  slider.value = boundary;
  slider.setAttribute("aria-valuetext", `Boundary ${boundary}: ${eventLabel(point.event)}`);
  previous.disabled = boundary === 0;
  next.disabled = boundary === scenario.checkpoints.length - 1;
  document.getElementById("step-counter").textContent = `${boundary} / ${scenario.checkpoints.length - 1}`;

  for (const [index, button] of [...timeline.querySelectorAll("button")].entries()) {
    button.setAttribute("aria-current", index === boundary ? "step" : "false");
  }

  const state = document.getElementById("state");
  const cards = element("div", undefined, "record-cards");
  for (const record of ["source", "manifest"]) {
    const card = element("div", undefined, "record-card");
    card.append(element("h4", record), element("p", `Visible version: ${point.visible[record]}`),
      element("p", `Forced durable version: ${point.forced[record]}`, "muted"));
    cards.append(card);
  }
  const seen = point.registers[1].seen;
  state.replaceChildren(element("h3", eventLabel(point.event)), cards,
    element("p", `Volatile ready: ${point.signals.includes("ready") ? "set" : "not set"} · Consumer register: ${seen === undefined ? "not read" : seen}`, "muted"));

  document.getElementById("images").replaceChildren(...point.crash_images.map((image) => {
    const row = element("tr", undefined, image.violations.length ? "bad" : "good");
    const outcome = image.violations.length ? `Violates ${image.violations.join(", ")}` : "Recovers: rule holds";
    row.append(element("td", image.disk.source), element("td", image.disk.manifest), element("td", outcome));
    return row;
  }));
  const failures = point.crash_images.filter((image) => image.violations.length).length;
  document.getElementById("crash-count").textContent = `${point.crash_images.length} allowed`;
  const verdict = document.getElementById("verdict");
  verdict.className = `verdict ${failures ? "bad" : "good"}`;
  if (failures) {
    const plural = failures === 1 ? "image violates" : "images violate";
    verdict.textContent = `${failures} allowed crash ${plural} recovery. The saved manifest can outlive its source.`;
  } else if (point.crash_images.length === 1) {
    verdict.textContent = "Every written version is already forced, so only one crash image is allowed. It satisfies recovery.";
  } else {
    verdict.textContent = "Every crash image at this boundary satisfies recovery. Losing an unreferenced new version is allowed.";
  }
}

previous.addEventListener("click", () => { boundary -= 1; render(); });
next.addEventListener("click", () => { boundary += 1; render(); });
slider.addEventListener("input", () => { boundary = Number(slider.value); render(); });
for (const radio of document.querySelectorAll('input[name="scenario"]')) {
  radio.addEventListener("change", () => {
    scenario = data.scenarios.find((candidate) => candidate.id === radio.value);
    boundary = scenario.focus_boundary;
    renderTimeline();
    render();
  });
}
renderTimeline();
render();
explorer.hidden = false;
