import json
import time
import textwrap

import streamlit as st
from google import genai
from google.genai import types
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudySnap AI · Luxury Study Companion",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HTML HELPER
# ============================================================

def html(markup: str):
    st.html(textwrap.dedent(markup).strip())


# ============================================================
# GLOBAL CSS — ULTRA PREMIUM DESIGN SYSTEM
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;0,900;1,500;1,600;1,700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-0: #02030A;
    --bg-1: #050713;
    --card: rgba(8, 10, 22, 0.62);
    --glass: rgba(255, 255, 255, 0.045);
    --purple: #7C3AED;
    --violet: #A855F7;
    --violet-soft: #C9A5FF;
    --cyan: #38BDF8;
    --cyan-soft: #7FD0FF;
    --gold: #F5D38A;
    --gold-soft: #FFE9B8;
    --white: #F8FAFC;
    --text-2: #CBD5E1;
    --muted: #94A3B8;
    --muted-2: #64748B;
    --ease: cubic-bezier(0.22, 1, 0.36, 1);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 15% -5%, rgba(124,58,237,0.22), transparent 55%),
        radial-gradient(ellipse 70% 55% at 105% 5%, rgba(56,189,248,0.16), transparent 55%),
        radial-gradient(ellipse 75% 60% at 50% 115%, rgba(236,72,153,0.12), transparent 60%),
        radial-gradient(ellipse 60% 40% at 20% 90%, rgba(245,211,138,0.10), transparent 60%),
        linear-gradient(180deg, #02030A 0%, #050713 45%, #02030A 100%);
    background-attachment: fixed;
    color: var(--white);
    position: relative;
    overflow-x: hidden;
    min-height: 100vh;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: -25%;
    background:
        radial-gradient(circle 40% at 22% 30%, rgba(124,58,237,0.20), transparent 60%),
        radial-gradient(circle 40% at 78% 70%, rgba(56,189,248,0.16), transparent 60%),
        radial-gradient(circle 35% at 50% 50%, rgba(236,72,153,0.10), transparent 60%),
        radial-gradient(circle 30% at 15% 85%, rgba(245,211,138,0.09), transparent 60%);
    animation: auroraDrift 30s ease-in-out infinite alternate;
    filter: blur(60px);
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.055 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
    opacity: 0.40;
    pointer-events: none;
    z-index: 1;
    mix-blend-mode: overlay;
    animation: noiseShift 8s steps(6) infinite;
}

.stApp > div[data-testid="stAppViewContainer"] { position: relative; z-index: 3; }

.stApp > div[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: -15%;
    left: 20%;
    width: 900px;
    height: 900px;
    background: radial-gradient(circle, rgba(124,58,237,0.24), transparent 65%);
    filter: blur(80px);
    animation: lightSweep 22s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: -1;
}

.stApp > div[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    bottom: -25%;
    left: 50%;
    transform: translateX(-50%);
    width: 1400px;
    height: 700px;
    background: radial-gradient(ellipse, rgba(245,211,138,0.10), transparent 70%);
    filter: blur(90px);
    animation: softPulse 14s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

.stApp > div[data-testid="stAppViewContainer"] > div::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: radial-gradient(rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: -1;
    opacity: 0.55;
}

.stApp > div[data-testid="stAppViewContainer"] > div::after {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse 90% 80% at 50% 50%, transparent 40%, rgba(0,0,0,0.35) 100%);
    pointer-events: none;
    z-index: 1;
}

.rays-overlay {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    background:
        linear-gradient(115deg, transparent 35%, rgba(201,165,255,0.035) 48%, transparent 60%),
        linear-gradient(115deg, transparent 55%, rgba(56,189,248,0.030) 68%, transparent 78%);
    animation: rayShift 40s ease-in-out infinite alternate;
    mix-blend-mode: screen;
}

.floating-particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
    contain: strict;
}

header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

@keyframes auroraDrift {
    0%   { transform: translate3d(-4%, -2%, 0) rotate(0deg) scale(1); }
    33%  { transform: translate3d(3%, 2%, 0) rotate(5deg) scale(1.07); }
    66%  { transform: translate3d(5%, -3%, 0) rotate(-4deg) scale(1.04); }
    100% { transform: translate3d(-2%, 4%, 0) rotate(2deg) scale(1.06); }
}
@keyframes noiseShift {
    0%   { background-position: 0 0; }
    33%  { background-position: 30px -20px; }
    66%  { background-position: -20px 30px; }
    100% { background-position: 0 0; }
}
@keyframes lightSweep {
    0%   { transform: translate(0, 0) scale(1); opacity: 0.95; }
    50%  { transform: translate(200px, -100px) scale(1.18); opacity: 0.65; }
    100% { transform: translate(-140px, 120px) scale(0.96); opacity: 1; }
}
@keyframes rayShift {
    0%   { background-position: 0 0, 0 0; }
    100% { background-position: 60px -30px, -40px 50px; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(28px); filter: blur(6px); }
    to   { opacity: 1; transform: translateY(0);   filter: blur(0); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes shimmerSweep {
    0%   { background-position: -220% 0; }
    100% { background-position: 220% 0; }
}
@keyframes gradientFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes breathe {
    0%, 100% { box-shadow: 0 0 0 0 rgba(139,92,246,0.35), 0 0 40px rgba(139,92,246,0.30); }
    50%      { box-shadow: 0 0 0 6px rgba(139,92,246,0.0), 0 0 60px rgba(139,92,246,0.55); }
}
@keyframes coreBreathe {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.045); }
}
@keyframes corePulse {
    0%, 100% {
        box-shadow:
            0 0 80px rgba(168,85,247,0.70),
            0 0 160px rgba(245,211,138,0.30),
            0 0 60px rgba(56,189,248,0.45),
            inset 0 0 50px rgba(255,255,255,0.28);
    }
    50% {
        box-shadow:
            0 0 110px rgba(168,85,247,0.95),
            0 0 220px rgba(245,211,138,0.45),
            0 0 80px rgba(56,189,248,0.65),
            inset 0 0 60px rgba(255,255,255,0.40);
    }
}
@keyframes floatY {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-12px); }
}
@keyframes floatYSmall {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
}
@keyframes ringPulse {
    0%   { transform: scale(0.82); opacity: 0.85; }
    100% { transform: scale(2.05); opacity: 0; }
}
@keyframes orbitSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes orbitReverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
@keyframes particleFloat {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
    25%      { transform: translate(10px, -18px) scale(1.15); opacity: 0.85; }
    50%      { transform: translate(-6px, -28px) scale(0.95); opacity: 0.6; }
    75%      { transform: translate(12px, -12px) scale(1.1); opacity: 0.9; }
}
@keyframes particleTwinkle {
    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.7; }
    50%      { transform: scale(1.4) rotate(180deg); opacity: 1; }
}
@keyframes softPulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; } }
@keyframes shine { 0% { left: -130%; } 100% { left: 140%; } }
@keyframes waRing {
    0%   { transform: scale(0.85); opacity: 0.75; }
    100% { transform: scale(1.7);  opacity: 0; }
}

h1, h2, h3, h4, h5, h6 {
    color: var(--white);
    letter-spacing: -0.015em;
    font-weight: 700;
}

.brand-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.70rem;
    font-weight: 600;
    letter-spacing: 0.50em;
    text-transform: uppercase;
    background: linear-gradient(90deg, var(--violet-soft), var(--gold), var(--cyan-soft), var(--violet-soft));
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 9s ease infinite;
    margin-bottom: 1.4rem;
    text-align: center;
    filter: drop-shadow(0 0 18px rgba(201,165,255,0.55));
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: clamp(3.5rem, 7vw, 6.5rem);
    letter-spacing: -0.035em;
    line-height: 0.98;
    margin: 0.4rem 0 0 0;
    text-align: center;
    background: linear-gradient(120deg, #F5D38A 0%, #FFF6D5 18%, #C9A5FF 42%, #7FD0FF 68%, #F5D38A 100%);
    background-size: 320% 320%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 10s ease infinite;
    filter: drop-shadow(0 6px 44px rgba(201,165,255,0.40));
}

.brand-title-sm {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.025em;
    line-height: 1.05;
    margin: 0;
    background: linear-gradient(120deg, #F5D38A 0%, #FFF6D5 20%, #C9A5FF 48%, #7FD0FF 72%, #F5D38A 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 8s ease infinite;
}

.brand-tagline {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 1.45rem;
    color: var(--text-2);
    margin: 1rem auto 0 auto;
    letter-spacing: 0.02em;
    text-align: center;
    animation: fadeUp 1s ease both;
    animation-delay: 0.2s;
}

.brand-tagline-sm {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1rem;
    color: var(--text-2);
    margin-top: 0.4rem;
}

.brand-desc {
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.8;
    max-width: 650px;
    margin: 1.4rem auto 0 auto;
    text-align: center;
    animation: fadeUp 1.1s ease both;
    animation-delay: 0.35s;
}

.hero-stage {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 64vh;
    padding: 1rem 0 1.4rem 0;
    text-align: center;
    animation: fadeUp 1s var(--ease) both;
    position: relative;
}

.ai-core-stage {
    position: relative;
    width: 260px;
    height: 260px;
    margin: 0.6rem auto 1.6rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ai-core-glow {
    position: absolute;
    inset: -70px;
    border-radius: 50%;
    background: radial-gradient(circle,
        rgba(168,85,247,0.42) 0%,
        rgba(56,189,248,0.22) 40%,
        rgba(245,211,138,0.12) 62%,
        transparent 78%);
    filter: blur(36px);
    animation: coreBreathe 7s ease-in-out infinite;
    z-index: 0;
}

.ai-core-ring {
    position: absolute;
    inset: 6px;
    border-radius: 50%;
    border: 1.5px solid rgba(245,211,138,0.58);
    animation: ringPulse 4s ease-out infinite;
    z-index: 1;
    pointer-events: none;
}
.ai-core-ring.r2 { border-color: rgba(201,165,255,0.68); animation-delay: 1.3s; }
.ai-core-ring.r3 { border-color: rgba(56,189,248,0.58);  animation-delay: 2.6s; }

.ai-core-orbit {
    position: absolute;
    inset: -26px;
    border-radius: 50%;
    border: 1px dashed rgba(201,165,255,0.30);
    animation: orbitSpin 22s linear infinite;
    z-index: 4;
    pointer-events: none;
}
.ai-core-orbit-2 {
    inset: -46px;
    border-style: dotted;
    border-color: rgba(56,189,248,0.24);
    animation: orbitReverse 32s linear infinite;
}
.ai-core-orbit::before,
.ai-core-orbit::after {
    content: "✦";
    position: absolute;
    color: var(--gold);
    font-size: 1.10rem;
    text-shadow: 0 0 16px rgba(245,211,138,1);
    animation: particleTwinkle 3.4s ease-in-out infinite;
}
.ai-core-orbit::before { top: -9px; left: 50%; transform: translateX(-50%); }
.ai-core-orbit::after  { bottom: -9px; left: 50%; transform: translateX(-50%); animation-delay: 1.7s; }
.ai-core-orbit-2::before {
    content: "◆"; color: var(--cyan-soft);
    text-shadow: 0 0 16px rgba(127,208,255,1);
    top: 50%; left: -8px; transform: translateY(-50%);
}
.ai-core-orbit-2::after {
    content: "•"; color: var(--violet-soft); font-size: 1.5rem;
    text-shadow: 0 0 16px rgba(201,165,255,1);
    top: 50%; left: auto; right: -8px; transform: translateY(-50%);
    bottom: auto; animation-delay: 0.9s;
}

.ai-core-shell {
    position: absolute;
    inset: 20px;
    border-radius: 50%;
    background:
        radial-gradient(circle at 32% 28%, rgba(255,255,255,0.16) 0%, rgba(201,165,255,0.06) 30%, transparent 55%),
        radial-gradient(circle at 70% 78%, rgba(56,189,248,0.10) 0%, transparent 45%);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow:
        inset 0 0 40px rgba(255,255,255,0.06),
        inset 0 0 20px rgba(168,85,247,0.20);
    z-index: 2;
    backdrop-filter: blur(2px);
}

.ai-core {
    position: absolute;
    inset: 42px;
    border-radius: 50%;
    background: radial-gradient(circle at 34% 30%,
        #FFE9B8 0%, #F5D38A 14%, #A855F7 48%, #6D28D9 76%, #1e1b4b 100%);
    box-shadow:
        0 0 80px rgba(168,85,247,0.70),
        0 0 160px rgba(245,211,138,0.30),
        0 0 60px rgba(56,189,248,0.40),
        inset 0 0 50px rgba(255,255,255,0.28),
        inset -14px -14px 50px rgba(0,0,0,0.45);
    animation: floatY 5.5s ease-in-out infinite, corePulse 6s ease-in-out infinite;
    z-index: 3;
    overflow: hidden;
}

.ai-core-highlight {
    position: absolute;
    inset: 18%;
    border-radius: 50%;
    background: radial-gradient(circle at 40% 35%,
        rgba(255,255,255,0.80), rgba(255,246,213,0.20) 45%, transparent 70%);
    filter: blur(10px);
    animation: softPulse 3.5s ease-in-out infinite;
    z-index: 4;
    pointer-events: none;
}

.ai-core-diamond {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 6;
    animation: floatYSmall 3.6s ease-in-out infinite;
}
.ai-core-diamond svg {
    width: 54px; height: 54px;
    filter:
        drop-shadow(0 0 20px rgba(255,246,213,1))
        drop-shadow(0 0 34px rgba(201,165,255,0.85))
        drop-shadow(0 6px 20px rgba(0,0,0,0.55));
}

.ai-core-particle {
    position: absolute;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--gold);
    box-shadow: 0 0 12px rgba(245,211,138,1);
    animation: particleFloat 7s ease-in-out infinite;
    z-index: 5;
}
.ai-core-particle.p1 { top: -6%;  left: 22%;  animation-delay: 0s; }
.ai-core-particle.p2 { top: 26%;  left: -10%; animation-delay: 1.2s; background: var(--cyan-soft); box-shadow: 0 0 12px rgba(127,208,255,1); }
.ai-core-particle.p3 { top: 72%;  left: 108%; animation-delay: 2.4s; }
.ai-core-particle.p4 { top: 106%; left: 30%;  animation-delay: 3.6s; background: var(--violet-soft); box-shadow: 0 0 12px rgba(201,165,255,1); }
.ai-core-particle.p5 { top: 50%;  left: 112%; animation-delay: 0.9s; }
.ai-core-particle.p6 { top: -4%;  left: 76%;  animation-delay: 2.1s; background: var(--violet-soft); box-shadow: 0 0 12px rgba(201,165,255,1); }

.pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    justify-content: center;
    margin: 2rem auto 0 auto;
    max-width: 720px;
}

.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(139,92,246,0.16) 0%, rgba(56,189,248,0.10) 100%);
    color: #DCD6FF;
    border: 1px solid rgba(201,165,255,0.32);
    border-radius: 999px;
    padding: 0.65rem 1.30rem;
    font-size: 0.86rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 18px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.04) inset;
    transition: transform 0.3s var(--ease), box-shadow 0.3s ease, border-color 0.3s ease, color 0.3s ease;
    animation: fadeUp 0.7s var(--ease) both;
    user-select: none;
    white-space: nowrap;
}
.pill:nth-child(1) { animation-delay: 0.55s; }
.pill:nth-child(2) { animation-delay: 0.68s; }
.pill:nth-child(3) { animation-delay: 0.81s; }
.pill:nth-child(4) { animation-delay: 0.94s; }

.pill:hover {
    transform: translateY(-4px) scale(1.03);
    border-color: rgba(245,211,138,0.78);
    color: var(--gold-soft);
    box-shadow:
        0 14px 34px rgba(245,211,138,0.22),
        0 0 34px rgba(168,85,247,0.38),
        0 0 0 1px rgba(245,211,138,0.18) inset;
}

.panel-card {
    position: relative;
    background: linear-gradient(180deg, rgba(15,18,38,0.72) 0%, rgba(8,10,22,0.72) 100%);
    backdrop-filter: blur(28px) saturate(150%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 30px;
    padding: 2.4rem 2.2rem;
    box-shadow:
        0 30px 80px rgba(0,0,0,0.65),
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 0 100px rgba(124,58,237,0.14);
    animation: fadeUp 0.9s var(--ease) both;
    overflow: hidden;
    max-width: 780px;
    margin: 0 auto;
}

.panel-card::before {
    content: "";
    position: absolute;
    top: -1px; left: 10%;
    width: 80%; height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(201,165,255,0.85),
        rgba(56,189,248,0.85),
        rgba(201,165,255,0.85),
        transparent);
    filter: blur(0.6px);
    animation: softPulse 4s ease-in-out infinite;
}

.panel-title {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 1.65rem;
    letter-spacing: -0.015em;
    text-align: center;
    background: linear-gradient(120deg, var(--gold-soft), var(--violet-soft), var(--cyan-soft));
    background-size: 260% 260%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 9s ease infinite;
    margin-bottom: 0.4rem;
}

.panel-sub {
    text-align: center;
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 1.6rem;
    letter-spacing: 0.01em;
}

.wa-card {
    position: relative;
    margin-top: 1.6rem;
    background: linear-gradient(180deg, rgba(15, 30, 25, 0.55) 0%, rgba(8, 15, 20, 0.55) 100%);
    border: 1px solid rgba(37, 211, 102, 0.28);
    border-radius: 24px;
    padding: 1.6rem 1.6rem 1.3rem 1.6rem;
    backdrop-filter: blur(26px) saturate(150%);
    box-shadow:
        0 22px 60px rgba(0,0,0,0.55),
        0 0 0 1px rgba(37,211,102,0.10) inset,
        0 0 90px rgba(37,211,102,0.10);
    animation: fadeUp 0.9s var(--ease) both;
    overflow: hidden;
    isolation: isolate;
}

.wa-card::before {
    content: "";
    position: absolute;
    top: -1px; left: 14%;
    width: 72%; height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(37,211,102,0.95) 40%,
        rgba(180,255,215,1) 50%,
        rgba(37,211,102,0.95) 60%,
        transparent);
    filter: blur(0.5px);
    animation: softPulse 4s ease-in-out infinite;
}

.wa-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(115deg,
        transparent 30%, rgba(255,255,255,0.05) 46%,
        rgba(37,211,102,0.10) 50%,
        rgba(255,255,255,0.05) 54%, transparent 70%);
    background-size: 240% 100%;
    animation: shimmerSweep 9s ease-in-out infinite;
    pointer-events: none;
    border-radius: inherit;
    z-index: 1;
}

.wa-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}

.wa-icon {
    position: relative;
    width: 44px;
    height: 44px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(37,211,102,0.22) 0%, rgba(20,180,80,0.10) 100%);
    border: 1px solid rgba(37,211,102,0.35);
    box-shadow:
        0 8px 22px rgba(37,211,102,0.25),
        0 0 0 1px rgba(255,255,255,0.04) inset;
    font-size: 1.35rem;
    flex-shrink: 0;
    animation: softPulse 3s ease-in-out infinite;
}

.wa-icon::before {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 18px;
    border: 1px solid rgba(37,211,102,0.45);
    animation: waRing 2.8s ease-out infinite;
    pointer-events: none;
}

.wa-icon::after {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 18px;
    border: 1px solid rgba(180,255,215,0.35);
    animation: waRing 2.8s ease-out infinite;
    animation-delay: 1.4s;
    pointer-events: none;
}

.wa-title {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--white);
    letter-spacing: -0.01em;
    line-height: 1.2;
}

.wa-sub {
    color: var(--muted);
    font-size: 0.83rem;
    margin-top: 0.15rem;
    letter-spacing: 0.01em;
}

.wa-sub b { color: #B4FFD7; font-weight: 600; }

.wa-user {
    margin-top: 1rem;
    padding-top: 0.9rem;
    border-top: 1px solid rgba(37,211,102,0.14);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.80rem;
    color: var(--muted);
    letter-spacing: 0.02em;
    position: relative;
    z-index: 2;
}

.wa-user b { color: var(--gold); font-weight: 600; letter-spacing: 0.02em; }
.wa-user .dot { color: rgba(37,211,102,0.6); margin: 0 0.15rem; }

.stButton > button {
    position: relative;
    background: linear-gradient(135deg, #6D28D9 0%, #8B5CF6 35%, #A855F7 62%, #38BDF8 100%);
    background-size: 200% 200%;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 16px;
    padding: 0.95rem 1.8rem;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    transition:
        transform 0.3s var(--ease),
        box-shadow 0.3s ease,
        filter 0.3s ease,
        background-position 0.6s ease;
    box-shadow:
        0 14px 36px rgba(139,92,246,0.42),
        0 0 0 1px rgba(255,255,255,0.06) inset,
        0 0 40px rgba(168,85,247,0.22);
    overflow: hidden;
    isolation: isolate;
}

.stButton > button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -130%;
    width: 55%;
    height: 100%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,0.45), transparent);
    animation: shine 5.5s ease-in-out infinite;
    animation-delay: 1s;
    pointer-events: none;
    z-index: 1;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.015);
    background-position: 100% 50%;
    box-shadow:
        0 24px 60px rgba(139,92,246,0.65),
        0 0 50px rgba(245,211,138,0.28),
        0 0 0 1px rgba(255,255,255,0.14) inset;
    filter: brightness(1.12);
}

.stButton > button:active { transform: translateY(-1px) scale(0.99); }

.stButton > button:focus {
    outline: none;
    box-shadow:
        0 0 0 4px rgba(168,85,247,0.40),
        0 14px 36px rgba(139,92,246,0.55);
}

.stButton > button:disabled {
    opacity: 0.42;
    cursor: not-allowed;
    filter: grayscale(0.55);
    box-shadow: none;
}
.stButton > button:disabled:hover { transform: none; filter: grayscale(0.55); }
.stButton > button:disabled::before { display: none; }

.stTextInput > div > div > input {
    height: 58px !important;
    background: rgba(255,255,255,0.035) !important;
    color: var(--white) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 16px !important;
    padding: 0 1.15rem !important;
    font-size: 0.98rem !important;
    font-weight: 400 !important;
    transition: all 0.32s var(--ease) !important;
    box-shadow:
        0 6px 22px rgba(0,0,0,0.40) inset,
        0 0 0 0 rgba(168,85,247,0) !important;
    backdrop-filter: blur(16px);
}

.stTextInput > div > div > input::placeholder { color: #475569 !important; font-weight: 400 !important; }
.stTextInput > div > div > input:hover { border-color: rgba(201,165,255,0.35) !important; }
.stTextInput > div > div > input:focus {
    border-color: rgba(201,165,255,0.85) !important;
    box-shadow:
        0 0 0 4px rgba(139,92,246,0.22),
        0 6px 22px rgba(0,0,0,0.40) inset,
        0 0 36px rgba(168,85,247,0.30) !important;
    background: rgba(20, 22, 44, 0.95) !important;
    outline: none !important;
}

.stTextInput label,
.stTextInput label p {
    color: var(--text-2) !important;
    font-weight: 600 !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.16em !important;
    margin-bottom: 0.5rem !important;
    text-transform: uppercase;
}

[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

[data-testid="stChatMessage"] {
    background: linear-gradient(180deg, rgba(24,27,54,0.60) 0%, rgba(12,14,32,0.60) 100%);
    border: 1px solid rgba(255,255,255,0.075);
    border-radius: 22px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(22px);
    box-shadow:
        0 14px 38px rgba(0,0,0,0.40),
        0 0 0 1px rgba(255,255,255,0.02) inset;
    animation: fadeUp 0.55s var(--ease) both;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

[data-testid="stChatMessage"]:hover {
    transform: translateY(-2px);
    border-color: rgba(201,165,255,0.32);
    box-shadow:
        0 20px 50px rgba(0,0,0,0.50),
        0 0 44px rgba(139,92,246,0.24);
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(109,40,217,0.26) 0%, rgba(56,189,248,0.14) 100%);
    border-color: rgba(201,165,255,0.32);
    box-shadow:
        0 16px 42px rgba(0,0,0,0.50),
        0 0 46px rgba(139,92,246,0.24);
}

[data-testid="stChatInput"] {
    background: rgba(8, 10, 24, 0.96) !important;
    border: 1px solid rgba(201,165,255,0.42) !important;
    border-radius: 22px !important;
    animation: breathe 6s ease-in-out infinite;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(245,211,138,0.80) !important;
    box-shadow:
        0 0 0 4px rgba(245,211,138,0.16),
        0 0 46px rgba(168,85,247,0.35) !important;
}

[data-testid="stChatInput"] textarea { color: var(--white) !important; font-size: 0.98rem !important; }

hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(201,165,255,0.45) 30%,
        rgba(245,211,138,0.45) 50%,
        rgba(201,165,255,0.45) 70%,
        transparent);
    margin: 2.2rem 0;
    opacity: 0.7;
}

.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
}

.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(180deg, rgba(23,26,52,0.82) 0%, rgba(12,14,32,0.82) 100%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 0.65rem 1.1rem;
    font-size: 0.84rem;
    color: var(--text-2);
    letter-spacing: 0.015em;
    backdrop-filter: blur(18px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    transition: transform 0.3s var(--ease), border-color 0.3s ease, box-shadow 0.3s ease;
    animation: fadeUp 0.8s ease both;
}
.stat-chip:nth-child(1) { animation-delay: 0.05s; }
.stat-chip:nth-child(2) { animation-delay: 0.12s; }
.stat-chip:nth-child(3) { animation-delay: 0.19s; }
.stat-chip:nth-child(4) { animation-delay: 0.26s; }

.stat-chip:hover {
    transform: translateY(-2px);
    border-color: rgba(201,165,255,0.42);
    box-shadow:
        0 14px 34px rgba(139,92,246,0.26),
        0 0 24px rgba(245,211,138,0.12);
}

.stat-chip b { color: var(--gold); font-weight: 600; letter-spacing: 0.01em; }

[data-testid="stChatMessage"] img {
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.10);
    animation: fadeIn 0.7s ease both;
    transition: transform 0.4s var(--ease), box-shadow 0.4s ease;
    box-shadow: 0 14px 36px rgba(0,0,0,0.45);
}

[data-testid="stChatMessage"] img:hover {
    transform: scale(1.015);
    box-shadow:
        0 22px 60px rgba(139,92,246,0.40),
        0 0 46px rgba(245,211,138,0.18);
}

.stSpinner > div {
    border-top-color: var(--violet-soft) !important;
    border-right-color: var(--gold) !important;
    border-bottom-color: var(--purple) !important;
}

[data-testid="stAlert"] {
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    backdrop-filter: blur(18px);
    animation: fadeUp 0.5s ease both;
}

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--purple), var(--violet));
    border-radius: 6px;
    border: 2px solid transparent;
    background-clip: padding-box;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, var(--violet), var(--gold));
    background-clip: padding-box;
}

.lux-footer {
    text-align: center;
    color: var(--muted-2);
    font-size: 0.84rem;
    letter-spacing: 0.20em;
    text-transform: uppercase;
    padding: 2rem 0 1.4rem 0;
    animation: fadeIn 1.4s ease both;
    font-weight: 500;
}

.lux-footer .gold {
    color: var(--gold);
    font-weight: 600;
    letter-spacing: 0.20em;
    text-shadow: 0 0 20px rgba(245,211,138,0.55);
    display: inline-block;
    animation: softPulse 3s ease-in-out infinite;
}

.fp {
    position: absolute;
    color: var(--gold);
    opacity: 0.35;
    font-size: 0.9rem;
    text-shadow: 0 0 14px rgba(245,211,138,0.9);
    animation: particleFloat 14s ease-in-out infinite;
    will-change: transform, opacity;
}

.fp-1  { top: 12%; left: 6%;  animation-duration: 16s; animation-delay: 0s;    color: var(--violet-soft); font-size: 0.7rem; }
.fp-2  { top: 18%; left: 94%; animation-duration: 18s; animation-delay: 2s;    color: var(--cyan-soft);   font-size: 1rem;   }
.fp-3  { top: 74%; left: 4%;  animation-duration: 20s; animation-delay: 4s;    color: var(--gold);        font-size: 0.8rem; }
.fp-4  { top: 82%; left: 90%; animation-duration: 17s; animation-delay: 1s;    color: var(--violet-soft); font-size: 0.9rem; }
.fp-5  { top: 42%; left: 2%;  animation-duration: 22s; animation-delay: 3s;    color: var(--cyan-soft);   font-size: 0.65rem;}
.fp-6  { top: 58%; left: 96%; animation-duration: 19s; animation-delay: 5s;    color: var(--gold);        font-size: 0.75rem;}
.fp-7  { top: 6%;  left: 50%; animation-duration: 21s; animation-delay: 6s;    color: var(--gold-soft);   font-size: 0.85rem;}
.fp-8  { top: 92%; left: 45%; animation-duration: 15s; animation-delay: 2.5s;  color: var(--violet-soft); font-size: 0.7rem; }
.fp-9  { top: 32%; left: 46%; animation-duration: 24s; animation-delay: 7s;    color: var(--cyan-soft);   font-size: 0.6rem; }
.fp-10 { top: 88%; left: 62%; animation-duration: 23s; animation-delay: 8s;    color: var(--gold);        font-size: 0.8rem; }
.fp-11 { top: 24%; left: 20%; animation-duration: 25s; animation-delay: 4.5s;  color: var(--violet-soft); font-size: 0.55rem;}
.fp-12 { top: 66%; left: 78%; animation-duration: 26s; animation-delay: 6.5s;  color: var(--gold-soft);   font-size: 0.65rem;}
.fp-13 { top: 4%;  left: 30%; animation-duration: 20s; animation-delay: 3.5s;  color: var(--cyan-soft);   font-size: 0.7rem; }
.fp-14 { top: 44%; left: 90%; animation-duration: 27s; animation-delay: 9s;    color: var(--gold);        font-size: 0.6rem; }
.fp-15 { top: 78%; left: 30%; animation-duration: 24s; animation-delay: 5.5s;  color: var(--violet-soft); font-size: 0.75rem;}
.fp-16 { top: 14%; left: 66%; animation-duration: 22s; animation-delay: 1.5s;  color: var(--cyan-soft);   font-size: 0.65rem;}
.fp-17 { top: 60%; left: 14%; animation-duration: 26s; animation-delay: 7.5s;  color: var(--gold-soft);   font-size: 0.55rem;}
.fp-18 { top: 96%; left: 20%; animation-duration: 19s; animation-delay: 4.2s;  color: var(--violet-soft); font-size: 0.7rem; }
.fp-19 { top: 36%; left: 78%; animation-duration: 23s; animation-delay: 8.8s;  color: var(--gold);        font-size: 0.65rem;}
.fp-20 { top: 52%; left: 62%; animation-duration: 25s; animation-delay: 6.2s;  color: var(--cyan-soft);   font-size: 0.55rem;}

@media (max-width: 1440px) {
    .ai-core-stage { width: 240px; height: 240px; }
    .ai-core-diamond svg { width: 50px; height: 50px; }
}

@media (max-width: 1280px) {
    .ai-core-stage { width: 220px; height: 220px; }
    .ai-core-diamond svg { width: 46px; height: 46px; }
    .panel-card { padding: 2.2rem 2rem; }
}

@media (max-width: 1024px) {
    .brand-title { font-size: 4.2rem; }
    .brand-title-sm { font-size: 2.1rem; }
    .brand-tagline { font-size: 1.25rem; }
    .ai-core-stage { width: 200px; height: 200px; }
    .ai-core-diamond svg { width: 42px; height: 42px; }
    .panel-card { padding: 2rem 1.8rem; border-radius: 26px; }
    .hero-stage { min-height: 58vh; }
}

@media (max-width: 768px) {
    .brand-title { font-size: 3.4rem; }
    .brand-title-sm { font-size: 1.9rem; }
    .brand-tagline { font-size: 1.15rem; }
    .brand-desc { font-size: 0.98rem; }
    .brand-eyebrow { font-size: 0.62rem; letter-spacing: 0.36em; }
    .ai-core-stage { width: 180px; height: 180px; margin-bottom: 1.2rem; }
    .ai-core-diamond svg { width: 38px; height: 38px; }
    .ai-core-orbit { inset: -18px; }
    .ai-core-orbit-2 { inset: -34px; }
    .panel-card { padding: 1.9rem 1.5rem; border-radius: 24px; }
    .panel-title { font-size: 1.4rem; }
    .panel-sub { font-size: 0.85rem; }
    .wa-card { padding: 1.3rem 1.2rem 1.1rem 1.2rem; border-radius: 20px; }
    .wa-title { font-size: 1.02rem; }
    .wa-icon { width: 40px; height: 40px; font-size: 1.2rem; }
    .pills-row { gap: 0.5rem; margin-top: 1.6rem; }
    .pill { font-size: 0.78rem; padding: 0.5rem 1rem; }
    .stButton > button { width: 100%; padding: 0.85rem 1.2rem; }
    .hero-stage { min-height: auto; padding-bottom: 1.2rem; }
    hr { margin: 1.6rem 0; }
}

@media (max-width: 480px) {
    .brand-title { font-size: 2.7rem; }
    .brand-title-sm { font-size: 1.7rem; }
    .brand-tagline { font-size: 1.02rem; margin-top: 0.7rem; }
    .brand-desc { font-size: 0.92rem; line-height: 1.7; padding: 0 0.4rem; }
    .brand-eyebrow { font-size: 0.56rem; letter-spacing: 0.30em; margin-bottom: 0.9rem; }
    .ai-core-stage { width: 150px; height: 150px; margin-bottom: 1rem; }
    .ai-core-diamond svg { width: 32px; height: 32px; }
    .ai-core-orbit { inset: -14px; }
    .ai-core-orbit-2 { inset: -26px; }
    .ai-core-orbit::before, .ai-core-orbit::after { font-size: 0.8rem; }
    .panel-card { padding: 1.6rem 1.2rem; border-radius: 20px; margin: 0 0.2rem; }
    .panel-title { font-size: 1.2rem; }
    .wa-card { padding: 1.15rem 1.05rem 1rem 1.05rem; border-radius: 18px; }
    .wa-title { font-size: 0.96rem; }
    .wa-icon { width: 38px; height: 38px; font-size: 1.1rem; border-radius: 12px; }
    .wa-user { font-size: 0.74rem; }
    .pills-row { gap: 0.4rem; margin-top: 1.2rem; max-width: 100%; }
    .pill { font-size: 0.72rem; padding: 0.42rem 0.85rem; }
    .stat-chip { font-size: 0.78rem; padding: 0.5rem 0.85rem; }
    .chips-row { gap: 0.45rem; }
    .lux-footer { font-size: 0.72rem; letter-spacing: 0.14em; padding: 1.4rem 0 1rem 0; }
    .stTextInput > div > div > input {
        height: 54px !important;
        padding: 0 1rem !important;
        font-size: 0.94rem !important;
    }
    [data-testid="stChatMessage"] { padding: 1rem 1.05rem; border-radius: 18px; }
    hr { margin: 1.2rem 0; }
}

@media (max-width: 390px) {
    .brand-title { font-size: 2.3rem; }
    .brand-title-sm { font-size: 1.55rem; }
    .brand-tagline { font-size: 0.94rem; }
    .ai-core-stage { width: 132px; height: 132px; }
    .ai-core-diamond svg { width: 28px; height: 28px; }
    .panel-card { padding: 1.4rem 1rem; border-radius: 18px; }
}

@media (max-width: 360px) {
    .brand-title { font-size: 2rem; }
    .brand-title-sm { font-size: 1.45rem; }
    .brand-desc { font-size: 0.88rem; }
    .pill { font-size: 0.68rem; padding: 0.36rem 0.75rem; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
    }
    .stApp::before,
    .stApp::after,
    .stApp > div[data-testid="stAppViewContainer"]::before,
    .stApp > div[data-testid="stAppViewContainer"]::after,
    .floating-particles,
    .rays-overlay {
        animation: none !important;
        opacity: 0.12 !important;
    }
    .ai-core,
    .ai-core-glow,
    .ai-core-highlight,
    .ai-core-diamond,
    .wa-icon {
        animation: none !important;
    }
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 1rem !important;
    max-width: 1240px !important;
}
</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# BACKGROUND OVERLAYS
# ============================================================

html(
    """
    <div class="rays-overlay" aria-hidden="true"></div>

    <div class="floating-particles" aria-hidden="true">
        <span class="fp fp-1">✦</span>
        <span class="fp fp-2">◆</span>
        <span class="fp fp-3">·</span>
        <span class="fp fp-4">✦</span>
        <span class="fp fp-5">•</span>
        <span class="fp fp-6">◆</span>
        <span class="fp fp-7">✦</span>
        <span class="fp fp-8">·</span>
        <span class="fp fp-9">•</span>
        <span class="fp fp-10">✦</span>
        <span class="fp fp-11">·</span>
        <span class="fp fp-12">◆</span>
        <span class="fp fp-13">✦</span>
        <span class="fp fp-14">•</span>
        <span class="fp fp-15">·</span>
        <span class="fp fp-16">◆</span>
        <span class="fp fp-17">✦</span>
        <span class="fp fp-18">·</span>
        <span class="fp fp-19">•</span>
        <span class="fp fp-20">✦</span>
    </div>
    """
)


# ============================================================
# LOAD SECRETS
# ============================================================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
    TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]
    TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]
except Exception as error:
    st.error("❌ **Configuration Error**")
    st.warning("Please check your `.streamlit/secrets.toml` file.")
    st.code(str(error))
    st.stop()


# ============================================================
# CLIENTS
# ============================================================

MODEL_NAME = "gemini-2.5-flash"


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


@st.cache_resource
def get_twilio_client():
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


gemini_client = get_gemini_client()
twilio_client = get_twilio_client()


# ============================================================
# SESSION STATE
# ============================================================

for key, value in {
    "onboarded": False,
    "name": "",
    "whatsapp_number": "",
    "chat": None,
    "messages": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPERS
# ============================================================

def add_message(role, kind, content):
    st.session_state.messages.append(
        {"role": role, "kind": kind, "content": content}
    )


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(
                message["content"],
                caption="📷 Uploaded study material",
                use_container_width=True,
            )


# ------------------------------------------------------------
# GEMINI CALL — WITH RETRY ON TRANSIENT ERRORS
# ------------------------------------------------------------
# Gemini occasionally returns 503 UNAVAILABLE under load or
# 429 RESOURCE_EXHAUSTED for rate limits. Both are transient.
# We retry up to 3 times with exponential backoff. Anything
# else raises immediately.
# ------------------------------------------------------------

TRANSIENT_GEMINI_PATTERNS = (
    "503",
    "unavailable",
    "high demand",
    "429",
    "resource_exhausted",
    "resource exhausted",
    "rate limit",
    "deadline_exceeded",
    "deadline exceeded",
    "overloaded",
)


def _is_transient_gemini_error(error: Exception) -> bool:
    text = str(error).lower()
    return any(p in text for p in TRANSIENT_GEMINI_PATTERNS)


def ask_gemini(parts, max_retries: int = 3):
    """
    Send content to Gemini with retry logic for transient errors.

    Returns:
        (True, text)                on success
        (False, friendly_message)   on failure
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            response = st.session_state.chat.send_message(parts)
            if response.text:
                return True, response.text
            # Empty response is technically a failure
            last_error = "Gemini returned an empty response."
        except Exception as e:
            last_error = e
            if _is_transient_gemini_error(e) and attempt < max_retries - 1:
                # Exponential backoff: 2s, 4s, 8s
                time.sleep(2 * (attempt + 1))
                continue
            break

    return False, (
        "⚠️ **Gemini is temporarily busy.** "
        "Please try again in a moment."
    )


def clean_whatsapp_text(text):
    if not text:
        return "No study summary available."
    text = " ".join(text.split())
    if len(text) > 1500:
        text = text[:1500] + "..."
    return text


# ------------------------------------------------------------
# TWILIO — TRIAL-AWARE ERROR MAPPING
# ------------------------------------------------------------

TRIAL_LIMITATION_CODES = {63018, 21660, 21661}

TWILIO_ERROR_HINTS = {
    21610: "The recipient number is the same as the sender number. Use a different recipient.",
    21211: "The recipient number is invalid. Use E.164 format, e.g. +919014226168.",
    21606: "The sender number isn't a valid Twilio WhatsApp sender. Check TWILIO_WHATSAPP_FROM.",
    21656: "The WhatsApp template needs variables that weren't sent. Twilio requires {{1}} and {{2}}.",
    21654: "The variables don't match the template's placeholders.",
    21652: "Too many variables were sent for this template.",
    63003: "The recipient hasn't joined your Twilio WhatsApp Sandbox yet.",
    63007: "The WhatsApp sender isn't fully approved. Complete verification in Twilio Console.",
    63016: "Free-form messages can only be sent within 24 hours of the user's last reply.",
    20003: "Authentication failed. Your Twilio Account SID or Auth Token is wrong or has been rotated.",
    20404: "The Content Template SID was not found. Check TWILIO_CONTENT_SID.",
    14107: "Message body exceeded the maximum length. Shorten the summary.",
}


def _detect_trial_restriction(error: Exception) -> bool:
    msg = (str(error) or "").lower()
    if "trial" in msg and (
        "limited parameter" in msg
        or "upgrade" in msg
        or "not able to send" in msg
    ):
        return True
    if isinstance(error, TwilioRestException):
        code = getattr(error, "code", None)
        if code in TRIAL_LIMITATION_CODES:
            return True
    return False


def format_twilio_error(error: Exception) -> str:
    if _detect_trial_restriction(error):
        return (
            "**📲 WhatsApp couldn't send the summary.**\n\n"
            "Your Twilio account is currently in **Trial mode**, which only "
            "allows **Twilio-provided WhatsApp templates** and a limited set "
            "of parameters. Custom templates are not permitted on trial accounts.\n\n"
            "**To send the full Gemini study summary, you need to either:**\n\n"
            "1. Upgrade your Twilio account (Console → Billing), **or**\n"
            "2. Switch `TWILIO_CONTENT_SID` in `secrets.toml` to a "
            "Twilio-provided trial template SID from Twilio Console → "
            "Messaging → Content Template Builder → Samples."
        )

    if isinstance(error, TwilioRestException):
        code = getattr(error, "code", None)
        raw_msg = getattr(error, "msg", str(error)) or ""
        if code in TWILIO_ERROR_HINTS:
            return (
                f"**📲 WhatsApp couldn't send the summary.**\n\n"
                f"{TWILIO_ERROR_HINTS[code]}\n\n"
                f"*Twilio code: {code}*"
            )
        return (
            f"**📲 WhatsApp couldn't send the summary.**\n\n"
            f"{raw_msg}\n\n"
            f"*Twilio code: {code}*"
        )

    return (
        "**📲 WhatsApp couldn't send the summary.**\n\n"
        f"{str(error)}\n\n"
        "*Please check your Twilio configuration and try again.*"
    )


def send_whatsapp(to_number, user_name, summary):
    """
    Send study summary via Twilio WhatsApp Content Template.
    Only trial-safe parameters are sent.
    """
    try:
        content_variables = json.dumps(
            {"1": user_name, "2": clean_whatsapp_text(summary)},
            ensure_ascii=False,
        )
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to_number}",
            content_sid=TWILIO_CONTENT_SID,
            content_variables=content_variables,
        )
        return True, message.sid

    except TwilioRestException as e:
        return False, format_twilio_error(e)
    except Exception as e:
        return False, format_twilio_error(e)


# ============================================================
# ONBOARDING — ULTRA PREMIUM HERO
# ============================================================

if not st.session_state.onboarded:

    html(
        """
        <div class="hero-stage">
            <div class="brand-eyebrow">✦ — Premium Study Companion — ✦</div>

            <div class="ai-core-stage">
                <div class="ai-core-glow"></div>
                <div class="ai-core-ring r3"></div>
                <div class="ai-core-ring r2"></div>
                <div class="ai-core-ring"></div>
                <div class="ai-core-orbit-2"></div>
                <div class="ai-core-orbit"></div>
                <div class="ai-core-shell"></div>
                <div class="ai-core"></div>
                <div class="ai-core-highlight"></div>

                <div class="ai-core-diamond">
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <defs>
                            <linearGradient id="gemGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%"  stop-color="#FFF6D5"/>
                                <stop offset="35%" stop-color="#F5D38A"/>
                                <stop offset="70%" stop-color="#C9A5FF"/>
                                <stop offset="100%" stop-color="#7FD0FF"/>
                            </linearGradient>
                        </defs>
                        <polygon points="50,8 82,38 68,90 32,90 18,38"
                                 fill="url(#gemGrad)"
                                 stroke="rgba(255,255,255,0.65)"
                                 stroke-width="1.4"
                                 stroke-linejoin="round"/>
                        <polyline points="18,38 32,50 50,38 68,50 82,38"
                                  fill="none"
                                  stroke="rgba(255,255,255,0.55)"
                                  stroke-width="1.2"
                                  stroke-linejoin="round"/>
                        <line x1="50" y1="8"  x2="50" y2="38" stroke="rgba(255,255,255,0.45)" stroke-width="1"/>
                        <line x1="50" y1="38" x2="50" y2="90" stroke="rgba(255,255,255,0.35)" stroke-width="1"/>
                    </svg>
                </div>

                <span class="ai-core-particle p1"></span>
                <span class="ai-core-particle p2"></span>
                <span class="ai-core-particle p3"></span>
                <span class="ai-core-particle p4"></span>
                <span class="ai-core-particle p5"></span>
                <span class="ai-core-particle p6"></span>
            </div>

            <h1 class="brand-title">StudySnap&nbsp;AI</h1>
            <p class="brand-tagline">Snap it · Understand it · Master it</p>
            <p class="brand-desc">
                Upload a question, textbook page, handwritten note,
                diagram, equation, or code.
                StudySnap turns it into a clear, step-by-step
                explanation in simple English.
            </p>

            <div class="pills-row">
                <span class="pill">✦ AI Explanations</span>
                <span class="pill">◈ Image Analysis</span>
                <span class="pill">⌁ WhatsApp Summary</span>
                <span class="pill">◎ Step-by-Step</span>
            </div>
        </div>
        """
    )

    left, center, right = st.columns([1, 2.6, 1])

    with center:

        html(
            """
            <div class="panel-card">
                <div class="panel-title">Begin Your Study Journey</div>
                <div class="panel-sub">Your personal AI study chamber is ready.</div>
            </div>
            """
        )

        with st.form("onboarding_form", clear_on_submit=False):

            name = st.text_input(
                "Your Name",
                placeholder="Enter your name",
            )

            whatsapp_number = st.text_input(
                "WhatsApp Number",
                placeholder="+91XXXXXXXXXX",
                help="Use the number that joined your Twilio WhatsApp Sandbox.",
            )

            html("<div style='height: 0.5rem;'></div>")

            submitted = st.form_submit_button(
                "✦  Begin Your Journey",
                use_container_width=True,
            )

        if submitted:
            if not name.strip():
                st.warning("⚠️ Please enter your name.")
            elif not whatsapp_number.strip():
                st.warning("⚠️ Please enter your WhatsApp number.")
            else:
                st.session_state.name = name.strip()
                st.session_state.whatsapp_number = whatsapp_number.strip()

                st.session_state.chat = gemini_client.chats.create(
                    model=MODEL_NAME,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    ),
                )

                st.session_state.messages = []
                st.session_state.onboarded = True

                with st.spinner("✦  Preparing your study chamber..."):
                    time.sleep(0.8)

                st.rerun()

    st.stop()


# ============================================================
# MAIN HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 2],
    vertical_alignment="center",
)

with header_left:
    html(
        f"""
        <div class="brand-eyebrow" style="text-align:left; margin-bottom: 0.4rem;">✦ — Study Chamber — ✦</div>
        <div class="brand-title-sm">StudySnap&nbsp;AI</div>
        <div class="brand-tagline-sm">
            Welcome back, <b style="color:#F5D38A;">{st.session_state.name}</b>
            — your personal study atelier.
        </div>
        """
    )

with header_right:
    st.empty()


# ============================================================
# STAT CHIPS
# ============================================================

html(
    f"""
    <div class="chips-row">
        <div class="stat-chip">📱 <b>Destination</b>&nbsp;·&nbsp;{st.session_state.whatsapp_number}</div>
        <div class="stat-chip">💬 <b>Messages</b>&nbsp;·&nbsp;{len(st.session_state.messages)}</div>
        <div class="stat-chip">⚡ <b>Engine</b>&nbsp;·&nbsp;{MODEL_NAME}</div>
        <div class="stat-chip">✦ <b>Status</b>&nbsp;·&nbsp;Ready</div>
    </div>
    """
)

st.divider()


# ============================================================
# WELCOME MESSAGE
# ============================================================

if not st.session_state.messages:
    welcome_message = WELCOME_MESSAGE_TEMPLATE.format(
        name=st.session_state.name
    )
    add_message("assistant", "text", welcome_message)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    render_message(message)


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask a question, or upload a study image…",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "webp"],
)


# ============================================================
# HANDLE USER INPUT
# ============================================================

if user_input:

    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        try:
            photo_bytes = photo.getvalue()
            add_message("user", "image", photo_bytes)
            parts.append(
                types.Part.from_bytes(
                    data=photo_bytes,
                    mime_type=photo.type,
                )
            )
        except Exception as error:
            st.error(f"❌ Could not process image: {error}")
            st.stop()

    if text:
        add_message("user", "text", text)
        parts.append(text)

    elif photo is not None:
        parts.append(
            """
Analyze this study material carefully.

Identify what the image contains — it may be a question,
textbook content, handwritten notes, an equation, a science
problem, a diagram, a chart, code, an assignment, or exam material.

If it contains a question: solve it step by step and explain the reasoning.
If it contains theory: explain the important concepts in simple English.
If it contains a diagram: explain the visible components and how they connect.
If it contains code: explain what it does and flag visible errors.
If the image is blurry or unreadable: don't guess — tell the
student which part needs a clearer image.
"""
        )

    if parts:
        with st.spinner("✧  StudySnap is analyzing…"):
            gemini_ok, gemini_result = ask_gemini(parts)

        if gemini_ok:
            add_message("assistant", "text", gemini_result)
        else:
            # Show the clean, friendly message — not a raw traceback
            add_message("assistant", "text", gemini_result)

        st.rerun()


# ============================================================
# WHATSAPP DELIVERY — PREMIUM CARD + BUTTON
# ============================================================

st.markdown("<div style='height: 1.6rem;'></div>", unsafe_allow_html=True)

html(
    f"""
    <div class="wa-card">
        <div class="wa-header">
            <div class="wa-icon">📲</div>
            <div>
                <div class="wa-title">Send to WhatsApp</div>
                <div class="wa-sub">
                    Receive a curated study summary on
                    <b>{st.session_state.whatsapp_number}</b>.
                </div>
            </div>
        </div>

        <div class="wa-user">
            <span>Logged in as <b>{st.session_state.name}</b></span>
            <span class="dot">·</span>
            <span>Updates go to <b>{st.session_state.whatsapp_number}</b></span>
        </div>
    </div>
    """
)

send_disabled = len(st.session_state.messages) <= 1

if st.button(
    "📲  Send to WhatsApp",
    disabled=send_disabled,
    use_container_width=True,
):
    # ---- STEP 1: Generate summary via Gemini ----
    with st.spinner("Summarizing your day..."):
        gemini_ok, summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

    if not gemini_ok:
        # Gemini failed — do NOT call Twilio. Show only the Gemini message.
        st.warning(summary)
    else:
        # ---- STEP 2: Send to WhatsApp only on Gemini success ----
        with st.spinner("Dispatching to WhatsApp..."):
            success, info = send_whatsapp(
                st.session_state.whatsapp_number,
                st.session_state.name,
                summary,
            )

        if success:
            st.success("✅  Study summary sent to WhatsApp.")
            st.balloons()
        else:
            st.error(info)


# ============================================================
# FOOTER
# ============================================================

st.divider()
html(
    """
    <div class="lux-footer">
        <span class="gold">✦</span>&nbsp;&nbsp;
        StudySnap AI · Learn the concept, not just the answer
        &nbsp;&nbsp;<span class="gold">✦</span>
    </div>
    """
)