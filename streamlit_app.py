import urllib.parse
import streamlit as st
import base64
import math

# --- 1. SET UP THE VIRGINIA CALCULATOR DISPLAY ---
st.set_page_config(page_title="Virginia Testing Calculator", page_icon="🧮", layout="centered")

st.title("Virginia Testing Calculator")
st.caption("Modeled after the Desmos Virginia Scientific Calculator")

# Initialize calculator state variables
if "calc_input" not in st.session_state:
    st.session_state.calc_input = ""
if "calc_output" not in st.session_state:
    st.session_state.calc_output = "0"

# Helper function to append keys safely and force immediate update
def append_key(char):
    st.session_state.calc_input += str(char)
    st.rerun()

# Helper function to evaluate expressions safely
def evaluate_expression(expr_to_eval=None):
    expr = expr_to_eval if expr_to_eval is not None else st.session_state.calc_input
    if not expr:
        st.session_state.calc_output = "0"
        return
    
    # Clean up standard variations and custom visual symbols before eval
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("π", "math.pi")
    expr = expr.replace("√", "math.sqrt")
    expr = expr.replace("^", "**")
    
    try:
        # Safe execution sandbox mapping core math operations allowed under VA rules
        allowed_globals = {
            "math": math,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "sqrt": math.sqrt,
            "pi": math.pi
        }
        
        result = eval(expr, {"__builtins__": None}, allowed_globals)
        # Format floating-point answers neatly
        if isinstance(result, float) and result.is_integer():
            st.session_state.calc_output = str(int(result))
        else:
            st.session_state.calc_output = f"{result:.10g}"
            
    except Exception:
        st.session_state.calc_output = "Error"

# Custom CSS styling to link the input bar and result tightly with clear visibility
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #f1f3f4;
        border-radius: 0 0 8px 8px;
        padding: 10px 16px;
        margin-top: -16px;
        border: 1px solid #ccced0;
        border-top: none;
    }
    div[data-testid="stTextInput"] input {
        font-size: 22px !important;
        font-weight: 500;
        border-radius: 8px 8px 0 0 !important;
        border: 1px solid #ccced0 !important;
        background-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Combined Expression Entry (Supports Keyboard Typing + Enter key evaluation)
typed_input = st.text_input(
    "Expression Entry", 
    value=st.session_state.calc_input, 
    label_visibility="collapsed", 
    placeholder="Type an expression or use the buttons below..."
)

# If the user typed something directly and hit enter, evaluate it immediately
if typed_input != st.session_state.calc_input:
    st.session_state.calc_input = typed_input
    evaluate_expression(typed_input)
    st.rerun()

# Balanced adjacent Result metric view block attached directly underneath
st.metric(label="Result", value=st.session_state.calc_output)

# --- 2. CALCULATOR KEYPAD UNIFIED GRID ---

# Top Control Row (4 Columns)
col_c, col_back, col_left_p, col_right_p = st.columns(4)
with col_c:
    if st.button("Clear All", use_container_width=True, type="primary"):
        st.session_state.calc_input = ""
        st.session_state.calc_output = "0"
        st.rerun()
with col_back:
    if st.button("⌫ Back", use_container_width=True):
        st.session_state.calc_input = st.session_state.calc_input[:-1]
        st.rerun()
with col_left_p:
    if st.button("(", use_container_width=True):
        append_key("(")
with col_right_p:
    if st.button(")", use_container_width=True):
        append_key(")")

st.write("")

# Unified Keypad Rows (6 Columns each for a perfectly balanced layout)
# Row 1
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("sin", use_container_width=True): append_key("sin(")
with c2:
    if st.button("cos", use_container_width=True): append_key("cos(")
with c3:
    if st.button("7", use_container_width=True): append_key("7")
with c4:
    if st.button("8", use_container_width=True): append_key("8")
with c5:
    if st.button("9", use_container_width=True): append_key("9")
with c6:
    if st.button("÷", use_container_width=True): append_key("÷")

# Row 2
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("tan", use_container_width=True): append_key("tan(")
with c2:
    if st.button("π", use_container_width=True): append_key("π")
with c3:
    if st.button("4", use_container_width=True): append_key("4")
with c4:
    if st.button("5", use_container_width=True): append_key("5")
with c5:
    if st.button("6", use_container_width=True): append_key("6")
with c6:
    if st.button("×", use_container_width=True): append_key("×")

# Row 3
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("√", use_container_width=True): append_key("√(")
with c2:
    if st.button("x²", use_container_width=True): append_key("^2")
with c3:
    if st.button("1", use_container_width=True): append_key("1")
with c4:
    if st.button("2", use_container_width=True): append_key("2")
with c5:
    if st.button("3", use_container_width=True): append_key("3")
with c6:
    if st.button("-", use_container_width=True): append_key("-")

# Row 4
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("a^b", use_container_width=True): append_key("^")
with c2:
    st.button("DEG", use_container_width=True, disabled=True, help="Virginia testing locks to Degrees.")
with c3:
    if st.button("0", use_container_width=True): append_key("0")
with c4:
    if st.button(".", use_container_width=True): append_key(".")
with c5:
    if st.button("=", use_container_width=True): 
        evaluate_expression()
        st.rerun()
with c6:
    if st.button("+", use_container_width=True): append_key("+")

st.write("---")




# --- 3. CUSTOM HTML POPUP SECTION ---
st.write("---")

# 1. Create a secure text entry box for the access code
access_code = st.text_input("🔑 Enter Secret Access Code (Authorized People Only):", type="password", placeholder="Type code here...")

# 2. Check if the entry matches 'gamer123' exactly (no caps)
if access_code == "gamer123":
    
    # Your raw dashboard code
    my_custom_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Virginia Calculator</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Outfit:wght@300;500&display=swap" rel="stylesheet">
<style>
  :root {
    --gold: #ffd700;
    --amber: #ffb000;
    --ink: #07050a;
    --glow: .7;
    --speed: 1;xwez
    --orb: 280px;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; font-family: Outfit, sans-serif; color: #fff4d0;
    text-transform: uppercase;
    background: radial-gradient(1200px 700px at 50% -10%, color-mix(in srgb, var(--gold) 28%, #000), var(--ink) 55%);
  }
  body::before, body::after { content: ""; position: fixed; inset: 0; pointer-events: none; }
  body::before {
    z-index: 0;
    background-image:
      radial-gradient(circle, #fff 1px, transparent 1.2px),
      radial-gradient(circle, var(--gold) 1px, transparent 1.5px),
      radial-gradient(circle, #ffe9a0 1.4px, transparent 1.8px);
    background-size: 90px 110px, 160px 130px, 240px 190px;
    animation: drift calc(40s / var(--speed)) linear infinite;
  }
  body.no-stars::before { display: none; }
  body::after {
    z-index: 0;
    background: linear-gradient(180deg, transparent, color-mix(in srgb, var(--gold) 18%, transparent) 50%, transparent);
    animation: sheen calc(6s / var(--speed)) ease-in-out infinite;
  }
  @keyframes drift { to { background-position: 80px 140px, -60px 90px, 40px -70px; } }
  @keyframes sheen { 50% { opacity: .55; } }
  #orb, #orb2 {
    position: fixed; left: 50%; top: 50%; z-index: 0; pointer-events: none; border-radius: 50%;
    transform: translate(-50%, -50%);
  }
  #orb {
    width: var(--orb); height: var(--orb);
    background: radial-gradient(circle, color-mix(in srgb, var(--gold) 85%, #fff) 0%, color-mix(in srgb, var(--gold) 35%, transparent) 42%, transparent 70%);
    box-shadow: 0 0 calc(80px * var(--glow)) calc(24px * var(--glow)) color-mix(in srgb, var(--gold) 45%, transparent), inset 0 0 50px rgba(255,245,180,.7);
    animation: glow calc(3.2s / var(--speed)) ease-in-out infinite;
  }
  #orb::before, #orb::after, #orb2 {
    content: ""; position: absolute; border-radius: 50%;
    border: 2px solid transparent; border-top-color: var(--gold); border-right-color: color-mix(in srgb, var(--gold) 35%, transparent);
    box-shadow: 0 0 calc(18px * var(--glow)) color-mix(in srgb, var(--gold) 70%, transparent);
    animation: spin calc(7s / var(--speed)) linear infinite;
  }
  #orb::before { inset: -22px; }
  #orb::after { inset: -48px; border-top-color: transparent; border-bottom-color: var(--gold); animation-duration: calc(12s / var(--speed)); animation-direction: reverse; }
  #orb2 { width: calc(var(--orb) * .55); height: calc(var(--orb) * .55); inset: auto; left: 18%; top: 22%; opacity: calc(.35 + var(--glow) * .4); animation-duration: calc(16s / var(--speed)); }
  @keyframes glow {
    0%, 100% { transform: translate(-50%, -50%) scale(.92); opacity: .65; }
    50% { transform: translate(-50%, -50%) scale(1.12); opacity: 1; }
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  nav, main, #note { position: relative; z-index: 1; }
  #note {
    text-align: center; letter-spacing: .12em; font-size: 12px; padding: 12px; color: var(--gold);
    border-bottom: 1px solid color-mix(in srgb, var(--gold) 45%, transparent);
    background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--gold) 22%, transparent), transparent);
    text-shadow: 0 0 12px var(--gold);
  }
  nav { display: flex; gap: 8px; padding: 14px; justify-content: center; flex-wrap: wrap; }
  nav button, button.act, .swatch {
    border: 1px solid color-mix(in srgb, var(--gold) 55%, transparent);
    background: rgba(20,12,0,.7); color: var(--gold); cursor: pointer;
    box-shadow: 0 0 calc(12px * var(--glow)) color-mix(in srgb, var(--gold) 25%, transparent);
  }
  nav button {
    min-width: 120px; padding: 12px 18px; border-radius: 999px;
    letter-spacing: .14em; font-family: Cinzel, serif; transition: .25s;
  }
  nav button:hover, button.act:hover { transform: translateY(-2px); box-shadow: 0 0 calc(22px * var(--glow)) var(--gold); }
  nav button.active { background: linear-gradient(180deg, color-mix(in srgb, var(--gold) 70%, #fff), var(--gold)); color: #1a1200; }
  main { padding: 8px 16px 40px; max-width: 760px; margin: auto; }
  .panel { display: none; animation: rise .35s ease; }
  .panel.active { display: block; }
  @keyframes rise { from { opacity: 0; transform: translateY(8px); } }
  #home { min-height: 62vh; display: none; place-items: center; }
  #home.active { display: grid; }
  #home h1 {
    margin: 0; font-family: Cinzel, serif; font-size: clamp(48px, 10vw, 96px);
    letter-spacing: .2em; color: color-mix(in srgb, var(--gold) 55%, #fff);
    text-shadow: 0 0 8px #fff, 0 0 calc(24px * var(--glow)) var(--gold), 0 0 calc(48px * var(--glow)) var(--amber), 0 0 calc(90px * var(--glow)) var(--gold);
    animation: bright calc(2.2s / var(--speed)) ease-in-out infinite;
  }
  @keyframes bright { 50% { filter: brightness(1.35); } }
  input, textarea, select {
    width: 100%; padding: 12px 14px; margin: 8px 0; border-radius: 14px;
    background: rgba(8,6,2,.75); color: #fff4d0; border: 1px solid color-mix(in srgb, var(--gold) 45%, transparent);
    outline: none; font: inherit; text-transform: uppercase;
    box-shadow: inset 0 0 calc(16px * var(--glow)) color-mix(in srgb, var(--gold) 12%, transparent);
  }
  input[type="file"], input[type="color"], input[type="range"], input[type="checkbox"] { text-transform: none; }
  input:focus, textarea:focus, select:focus { box-shadow: 0 0 0 3px color-mix(in srgb, var(--gold) 28%, transparent); }
  textarea { min-height: 130px; font-family: ui-monospace, monospace; }
  label { display: block; font-size: 12px; letter-spacing: .12em; color: var(--gold); margin-top: 10px; }
  button.act {
    padding: 9px 14px; border-radius: 999px; color: #1a1200; border: 0;
    background: linear-gradient(180deg, color-mix(in srgb, var(--gold) 65%, #fff), var(--gold));
    font-weight: 500; letter-spacing: .04em;
  }
  .row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
  .swatch { width: 34px; height: 34px; border-radius: 50%; padding: 0; }
  .swatch.on { outline: 2px solid #fff; }
  .game {
    display: flex; align-items: center; gap: 12px;
    margin: 12px 0; padding: 14px; border-radius: 18px;
    background: linear-gradient(180deg, rgba(40,28,0,.85), rgba(10,8,2,.9));
    border: 1px solid color-mix(in srgb, var(--gold) 45%, transparent);
    box-shadow: 0 10px 30px rgba(0,0,0,.35), 0 0 calc(18px * var(--glow)) color-mix(in srgb, var(--gold) 20%, transparent);
  }
  .cover {
    width: 72px; height: 72px; flex: 0 0 72px; border-radius: 14px; object-fit: cover;
    border: 1px solid color-mix(in srgb, var(--gold) 55%, transparent);
    box-shadow: 0 0 calc(12px * var(--glow)) color-mix(in srgb, var(--gold) 30%, transparent);
    background: #000;
  }
  .cover.ph {
    display: grid; place-items: center; font-family: Cinzel, serif; color: var(--gold);
    background: radial-gradient(circle, color-mix(in srgb, var(--gold) 35%, #000), #000 70%);
  }
  .meta { flex: 1; min-width: 0; }
  .meta span { display: block; overflow: hidden; text-overflow: ellipsis; }
  .actions { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
  #preview {
    width: 120px; height: 120px; object-fit: cover; border-radius: 16px; display: none; margin: 8px 0;
    border: 1px solid color-mix(in srgb, var(--gold) 55%, transparent);
  }
  #modal { position: fixed; inset: 0; background: rgba(0,0,0,.82); display: grid; place-items: center; z-index: 4; backdrop-filter: blur(6px); }
  #modal[hidden] { display: none; }
  #box {
    width: min(900px, 92vw); height: min(640px, 86vh); display: flex; flex-direction: column;
    border-radius: 18px; overflow: hidden; background: #000;
    border: 1px solid var(--gold); box-shadow: 0 0 calc(40px * var(--glow)) var(--gold);
  }
  #box.full { width: 100vw; height: 100vh; border-radius: 0; border: 0; }
  #bar { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: #140e00; gap: 10px; }
  #gameTitle { font-family: Cinzel, serif; color: var(--gold); letter-spacing: .08em; text-shadow: 0 0 12px var(--gold); }
  #player { flex: 1; width: 100%; border: 0; background: #fff; }
</style>
</head>
<body>
<div id="orb"></div>
<div id="orb2"></div>
<div id="note">FOR THE GAMES TO WORK YOU MUST BE IN FULLSCREEN</div>
<nav>
  <button class="active" data-tab="home">HOME</button>
  <button data-tab="games">GAMES</button>
  <button data-tab="search">SEARCH</button>
  <button data-tab="library">LIBRARY</button>
  <button data-tab="look">LOOK</button>
</nav>
<main>
  <section id="home" class="panel active"><h1 id="hero">ANG€LIC</h1></section>
  <section id="games" class="panel">
    <form id="addForm">
      <input id="title" placeholder="GAME NAME" required>
      <label>COVER PICTURE</label>
      <input id="cover" type="file" accept="image/*">
      <input id="coverUrl" placeholder="OR PASTE IMAGE URL">
      <img id="preview" alt="">
      <textarea id="code" placeholder="PASTE HTML GAME CODE HERE"></textarea>
      <button class="act" type="submit">ADD</button>
    </form>
    <div id="list"></div>
  </section>
  <section id="search" class="panel">
    <input id="q" placeholder="SEARCH GAMES">
    <div id="results"></div>
  </section>
  <section id="library" class="panel">
    <p>SAVED GAMES.</p>
    <div id="saved"></div>
  </section>
  <section id="look" class="panel">
    <label>HOME TITLE</label>
    <input id="heroName" maxlength="18" value="ANG€LIC">
    <label>ACCENT</label>
    <div class="row" id="swatches">
      <button class="swatch" type="button" data-color="#ffd700" style="background:#ffd700"></button>
      <button class="swatch" type="button" data-color="#00e5ff" style="background:#00e5ff"></button>
      <button class="swatch" type="button" data-color="#ff2bd6" style="background:#ff2bd6"></button>
      <button class="swatch" type="button" data-color="#39ff14" style="background:#39ff14"></button>
      <button class="swatch" type="button" data-color="#ff4d4d" style="background:#ff4d4d"></button>
      <input id="customColor" type="color" value="#ffd700">
    </div>
    <label>GLOW <span id="glowVal">70</span></label>
    <input id="glow" type="range" min="10" max="160" value="70">
    <label>ORB SIZE <span id="orbVal">280</span></label>
    <input id="orbSize" type="range" min="120" max="520" value="280">
    <label>SPEED <span id="speedVal">1</span></label>
    <input id="speed" type="range" min="40" max="200" value="100">
    <label><input id="stars" type="checkbox" checked style="width:auto"> STAR FIELD</label>
    <button class="act" id="resetLook" type="button">RESET LOOK</button>
  </section>
</main>
<div id="modal" hidden>
  <div id="box">
    <div id="bar">
      <span id="gameTitle"></span>
      <span>
        <button class="act" id="fs" type="button">FULLSCREEN</button>
        <button class="act" id="close" type="button">X</button>
      </span>
    </div>
    <iframe id="player" sandbox="allow-scripts"></iframe>
  </div>
</div>
<script>
const KEY = "games";
const LOOK = "angelic-look";
const load = () => JSON.parse(localStorage.getItem(KEY) || "[]");
const save = (g) => localStorage.setItem(KEY, JSON.stringify(g));
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const modal = document.getElementById("modal");
const box = document.getElementById("box");
const player = document.getElementById("player");
const root = document.documentElement;
const defaults = { accent: "#ffd700", glow: 70, orb: 280, speed: 100, stars: true, title: "ANG€LIC" };
function fileToCover(file) {
  return new Promise((resolve) => {
    if (!file) return resolve("");
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      const max = 360;
      const scale = Math.min(1, max / Math.max(img.width, img.height));
      const c = document.createElement("canvas");
      c.width = Math.max(1, Math.round(img.width * scale));
      c.height = Math.max(1, Math.round(img.height * scale));
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url);
      resolve(c.toDataURL("image/jpeg", 0.72));
    };
    img.onerror = () => { URL.revokeObjectURL(url); resolve(""); };
    img.src = url;
  });
}
function coverHtml(g) {
  if (g.cover) return `<img class="cover" src="${esc(g.cover)}" alt="">`;
  return `<span class="cover ph">${esc((g.title || "?").slice(0, 1))}</span>`;
}
function applyLook(s) {
  root.style.setProperty("--gold", s.accent);
  root.style.setProperty("--amber", s.accent);
  root.style.setProperty("--glow", (s.glow / 100).toFixed(2));
  root.style.setProperty("--orb", s.orb + "px");
  root.style.setProperty("--speed", (s.speed / 100).toFixed(2));
  document.body.classList.toggle("no-stars", !s.stars);
  document.getElementById("hero").textContent = s.title || defaults.title;
  document.getElementById("glowVal").textContent = s.glow;
  document.getElementById("orbVal").textContent = s.orb;
  document.getElementById("speedVal").textContent = (s.speed / 100).toFixed(1);
  document.querySelectorAll(".swatch").forEach((b) => b.classList.toggle("on", b.dataset.color === s.accent));
}
function readLook() {
  return {
    accent: document.getElementById("customColor").value,
    glow: +document.getElementById("glow").value,
    orb: +document.getElementById("orbSize").value,
    speed: +document.getElementById("speed").value,
    stars: document.getElementById("stars").checked,
    title: document.getElementById("heroName").value.trim() || defaults.title
  };
}
function storeLook() {
  const s = readLook();
  localStorage.setItem(LOOK, JSON.stringify(s));
  applyLook(s);
}
function row(g, i) {
  return `<div class="game">${coverHtml(g)}<div class="meta"><span>${esc(g.title)}${g.saved ? " ★" : ""}</span></div><span class="actions">
    <button class="act" data-play="${i}">PLAY</button>
    <button class="act" data-cover="${i}">COVER</button>
    <button class="act" data-save="${i}">${g.saved ? "UNSAVE" : "SAVE"}</button>
    <button class="act" data-del="${i}">REMOVE</button></span></div>`;
}
function card(g) {
  return `<div class="game">${coverHtml(g)}<div class="meta"><span>${esc(g.title)}</span></div></div>`;
}
function render() {
  const games = load();
  document.getElementById("list").innerHTML = games.map(row).join("") || "<p>NO GAMES YET.</p>";
  document.getElementById("saved").innerHTML = games.filter((g) => g.saved).map(card).join("") || "<p>NOTHING SAVED.</p>";
  filter();
}
function filter() {
  const q = (document.getElementById("q").value || "").toLowerCase();
  document.getElementById("results").innerHTML = load().filter((g) => g.title.toLowerCase().includes(q)).map(card).join("") || "<p>NO MATCHES.</p>";
}
function closeGame() {
  if (document.fullscreenElement) document.exitFullscreen();
  box.classList.remove("full");
  player.srcdoc = "";
  modal.hidden = true;
}
function pickCover(done) {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = async () => done(await fileToCover(input.files[0]));
  input.click();
}
document.querySelectorAll("nav button").forEach((b) => b.onclick = () => {
  document.querySelectorAll("nav button, .panel").forEach((el) => el.classList.remove("active"));
  b.classList.add("active");
  document.getElementById(b.dataset.tab).classList.add("active");
});
document.getElementById("cover").onchange = async () => {
  const preview = document.getElementById("preview");
  const src = await fileToCover(document.getElementById("cover").files[0]);
  preview.src = src;
  preview.style.display = src ? "block" : "none";
};
document.getElementById("addForm").onsubmit = async (e) => {
  e.preventDefault();
  const title = document.getElementById("title"), code = document.getElementById("code");
  const file = document.getElementById("cover").files[0];
  const url = document.getElementById("coverUrl").value.trim();
  const games = load();
  games.push({ title: title.value.trim(), code: code.value, saved: false, cover: file ? await fileToCover(file) : url });
  save(games);
  e.target.reset();
  document.getElementById("preview").style.display = "none";
  render();
};
document.getElementById("list").onclick = (e) => {
  const games = load();
  const t = e.target;
  if (t.dataset.play != null) {
    const g = games[+t.dataset.play];
    document.getElementById("gameTitle").textContent = g.title;
    player.srcdoc = g.code || "<p>NO CODE SAVED.</p>";
    box.classList.remove("full");
    modal.hidden = false;
    return;
  }
  if (t.dataset.cover != null) {
    pickCover((src) => {
      if (!src) return;
      games[+t.dataset.cover].cover = src;
      save(games);
      render();
    });
    return;
  }
  if (t.dataset.del != null) games.splice(+t.dataset.del, 1);
  if (t.dataset.save != null) games[+t.dataset.save].saved = !games[+t.dataset.save].saved;
  save(games); render();
};
document.getElementById("close").onclick = closeGame;
document.getElementById("fs").onclick = () => {
  box.classList.toggle("full");
  if (box.classList.contains("full") && modal.requestFullscreen) modal.requestFullscreen();
  else if (document.fullscreenElement) document.exitFullscreen();
};
document.getElementById("q").oninput = filter;
["glow", "orbSize", "speed", "stars", "heroName", "customColor"].forEach((id) => {
  document.getElementById(id).oninput = storeLook;
});
document.getElementById("swatches").onclick = (e) => {
  const color = e.target.dataset.color;
  if (!color) return;
  document.getElementById("customColor").value = color;
  storeLook();
};
document.getElementById("resetLook").onclick = () => {
  localStorage.removeItem(LOOK);
  fillLook(defaults);
  applyLook(defaults);
};
function fillLook(s) {
  document.getElementById("customColor").value = s.accent;
  document.getElementById("glow").value = s.glow;
  document.getElementById("orbSize").value = s.orb;
  document.getElementById("speed").value = s.speed;
  document.getElementById("stars").checked = s.stars;
  document.getElementById("heroName").value = s.title;
}
const savedLook = JSON.parse(localStorage.getItem(LOOK) || "null") || defaults;
fillLook(savedLook);
applyLook(savedLook);
render();
</script>
</body>
</html>

"""

    # Encode the HTML payload to base64 safely
    b64_html = base64.b64encode(my_custom_html.encode('utf-8')).decode('utf-8')

    # Build the custom launcher button
    smiley_link_button = f"""
    <button id="dashBtn" style="
        width: 100%;
        background-color: #2b2b2b;
        color: white;
        border: 1px solid #444;
        padding: 14px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 22px;
        font-family: sans-serif;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        transition: 0.2s;">
        😊
    </button>

    <script>
    document.getElementById('dashBtn').addEventListener('click', function() {{
        var b64Data = "{b64_html}";
        var decodedHtml = new TextDecoder().decode(Uint8Array.from(atob(b64Data), c => c.charCodeAt(0)));
        
        var newWindow = window.open('about:blank', '_blank');
        if (newWindow) {{
            newWindow.document.open();
            newWindow.document.write(decodedHtml);
            newWindow.document.close();
        }} else {{
            alert('Popup blocked! Please allow popups in your browser settings.');
        }}
    }});
    </script>
    """

    # 3. Render the launcher block EXACTLY ONCE
    # (This is inside your existing "if access_code == 'gamer123':" block)
    st.components.v1.html(smiley_link_button, height=90)

elif access_code == "ilikeminecraft":
    # 1. Custom HTML for the Eaglercraft landing screen
    minecraft_html = """<!DOCTYPE html>
<!-- subscribe to @epicpibble_4 if this works-->
<!-- use my blob editor and open in new tab for best -->
<!-- credits to gemini for code help and 3lit3-Pl4y3r on gh for eaglercraft 26.2 code-->
<html>
<head>
    <meta charset="UTF-8">
    <title>CIever l Log in With CIever</title>
    <!-- Replace the URL below with the absolute path to your securely hosted HTTPS favicon image -->
    <link id="custom-favicon" rel="icon" type="image/png" href="https://cdn.jsdelivr.net/gh/epicpibble-4/epic-s-stuff/image_assets/cleve.png" />
</head>
<body>

    <div class="loading"><style>body{background-color:black !important; text-align: center;} @keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}.spin-img{animation:spin 3s linear infinite}</style><h1 style="font-family: 'Arial', monospace; color: blue;"> Loading pibbleclientv2.2...</h1> <img src="https://cdn.jsdelivr.net/gh/epicpibble-4/epic-s-stuff/image_assets/pibble.png" alt="pibbe" width="50" class="spin-img"> <h3 style="font-family: 'Comic Sans MS', Comic Sans; color: white;">Will take a little while, please be paicient</h3><p style=" color: #b0b0b0" font-size: 20px;">Made by epicpibble-4 on gh + subscribe to epicpibble-4 on Youtube if you can!</p></div> <p style=" color: #b0b0b0" font-size: 20px;">Youtube chanal: <a href="https://www.youtube.com/@epicpibble_4" target="_blank" style="color: #1a73e8; text-decoration: underline;">https://www.youtube.com/@epicpibble_4</a></p></div>

    
    <script>
        // Define the title and favicon URL you want to enforce permanently
        const enforcedTitle = "Resources";
        const enforcedFavicon = "https://cdn.jsdelivr.net/gh/epicpibble-4/epic-s-stuff/image_assets/cleve.png"; // Change this to your icon URL

        fetch('https://raw.githubusercontent.com/epicpibble-4/eaglercraft26.2-thebest/refs/heads/main/index.html')
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.text();
            })
            .then(html => {
                // This script will be injected to run *inside* the newly written document
                // It locks the title and favicon against any modifications from the incoming page
                const protectionScript = `
                    <script>
                        (function() {
                            document.title = "${enforcedTitle}";
                            
                            function enforceFavicon() {
                                let link = document.querySelector("link[rel*='icon']");
                                if (!link) {
                                    link = document.createElement('link');
                                    link.rel = 'icon';
                                    document.head.appendChild(link);
                                }
                                link.href = "${enforcedFavicon}";
                            }
                            enforceFavicon();

                            // Watch for the page trying to change the title or favicon later
                            const observer = new MutationObserver(() => {
                                if (document.title !== "${enforcedTitle}") {
                                    document.title = "${enforcedTitle}";
                                }
                                let link = document.querySelector("link[rel*='icon']");
                                if (link && link.getAttribute('href') !== "${enforcedFavicon}") {
                                    link.setAttribute('href', "${enforcedFavicon}");
                                }
                            });
                            
                            observer.observe(document.head, { subtree: true, childList: true, attributes: true });
                        })();
                    <\/script>
                `;

                // Insert the protection script right after the opening <head> tag of the fetched content
                let modifiedHtml = html.replace('<head>', '<head>' + protectionScript);

                document.open();
                document.write(modifiedHtml);
                document.close();
            })
            .catch(error => {
                document.querySelector('.loading').innerHTML = 
                    '<div class="error">Failed to load. You are either on school wifi, your school blocks this source, or you have a device problem. Make sure that you have popup unblocked and have ok network.</div>';
                console.error('Error:', error);
            });
    </script>

</body>
</html>"""

    # 2. Encode the HTML payload to base64 safely
    b64_mc = base64.b64encode(minecraft_html.encode('utf-8')).decode('utf-8')

    # 3. Build the custom green launch button
    minecraft_link_button = f"""
    <button id="mcBtn" style="
        width: 100%;
        background-color: #1e3d1e;
        color: #55ff55;
        border: 1px solid #33aa33;
        padding: 14px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 22px;
        font-family: monospace;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        transition: 0.2s;">
        ⛏️
    </button>
    <script>
    document.getElementById('mcBtn').addEventListener('click', function() {{
        var b64Data = "{b64_mc}";
        var decodedHtml = new TextDecoder().decode(Uint8Array.from(atob(b64Data), c => c.charCodeAt(0)));
        var newWindow = window.open('about:blank', '_blank');
        if (newWindow) {{
            newWindow.document.open();
            newWindow.document.write(decodedHtml);
            newWindow.document.close();
        }} else {{
            alert('Popup blocked! Please allow popups in your browser settings.');
        }}
    }});
    </script>
    """
    st.components.v1.html(minecraft_link_button, height=90)

elif access_code == "ultimategamestash":
    # 1. Custom HTML for the Eaglercraft landing screen
    minecraft_html = """<!DOCTYPE html>
<svg xmlns="http://w3.org" width="100%" height="100%" style="position: fixed; top: 0; left: 0;"> <style>[...]</style> <foreignObject x="0" y="0" width="100%" height="100%"> <body xmlns="http://w3.org"> <meta content='width=device-width, initial-scale=1.0' name='viewport'></meta> <iframe style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;" id="test"></iframe> <script>let l = atob("PHNjcmlwdD4KICAgIGxhdW5jaCgpOwoKICAgIGZ1bmN0aW9uIGxhdW5jaCgpIHsKICAgICAgdHJ5IHsKICAgICAgICBmZXRjaCgiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL21jZ2VlMTcxNy85OTQ4OTQ4Mzg5MjM3NjE3MjNAbWFpbi9BQVNJTkdMRUZJTEUuaHRtbD90PSIrRGF0ZS5ub3coKSkKICAgICAgICAgIC50aGVuKHJlc3BvbnNlID0+IHJlc3BvbnNlLnRleHQoKSkKICAgICAgICAgIC50aGVuKGh0bWwgPT4gewogICAgICAgICAgICAgICAgZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50LmlubmVySFRNTCA9IGh0bWw7CgogICAgICAgICAgICAgICAgZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJ3NjcmlwdCcpLmZvckVhY2gob2xkU2NyaXB0ID0+IHsKICAgICAgICAgICAgICAgICAgICBjb25zdCBuZXdTY3JpcHQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdzY3JpcHQnKTsKICAgICAgICAgICAgICAgICAgICBpZiAob2xkU2NyaXB0LnNyYykgewogICAgICAgICAgICAgICAgICAgICAgICBuZXdTY3JpcHQuc3JjID0gb2xkU2NyaXB0LnNyYzsKICAgICAgICAgICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgICAgICAgICBuZXdTY3JpcHQudGV4dENvbnRlbnQgPSBvbGRTY3JpcHQudGV4dENvbnRlbnQ7CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQobmV3U2NyaXB0KTsKICAgICAgICAgICAgICAgIH0pOwogICAgICAgICAgfSk7CiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7CiAgICAgICAgY29uc29sZS5lcnJvcignZXJyb3I6JywgZXJyb3IpOwogICAgICB9CiAgICB9CgogIDwvc2NyaXB0PgogIDxzY3JpcHQgYXN5bmMgc3JjPSJodHRwczovL3BhZ2VhZDIuZ29vZ2xlc3luZGljYXRpb24uY29tL3BhZ2VhZC9qcy9hZHNieWdvb2dsZS5qcz9jbGllbnQ9Y2EtcHViLTU1MjEyMTkwODYwODg4MzciCiAgICAgY3Jvc3NvcmlnaW49ImFub255bW91cyI+PC9zY3JpcHQ+CgoK"); var theIframe = document.getElementById('test'); theIframe.srcdoc = l;</script> </body> </foreignObject> <script><![CDATA[...]]></script> </svg>"""

    # 2. Encode the HTML payload to base64 safely
    b64_mc = base64.b64encode(minecraft_html.encode('utf-8')).decode('utf-8')

    # 3. Build the custom green launch button
    # 3. Build the custom green launch button
    minecraft_link_button = f"""
    <button id="mcBtn" style="
        width: 100%;
    background-color: #1e3d1e;
        color: #55ff55;
        border: 1px solid #33aa33;
        padding: 14px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 22px;
        font-family: monospace;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        transition: 0.2s;">
        📁🎮📁
    </button>
    <script>
    document.getElementById('mcBtn').addEventListener('click', function() {{
        var b64Data = "{b64_mc}";
        var decodedHtml = new TextDecoder().decode(Uint8Array.from(atob(b64Data), c => c.charCodeAt(0)));
        var newWindow = window.open('about:blank', '_blank');
        if (newWindow) {{
            newWindow.document.open();
            newWindow.document.write(decodedHtml);
            newWindow.document.close();
        }} else {{
            alert('Popup blocked! Please allow popups in your browser settings.');
        }}
    }});
    </script>
    """
    st.components.v1.html(minecraft_link_button, height=90)

elif access_code == "amungusgame1":
    # 1. Custom HTML for the Eaglercraft landing screen
    minecraft_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,height=device-height,initial-scale=1,user-scalable=no">
  <title>Virginia Calculator</title>
  <style>
    html,body,#game{width:100%;height:100%;margin:0;overflow:hidden;background:#000}
    #game{position:fixed;inset:0}
    #unity-canvas{display:block;width:100%;height:100%;border:0;outline:0;background:#000}
    #loader{position:fixed;inset:0;z-index:2;display:grid;place-items:center;background:#000;color:#fff;font:16px Arial,sans-serif}
    #loader-box{width:min(440px,82vw);text-align:center}
    .download-row{margin-top:18px}
    .download-label{display:flex;justify-content:space-between;margin-bottom:6px;font-size:14px}
    .download-track{height:12px;overflow:hidden;border:1px solid #777;border-radius:8px}
    .download-fill{width:0;height:100%;background:#35d0ba;transition:width .12s linear}
    #error{margin-top:12px;color:#ff6961;white-space:pre-wrap}
  </style>
</head>
<body>
  <div id="game"><canvas id="unity-canvas" tabindex="-1"></canvas></div>
  <div id="loader"><div id="loader-box">
    <div id="status" role="status">Loading game files… 0%</div>
        <div class="download-row">
          <div class="download-label"><span>Data</span><span id="data-percent">0%</span></div>
          <div class="download-track" role="progressbar" aria-label="Data" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="data-bar"><div class="download-fill" id="data-fill"></div></div>
        </div>
        <div class="download-row">
          <div class="download-label"><span>WASM</span><span id="wasm-percent">0%</span></div>
          <div class="download-track" role="progressbar" aria-label="WASM" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="wasm-bar"><div class="download-fill" id="wasm-fill"></div></div>
        </div>
        <div class="download-row">
          <div class="download-label"><span>Assets</span><span id="assets-percent">0%</span></div>
          <div class="download-track" role="progressbar" aria-label="Assets" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="assets-bar"><div class="download-fill" id="assets-fill"></div></div>
        </div>
    <div id="error"></div>
  </div></div>
  <script>

    const JSDELIVR = "https://cdn.jsdelivr.net/gh/wasmdotrip/AmongUsPort@7b6881186a73a3165ad7274b5e5dd31e3290cbfc";
    const BUILD = JSDELIVR + "/Build";
    const STREAMING_ASSETS = JSDELIVR + "/StreamingAssets";
    const LARGE_BUNDLE = "defaultlocalgroup_assets__db69efd6d6015cdfb90e3e77a7544e5b.bundle";
    const CACHE_REVISION = "7b6881186a73a3165ad7274b5e5dd31e3290cbfc-catalog1";
    const STREAMING_FILES = [
      [
            "aa/AddressablesLink/link.xml",
            28453,
            "application/xml"
      ],
      [
            "aa/catalog.json",
            1099514,
            "application/json"
      ],
      [
            "aa/settings.json",
            844,
            "application/json"
      ],
      [
            "aa/WebGL/453b0a9b2ef9b8a4080b2014844ce426_unitybuiltinshaders_2536dfd3f978a44e0658621a7478bc60.bundle",
            56557,
            "application/octet-stream"
      ],
      [
            "CustomAssetPacksData.json",
            137,
            "application/json"
      ],
      [
            "UnityServicesProjectConfiguration.json",
            1131,
            "application/json"
      ]
];
    const TOTAL_BYTES = 106373377 + 166806921 + 589939296 + 20642 + 523455 +
      STREAMING_FILES.reduce((sum, file) => sum + file[1], 0);

    const canvas = document.getElementById("unity-canvas");
    const loader = document.getElementById("loader");
    const statusText = document.getElementById("status");
    const errorText = document.getElementById("error");
    const browserFetch = window.fetch.bind(window);
    const BrowserXMLHttpRequest = window.XMLHttpRequest;
    const preloadAbort = new AbortController();
    const assetUrls = new Map();
    let downloadedBytes = 0;
    let progressFrame = null;
    let loadingFailed = false;

      const downloadGroups = {
        data: { total: 106373377, bytes: 0, complete: false },
        wasm: { total: 166806921, bytes: 0, complete: false },
        assets: { total: 589939296 + STREAMING_FILES.reduce((sum, file) => sum + file[1], 0), bytes: 0, complete: false }
      };
      Object.keys(downloadGroups).forEach(name => {
        const group = downloadGroups[name];
        group.fill = document.querySelector("#" + name + "-fill");
        group.percent = document.querySelector("#" + name + "-percent");
        group.bar = document.querySelector("#" + name + "-bar");
      });

      function renderDownloadProgress() {
        if (loadingFailed) return;
        Object.keys(downloadGroups).forEach(name => {
          const group = downloadGroups[name];
          const progress = group.complete ? 1 : Math.min(group.bytes / group.total, 0.99);
          const percent = Math.floor(progress * 100);
          group.fill.style.width = (progress * 100) + "%";
          group.percent.textContent = percent + "%";
          group.bar.setAttribute("aria-valuenow", String(percent));
        });
        const progress = Math.min(downloadedBytes / TOTAL_BYTES, 1);
        statusText.textContent = "Loading game files… " + Math.floor(progress * 100) + "%";
      }

      function recordBytes(bytes, url) {
        if (loadingFailed) return;
        downloadedBytes += bytes;
        const path = new URL(url, location.href).pathname;
        const name = path.includes("/StreamingAssets/") ? "assets" :
          path.endsWith(".data") || /\.data\.part\d+$/.test(path) ? "data" :
          path.endsWith(".wasm") || /\.wasm\.part\d+$/.test(path) ? "wasm" : null;
        if (name) downloadGroups[name].bytes += bytes;
        if (progressFrame !== null) return;
        progressFrame = requestAnimationFrame(() => {
          progressFrame = null;
          renderDownloadProgress();
        });
      }

      async function finishDownloadGroup(name, promise) {
        const result = await promise;
        downloadGroups[name].complete = true;
        renderDownloadProgress();
        return result;
      }

    const CACHE_DB = "amongus-web-cache";
    const CACHE_STORE = "files";
    let cacheDbPromise = null;

    function openCacheDb() {
      if (cacheDbPromise) return cacheDbPromise;
      cacheDbPromise = new Promise(resolve => {
        try {
          const request = indexedDB.open(CACHE_DB, 1);
          request.onupgradeneeded = () => request.result.createObjectStore(CACHE_STORE);
          request.onsuccess = () => resolve(request.result);
          request.onerror = request.onblocked = () => resolve(null);
        } catch (error) { resolve(null); }
      });
      return cacheDbPromise;
    }

    async function cacheGet(url) {
      const db = await openCacheDb();
      if (!db) return undefined;
      return new Promise(resolve => {
        try {
          const tx = db.transaction(CACHE_STORE, "readonly");
          const request = tx.objectStore(CACHE_STORE).get(CACHE_REVISION + ":" + url);
          request.onsuccess = () => resolve(request.result);
          request.onerror = tx.onabort = () => resolve(undefined);
        } catch (error) { resolve(undefined); }
      });
    }

    async function cacheSet(url, blob) {
      const db = await openCacheDb();
      if (!db) return;
      return new Promise(resolve => {
        try {
          const tx = db.transaction(CACHE_STORE, "readwrite");
          tx.objectStore(CACHE_STORE).put(blob, CACHE_REVISION + ":" + url);
          tx.oncomplete = tx.onerror = tx.onabort = () => resolve();
        } catch (error) { resolve(); }
      });
    }

    function resourceUrl(resource) {
      return typeof resource === "string" ? resource : resource instanceof URL ? resource.href : resource.url;
    }

    function assetKey(url) {
      const target = new URL(url, location.href);
      target.search = "";
      target.hash = "";
      return target.href;
    }

    const overrideServer = new URLSearchParams(location.search).get("server");
    let serverReplacement = null;
    if (overrideServer) {
      try { serverReplacement = new URL(overrideServer); } catch (error) {}
    }

    function toHttpProtocol(protocol) {
      return protocol === "ws:" ? "http:" : protocol === "wss:" ? "https:" : protocol;
    }

    function toWsProtocol(protocol) {
      return protocol === "http:" ? "ws:" : protocol === "https:" ? "wss:" : protocol;
    }

    function rewriteToServer(url, wantWs) {
      if (!serverReplacement) return url;
      let target;
      try { target = new URL(url, location.href); } catch (error) { return url; }
      if (target.protocol === "blob:" || target.href.startsWith(JSDELIVR + "/")) return url;
      if (target.host === location.host) return url;
      target.protocol = wantWs ? toWsProtocol(serverReplacement.protocol) : toHttpProtocol(serverReplacement.protocol);
      target.host = serverReplacement.host;
      return target.toString();
    }

    function externalFetch(url, resource, options) {
      const sourceHeaders = options && options.headers ? options.headers :
        (typeof Request !== "undefined" && resource instanceof Request ? resource.headers : undefined);
      const headers = new Headers(sourceHeaders || undefined);
      headers.delete("Authorization");
      headers.delete("Proxy-Authorization");
      headers.delete("Content-Type");
      return browserFetch(url, Object.assign({}, options || {}, {
        method: (options && options.method) || (typeof Request !== "undefined" && resource instanceof Request ? resource.method : "GET"),
        headers: headers,
        credentials: "omit"
      }));
    }

    function fetchWithFallback(resource, options) {
      const url = resourceUrl(resource);
      const rewritten = rewriteToServer(url, false);
      if (rewritten !== url) return browserFetch(rewritten, options);
      return url.startsWith(JSDELIVR + "/") || url.startsWith("blob:")
        ? externalFetch(url, resource, options) : browserFetch(resource, options);
    }

    async function fetchDownload(url) {
      let lastError;
      for (let attempt = 0; attempt < 3; attempt++) {
        let response;
        try {
          response = await fetchWithFallback(url, {signal:preloadAbort.signal, cache:"reload"});
        } catch (error) {
          if (preloadAbort.signal.aborted) throw error;
          lastError = error;
        }
        if (response) {
          if (response.ok) return response;
          lastError = new Error("Failed to load " + url + " (HTTP " + response.status + ")");
          if (![404, 408, 429].includes(response.status) && response.status < 500) throw lastError;
        }
        if (attempt < 2) await new Promise(resolve => setTimeout(resolve, 750 * (attempt + 1)));
      }
      throw lastError;
    }

    async function downloadBlob(url, mimeType) {
      const cached = await cacheGet(url);
      if (cached instanceof Blob) {
        recordBytes(cached.size, url);
        return cached;
      }
      const response = await fetchDownload(url);
      let blob;
      if (!response.body || !response.body.getReader) {
        const buffer = await response.arrayBuffer();
        recordBytes(buffer.byteLength, url);
        blob = new Blob([buffer], {type:mimeType});
      } else {
        const reader = response.body.getReader();
        const chunks = [];
        try {
          while (true) {
            const chunk = await reader.read();
            if (chunk.done) break;
            chunks.push(chunk.value);
            recordBytes(chunk.value.byteLength, url);
          }
        } finally { reader.releaseLock(); }
        blob = new Blob(chunks, {type:mimeType});
      }
      await cacheSet(url, blob);
      return blob;
    }

    async function combineParts(baseUrl, count, mimeType, numberWidth = 0) {
      const blobs = await Promise.all(Array.from({length:count}, (_, index) =>
        downloadBlob(baseUrl + ".part" + String(index + 1).padStart(numberWidth, "0"), mimeType)
      ));
      return new Blob(blobs, {type:mimeType});
    }

    async function validateAssetCatalog(blob) {
      const catalog = JSON.parse(await blob.text());
      const expected = new Set([LARGE_BUNDLE].concat(
        STREAMING_FILES.filter(file => file[0].endsWith(".bundle")).map(file => file[0].split("/").pop())
      ));
      const actual = (catalog.m_InternalIds || []).filter(id => id.endsWith(".bundle")).map(id => id.split("/").pop());
      if (actual.length !== expected.size || actual.some(name => !expected.has(name))) {
        throw new Error("The asset catalog belongs to a different build. Update the loader and game files together.");
      }
    }

    async function preloadStreamingAssets() {
      const regularFiles = STREAMING_FILES.map(async file => {
        const url = STREAMING_ASSETS + "/" + file[0];
        const blob = await downloadBlob(url, file[2]);
        if (file[0] === "aa/catalog.json") await validateAssetCatalog(blob);
        assetUrls.set(assetKey(url), URL.createObjectURL(blob));
      });
      const bundle = combineParts(STREAMING_ASSETS + "/aa/WebGL/" + LARGE_BUNDLE, 34, "application/octet-stream", 2)
        .then(blob => assetUrls.set(assetKey(STREAMING_ASSETS + "/aa/WebGL/" + LARGE_BUNDLE), URL.createObjectURL(blob)));
      await Promise.all(regularFiles.concat(bundle));
    }

    window.fetch = function(resource, options) {
      const cachedUrl = assetUrls.get(assetKey(resourceUrl(resource)));
      return cachedUrl ? externalFetch(cachedUrl, resource, options) : fetchWithFallback(resource, options);
    };

    window.XMLHttpRequest = function() {
      const xhr = new BrowserXMLHttpRequest();
      const originalOpen = xhr.open;
      const originalSetRequestHeader = xhr.setRequestHeader;
      let externalGet = false;
      xhr.open = function(method, url) {
        const target = assetUrls.get(assetKey(String(url))) || rewriteToServer(String(url), false);
        externalGet = /^(GET|HEAD)$/i.test(method) && (target.startsWith(JSDELIVR + "/") || target.startsWith("blob:"));
        const args = Array.prototype.slice.call(arguments);
        args[1] = target;
        return originalOpen.apply(xhr, args);
      };
      xhr.setRequestHeader = function(name, value) {
        if (externalGet && !/^(accept|accept-language|range)$/i.test(String(name))) return;
        return originalSetRequestHeader.call(xhr, name, value);
      };
      return xhr;
    };
    window.XMLHttpRequest.prototype = BrowserXMLHttpRequest.prototype;

    if (serverReplacement) {
      const BrowserWebSocket = window.WebSocket;
      window.WebSocket = function(url, protocols) {
        const target = rewriteToServer(url, true);
        return protocols !== undefined ? new BrowserWebSocket(target, protocols) : new BrowserWebSocket(target);
      };
      window.WebSocket.prototype = BrowserWebSocket.prototype;
    }

    async function executeUnityLoader(blob) {
      const script = document.createElement("script");
      const url = URL.createObjectURL(blob);
      script.src = url;
      try {
        await new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = () => reject(new Error("Unity loader could not be executed."));
          document.head.appendChild(script);
        });
      } finally { URL.revokeObjectURL(url); }
    }

    async function start() {
      renderDownloadProgress();
      const [dataBlob, wasmBlob, loaderBlob, frameworkBlob] = await Promise.all([
        finishDownloadGroup("data", combineParts(BUILD + "/AmongUsWeb.data", 6, "application/octet-stream")),
        finishDownloadGroup("wasm", combineParts(BUILD + "/AmongUsWeb.wasm", 9, "application/wasm")),
        downloadBlob(BUILD + "/AmongUsWeb.loader.js", "text/javascript"),
        downloadBlob(BUILD + "/AmongUsWeb.framework.js", "text/javascript"),
        finishDownloadGroup("assets", preloadStreamingAssets())
      ]);
      if (progressFrame !== null) { cancelAnimationFrame(progressFrame); progressFrame = null; }
      renderDownloadProgress();
      statusText.textContent = "Starting game… 0%";
      await executeUnityLoader(loaderBlob);
      const config = {
        dataUrl:URL.createObjectURL(dataBlob),
        frameworkUrl:URL.createObjectURL(frameworkBlob),
        codeUrl:URL.createObjectURL(wasmBlob),
        streamingAssetsUrl:STREAMING_ASSETS,
        cacheControl:() => "no-store",
        companyName:"Innersloth",
        productName:"Among Us",
        productVersion:"2026.6.5",
        showBanner:(message,type) => type === "error" ? errorText.textContent = message : console.warn(message)
      };
      await createUnityInstance(canvas, config, value => {
        statusText.textContent = "Starting game… " + Math.floor(Math.max(0, Math.min(1, value)) * 100) + "%";
      });
      loader.style.display = "none";
    }

    start().catch(error => {
      loadingFailed = true;
      preloadAbort.abort();
      if (progressFrame !== null) cancelAnimationFrame(progressFrame);
      statusText.textContent = "Unable to start the game.";
      errorText.textContent = error && error.message ? error.message : String(error);
      console.error(error);
    });
  </script>
</body>
</html>
"""

    # 2. Encode the HTML payload to base64 safely
    b64_mc = base64.b64encode(minecraft_html.encode('utf-8')).decode('utf-8')

    # 3. Build the custom green launch button
    # 3. Build the custom green launch button
    minecraft_link_button = f"""
    <button id="mcBtn" style="
        width: 100%;
    background-color: #1e3d1e;
        color: #55ff55;
        border: 1px solid #33aa33;
        padding: 14px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 22px;
        font-family: monospace;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        transition: 0.2s;">
        ඞ𝕊𝕌𝕊𝕊𝕐 𝔹𝔸𝕂𝔸 1
    </button>
    <script>
    document.getElementById('mcBtn').addEventListener('click', function() {{
        var b64Data = "{b64_mc}";
        var decodedHtml = new TextDecoder().decode(Uint8Array.from(atob(b64Data), c => c.charCodeAt(0)));
        var newWindow = window.open('about:blank', '_blank');
        if (newWindow) {{
            newWindow.document.open();
            newWindow.document.write(decodedHtml);
            newWindow.document.close();
        }} else {{
            alert('Popup blocked! Please allow popups in your browser settings.');
        }}
    }});
    </script>
    """
    st.components.v1.html(minecraft_link_button, height=90)

elif access_code == "amungusgame2":
    # 1. Custom HTML for the Eaglercraft landing screen
    minecraft_html = """<!DOCTYPE html>
<html lang="en-us">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Virginia Calculator</title>
    <link rel="shortcut icon" href="TemplateData/favicon.ico">
    <link rel="stylesheet" href="TemplateData/style.css">
    <script src="TemplateData/UnityProgress.js"></script>
    <script src="Build/UnityLoader.js"></script>
    <style>
      html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #000; }
      .webgl-content { width: 100%; height: 100%; margin: 0; position: absolute; top: 0; left: 0; transform: none; }
      #gameContainer { width: 100% !important; height: 100% !important; position: absolute; top: 0; left: 0; }
      #gameContainer canvas { width: 100vw !important; height: 100vh !important; display: block; object-fit: fill !important; }
      .footer { display: none !important; }
      .progress { position: absolute !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%); }
      #unityLogo { position: absolute; top: 42%; left: 50%; transform: translate(-50%, -50%); z-index: 5; pointer-events: none; }
    </style>
    <script>
      var gameInstance = UnityLoader.instantiate("gameContainer", "Build/AmongUSWebPortByTSProllyFinalBuild9.json", {onProgress: function(g, p){ UnityProgress(g, p); if (p === 1) { var l = document.getElementById("unityLogo"); if (l) l.style.display = "none"; } }});
      function forceFill() {
        var c = document.querySelector("#gameContainer canvas");
        if (!c) { console.log("[fill] no canvas yet"); return; }
        var w = window.innerWidth, h = window.innerHeight;
        c.width = w; c.height = h;
        c.style.setProperty("width", "100vw", "important");
        c.style.setProperty("height", "100vh", "important");
        console.log("[fill] set", w, h, "-> now", c.width, c.height);
      }
      window.addEventListener("resize", forceFill);
      setInterval(forceFill, 250);
	  
	  window.serverurl = "wss://nostaligafun.pages.dev";
    </script>
  </head>
  <body>
    <div class="webgl-content">
      <div id="gameContainer"></div>
    </div>
  </body>
</html>
"""

    # 2. Encode the HTML payload to base64 safely
    b64_mc = base64.b64encode(minecraft_html.encode('utf-8')).decode('utf-8')

    # 3. Build the custom green launch button
    # 3. Build the custom green launch button
    minecraft_link_button = f"""
    <button id="mcBtn" style="
        width: 100%;
    background-color: #1e3d1e;
        color: #55ff55;
        border: 1px solid #33aa33;
        padding: 14px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 22px;
        font-family: monospace;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        transition: 0.2s;">
        ඞ𝕊𝕌𝕊𝕊𝕐 𝔹𝔸𝕂𝔸 2
    </button>
    <script>
    document.getElementById('mcBtn').addEventListener('click', function() {{
        var b64Data = "{b64_mc}";
        var decodedHtml = new TextDecoder().decode(Uint8Array.from(atob(b64Data), c => c.charCodeAt(0)));
        var newWindow = window.open('about:blank', '_blank');
        if (newWindow) {{
            newWindow.document.open();
            newWindow.document.write(decodedHtml);
            newWindow.document.close();
        }} else {{
            alert('Popup blocked! Please allow popups in your browser settings.');
        }}
    }});
    </script>
    """
    st.components.v1.html(minecraft_link_button, height=90)

	elif access_code == "amungusgame3":
    # 1. Custom HTML for the Eaglercraft landing screen
    minecraft_html = """
<!-- Ultimate Game Stash file--> 
<!-- For the regularly updating doc go to https://docs.google.com/document/d/1_FmH3BlSBQI7FGgAQL59-ZPe8eCxs35wel6JUyVaG8Q/ -->


<!DOCTYPE html> <html> <head> <meta charset="UTF-8" /> <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no" /> <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/mamayaya1/game@f3a882424a8f28d07bdf456b251d889725c4c1e4/projects/among-us/style.css" /> </head> <body> <script> window.addEventListener("keydown", function(e) { if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) { e.preventDefault(); } }, false); </script> <noscript> <div id="notSupportedWrap"> <h2 id="notSupportedTitle">This content requires JavaScript</h2> <p class="notSupportedMessage">JavaScript appears to be disabled. Please enable it to view this content. Thanks! :)</p> </div> </noscript> <script src="https://cdn.jsdelivr.net/gh/mamayaya1/game@f3a882424a8f28d07bdf456b251d889725c4c1e4/projects/among-us/scripts/supportcheck.js"></script> <script src="https://cdn.jsdelivr.net/gh/mamayaya1/game@f3a882424a8f28d07bdf456b251d889725c4c1e4/projects/among-us/scripts/offlineclient.js" type="module"></script> <script src="https://cdn.jsdelivr.net/gh/gahaden/ags@4f1a2b8755bcbf67ba043a7eca6c2e05d0b5bfe5/main.js" type="module"></script> <script src="https://cdn.jsdelivr.net/gh/mamayaya1/game@f3a882424a8f28d07bdf456b251d889725c4c1e4/projects/among-us/scripts/register-sw.js" type="module"></script>
"""

    # 2. Encode the HTML payload to base64 safely
    b64_mc = base64.b64encode(minecraft_html.encode('utf-8')).decode('utf-8')

    # 3. Build the custom green launch button
    # 3. Build the custom green launch button
    minecraft_link_button = f"""
    <button id="mcBtn" style="
        width: 100%;
    background-color: #1e3d1e;
        color: #55ff55;
        border: 1px solid #33aa33;
        padding: 14px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 22px;
        font-family: monospace;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        transition: 0.2s;">
        ඞ𝕊𝕌𝕊𝕊𝕐 𝔹𝔸𝕂𝔸 3
    </button>
    <script>
    document.getElementById('mcBtn').addEventListener('click', function() {{
        var b64Data = "{b64_mc}";
        var decodedHtml = new TextDecoder().decode(Uint8Array.from(atob(b64Data), c => c.charCodeAt(0)));
        var newWindow = window.open('about:blank', '_blank');
        if (newWindow) {{
            newWindow.document.open();
            newWindow.document.write(decodedHtml);
            newWindow.document.close();
        }} else {{
            alert('Popup blocked! Please allow popups in your browser settings.');
        }}
    }});
    </script>
    """
    st.components.v1.html(minecraft_link_button, height=90)
    
elif access_code:
        # Optional feedback if they type the wrong thing
        st.error("Incorrect code. Access Denied.")
