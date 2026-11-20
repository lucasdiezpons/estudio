// =============================================================
//  Estudio — feed tipo TikTok con vídeos fijos
//  · Orden: primero lo no visto (mezclado) + algún visto al azar
//  · Filtro Asignatura › Examen › Tema: interruptores guardados en el móvil
//  · "Visto" se guarda en el móvil (localStorage)
// =============================================================

const PROB_VISTO_INTERCALADO = 0.15; // 15 % de las veces se cuela un vídeo ya visto
const UMBRAL_VISTO = 0.6;            // visto = has visto el 60 % del vídeo

const $ = (s) => document.querySelector(s);
const feed = $("#feed");
let videos = [];
let muted = false;       // sonido activado por defecto
let bloqueado = false;
let desbloqueadoEn = 0;   // iOS: hasta el primer toque solo deja reproducir en silencio
const player = document.createElement("video");
player.playsInline = true; player.setAttribute("webkit-playsinline", ""); player.loop = false; // al acabar pasa solo al siguiente player.preload = "auto";
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
// ---------- Asignatura › Examen › Tema (interruptores guardados en el móvil) ----------
const asig = (v) => v.asignatura || (v.tema || "Otros").split(" · ")[0];
const exam = (v) => v.examen || "General";
const tem = (v) => (v.tema || "Sin tema").split(" · ").slice(1).join(" · ") || v.tema || "Sin tema";
const claves = (v) => [`A:${asig(v)}`, `E:${asig(v)}/${exam(v)}`, `T:${asig(v)}/${exam(v)}/${tem(v)}`];
const apagados = new Set(leerApagados());
function leerApagados() {
  try { const x = localStorage.getItem("apagados"); return x ? JSON.parse(x) : ["E:CESA/MQ"]; } catch { return ["E:CESA/MQ"]; }
}
function guardarApagados() { try { localStorage.setItem("apagados", JSON.stringify([...apagados])); } catch {} }
const activoV = (v) => !claves(v).some((k) => apagados.has(k));
const listaActual = () => videos.filter(activoV);

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
    <div class="pausa">▶</div>
    <div class="info">
      ${v.tema ? `<span class="tema">${esc(v.tema)}</span>` : ""}
      <h2>${esc(v.titulo || v.archivo)}</h2>
      ${v.texto ? `<p>${esc(v.texto)}</p>` : ""}
    </div>
    <div class="barra"><div class="pista"><i><b></b></i></div><span class="tiempo"></span></div>`;
  // ---- barra de progreso arrastrable (como TikTok) ----
  const barra = s.querySelector(".barra");
  let arrastrando = false, seguia = false;
  const mover = (e) => {
    if (!player.duration) return;
    const r = barra.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
    player.currentTime = p * player.duration;
    barra.querySelector("i").style.width = p * 100 + "%";
    barra.querySelector(".tiempo").textContent = mmss(p * player.duration) + " / " + mmss(player.duration);
  };
  barra.addEventListener("pointerdown", (e) => {
    if (+s.dataset.i !== activo) return;
    e.preventDefault(); e.stopPropagation();
    arrastrando = true; seguia = !player.paused;
    barra.setPointerCapture(e.pointerId);
    s.classList.add("scrub"); player.pause(); mover(e);
  });
  barra.addEventListener("pointermove", (e) => { if (arrastrando) { e.preventDefault(); mover(e); } });
  const soltar = (e) => {
    if (!arrastrando) return;
    arrastrando = false; s.classList.remove("scrub");
    if (seguia) player.play().catch(() => {});
    desbloqueadoEn = Date.now(); // que el "click" de soltar no pause el vídeo
  };
  barra.addEventListener("pointerup", soltar);
  barra.addEventListener("pointercancel", soltar);
  barra.addEventListener("click", (e) => e.stopPropagation());

  s.addEventListener("click", () => {
    if (+s.dataset.i !== activo) return;
    if (bloqueado) { desbloquear(); return; }
    if (Date.now() - desbloqueadoEn < 600) return; // ese toque solo activaba el sonido
    if (player.paused) { player.play().catch(() => {}); s.classList.remove("pausado"); }
    else { player.pause(); s.classList.add("pausado"); }
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
  const s = feed.querySelector(`.slide[data-i="${i}"]`);
  if (!s) return;
  s.classList.remove("pausado");
  s.insertBefore(player, s.firstChild);
  const src = "videos/" + cola[i].archivo;
  if (!player.src.endsWith(src)) player.src = src;
  player.currentTime = 0;
  reproducir();
  // precarga el siguiente
  const sig = cola[i + 1];
  if (sig) { const l = document.createElement("link"); l.rel = "prefetch"; l.href = "videos/" + sig.archivo; document.head.appendChild(l); }
  // feed infinito: cuando quedan 2, se añade otra ronda
  if (i >= cola.length - 2) añadir(ronda(listaActual()));
}

function reproducir() {
  player.muted = muted || bloqueado;
  player.play().catch(() => {
    if (!player.muted) { bloqueado = true; player.muted = true; player.play().catch(() => {}); toast("🔊 Toca la pantalla para activar el sonido"); }
  });
  $("#btn-sonido").textContent = muted ? "🔇" : "🔊";
}

function desbloquear() {
  bloqueado = false;
  desbloqueadoEn = Date.now();
  player.muted = muted;
  player.play().catch(() => {});
}
// el primer toque en cualquier sitio desbloquea el sonido
["touchend", "click"].forEach((ev) => document.addEventListener(ev, () => { if (bloqueado) desbloquear(); }, { once: false, passive: true }));

// deslizamiento automático: al terminar un vídeo, baja al siguiente
player.addEventListener("ended", () => {
  if ($("#lista").hidden === false) return; // si estás en la lista, no
  marcarVisto(cola[activo].id);
  const sig = feed.querySelector(`.slide[data-i="${activo + 1}"]`);
  if (sig) sig.scrollIntoView({ behavior: "smooth" });
  else { player.currentTime = 0; player.play().catch(() => {}); }
});

player.addEventListener("timeupdate", () => {
  if (!player.duration || activo < 0) return;
  const p = player.currentTime / player.duration;
  const bar = feed.querySelector(`.slide[data-i="${activo}"] .barra i`);
  if (bar) bar.style.width = p * 100 + "%";
  if (p >= UMBRAL_VISTO) marcarVisto(cola[activo].id);
});

// ---------- Sonido ----------
$("#btn-sonido").addEventListener("click", (e) => {
  e.stopPropagation();
  muted = !muted;
  bloqueado = false;
  reproducir();
});

// ---------- Filtro: árbol de interruptores ----------
function arbol(lista) {
  const t = {};
  for (const v of lista) (((t[asig(v)] ??= {})[exam(v)] ??= {})[tem(v)] ??= []).push(v);
  return t;
}
const ord = (o) => Object.keys(o).sort((a, b) => a.localeCompare(b, "es"));
function etiquetaFiltro() {
  const on = new Set(listaActual().map((v) => `${asig(v)} · ${exam(v)}`));
  const n = listaActual().length;
  $("#btn-tema").textContent = (on.size === 1 ? [...on][0] : on.size ? `${on.size} exámenes` : "Nada") + ` (${n}) ▾`;
}
function pintarFiltro() {
  const box = $("#sheet-temas");
  box.innerHTML = "";
  const t = arbol(videos);
  const fila = (clave, texto, n, nivel, padreOff) => {
    const b = document.createElement("button");
    b.className = `nodo n${nivel}` + (apagados.has(clave) ? "" : " on") + (padreOff ? " gris" : "");
    b.innerHTML = `<span class="sw"></span><span class="txt">${esc(texto)}</span><span class="cnt">${n}</span>`;
    b.onclick = () => { apagados.has(clave) ? apagados.delete(clave) : apagados.add(clave); guardarApagados(); pintarFiltro(); };
    box.appendChild(b);
  };
  const cuenta = (o) => Array.isArray(o) ? o.length : Object.values(o).reduce((s, x) => s + cuenta(x), 0);
  for (const A of ord(t)) {
    const kA = `A:${A}`; fila(kA, A, cuenta(t[A]), 0, false);
    for (const E of ord(t[A])) {
      const kE = `E:${A}/${E}`; const offA = apagados.has(kA);
      fila(kE, E, cuenta(t[A][E]), 1, offA);
      for (const T of ord(t[A][E])) fila(`T:${A}/${E}/${T}`, T, t[A][E][T].length, 2, offA || apagados.has(kE));
    }
  }
}
$("#btn-tema").addEventListener("click", () => { pintarFiltro(); $("#sheet").hidden = false; });
$("#sheet").addEventListener("click", (e) => {
  if (e.target.id !== "sheet" && e.target.id !== "sheet-ok") return;
  $("#sheet").hidden = true; etiquetaFiltro(); montarFeed();
});

// ---------- Lista ----------
function pintarLista() {
  const q = $("#buscar").value.trim().toLowerCase();
  const cont = $("#lista-contenido");
  cont.innerHTML = "";
  const grupos = {};
  for (const v of videos) {
    if (q && !`${v.titulo} ${v.texto} ${v.tema}`.toLowerCase().includes(q)) continue;
    (grupos[`${asig(v)} › ${exam(v)} › ${tem(v)}`] ??= []).push(v);
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
      b.onclick = () => { vista("feed"); montarFeed(v); };
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
  if (enFeed) player.play().catch(() => {}); else player.pause();
  if (!enFeed) pintarLista();
}
document.querySelectorAll("#bottom button").forEach((b) => b.addEventListener("click", () => vista(b.dataset.vista)));

// ---------- Utilidades ----------
function mmss(t) { t = Math.max(0, Math.floor(t || 0)); return Math.floor(t / 60) + ":" + String(t % 60).padStart(2, "0"); }
function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function toast(t) { const el = $("#toast"); el.textContent = t; el.hidden = false; setTimeout(() => (el.hidden = true), 1600); }

// ---------- Arranque ----------
fetch("videos/videos.json", { cache: "no-cache" })
  .then((r) => r.json())
  .then((data) => { videos = data.filter((v) => v && v.archivo).map((v) => ({ ...v, id: v.id || v.archivo })); etiquetaFiltro(); montarFeed(); })
  .catch(() => { feed.innerHTML = `<div class="vacio">⚠️ No se pudo leer videos/videos.json</div>`; });
