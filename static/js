// ====== STATE & HELPERS ======
const stateKey = "portfolioState";
const themeKey = "theme";
let zIndexCounter = 20;

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function saveState() {
  const open = $$(".window").filter(w => w.style.display === "block").map(w => w.id);
  const pos = {};
  $$(".window").forEach(w => pos[w.id] = { left: w.offsetLeft, top: w.offsetTop });
  localStorage.setItem(stateKey, JSON.stringify({ open, pos }));
}
function restoreState() {
  const s = JSON.parse(localStorage.getItem(stateKey) || "{}");
  (s.open || []).forEach(id => openWindow(id));
  Object.entries(s.pos || {}).forEach(([id, { left, top }]) => {
    const w = document.getElementById(id);
    if (!w) return;
    w.style.left = left + "px";
    w.style.top = top + "px";
  });
}
function setTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem(themeKey, t);
}

// ====== CLOCK ======
function updateClock() {
  const now = new Date();
  $("#time").textContent = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  $("#date").textContent = now.toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" });
}
setInterval(updateClock, 60000);
updateClock();

// ====== WINDOWS OPEN/CLOSE ======
function openWindow(id) {
  const win = document.getElementById(id);
  if (!win) return;
  win.style.display = "block";
  win.style.zIndex = ++zIndexCounter;
  saveState();
  if (id === "projects") loadProjects();
}
function closeWindow(id) {
  const win = document.getElementById(id);
  if (!win) return;
  win.style.display = "none";
  saveState();
}

// ====== DRAGGABLE WINDOWS ======
function makeDraggable(win) {
  const title = $(".titlebar", win);
  let isDragging = false, offsetX = 0, offsetY = 0;

  title.addEventListener("mousedown", e => {
    isDragging = true;
    win.style.zIndex = ++zIndexCounter;
    offsetX = e.clientX - win.offsetLeft;
    offsetY = e.clientY - win.offsetTop;
    document.body.style.userSelect = "none";
  });

  document.addEventListener("mousemove", e => {
    if (!isDragging) return;
    const pad = 8;
    const x = Math.max(pad, Math.min(e.clientX - offsetX, window.innerWidth - win.offsetWidth - pad));
    const y = Math.max(50, Math.min(e.clientY - offsetY, window.innerHeight - win.offsetHeight - pad));
    win.style.left = x + "px";
    win.style.top = y + "px";
  });

  document.addEventListener("mouseup", () => {
    if (!isDragging) return;
    isDragging = false;
    document.body.style.userSelect = "";
    saveState();
  });

  win.addEventListener("mousedown", () => { win.style.zIndex = ++zIndexCounter; });
}
$$(".window").forEach(makeDraggable);

// ====== DOCK MAGNIFICATION ======
const dock = $("#dock");
const dockItems = $$(".dock-icon", dock);
dock.addEventListener("mousemove", e => {
  dockItems.forEach(it => {
    const rect = it.getBoundingClientRect();
    const center = rect.left + rect.width / 2;
    const dist = Math.abs(e.clientX - center);
    const scale = Math.max(1, 2 - dist / 140);
    it.style.transform = `scale(${scale})`;
  });
});
dock.addEventListener("mouseleave", () => dockItems.forEach(it => it.style.transform = "scale(1)"));

// Open windows from dock
dockItems.forEach(btn => btn.addEventListener("click", () => openWindow(btn.dataset.open)));

// Close buttons
$$(".close").forEach(btn => btn.addEventListener("click", () => closeWindow(btn.dataset.close)));

// ====== THEME TOGGLE ======
const initialTheme = localStorage.getItem(themeKey) || "light";
setTheme(initialTheme);
$("#themeToggle").addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme");
  setTheme(current === "dark" ? "light" : "dark");
});

// ====== PROJECTS (from Flask) ======
async function loadProjects() {
  const container = $("#projectsList");
  container.innerHTML = `<div class="loading">Loading projects…</div>`;
  try {
    const res = await fetch("/api/projects");
    const data = await res.json();
    container.innerHTML = data.map(p => `
      <article class="project-card">
        <a href="${p.link}" target="_blank" rel="noopener">${p.title}</a>
        <div>${p.description}</div>
        <small>${p.stack}</small>
      </article>
    `).join("");
  } catch {
    container.innerHTML = `<div class="loading">Failed to load projects.</div>`;
  }
}

// ====== CONTACT FORM ======
$("#contactForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const payload = Object.fromEntries(fd.entries());
  try {
    await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    alert("Message sent. Thank you!");
    e.target.reset();
  } catch {
    alert("Failed to send. Please try again.");
  }
});

// ====== NOTIFICATIONS ======
$("#bell").addEventListener("click", () => {
  const pane = $("#notif");
  const visible = pane.style.display === "block";
  pane.style.display = visible ? "none" : "block";
  if (!visible) {
    pane.innerHTML = `
      <div class="result-item"><strong>Welcome</strong><br>Thanks for visiting my portfolio!</div>
      <div class="result-item"><strong>Tip</strong><br>Press Cmd+Space (or Ctrl+Space) for Spotlight.</div>
    `;
  }
});

// ====== SPOTLIGHT SEARCH ======
const spotlight = $("#spotlight");
const search = $("#search");
const results = $("#results");
const closeSpotlight = () => { spotlight.style.display = "none"; };
const openSpotlight = () => { spotlight.style.display = "block"; search.focus(); };

$("#spotlightBtn").addEventListener("click", openSpotlight);
$("#closeSpotlight").addEventListener("click", closeSpotlight);

window.addEventListener("keydown", (e) => {
  const shortcut = (e.metaKey || e.ctrlKey) && e.code === "Space";
  if (shortcut) { e.preventDefault(); openSpotlight(); }
  if (e.code === "Escape") closeSpotlight();
});

// Registry: windows + projects
const registry = [
  { type: "window", id: "about", label: "About Me" },
  { type: "window", id: "projects", label: "Projects" },
  { type: "window", id: "contact", label: "Contact" }
];

search.addEventListener("input", async (e) => {
  const q = e.target.value.toLowerCase();
  let items = registry.filter(r => r.label.toLowerCase().includes(q));

  // Include projects in search
  try {
    const res = await fetch("/api/projects");
    const data = await res.json();
    items = items.concat(
      data
        .filter(p => p.title.toLowerCase().includes(q) || p.description.toLowerCase().includes(q))
        .map(p => ({ type: "project", label: `Project: ${p.title}`, link: p.link || "#" }))
    );
  } catch {}

  results.innerHTML = items.map((r, i) => `
    <div class="result-item" data-type="${r.type}" data-id="${r.id || ""}" data-link="${r.link || ""}">
      ${r.label}
    </div>
  `).join("");
});

results.addEventListener("click", (e) => {
  const item = e.target.closest(".result-item");
  if (!item) return;
  const type = item.dataset.type;
  if (type === "window") {
    const id = item.dataset.id;
    openWindow(id);
  } else if (type === "project") {
    const link = item.dataset.link;
    if (link) window.open(link, "_blank", "noopener");
  }
  closeSpotlight();
});

// ====== RESTORE STATE ON LOAD ======
window.addEventListener("load", restoreState);
