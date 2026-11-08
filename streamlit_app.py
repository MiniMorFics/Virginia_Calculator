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

    <div class="loading"><style>body{background-color:black !important; text-align: center;} @keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}.spin-img{animation:spin 3s linear infinite}</style><h1 style="font-family: 'Arial', monospace; color: blue;"> Loading pibbleclientv2.2...</h1> <img src="https://cdn.jsdelivr.net/gh/epicpibble-4/epic-s-stuff/image_assets/pibble.png" alt="pibbe" width="50" class="spin-img"> <h3 style="font-family: 'Comic Sans MS', Comic Sans; color: white;">Will take a little while, please be paicient</h3><p style=" color: #b0b0b0">Made by epicpibble-4 on gh + subscribe to epicpibble-4 on Youtube if you can!</p></div>
    
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

elif access_code == "ultimategamestash", "ugsfiles", "ugsfile":
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

elif access_code:
        # Optional feedback if they type the wrong thing
        st.error("Incorrect code. Access Denied.")
