from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.parse
import json
import html
import re
import ast
import operator
import random
import math

app = Flask(__name__)

# =========================================================
# NYVEXIA AI — PREMIUM GALAXY EDITION
# =========================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#080a18">
<title>Nyvexia AI — Think Beyond</title>
<style>
:root {
  --purple: #8B5CF6;
  --cyan: #22D3EE;
  --pink: #F472B6;
  --background: #080a18;
  --panel: rgba(9, 13, 34, .94);
  --panel-light: rgba(18, 24, 56, .9);
  --text: #F5F7FF;
  --muted: #98a6cf;
  --border: rgba(117, 133, 255, .22);
}

* { box-sizing: border-box; }
html, body { margin: 0; width: 100%; height: 100%; }

body {
  overflow: hidden;
  color: var(--text);
  background: var(--background);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
}

button, input, textarea { font: inherit; }
button { cursor: pointer; }
button:focus-visible, input:focus-visible,
textarea:focus-visible {
  outline: 2px solid var(--cyan);
  outline-offset: 3px;
}
button:disabled { opacity: .45; cursor: not-allowed; }

.space-background {
  position: fixed;
  inset: 0;
  z-index: -2;
  background:
    radial-gradient(ellipse at 72% 15%, rgba(78, 37, 164, .24), transparent 36%),
    radial-gradient(ellipse at 45% 88%, rgba(15, 87, 170, .17), transparent 42%),
    #080a18;
}

.space-background::before {
  content: "";
  position: absolute;
  inset: 0;
  opacity: .4;
  background-image:
    radial-gradient(1px 1px at 8% 18%, #fff 99%, transparent),
    radial-gradient(1px 1px at 22% 72%, #9eeaff 99%, transparent),
    radial-gradient(1px 1px at 41% 12%, #fff 99%, transparent),
    radial-gradient(2px 2px at 69% 35%, #a7a5ff 99%, transparent),
    radial-gradient(1px 1px at 85% 81%, #fff 99%, transparent),
    radial-gradient(1px 1px at 94% 25%, #8bdfff 99%, transparent);
  background-size: 240px 220px, 300px 260px, 350px 300px,
    280px 240px, 320px 290px, 260px 270px;
  pointer-events: none;
}

.app {
  position: relative;
  display: grid;
  grid-template-columns: 265px minmax(0, 1fr) 290px;
  gap: 10px;
  width: 100%;
  height: 100dvh;
  padding: 12px;
}

.sidebar, .main, .right-panel {
  min-width: 0;
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 20px;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.sidebar {
  display: flex;
  flex-direction: column;
  padding: 17px 13px 12px;
  overflow: hidden;
}

.brand {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 7px 7px 23px;
}

.logo {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 15px;
  overflow: hidden;
  background: linear-gradient(145deg, rgba(139, 92, 246, .14), rgba(34, 211, 238, .07));
  border: 1px solid rgba(167, 139, 250, .42);
  box-shadow: 0 8px 24px rgba(7, 5, 28, .24);
}
.logo svg { width: 39px; height: 39px; display: block; }

.brand-name {
  font-size: 17px;
  font-weight: 780;
  letter-spacing: -.5px;
}

.brand-sub {
  color: #b39bff;
  font-size: 9px;
  margin-top: 4px;
  letter-spacing: 1.8px;
  font-weight: 750;
}

.new-chat {
  width: 100%;
  padding: 13px 14px;
  border: 1px solid rgba(139, 92, 246, .55);
  border-radius: 12px;
  color: white;
  text-align: left;
  background: linear-gradient(110deg, #5424d7, #3921a7);
  box-shadow: inset 0 1px rgba(255,255,255,.08);
  transition: filter .18s, transform .18s;
}
.new-chat:hover { filter: brightness(1.16); transform: translateY(-1px); }

.search-wrap { margin: 13px 0 21px; }
.search-wrap input {
  width: 100%;
  min-width: 0;
  padding: 11px 12px;
  border: 1px solid var(--border);
  border-radius: 11px;
  color: white;
  background: rgba(4, 8, 28, .75);
  outline: none;
  font-size: 12px;
}
.search-wrap input:focus { border-color: var(--purple); }

.section-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 8px 10px;
  color: #8497e4;
  font-size: 10px;
  font-weight: 750;
  letter-spacing: 1.3px;
}

.chat-list { overflow-y: auto; flex: 1; min-height: 60px; }
.chat-item {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 5px;
  padding: 11px 8px;
  border: 1px solid transparent;
  border-radius: 12px;
  color: #c7d1f4;
  cursor: pointer;
  font-size: 12px;
  transition: background .18s, border-color .18s;
}
.chat-item:hover { background: rgba(91, 88, 194, .12); }
.chat-item.active {
  background: linear-gradient(110deg, rgba(90, 48, 208, .24), rgba(25, 42, 103, .2));
  border-color: rgba(119, 92, 255, .35);
  color: white;
}

.chat-icon {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 31px;
  height: 31px;
  border: 1px solid rgba(123, 113, 255, .35);
  border-radius: 10px;
  background: rgba(85, 64, 197, .18);
  font-size: 14px;
}
.chat-copy { min-width: 0; flex: 1; }
.chat-title {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chat-date { display: block; margin-top: 4px; color: #8191c4; font-size: 10px; }

.delete-chat {
  flex-shrink: 0;
  padding: 3px 5px;
  border: 0;
  color: #8290bc;
  background: transparent;
  font-size: 17px;
}
.delete-chat:hover { color: #ff9ab9; }

.galaxy-toggle {
  margin-top: 12px;
  padding: 12px 10px;
  border: 1px solid rgba(108, 82, 240, .36);
  border-radius: 13px;
  background: rgba(41, 31, 104, .15);
}
.toggle-line { display: flex; align-items: center; gap: 9px; }
.toggle-symbol {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: rgba(118, 77, 255, .2);
  font-size: 16px;
}
.toggle-copy { flex: 1; font-size: 12px; font-weight: 650; }
.toggle-description { margin: 8px 0 0 41px; color: #7f8ebc; font-size: 9px; }

.switch {
  width: 34px;
  height: 19px;
  border: 0;
  border-radius: 20px;
  padding: 2px;
  background: #454a69;
}
.switch span {
  display: block;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: white;
  transition: transform .2s;
}
.switch.on { background: #7042f5; }
.switch.on span { transform: translateX(15px); }

.sidebar-bottom {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 11px;
  padding: 13px 6px 4px;
  border-top: 1px solid var(--border);
}
.profile-icon {
  display: grid;
  place-items: center;
  width: 37px;
  height: 37px;
  border: 1px solid rgba(119, 117, 255, .4);
  border-radius: 50%;
  background: #171d48;
  font-size: 17px;
}
.profile-name { font-size: 11px; font-weight: 650; }
.profile-sub { margin-top: 4px; color: #8b9bd0; font-size: 10px; }

.main {
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.topbar {
  min-height: 72px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(112, 130, 255, .16);
  background: rgba(8, 11, 29, .6);
}
.topbar-left { display: flex; align-items: center; gap: 11px; min-width: 0; }
.topbar-icon {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: 12px;
  background: #111943;
  color: #a99cff;
}
.current-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  font-weight: 700;
}
.current-subtitle { margin-top: 4px; color: #9aa9dc; font-size: 11px; }
.top-actions { display: flex; align-items: center; gap: 7px; }

.small-btn {
  min-width: 34px;
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: 10px;
  color: #d5ddff;
  background: rgba(31, 39, 84, .5);
  font-size: 12px;
}
.small-btn:hover { border-color: rgba(139, 92, 246, .55); background: #171e48; }
.mobile-menu { display: none; }

.messages {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 26px 24px 24px;
  scroll-behavior: smooth;
}
.message-list { width: 100%; max-width: 820px; margin: 0 auto; }
.welcome { padding: 5vh 0 25px; text-align: center; }

.welcome-mark {
  display: grid;
  place-items: center;
  width: 82px;
  height: 82px;
  margin: 0 auto 17px;
  border: 1px solid rgba(167, 139, 250, .4);
  border-radius: 25px;
  background: linear-gradient(145deg, rgba(111, 61, 255, .14), rgba(30, 108, 184, .12));
  box-shadow: 0 12px 36px rgba(102, 69, 255, .12);
}
.welcome-mark svg { width: 67px; height: 67px; display: block; }

.welcome h1 {
  margin: 0 0 9px;
  font-size: clamp(28px, 3.4vw, 43px);
  letter-spacing: -1.7px;
  font-weight: 760;
}
.welcome h1 span {
  color: #c3b1ff;
  background: linear-gradient(95deg, #e0d3ff, #a58bff 52%, #67e8f9);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.welcome p {
  max-width: 450px;
  margin: 0 auto;
  color: #9ba9d3;
  font-size: 13px;
  line-height: 1.75;
}

.suggestions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  max-width: 610px;
  margin: 25px auto 0;
}
.suggestion {
  display: flex;
  align-items: center;
  gap: 11px;
  min-height: 68px;
  padding: 12px;
  text-align: left;
  border: 1px solid rgba(106, 116, 255, .24);
  border-radius: 14px;
  color: #e4e9ff;
  background: linear-gradient(120deg, rgba(24, 32, 80, .66), rgba(11, 15, 43, .7));
  transition: transform .18s, border-color .18s, background .18s;
}
.suggestion:hover {
  transform: translateY(-2px);
  border-color: rgba(139, 92, 246, .7);
  background: rgba(61, 42, 135, .25);
}
.suggestion-icon {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border: 1px solid rgba(100, 130, 255, .3);
  border-radius: 12px;
  background: rgba(38, 58, 156, .4);
  color: #83eaff;
  font-size: 16px;
}
.suggestion-copy { min-width: 0; font-size: 11px; font-weight: 650; }
.suggestion-copy span {
  display: block;
  margin-top: 5px;
  color: #93a2d2;
  font-size: 10px;
  font-weight: 400;
}

.message { display: flex; gap: 12px; margin-bottom: 25px; align-items: flex-start; }
.avatar {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border: 1px solid rgba(128, 118, 255, .35);
  border-radius: 12px;
  color: white;
  background: linear-gradient(145deg, #6139df, #174b98);
  font-size: 14px;
  font-weight: 750;
}
.avatar.user { background: #242c54; color: #d9e5ff; }
.message-body { min-width: 0; flex: 1; padding-top: 3px; }
.message-name { margin-bottom: 8px; color: #a8b4df; font-size: 11px; font-weight: 700; }
.message-text {
  color: #e5eaff;
  font-size: 13px;
  line-height: 1.85;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.message.bot-message .message-body {
  padding: 15px 17px;
  border: 1px solid rgba(110, 116, 255, .28);
  border-radius: 5px 16px 16px 16px;
  background: linear-gradient(135deg, rgba(22, 30, 78, .83), rgba(10, 16, 43, .85));
}
.message.bot-message .message-name { color: #b8a5ff; }

.sources { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 13px; }
.source-link {
  max-width: 100%;
  overflow-wrap: anywhere;
  padding: 6px 9px;
  border: 1px solid rgba(120, 104, 255, .38);
  border-radius: 20px;
  color: #c4bcff;
  background: rgba(99, 68, 225, .12);
  font-size: 10px;
  text-decoration: none;
}
.source-link:hover { border-color: var(--cyan); color: #aaf5ff; }

.composer-area { flex-shrink: 0; padding: 8px 22px 18px; }
.composer-wrap { max-width: 850px; margin: 0 auto; }
.composer {
  display: flex;
  align-items: flex-end;
  gap: 7px;
  padding: 9px;
  border: 1px solid rgba(139, 92, 246, .55);
  border-radius: 24px;
  background: rgba(7, 11, 31, .96);
  box-shadow: 0 0 25px rgba(87, 49, 235, .09);
  transition: border-color .2s, box-shadow .2s;
}
.composer:focus-within {
  border-color: rgba(34, 211, 238, .8);
  box-shadow: 0 0 25px rgba(34, 211, 238, .09);
}
#question {
  min-width: 0;
  flex: 1;
  resize: none;
  max-height: 140px;
  padding: 9px 7px;
  border: 0;
  outline: 0;
  color: white;
  background: transparent;
  font-size: 13px;
  line-height: 1.6;
}
#question::placeholder { color: #8998c7; }

.icon-btn, .send-btn {
  display: grid;
  place-items: center;
  width: 37px;
  height: 37px;
  flex-shrink: 0;
  border: 1px solid transparent;
  border-radius: 12px;
  color: #a7b4e5;
  background: transparent;
  font-size: 17px;
}
.icon-btn:hover, .icon-btn.active {
  border-color: rgba(34, 211, 238, .3);
  color: var(--cyan);
  background: rgba(34, 211, 238, .09);
}
.send-btn {
  color: white;
  background: linear-gradient(140deg, #8549ff, #5330d8);
  box-shadow: 0 0 18px rgba(113, 65, 255, .19);
  font-size: 20px;
}
.send-btn:hover { filter: brightness(1.15); }
.disclaimer { margin-top: 10px; color: #7281b0; text-align: center; font-size: 9px; }

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  overflow-y: auto;
}
.panel-card {
  padding: 13px;
  border: 1px solid rgba(103, 117, 255, .24);
  border-radius: 16px;
  background: rgba(7, 11, 32, .72);
}
.panel-title { margin: 0 0 12px; font-size: 13px; font-weight: 750; }

.action-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  margin-bottom: 7px;
  padding: 9px;
  border: 1px solid rgba(99, 116, 255, .25);
  border-radius: 12px;
  text-align: left;
  color: white;
  background: rgba(17, 23, 58, .65);
  transition: border-color .18s, background .18s;
}
.action-item:last-child { margin-bottom: 0; }
.action-item:hover { border-color: rgba(139, 92, 246, .65); background: rgba(69, 48, 145, .2); }
.action-icon {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border: 1px solid rgba(80, 160, 255, .3);
  border-radius: 11px;
  color: #7be9ff;
  background: rgba(30, 68, 159, .35);
  font-size: 16px;
}
.action-copy { min-width: 0; font-size: 11px; font-weight: 650; }
.action-copy span { display: block; margin-top: 4px; color: #94a4d4; font-size: 10px; font-weight: 400; }

.feature-list { display: grid; gap: 10px; }
.feature-row { display: flex; align-items: center; gap: 9px; color: #c1cff6; font-size: 11px; }
.feature-dot {
  display: grid;
  place-items: center;
  width: 19px;
  height: 19px;
  flex-shrink: 0;
  border: 1px solid rgba(118, 112, 255, .35);
  border-radius: 7px;
  color: #a7a1ff;
  background: rgba(80, 62, 188, .22);
  font-size: 10px;
}

.promo {
  position: relative;
  display: flex;
  flex: 1;
  min-height: 150px;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
  padding: 16px;
  border: 1px solid rgba(110, 101, 255, .32);
  border-radius: 16px;
  background:
    radial-gradient(ellipse at 50% 28%, rgba(116, 52, 255, .36), transparent 44%),
    radial-gradient(ellipse at 70% 75%, rgba(18, 117, 196, .24), transparent 50%),
    #080d27;
}
.promo-orbit {
  position: absolute;
  top: 17px;
  left: 50%;
  transform: translateX(-50%);
  width: 95px;
  height: 95px;
  border: 1px solid rgba(156, 130, 255, .5);
  border-radius: 50%;
  box-shadow: 0 0 24px rgba(120, 75, 255, .15), inset 0 0 22px rgba(89, 76, 240, .12);
}
.promo-orbit::before, .promo-orbit::after {
  content: "";
  position: absolute;
  inset: 16px -8px;
  border: 2px solid rgba(133, 102, 255, .7);
  border-radius: 50%;
  transform: rotate(-32deg);
}
.promo-orbit::after {
  inset: 27px -13px;
  border-color: rgba(34, 211, 238, .5);
  transform: rotate(35deg);
}
.promo-copy { position: relative; text-align: center; }
.promo-copy strong { display: block; font-size: 14px; }
.promo-copy p { margin: 7px 0 0; color: #a9b8e7; font-size: 11px; line-height: 1.7; }

.typing { display: inline-flex; gap: 5px; padding: 5px 0; }
.typing span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #b2a0ff;
  animation: pulse 1s infinite alternate;
}
.typing span:nth-child(2) { animation-delay: .2s; }
.typing span:nth-child(3) { animation-delay: .4s; }
@keyframes pulse {
  from { opacity: .3; transform: translateY(0); }
  to { opacity: 1; transform: translateY(-3px); }
}

.toast {
  position: fixed;
  z-index: 100;
  bottom: 25px;
  left: 50%;
  transform: translateX(-50%);
  display: none;
  max-width: calc(100vw - 30px);
  padding: 11px 16px;
  border: 1px solid var(--border);
  border-radius: 12px;
  color: white;
  background: #171b3a;
  box-shadow: 0 10px 40px #0008;
  font-size: 12px;
}

body.galaxy-off .space-background::before { opacity: .08; }
body.galaxy-off .space-background {
  background: radial-gradient(ellipse at 75% 5%, #17133c, transparent 42%), #0b1021;
}

@media (min-width: 1450px) {
  .app { grid-template-columns: 285px minmax(0, 1fr) 310px; gap: 12px; padding: 15px; }
  .messages { padding: 32px; }
}
@media (max-width: 1120px) {
  .app { grid-template-columns: 245px minmax(0, 1fr); }
  .right-panel { display: none; }
}
@media (max-width: 720px) {
  .app { display: block; padding: 0; }
  .sidebar {
    position: fixed;
    z-index: 30;
    top: 0; bottom: 0; left: 0;
    width: min(290px, 86vw);
    border-radius: 0 18px 18px 0;
    transform: translateX(-110%);
    transition: transform .22s ease;
    box-shadow: 15px 0 45px #0009;
  }
  .sidebar.open { transform: translateX(0); }
  .main {
    width: 100%;
    height: 100dvh;
    border: 0;
    border-radius: 0;
  }
  .topbar { min-height: 62px; padding: 0 12px; gap: 7px; }
  .mobile-menu { display: inline-block; }
  .current-title { max-width: 155px; font-size: 12px; }
  .current-subtitle { font-size: 10px; }
  .top-actions { gap: 4px; }
  .small-btn { padding: 7px 8px; font-size: 11px; }
  .messages { padding: 18px 13px; }
  .welcome { padding-top: 5vh; }
  .welcome h1 { font-size: 30px; }
  .welcome-mark { width: 64px; height: 64px; border-radius: 19px; }
  .welcome-mark svg { width: 53px; height: 53px; }
  .suggestions { grid-template-columns: 1fr; gap: 8px; margin-top: 22px; }
  .suggestion { min-height: 59px; }
  .message { gap: 8px; margin-bottom: 20px; }
  .avatar { width: 30px; height: 30px; border-radius: 10px; }
  .message.bot-message .message-body { padding: 12px; }
  .message-text { font-size: 13px; }
  .composer-area { padding: 7px 10px 12px; }
  .composer { gap: 3px; padding: 7px; }
  .icon-btn, .send-btn { width: 34px; height: 35px; }
  .disclaimer { font-size: 9px; }
}
@media (max-height: 720px) {
  .welcome { padding-top: 2vh; }
  .welcome-mark { width: 58px; height: 58px; margin-bottom: 12px; }
  .welcome-mark svg { width: 48px; height: 48px; }
  .welcome h1 { font-size: 30px; }
  .suggestions { margin-top: 17px; }
  .suggestion { min-height: 57px; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
</style>
</head>
<body>
<div class="space-background"></div>

<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="logo" aria-label="Nyvexia logo">
        <svg viewBox="0 0 100 100" role="img" aria-hidden="true">
          <defs>
            <linearGradient id="nxCore" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#F5F3FF"/>
              <stop offset="48%" stop-color="#A78BFA"/>
              <stop offset="100%" stop-color="#22D3EE"/>
            </linearGradient>
            <linearGradient id="nxOrbit" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#C4B5FD"/>
              <stop offset="100%" stop-color="#22D3EE"/>
            </linearGradient>
          </defs>
          <circle cx="50" cy="50" r="29" fill="none" stroke="url(#nxOrbit)" stroke-width="2.8" opacity=".9"/>
          <ellipse cx="50" cy="50" rx="43" ry="17" fill="none" stroke="url(#nxOrbit)" stroke-width="3.4" transform="rotate(-38 50 50)"/>
          <path d="M50 24 L56 43 L76 50 L56 56 L50 76 L44 56 L24 50 L44 43 Z" fill="url(#nxCore)"/>
          <circle cx="77" cy="23" r="4" fill="#F8FAFF"/>
          <circle cx="22" cy="76" r="2.8" fill="#22D3EE"/>
        </svg>
      </div>
      <div>
        <div class="brand-name">Nyvexia AI</div>
        <div class="brand-sub">SINCE 2026</div>
      </div>
    </div>

    <button class="new-chat" id="newChat">＋ &nbsp; New Chat</button>

    <div class="search-wrap">
      <input id="historySearch" placeholder="⌕  Search chats..." autocomplete="off">
    </div>

    <div class="section-label">
      <span>CHAT HISTORY</span><span>⌃</span>
    </div>
    <div class="chat-list" id="chatList"></div>

    <div class="galaxy-toggle">
      <div class="toggle-line">
        <div class="toggle-symbol">✧</div>
        <div class="toggle-copy">Galaxy Mode</div>
        <button class="switch on" id="galaxyToggle" aria-label="Toggle galaxy mode"><span></span></button>
      </div>
      <div class="toggle-description">A little more cosmic. Still focused.</div>
    </div>

    <div class="sidebar-bottom">
      <div class="profile-icon">✦</div>
      <div>
        <div class="profile-name">Nyvexia AI</div>
        <div class="profile-sub">Your AI assistant</div>
      </div>
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div class="topbar-left">
        <button class="small-btn mobile-menu" id="menuBtn" aria-label="Open chat history">☰</button>
        <div class="topbar-icon">▤</div>
        <div style="min-width:0">
          <div class="current-title" id="currentTitle">New Chat</div>
          <div class="current-subtitle">Your universe. Your questions.</div>
        </div>
      </div>
      <div class="top-actions">
        <button class="small-btn" id="renameBtn" title="Rename conversation">✎ <span class="desktop-label">Rename</span></button>
        <button class="small-btn" id="voiceToggle" title="Toggle spoken replies">◖))</button>
        <button class="small-btn" id="fullscreenBtn" title="Toggle fullscreen">⛶</button>
      </div>
    </header>

    <section class="messages" id="messages">
      <div class="message-list" id="messageList"></div>
    </section>

    <div class="composer-area">
      <div class="composer-wrap">
        <form class="composer" id="form">
          <button class="icon-btn" type="button" id="micBtn" title="Speak your message" aria-label="Microphone">♩</button>
          <textarea id="question" rows="1" placeholder="Ask Nyvexia anything..." autocomplete="off"></textarea>
          <button class="icon-btn" type="button" id="webBtn" title="Search the web" aria-label="Search the web">◎</button>
          <button class="icon-btn" type="button" id="mathBtn" title="Calculate" aria-label="Calculate">▦</button>
          <button class="icon-btn" type="button" id="translateBtn" title="Translate" aria-label="Translate">文</button>
          <button class="send-btn" id="send" type="submit" aria-label="Send message">➤</button>
        </form>
        <div class="disclaimer">Nyvexia can make mistakes. Verify important information.</div>
      </div>
    </div>
  </main>

  <aside class="right-panel">
    <section class="panel-card">
      <h2 class="panel-title">Quick Actions</h2>
      <button class="action-item" data-prompt="Search the web for the latest news about space exploration">
        <span class="action-icon">⌕</span>
        <span class="action-copy">Search the Web<span>Find relevant web results</span></span>
      </button>
      <button class="action-item" data-prompt="Solve 3x + 7 = 22 and show the steps">
        <span class="action-icon">▦</span>
        <span class="action-copy">Solve Math<span>Calculations and equations</span></span>
      </button>
      <button class="action-item" data-prompt="Translate 'Hello, how are you?' into French">
        <span class="action-icon">文</span>
        <span class="action-copy">Translate<span>Try another language</span></span>
      </button>
      <button class="action-item" id="voiceAction">
        <span class="action-icon">♩</span>
        <span class="action-copy">Voice Input<span>Talk to Nyvexia</span></span>
      </button>
      <button class="action-item" id="listenAction">
        <span class="action-icon">◖))</span>
        <span class="action-copy">Listen<span>Toggle spoken replies</span></span>
      </button>
    </section>

    <section class="panel-card">
      <h2 class="panel-title">Features</h2>
      <div class="feature-list">
        <div class="feature-row"><span class="feature-dot">✓</span> Web search and source links</div>
        <div class="feature-row"><span class="feature-dot">✓</span> Math and calculations</div>
        <div class="feature-row"><span class="feature-dot">✓</span> Multilingual translation</div>
        <div class="feature-row"><span class="feature-dot">✓</span> Voice input and speech</div>
        <div class="feature-row"><span class="feature-dot">✓</span> Saved browser chat history</div>
        <div class="feature-row"><span class="feature-dot">✓</span> Rename and delete chats</div>
      </div>
    </section>

    <section class="promo">
      <div class="promo-orbit"></div>
      <div class="promo-copy">
        <strong>Explore more...</strong>
        <p>The universe of knowledge<br>starts with a question.</p>
      </div>
    </section>
  </aside>
</div>

<div class="toast" id="toast"></div>

<script>
const STORAGE_KEY = "nyvexia_galaxy_chats_v1";
const VOICE_KEY = "nyvexia_voice_enabled_v1";
const GALAXY_KEY = "nyvexia_galaxy_mode_v1";

const welcomeMessage = {
  who: "bot",
  text: "Hey! Welcome to Nyvexia AI. Ask me a question, search the web, solve a math problem, or translate between languages.",
  links: []
};

let chats = [];
let activeId = null;
let busy = false;
let voiceEnabled = localStorage.getItem(VOICE_KEY) === "true";
let galaxyEnabled = localStorage.getItem(GALAXY_KEY) !== "false";
let recognition = null;
let toastTimer = null;

const $ = id => document.getElementById(id);
const messagesBox = $("messages");
const messageList = $("messageList");
const questionBox = $("question");
const sendButton = $("send");

function makeChat() {
  return {
    id: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random()),
    title: "New conversation",
    messages: [{...welcomeMessage}],
    apiHistory: [],
    created: Date.now()
  };
}

function loadChats() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    if (Array.isArray(saved)) {
      chats = saved.filter(c => c && c.id && Array.isArray(c.messages)).map(c => ({
        id: c.id,
        title: c.title || "New conversation",
        messages: c.messages,
        apiHistory: Array.isArray(c.apiHistory) ? c.apiHistory : [],
        created: c.created || Date.now()
      }));
    }
  } catch (e) {
    chats = [];
  }

  if (!chats.length) chats = [makeChat()];
  activeId = chats[0].id;
  saveChats();
}

function saveChats() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
  } catch (e) {
    showToast("Could not save chats in this browser.");
  }
}

function activeChat() {
  return chats.find(c => c.id === activeId) || chats[0];
}

function showToast(text) {
  const el = $("toast");
  el.textContent = text;
  el.style.display = "block";
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.style.display = "none", 2800);
}

function escapeHTML(text) {
  return String(text).replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#39;"
  }[ch]));
}

function relativeDate(timestamp) {
  const d = new Date(timestamp || Date.now());
  const today = new Date();
  if (d.toDateString() === today.toDateString()) {
    return "Today, " + d.toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
  }
  return d.toLocaleDateString([], {month: "short", day: "numeric"});
}

function renderChats() {
  const term = $("historySearch").value.trim().toLowerCase();
  const list = $("chatList");
  list.innerHTML = "";

  const filtered = [...chats]
    .sort((a, b) => (b.created || 0) - (a.created || 0))
    .filter(c => !term ||
      c.title.toLowerCase().includes(term) ||
      c.messages.some(m => String(m.text || "").toLowerCase().includes(term))
    );

  if (!filtered.length) {
    list.textContent = "No matching conversations.";
    list.style.padding = "10px";
    list.style.color = "#91a0cf";
    list.style.fontSize = "12px";
    return;
  }

  filtered.forEach(chat => {
    const item = document.createElement("div");
    item.className = "chat-item" + (chat.id === activeId ? " active" : "");

    const icon = document.createElement("span");
    icon.className = "chat-icon";
    icon.textContent = chat.title.toLowerCase().includes("math") ? "▦" :
      chat.title.toLowerCase().includes("translat") ? "文" : "◇";

    const copy = document.createElement("span");
    copy.className = "chat-copy";

    const title = document.createElement("span");
    title.className = "chat-title";
    title.textContent = chat.title;

    const date = document.createElement("span");
    date.className = "chat-date";
    date.textContent = relativeDate(chat.created);

    copy.append(title, date);

    const del = document.createElement("button");
    del.className = "delete-chat";
    del.textContent = "⋮";
    del.title = "Delete conversation";
    del.setAttribute("aria-label", "Delete " + chat.title);
    del.onclick = e => {
      e.stopPropagation();
      deleteChat(chat.id);
    };

    item.append(icon, copy, del);
    item.onclick = () => {
      activeId = chat.id;
      renderAll();
      if (innerWidth <= 720) $("sidebar").classList.remove("open");
    };
    list.append(item);
  });
}

function welcomeHTML() {
  return `
    <div class="welcome">
      <div class="welcome-mark" aria-label="Nyvexia logo">
        <svg viewBox="0 0 100 100" role="img" aria-hidden="true">
          <defs>
            <linearGradient id="welcomeCore" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#F5F3FF"/>
              <stop offset="48%" stop-color="#A78BFA"/>
              <stop offset="100%" stop-color="#22D3EE"/>
            </linearGradient>
            <linearGradient id="welcomeOrbit" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#C4B5FD"/>
              <stop offset="100%" stop-color="#22D3EE"/>
            </linearGradient>
          </defs>
          <circle cx="50" cy="50" r="29" fill="none" stroke="url(#welcomeOrbit)" stroke-width="2.8" opacity=".9"/>
          <ellipse cx="50" cy="50" rx="43" ry="17" fill="none" stroke="url(#welcomeOrbit)" stroke-width="3.4" transform="rotate(-38 50 50)"/>
          <path d="M50 24 L56 43 L76 50 L56 56 L50 76 L44 56 L24 50 L44 43 Z" fill="url(#welcomeCore)"/>
          <circle cx="77" cy="23" r="4" fill="#F8FAFF"/>
          <circle cx="22" cy="76" r="2.8" fill="#22D3EE"/>
        </svg>
      </div>
      <h1>Nyvexia <span>AI</span></h1>
      <p>Ask. Explore. Discover. Your space to think beyond the ordinary.</p>
      <div class="suggestions">
        <button class="suggestion" data-prompt="Search the web for the latest news about space exploration">
          <span class="suggestion-icon">⌕</span>
          <span class="suggestion-copy">Search the web<span>Find current information</span></span>
        </button>
        <button class="suggestion" data-prompt="Solve 3x + 7 = 22 and show the steps">
          <span class="suggestion-icon">▦</span>
          <span class="suggestion-copy">Solve a math problem<span>See the steps</span></span>
        </button>
        <button class="suggestion" data-prompt="Translate 'How are you today?' into French">
          <span class="suggestion-icon">文</span>
          <span class="suggestion-copy">Translate a sentence<span>Explore other languages</span></span>
        </button>
        <button class="suggestion" data-prompt="Tell me an interesting science fact and explain why it matters">
          <span class="suggestion-icon">✧</span>
          <span class="suggestion-copy">Explore an idea<span>Discover something new</span></span>
        </button>
      </div>
    </div>`;
}

function renderMessages() {
  const chat = activeChat();
  if (!chat) return;

  $("currentTitle").textContent = chat.title;
  messageList.innerHTML = "";

  if (chat.messages.length === 1 && chat.messages[0].text === welcomeMessage.text) {
    messageList.innerHTML = welcomeHTML();
    messageList.querySelectorAll("[data-prompt]").forEach(b => {
      b.onclick = () => {
        questionBox.value = b.dataset.prompt;
        questionBox.focus();
        resizeInput();
      };
    });
    return;
  }

  chat.messages.forEach(msg => {
    const row = document.createElement("div");
    row.className = "message" + (msg.who === "user" ? " user-message" : " bot-message");

    const av = document.createElement("div");
    av.className = "avatar " + (msg.who === "user" ? "user" : "bot");
    av.textContent = msg.who === "user" ? "Y" : "✦";

    const body = document.createElement("div");
    body.className = "message-body";

    const name = document.createElement("div");
    name.className = "message-name";
    name.textContent = msg.who === "user" ? "You" : "Nyvexia AI";

    const content = document.createElement("div");
    content.className = "message-text";
    content.textContent = msg.text || "";

    body.append(name, content);

    if (msg.who !== "user" && Array.isArray(msg.links) && msg.links.length) {
      const links = document.createElement("div");
      links.className = "sources";

      msg.links.forEach(link => {
        if (!link.url || !/^https?:\/\//i.test(link.url)) return;
        const a = document.createElement("a");
        a.className = "source-link";
        a.href = link.url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = link.title || "Source";
        links.append(a);
      });

      body.append(links);
    }

    row.append(av, body);
    messageList.append(row);
  });

  if (busy) {
    const row = document.createElement("div");
    row.className = "message bot-message";
    row.innerHTML = '<div class="avatar bot">✦</div><div class="message-body"><div class="message-name">Nyvexia AI</div><div class="typing"><span></span><span></span><span></span></div></div>';
    messageList.append(row);
  }
}

function renderAll() {
  renderChats();
  renderMessages();
  saveChats();

  $("voiceToggle").textContent = voiceEnabled ? "◖)) On" : "◖))";
  $("galaxyToggle").classList.toggle("on", galaxyEnabled);
  document.body.classList.toggle("galaxy-off", !galaxyEnabled);
  $("galaxyToggle").setAttribute("aria-pressed", String(galaxyEnabled));

  requestAnimationFrame(() => {
    messagesBox.scrollTop = messagesBox.scrollHeight;
  });
}

function createNewChat() {
  const c = makeChat();
  chats.unshift(c);
  activeId = c.id;
  questionBox.value = "";
  resizeInput();
  renderAll();
  questionBox.focus();
  if (innerWidth <= 720) $("sidebar").classList.remove("open");
}

function deleteChat(id) {
  const c = chats.find(x => x.id === id);
  if (!c || !confirm('Delete "' + c.title + '"?')) return;

  chats = chats.filter(x => x.id !== id);
  if (!chats.length) chats = [makeChat()];
  if (activeId === id) activeId = chats[0].id;
  renderAll();
}

function renameChat() {
  const c = activeChat();
  if (!c) return;

  const v = prompt("Rename this conversation:", c.title);
  if (v === null) return;

  const n = v.trim().slice(0, 70);
  if (!n) return showToast("The title can't be empty.");

  c.title = n;
  renderAll();
}

function autoTitle(c, t) {
  if (c.title === "New conversation") {
    t = t.replace(/\s+/g, " ").trim();
    c.title = t.length > 34 ? t.slice(0, 31) + "..." : t;
  }
}

function resizeInput() {
  questionBox.style.height = "auto";
  questionBox.style.height = Math.min(questionBox.scrollHeight, 140) + "px";
}

async function sendMessage(override) {
  if (busy) return;

  const question = (typeof override === "string" ? override : questionBox.value).trim();
  if (!question) return;

  const chat = activeChat();
  questionBox.value = "";
  resizeInput();

  autoTitle(chat, question);
  chat.messages.push({who: "user", text: question, links: []});

  busy = true;
  sendButton.disabled = true;
  renderAll();

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, history: chat.apiHistory})
    });

    const data = await response.json();
    if (!response.ok) throw Error(data.error || "Request failed");

    chat.messages.push({
      who: "bot",
      text: data.answer || "Sorry, I couldn't find an answer.",
      links: Array.isArray(data.links) ? data.links : []
    });

    if (Array.isArray(data.history)) chat.apiHistory = data.history;

    saveChats();
    renderAll();
    if (voiceEnabled) speak(data.answer || "");
  } catch (e) {
    chat.messages.push({
      who: "bot",
      text: "I couldn't reach the answer service. Please try again in a moment.",
      links: []
    });
    renderAll();
    showToast("Connection problem. Try again.");
  } finally {
    busy = false;
    sendButton.disabled = false;
    renderAll();
    questionBox.focus();
  }
}

function speak(text) {
  if (!("speechSynthesis" in window)) {
    return showToast("Spoken replies aren't supported in this browser.");
  }

  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = detectSpeechLanguage(text);
  speechSynthesis.speak(u);
}

function detectSpeechLanguage(t) {
  if (/[ñ¿¡áéíóú]/i.test(t)) return "es-ES";
  if (/[àâçéèêëîïôûùüÿœ]/i.test(t)) return "fr-FR";
  return "en-US";
}

function toggleVoice() {
  voiceEnabled = !voiceEnabled;
  localStorage.setItem(VOICE_KEY, String(voiceEnabled));
  if (!voiceEnabled && "speechSynthesis" in window) speechSynthesis.cancel();
  renderAll();
  showToast(voiceEnabled ? "Spoken replies enabled." : "Spoken replies disabled.");
}

function startMic() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return showToast("Voice input works in supported browsers such as Chrome or Edge.");

  if (recognition) {
    recognition.stop();
    recognition = null;
    $("micBtn").classList.remove("active");
    return;
  }

  recognition = new SR();
  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = true;
  $("micBtn").classList.add("active");

  let finalText = "";

  recognition.onresult = e => {
    let interim = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const t = e.results[i][0].transcript;
      if (e.results[i].isFinal) finalText += t;
      else interim += t;
    }
    questionBox.value = (finalText + " " + interim).trim();
    resizeInput();
  };

  recognition.onerror = e => showToast(
    e.error === "not-allowed"
      ? "Allow microphone access in your browser settings."
      : "Couldn't hear that. Try again."
  );

  recognition.onend = () => {
    $("micBtn").classList.remove("active");
    recognition = null;
  };

  try {
    recognition.start();
  } catch (e) {
    recognition = null;
    $("micBtn").classList.remove("active");
    showToast("Microphone couldn't start. Try again.");
  }
}

function insertPrompt(text) {
  questionBox.value = text;
  questionBox.focus();
  resizeInput();
}

$("form").addEventListener("submit", e => {
  e.preventDefault();
  sendMessage();
});

questionBox.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

questionBox.addEventListener("input", resizeInput);
$("newChat").onclick = createNewChat;
$("renameBtn").onclick = renameChat;
$("voiceToggle").onclick = toggleVoice;
$("micBtn").onclick = startMic;
$("historySearch").oninput = renderChats;

$("menuBtn").onclick = () => $("sidebar").classList.toggle("open");
$("galaxyToggle").onclick = () => {
  galaxyEnabled = !galaxyEnabled;
  localStorage.setItem(GALAXY_KEY, String(galaxyEnabled));
  renderAll();
};

$("voiceAction").onclick = startMic;
$("listenAction").onclick = toggleVoice;

$("webBtn").onclick = () => insertPrompt("Search the web for ");
$("mathBtn").onclick = () => insertPrompt("Calculate ");
$("translateBtn").onclick = () => insertPrompt("Translate ");

$("fullscreenBtn").onclick = async () => {
  try {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
    else await document.exitFullscreen();
  } catch (e) {
    showToast("Fullscreen isn't available in this browser.");
  }
};

document.querySelectorAll(".action-item[data-prompt]").forEach(button => {
  button.onclick = () => insertPrompt(button.dataset.prompt);
});

loadChats();
renderAll();
</script>
</body>
</html>
"""


# =========================================================
# NETWORK HELPERS
# =========================================================

def fetch_text(url, timeout=12, headers=None):
    default_headers = {
        "User-Agent": "NyvexiaAI/6.0 (personal educational assistant)"
    }
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def normalize(text):
    return re.sub(r"\s+", " ", str(text or "").lower().strip()).rstrip("?!., ")


# =========================================================
# TRANSLATION
# =========================================================

def translate_text(text, target, source="auto"):
    target_codes = {
        "english": "en", "anglais": "en", "en": "en",
        "french": "fr", "français": "fr", "francais": "fr", "fr": "fr",
        "spanish": "es", "español": "es", "espagnol": "es", "es": "es",
        "german": "de", "allemand": "de", "deutsch": "de", "de": "de",
        "italian": "it", "italien": "it", "italiano": "it", "it": "it",
        "portuguese": "pt", "portugais": "pt", "português": "pt", "pt": "pt",
        "japanese": "ja", "japonais": "ja", "日本語": "ja", "ja": "ja",
        "chinese": "zh-CN", "chinois": "zh-CN", "中文": "zh-CN",
        "arabic": "ar", "arabe": "ar", "العربية": "ar",
        "korean": "ko", "coréen": "ko", "한국어": "ko",
        "hindi": "hi", "हिन्दी": "hi",
        "russian": "ru", "russe": "ru", "русский": "ru"
    }

    tgt = target_codes.get(target.lower().strip(), target.strip())
    src = "en" if source == "auto" else target_codes.get(
        source.lower().strip(), source.strip()
    )

    query = urllib.parse.urlencode({
        "q": text[:450],
        "langpair": src + "|" + tgt
    })

    data = json.loads(fetch_text(
        "https://api.mymemory.translated.net/get?" + query,
        timeout=15
    ))

    translated = html.unescape(
        data.get("responseData", {}).get("translatedText", "")
    )

    if not translated or data.get("responseStatus") not in (200, "200"):
        raise ValueError("Translation service did not return a translation.")

    return translated


def extract_translation_request(question):
    patterns = [
        r"(?is)^\s*translate\s+(.+?)\s+(?:into|to|in)\s+([a-zA-ZÀ-ÿ\u4e00-\u9fff -]+)[.!?]*\s*$",
        r"(?is)^\s*traduis\s+(.+?)\s+(?:en|vers)\s+([a-zA-ZÀ-ÿ -]+)[.!?]*\s*$",
        r"(?is)^\s*traduce\s+(.+?)\s+(?:al|a|en)\s+([a-zA-ZÀ-ÿ -]+)[.!?]*\s*$"
    ]

    for pattern in patterns:
        match = re.match(pattern, question)
        if match:
            return (
                match.group(1).strip(" '\""),
                match.group(2).strip(" .?!")
            )

    return None


# =========================================================
# MATH
# =========================================================

def safe_calculate(expression):
    expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
    expression = expression.replace(",", "")

    tree = ast.parse(expression, mode="eval")

    binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv
    }

    unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
            left = visit(node.left)
            right = visit(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent is too large.")

            result = binary_ops[type(node.op)](left, right)

            if not math.isfinite(float(result)) or abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
            return unary_ops[type(node.op)](visit(node.operand))

        raise ValueError("Unsupported arithmetic expression.")

    return visit(tree)


def math_answer(question):
    q = question.strip()

    eq = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)\s*\*?\s*x\s*([+-]\s*\d+(?:\.\d+)?)?\s*=\s*(-?\d+(?:\.\d+)?)\s*",
        q,
        re.I
    )

    if eq:
        a = float(eq.group(1))
        b = float((eq.group(2) or "0").replace(" ", ""))
        c = float(eq.group(3))

        if a == 0:
            return (
                "This equation has no unique solution because the coefficient of x is 0.",
                []
            )

        x = (c - b) / a

        return (
            f"Let's solve it step by step:\n\n"
            f"{a:g}x {b:+g} = {c:g}\n"
            f"Subtract {b:g} from both sides: {a:g}x = {c-b:g}\n"
            f"Divide both sides by {a:g}: x = {x:g}\n\n"
            f"Answer: x = {x:g}",
            []
        )

    cleaned = re.sub(
        r"^(what is|what's|calculate|compute|evaluate|solve)\s+",
        "",
        q,
        flags=re.I
    ).strip().rstrip("?=")

    cleaned = cleaned.replace("²", "**2").replace("³", "**3")

    if not re.fullmatch(r"[\d\s.+\-*/()%^×÷,]+", cleaned):
        return None

    try:
        result = safe_calculate(cleaned)

        if isinstance(result, float):
            shown = str(int(result)) if result.is_integer() else f"{result:.10g}"
        else:
            shown = str(result)

        return f"{cleaned} = {shown}", []

    except ZeroDivisionError:
        return "You can't divide by zero.", []

    except Exception:
        return None


# =========================================================
# WEB SEARCH AND WIKIPEDIA FALLBACK
# =========================================================

def web_search(question, limit=5):
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({
        "q": question
    })

    page = fetch_text(url, timeout=15)

    blocks = re.findall(
        r'(?is)<div[^>]+class="result[^"]*"[^>]*>(.*?)</div>\s*</div>',
        page
    )

    results = []

    for block in blocks:
        link_match = re.search(
            r'(?is)<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            block
        )

        if not link_match:
            continue

        url_value = html.unescape(link_match.group(1))
        title = re.sub(r"<.*?>", "", html.unescape(link_match.group(2)))
        title = re.sub(r"\s+", " ", title).strip()

        snippet_match = re.search(
            r'(?is)class="result__snippet"[^>]*>(.*?)</',
            block
        )

        snippet = re.sub(
            r"<.*?>", "", html.unescape(snippet_match.group(1))
        ) if snippet_match else ""

        snippet = re.sub(r"\s+", " ", snippet).strip()

        if "uddg=" in url_value:
            try:
                url_value = urllib.parse.parse_qs(
                    urllib.parse.urlparse(url_value).query
                ).get("uddg", [url_value])[0]
            except Exception:
                pass

        if url_value.startswith("http") and title:
            results.append({
                "title": title[:180],
                "url": url_value,
                "snippet": snippet[:500]
            })

        if len(results) >= limit:
            break

    return results


def wikipedia_search(question):
    api = "https://en.wikipedia.org/w/api.php?"

    search_url = api + urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "format": "json",
        "utf8": 1,
        "srsearch": question,
        "srlimit": 4
    })

    data = json.loads(fetch_text(search_url))
    results = data.get("query", {}).get("search", [])
    links = []
    pieces = []

    for item in results[:3]:
        title = item.get("title", "")
        if not title:
            continue

        page_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(
            title.replace(" ", "_"), safe="()_,-"
        )

        links.append({
            "title": title + " — Wikipedia",
            "url": page_url
        })

        snippet = re.sub(
            r"<.*?>", "", html.unescape(item.get("snippet", ""))
        )

        if snippet:
            pieces.append(title + ": " + snippet)

    return ("\n\n".join(pieces) if pieces else ""), links


# =========================================================
# ANSWER ROUTER
# =========================================================

def answer_question(question, history):
    q = normalize(question)

    if q in {
        "hi", "hello", "hey", "heyy", "yo", "sup",
        "good morning", "good afternoon", "good evening"
    }:
        return random.choice([
            "Hey! What's on your mind?",
            "Heyyy! What should we explore today?",
            "Hi! Ask me a question and let's figure it out."
        ]), []

    if q in {"thanks", "thank you", "thx", "ty", "thank u"}:
        return "You're welcome! 💜", []

    if q in {
        "who are you", "what are you", "what is your name", "whats your name"
    }:
        return (
            "I'm Nyvexia AI. I can search the web, help with calculations, "
            "and translate text between many languages. I can still make "
            "mistakes, so verify important information."
        ), []

    if q in {"what can you do", "help me"}:
        return (
            "I can search the web for current information, solve many "
            "arithmetic problems and simple linear equations, translate "
            "text, and answer in several languages. Try: “What is the latest "
            "news about space?”, “Solve 3x + 7 = 22”, or "
            "“Translate hello to French.”"
        ), []

    translation = extract_translation_request(question)

    if translation:
        text, target = translation

        try:
            translated = translate_text(text, target)
            return (
                f"Translation into {target}:\n{translated}\n\n"
                "Note: automatic translations can miss context or nuance."
            ), []
        except Exception:
            return (
                "I couldn't reach the translation service right now. "
                "Please try again in a moment."
            ), []

    say_match = re.match(
        r"(?is)^\s*(?:how do you say|how to say)\s+(.+?)\s+in\s+([a-zA-ZÀ-ÿ -]+)[?!.]*\s*$",
        question
    )

    if say_match:
        try:
            return translate_text(
                say_match.group(1).strip(" '\""),
                say_match.group(2).strip()
            ), []
        except Exception:
            pass

    math_result = math_answer(question)

    if math_result is not None:
        return math_result

    try:
        results = web_search(question, 5)
    except Exception:
        results = []

    if results:
        answer_lines = ["I searched the web. Here are some relevant results:"]
        links = []

        for item in results[:4]:
            line = "• " + item["title"]

            if item["snippet"]:
                line += "\n  " + item["snippet"]

            answer_lines.append(line)

            links.append({
                "title": item["title"],
                "url": item["url"]
            })

        answer_lines.append(
            "\nThese are search-result excerpts, not a fully verified "
            "summary. Open the source links to check the details."
        )

        return "\n\n".join(answer_lines), links

    try:
        answer, links = wikipedia_search(question)

        if answer:
            return (
                answer + "\n\nI couldn't retrieve broader web results, "
                "so this fallback uses Wikipedia search excerpts."
            ), links

    except Exception:
        pass

    return (
        "I couldn't retrieve web results right now. Please try again, "
        "or rephrase your question. Math expressions and translation "
        "requests can still work when their services are available."
    ), []


# =========================================================
# FLASK ROUTES
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        question = str(data.get("question", "")).strip()
        history = data.get("history", [])

        if not question:
            return jsonify({
                "answer": "Type a question first and I'll do my best to help.",
                "links": [],
                "history": history if isinstance(history, list) else []
            })

        if not isinstance(history, list):
            history = []

        history = [
            item for item in history[-10:]
            if isinstance(item, dict)
            and item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ]

        answer, links = answer_question(question, history)

        updated_history = (
            history + [
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ]
        )[-10:]

        return jsonify({
            "answer": answer,
            "links": links,
            "history": updated_history
        })

    except Exception:
        return jsonify({
            "answer": "Something went wrong while processing that message. Please try again.",
            "links": [],
            "history": []
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
