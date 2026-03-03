const keys = {
  notes: "pf2e_notes",
  loot: "pf2e_loot",
  checks: "pf2e_checks",
};

const notes = document.getElementById("notes");
const clearNotes = document.getElementById("clear-notes");
const partyLevel = document.getElementById("party-level");
const enemyLevels = document.getElementById("enemy-levels");
const calcXp = document.getElementById("calc-xp");
const xpResult = document.getElementById("xp-result");
const lootInput = document.getElementById("loot-input");
const addLoot = document.getElementById("add-loot");
const lootList = document.getElementById("loot-list");
const checks = ["chk-healing", "chk-spells", "chk-funds", "chk-map"];

const xpByDelta = {
  "-4": 10,
  "-3": 15,
  "-2": 20,
  "-1": 30,
  "0": 40,
  "1": 60,
  "2": 80,
  "3": 120,
  "4": 160,
};

function load() {
  notes.value = localStorage.getItem(keys.notes) ?? "";
  renderLoot(JSON.parse(localStorage.getItem(keys.loot) ?? "[]"));
  const savedChecks = JSON.parse(localStorage.getItem(keys.checks) ?? "{}");
  checks.forEach((id) => {
    const el = document.getElementById(id);
    el.checked = Boolean(savedChecks[id]);
  });
}

function renderLoot(items) {
  lootList.innerHTML = "";
  items.forEach((item, idx) => {
    const li = document.createElement("li");
    li.textContent = item;
    const del = document.createElement("button");
    del.textContent = "Remove";
    del.addEventListener("click", () => {
      const current = JSON.parse(localStorage.getItem(keys.loot) ?? "[]");
      current.splice(idx, 1);
      localStorage.setItem(keys.loot, JSON.stringify(current));
      renderLoot(current);
    });
    li.appendChild(del);
    lootList.appendChild(li);
  });
}

notes.addEventListener("input", () => {
  localStorage.setItem(keys.notes, notes.value);
});

clearNotes.addEventListener("click", () => {
  notes.value = "";
  localStorage.setItem(keys.notes, "");
});

calcXp.addEventListener("click", () => {
  const party = Number(partyLevel.value);
  const enemies = enemyLevels.value
    .split(",")
    .map((value) => Number(value.trim()))
    .filter((value) => !Number.isNaN(value));

  const total = enemies.reduce((sum, level) => {
    const delta = Math.max(-4, Math.min(4, level - party));
    return sum + (xpByDelta[String(delta)] ?? 0);
  }, 0);

  xpResult.textContent = `XP Total: ${total}`;
});

addLoot.addEventListener("click", () => {
  const item = lootInput.value.trim();
  if (!item) {
    return;
  }
  const current = JSON.parse(localStorage.getItem(keys.loot) ?? "[]");
  current.push(item);
  localStorage.setItem(keys.loot, JSON.stringify(current));
  lootInput.value = "";
  renderLoot(current);
});

checks.forEach((id) => {
  document.getElementById(id).addEventListener("change", () => {
    const savedChecks = {};
    checks.forEach((checkId) => {
      savedChecks[checkId] = document.getElementById(checkId).checked;
    });
    localStorage.setItem(keys.checks, JSON.stringify(savedChecks));
  });
});

load();
