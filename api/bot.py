from flask import Flask, request, Response
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
# کلید واقعی جمنای خود را در خط زیر جایگزین کنید
GEMINI_API_KEY = "AQ.Ab8RN6L-MseJmNRPCojeruDlt7qi5S6cHoqVM_EGO8LGmmyrng"
APP_URL = "https://malibot2.vercel.app"

GAME_HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Meow 2048 - 20 Levels</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@500;700;900&display=swap" rel="stylesheet">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  * {
    box-sizing: border-box;
    user-select: none;
    -webkit-user-select: none;
    margin: 0;
    padding: 0;
    font-family: 'Vazirmatn', Tahoma, sans-serif;
  }
  body {
    background: radial-gradient(circle at top, #3b1d5e 0%, #170b29 70%, #0d061a 100%);
    color: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 10px 12px;
    overflow-x: hidden;
    touch-action: none;
  }
  .top-bar {
    width: 100%;
    max-width: 360px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 8px 12px;
    margin-bottom: 8px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .brand-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #ff6b9d, #ff8e53);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 10px rgba(255, 107, 157, 0.5);
  }
  .brand-text h1 {
    font-size: 16px;
    font-weight: 900;
    color: #fff;
    line-height: 1.2;
  }
  .brand-text p {
    font-size: 10px;
    color: #d8b4fe;
    font-weight: 500;
  }
  .scores {
    display: flex;
    gap: 6px;
  }
  .score-box {
    background: rgba(15, 7, 30, 0.65);
    border: 1px solid rgba(255, 209, 102, 0.35);
    border-radius: 12px;
    padding: 4px 10px;
    text-align: center;
    min-width: 66px;
  }
  .score-box span {
    font-size: 9px;
    color: #ffd166;
    display: block;
    font-weight: 700;
  }
  .score-box strong {
    font-size: 14px;
    color: #fff;
    font-weight: 900;
  }

  .quest-bar {
    width: 100%;
    max-width: 360px;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 6px 10px;
    margin-bottom: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  .quest-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    font-weight: 700;
    color: #f3e8ff;
  }
  .quest-info b {
    color: #fde047;
  }
  .progress-track {
    width: 100%;
    height: 7px;
    background: rgba(0, 0, 0, 0.45);
    border-radius: 10px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #f43f5e, #fbbf24, #34d399);
    border-radius: 10px;
    width: 5%;
    transition: width 0.3s ease;
  }

  .power-bar {
    width: 100%;
    max-width: 360px;
    display: grid;
    grid-template-columns: repeat(4, 1fr) 40px 40px;
    gap: 5px;
    margin-bottom: 8px;
  }
  .p-btn {
    background: linear-gradient(180deg, #4c2882 0%, #311759 100%);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-bottom: 3px solid #1c0b38;
    color: #fff;
    border-radius: 12px;
    padding: 6px 2px;
    font-size: 10px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    position: relative;
    transition: transform 0.1s;
  }
  .p-btn:active {
    transform: translateY(2px);
    border-bottom-width: 1px;
  }
  .p-btn.disabled {
    opacity: 0.4;
    pointer-events: none;
  }
  .p-btn svg {
    width: 16px;
    height: 16px;
    fill: #ffd166;
  }
  .p-badge {
    position: absolute;
    top: -4px;
    left: -4px;
    background: #ff3b6b;
    color: #fff;
    font-size: 9px;
    font-weight: 900;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1.5px solid #fff;
  }

  #board-wrap {
    position: relative;
    width: 340px;
    height: 340px;
    max-width: 92vw;
    max-height: 92vw;
    background: #140826;
    border-radius: 20px;
    padding: 8px;
    border: 2px solid rgba(255, 255, 255, 0.16);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), inset 0 2px 10px rgba(255, 255, 255, 0.05);
    touch-action: none;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 8px;
    width: 100%;
    height: 100%;
  }
  .cell {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  .cell.filled {
    border: 1.5px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35), inset 0 2px 5px rgba(255, 255, 255, 0.35);
  }
  .cell.pop {
    animation: popIn 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .cell.merge {
    animation: mergePulse 0.32s ease;
  }
  @keyframes popIn {
    0% { transform: scale(0.3); opacity: 0.4; }
    100% { transform: scale(1); opacity: 1; }
  }
  @keyframes mergePulse {
    0% { transform: scale(1); }
    45% { transform: scale(1.2); filter: brightness(1.35); }
    100% { transform: scale(1); }
  }

  .lvl-tag {
    position: absolute;
    top: 3px;
    right: 4px;
    font-size: 8px;
    font-weight: 900;
    background: rgba(0, 0, 0, 0.55);
    color: #fff;
    padding: 1px 4px;
    border-radius: 6px;
    line-height: 1.2;
    z-index: 2;
  }
  .cat-art {
    width: 62%;
    height: 62%;
    margin-top: 4px;
    filter: drop-shadow(0 3px 4px rgba(0, 0, 0, 0.4));
  }
  .cat-label {
    font-size: 9px;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
    margin-top: -1px;
    white-space: nowrap;
  }

  .dex-panel {
    width: 100%;
    max-width: 360px;
    margin-top: 8px;
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 6px 10px;
  }
  .dex-head {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    font-weight: 700;
    color: #ffd166;
    margin-bottom: 5px;
  }
  .dex-scroll {
    display: flex;
    gap: 5px;
    overflow-x: auto;
    padding-bottom: 3px;
    scrollbar-width: none;
  }
  .dex-scroll::-webkit-scrollbar { display: none; }
  .dex-slot {
    min-width: 34px;
    height: 38px;
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0.3;
    position: relative;
  }
  .dex-slot.open {
    opacity: 1;
    border-color: #ffd166;
    background: rgba(255, 255, 255, 0.12);
  }
  .dex-slot svg { width: 22px; height: 22px; }
  .dex-slot span { font-size: 7px; font-weight: 700; color: #fff; }

  .controls {
    width: 100%;
    max-width: 360px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-top: 8px;
  }
  .ctrl-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-bottom: 3px solid rgba(0, 0, 0, 0.5);
    border-radius: 12px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .ctrl-btn:active { transform: translateY(2px); }
  .ctrl-btn svg { width: 20px; height: 20px; fill: #fff; }

  #modal {
    position: absolute;
    inset: 0;
    background: rgba(15, 6, 30, 0.92);
    border-radius: 18px;
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 20;
    padding: 20px;
    text-align: center;
  }
  #modal h2 { font-size: 22px; color: #ffd166; margin-bottom: 6px; font-weight: 900; }
  #modal p { font-size: 13px; color: #e9d5ff; margin-bottom: 16px; }
  .play-btn {
    background: linear-gradient(90deg, #ec4899, #f97316);
    border: none;
    color: #fff;
    padding: 10px 26px;
    border-radius: 14px;
    font-weight: 900;
    font-size: 14px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(236, 72, 153, 0.5);
  }
</style>
</head>
<body>

<div class="top-bar">
  <div class="brand">
    <div class="brand-icon">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#fff">
        <circle cx="7" cy="6" r="2.2"/><circle cx="12" cy="4.5" r="2.2"/><circle cx="17" cy="6" r="2.2"/><circle cx="19.5" cy="10.5" r="2"/>
        <path d="M12 9c-3.8 0-6.5 2.6-6.5 5.8 0 2.3 1.8 4.2 4.2 4.2.9 0 1.6-.3 2.3-.3s1.4.3 2.3.3c2.4 0 4.2-1.9 4.2-4.2C18.5 11.6 15.8 9 12 9z"/>
      </svg>
    </div>
    <div class="brand-text">
      <h1>قلمرو گربه‌ها</h1>
      <p id="sub-title">۲۰ مرحله تکامل جادویی</p>
    </div>
  </div>
  <div class="scores">
    <div class="score-box"><span>امتیاز</span><strong id="score-val">0</strong></div>
    <div class="score-box"><span>رکورد</span><strong id="best-val">0</strong></div>
  </div>
</div>

<div class="quest-bar">
  <div class="quest-info">
    <span id="highest-txt">بالاترین گربه: سطح ۱ (ملوس)</span>
    <b id="quest-pct">5% (1/20)</b>
  </div>
  <div class="progress-track">
    <div class="progress-fill" id="prog-fill"></div>
  </div>
</div>

<div class="power-bar">
  <button class="p-btn" id="btn-undo" onclick="useUndo()">
    <span class="p-badge" id="cnt-undo">3</span>
    <svg viewBox="0 0 24 24"><path d="M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z"/></svg>
    <span>عقبگرد</span>
  </button>
  <button class="p-btn" id="btn-sweep" onclick="useSweep()">
    <span class="p-badge" id="cnt-sweep">2</span>
    <svg viewBox="0 0 24 24"><path d="M19.36 2.72L20.78 4.14L15.06 9.85C16.13 11.39 16.28 13.24 15.38 14.44L9.06 8.12C10.26 7.22 12.11 7.37 13.65 8.44L19.36 2.72M5.93 17.57C3.92 15.56 2.69 13.16 2.35 10.92L7.23 8.83L14.67 16.27L12.58 21.15C10.34 20.81 7.94 19.58 5.93 17.57Z"/></svg>
    <span>پاکسازی</span>
  </button>
  <button class="p-btn" id="btn-wand" onclick="useWand()">
    <span class="p-badge" id="cnt-wand">2</span>
    <svg viewBox="0 0 24 24"><path d="M7.5 5.6L10 7 8.6 4.5 10 2 7.5 3.4 5 2l1.4 2.5L5 7zm12 9.8L17 14l1.4 2.5L17 19l2.5-1.4L22 19l-1.4-2.5L22 14zM22 2l-2.5 1.4L17 2l1.4 2.5L17 7l2.5-1.4L22 7l-1.4-2.5zm-7.63 5.29a1 1 0 00-1.41 0L1.29 18.96a1 1 0 000 1.41l2.34 2.34c.39.39 1.02.39 1.41 0L16.7 11.05a1 1 0 000-1.41l-2.33-2.35z"/></svg>
    <span>ارتقا +۱</span>
  </button>
  <button class="p-btn" id="btn-shuffle" onclick="useShuffle()">
    <span class="p-badge" id="cnt-shuffle">2</span>
    <svg viewBox="0 0 24 24"><path d="M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z"/></svg>
    <span>بُر زدن</span>
  </button>
  <button class="p-btn" onclick="toggleSound()">
    <svg id="snd-icon" viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/></svg>
    <span>صدا</span>
  </button>
  <button class="p-btn" onclick="initGame()">
    <svg viewBox="0 0 24 24"><path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0112 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
    <span>جدید</span>
  </button>
</div>

<div id="board-wrap">
  <div class="grid" id="grid"></div>
  <div id="modal">
    <h2 id="mod-title">پایان بازی!</h2>
    <p id="mod-desc">امتیاز شما: 0</p>
    <button class="play-btn" onclick="initGame()">شروع دوباره</button>
  </div>
</div>

<div class="dex-panel">
  <div class="dex-head">
    <span>کلکسیون ۲۰ گربه افسانه‌ای</span>
    <span id="dex-count">1 / 20</span>
  </div>
  <div class="dex-scroll" id="dex-list"></div>
</div>

<div class="controls">
  <button class="ctrl-btn" onclick="move('right')" title="راست">
    <svg viewBox="0 0 24 24"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>
  </button>
  <button class="ctrl-btn" onclick="move('up')" title="بالا">
    <svg viewBox="0 0 24 24"><path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"/></svg>
  </button>
  <button class="ctrl-btn" onclick="move('down')" title="پایین">
    <svg viewBox="0 0 24 24"><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"/></svg>
  </button>
  <button class="ctrl-btn" onclick="move('left')" title="چپ">
    <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
  </button>
</div>

<script>
function safeGet(k, defVal) {
  try {
    var v = window.localStorage.getItem(k);
    return v ? v : defVal;
  } catch (e) { return defVal; }
}
function safeSet(k, val) {
  try { window.localStorage.setItem(k, val); } catch (e) {}
}

try {
  if (window.Telegram && window.Telegram.WebApp) {
    var tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();
    if (tg.disableVerticalSwipes) tg.disableVerticalSwipes();
  }
} catch (e) {}

var CAT_DATA = {
  1:  { name: "ملوس",     bg: "linear-gradient(145deg, #ff758f, #ff4d6d)", fur: "#ffe5ec", ear: "#ff4d6d", acc: "none" },
  2:  { name: "حنایی",    bg: "linear-gradient(145deg, #fb8500, #ffb703)", fur: "#ffd166", ear: "#d62828", acc: "stripes" },
  3:  { name: "اشرافی",   bg: "linear-gradient(145deg, #0096c7, #48cae4)", fur: "#caf0f8", ear: "#023e8a", acc: "bow" },
  4:  { name: "عینکی",    bg: "linear-gradient(145deg, #10b981, #059669)", fur: "#a7f3d0", ear: "#065f46", acc: "nerd" },
  5:  { name: "نینجا",    bg: "linear-gradient(145deg, #374151, #111827)", fur: "#9ca3af", ear: "#ef4444", acc: "ninja" },
  6:  { name: "جادوگر",   bg: "linear-gradient(145deg, #9333ea, #6b21a8)", fur: "#e9d5ff", ear: "#581c87", acc: "hat" },
  7:  { name: "خفن",      bg: "linear-gradient(145deg, #eab308, #ca8a04)", fur: "#fef08a", ear: "#854d0e", acc: "sunglass" },
  8:  { name: "دزددریایی",bg: "linear-gradient(145deg, #0f766e, #115e59)", fur: "#99f6e4", ear: "#134e4a", acc: "pirate" },
  9:  { name: "سایبر",    bg: "linear-gradient(145deg, #2563eb, #1d4ed8)", fur: "#bfdbfe", ear: "#00f5d4", acc: "cyber" },
  10: { name: "سرآشپز",   bg: "linear-gradient(145deg, #f43f5e, #e11d48)", fur: "#ffe4e6", ear: "#9f1239", acc: "chef" },
  11: { name: "سامورایی", bg: "linear-gradient(145deg, #dc2626, #7f1d1d)", fur: "#fca5a5", ear: "#fbbf24", acc: "samurai" },
  12: { name: "آتشین",    bg: "linear-gradient(145deg, #ea580c, #9a3412)", fur: "#fed7aa", ear: "#ff0055", acc: "fire" },
  13: { name: "یخی",      bg: "linear-gradient(145deg, #0284c7, #0369a1)", fur: "#e0f2fe", ear: "#38bdf8", acc: "ice" },
  14: { name: "فضانورد",  bg: "linear-gradient(145deg, #4f46e5, #312e81)", fur: "#c7d2fe", ear: "#818cf8", acc: "astro" },
  15: { name: "خون‌آشام", bg: "linear-gradient(145deg, #831843, #4c0519)", fur: "#fbcfe8", ear: "#db2777", acc: "vamp" },
  16: { name: "فرشته",    bg: "linear-gradient(145deg, #f59e0b, #b45309)", fur: "#fef3c7", ear: "#fbbf24", acc: "halo" },
  17: { name: "رعدوبرق",  bg: "linear-gradient(145deg, #7c3aed, #4c1d95)", fur: "#fde047", ear: "#a855f7", acc: "bolt" },
  18: { name: "کهکشانی",  bg: "linear-gradient(145deg, #3b0764, #1e1b4b)", fur: "#d8b4fe", ear: "#f472b6", acc: "galaxy" },
  19: { name: "سلطان",    bg: "linear-gradient(145deg, #d97706, #78350f)", fur: "#fde68a", ear: "#ef4444", acc: "crown" },
  20: { name: "خدای گربه",bg: "linear-gradient(135deg, #ff007f, #7928ca, #00d4ff)", fur: "#ffffff", ear: "#ffd700", acc: "god" }
};

function buildCatSVG(lvl) {
  var c = CAT_DATA[lvl] || CAT_DATA[20];
  var acc = "";
  if (c.acc === "stripes") acc = '<path d="M40 27 H60 M43 32 H57" stroke="#d97706" stroke-width="3.5" stroke-linecap="round"/>';
  if (c.acc === "bow") acc = '<polygon points="36,77 50,83 36,89" fill="#ef4444"/><polygon points="64,77 50,83 64,89" fill="#ef4444"/><circle cx="50" cy="83" r="4.5" fill="#fbbf24"/>';
  if (c.acc === "nerd") acc = '<circle cx="37" cy="49" r="10" fill="none" stroke="#111" stroke-width="3"/><circle cx="63" cy="49" r="10" fill="none" stroke="#111" stroke-width="3"/><line x1="47" y1="49" x2="53" y2="49" stroke="#111" stroke-width="3"/>';
  if (c.acc === "ninja") acc = '<rect x="19" y="29" width="62" height="10" rx="4" fill="#ef4444"/><circle cx="50" cy="34" r="3.5" fill="#fff"/>';
  if (c.acc === "hat") acc = '<polygon points="24,28 50,2 76,28" fill="#4c1d95"/><ellipse cx="50" cy="28" rx="30" ry="5" fill="#a855f7"/>';
  if (c.acc === "sunglass") acc = '<rect x="23" y="42" width="23" height="13" rx="3" fill="#111"/><rect x="54" y="42" width="23" height="13" rx="3" fill="#111"/><line x1="46" y1="46" x2="54" y2="46" stroke="#111" stroke-width="3"/>';
  if (c.acc === "pirate") acc = '<circle cx="37" cy="49" r="8" fill="#111"/><line x1="20" y1="38" x2="78" y2="55" stroke="#111" stroke-width="3"/>';
  if (c.acc === "cyber") acc = '<rect x="22" y="43" width="56" height="11" rx="5" fill="#00f5d4" stroke="#fff" stroke-width="1.5"/>';
  if (c.acc === "chef") acc = '<ellipse cx="50" cy="16" rx="22" ry="11" fill="#fff"/><rect x="33" y="20" width="34" height="9" rx="2" fill="#f3f4f6"/>';
  if (c.acc === "samurai") acc = '<polygon points="50,4 35,28 65,28" fill="#fbbf24"/><circle cx="50" cy="22" r="5" fill="#dc2626"/>';
  if (c.acc === "fire") acc = '<path d="M32 22 L40 6 L50 18 L60 6 L68 22" fill="#facc15" stroke="#ef4444" stroke-width="2"/>';
  if (c.acc === "ice") acc = '<polygon points="50,4 42,24 58,24" fill="#38bdf8"/><polygon points="34,12 36,26 46,24" fill="#7dd3fc"/><polygon points="66,12 64,26 54,24" fill="#7dd3fc"/>';
  if (c.acc === "astro") acc = '<circle cx="50" cy="54" r="37" fill="none" stroke="#fff" stroke-width="3.5" opacity="0.8"/>';
  if (c.acc === "vamp") acc = '<polygon points="43,66 46,74 49,66" fill="#fff"/><polygon points="51,66 54,74 57,66" fill="#fff"/>';
  if (c.acc === "halo") acc = '<ellipse cx="50" cy="10" rx="22" ry="5" fill="none" stroke="#fde047" stroke-width="4"/>';
  if (c.acc === "bolt") acc = '<polygon points="53,6 42,22 51,22 46,36 60,18 50,18" fill="#fde047"/>';
  if (c.acc === "galaxy") acc = '<circle cx="50" cy="31" r="5" fill="#fde047"/><circle cx="34" cy="35" r="2.5" fill="#f472b6"/><circle cx="66" cy="35" r="2.5" fill="#38bdf8"/>';
  if (c.acc === "crown" || c.acc === "god") acc = '<polygon points="28,25 33,7 50,18 67,7 72,25" fill="#ffd700" stroke="#b45309" stroke-width="2"/><circle cx="50" cy="19" r="3.5" fill="#ef4444"/>';

  return '<svg class="cat-art" viewBox="0 0 100 100">' +
    '<polygon points="18,46 13,12 43,26" fill="' + c.fur + '" stroke="rgba(0,0,0,0.25)" stroke-width="2"/>' +
    '<polygon points="82,46 87,12 57,26" fill="' + c.fur + '" stroke="rgba(0,0,0,0.25)" stroke-width="2"/>' +
    '<polygon points="22,40 19,19 37,28" fill="' + c.ear + '"/>' +
    '<polygon points="78,40 81,19 63,28" fill="' + c.ear + '"/>' +
    '<circle cx="50" cy="55" r="32" fill="' + c.fur + '" stroke="rgba(0,0,0,0.2)" stroke-width="2"/>' +
    '<circle cx="37" cy="49" r="5.5" fill="#18181b"/>' +
    '<circle cx="63" cy="49" r="5.5" fill="#18181b"/>' +
    '<circle cx="35" cy="47" r="2" fill="#fff"/>' +
    '<circle cx="61" cy="47" r="2" fill="#fff"/>' +
    '<ellipse cx="27" cy="58" rx="5.5" ry="3.2" fill="#fb7185" opacity="0.65"/>' +
    '<ellipse cx="73" cy="58" rx="5.5" ry="3.2" fill="#fb7185" opacity="0.65"/>' +
    '<polygon points="46,56 54,56 50,61" fill="#f43f5e"/>' +
    '<path d="M42 65 Q50 71 50 61 Q50 71 58 65" fill="none" stroke="#18181b" stroke-width="2.8" stroke-linecap="round"/>' +
    acc + '</svg>';
}

var board = [];
var score = 0;
var best = parseInt(safeGet('meow20_best', '0'), 10) || 0;
var unlocked = [1];
try {
  var savedDex = JSON.parse(safeGet('meow20_dex', '[1]'));
  if (Array.isArray(savedDex) && savedDex.length > 0) unlocked = savedDex;
} catch (e) { unlocked = [1]; }

var historyList = [];
var undoLeft = 3, sweepLeft = 2, wandLeft = 2, shuffleLeft = 2;
var nextBonusScore = 500;
var soundOn = true;
var audioCtx = null;

function playTone(lvl) {
  if (!soundOn) return;
  try {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    if (!audioCtx) audioCtx = new AC();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    var freq = 300 + (lvl * 42);
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq * 1.3, audioCtx.currentTime + 0.08);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.95, audioCtx.currentTime + 0.16);
    gain.gain.setValueAtTime(0.14, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.17);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.18);
  } catch (e) {}
}

function vibrate(style) {
  try {
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.HapticFeedback) {
      window.Telegram.WebApp.HapticFeedback.impactOccurred(style || 'light');
    }
  } catch (e) {}
}

function getHighestOnBoard() {
  var m = 1;
  for (var r = 0; r < 4; r++) {
    for (var c = 0; c < 4; c++) {
      if (board[r][c] > m) m = board[r][c];
    }
  }
  return m;
}

function addRandomCat() {
  var empty = [];
  for (var r = 0; r < 4; r++) {
    for (var c = 0; c < 4; c++) {
      if (board[r][c] === 0) empty.push([r, c]);
    }
  }
  if (empty.length === 0) return;
  var pick = empty[Math.floor(Math.random() * empty.length)];
  var high = getHighestOnBoard();
  var base = 1;
  if (high >= 10 && Math.random() < 0.25) base = 3;
  else if (high >= 6 && Math.random() < 0.35) base = 2;
  else base = Math.random() < 0.85 ? 1 : 2;
  board[pick[0]][pick[1]] = base;
}

function initGame() {
  board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ];
  score = 0;
  historyList = [];
  undoLeft = 3;
  sweepLeft = 2;
  wandLeft = 2;
  shuffleLeft = 2;
  nextBonusScore = 500;
  document.getElementById('modal').style.display = 'none';
  addRandomCat();
  addRandomCat();
  render([]);
}

function render(mergedList) {
  document.getElementById('score-val').innerText = score;
  if (score > best) {
    best = score;
    safeSet('meow20_best', String(best));
  }
  document.getElementById('best-val').innerText = best;

  if (score >= nextBonusScore) {
    wandLeft++;
    nextBonusScore += 600;
  }

  document.getElementById('cnt-undo').innerText = undoLeft;
  document.getElementById('cnt-sweep').innerText = sweepLeft;
  document.getElementById('cnt-wand').innerText = wandLeft;
  document.getElementById('cnt-shuffle').innerText = shuffleLeft;

  document.getElementById('btn-undo').className = 'p-btn' + (undoLeft <= 0 || historyList.length === 0 ? ' disabled' : '');
  document.getElementById('btn-sweep').className = 'p-btn' + (sweepLeft <= 0 ? ' disabled' : '');
  document.getElementById('btn-wand').className = 'p-btn' + (wandLeft <= 0 ? ' disabled' : '');
  document.getElementById('btn-shuffle').className = 'p-btn' + (shuffleLeft <= 0 ? ' disabled' : '');

  var grid = document.getElementById('grid');
  grid.innerHTML = '';
  var highest = 1;

  for (var r = 0; r < 4; r++) {
    for (var c = 0; c < 4; c++) {
      var lvl = board[r][c];
      if (lvl > highest) highest = lvl;
      var cell = document.createElement('div');
      if (lvl > 0) {
        if (lvl > 20) lvl = 20;
        var info = CAT_DATA[lvl] || CAT_DATA[20];
        var isM = false;
        for (var k = 0; k < mergedList.length; k++) {
          if (mergedList[k][0] === r && mergedList[k][1] === c) isM = true;
        }
        cell.className = 'cell filled ' + (isM ? 'merge' : 'pop');
        cell.style.background = info.bg;
        cell.innerHTML = '<span class="lvl-tag">Lv.' + lvl + '</span>' + buildCatSVG(lvl) + '<span class="cat-label">' + info.name + '</span>';
        if (unlocked.indexOf(lvl) === -1) {
          unlocked.push(lvl);
          safeSet('meow20_dex', JSON.stringify(unlocked));
        }
      } else {
        cell.className = 'cell';
      }
      grid.appendChild(cell);
    }
  }

  var maxUnlocked = Math.max.apply(null, unlocked);
  if (highest > maxUnlocked) maxUnlocked = highest;
  var hInfo = CAT_DATA[highest] || CAT_DATA[1];
  document.getElementById('highest-txt').innerText = 'بالاترین گربه فعلی: سطح ' + highest + ' (' + hInfo.name + ')';
  var pct = Math.min(100, Math.round((maxUnlocked / 20) * 100));
  document.getElementById('quest-pct').innerText = pct + '% (' + maxUnlocked + '/20)';
  document.getElementById('prog-fill').style.width = pct + '%';

  renderDex();
}

function renderDex() {
  var list = document.getElementById('dex-list');
  list.innerHTML = '';
  for (var i = 1; i <= 20; i++) {
    var slot = document.createElement('div');
    var isOpen = unlocked.indexOf(i) !== -1;
    slot.className = 'dex-slot' + (isOpen ? ' open' : '');
    slot.innerHTML = buildCatSVG(i) + '<span>Lv.' + i + '</span>';
    list.appendChild(slot);
  }
  document.getElementById('dex-count').innerText = unlocked.length + ' / 20';
}

function move(dir) {
  var prevB = board.map(function(r) { return r.slice(); });
  var prevS = score;
  var moved = false;
  var maxM = 0;
  var mergedCoords = [];

  function slideLine(arr, fixedIdx, isRev, isCol) {
    var filtered = arr.filter(function(v) { return v !== 0; });
    var res = [];
    for (var i = 0; i < filtered.length; i++) {
      if (i < filtered.length - 1 && filtered[i] === filtered[i + 1] && filtered[i] < 20) {
        var nextLvl = filtered[i] + 1;
        res.push(nextLvl);
        score += nextLvl * 15;
        if (nextLvl > maxM) maxM = nextLvl;
        var pos = isRev ? 3 - (res.length - 1) : (res.length - 1);
        if (isCol) mergedCoords.push([pos, fixedIdx]);
        else mergedCoords.push([fixedIdx, pos]);
        i++;
      } else {
        res.push(filtered[i]);
      }
    }
    while (res.length < 4) res.push(0);
    return res;
  }

  if (dir === 'right' || dir === 'left') {
    for (var r = 0; r < 4; r++) {
      var row = board[r].slice();
      var toZero = (dir === 'right');
      if (!toZero) row.reverse();
      var nRow = slideLine(row, r, !toZero, false);
      if (!toZero) nRow.reverse();
      if (nRow.join(',') !== board[r].join(',')) moved = true;
      board[r] = nRow;
    }
  } else {
    for (var c = 0; c < 4; c++) {
      var col = [board[0][c], board[1][c], board[2][c], board[3][c]];
      var toTop = (dir === 'up');
      if (!toTop) col.reverse();
      var nCol = slideLine(col, c, !toTop, true);
      if (!toTop) nCol.reverse();
      for (var r2 = 0; r2 < 4; r2++) {
        if (board[r2][c] !== nCol[r2]) moved = true;
        board[r2][c] = nCol[r2];
      }
    }
  }

  if (moved) {
    historyList.push({ b: prevB, s: prevS });
    if (historyList.length > 5) historyList.shift();
    addRandomCat();
    if (maxM > 0) {
      playTone(maxM);
      vibrate(maxM >= 6 ? 'heavy' : 'medium');
    } else {
      vibrate('light');
    }
    render(mergedCoords);
    if (checkGameOver()) {
      document.getElementById('mod-desc').innerText = 'امتیاز نهایی شما: ' + score;
      document.getElementById('modal').style.display = 'flex';
    }
  }
}

function checkGameOver() {
  for (var r = 0; r < 4; r++) {
    for (var c = 0; c < 4; c++) {
      if (board[r][c] === 0) return false;
      if (c < 3 && board[r][c] === board[r][c + 1]) return false;
      if (r < 3 && board[r][c] === board[r + 1][c]) return false;
    }
  }
  return true;
}

function useUndo() {
  if (undoLeft > 0 && historyList.length > 0) {
    var last = historyList.pop();
    board = last.b;
    score = last.s;
    undoLeft--;
    vibrate('medium');
    render([]);
  }
}

function useSweep() {
  if (sweepLeft <= 0) return;
  var total = 0;
  for (var r = 0; r < 4; r++) for (var c = 0; c < 4; c++) if (board[r][c] > 0) total++;
  if (total <= 2) return;
  var removed = false;
  for (var r2 = 0; r2 < 4; r2++) {
    for (var c2 = 0; c2 < 4; c2++) {
      if (board[r2][c2] === 1 || board[r2][c2] === 2) {
        board[r2][c2] = 0;
        removed = true;
      }
    }
  }
  if (removed) {
    var anyLeft = false;
    for (var r3 = 0; r3 < 4; r3++) for (var c3 = 0; c3 < 4; c3++) if (board[r3][c3] > 0) anyLeft = true;
    if (!anyLeft) addRandomCat();
    sweepLeft--;
    vibrate('heavy');
    render([]);
  }
}

function useWand() {
  if (wandLeft <= 0) return;
  var maxL = 0, mr = -1, mc = -1;
  for (var r = 0; r < 4; r++) {
    for (var c = 0; c < 4; c++) {
      if (board[r][c] > maxL && board[r][c] < 20) {
        maxL = board[r][c];
        mr = r;
        mc = c;
      }
    }
  }
  if (mr !== -1) {
    board[mr][mc] += 1;
    score += board[mr][mc] * 25;
    wandLeft--;
    playTone(board[mr][mc]);
    vibrate('heavy');
    render([[mr, mc]]);
  }
}

function useShuffle() {
  if (shuffleLeft <= 0) return;
  var vals = [];
  for (var r = 0; r < 4; r++) for (var c = 0; c < 4; c++) if (board[r][c] > 0) vals.push(board[r][c]);
  vals.sort(function() { return Math.random() - 0.5; });
  board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]];
  var idx = 0;
  for (var r2 = 0; r2 < 4; r2++) {
    for (var c2 = 0; c2 < 4; c2++) {
      if (idx < vals.length) board[r2][c2] = vals[idx++];
    }
  }
  shuffleLeft--;
  vibrate('heavy');
  render([]);
}

function toggleSound() {
  soundOn = !soundOn;
  var icon = document.getElementById('snd-icon');
  if (soundOn) {
    icon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>';
  } else {
    icon.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
  }
}

var sx = 0, sy = 0;
var bw = document.getElementById('board-wrap');
bw.addEventListener('touchstart', function(e) {
  sx = e.touches[0].clientX;
  sy = e.touches[0].clientY;
}, {passive: false});
bw.addEventListener('touchmove', function(e) {
  e.preventDefault();
}, {passive: false});
bw.addEventListener('touchend', function(e) {
  var dx = e.changedTouches[0].clientX - sx;
  var dy = e.changedTouches[0].clientY - sy;
  if (Math.max(Math.abs(dx), Math.abs(dy)) > 22) {
    if (Math.abs(dx) > Math.abs(dy)) move(dx > 0 ? 'right' : 'left');
    else move(dy > 0 ? 'down' : 'up');
  }
});

window.addEventListener('keydown', function(e) {
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
    return "Telegram Bot & Meow 2048 (20 Levels) are running!"

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
            
            if user_text in ["/start", "/game", "بازی", "گربه"]:
                welcome_msg = (
                    "\U0001F431 *به بازی قلمرو گربه‌ها (۲۰ مرحله) خوش آمدید!* \U0001F3AE\n\n"
                    "گربه‌های هم‌شکل رو به هم بزنید تا در ۲۰ سطح جادویی تکامل پیدا کنن!\n\n"
                    "\U0001F447 برای شروع روی دکمه زیر بزنید:"
                )
                reply_markup = {
                    "inline_keyboard": [[
                        {
                            "text": "\U0001F43E شروع بازی قلمرو گربه‌ها \U0001F3AE",
                            "web_app": {"url": f"{APP_URL}/game?v=2"}
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

          
  if user_text:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
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
        
 
