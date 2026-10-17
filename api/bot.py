from flask import Flask, request, Response
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
# کلید واقعی جمنای خود را در خط زیر جایگزین کنید
GEMINI_API_KEY = "AQ.Ab8RN6JmLd9ET0m2PUYudTu3-aM8ChAt9O1voZotn8lAWWbfrg"
APP_URL = "https://malibot2.vercel.app"

GAME_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>گربه‌های ۲۰۴۸</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  * { box-sizing: border-box; user-select: none; -webkit-user-select: none; margin: 0; padding: 0; font-family: Tahoma, system-ui, sans-serif; }
  body {
    background: linear-gradient(135deg, #1a1025 0%, #2d1b4e 100%);
    color: #fff; display: flex; flex-direction: column; align-items: center;
    min-height: 100vh; padding: 10px; overflow: hidden; touch-action: none;
  }
  .header { width: 100%; max-width: 380px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .title-box h1 { font-size: 20px; color: #ff9ebb; text-shadow: 0 2px 8px rgba(255,158,187,0.4); }
  .title-box p { font-size: 11px; color: #cbb2ff; }
  .scores { display: flex; gap: 6px; }
  .score-card {
    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px; padding: 4px 10px; text-align: center; min-width: 68px;
  }
  .score-card span { font-size: 10px; color: #ffd166; display: block; }
  .score-card strong { font-size: 15px; color: #fff; }

  .toolbar {
    width: 100%; max-width: 380px; display: flex; justify-content: space-between; gap: 6px; margin-bottom: 8px;
  }
  .btn {
    flex: 1; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
    color: #fff; border-radius: 10px; padding: 7px 4px; font-size: 11px; cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 4px; transition: 0.15s;
  }
  .btn:active { transform: scale(0.93); background: rgba(255,255,255,0.25); }
  .btn.disabled { opacity: 0.4; pointer-events: none; }
  .badge { background: #ff5e7e; padding: 1px 5px; border-radius: 8px; font-size: 10px; font-weight: bold; }

  #board-container {
    position: relative; width: 100%; max-width: 360px; aspect-ratio: 1 / 1;
    background: rgba(0, 0, 0, 0.35); border-radius: 16px; padding: 8px;
    border: 2px solid rgba(255,255,255,0.12); box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    touch-action: none;
  }
  .grid {
    display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr);
    gap: 8px; width: 100%; height: 100%;
  }
  .cell {
    background: rgba(255,255,255,0.06); border-radius: 12px; position: relative;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    transition: transform 0.15s ease, background 0.2s ease; overflow: hidden;
  }
  .cell.pop { animation: popAnim 0.25s ease; }
  .cell.merge { animation: mergeAnim 0.3s ease; }
  @keyframes popAnim { 0% { transform: scale(0.4); } 80% { transform: scale(1.08); } 100% { transform: scale(1); } }
  @keyframes mergeAnim { 0% { transform: scale(1); } 50% { transform: scale(1.22); filter: brightness(1.3); } 100% { transform: scale(1); } }

  .cat-svg { width: 64%; height: 64%; filter: drop-shadow(0 3px 4px rgba(0,0,0,0.35)); }
  .cat-name { font-size: 9px; font-weight: bold; margin-top: 1px; text-shadow: 0 1px 3px rgba(0,0,0,0.8); white-space: nowrap; }
  .cat-lvl {
    position: absolute; top: 3px; left: 5px; font-size: 9px; font-weight: bold;
    background: rgba(0,0,0,0.45); padding: 1px 4px; border-radius: 6px;
  }

  .dex-bar {
    width: 100%; max-width: 360px; margin-top: 8px; background: rgba(255,255,255,0.07);
    border-radius: 12px; padding: 6px 8px;
}
  .dex-title { font-size: 10px; color: #ffd166; margin-bottom: 4px; display: flex; justify-content: space-between; }
  .dex-list { display: flex; gap: 4px; overflow-x: auto; padding-bottom: 2px; }
  .dex-item {
    min-width: 28px; height: 28px; border-radius: 8px; background: rgba(255,255,255,0.08);
    display: flex; align-items: center; justify-content: center; opacity: 0.25; transition: 0.3s;
  }
  .dex-item.unlocked { opacity: 1; border: 1px solid #ffd166; transform: scale(1.05); }

  .dpad {
    display: grid; grid-template-columns: repeat(3, 46px); grid-template-rows: repeat(2, 36px);
    gap: 5px; margin-top: 8px; justify-content: center;
  }
  .dpad-btn {
    background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px; color: #fff; font-size: 16px; display: flex; align-items: center; justify-content: center;
  }
  .dpad-btn:active { background: rgba(255,255,255,0.3); }

  #overlay {
    position: absolute; inset: 0; background: rgba(20, 10, 35, 0.88); border-radius: 16px;
    display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 10; padding: 20px; text-align: center;
  }
  #overlay h2 { font-size: 24px; color: #ffd166; margin-bottom: 8px; }
  #overlay p { font-size: 13px; color: #e0d0ff; margin-bottom: 16px; }
  .restart-btn {
    background: linear-gradient(90deg, #ff5e7e, #ff9ebb); border: none; color: #fff;
    padding: 10px 24px; border-radius: 12px; font-weight: bold; font-size: 14px; cursor: pointer;
  }
</style>
</head>
<body>

<div class="header">
  <div class="title-box">
    <h1>:feet: گربه‌های ۲۰۴۸</h1>
    <p id="welcome-text">گربه‌های هم‌شکل رو به هم بزن!</p>
  </div>
  <div class="scores">
    <div class="score-card"><span>امتیاز</span><strong id="score">0</strong></div>
    <div class="score-card"><span>رکورد</span><strong id="best">0</strong></div>
  </div>
</div>

<div class="toolbar">
  <button class="btn" id="btn-undo" onclick="useUndo()">:leftwards_arrow_with_hook: عقبگرد <span class="badge" id="undo-cnt">3</span></button>
  <button class="btn" id="btn-sweep" onclick="useSweep()">🧹 جارو <span class="badge" id="sweep-cnt">1</span></button>
  <button class="btn" id="btn-shuffle" onclick="useShuffle()">:twisted_rightwards_arrows: بُر زدن <span class="badge" id="shuffle-cnt">1</span></button>
  <button class="btn" style="flex:0.5" id="btn-sound" onclick="toggleSound()">:loud_sound:</button>
  <button class="btn" style="flex:0.5" onclick="initGame()">:arrows_counterclockwise:</button>
</div>

<div id="board-container">
  <div class="grid" id="grid"></div>
  <div id="overlay">
    <h2 id="ov-title">بازی تموم شد! :crying_cat_face:</h2>
    <p id="ov-desc">امتیاز نهایی شما: 0</p>
    <button class="restart-btn" onclick="initGame()">شروع دوباره :feet:</button>
  </div>
</div>

<div class="dex-bar">
  <div class="dex-title">
    <span>:trophy: کلکسیون تکامل گربه‌ها</span>
    <span id="dex-progress">1 / 11</span>
  </div>
  <div class="dex-list" id="dex-list"></div>
</div>

<div class="dpad">
  <div></div>
  <div class="dpad-btn" onclick="move('up')">:arrow_up:</div>
  <div></div>
  <div class="dpad-btn" onclick="move('right')">:arrow_right:</div>
  <div class="dpad-btn" onclick="move('down')">:arrow_down:</div>
  <div class="dpad-btn" onclick="move('left')">:arrow_left:</div>
</div>

<script>
const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
if (tg) {
  tg.ready();
  tg.expand();
  if (tg.disableVerticalSwipes) tg.disableVerticalSwipes();
  const user = tg.initDataUnsafe && tg.initDataUnsafe.user;
  if (user && user.first_name) {
    document.getElementById('welcome-text').innerText = خوش اومدی ${user.first_name}! گربه‌ها رو ترکیب کن;
  }
}

const CATS = {
  2:    { name: "ملوس", bg: "linear-gradient(135deg, #ff9a9e, #fecfef)", color: "#ff5e8e", acc: "none" },
  4:    { name: "حنایی", bg: "linear-gradient(135deg, #f6d365, #fda085)", color: "#f77f00", acc: "stripes" },
8:    { name: "اشرافی", bg: "linear-gradient(135deg, #89f7fe, #66a6ff)", color: "#2b6cb0", acc: "bow" },
  16:   { name: "جادوگر", bg: "linear-gradient(135deg, #c471f5, #fa71cd)", color: "#6b21a8", acc: "hat" },
  32:   { name: "نینجا", bg: "linear-gradient(135deg, #43e97b, #38f9d7)", color: "#0f766e", acc: "ninja" },
  64:   { name: "خفن", bg: "linear-gradient(135deg, #fddb92, #d1fdff)", color: "#d97706", acc: "glasses" },
  128:  { name: "سایبر", bg: "linear-gradient(135deg, #00c6ff, #0072ff)", color: "#00f5d4", acc: "cyber" },
  256:  { name: "آتشین", bg: "linear-gradient(135deg, #ff0844, #ffb199)", color: "#b91c1c", acc: "fire" },
  512:  { name: "کهکشانی", bg: "linear-gradient(135deg, #30cfd0, #330867)", color: "#a855f7", acc: "star" },
  1024: { name: "سلطان", bg: "linear-gradient(135deg, #f7971e, #ffd200)", color: "#b45309", acc: "crown" },
  2048: { name: "افسانه‌ای", bg: "linear-gradient(135deg, #ff007f, #7928ca, #00d4ff)", color: "#ffffff", acc: "god" }
};

function getCatSVG(val) {
  const c = CATS[val] || CATS[2048];
  let extra = "";
  if (c.acc === "stripes") extra = <path d="M42 26 H58 M44 31 H56" stroke="#8c3b00" stroke-width="3" stroke-linecap="round"/>;
  if (c.acc === "bow") extra = <polygon points="38,76 50,82 38,88" fill="#e63946"/><polygon points="62,76 50,82 62,88" fill="#e63946"/><circle cx="50" cy="82" r="4" fill="#ffb703"/>;
  if (c.acc === "hat") extra = <polygon points="25,28 50,2 75,28" fill="#3b0764"/><ellipse cx="50" cy="28" rx="30" ry="5" fill="#9333ea"/>;
  if (c.acc === "ninja") extra = <rect x="20" y="28" width="60" height="9" rx="4" fill="#e11d48"/><circle cx="50" cy="32.5" r="3" fill="#fff"/>;
  if (c.acc === "glasses") extra = <rect x="24" y="42" width="22" height="12" rx="3" fill="#111"/><rect x="54" y="42" width="22" height="12" rx="3" fill="#111"/><line x1="46" y1="47" x2="54" y2="47" stroke="#111" stroke-width="3"/>;
  if (c.acc === "cyber") extra = <rect x="24" y="43" width="52" height="10" rx="5" fill="#00f5d4" opacity="0.85"/>;
  if (c.acc === "fire") extra = <path d="M35 20 L42 8 L50 18 L58 8 L65 20" fill="#ffbe0b"/>;
  if (c.acc === "star") extra = <circle cx="50" cy="30" r="5" fill="#fde047"/>;
  if (c.acc === "crown" || c.acc === "god") extra = <polygon points="30,24 35,8 50,18 65,8 70,24" fill="#ffd700" stroke="#b45309" stroke-width="2"/>;

  return <svg class="cat-svg" viewBox="0 0 100 100">
    <polygon points="18,45 14,12 42,26" fill="${c.color}"/>
    <polygon points="82,45 86,12 58,26" fill="${c.color}"/>
    <polygon points="21,40 19,19 37,28" fill="#ffb3c6"/>
    <polygon points="79,40 81,19 63,28" fill="#ffb3c6"/>
    <circle cx="50" cy="54" r="32" fill="${c.color}"/>
    <circle cx="37" cy="49" r="5.5" fill="#1f1f1f"/>
    <circle cx="63" cy="49" r="5.5" fill="#1f1f1f"/>
    <circle cx="35.5" cy="47" r="2" fill="#fff"/>
    <circle cx="61.5" cy="47" r="2" fill="#fff"/>
    <ellipse cx="28" cy="58" rx="5" ry="3" fill="#ff758f" opacity="0.6"/>
    <ellipse cx="72" cy="58" rx="5" ry="3" fill="#ff758f" opacity="0.6"/>
    <polygon points="46,56 54,56 50,61" fill="#ff4d6d"/>
    <path d="M43 65 Q50 70 50 61 Q50 70 57 65" fill="none" stroke="#1f1f1f" stroke-width="2.5" stroke-linecap="round"/>
    ${extra}
  </svg>;
}

let board = [], score = 0, best = Number(localStorage.getItem('cat2048_best') || 0);
let history = [], undoLeft = 3, sweepLeft = 1, shuffleLeft = 1;
let unlocked = JSON.parse(localStorage.getItem('cat2048_dex') || '[2]');
let soundOn = true;
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playMeow(val) {
  if (!soundOn) return;
  try {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    const lvl = Math.log2(val || 2);
const baseFreq = 320 + lvl * 55;
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.35, audioCtx.currentTime + 0.09);
    osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.9, audioCtx.currentTime + 0.18);
    gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.19);
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.start(); osc.stop(audioCtx.currentTime + 0.2);
  } catch(e) {}
}

function haptic(type='light') {
  if (tg && tg.HapticFeedback) tg.HapticFeedback.impactOccurred(type);
}

function initGame() {
  board = Array(4).fill(0).map(() => Array(4).fill(0));
  score = 0; history = []; undoLeft = 3; sweepLeft = 1; shuffleLeft = 1;
  document.getElementById('overlay').style.display = 'none';
  addRandomTile(); addRandomTile();
  render();
}

function addRandomTile() {
  const empty = [];
  for (let r=0; r<4; r++) for (let c=0; c<4; c++) if (board[r][c] === 0) empty.push([r,c]);
  if (empty.length > 0) {
    const [r, c] = empty[Math.floor(Math.random() * empty.length)];
    board[r][c] = Math.random() < 0.88 ? 2 : 4;
  }
}

function render(mergedCoords = []) {
  document.getElementById('score').innerText = score;
  if (score > best) { best = score; localStorage.setItem('cat2048_best', best); }
  document.getElementById('best').innerText = best;

  document.getElementById('undo-cnt').innerText = undoLeft;
  document.getElementById('sweep-cnt').innerText = sweepLeft;
  document.getElementById('shuffle-cnt').innerText = shuffleLeft;
  document.getElementById('btn-undo').classList.toggle('disabled', undoLeft <= 0 || history.length === 0);
  document.getElementById('btn-sweep').classList.toggle('disabled', sweepLeft <= 0);
  document.getElementById('btn-shuffle').classList.toggle('disabled', shuffleLeft <= 0);

  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  for (let r=0; r<4; r++) {
    for (let c=0; c<4; c++) {
      const val = board[r][c];
      const cell = document.createElement('div');
      cell.className = 'cell';
      if (val > 0) {
        const cat = CATS[val] || CATS[2048];
        cell.style.background = cat.bg;
        const isMerged = mergedCoords.some(([mr, mc]) => mr === r && mc === c);
        cell.classList.add(isMerged ? 'merge' : 'pop');
        cell.innerHTML = <span class="cat-lvl">${val}</span>${getCatSVG(val)}<span class="cat-name">${cat.name}</span>;
        if (!unlocked.includes(val)) {
          unlocked.push(val);
          localStorage.setItem('cat2048_dex', JSON.stringify(unlocked));
        }
      }
      grid.appendChild(cell);
    }
  }
  renderDex();
}

function renderDex() {
  const dexList = document.getElementById('dex-list');
  dexList.innerHTML = '';
  const keys = Object.keys(CATS).map(Number);
  keys.forEach(k => {
    const item = document.createElement('div');
    item.className = 'dex-item' + (unlocked.includes(k) ? ' unlocked' : '');
    item.innerHTML = getCatSVG(k);
    dexList.appendChild(item);
  });
  document.getElementById('dex-progress').innerText = ${unlocked.length} / ${keys.length};
}

function move(dir) {
  const prevBoard = board.map(r => [...r]);
  const prevScore = score;
  let moved = false;
  let maxMerged = 0;
  let mergedCoords = [];

  const slideRow = (row, rIdx, isRev) => {
    let arr = row.filter(v => v !== 0);
    let res = [];
    for (let i=0; i<arr.length; i++) {
      if (i < arr.length - 1 && arr[i] === arr[i+1]) {
        const mergedVal = arr[i] * 2;
        res.push(mergedVal);
        score += mergedVal;
        if (mergedVal > maxMerged) maxMerged = mergedVal;
        mergedCoords.push([rIdx, isRev ? 3 - (res.length - 1) : res.length - 1]);
        i++;
      } else {
        res.push(arr[i]);
      }
    }
    while (res.length < 4) res.push(0);
    return res;
  };
if (dir === 'right' || dir === 'left') {
    for (let r=0; r<4; r++) {
      let row = [...board[r]];
      // In RTL layout, column 0 is on the RIGHT and column 3 is on the LEFT!
      const goZeroSide = (dir === 'right');
      if (!goZeroSide) row.reverse();
      let newRow = slideRow(row, r, !goZeroSide);
      if (!goZeroSide) newRow.reverse();
      if (newRow.join(',') !== board[r].join(',')) moved = true;
      board[r] = newRow;
    }
  } else {
    for (let c=0; c<4; c++) {
      let col = [board[0][c], board[1][c], board[2][c], board[3][c]];
      const goTop = (dir === 'up');
      if (!goTop) col.reverse();
      let newCol = slideRow(col, c, !goTop);
      if (!goTop) newCol.reverse();
      for (let r=0; r<4; r++) {
        if (board[r][c] !== newCol[r]) moved = true;
        board[r][c] = newCol[r];
      }
    }
  }

  if (moved) {
    history.push({ board: prevBoard, score: prevScore });
    if (history.length > 5) history.shift();
    addRandomTile();
    if (maxMerged > 0) {
      playMeow(maxMerged);
      haptic(maxMerged >= 64 ? 'heavy' : 'medium');
    } else {
      haptic('light');
    }
    render(mergedCoords);
    if (isGameOver()) {
      document.getElementById('ov-desc').innerText = امتیاز نهایی شما: ${score};
      document.getElementById('overlay').style.display = 'flex';
    }
  }
}

function isGameOver() {
  for (let r=0; r<4; r++) {
    for (let c=0; c<4; c++) {
      if (board[r][c] === 0) return false;
      if (c < 3 && board[r][c] === board[r][c+1]) return false;
      if (r < 3 && board[r][c] === board[r+1][c]) return false;
    }
  }
  return true;
}

function useUndo() {
  if (undoLeft > 0 && history.length > 0) {
    const last = history.pop();
    board = last.board; score = last.score; undoLeft--;
    haptic('medium'); render();
  }
}

function useSweep() {
  if (sweepLeft <= 0) return;
  let count = 0;
  for (let r=0; r<4; r++) for (let c=0; c<4; c++) if (board[r][c] > 0) count++;
  if (count <= 2) return;
  let removed = false;
  for (let r=0; r<4; r++) for (let c=0; c<4; c++) {
    if (board[r][c] === 2) { board[r][c] = 0; removed = true; }
  }
  if (removed) { sweepLeft--; haptic('heavy'); render(); }
}

function useShuffle() {
  if (shuffleLeft <= 0) return;
  const vals = [];
  for (let r=0; r<4; r++) for (let c=0; c<4; c++) if (board[r][c] > 0) vals.push(board[r][c]);
  vals.sort(() => Math.random() - 0.5);
  board = Array(4).fill(0).map(() => Array(4).fill(0));
  let idx = 0;
  for (let r=0; r<4; r++) for (let c=0; c<4; c++) if (idx < vals.length) board[r][c] = vals[idx++];
  shuffleLeft--; haptic('heavy'); render();
}

function toggleSound() {
  soundOn = !soundOn;
  document.getElementById('btn-sound').innerText = soundOn ? ':loud_sound:' : ':mute:';
}

// کنترل لمسی (کشیدن انگشت روی صفحه)
let sx = 0, sy = 0;
const bc = document.getElementById('board-container');
bc.addEventListener('touchstart', e => { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, {passive: false});
bc.addEventListener('touchmove', e => { e.preventDefault(); }, {passive: false});
bc.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - sx;
  const dy = e.changedTouches[0].clientY - sy;
  if (Math.max(Math.abs(dx), Math.abs(dy)) > 25) {
    if (Math.abs(dx) > Math.abs(dy)) move(dx > 0 ? 'right' : 'left');
    else move(dy > 0 ? 'down' : 'up');
  }
});

// کنترل با کیبورد
window.addEventListener('keydown', e => {
  if (e.key === 'ArrowUp') move('up');
  if (e.key === 'ArrowDown') move('down');
  if (e.key === 'ArrowRight') move('right');
  if (e.key === 'ArrowLeft') move('left');
});

initGame();
</script>
</body>
</html>"""

@app.route('/', methods=['GET'])
def home():
    return "Telegram Bot & Cat 2048 Mini App are running!"

@app.route('/game', methods=['GET'])
def game_page():
    return Response(GAME_HTML, mimetype='text/html')
@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "").strip()
            
            # اگر کاربر دستور شروع یا بازی را فرستاد، دکمه مینی‌اپ بازی را نشان بده
            if user_text in ["/start", "/game", "بازی", "گربه"]:
                welcome_msg = (
                    ":cat: به بازی گربه‌های ۲۰۴۸ خوش آمدید! :video_game:\n\n"
                    "گربه‌های هم‌شکل رو به هم بزنید تا گربه‌های جدید با رنگ‌ها و قدرت‌های باحال‌تر آزاد بشن!\n\n"
                    ":point_down: برای شروع بازی روی دکمه شیشه‌ای زیر کلیک کنید (یا هر سوالی دارید بپرسید تا هوش مصنوعی جواب بده):"
                )
                reply_markup = {
                    "inline_keyboard": [[
                        {
                            "text": ":feet: شروع بازی گربه‌های ۲۰۴۸ :video_game:",
                            "web_app": {"url": f"{APP_URL}/game"}
                        }
                    ]]
                }
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": welcome_msg,
                        "parse_mode": "Markdown",
                        "reply_markup": reply_markup
                    }
                )
                return "OK", 200

            # در غیر این صورت، پیام را به هوش مصنوعی جمنای بفرست
            if user_text:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                payload = {"contents": [{"parts": [{"text": user_text}]}]}
                
                res = requests.post(gemini_url, json=payload)
                if res.status_code == 200:
                    reply_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    reply_text = f"خطای جمنای: {res.text}"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": reply_text}
                )
    except Exception as e:
        print(f"Error: {e}")
        
    return "OK", 200
