// =============================================================
//  Estudio — feed tipo TikTok con vídeos fijos
//  · Orden: primero lo no visto (mezclado) + algún visto al azar
//  · Filtro por tema: solo dura mientras la app está abierta
//  · "Visto" se guarda en el móvil (localStorage)
// =============================================================

const PROB_VISTO_INTERCALADO = 0.15; // 15 % de las veces se cuela un vídeo ya visto
const UMBRAL_VISTO = 0.6;            // visto = has visto el 60 % del vídeo
const PRECARGA = 1;                  // cuántos vídeos alrededor se cargan

const $ = (s) => document.querySelector(s);
const feed = $("#feed");
let videos = [];
let filtroTema = null;   // NO se guarda: al cerrar la app vuelve a "Para ti"
let muted = true;        // iOS solo permite autoplay en silencio; tocas 🔇 y ya
let cola = [];           // vídeos en el feed (en orden)
let activo = -1;

// ---------- Vistos (persistentes) ----------
const vistos = new Set(leerVistos());
function leerVistos() { try { return JSON.parse(localStorage.getItem("vistos") || "[]"); } catch { return []; } }
function marcarVisto(id) {
  if (vistos.has(id)) return;
  vistos.add(id);
  try { localStorage.setItem("vistos", JSON.stringify([...vistos])); } catch {}
}

// ---------- Orden ----------
function mezclar(a) {
  a = [...a];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
function ronda(lista) {
  const noVistos = mezclar(lista.filter((v) => !vistos.has(v.id)));
  const siVistos = mezclar(lista.filter((v) => vistos.has(v.id)));
  const out = [];
  for (const v of noVistos) {
    if (siVistos.length && Math.random() < PROB_VISTO_INTERCALADO) out.push(siVistos.pop());
    out.push(v);
  }
  return out.concat(siVistos);
}
const listaActual = () => (filtroTema ? videos.filter((v) => v.tema === filtroTema) : videos);

// ---------- Feed ----------
function montarFeed(primero = null) {
  feed.innerHTML = "";
  cola = [];
  activo = -1;
  const lista = listaActual();
  if (!lista.length) {
    feed.innerHTML = `<div class="vacio"><div style="font-size:48px">📭</div>
      <div>No hay vídeos todavía.<br>Mételos en <b>videos/</b> y ejecuta <b>tools/actualizar.py</b></div></div>`;
    return;
  }
  let orden = ronda(lista);
  if (primero) orden = [primero, ...orden.filter((v) => v.id !== primero.id)];
  añadir(orden);
  feed.scrollTop = 0;
  requestAnimationFrame(() => activar(0));
}

function añadir(orden) {
  // evita el mismo vídeo dos veces seguidas entre rondas
  if (cola.length && orden.length > 1 && orden[0].id === cola[cola.length - 1].id) orden.push(orden.shift());
  for (const v of orden) {
    const i = cola.length;
    cola.push(v);
    feed.appendChild(crearSlide(v, i));
  }
}

function crearSlide(v, i) {
  const s = document.createElement("section");
  s.className = "slide";
  s.dataset.i = i;
  if (v.poster) s.style.backgroundImage = `url("videos/${v.poster}")`;
  s.innerHTML = `
    <video playsinline webkit-playsinline loop muted preload="none"></video>
    <div class="pausa">▶</div>
    <div class="info">
      ${v.tema ? `<span class="tema">${esc(v.tema)}</span>` : ""}
      <h2>${esc(v.titulo || v.archivo)}</h2>
      ${v.texto ? `<p>${esc(v.texto)}</p>` : ""}
    </div>
    <div class="barra"><i></i></div>`;
  const vid = s.querySelector("video");
  vid.addEventListener("timeupdate", () => {
    if (!vid.duration) return;
    const p = vid.currentTime / vid.duration;
    s.querySelector(".barra i").style.width = p * 100 + "%";
    if (p >= UMBRAL_VISTO) marcarVisto(v.id);
  });
  s.addEventListener("click", () => {
    if (vid.paused) { vid.play().catch(() => {}); s.classList.remove("pausado"); }
    else { vid.pause(); s.classList.add("pausado"); }
  });
  obs.observe(s);
  return s;
}

const obs = new IntersectionObserver((entries) => {
  for (const e of entries) if (e.isIntersecting && e.intersectionRatio >= 0.6) activar(+e.target.dataset.i);
}, { root: feed, threshold: [0.6] });

function activar(i) {
  if (i === activo) return;
  activo = i;
  const slides = feed.querySelectorAll(".slide");
  slides.forEach((s, j) => {
    const vid = s.querySelector("video");
    const v = cola[j];
    if (Math.abs(j - i) <= PRECARGA) {
      if (!vid.src) { vid.src = "videos/" + v.archivo; vid.preload = "auto"; }
    } else if (vid.src) {
      vid.pause(); vid.removeAttribute("src"); vid.load(); // libera memoria
    }
    if (j === i) {
      vid.muted = muted; vid.currentTime = 0;
      s.classList.remove("pausado");
      vid.play().catch(() => { vid.muted = true; vid.play().catch(() => {}); });
    } else if (vid.src) vid.pause();
  });
  // feed infinito: cuando quedan 2, se añade otra ronda
  if (i >= cola.length - 2) añadir(ronda(listaActual()));
}

// ---------- Sonido ----------
$("#btn-sonido").addEventListener("click", (e) => {
  e.stopPropagation();
  muted = !muted;
  $("#btn-sonido").textContent = muted ? "🔇" : "🔊";
  const s = feed.querySelector(`.slide[data-i="${activo}"] video`);
  if (s) { s.muted = muted; s.play().catch(() => {}); }
});

// ---------- Filtro por tema ----------
const temas = () => [...new Set(videos.map((v) => v.tema).filter(Boolean))].sort((a, b) => a.localeCompare(b, "es"));
$("#btn-tema").addEventListener("click", () => {
  const box = $("#sheet-temas");
  box.innerHTML = "";
  [null, ...temas()].forEach((t) => {
    const b = document.createElement("button");
    b.textContent = t ?? "Todo mezclado";
    if (t === filtroTema) b.classList.add("on");
    b.onclick = () => {
      filtroTema = t;
      $("#btn-tema").textContent = (t ?? "Para ti") + " ▾";
      $("#sheet").hidden = true;
      montarFeed();
    };
    box.appendChild(b);
  });
  $("#sheet").hidden = false;
});
$("#sheet").addEventListener("click", (e) => { if (e.target.id === "sheet") $("#sheet").hidden = true; });

// ---------- Lista ----------
function pintarLista() {
  const q = $("#buscar").value.trim().toLowerCase();
  const cont = $("#lista-contenido");
  cont.innerHTML = "";
  const grupos = {};
  for (const v of videos) {
    if (q && !`${v.titulo} ${v.texto} ${v.tema}`.toLowerCase().includes(q)) continue;
    (grupos[v.tema || "Sin tema"] ??= []).push(v);
  }
  const nombres = Object.keys(grupos).sort((a, b) => a.localeCompare(b, "es"));
  if (!nombres.length) { cont.innerHTML = `<p style="opacity:.6;margin-top:20px">Nada por aquí.</p>`; return; }
  for (const t of nombres) {
    const g = document.createElement("div");
    g.className = "grupo";
    g.innerHTML = `<h3>${esc(t)} · ${grupos[t].length}</h3>`;
    grupos[t].sort((a, b) => (a.titulo || "").localeCompare(b.titulo || "", "es")).forEach((v) => {
      const b = document.createElement("button");
      b.className = "item";
      b.innerHTML = `<img loading="lazy" src="${v.poster ? "videos/" + v.poster : ""}" alt="">
        <div><b>${esc(v.titulo || v.archivo)}</b><small>${vistos.has(v.id) ? "✓ visto" : "● nuevo"}${v.texto ? " · " + esc(v.texto) : ""}</small></div>`;
      b.onclick = () => { filtroTema = null; $("#btn-tema").textContent = "Para ti ▾"; vista("feed"); montarFeed(v); };
      g.appendChild(b);
    });
    cont.appendChild(g);
  }
}
$("#buscar").addEventListener("input", pintarLista);

// ---------- Navegación ----------
function vista(n) {
  document.querySelectorAll("#bottom button").forEach((b) => b.classList.toggle("activo", b.dataset.vista === n));
  const enFeed = n === "feed";
  $("#lista").hidden = enFeed;
  $("#top").style.display = enFeed ? "" : "none";
  const v = feed.querySelector(`.slide[data-i="${activo}"] video`);
  if (v) enFeed ? v.play().catch(() => {}) : v.pause();
  if (!enFeed) pintarLista();
}
document.querySelectorAll("#bottom button").forEach((b) => b.addEventListener("click", () => vista(b.dataset.vista)));

// ---------- Utilidades ----------
function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function toast(t) { const el = $("#toast"); el.textContent = t; el.hidden = false; setTimeout(() => (el.hidden = true), 1600); }

// ---------- Arranque ----------
fetch("videos/videos.json", { cache: "no-cache" })
  .then((r) => r.json())
  .then((data) => { videos = data.filter((v) => v && v.archivo).map((v) => ({ ...v, id: v.id || v.archivo })); montarFeed(); })
  .catch(() => { feed.innerHTML = `<div class="vacio">⚠️ No se pudo leer videos/videos.json</div>`; });
