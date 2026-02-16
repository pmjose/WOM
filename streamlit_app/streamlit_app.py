import streamlit as st
from textwrap import dedent

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.config('connection_name', 'default').create()

# ---------------------------------------------------------------------------
# CSS faithfully mirroring https://wom.cl/
# ---------------------------------------------------------------------------
WOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=block');
@import url('https://fonts.googleapis.com/css2?family=Material+Icons+Outlined&display=block');
@import url('https://fonts.googleapis.com/css2?family=Material+Icons+Round&display=block');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');

/* ── WOM brand tokens (extracted from wom.cl) ──────────────── */
:root {
    --mf-blue:        #7B1FA2;
    --mf-navy:        #4A148C;
    --mf-navy-dark:   #311B92;
    --mf-orange:      #F57C00;
    --mf-orange-hover:#EF6C00;
    --mf-dark:        #1a1a2e;
    --mf-light:       #F3E5F5;
    --mf-gray:        #6c757d;
    --mf-border:      #dee2e6;
    --mf-success:     #28a745;
    --mf-danger:      #dc3545;
    --mf-grad-hero:   linear-gradient(135deg, #4A148C 0%, #311B92 60%, #1A237E 100%);
    --mf-grad-blue:   linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%);
    --mf-grad-card:   linear-gradient(135deg, #7B1FA2 0%, #6A1B9A 100%);
    --mf-grad-recommended: linear-gradient(135deg, #4A148C 0%, #311B92 100%);
    --mf-shadow-sm:   0 2px 8px rgba(0,0,0,0.08);
    --mf-shadow-md:   0 5px 20px rgba(0,0,0,0.10);
    --mf-shadow-lg:   0 10px 40px rgba(0,0,0,0.15);
    --mf-radius:      16px;
    --mf-radius-sm:   10px;
    --mf-radius-pill:  50px;
}

/* ── Global reset ──────────────────────────────────────────────────── */
html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif !important;
}

/* Keep Material glyphs from being replaced by Poppins. */
.material-icons,
.material-icons-outlined,
.material-icons-round,
.material-icons-outlined,
.material-icons-round,
.material-icons-sharp,
.material-symbols-outlined,
.material-symbols-rounded,
.material-symbols-sharp {
    font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons' !important;
    font-style: normal;
    font-weight: normal;
    letter-spacing: normal;
    text-transform: none;
}

/* Streamlit sidebar collapse / expand icon fallback:
   force icon font and hide accidental ligature text rendering. */
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] span {
    font-family: 'Material Symbols Outlined', 'Material Icons Round', 'Material Icons Outlined', 'Material Icons' !important;
    font-size: 20px !important;
    line-height: 1 !important;
    color: #ffffff !important;
}

[data-testid="stSidebarCollapseButton"] p,
[data-testid="collapsedControl"] p {
    display: none !important;
}

/* Hard fallback: hide Streamlit collapse controls to avoid
   keyboard_arrow_* ligature text appearing in sidebar header. */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}

.stApp {
    background: #f0f2f6;
}

/* Hide Streamlit default header / footer */
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* ── Sidebar ───────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--mf-grad-hero) !important;
    border-right: none;
    overflow-x: hidden;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    color: #ffffff !important;
    background: rgba(255,255,255,0.07);
    border-radius: var(--mf-radius-sm);
    padding: 12px 16px;
    margin: 4px 0;
    transition: all 0.25s ease;
    border: 1px solid rgba(255,255,255,0.06);
    width: 100% !important;
    min-height: 52px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
    color: #ffffff !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    margin: 0 !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(0,160,227,0.25);
    border-color: rgba(0,160,227,0.4);
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
}

/* ── Buttons (WOM orange CTA style) ────────────────────────────── */
.stButton > button {
    background: var(--mf-orange) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--mf-radius-pill) !important;
    padding: 12px 32px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255,107,0,0.3) !important;
}

.stButton > button:hover {
    background: var(--mf-orange-hover) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(255,107,0,0.45) !important;
}

/* ── Navbar / top bar ──────────────────────────────────────────────── */
.mf-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    padding: 12px 30px;
    border-radius: var(--mf-radius);
    box-shadow: var(--mf-shadow-sm);
    margin-bottom: 24px;
}

.mf-topbar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.mf-topbar-logo img {
    height: 40px;
    border-radius: 10px;
}

.mf-topbar-brand {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--mf-navy);
    letter-spacing: 0.5px;
}

.mf-topbar-brand span {
    color: var(--mf-blue);
}

.mf-topbar-nav {
    display: flex;
    gap: 24px;
    align-items: center;
}

.mf-topbar-nav a {
    color: var(--mf-navy);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.2s;
}

.mf-topbar-nav a:hover {
    color: var(--mf-blue);
}

.mf-topbar-phone {
    background: var(--mf-blue);
    color: #fff;
    padding: 8px 20px;
    border-radius: var(--mf-radius-pill);
    font-weight: 600;
    font-size: 0.85rem;
    text-decoration: none;
    transition: background 0.2s;
}

.mf-topbar-phone:hover { background: var(--mf-navy); }

/* ── Hero section (matches wom.cl dark gradient hero) ──────────── */
.mf-hero {
    background: var(--mf-grad-hero);
    border-radius: var(--mf-radius);
    padding: 50px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--mf-shadow-lg);
}

.mf-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0,160,227,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.mf-hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,160,227,0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.mf-hero-content {
    position: relative;
    z-index: 2;
}

.mf-hero h1 {
    color: #ffffff;
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    line-height: 1.15;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.mf-hero h1 span {
    color: var(--mf-blue);
}

.mf-hero p {
    color: rgba(255,255,255,0.8);
    font-size: 1.1rem;
    font-weight: 300;
    margin: 0;
    max-width: 600px;
}

.mf-hero-badge {
    display: inline-block;
    background: var(--mf-orange);
    color: #fff;
    padding: 6px 18px;
    border-radius: var(--mf-radius-pill);
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
}

/* ── Section headings ──────────────────────────────────────────────── */
.mf-section-title {
    text-align: center;
    margin-bottom: 40px;
}

.mf-section-title h2 {
    color: var(--mf-navy);
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.mf-section-title p {
    color: var(--mf-gray);
    font-size: 1rem;
    font-weight: 400;
}

.mf-section-title .mf-title-accent {
    display: inline-block;
    width: 60px;
    height: 4px;
    background: var(--mf-blue);
    border-radius: 2px;
    margin-bottom: 16px;
}

/* ── Plan cards (matches wom.cl pricing cards) ─────────────────── */
.mf-plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}

.mf-plan-card {
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 32px 24px;
    text-align: center;
    box-shadow: var(--mf-shadow-md);
    border: 2px solid transparent;
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
}

.mf-plan-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--mf-shadow-lg);
    border-color: var(--mf-blue);
}

.mf-plan-card.recommended {
    background: var(--mf-grad-recommended);
    color: #ffffff;
    border-color: var(--mf-blue);
    transform: scale(1.03);
}

.mf-plan-card.recommended:hover {
    transform: scale(1.03) translateY(-8px);
}

.mf-plan-card .badge-recommended {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background: var(--mf-orange);
    color: #fff;
    padding: 6px 24px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    border-radius: 0 0 10px 10px;
}

.mf-plan-card .speed-promo {
    font-size: 0.8rem;
    color: var(--mf-gray);
    font-weight: 400;
    margin-bottom: 4px;
}

.mf-plan-card.recommended .speed-promo {
    color: rgba(255,255,255,0.6);
}

.mf-plan-card .speed-main {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--mf-navy);
    margin: 4px 0;
    line-height: 1.1;
}

.mf-plan-card.recommended .speed-main {
    color: #ffffff;
}

.mf-plan-card .speed-unit {
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--mf-gray);
}

.mf-plan-card.recommended .speed-unit {
    color: rgba(255,255,255,0.7);
}

.mf-plan-card .fiber-label {
    display: inline-block;
    background: rgba(0,160,227,0.1);
    color: var(--mf-blue);
    padding: 4px 14px;
    border-radius: var(--mf-radius-pill);
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 12px 0;
}

.mf-plan-card.recommended .fiber-label {
    background: rgba(0,160,227,0.25);
    color: #ffffff;
}

.mf-plan-card .plan-features {
    text-align: left;
    margin: 16px 0;
    padding: 0;
    list-style: none;
    font-size: 0.85rem;
    color: var(--mf-gray);
}

.mf-plan-card.recommended .plan-features {
    color: rgba(255,255,255,0.8);
}

.mf-plan-card .plan-features li {
    padding: 4px 0;
    padding-left: 20px;
    position: relative;
}

.mf-plan-card .plan-features li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: var(--mf-blue);
    font-weight: 700;
}

.mf-plan-card.recommended .plan-features li::before {
    color: var(--mf-orange);
}

.mf-plan-card .plan-divider {
    border: none;
    height: 1px;
    background: var(--mf-border);
    margin: 16px 0;
}

.mf-plan-card.recommended .plan-divider {
    background: rgba(255,255,255,0.15);
}

.mf-plan-card .plan-price {
    margin: 16px 0 4px;
}

.mf-plan-card .price-currency {
    font-size: 1rem;
    font-weight: 600;
    color: var(--mf-navy);
    vertical-align: top;
}

.mf-plan-card.recommended .price-currency {
    color: #ffffff;
}

.mf-plan-card .price-amount {
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--mf-navy);
    line-height: 1;
}

.mf-plan-card.recommended .price-amount {
    color: #ffffff;
}

.mf-plan-card .price-decimal {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--mf-navy);
    vertical-align: top;
}

.mf-plan-card.recommended .price-decimal {
    color: #ffffff;
}

.mf-plan-card .price-period {
    display: block;
    font-size: 0.75rem;
    color: var(--mf-gray);
    margin-top: 4px;
}

.mf-plan-card.recommended .price-period {
    color: rgba(255,255,255,0.6);
}

.mf-plan-card .plan-cta {
    display: inline-block;
    background: var(--mf-orange);
    color: #ffffff;
    padding: 12px 32px;
    border-radius: var(--mf-radius-pill);
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    margin-top: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255,107,0,0.3);
}

.mf-plan-card .plan-cta:hover {
    background: var(--mf-orange-hover);
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(255,107,0,0.45);
}

.mf-plan-card.recommended .plan-cta {
    background: #ffffff;
    color: var(--mf-navy);
}

.mf-plan-card.recommended .plan-cta:hover {
    background: var(--mf-light);
}

.mf-plan-note {
    text-align: center;
    font-size: 0.8rem;
    color: var(--mf-gray);
    margin-top: 8px;
    margin-bottom: 40px;
}

/* ── Benefits section (matches wom.cl 4-column benefits) ───────── */
.mf-benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}

.mf-benefit-card {
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 32px 24px;
    text-align: center;
    box-shadow: var(--mf-shadow-sm);
    transition: all 0.3s ease;
    border-top: 4px solid var(--mf-blue);
}

.mf-benefit-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--mf-shadow-md);
}

.mf-benefit-icon {
    font-size: 2.5rem;
    margin-bottom: 16px;
    display: inline-block;
    width: 70px;
    height: 70px;
    line-height: 70px;
    border-radius: 50%;
    background: rgba(0,160,227,0.1);
}

.mf-benefit-card h3 {
    color: var(--mf-navy);
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.mf-benefit-card p {
    color: var(--mf-gray);
    font-size: 0.88rem;
    font-weight: 400;
    line-height: 1.6;
    margin: 0;
}

/* ── Ookla recognition section ─────────────────────────────────────── */
.mf-ookla {
    background: var(--mf-grad-hero);
    border-radius: var(--mf-radius);
    padding: 48px 40px;
    margin-bottom: 32px;
    color: #ffffff;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.mf-ookla::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -15%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,160,227,0.12) 0%, transparent 70%);
    border-radius: 50%;
}

.mf-ookla h3 {
    color: var(--mf-blue);
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0 0 12px 0;
}

.mf-ookla h2 {
    color: #ffffff;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 16px 0;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.3;
}

.mf-ookla p {
    color: rgba(255,255,255,0.75);
    font-size: 0.9rem;
    line-height: 1.7;
    max-width: 750px;
    margin: 0 auto 16px;
}

.mf-ookla-badges {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin: 24px 0;
    flex-wrap: wrap;
}

.mf-ookla-badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: var(--mf-radius-sm);
    padding: 20px 28px;
    text-align: center;
    min-width: 180px;
}

.mf-ookla-badge .badge-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.mf-ookla-badge .badge-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
    display: block;
}

.mf-ookla-badge .badge-sub {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
    display: block;
}

.mf-ookla-cta {
    display: inline-block;
    background: var(--mf-orange);
    color: #fff;
    padding: 14px 36px;
    border-radius: var(--mf-radius-pill);
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    margin-top: 24px;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(255,107,0,0.3);
}

.mf-ookla-cta:hover {
    background: var(--mf-orange-hover);
    transform: translateY(-2px);
}

/* ── Comparison section (numbered steps like wom.cl) ───────────── */
.mf-comparison {
    margin-bottom: 40px;
}

.mf-comparison-item {
    display: flex;
    gap: 24px;
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 28px;
    margin-bottom: 16px;
    box-shadow: var(--mf-shadow-sm);
    align-items: flex-start;
    transition: all 0.3s ease;
    border-left: 4px solid var(--mf-blue);
}

.mf-comparison-item:hover {
    box-shadow: var(--mf-shadow-md);
    transform: translateX(4px);
}

.mf-comparison-num {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    background: var(--mf-grad-blue);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: 800;
}

.mf-comparison-body h3 {
    color: var(--mf-navy);
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 4px 0;
}

.mf-comparison-body .comp-subtitle {
    color: var(--mf-blue);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    display: block;
}

.mf-comparison-body p {
    color: var(--mf-gray);
    font-size: 0.88rem;
    line-height: 1.6;
    margin: 0;
}

/* ── Dashboard metric cards ────────────────────────────────────────── */
.mf-metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 32px;
}

.mf-metric-card {
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 24px;
    box-shadow: var(--mf-shadow-sm);
    border-left: 4px solid var(--mf-blue);
    transition: all 0.3s ease;
}

.mf-metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--mf-shadow-md);
}

.mf-metric-card .metric-icon {
    font-size: 1.5rem;
    margin-bottom: 8px;
}

.mf-metric-card .metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--mf-navy);
    line-height: 1.2;
}

.mf-metric-card .metric-label {
    font-size: 0.8rem;
    color: var(--mf-gray);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 500;
    margin-top: 4px;
}

.mf-metric-card .metric-delta {
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 8px;
}

.mf-metric-card .metric-delta.positive { color: var(--mf-success); }
.mf-metric-card .metric-delta.negative { color: var(--mf-danger); }

/* ── Empty / placeholder states ────────────────────────────────────── */
.mf-empty {
    text-align: center;
    padding: 60px 40px;
    background: #ffffff;
    border-radius: var(--mf-radius);
    box-shadow: var(--mf-shadow-sm);
}

.mf-empty-icon {
    font-size: 3.5rem;
    margin-bottom: 16px;
}

.mf-empty h3 {
    color: var(--mf-navy);
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.mf-empty p {
    color: var(--mf-gray);
    font-size: 0.95rem;
    margin: 0;
}

/* ── Sidebar logo block ────────────────────────────────────────────── */
.mf-sidebar-logo {
    text-align: center;
    padding: 20px 12px;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.mf-sidebar-logo img {
    max-width: 80px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.mf-sidebar-brand {
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 800;
    margin-top: 10px;
    letter-spacing: 1px;
}

.mf-sidebar-brand span {
    color: var(--mf-blue);
}

.mf-sidebar-tagline {
    color: rgba(255,255,255,0.55);
    font-size: 0.75rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

@keyframes mfTickerSlide {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-50%); }
}
.mf-sidebar-ticker {
    margin: 4px 6px 12px;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}
.mf-sidebar-ticker-track {
    display: inline-flex;
    align-items: center;
    gap: 28px;
    min-width: max-content;
    white-space: nowrap;
    padding: 7px 0;
    animation: mfTickerSlide 20s linear infinite;
}
.mf-sidebar-ticker-item {
    color: #FDE68A;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.25px;
}
.mf-sidebar-ticker-item .dot {
    color: #F59E0B;
    margin-right: 6px;
}

.mf-sidebar-badge {
    display: inline-block;
    background: var(--mf-orange);
    color: #fff;
    padding: 4px 14px;
    border-radius: var(--mf-radius-pill);
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.mf-sidebar-version {
    color: rgba(255,255,255,0.35);
    font-size: 0.68rem;
    text-align: center;
    margin-top: 24px;
}

.mf-menu-header {
    color: var(--mf-blue) !important;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 20px 0 8px 0;
    padding-left: 4px;
}

/* ── Footer ────────────────────────────────────────────────────────── */
.mf-footer {
    background: var(--mf-grad-hero);
    border-radius: var(--mf-radius);
    padding: 40px 30px;
    margin-top: 48px;
    color: rgba(255,255,255,0.7);
    text-align: center;
}

.mf-footer-brand {
    font-size: 1.5rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 8px;
}

.mf-footer-brand span {
    color: var(--mf-blue);
}

.mf-footer-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
    margin: 16px 0;
}

.mf-footer-links a {
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 400;
    transition: color 0.2s;
}

.mf-footer-links a:hover { color: var(--mf-blue); }

.mf-footer-contact {
    margin: 20px 0 0;
    display: flex;
    justify-content: center;
    gap: 32px;
    flex-wrap: wrap;
}

.mf-footer-contact-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
}

.mf-footer-contact-item span.icon {
    font-size: 1.1rem;
}

.mf-footer-divider {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.1);
    margin: 24px 0 16px;
}

.mf-footer-copy {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
}

/* ── Tabs override ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(0,160,227,0.08);
    border-radius: var(--mf-radius-pill);
    padding: 8px 20px;
    font-weight: 500;
    color: var(--mf-navy);
}

.stTabs [aria-selected="true"] {
    background: var(--mf-blue) !important;
    color: #ffffff !important;
}

/* ── Intro page – Snowflake-style animated dashboard ───────────────── */

/* Keyframe animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.85); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(0,160,227,0.15); }
    50%      { box-shadow: 0 0 40px rgba(0,160,227,0.35); }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
@keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes spinSlow {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes slideInScale {
    from { opacity: 0; transform: scale(0.9) translateY(20px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes borderPulse {
    0%, 100% { border-color: rgba(0,160,227,0.2); }
    50%      { border-color: rgba(0,160,227,0.5); }
}

/* ── Intro: Hero hub card ──────────────────────────────────────────── */
.intro-hub {
    background: linear-gradient(135deg, #f0faff 0%, #e6f7ff 50%, #f0f4ff 100%);
    border: 2px solid rgba(0,160,227,0.15);
    border-radius: var(--mf-radius);
    padding: 48px 32px 40px;
    text-align: center;
    margin-bottom: 32px;
    animation: fadeInDown 0.7s ease-out;
    position: relative;
    overflow: hidden;
}
.intro-hub::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--mf-blue), var(--mf-navy), var(--mf-blue));
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}
.intro-hub-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--mf-navy);
    margin: 0 0 4px;
}
.intro-hub-title span { color: var(--mf-blue); }
.intro-hub-sub {
    font-size: 0.85rem;
    color: var(--mf-gray);
    margin-bottom: 28px;
}

/* Hub diagram — circular center + orbiting nodes */
.hub-diagram {
    position: relative;
    width: 260px;
    height: 260px;
    margin: 0 auto 28px;
    animation: scaleIn 0.8s ease-out 0.2s both;
}
.hub-center {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 90px; height: 90px;
    border-radius: 50%;
    background: var(--mf-grad-blue);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    color: #fff;
    box-shadow: 0 8px 30px rgba(0,160,227,0.35);
    animation: pulseGlow 3s ease-in-out infinite;
    z-index: 2;
}
.hub-ring {
    position: absolute;
    top: 50%; left: 50%;
    width: 220px; height: 220px;
    transform: translate(-50%, -50%);
    border: 2px dashed rgba(0,160,227,0.2);
    border-radius: 50%;
    animation: spinSlow 60s linear infinite;
}
.hub-node {
    position: absolute;
    width: 52px; height: 52px;
    border-radius: 50%;
    background: #fff;
    border: 2px solid rgba(0,160,227,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 600; color: var(--mf-navy);
    box-shadow: var(--mf-shadow-sm);
    transition: all 0.3s ease;
    flex-direction: column;
    line-height: 1.1;
    text-align: center;
}
.hub-node:hover {
    border-color: var(--mf-blue);
    transform: scale(1.12);
    box-shadow: 0 4px 16px rgba(0,160,227,0.25);
}
.hub-node .hub-icon { font-size: 1rem; margin-bottom: 2px; }
/* Positions around circle (6 nodes at 60° intervals) */
.hub-node:nth-child(3) { top: -10px; left: 50%; transform: translateX(-50%); }
.hub-node:nth-child(4) { top: 18%;  right: -10px; }
.hub-node:nth-child(5) { bottom: 18%; right: -10px; }
.hub-node:nth-child(6) { bottom: -10px; left: 50%; transform: translateX(-50%); }
.hub-node:nth-child(7) { bottom: 18%; left: -10px; }
.hub-node:nth-child(8) { top: 18%;  left: -10px; }

/* Hub stats row */
.hub-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
}
.hub-stat {
    text-align: center;
    animation: countUp 0.6s ease-out both;
}
.hub-stat:nth-child(1) { animation-delay: 0.5s; }
.hub-stat:nth-child(2) { animation-delay: 0.7s; }
.hub-stat:nth-child(3) { animation-delay: 0.9s; }
.hub-stat:nth-child(4) { animation-delay: 1.1s; }
.hub-stat-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--mf-blue);
}
.hub-stat-label {
    font-size: 0.65rem;
    color: var(--mf-gray);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Intro: section labels ─────────────────────────────────────────── */
.intro-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--mf-blue);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
    animation: fadeInLeft 0.5s ease-out both;
}

/* ── Intro: stat cards row ─────────────────────────────────────────── */
.intro-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.intro-stat-card {
    background: #fff;
    border: 2px solid rgba(0,160,227,0.12);
    border-radius: var(--mf-radius);
    padding: 24px 16px;
    text-align: center;
    animation: slideInScale 0.6s ease-out both;
    transition: all 0.3s ease;
}
.intro-stat-card:nth-child(1) { animation-delay: 0.3s; }
.intro-stat-card:nth-child(2) { animation-delay: 0.45s; }
.intro-stat-card:nth-child(3) { animation-delay: 0.6s; }
.intro-stat-card:nth-child(4) { animation-delay: 0.75s; }
.intro-stat-card:hover {
    border-color: var(--mf-blue);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,160,227,0.12);
}
.intro-stat-val {
    font-size: 2rem;
    font-weight: 800;
    color: var(--mf-navy);
    line-height: 1.1;
}
.intro-stat-val span { color: var(--mf-blue); }
.intro-stat-lbl {
    font-size: 0.72rem;
    color: var(--mf-gray);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* ── Intro: 3-column pillar cards ──────────────────────────────────── */
.intro-pillars {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-bottom: 32px;
}
.intro-pillar {
    background: #fff;
    border: 2px solid rgba(0,160,227,0.10);
    border-radius: var(--mf-radius);
    padding: 32px 24px;
    text-align: center;
    animation: fadeInUp 0.6s ease-out both;
    transition: all 0.35s ease;
}
.intro-pillar:nth-child(1) { animation-delay: 0.2s; }
.intro-pillar:nth-child(2) { animation-delay: 0.4s; }
.intro-pillar:nth-child(3) { animation-delay: 0.6s; }
.intro-pillar:hover {
    border-color: var(--mf-blue);
    transform: translateY(-6px);
    box-shadow: var(--mf-shadow-md);
}
.intro-pillar .pillar-icon {
    font-size: 2rem;
    margin-bottom: 12px;
    animation: float 4s ease-in-out infinite;
}
.intro-pillar:nth-child(2) .pillar-icon { animation-delay: 0.5s; }
.intro-pillar:nth-child(3) .pillar-icon { animation-delay: 1s; }
.intro-pillar h3 {
    color: var(--mf-navy);
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0 0 8px;
}
.intro-pillar p {
    color: var(--mf-gray);
    font-size: 0.8rem;
    line-height: 1.6;
    margin: 0;
}

/* ── Intro: logo / trust bar ───────────────────────────────────────── */
.intro-trust {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 48px;
    flex-wrap: wrap;
    margin-bottom: 32px;
    padding: 28px 24px;
    background: #fff;
    border: 2px solid rgba(0,160,227,0.08);
    border-radius: var(--mf-radius);
    animation: fadeInUp 0.7s ease-out 0.3s both;
}
.intro-trust-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--mf-navy);
    opacity: 0.6;
    transition: opacity 0.3s;
    display: flex;
    align-items: center;
    gap: 8px;
}
.intro-trust-logo:hover { opacity: 1; }

/* ── Intro: 2×2 KPI benefit cards ──────────────────────────────────── */
.intro-kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.intro-kpi {
    border-radius: var(--mf-radius);
    padding: 28px 24px;
    animation: slideInScale 0.6s ease-out both;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}
.intro-kpi:nth-child(1) { background: linear-gradient(135deg, #e8f8f0 0%, #f0fdf4 100%); border-color: rgba(40,167,69,0.15); animation-delay: 0.2s; }
.intro-kpi:nth-child(2) { background: linear-gradient(135deg, #e6f7ff 0%, #f0faff 100%); border-color: rgba(0,160,227,0.15); animation-delay: 0.35s; }
.intro-kpi:nth-child(3) { background: linear-gradient(135deg, #fff8e6 0%, #fffbf0 100%); border-color: rgba(255,107,0,0.15); animation-delay: 0.5s; }
.intro-kpi:nth-child(4) { background: linear-gradient(135deg, #f0e6ff 0%, #f8f0ff 100%); border-color: rgba(111,66,193,0.15); animation-delay: 0.65s; }
.intro-kpi:hover {
    transform: translateY(-4px);
    box-shadow: var(--mf-shadow-md);
}
.intro-kpi h4 {
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 12px;
}
.intro-kpi:nth-child(1) h4 { color: #1b7a3d; }
.intro-kpi:nth-child(2) h4 { color: #0077b3; }
.intro-kpi:nth-child(3) h4 { color: #cc5500; }
.intro-kpi:nth-child(4) h4 { color: #6f42c1; }
.intro-kpi ul {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.82rem;
    color: #555;
    line-height: 1.8;
}
.intro-kpi ul li::before {
    content: '•';
    font-weight: 700;
    margin-right: 8px;
}
.intro-kpi:nth-child(1) ul li::before { color: #28a745; }
.intro-kpi:nth-child(2) ul li::before { color: var(--mf-blue); }
.intro-kpi:nth-child(3) ul li::before { color: var(--mf-orange); }
.intro-kpi:nth-child(4) ul li::before { color: #6f42c1; }
.intro-kpi ul li strong { font-weight: 600; color: #333; }

/* ── Intro: solution cards grid ────────────────────────────────────── */
.intro-solutions {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 16px;
}
.intro-sol {
    background: #fff;
    border: 2px solid rgba(0,160,227,0.10);
    border-radius: var(--mf-radius-sm);
    padding: 22px 20px;
    animation: fadeInUp 0.5s ease-out both;
    transition: all 0.3s ease;
}
.intro-sol:nth-child(1) { animation-delay: 0.1s; }
.intro-sol:nth-child(2) { animation-delay: 0.2s; }
.intro-sol:nth-child(3) { animation-delay: 0.3s; }
.intro-sol:nth-child(4) { animation-delay: 0.4s; }
.intro-sol:nth-child(5) { animation-delay: 0.5s; }
.intro-sol:nth-child(6) { animation-delay: 0.6s; }
.intro-sol:hover {
    border-color: var(--mf-blue);
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(0,160,227,0.10);
}
.intro-sol h5 {
    color: var(--mf-blue);
    font-size: 0.88rem;
    font-weight: 700;
    margin: 0 0 4px;
}
.intro-sol p {
    color: var(--mf-gray);
    font-size: 0.75rem;
    margin: 0;
    line-height: 1.5;
}

/* ── Responsive tweaks ─────────────────────────────────────────────── */
@media (max-width: 768px) {
    .mf-hero { padding: 32px 24px; }
    .mf-hero h1 { font-size: 1.8rem; }
    .mf-plans-grid { grid-template-columns: 1fr; }
    .mf-benefits-grid { grid-template-columns: 1fr 1fr; }
    .mf-ookla { padding: 32px 20px; }
    .mf-ookla h2 { font-size: 1.4rem; }
    .mf-topbar { flex-direction: column; gap: 12px; }
    .mf-comparison-item { flex-direction: column; gap: 16px; }
    .intro-stats { grid-template-columns: repeat(2, 1fr); }
    .intro-pillars { grid-template-columns: 1fr; }
    .intro-kpi-grid { grid-template-columns: 1fr; }
    .intro-solutions { grid-template-columns: 1fr; }
}
</style>
"""

st.set_page_config(
    page_title="WOM Chile | Movil, Fibra, TV - Dashboard",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/WOM_Chile.svg/1280px-WOM_Chile.svg.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(WOM_CSS, unsafe_allow_html=True)

LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/WOM_Chile.svg/1280px-WOM_Chile.svg.png"
WA_LINK = "https://api.whatsapp.com/send?phone=56935223070"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(dedent("""
        <div class="mf-sidebar-ticker">
            <div class="mf-sidebar-ticker-track">
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Prepago churn risk: 72%</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>$2.8B CLP ARR at risk</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Valparaiso NPS below target</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>5G rollout ahead of schedule</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Prepago churn risk: 72%</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>$2.8B CLP ARR at risk</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Valparaiso NPS below target</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>5G rollout ahead of schedule</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

    st.markdown(dedent(f"""
        <div class="mf-sidebar-logo">
            <img src="{LOGO_URL}" alt="WOM">
            <div class="mf-sidebar-tagline">Movil | Fibra | TV</div>
        </div>
    """), unsafe_allow_html=True)

    st.markdown('<p class="mf-menu-header">Dashboard</p>', unsafe_allow_html=True)

    menu_options = [
        "Intro",
        "Executive Overview",
        "Subscribers",
        "Revenue Analytics",
        "Network Status",
        "Marketing",
        "HR & Workforce",
        "Conclusion",
    ]

    selected_menu = st.radio(
        label="Menu",
        options=menu_options,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(dedent("""
        <div style="text-align:center; padding: 8px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
            <span class="mf-sidebar-badge">5G</span>
            <span class="mf-sidebar-badge" style="background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);">Fibra</span>
            <span class="mf-sidebar-badge" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);">Hogar</span>
        </div>
    """), unsafe_allow_html=True)

    st.markdown('<div class="mf-sidebar-version">v1.0.0 &middot; Chile &middot; Snowflake</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Intro — Executive Summary (from example.py)
# ---------------------------------------------------------------------------
if selected_menu == "Intro":

    # ── Hub & Spoke Banner with Floating Particles ─────────────────────
    st.markdown("""
<style>
@keyframes hub-pulse { 0%, 100% { transform: scale(1); box-shadow: 0 0 25px rgba(41,181,232,0.5); } 50% { transform: scale(1.08); box-shadow: 0 0 45px rgba(41,181,232,0.8); } }
@keyframes hub-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes hub-arrow { 0%, 100% { opacity: 0.4; transform: translateX(0); } 50% { opacity: 1; transform: translateX(5px); } }
@keyframes particle-drift {
    0% { transform: translateY(0) translateX(0) scale(1); opacity: 0; }
    10% { opacity: 0.8; }
    90% { opacity: 0.8; }
    100% { transform: translateY(-100px) translateX(30px) scale(0.5); opacity: 0; }
}
@keyframes sparkle { 0%, 100% { opacity: 0.3; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
.hub-banner { background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; position: relative; overflow: hidden; border: 1px solid #BAE6FD; }
.hub-particles { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; overflow: hidden; }
.hub-particle { position: absolute; width: 6px; height: 6px; background: #29B5E8; border-radius: 50%; animation: particle-drift 4s ease-out infinite; }
.hub-particle.small { width: 4px; height: 4px; background: rgba(41,181,232,0.6); }
.hub-sparkle { position: absolute; width: 8px; height: 8px; background: white; border-radius: 50%; animation: sparkle 2s ease-in-out infinite; }
.hub-title { text-align: center; color: #1B2A4E; font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem; position: relative; z-index: 1; }
.hub-subtitle { text-align: center; color: #64748B; font-size: 0.85rem; margin-bottom: 1.5rem; position: relative; z-index: 1; }
.hub-content { display: flex; align-items: center; justify-content: center; gap: 0.8rem; position: relative; z-index: 1; flex-wrap: wrap; }
.hub-sources { display: flex; flex-direction: column; gap: 0.6rem; }
.hub-source { background: white; border-radius: 10px; padding: 0.7rem 1rem; display: flex; align-items: center; gap: 0.6rem; border: 1px solid #E2E8F0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); animation: hub-float 3s ease-in-out infinite; }
.hub-source:nth-child(2) { animation-delay: 0.3s; }
.hub-source:nth-child(3) { animation-delay: 0.6s; }
.hub-source-icon { font-size: 1.3rem; }
.hub-source-label { color: #1B2A4E; font-size: 0.75rem; font-weight: 600; }
.hub-arrows { display: flex; flex-direction: column; gap: 1.2rem; padding: 0 0.5rem; }
.hub-arrow { color: #29B5E8; font-size: 1.2rem; animation: hub-arrow 1.5s ease-in-out infinite; }
.hub-arrow:nth-child(2) { animation-delay: 0.2s; }
.hub-arrow:nth-child(3) { animation-delay: 0.4s; }
.es-hub-center { background: linear-gradient(135deg, #29B5E8, #0EA5E9); border-radius: 50%; width: 120px; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; animation: hub-pulse 2s ease-in-out infinite; flex-shrink: 0; position: relative; }
.es-hub-center::after { content: ''; position: absolute; width: 140px; height: 140px; border: 2px solid rgba(41,181,232,0.3); border-radius: 50%; animation: hub-pulse 2s ease-in-out infinite 0.5s; }
.es-hub-center-icon { font-size: 2.5rem; }
.es-hub-center-label { color: white; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-top: 4px; }
.es-hub-stats { display: flex; justify-content: center; gap: 3rem; margin-top: 1.5rem; position: relative; z-index: 1; flex-wrap: wrap; }
.es-hub-stat { text-align: center; animation: hub-float 3s ease-in-out infinite; }
.es-hub-stat:nth-child(2) { animation-delay: 0.25s; }
.es-hub-stat:nth-child(3) { animation-delay: 0.5s; }
.es-hub-stat:nth-child(4) { animation-delay: 0.75s; }
.es-hub-stat-value { color: #29B5E8; font-size: 1.4rem; font-weight: 700; }
.es-hub-stat-label { color: #64748B; font-size: 0.65rem; text-transform: uppercase; }
@keyframes section-header-fade {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes section-header-shimmer {
    0% { transform: translateX(-120%); opacity: 0; }
    25% { opacity: 1; }
    100% { transform: translateX(220%); opacity: 0; }
}
@keyframes section-header-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(41,181,232,0.32); }
    50% { box-shadow: 0 0 0 6px rgba(41,181,232,0); }
}
.section-header {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1.02rem;
    font-weight: 700;
    color: #1B2A4E;
    margin: 1.35rem 0 0.9rem;
    padding: 0.62rem 0.85rem;
    border: 1px solid #DBEAFE;
    border-radius: 12px;
    background: linear-gradient(135deg, #F8FAFF 0%, #EEF5FF 100%);
    animation: section-header-fade 0.45s ease-out both;
}
.section-header::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #29B5E8 0%, #6366F1 100%);
    animation: section-header-pulse 2.2s ease-in-out infinite;
}
.section-header::after {
    content: "";
    position: absolute;
    top: 0;
    left: -30%;
    width: 28%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
    animation: section-header-shimmer 2.8s ease-in-out infinite;
}
.eo-subtitle {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin: 0.15rem 0 0.55rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E3A8A;
    letter-spacing: 0.01em;
    animation: section-header-fade 0.35s ease-out both;
}
.eo-subtitle::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, #22C1EE 0%, #8B5CF6 100%);
    opacity: 0.95;
}
.metric-card { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.metric-value { font-size: 1.8rem; font-weight: 700; }
.metric-label { font-size: 0.8rem; color: #6B7280; }
.architecture-box { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.architecture-box h4 { color: #1B2A4E; margin-top: 0.5rem; }
.architecture-box p { color: #6B7280; font-size: 0.85rem; line-height: 1.6; }
.talking-point { background: white; border: 1px solid #E5E7EB; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.5rem; color: #1B2A4E; font-size: 0.9rem; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
@keyframes arch-particle { 0% { left: 0%; opacity: 0; } 15% { opacity: 1; } 85% { opacity: 1; } 100% { left: 100%; opacity: 0; } }
@keyframes arch-pulse { 0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(41,181,232,0.3); } 50% { transform: scale(1.02); box-shadow: 0 6px 25px rgba(41,181,232,0.5); } }
@keyframes arch-glow { 0%, 100% { border-color: rgba(41,181,232,0.3); } 50% { border-color: rgba(41,181,232,0.8); } }
.arch-container { background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%); border-radius: 16px; padding: 2rem; border: 2px solid #E5E7EB; }
.arch-row { display: flex; align-items: center; justify-content: center; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }
.arch-column { display: flex; flex-direction: column; gap: 0.6rem; min-width: 140px; }
.arch-box { background: white; border: 2px solid #E5E7EB; border-radius: 10px; padding: 0.6rem 1rem; display: flex; align-items: center; gap: 0.5rem; animation: arch-glow 3s ease-in-out infinite; transition: all 0.3s; }
.arch-box:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.arch-box.source { border-left: 4px solid #F59E0B; }
.arch-box.output { border-left: 4px solid #10B981; }
.arch-icon { font-size: 1.2rem; }
.arch-label { font-size: 0.75rem; font-weight: 600; color: #1B2A4E; }
.arch-sublabel { font-size: 0.6rem; color: #6B7280; }
.arch-center { background: linear-gradient(135deg, #29B5E8 0%, #0EA5E9 100%); border-radius: 16px; padding: 1.5rem 2rem; animation: arch-pulse 3s ease-in-out infinite; min-width: 200px; }
.arch-center-title { color: white; font-size: 1.1rem; font-weight: 700; text-align: center; margin-bottom: 0.3rem; }
.arch-center-sub { color: rgba(255,255,255,0.8); font-size: 0.7rem; text-align: center; }
.arch-center-features { display: flex; flex-wrap: wrap; gap: 0.4rem; justify-content: center; margin-top: 0.8rem; }
.arch-feature { background: rgba(255,255,255,0.2); color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.6rem; }
.arch-pipes { position: relative; width: 60px; height: 200px; }
.arch-pipe { position: absolute; width: 100%; height: 2px; background: linear-gradient(90deg, #F59E0B, #29B5E8); }
.arch-pipe.out { background: linear-gradient(90deg, #29B5E8, #10B981); }
.arch-dot { position: absolute; width: 8px; height: 8px; border-radius: 50%; top: -3px; background: #F59E0B; animation: arch-particle 2.5s linear infinite; }
.arch-pipe.out .arch-dot { background: #10B981; }
.arch-section-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: #6B7280; margin-bottom: 0.5rem; font-weight: 600; }
</style>
    """, unsafe_allow_html=True)

    # Hub banner HTML (single line to avoid indentation issues)
    st.markdown("""<div class="hub-banner"><div class="hub-particles"><div class="hub-particle" style="left: 10%; top: 80%; animation-delay: 0s;"></div><div class="hub-particle small" style="left: 20%; top: 70%; animation-delay: 0.5s;"></div><div class="hub-particle" style="left: 30%; top: 85%; animation-delay: 1s;"></div><div class="hub-particle small" style="left: 40%; top: 75%; animation-delay: 1.5s;"></div><div class="hub-particle" style="left: 50%; top: 90%; animation-delay: 2s;"></div><div class="hub-particle small" style="left: 60%; top: 80%; animation-delay: 2.5s;"></div><div class="hub-particle" style="left: 70%; top: 85%; animation-delay: 3s;"></div><div class="hub-particle small" style="left: 80%; top: 75%; animation-delay: 3.5s;"></div><div class="hub-particle" style="left: 90%; top: 80%; animation-delay: 0.8s;"></div><div class="hub-sparkle" style="left: 15%; top: 20%; animation-delay: 0s;"></div><div class="hub-sparkle" style="left: 85%; top: 30%; animation-delay: 1s;"></div><div class="hub-sparkle" style="left: 45%; top: 15%; animation-delay: 2s;"></div></div><div class="hub-title">❄️ Snowflake AI Data Cloud</div><div class="hub-subtitle">Breaking Down Data Silos in Real-Time</div><div class="hub-content"><div class="hub-sources"><div class="hub-source"><span class="hub-source-icon">📡</span><span class="hub-source-label">Network</span></div><div class="hub-source"><span class="hub-source-icon">⚙️</span><span class="hub-source-label">OSCLP BSS</span></div><div class="hub-source"><span class="hub-source-icon">🏪</span><span class="hub-source-label">Marketplace</span></div></div><div class="hub-arrows"><span class="hub-arrow">→</span><span class="hub-arrow">→</span><span class="hub-arrow">→</span></div><div class="es-hub-center"><span class="es-hub-center-icon">❄️</span><span class="es-hub-center-label">Snowflake</span></div><div class="hub-arrows"><span class="hub-arrow">→</span><span class="hub-arrow">→</span><span class="hub-arrow">→</span></div><div class="hub-sources"><div class="hub-source"><span class="hub-source-icon">📊</span><span class="hub-source-label">Analytics</span></div><div class="hub-source"><span class="hub-source-icon">🤖</span><span class="hub-source-label">AI/ML</span></div><div class="hub-source"><span class="hub-source-icon">💡</span><span class="hub-source-label">Insights</span></div></div></div><div class="es-hub-stats"><div class="es-hub-stat"><div class="es-hub-stat-value">60%</div><div class="es-hub-stat-label">Faster Insights</div></div><div class="es-hub-stat"><div class="es-hub-stat-value">40%</div><div class="es-hub-stat-label">Cost Reduction</div></div><div class="es-hub-stat"><div class="es-hub-stat-value">100%</div><div class="es-hub-stat-label">Data Unified</div></div><div class="es-hub-stat"><div class="es-hub-stat-value">5x</div><div class="es-hub-stat-label">ROI</div></div></div></div>""", unsafe_allow_html=True)

    # ── About Snowflake ────────────────────────────────────────────────
    st.markdown('<div class="section-header">About Snowflake</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("11,000+", "Enterprise Customers"),
        ("$3.5B+", "Annual Revenue"),
        ("~50%", "Fortune 500 Companies"),
        ("#1", "Data Cloud Platform"),
    ]
    for col, (value, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""<div class="metric-card" style="text-align: center;"><div class="metric-value" style="color: #29B5E8;">{value}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

    # ── Why Snowflake for Telecom ──────────────────────────────────────
    st.markdown('<div class="section-header">Why Snowflake for Telecom</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="architecture-box" style="min-height: 220px;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div><h4>Bring Data & AI to Life</h4><p>Save time on building, configuring and tuning infrastructure with a single, fully managed platform. Streamline workflows, power business-critical use cases and uncover new commercial strategies.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="architecture-box" style="min-height: 220px;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div><h4>Connected Ecosystem</h4><p>Connect with mobile network operators, content providers, network equipment providers, and top data solutions providers. Optimize network performance, enhance customer experiences and monetize services more effectively.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="architecture-box" style="min-height: 220px;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div><h4>Trusted Governance</h4><p>Govern and protect your data with best-in-class security. Use AI and large language models within Snowflake's security perimeter, with built-in policies, access controls and end-to-end observability.</p></div>""", unsafe_allow_html=True)

    # ── Leading Telcos Trust Snowflake ─────────────────────────────────
    st.markdown('<div class="section-header">Leading Telcos Trust Snowflake</div>', unsafe_allow_html=True)

    customers = [
        {"name": "AT&T", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/AT%26T_logo_2016.svg/200px-AT%26T_logo_2016.svg.png"},
        {"name": "T-Mobile", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/T-Mobile_US_Logo_2022_RGB_Magenta_on_Transparent.svg/500px-T-Mobile_US_Logo_2022_RGB_Magenta_on_Transparent.svg.png"},
        {"name": "Deutsche Telekom", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Deutsche_Telekom_2022.svg/250px-Deutsche_Telekom_2022.svg.png"},
        {"name": "Vodafone", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Vodafone_2017_logo.svg/500px-Vodafone_2017_logo.svg.png"},
    ]
    cols = st.columns(4)
    for col, customer in zip(cols, customers):
        with col:
            st.markdown(f"""<div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center;"><div style="height: 60px; display: flex; align-items: center; justify-content: center;"><img src="{customer['logo']}" alt="{customer['name']}" style="max-height: 50px; max-width: 120px; object-fit: contain;"></div></div>""", unsafe_allow_html=True)

    # ── Business Benefits & KPIs (animated) ──────────────────────────
    st.markdown("""<style>
@keyframes kpi-slide-up { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes kpi-border-glow { 0%,100% { border-color: rgba(0,0,0,0.06); } 50% { border-color: rgba(41,181,232,0.25); } }
@keyframes kpi-icon-bob { 0%,100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-4px) scale(1.08); } }
@keyframes sol-fade { from { opacity: 0; transform: translateY(16px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }
.kpi-card { border-radius: 16px; padding: 1.6rem 1.5rem; border: 1.5px solid rgba(0,0,0,0.06); animation: kpi-slide-up 0.6s ease-out both, kpi-border-glow 4s ease-in-out infinite; transition: transform 0.3s ease, box-shadow 0.3s ease; position: relative; overflow: hidden; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); }
.kpi-card.blue { background: linear-gradient(135deg, #EBF8FF 0%, #F0FAFF 100%); }
.kpi-card.blue::before { background: linear-gradient(90deg, #29B5E8, #0EA5E9); }
.kpi-card.green { background: linear-gradient(135deg, #D1FAE5 0%, #ECFDF5 100%); }
.kpi-card.green::before { background: linear-gradient(90deg, #10B981, #34D399); }
.kpi-card.amber { background: linear-gradient(135deg, #FEF3C7 0%, #FFFBEB 100%); }
.kpi-card.amber::before { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.kpi-card.purple { background: linear-gradient(135deg, #EDE9FE 0%, #F5F3FF 100%); }
.kpi-card.purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
.kpi-card .kpi-head { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.kpi-card .kpi-icon { font-size: 1.5rem; animation: kpi-icon-bob 3s ease-in-out infinite; }
.kpi-card .kpi-title { font-size: 1.05rem; font-weight: 700; color: #1B2A4E; }
.kpi-card ul { color: #374151; margin: 0; padding-left: 0; list-style: none; font-size: 0.88rem; line-height: 2; }
.kpi-card ul li { position: relative; padding-left: 18px; }
.kpi-card ul li::before { content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 7px; height: 7px; border-radius: 50%; }
.kpi-card.blue ul li::before { background: #29B5E8; }
.kpi-card.green ul li::before { background: #10B981; }
.kpi-card.amber ul li::before { background: #F59E0B; }
.kpi-card.purple ul li::before { background: #8B5CF6; }
.kpi-card ul li strong { color: #1B2A4E; }
.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.sol-card { background: white; border: 1.5px solid #E5E7EB; border-radius: 14px; padding: 1.3rem 1.4rem; min-height: 80px; animation: sol-fade 0.5s ease-out both; transition: all 0.3s ease; position: relative; overflow: hidden; }
.sol-card::after { content: ''; position: absolute; bottom: 0; left: 0; width: 0; height: 2px; background: linear-gradient(90deg, #29B5E8, #0EA5E9); transition: width 0.4s ease; }
.sol-card:hover { border-color: #29B5E8; transform: translateY(-3px); box-shadow: 0 8px 24px rgba(41,181,232,0.10); }
.sol-card:hover::after { width: 100%; }
.sol-card .sol-icon { font-size: 1.6rem; margin-bottom: 8px; display: block; }
.sol-card .sol-title { font-size: 0.92rem; font-weight: 700; color: #1B2A4E; margin-bottom: 4px; }
.sol-card .sol-desc { font-size: 0.8rem; color: #6B7280; line-height: 1.5; }
</style>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Business Benefits & KPIs</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="kpi-card blue"><div class="kpi-head"><span class="kpi-icon">💰</span><span class="kpi-title">Revenue & Growth</span></div><ul><li><strong>15-25%</strong> reduction in customer churn</li><li><strong>20-30%</strong> increase in upsell conversion</li><li><strong>10-15%</strong> ARPU improvement</li><li><strong>$10M+</strong> fraud prevention savings</li></ul></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("""<div class="kpi-card amber"><div class="kpi-head"><span class="kpi-icon">⚡</span><span class="kpi-title">Operational Excellence</span></div><ul><li><strong>40-60%</strong> faster time-to-insight</li><li><strong>30%</strong> network ops cost reduction</li><li><strong>50%</strong> less data engineering effort</li><li><strong>80%</strong> faster reporting</li></ul></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="kpi-card green"><div class="kpi-head"><span class="kpi-icon">📈</span><span class="kpi-title">Customer Experience</span></div><ul><li><strong>+15 pts</strong> NPS improvement</li><li><strong>25%</strong> call center volume reduction</li><li><strong>Real-time</strong> network issue detection</li><li><strong>360°</strong> unified customer view</li></ul></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("""<div class="kpi-card purple"><div class="kpi-head"><span class="kpi-icon">🔒</span><span class="kpi-title">Security & Governance</span></div><ul><li><strong>Single source</strong> of truth</li><li><strong>Ley 19628/CCPA</strong> compliance built-in</li><li><strong>Row/column</strong> level access control</li><li><strong>Full audit</strong> trail & lineage</li></ul></div>""", unsafe_allow_html=True)

    # ── Join the Connected Future of Telecom (animated) ────────────────
    st.markdown('<div class="section-header">Join the Connected Future of Telecom</div>', unsafe_allow_html=True)

    use_cases = [
        ("🔮", "Churn Prediction", "Identify at-risk customers with ML models"),
        ("📡", "Network Analytics", "Real-time performance monitoring"),
        ("💳", "Revenue Assurance", "Detect billing anomalies and leakage"),
        ("👤", "Customer 360", "Unified cross-channel customer view"),
        ("🛡️", "Fraud Detection", "AI-powered SIM swap detection"),
        ("📶", "5G Monetization", "Optimize 5G pricing and adoption"),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(use_cases):
        with cols[i % 3]:
            delay = round(0.1 + i * 0.1, 1)
            st.markdown(f"""<div class="sol-card" style="animation-delay: {delay}s;"><span class="sol-icon">{icon}</span><div class="sol-title">{title}</div><div class="sol-desc">{desc}</div></div>""", unsafe_allow_html=True)

    # ── Architecture Overview ──────────────────────────────────────────
    st.markdown('<div class="section-header">Architecture Overview</div>', unsafe_allow_html=True)

    st.markdown("""<div class="arch-container"><div class="arch-row"><div class="arch-column"><div class="arch-section-label">Data Sources</div><div class="arch-box source"><span class="arch-icon">📡</span><div><div class="arch-label">Network Ops</div><div class="arch-sublabel">Performance & Sites</div></div></div><div class="arch-box source"><span class="arch-icon">🚨</span><div><div class="arch-label">Network Alarms</div><div class="arch-sublabel">NOC Events</div></div></div><div class="arch-box source"><span class="arch-icon">📶</span><div><div class="arch-label">FTTH Access Data</div><div class="arch-sublabel">OLT and CPE Telemetry</div></div></div><div class="arch-box source"><span class="arch-icon">💳</span><div><div class="arch-label">Billing</div><div class="arch-sublabel">Revenue & Invoices</div></div></div><div class="arch-box source"><span class="arch-icon">👥</span><div><div class="arch-label">Subscribers</div><div class="arch-sublabel">Customer Records</div></div></div><div class="arch-box source"><span class="arch-icon">🎫</span><div><div class="arch-label">Support Tickets</div><div class="arch-sublabel">Contact Center</div></div></div><div class="arch-box source"><span class="arch-icon">📦</span><div><div class="arch-label">Orders</div><div class="arch-sublabel">Installations and ONTs</div></div></div><div class="arch-box source"><span class="arch-icon">🤝</span><div><div class="arch-label">Partners</div><div class="arch-sublabel">Channel & Retail</div></div></div><div class="arch-box source"><span class="arch-icon">📊</span><div><div class="arch-label">Market Intel</div><div class="arch-sublabel">Competitor Data</div></div></div><div class="arch-box source"><span class="arch-icon">📄</span><div><div class="arch-label">Documents</div><div class="arch-sublabel">Policies & Strategy</div></div></div></div><div class="arch-pipes" style="height: 340px;"><div class="arch-pipe" style="top: 6%;"><div class="arch-dot" style="animation-delay: 0s;"></div></div><div class="arch-pipe" style="top: 16%;"><div class="arch-dot" style="animation-delay: 0.25s;"></div></div><div class="arch-pipe" style="top: 26%;"><div class="arch-dot" style="animation-delay: 0.5s;"></div></div><div class="arch-pipe" style="top: 36%;"><div class="arch-dot" style="animation-delay: 0.75s;"></div></div><div class="arch-pipe" style="top: 46%;"><div class="arch-dot" style="animation-delay: 1s;"></div></div><div class="arch-pipe" style="top: 56%;"><div class="arch-dot" style="animation-delay: 1.25s;"></div></div><div class="arch-pipe" style="top: 66%;"><div class="arch-dot" style="animation-delay: 1.5s;"></div></div><div class="arch-pipe" style="top: 76%;"><div class="arch-dot" style="animation-delay: 1.75s;"></div></div><div class="arch-pipe" style="top: 86%;"><div class="arch-dot" style="animation-delay: 2s;"></div></div><div class="arch-pipe" style="top: 96%;"><div class="arch-dot" style="animation-delay: 2.25s;"></div></div></div><div class="arch-center"><div class="arch-center-title">❄️ Snowflake</div><div class="arch-center-sub">AI Data Cloud</div><div class="arch-center-features"><span class="arch-feature">Cortex AI</span><span class="arch-feature">ML Models</span><span class="arch-feature">Semantic Views</span><span class="arch-feature">Search</span><span class="arch-feature">Notebooks</span><span class="arch-feature">Streamlit</span></div></div><div class="arch-pipes" style="height: 340px;"><div class="arch-pipe out" style="top: 6%;"><div class="arch-dot" style="animation-delay: 0.1s;"></div></div><div class="arch-pipe out" style="top: 16%;"><div class="arch-dot" style="animation-delay: 0.35s;"></div></div><div class="arch-pipe out" style="top: 26%;"><div class="arch-dot" style="animation-delay: 0.6s;"></div></div><div class="arch-pipe out" style="top: 36%;"><div class="arch-dot" style="animation-delay: 0.85s;"></div></div><div class="arch-pipe out" style="top: 46%;"><div class="arch-dot" style="animation-delay: 1.1s;"></div></div><div class="arch-pipe out" style="top: 56%;"><div class="arch-dot" style="animation-delay: 1.35s;"></div></div><div class="arch-pipe out" style="top: 66%;"><div class="arch-dot" style="animation-delay: 1.6s;"></div></div><div class="arch-pipe out" style="top: 76%;"><div class="arch-dot" style="animation-delay: 1.85s;"></div></div><div class="arch-pipe out" style="top: 86%;"><div class="arch-dot" style="animation-delay: 2.1s;"></div></div><div class="arch-pipe out" style="top: 96%;"><div class="arch-dot" style="animation-delay: 2.35s;"></div></div></div><div class="arch-column"><div class="arch-section-label">Intelligence</div><div class="arch-box output"><span class="arch-icon">🧠</span><div><div class="arch-label">Snowflake Intelligence</div><div class="arch-sublabel">Natural Language</div></div></div><div class="arch-box output"><span class="arch-icon">📊</span><div><div class="arch-label">Dashboards</div><div class="arch-sublabel">32 Executive Views</div></div></div><div class="arch-box output"><span class="arch-icon">🔮</span><div><div class="arch-label">Churn Model</div><div class="arch-sublabel">ML Predictions</div></div></div><div class="arch-box output"><span class="arch-icon">📈</span><div><div class="arch-label">Upsell Model</div><div class="arch-sublabel">Propensity Scores</div></div></div><div class="arch-box output"><span class="arch-icon">🔍</span><div><div class="arch-label">Document Search</div><div class="arch-sublabel">7 Collections</div></div></div><div class="arch-box output"><span class="arch-icon">📋</span><div><div class="arch-label">Semantic Views</div><div class="arch-sublabel">34 Business Domains</div></div></div><div class="arch-box output"><span class="arch-icon">💡</span><div><div class="arch-label">Real-time Insights</div><div class="arch-sublabel">Live Analytics</div></div></div><div class="arch-box output"><span class="arch-icon">🎯</span><div><div class="arch-label">Analyst Tools</div><div class="arch-sublabel">41 AI Tools</div></div></div><div class="arch-box output"><span class="arch-icon">📱</span><div><div class="arch-label">Streamlit Apps</div><div class="arch-sublabel">Interactive UI</div></div></div><div class="arch-box output"><span class="arch-icon">📝</span><div><div class="arch-label">Notebooks</div><div class="arch-sublabel">Data Science</div></div></div></div></div></div>""", unsafe_allow_html=True)

    st.markdown("""<div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #6B7280; font-size: 0.8rem;">Learn more at <a href="https://www.snowflake.com/en/solutions/industries/telecom/" target="_blank" style="color: #29B5E8;">snowflake.com/telecom</a></div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Executive Overview
# ---------------------------------------------------------------------------
elif selected_menu == "Executive Overview":
    import pandas as pd
    import altair as alt
    import numpy as np

    EXEC_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "title_color": "#0F172A",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
        "accent_blue": "#29B5E8",
        "accent_indigo": "#6366F1",
        "accent_green": "#10B981",
        "accent_amber": "#F59E0B",
        "accent_purple": "#8B5CF6",
        "accent_red": "#EF4444",
    }

    def style_exec_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_title(
                font=EXEC_CHART_THEME["font"],
                fontSize=15,
                fontWeight=700,
                color=EXEC_CHART_THEME["title_color"],
                anchor="start",
            )
            .configure_axis(
                labelFont=EXEC_CHART_THEME["font"],
                titleFont=EXEC_CHART_THEME["font"],
                labelColor=EXEC_CHART_THEME["label_color"],
                titleColor=EXEC_CHART_THEME["label_color"],
                labelFontSize=11,
                titleFontSize=12,
                domain=False,
                tickColor=EXEC_CHART_THEME["grid_color"],
                gridColor=EXEC_CHART_THEME["grid_color"],
                gridOpacity=0.75,
            )
            .configure_legend(
                labelFont=EXEC_CHART_THEME["font"],
                titleFont=EXEC_CHART_THEME["font"],
                labelColor=EXEC_CHART_THEME["label_color"],
                titleColor=EXEC_CHART_THEME["label_color"],
                orient="top",
                direction="horizontal",
                symbolType="circle",
                symbolSize=110,
                padding=8,
            )
        )

    def render_ai_recommendation(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        st.markdown(
            f"""<div class="ai-rec-card {level}"><div class="ai-rec-head">🤖 AI Recommendation · {headline}</div><div class="ai-rec-line"><strong>Insight:</strong> {insight}</div><div class="ai-rec-line"><strong>Action:</strong> {action}</div><div class="ai-rec-line"><strong>Expected Impact:</strong> {impact}</div></div>""",
            unsafe_allow_html=True,
        )

    # ── Animated CSS for Executive Overview ────────────────────────────
    st.markdown("""<style>
@keyframes pulse-ring { 0%,100% { transform: scale(0.95); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.8; } }
@keyframes value-count { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes trend-arrow { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@keyframes exec-metric-glow { 0%,100% { box-shadow: 0 2px 4px rgba(0,0,0,0.05); } 50% { box-shadow: 0 4px 20px rgba(41,181,232,0.20); } }
@keyframes icon-bounce { 0%,100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-4px) scale(1.1); } }
@keyframes metric-number-pop { 0% { opacity: 0; transform: scale(0.5) translateY(10px); } 60% { transform: scale(1.1) translateY(-3px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes metric-text-glow { 0%,100% { text-shadow: none; } 50% { text-shadow: 0 0 12px currentColor; } }
@keyframes shimmer-sweep { 0% { left: -100%; } 100% { left: 200%; } }
@keyframes live-pulse { 0%,100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.3); opacity: 1; } }
@keyframes pulse-dot-ring { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(2.5); opacity: 0; } }
@keyframes kpi-accent-pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
@keyframes kpi-value-pop { 0% { opacity: 0; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1); } }
@keyframes kpi-line-pulse { 0%,100% { stroke-width: 2; opacity: 0.25; } 50% { stroke-width: 4; opacity: 0.4; } }
@keyframes kpi-fill-pulse { 0%,100% { opacity: 0.2; transform: scaleY(1); } 50% { opacity: 0.35; transform: scaleY(1.05); } }
@keyframes kpi-bar-wave { 0%,100% { transform: scaleY(1); opacity: 0.25; } 50% { transform: scaleY(0.65); opacity: 0.4; } }
@keyframes eo-title-rise { 0% { opacity: 0; transform: translateY(8px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes eo-title-shimmer { 0% { left: -35%; } 100% { left: 120%; } }
@keyframes eo-dot-pulse { 0%,100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.25); opacity: 1; } }
.eo-title {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.3rem 0 0.85rem;
    padding: 0.62rem 0.9rem;
    border-radius: 12px;
    border: 1px solid #DBEAFE;
    background: linear-gradient(135deg, #F0F8FF 0%, #EEF2FF 100%);
    color: #1B2A4E;
    font-weight: 700;
    font-size: 1.04rem;
    letter-spacing: 0.01em;
    animation: eo-title-rise 0.4s ease-out both;
}
.eo-title::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #29B5E8, #6366F1);
    animation: eo-dot-pulse 1.8s ease-in-out infinite;
}
.eo-title::after {
    content: "";
    position: absolute;
    top: 0;
    left: -35%;
    width: 30%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
    animation: eo-title-shimmer 3.2s ease-in-out infinite;
}
.eo-mini-title {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin: 0.15rem 0 0.55rem;
    color: #1E3A8A;
    font-size: 0.93rem;
    font-weight: 700;
    animation: eo-title-rise 0.35s ease-out both;
}
.eo-mini-title::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, #22C1EE, #8B5CF6);
}
.business-pulse { background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%); border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid #BFDBFE; position: relative; overflow: hidden; }
.business-pulse::before { content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(41,181,232,0.1), transparent); animation: shimmer-sweep 3s ease-in-out infinite; }
.pulse-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; position: relative; z-index: 1; }
.pulse-title { color: #1B2A4E; font-size: 1.1rem; font-weight: 600; }
.pulse-live { display: inline-flex; align-items: center; gap: 0.5rem; }
.pulse-dot { width: 10px; height: 10px; background: #10B981; border-radius: 50%; animation: live-pulse 1.5s ease-in-out infinite; position: relative; }
.pulse-dot::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #10B981; border-radius: 50%; animation: pulse-dot-ring 1.5s ease-out infinite; }
.pulse-period { color: #10B981; font-size: 0.8rem; font-weight: 500; }
.pulse-metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; position: relative; z-index: 1; }
.pulse-metric { background: white; border-radius: 12px; padding: 1.25rem; text-align: center; border: 1px solid #E2E8F0; animation: exec-metric-glow 3s ease-in-out infinite; transition: all 0.3s ease; }
.pulse-metric:nth-child(1) { animation-delay: 0s; }
.pulse-metric:nth-child(2) { animation-delay: 0.5s; }
.pulse-metric:nth-child(3) { animation-delay: 1s; }
.pulse-metric:nth-child(4) { animation-delay: 1.5s; }
.pulse-metric:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(41,181,232,0.2); }
.pm-icon { font-size: 1.5rem; margin-bottom: 0.5rem; animation: icon-bounce 2s ease-in-out infinite; display: inline-block; }
.pulse-metric:nth-child(1) .pm-icon { animation-delay: 0s; }
.pulse-metric:nth-child(2) .pm-icon { animation-delay: 0.3s; }
.pulse-metric:nth-child(3) .pm-icon { animation-delay: 0.6s; }
.pulse-metric:nth-child(4) .pm-icon { animation-delay: 0.9s; }
.pm-val { font-size: 1.8rem; font-weight: 700; color: #1B2A4E; animation: metric-number-pop 0.6s ease-out forwards, metric-text-glow 3s ease-in-out 0.6s infinite; opacity: 0; }
.pulse-metric:nth-child(2) .pm-val { animation-delay: 0.15s, 0.75s; }
.pulse-metric:nth-child(3) .pm-val { animation-delay: 0.3s, 0.9s; }
.pulse-metric:nth-child(4) .pm-val { animation-delay: 0.45s, 1.05s; }
.pm-val.revenue { color: #10B981; }
.pm-val.customers { color: #29B5E8; }
.pm-val.nps { color: #F59E0B; }
.pm-val.growth { color: #8B5CF6; }
.pm-name { font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem; }
.pm-trend { font-size: 0.8rem; margin-top: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 0.25rem; }
.pm-trend.up { color: #10B981; }
.pm-trend.up span { animation: trend-arrow 1s ease-in-out infinite; display: inline-block; }
.eo-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem; }
.eo-kpi { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; position: relative; overflow: hidden; transition: all 0.3s ease; animation: exec-metric-glow 3s ease-in-out infinite; }
.eo-kpi:nth-child(1) { animation-delay: 0s; }
.eo-kpi:nth-child(2) { animation-delay: 0.4s; }
.eo-kpi:nth-child(3) { animation-delay: 0.8s; }
.eo-kpi:nth-child(4) { animation-delay: 1.2s; }
.eo-kpi:hover { border-color: #29B5E8; box-shadow: 0 8px 25px rgba(41,181,232,0.25) !important; transform: translateY(-4px); }
.eo-kpi::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: var(--accent); animation: kpi-accent-pulse 2s ease-in-out infinite; }
.eo-kpi-label { font-size: 0.8rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.eo-kpi-value { font-size: 2rem; font-weight: 700; color: #1B2A4E; line-height: 1.1; animation: kpi-value-pop 0.6s ease-out forwards; opacity: 0; }
.eo-kpi:nth-child(2) .eo-kpi-value { animation-delay: 0.1s; }
.eo-kpi:nth-child(3) .eo-kpi-value { animation-delay: 0.2s; }
.eo-kpi:nth-child(4) .eo-kpi-value { animation-delay: 0.3s; }
.eo-kpi-delta { display: inline-flex; align-items: center; font-size: 0.85rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 20px; margin-top: 0.5rem; }
.eo-kpi-delta.positive { background: #D1FAE5; color: #059669; }
.eo-kpi-delta.negative { background: #FEE2E2; color: #DC2626; }
.eo-kpi-delta.neutral { background: #F3F4F6; color: #6B7280; }
.eo-kpi-icon { position: absolute; top: 1rem; right: 1rem; font-size: 1.5rem; opacity: 0.3; }
.eo-kpi .kpi-chart { position: absolute; bottom: 0; left: 0; right: 0; height: 45px; opacity: 0.25; }
.eo-kpi .kpi-chart path[fill="none"] { animation: kpi-line-pulse 2s ease-in-out infinite; }
.eo-kpi .kpi-chart path[fill]:not([fill="none"]) { transform-origin: bottom; animation: kpi-fill-pulse 2.5s ease-in-out infinite; }
.eo-kpi .kpi-chart rect { transform-origin: bottom; animation: kpi-bar-wave 1.5s ease-in-out infinite; }
.exec-summary-shell { margin-top: 0.25rem; }
.exec-summary-hero {
    position: relative;
    overflow: hidden;
    border-radius: 14px;
    border: 1px solid #BFDBFE;
    background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
    padding: 1rem 1.1rem;
    margin-bottom: 0.9rem;
}
.exec-summary-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: -110%;
    width: 55%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(41,181,232,0.22), transparent);
    animation: shimmer-sweep 3.2s ease-in-out infinite;
}
.exec-summary-title {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    color: #1E3A8A;
    font-weight: 700;
    font-size: 0.98rem;
}
.exec-summary-sub {
    position: relative;
    z-index: 1;
    margin-top: 0.38rem;
    color: #334155;
    font-size: 0.9rem;
}
.exec-summary-grid {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    gap: 0.8rem;
}
.exec-summary-panel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 0.95rem 1rem;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}
.exec-summary-panel h4 {
    margin: 0 0 0.62rem 0;
    color: #1B2A4E;
    font-size: 0.94rem;
    font-weight: 700;
}
.exec-summary-kpis {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.55rem;
}
.exec-summary-kpi {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%);
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.62rem 0.7rem;
}
.exec-summary-kpi .v {
    color: #0F172A;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.2;
}
.exec-summary-kpi .l {
    margin-top: 0.12rem;
    color: #64748B;
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.exec-summary-list {
    margin: 0;
    padding-left: 1.08rem;
    color: #334155;
}
.exec-summary-list li {
    margin: 0.38rem 0;
    line-height: 1.32;
    font-size: 0.9rem;
}
.exec-summary-actions {
    margin: 0;
    padding-left: 1.05rem;
    color: #1E293B;
}
.exec-summary-actions li {
    margin: 0.42rem 0;
    line-height: 1.35;
    font-size: 0.9rem;
}
@keyframes cxo-fade-up {
    0% { opacity: 0; transform: translateY(12px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes cxo-urgent-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.30); }
    50% { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
}
@keyframes cxo-flow {
    0% { left: -35%; }
    100% { left: 120%; }
}
@keyframes cxo-bar-fill {
    0% { width: 0; }
    100% { width: var(--p); }
}
.cxo-snapshot {
    position: relative;
    overflow: hidden;
    background: linear-gradient(130deg, #0F172A 0%, #1E3A8A 62%, #1D4ED8 100%);
    border-radius: 14px;
    border: 1px solid rgba(191, 219, 254, 0.5);
    padding: 1rem 1.1rem;
    margin-bottom: 0.95rem;
    animation: cxo-fade-up 0.5s ease-out both;
}
.cxo-snapshot::after {
    content: "";
    position: absolute;
    top: 0;
    left: -35%;
    width: 30%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
    animation: cxo-flow 4s ease-in-out infinite;
}
.cxo-snapshot-title {
    color: #DBEAFE;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.35rem;
    position: relative;
    z-index: 1;
}
.cxo-snapshot-text {
    color: #F8FAFC;
    font-size: 0.96rem;
    line-height: 1.4;
    font-weight: 600;
    position: relative;
    z-index: 1;
}
.cxo-snapshot-risk {
    margin-top: 0.6rem;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.25rem 0.55rem;
    border-radius: 999px;
    background: rgba(239,68,68,0.18);
    color: #FECACA;
    font-size: 0.78rem;
    font-weight: 700;
    border: 1px solid rgba(252,165,165,0.45);
    position: relative;
    z-index: 1;
    animation: cxo-urgent-pulse 2.1s ease-in-out infinite;
}
.cxo-value-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}
.cxo-value-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
    position: relative;
    overflow: hidden;
    animation: cxo-fade-up 0.45s ease-out both;
}
.cxo-value-card:nth-child(1) { animation-delay: 0.05s; }
.cxo-value-card:nth-child(2) { animation-delay: 0.12s; }
.cxo-value-card:nth-child(3) { animation-delay: 0.2s; }
.cxo-value-card:nth-child(4) { animation-delay: 0.28s; }
.cxo-value-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 3px;
    background: var(--accent);
}
.cxo-value-label {
    color: #64748B;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.2rem;
}
.cxo-value-number {
    color: #0F172A;
    font-size: 1.35rem;
    font-weight: 800;
    line-height: 1.2;
}
.cxo-value-note {
    margin-top: 0.25rem;
    color: #334155;
    font-size: 0.78rem;
}
.cxo-value-note.urgent { color: #B91C1C; font-weight: 700; }
.cxo-decision-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 0.8rem;
}
.cxo-decision {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
    animation: cxo-fade-up 0.45s ease-out both;
}
.cxo-decision:nth-child(1) { animation-delay: 0.08s; }
.cxo-decision:nth-child(2) { animation-delay: 0.16s; }
.cxo-decision:nth-child(3) { animation-delay: 0.24s; }
.cxo-decision-title {
    color: #0F172A;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.cxo-decision-meta {
    color: #334155;
    font-size: 0.8rem;
    line-height: 1.36;
}
.cxo-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.46rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.cxo-badge.high { background: #FEE2E2; color: #991B1B; }
.cxo-badge.med { background: #FEF3C7; color: #92400E; }
.cxo-badge.ok { background: #DCFCE7; color: #166534; }
.cxo-initiatives {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
}
.cxo-initiative {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
    animation: cxo-fade-up 0.45s ease-out both;
}
.cxo-init-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.35rem;
}
.cxo-init-title {
    color: #0F172A;
    font-size: 0.88rem;
    font-weight: 700;
}
.cxo-rag {
    font-size: 0.67rem;
    font-weight: 700;
    border-radius: 999px;
    padding: 0.15rem 0.42rem;
}
.cxo-rag.green { background: #DCFCE7; color: #166534; }
.cxo-rag.amber { background: #FEF3C7; color: #92400E; }
.cxo-rag.red { background: #FEE2E2; color: #991B1B; animation: cxo-urgent-pulse 2s ease-in-out infinite; }
.cxo-init-meta {
    color: #475569;
    font-size: 0.76rem;
    margin-bottom: 0.44rem;
}
.cxo-progress {
    width: 100%;
    height: 8px;
    border-radius: 999px;
    background: #E2E8F0;
    overflow: hidden;
    margin-bottom: 0.35rem;
}
.cxo-progress > span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #29B5E8, #1D4ED8);
    width: var(--p);
    animation: cxo-bar-fill 1.2s ease-out both;
}
.cxo-init-foot {
    color: #334155;
    font-size: 0.76rem;
}
.cxo-board {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.85rem 0.9rem;
}
.cxo-board-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
}
.cxo-board-cell {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.55rem 0.6rem;
}
.cxo-board-cell h5 {
    margin: 0 0 0.2rem 0;
    color: #1E3A8A;
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.cxo-board-cell p {
    margin: 0;
    color: #334155;
    font-size: 0.8rem;
    line-height: 1.35;
}
.ai-rec-card {
    margin-top: 0.65rem;
    border-radius: 10px;
    border: 1px solid #D1E9FF;
    background: linear-gradient(135deg, #F8FBFF 0%, #EEF6FF 100%);
    padding: 0.62rem 0.78rem;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    animation: cxo-fade-up 0.35s ease-out both;
}
.ai-rec-card .ai-rec-head {
    color: #1E3A8A;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.28rem;
    letter-spacing: 0.02em;
}
.ai-rec-card .ai-rec-line {
    color: #334155;
    font-size: 0.77rem;
    line-height: 1.34;
    margin: 0.12rem 0;
}
.ai-rec-card.warning {
    border-color: #FCD34D;
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
}
.ai-rec-card.warning .ai-rec-head {
    color: #92400E;
}
.ai-rec-card.critical {
    border-color: #FCA5A5;
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
}
.ai-rec-card.critical .ai-rec-head {
    color: #991B1B;
}
@media (max-width: 768px) { .pulse-metrics, .eo-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 980px) { .exec-summary-grid { grid-template-columns: 1fr; } }
@media (max-width: 980px) { .cxo-value-grid, .cxo-decision-grid, .cxo-board-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 980px) { .cxo-initiatives { grid-template-columns: 1fr; } }
@media (max-width: 720px) { .cxo-value-grid, .cxo-decision-grid, .cxo-board-grid { grid-template-columns: 1fr; } }
</style>""", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # Synthetic "warehouse-consistent" dataset for all executive metrics
    # -------------------------------------------------------------------
    db_segment_perf = pd.DataFrame({
        "Segment": ["Consumer", "SMB", "Enterprise"],
        "Subscribers": [20500, 7600, 2147],
        "Monthly Revenue M": [2.6, 1.2, 0.6],
        "NPS": [44, 52, 61],
        "Churn %": [2.4, 1.9, 1.1],
    })
    db_risk = pd.DataFrame({
        "Segment": ["Budget", "Standard", "Premium", "VIP"],
        "At Risk": [312, 289, 178, 68],
        "Revenue at Risk K": [95, 78, 51, 16],
        "Avg Propensity": [0.78, 0.65, 0.52, 0.41],
    })
    db_network_regions = pd.DataFrame({
        "Region": ["Santiago Centro", "Santiago Norte", "Santiago Sur", "Maipu", "Concepcion", "Valparaiso"],
        "Network Score": [95.1, 92.4, 90.8, 91.7, 89.9, 88.7],
        "NPS": [54, 49, 45, 47, 42, 39],
        "Incidents": [18, 24, 29, 26, 34, 38],
    })
    db_incident_trend = pd.DataFrame({
        "Week": ["W1", "W2", "W3", "W4", "W5", "W6"],
        "Major Incidents": [22, 20, 18, 19, 16, 14],
        "MTTR Minutes": [62, 59, 57, 55, 52, 49],
    })

    active_subscribers = int(db_segment_perf["Subscribers"].sum())
    monthly_revenue_m = round(float(db_segment_perf["Monthly Revenue M"].sum()), 1)
    quarterly_revenue_m = round(monthly_revenue_m * 3, 1)
    arpu_blended = round((monthly_revenue_m * 1_000_000) / active_subscribers, 2)
    nps_score = int(round((db_segment_perf["NPS"] * db_segment_perf["Subscribers"]).sum() / active_subscribers, 0))
    churn_rate = round(float((db_segment_perf["Churn %"] * db_segment_perf["Subscribers"]).sum() / active_subscribers), 1)
    at_risk_revenue_m = round(float(db_risk["Revenue at Risk K"].sum()) * 12 / 1000, 1)
    at_risk_customers = int(db_risk["At Risk"].sum())
    market_share = 5.2
    net_adds = 257
    network_availability = 99.7
    support_csat = 4.2
    arpu_delta = "+CLP 3.8"
    value_in_flight_m = 1.6
    protectable_arr_m = round(at_risk_revenue_m * 0.6, 1)

    # ── Real-Time Business Pulse ──────────────────────────────────────
    st.markdown(
        f"""<div class="business-pulse"><div class="pulse-header"><div class="pulse-live"><div class="pulse-dot"></div><span class="pulse-title">📊 Real-Time Business Pulse</span></div><div class="pulse-period">● Live</div></div><div class="pulse-metrics"><div class="pulse-metric"><div class="pm-icon">💰</div><div class="pm-val revenue">CLP {monthly_revenue_m:.1f}M</div><div class="pm-name">Monthly Revenue</div><div class="pm-trend up"><span>↑</span> +8.4% vs target</div></div><div class="pulse-metric"><div class="pm-icon">👥</div><div class="pm-val customers">{active_subscribers:,}</div><div class="pm-name">Active Subscribers</div><div class="pm-trend up"><span>↑</span> +{net_adds} net adds</div></div><div class="pulse-metric"><div class="pm-icon">⭐</div><div class="pm-val nps">+{nps_score}</div><div class="pm-name">NPS Score</div><div class="pm-trend up"><span>↑</span> +5 pts QoQ</div></div><div class="pulse-metric"><div class="pm-icon">📈</div><div class="pm-val growth">{market_share:.1f}%</div><div class="pm-name">Market Share</div><div class="pm-trend up"><span>↑</span> +0.4% YoY</div></div></div></div>""",
        unsafe_allow_html=True,
    )

    overview_tab, ai_summary_tab = st.tabs(["📈 Executive Overview", "🤖 AI Strategy"])

    with overview_tab:
        # ── Business Health at a Glance ───────────────────────────────────
        st.markdown('<div class="eo-title">Business Health at a Glance</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="eo-kpi-grid"><div class="eo-kpi" style="--accent: #29B5E8;"><div class="eo-kpi-icon">👥</div><div class="eo-kpi-label">Total Subscribers</div><div class="eo-kpi-value">{active_subscribers:,}</div><div class="eo-kpi-delta positive">↑ +5.2% QoQ</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0,35 L15,32 L30,28 L45,25 L60,20 L75,15 L100,8" fill="none" stroke="#29B5E8" stroke-width="2"/><path d="M0,35 L15,32 L30,28 L45,25 L60,20 L75,15 L100,8 L100,40 L0,40 Z" fill="#29B5E8"/></svg></div><div class="eo-kpi" style="--accent: #10B981;"><div class="eo-kpi-icon">💰</div><div class="eo-kpi-label">Quarterly Revenue</div><div class="eo-kpi-value">CLP {quarterly_revenue_m:.1f}M</div><div class="eo-kpi-delta positive">↑ +8.4% YoY</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0,32 L15,30 L30,26 L45,28 L60,20 L75,14 L100,8" fill="none" stroke="#10B981" stroke-width="2"/><path d="M0,32 L15,30 L30,26 L45,28 L60,20 L75,14 L100,8 L100,40 L0,40 Z" fill="#10B981"/></svg></div><div class="eo-kpi" style="--accent: #8B5CF6;"><div class="eo-kpi-icon">⭐</div><div class="eo-kpi-label">NPS Score</div><div class="eo-kpi-value">+{nps_score}</div><div class="eo-kpi-delta positive">↑ +5 pts</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><rect x="5" y="28" width="10" height="12" fill="#8B5CF6"/><rect x="20" y="24" width="10" height="16" fill="#8B5CF6"/><rect x="35" y="26" width="10" height="14" fill="#8B5CF6"/><rect x="50" y="20" width="10" height="20" fill="#8B5CF6"/><rect x="65" y="16" width="10" height="24" fill="#8B5CF6"/><rect x="80" y="12" width="10" height="28" fill="#8B5CF6"/></svg></div><div class="eo-kpi" style="--accent: #F59E0B;"><div class="eo-kpi-icon">📉</div><div class="eo-kpi-label">Churn Rate</div><div class="eo-kpi-value">{churn_rate:.1f}%</div><div class="eo-kpi-delta positive">↓ -0.7%</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0,8 L15,12 L30,16 L45,18 L60,22 L75,28 L100,32" fill="none" stroke="#F59E0B" stroke-width="2"/><path d="M0,8 L15,12 L30,16 L45,18 L60,22 L75,28 L100,32 L100,40 L0,40 Z" fill="#F59E0B"/></svg></div></div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="eo-kpi-grid"><div class="eo-kpi" style="--accent: #06B6D4;"><div class="eo-kpi-icon">📡</div><div class="eo-kpi-label">Network Availability</div><div class="eo-kpi-value">{network_availability:.1f}%</div><div class="eo-kpi-delta positive">↑ +0.2%</div></div><div class="eo-kpi" style="--accent: #EC4899;"><div class="eo-kpi-icon">📊</div><div class="eo-kpi-label">ARPU (Blended)</div><div class="eo-kpi-value">CLP {arpu_blended:.2f}</div><div class="eo-kpi-delta positive">↑ {arpu_delta}</div></div><div class="eo-kpi" style="--accent: #14B8A6;"><div class="eo-kpi-icon">💬</div><div class="eo-kpi-label">Support CSAT</div><div class="eo-kpi-value">{support_csat:.1f}/5</div><div class="eo-kpi-delta positive">↑ +0.3</div></div><div class="eo-kpi" style="--accent: #EF4444;"><div class="eo-kpi-icon">⚠️</div><div class="eo-kpi-label">At-Risk Revenue</div><div class="eo-kpi-value">CLP {at_risk_revenue_m:.1f}M</div><div class="eo-kpi-delta neutral">{int(db_risk['At Risk'].sum())} customers</div></div></div>""", unsafe_allow_html=True)

        # ── Executive Performance Signals (Altair charts) ──────────────────
        st.markdown('<div class="eo-title">Executive Performance Signals</div>', unsafe_allow_html=True)
        exec_col1, exec_col2 = st.columns(2)

        with exec_col1:
            st.markdown('<div class="eo-mini-title">Revenue Mix by Segment</div>', unsafe_allow_html=True)
            with st.container(border=True):
                seg_df = db_segment_perf[["Segment", "Monthly Revenue M"]].rename(columns={"Monthly Revenue M": "Revenue"})
                seg_bar = (
                    alt.Chart(seg_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22)
                    .encode(
                        x=alt.X('Revenue:Q', title='Revenue (CLP  M)', axis=alt.Axis(format=".1f", tickCount=6)),
                        y=alt.Y('Segment:N', sort='-x', title=None),
                        color=alt.Color(
                            'Segment:N',
                            scale=alt.Scale(
                                domain=['Consumer', 'SMB', 'Enterprise'],
                                range=[
                                    EXEC_CHART_THEME["accent_blue"],
                                    "#1D9ED3",
                                    "#1677A5",
                                ],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Segment:N', title='Segment'),
                            alt.Tooltip('Revenue:Q', title='Revenue', format='.2f'),
                        ],
                    )
                )
                seg_text = alt.Chart(seg_df).mark_text(align="left", dx=6, fontSize=11, color="#0F172A").encode(
                    x='Revenue:Q',
                    y=alt.Y('Segment:N', sort='-x'),
                    text=alt.Text('Revenue:Q', format='.1f'),
                )
                st.altair_chart(style_exec_chart(seg_bar + seg_text, height=190), use_container_width=True)
                top_seg = seg_df.loc[seg_df["Revenue"].idxmax()]
                render_ai_recommendation(
                    "Revenue Mix",
                    f"{top_seg['Segment']} contributes the largest monthly revenue at CLP {top_seg['Revenue']:.1f}M.",
                    f"Protect {top_seg['Segment']} with loyalty bundles while accelerating SMB conversion playbooks.",
                    "Stabilize core revenue base and add +CLP 0.3M in 1 quarter.",
                )

        with exec_col2:
            st.markdown('<div class="eo-mini-title">NPS vs Churn Risk</div>', unsafe_allow_html=True)
            with st.container(border=True):
                churn_df = pd.DataFrame({
                    'Segment': db_segment_perf['Segment'],
                    'NPS': db_segment_perf['NPS'],
                    'Churn': db_segment_perf['Churn %'],
                })
                churn_scatter = (
                    alt.Chart(churn_df)
                    .mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.8)
                    .encode(
                        x=alt.X('NPS:Q', title='NPS', scale=alt.Scale(domain=[40, 66])),
                        y=alt.Y('Churn:Q', title='Churn %', scale=alt.Scale(domain=[0.8, 2.6])),
                        size=alt.Size('NPS:Q', legend=None, scale=alt.Scale(range=[180, 520])),
                        color=alt.Color(
                            'Segment:N',
                            scale=alt.Scale(
                                domain=['Consumer', 'SMB', 'Enterprise'],
                                range=[
                                    EXEC_CHART_THEME["accent_blue"],
                                    EXEC_CHART_THEME["accent_green"],
                                    EXEC_CHART_THEME["accent_purple"],
                                ],
                            ),
                            legend=alt.Legend(title=None),
                        ),
                        tooltip=[
                            alt.Tooltip('Segment:N', title='Segment'),
                            alt.Tooltip('NPS:Q', title='NPS'),
                            alt.Tooltip('Churn:Q', title='Churn %', format='.1f'),
                        ],
                    )
                )
                trend_line = churn_scatter.transform_regression('NPS', 'Churn').mark_line(
                    strokeDash=[5, 5],
                    color="#64748B",
                    size=2,
                    opacity=0.9,
                )
                point_labels = alt.Chart(churn_df).mark_text(dy=-14, fontSize=10, color="#334155").encode(
                    x='NPS:Q',
                    y='Churn:Q',
                    text='Segment:N',
                )
                st.altair_chart(style_exec_chart(trend_line + churn_scatter + point_labels, height=190), use_container_width=True)
                worst_seg = churn_df.loc[churn_df["Churn"].idxmax()]
                render_ai_recommendation(
                    "NPS vs Churn",
                    f"{worst_seg['Segment']} shows the highest churn ({worst_seg['Churn']:.1f}%) and the lowest relative NPS.",
                    f"Launch a segment-specific retention sprint for {worst_seg['Segment']} with service-credit triggers.",
                    "Reduce blended churn by ~0.2pp in 60 days.",
                    level="warning",
                )

        # ── Revenue Bridge ─────────────────────────────────────────────────
        st.markdown('<div class="eo-title">Revenue Bridge (YoY)</div>', unsafe_allow_html=True)
        with st.container(border=True):
            bridge_df = pd.DataFrame({
                'Driver': ['Base', 'Volume', 'Price', 'Mix', 'Churn', 'Discounts', 'Current'],
                'Impact': [12.0, 0.9, 0.5, 0.4, -0.4, -0.2, quarterly_revenue_m],
                'Type': ['Total', 'Up', 'Up', 'Up', 'Down', 'Down', 'Total'],
            })
            bridge_df['Label'] = bridge_df['Impact'].apply(lambda v: f"{v:+.1f}M" if v not in [12.0, quarterly_revenue_m] else f"{v:.1f}M")
            bridge_bar = alt.Chart(bridge_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                x=alt.X('Driver:N', title=None, sort=list(bridge_df['Driver']), axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Impact:Q', title='CLP  M'),
                color=alt.Color(
                    'Type:N',
                    scale=alt.Scale(
                        domain=['Up', 'Down', 'Total'],
                        range=[
                            EXEC_CHART_THEME["accent_green"],
                            EXEC_CHART_THEME["accent_red"],
                            "#3B82F6",
                        ],
                    ),
                    legend=alt.Legend(title=None),
                ),
                tooltip=[
                    alt.Tooltip('Driver:N', title='Driver'),
                    alt.Tooltip('Impact:Q', title='Impact', format='.1f'),
                    alt.Tooltip('Type:N', title='Type'),
                ],
            )
            bridge_text = alt.Chart(bridge_df).mark_text(dy=-8, fontSize=10, fontWeight='bold').encode(
                x=alt.X('Driver:N', sort=list(bridge_df['Driver'])),
                y='Impact:Q',
                text='Label:N',
                color=alt.value('#1B2A4E'),
            )
            baseline = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeDash=[4, 4], color="#94A3B8").encode(y="y:Q")
            st.altair_chart(style_exec_chart(baseline + bridge_bar + bridge_text, height=210), use_container_width=True)
            up_driver = bridge_df[bridge_df["Type"] == "Up"].sort_values("Impact", ascending=False).iloc[0]
            down_driver = bridge_df[bridge_df["Type"] == "Down"].sort_values("Impact").iloc[0]
            render_ai_recommendation(
                "Revenue Bridge",
                f"Biggest uplift comes from {up_driver['Driver']} (+CLP {up_driver['Impact']:.1f}M) while {down_driver['Driver']} is the main drag ({down_driver['Impact']:.1f}M).",
                f"Double down on {up_driver['Driver']} levers and assign an owner to recover losses from {down_driver['Driver']}.",
                "Protect ~CLP 0.4M and improve run-rate predictability.",
            )

        # ── ARPU & Plan Mix ───────────────────────────────────────────────
        st.markdown('<div class="eo-title">ARPU & Plan Mix</div>', unsafe_allow_html=True)
        arpu_col, mix_col = st.columns(2)
        with arpu_col:
            st.markdown('<div class="eo-mini-title">ARPU by Segment</div>', unsafe_allow_html=True)
            with st.container(border=True):
                arpu_df = db_segment_perf.copy()
                arpu_df['ARPU'] = (arpu_df['Monthly Revenue M'] * 1_000_000 / arpu_df['Subscribers']).round(0)
                arpu_df = arpu_df[['Segment', 'ARPU']]
                arpu_bar = (
                    alt.Chart(arpu_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22)
                    .encode(
                        x=alt.X('ARPU:Q', title='ARPU (CLP )', axis=alt.Axis(tickCount=6)),
                        y=alt.Y('Segment:N', sort='-x', title=None),
                        color=alt.Color(
                            'Segment:N',
                            scale=alt.Scale(
                                domain=['Enterprise', 'SMB', 'Consumer'],
                                range=["#0F766E", "#14B8A6", "#22D3EE"],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Segment:N', title='Segment'),
                            alt.Tooltip('ARPU:Q', title='ARPU', format='.0f'),
                        ],
                    )
                )
                st.altair_chart(style_exec_chart(arpu_bar, height=205), use_container_width=True)
                top_arpu = arpu_df.loc[arpu_df["ARPU"].idxmax()]
                render_ai_recommendation(
                    "ARPU by Segment",
                    f"{top_arpu['Segment']} has the highest ARPU at CLP {top_arpu['ARPU']:.0f}.",
                    f"Replicate {top_arpu['Segment']} offer architecture into upper SMB to lift blended ARPU.",
                    "Increase blended ARPU by ~CLP 1.2 within a quarter.",
                )
        with mix_col:
            st.markdown('<div class="eo-mini-title">Plan Mix by Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                plan_df = pd.DataFrame({
                    'Plan': ['WOM Hogar 300', 'WOM Hogar 600', 'WOM Gamer 1G', 'WOM Mesh Plus'],
                    'Share': [44, 29, 17, 10],
                })
                plan_bar = (
                    alt.Chart(plan_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22)
                    .encode(
                        x=alt.X('Share:Q', title='Share %', axis=alt.Axis(tickCount=6)),
                        y=alt.Y('Plan:N', sort='-x', title=None),
                        color=alt.Color(
                            'Plan:N',
                            scale=alt.Scale(
                                domain=['WOM Hogar 300', 'WOM Hogar 600', 'WOM Gamer 1G', 'WOM Mesh Plus'],
                                range=[EXEC_CHART_THEME["accent_indigo"], "#818CF8", "#A5B4FC", "#C7D2FE"],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Plan:N', title='Plan'),
                            alt.Tooltip('Share:Q', title='Share %', format='.0f'),
                        ],
                    )
                )
                st.altair_chart(style_exec_chart(plan_bar, height=205), use_container_width=True)
                top_plan = plan_df.loc[plan_df["Share"].idxmax()]
                render_ai_recommendation(
                    "Plan Mix",
                    f"{top_plan['Plan']} is the dominant mix component at {top_plan['Share']:.0f}%.",
                    "Introduce add-on bundles in the dominant plan to monetize without raising churn pressure.",
                    "Capture +CLP 0.2M monthly incremental revenue.",
                )

        # ── Mobile Network Insights ─────────────────────────────────────────
        st.markdown('<div class="eo-title">📱 Mobile Network Insights</div>', unsafe_allow_html=True)
        
        mobile_kpi_col1, mobile_kpi_col2, mobile_kpi_col3, mobile_kpi_col4 = st.columns(4)
        mobile_subscribers = 2_847_000
        mobile_data_gb = 18.7
        mobile_arpu = 12850
        mobile_5g_coverage = 68.4
        
        with mobile_kpi_col1:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #8B5CF615 0%, #8B5CF608 100%); border-left: 4px solid #8B5CF6; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Mobile Subscribers</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">{mobile_subscribers/1_000_000:.2f}M</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +6.8% YoY</div>
            </div>""", unsafe_allow_html=True)
        with mobile_kpi_col2:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #06B6D415 0%, #06B6D408 100%); border-left: 4px solid #06B6D4; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Avg Data Usage</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">{mobile_data_gb:.1f} GB</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +22% YoY</div>
            </div>""", unsafe_allow_html=True)
        with mobile_kpi_col3:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #10B98115 0%, #10B98108 100%); border-left: 4px solid #10B981; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Mobile ARPU</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">CLP {mobile_arpu:,}</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +3.2% QoQ</div>
            </div>""", unsafe_allow_html=True)
        with mobile_kpi_col4:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #F59E0B15 0%, #F59E0B08 100%); border-left: 4px solid #F59E0B; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">5G Coverage</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">{mobile_5g_coverage:.1f}%</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +12pp YoY</div>
            </div>""", unsafe_allow_html=True)

        mobile_col1, mobile_col2 = st.columns(2)
        
        with mobile_col1:
            st.markdown('<div class="eo-mini-title">Mobile Plan Distribution</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mobile_plan_df = pd.DataFrame({
                    'Plan': ['WOM Libre 30GB', 'WOM Libre 50GB', 'WOM Libre Ilimitado', 'WOM Prepago', 'WOM Empresas'],
                    'Subscribers': [680, 520, 890, 450, 307],
                    'ARPU': [9900, 12900, 18900, 5500, 24500],
                })
                mobile_plan_df['Subscribers_K'] = mobile_plan_df['Subscribers']
                mobile_plan_bar = (
                    alt.Chart(mobile_plan_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=20)
                    .encode(
                        x=alt.X('Subscribers_K:Q', title='Subscribers (K)', axis=alt.Axis(tickCount=5)),
                        y=alt.Y('Plan:N', sort='-x', title=None),
                        color=alt.Color(
                            'Plan:N',
                            scale=alt.Scale(
                                domain=['WOM Libre Ilimitado', 'WOM Libre 30GB', 'WOM Libre 50GB', 'WOM Prepago', 'WOM Empresas'],
                                range=['#8B5CF6', '#A78BFA', '#C4B5FD', '#DDD6FE', '#6D28D9'],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Plan:N', title='Plan'),
                            alt.Tooltip('Subscribers_K:Q', title='Subscribers (K)', format=','),
                            alt.Tooltip('ARPU:Q', title='ARPU (CLP)', format=','),
                        ],
                    )
                )
                st.altair_chart(style_exec_chart(mobile_plan_bar, height=200), use_container_width=True)
                top_mobile_plan = mobile_plan_df.loc[mobile_plan_df["Subscribers"].idxmax()]
                render_ai_recommendation(
                    "Mobile Plan Mix",
                    f"{top_mobile_plan['Plan']} leads with {top_mobile_plan['Subscribers']}K subscribers.",
                    "Promote unlimited plan upgrades with data add-on bundles for heavy users.",
                    "Increase mobile ARPU by CLP 800 in Q2.",
                )

        with mobile_col2:
            st.markdown('<div class="eo-mini-title">Mobile Data Consumption Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                data_trend_df = pd.DataFrame({
                    'Month': ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
                    'Data_GB': [15.2, 16.1, 16.8, 17.5, 18.1, 18.7],
                    '5G_Users_K': [420, 485, 550, 620, 695, 780],
                })
                data_line = alt.Chart(data_trend_df).mark_line(
                    point=alt.OverlayMarkDef(filled=True, size=60),
                    strokeWidth=3,
                    color='#8B5CF6',
                ).encode(
                    x=alt.X('Month:N', title=None, sort=['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']),
                    y=alt.Y('Data_GB:Q', title='Avg Data (GB)', scale=alt.Scale(domain=[14, 20])),
                    tooltip=[alt.Tooltip('Month:N'), alt.Tooltip('Data_GB:Q', title='Avg GB', format='.1f')],
                )
                users_bar = alt.Chart(data_trend_df).mark_bar(
                    opacity=0.3,
                    color='#06B6D4',
                    cornerRadiusTopLeft=4,
                    cornerRadiusTopRight=4,
                ).encode(
                    x=alt.X('Month:N', sort=['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']),
                    y=alt.Y('5G_Users_K:Q', title='5G Users (K)'),
                    tooltip=[alt.Tooltip('Month:N'), alt.Tooltip('5G_Users_K:Q', title='5G Users (K)')],
                )
                st.altair_chart(
                    style_exec_chart(
                        alt.layer(users_bar, data_line).resolve_scale(y='independent'),
                        height=200,
                    ),
                    use_container_width=True,
                )
                render_ai_recommendation(
                    "Data Growth",
                    f"Mobile data usage grew 23% in 6 months; 5G adoption driving consumption.",
                    "Accelerate 5G device financing programs to capture high-ARPU users.",
                    "Add 100K 5G subscribers by Q3 with +CLP 2.1M revenue uplift.",
                )

        mobile_col3, mobile_col4 = st.columns(2)
        
        with mobile_col3:
            st.markdown('<div class="eo-mini-title">Network Technology Mix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                tech_df = pd.DataFrame({
                    'Technology': ['5G', '4G LTE', '3G'],
                    'Users': [780, 1720, 347],
                    'Percentage': [27.4, 60.4, 12.2],
                })
                tech_donut = alt.Chart(tech_df).mark_arc(innerRadius=50, outerRadius=85, cornerRadius=4).encode(
                    theta=alt.Theta('Users:Q', stack=True),
                    color=alt.Color(
                        'Technology:N',
                        scale=alt.Scale(domain=['5G', '4G LTE', '3G'], range=['#8B5CF6', '#06B6D4', '#94A3B8']),
                        legend=alt.Legend(title=None, orient='right'),
                    ),
                    tooltip=[
                        alt.Tooltip('Technology:N'),
                        alt.Tooltip('Users:Q', title='Users (K)', format=','),
                        alt.Tooltip('Percentage:Q', title='Share %', format='.1f'),
                    ],
                )
                tech_center = alt.Chart(pd.DataFrame({'text': ['2.85M']})).mark_text(fontSize=18, fontWeight='bold', color='#1B2A4E').encode(text='text:N')
                st.altair_chart(style_exec_chart(tech_donut + tech_center, height=180), use_container_width=True)
                render_ai_recommendation(
                    "Technology Migration",
                    f"27% of users now on 5G; 3G still at 12% requiring migration.",
                    "Launch 3G sunset campaign with subsidized 4G/5G device trade-ins.",
                    "Reduce 3G users by 50% and improve network efficiency.",
                    level="warning",
                )

        with mobile_col4:
            st.markdown('<div class="eo-mini-title">Mobile Churn by Tenure</div>', unsafe_allow_html=True)
            with st.container(border=True):
                tenure_df = pd.DataFrame({
                    'Tenure': ['0-6 months', '6-12 months', '1-2 years', '2+ years'],
                    'Churn_Rate': [4.8, 2.9, 1.8, 0.9],
                    'Subscribers_K': [380, 520, 890, 1057],
                })
                tenure_bar = alt.Chart(tenure_df).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=18).encode(
                    x=alt.X('Churn_Rate:Q', title='Churn Rate %', scale=alt.Scale(domain=[0, 6])),
                    y=alt.Y('Tenure:N', sort=['0-6 months', '6-12 months', '1-2 years', '2+ years'], title=None),
                    color=alt.Color(
                        'Churn_Rate:Q',
                        scale=alt.Scale(scheme='orangered', domain=[0.5, 5]),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip('Tenure:N'),
                        alt.Tooltip('Churn_Rate:Q', title='Churn %', format='.1f'),
                        alt.Tooltip('Subscribers_K:Q', title='Subscribers (K)', format=','),
                    ],
                )
                st.altair_chart(style_exec_chart(tenure_bar, height=180), use_container_width=True)
                render_ai_recommendation(
                    "Tenure-Based Churn",
                    f"New subscribers (0-6mo) show 4.8% churn vs 0.9% for loyal users.",
                    "Implement 90-day onboarding program with usage milestones and rewards.",
                    "Reduce early churn by 1.5pp and improve LTV by CLP 45K.",
                    level="critical",
                )

        # ── Fibre/Hogar Insights ───────────────────────────────────────────
        st.markdown('<div class="eo-title">🏠 Fibre Hogar Insights</div>', unsafe_allow_html=True)
        
        fibre_kpi_col1, fibre_kpi_col2, fibre_kpi_col3, fibre_kpi_col4 = st.columns(4)
        fibre_subscribers = 485_000
        fibre_avg_speed = 412
        fibre_arpu = 24900
        fibre_ftth_coverage = 72.3
        
        with fibre_kpi_col1:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #3B82F615 0%, #3B82F608 100%); border-left: 4px solid #3B82F6; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Fibre Subscribers</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">{fibre_subscribers/1_000:.0f}K</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +12.4% YoY</div>
            </div>""", unsafe_allow_html=True)
        with fibre_kpi_col2:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #10B98115 0%, #10B98108 100%); border-left: 4px solid #10B981; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Avg Speed Delivered</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">{fibre_avg_speed} Mbps</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +18% YoY</div>
            </div>""", unsafe_allow_html=True)
        with fibre_kpi_col3:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #F59E0B15 0%, #F59E0B08 100%); border-left: 4px solid #F59E0B; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Fibre ARPU</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">CLP {fibre_arpu:,}</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +4.8% QoQ</div>
            </div>""", unsafe_allow_html=True)
        with fibre_kpi_col4:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #EC489915 0%, #EC489908 100%); border-left: 4px solid #EC4899; border-radius: 0 12px 12px 0; padding: 1rem;">
                <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">FTTH Coverage</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1B2A4E;">{fibre_ftth_coverage:.1f}%</div>
                <div style="font-size: 0.75rem; color: #10B981;">↑ +8pp YoY</div>
            </div>""", unsafe_allow_html=True)

        fibre_col1, fibre_col2 = st.columns(2)
        
        with fibre_col1:
            st.markdown('<div class="eo-mini-title">Fibre Plan Distribution</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fibre_plan_df = pd.DataFrame({
                    'Plan': ['WOM Hogar 300', 'WOM Hogar 600', 'WOM Gamer 1G', 'WOM Mesh Plus', 'WOM Empresas Fibra'],
                    'Subscribers': [195, 142, 78, 45, 25],
                    'ARPU': [18900, 24900, 32900, 38900, 54900],
                })
                fibre_plan_df['Subscribers_K'] = fibre_plan_df['Subscribers']
                fibre_plan_bar = (
                    alt.Chart(fibre_plan_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=20)
                    .encode(
                        x=alt.X('Subscribers_K:Q', title='Subscribers (K)', axis=alt.Axis(tickCount=5)),
                        y=alt.Y('Plan:N', sort='-x', title=None),
                        color=alt.Color(
                            'Plan:N',
                            scale=alt.Scale(
                                domain=['WOM Hogar 300', 'WOM Hogar 600', 'WOM Gamer 1G', 'WOM Mesh Plus', 'WOM Empresas Fibra'],
                                range=['#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#1D4ED8'],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Plan:N', title='Plan'),
                            alt.Tooltip('Subscribers_K:Q', title='Subscribers (K)', format=','),
                            alt.Tooltip('ARPU:Q', title='ARPU (CLP)', format=','),
                        ],
                    )
                )
                st.altair_chart(style_exec_chart(fibre_plan_bar, height=200), use_container_width=True)
                top_fibre_plan = fibre_plan_df.loc[fibre_plan_df["Subscribers"].idxmax()]
                render_ai_recommendation(
                    "Fibre Plan Mix",
                    f"{top_fibre_plan['Plan']} leads with {top_fibre_plan['Subscribers']}K subscribers.",
                    "Promote speed upgrades with gaming bundles and Mesh add-ons.",
                    "Increase fibre ARPU by CLP 1,200 in Q2.",
                )

        with fibre_col2:
            st.markdown('<div class="eo-mini-title">Speed Tier Adoption Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                speed_trend_df = pd.DataFrame({
                    'Month': ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
                    '300Mbps': [52, 50, 48, 45, 42, 40],
                    '600Mbps': [28, 29, 30, 31, 31, 32],
                    '1Gbps': [20, 21, 22, 24, 27, 28],
                })
                speed_melt = speed_trend_df.melt('Month', var_name='Tier', value_name='Share')
                speed_area = alt.Chart(speed_melt).mark_area(opacity=0.8).encode(
                    x=alt.X('Month:N', title=None, sort=['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']),
                    y=alt.Y('Share:Q', title='Share %', stack='normalize'),
                    color=alt.Color(
                        'Tier:N',
                        scale=alt.Scale(domain=['300Mbps', '600Mbps', '1Gbps'], range=['#93C5FD', '#3B82F6', '#1E40AF']),
                        legend=alt.Legend(title=None, orient='right'),
                    ),
                    tooltip=[alt.Tooltip('Month:N'), alt.Tooltip('Tier:N'), alt.Tooltip('Share:Q', format='.0f')],
                )
                st.altair_chart(style_exec_chart(speed_area, height=200), use_container_width=True)
                render_ai_recommendation(
                    "Speed Migration",
                    f"1Gbps tier grew from 20% to 28% in 6 months; 300Mbps declining.",
                    "Offer free speed trial upgrades to accelerate premium tier adoption.",
                    "Shift 15% more users to 600Mbps+ tiers by Q3.",
                )

        fibre_col3, fibre_col4 = st.columns(2)
        
        with fibre_col3:
            st.markdown('<div class="eo-mini-title">Installation & Service Quality</div>', unsafe_allow_html=True)
            with st.container(border=True):
                quality_df = pd.DataFrame({
                    'Metric': ['Install SLA Met', 'First-Call Resolution', 'Uptime SLA', 'Tech NPS'],
                    'Score': [94.2, 78.5, 99.4, 87.3],
                })
                quality_bar = alt.Chart(quality_df).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=18).encode(
                    x=alt.X('Score:Q', title='Score %', scale=alt.Scale(domain=[0, 100])),
                    y=alt.Y('Metric:N', sort='-x', title=None),
                    color=alt.Color(
                        'Score:Q',
                        scale=alt.Scale(domain=[70, 100], range=['#F59E0B', '#10B981']),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip('Metric:N'),
                        alt.Tooltip('Score:Q', title='Score %', format='.1f'),
                    ],
                )
                quality_text = alt.Chart(quality_df).mark_text(align='left', dx=4, fontSize=10, fontWeight='bold', color='#1B2A4E').encode(
                    x='Score:Q',
                    y=alt.Y('Metric:N', sort='-x'),
                    text=alt.Text('Score:Q', format='.1f'),
                )
                st.altair_chart(style_exec_chart(quality_bar + quality_text, height=180), use_container_width=True)
                render_ai_recommendation(
                    "Service Quality",
                    f"Install SLA at 94.2% vs 95% target; first-call resolution lagging.",
                    "Add field technician capacity in high-growth zones; improve diagnostic tools.",
                    "Hit 95% SLA and reduce repeat visits by 12%.",
                    level="warning",
                )

        with fibre_col4:
            st.markdown('<div class="eo-mini-title">Fibre Churn Drivers</div>', unsafe_allow_html=True)
            with st.container(border=True):
                churn_driver_df = pd.DataFrame({
                    'Reason': ['Price Sensitivity', 'Service Issues', 'Competitor Offer', 'Moving/Relocation', 'Speed Needs'],
                    'Percentage': [32, 28, 22, 12, 6],
                })
                churn_driver_bar = alt.Chart(churn_driver_df).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=18).encode(
                    x=alt.X('Percentage:Q', title='% of Churned Users'),
                    y=alt.Y('Reason:N', sort='-x', title=None),
                    color=alt.Color(
                        'Percentage:Q',
                        scale=alt.Scale(scheme='reds', domain=[5, 35]),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip('Reason:N'),
                        alt.Tooltip('Percentage:Q', title='Share %'),
                    ],
                )
                st.altair_chart(style_exec_chart(churn_driver_bar, height=180), use_container_width=True)
                render_ai_recommendation(
                    "Churn Root Causes",
                    f"Price sensitivity (32%) and service issues (28%) drive 60% of fibre churn.",
                    "Launch loyalty pricing for 12+ month customers; accelerate service quality fixes.",
                    "Reduce voluntary churn by 0.8pp and save CLP 0.5M ARR.",
                    level="critical",
                )

        # ── Revenue Mix by Customer Segment ────────────────────────────────
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown('<div class="eo-title">Revenue Mix by Customer Segment</div>', unsafe_allow_html=True)
            revenue_data = db_segment_perf[['Segment', 'Monthly Revenue M']].copy()
            revenue_data['Revenue'] = (revenue_data['Monthly Revenue M'] * 3).round(1)
            revenue_data['Percentage'] = (100 * revenue_data['Revenue'] / revenue_data['Revenue'].sum()).round(0)
            revenue_data = revenue_data[['Segment', 'Revenue', 'Percentage']]
            with st.container(border=True):
                donut = alt.Chart(revenue_data).mark_arc(innerRadius=74, outerRadius=118, cornerRadius=5, stroke="#FFFFFF", strokeWidth=2).encode(
                    theta=alt.Theta('Revenue:Q', stack=True),
                    color=alt.Color(
                        'Segment:N',
                        scale=alt.Scale(domain=['Consumer', 'SMB', 'Enterprise'], range=['#29B5E8', '#1B2A4E', '#10B981']),
                        legend=alt.Legend(title=None, orient='right'),
                    ),
                    tooltip=[
                        alt.Tooltip('Segment:N', title='Segment'),
                        alt.Tooltip('Revenue:Q', title='Revenue (CLP  M)', format='.1f'),
                        alt.Tooltip('Percentage:Q', title='Share %', format='.0f'),
                    ],
                    order=alt.Order('Revenue:Q', sort='descending'),
                )
                center_text = alt.Chart(pd.DataFrame({'text': [f'CLP {quarterly_revenue_m:.1f}M']})).mark_text(fontSize=24, fontWeight='bold', color='#1B2A4E').encode(text='text:N')
                center_sub = alt.Chart(pd.DataFrame({'text': ['Total Revenue']})).mark_text(fontSize=12, color='#6B7280', dy=20).encode(text='text:N')
                st.altair_chart(style_exec_chart(donut + center_text + center_sub, height=272), use_container_width=True)
                dominant_seg = revenue_data.loc[revenue_data["Revenue"].idxmax()]
                render_ai_recommendation(
                    "Customer Revenue Concentration",
                    f"{dominant_seg['Segment']} represents {dominant_seg['Percentage']:.0f}% of quarterly revenue.",
                    f"Run concentration-risk mitigation: upsell SMB and enterprise to reduce dependency on {dominant_seg['Segment']}.",
                    "Lower concentration risk while preserving growth resilience.",
                )

                seg_cols = st.columns(3)
                seg_info = []
                seg_colors = {"Consumer": "#29B5E8", "SMB": "#1B2A4E", "Enterprise": "#10B981"}
                seg_growth = {"Consumer": "+4.2%", "SMB": "+8.7%", "Enterprise": "+15.3%"}
                for _, row in db_segment_perf.iterrows():
                    seg = row["Segment"]
                    q_rev = row["Monthly Revenue M"] * 3
                    share = 100 * q_rev / quarterly_revenue_m
                    seg_arpu = row["Monthly Revenue M"] * 1_000_000 / row["Subscribers"]
                    seg_info.append((seg, seg_colors[seg], f"CLP {q_rev:.1f}M", f"{share:.0f}%", f"CLP {seg_arpu:.0f}", seg_growth[seg]))
                for i, (seg, color, rev, share, arpu, growth) in enumerate(seg_info):
                    with seg_cols[i]:
                        st.markdown(f"""<div style="background: linear-gradient(135deg, {color}15 0%, {color}08 100%); border-left: 4px solid {color}; border-radius: 0 8px 8px 0; padding: 0.75rem;"><div style="font-weight: 600; color: {color}; font-size: 0.9rem;">{seg}</div><div style="font-size: 1.2rem; font-weight: 700; color: #1B2A4E;">{rev}</div><div style="color: #6B7280; font-size: 0.75rem;">ARPU {arpu} · <span style="color: #10B981;">{growth}</span></div></div>""", unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="eo-title">At-Risk Customer Analysis</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_data = db_risk.rename(columns={"Revenue at Risk K": "Revenue at Risk"})
                lollipop_line = alt.Chart(risk_data).mark_rule(strokeWidth=3).encode(
                    x=alt.X('At Risk:Q', title='Customers at Risk', scale=alt.Scale(domain=[0, 350])),
                    x2=alt.value(0),
                    y=alt.Y('Segment:N', sort=['Budget', 'Standard', 'Premium', 'VIP'], title=None),
                    color=alt.Color('Avg Propensity:Q', scale=alt.Scale(scheme='orangered', domain=[0.4, 0.8]), legend=None),
                )
                lollipop_point = alt.Chart(risk_data).mark_circle(size=300).encode(
                    x='At Risk:Q',
                    y=alt.Y('Segment:N', sort=['Budget', 'Standard', 'Premium', 'VIP']),
                    color=alt.Color('Avg Propensity:Q', scale=alt.Scale(scheme='orangered', domain=[0.4, 0.8]), title='Churn Risk'),
                    tooltip=['Segment', alt.Tooltip('At Risk:Q', title='Customers'), alt.Tooltip('Revenue at Risk:Q', title='Revenue (CLP  K)', format=',.0f'), alt.Tooltip('Avg Propensity:Q', title='Risk Score', format='.0%')],
                )
                risk_labels = alt.Chart(risk_data).mark_text(align='left', dx=14, fontSize=10, fontWeight='bold', color="#7F1D1D").encode(
                    x='At Risk:Q',
                    y=alt.Y('Segment:N', sort=['Budget', 'Standard', 'Premium', 'VIP']),
                    text=alt.Text('Revenue at Risk:Q', format='CLP ,.0fK'),
                )
                st.altair_chart(style_exec_chart(lollipop_line + lollipop_point + risk_labels, height=190), use_container_width=True)
                highest_risk = risk_data.loc[risk_data["Avg Propensity"].idxmax()]
                render_ai_recommendation(
                    "At-Risk Cohorts",
                    f"{highest_risk['Segment']} has the highest churn propensity ({highest_risk['Avg Propensity']:.0%}) with material revenue exposure.",
                    f"Prioritize save-offers and proactive outreach for {highest_risk['Segment']} in the next 2 billing cycles.",
                    f"Protect up to CLP {(highest_risk['Revenue at Risk']/1000):.1f}M ARR from this cohort.",
                    level="critical",
                )

                st.markdown(f"""<div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 8px; padding: 0.75rem; margin-top: 0.5rem; border-left: 4px solid #F59E0B;"><div style="display: flex; align-items: center;"><span style="font-size: 1.5rem; margin-right: 0.5rem;">⚠️</span><div><strong style="color: #92400E;">Urgent: {at_risk_customers} customers at risk</strong><div style="color: #B45309; font-size: 0.85rem;">CLP {at_risk_revenue_m:.1f}M ARR exposed · Budget segment highest propensity</div></div></div></div>""", unsafe_allow_html=True)

    with ai_summary_tab:
        # ── C-Level AI Executive Cockpit ──────────────────────────────────
        st.markdown('<div class="eo-title">AI Strategy</div>', unsafe_allow_html=True)
        board_view_tab, deep_dive_tab = st.tabs(["🏛️ Board View", "🔍 Deep Dive"])
        st.caption("Board View: decision-ready summary. Deep Dive: diagnostics, scenarios, and risk analytics.")

        with board_view_tab:
            st.markdown(dedent(f"""
            <div class="cxo-snapshot">
                <div class="cxo-snapshot-title">CEO Snapshot · WOM Chile Next 90 Days</div>
                <div class="cxo-snapshot-text">Mobile growth strong with 5G adoption accelerating, but Fibre churn in Santiago metro and portability pressure from Entel/Movistar is putting <strong>CLP {at_risk_revenue_m:.1f}M ARR</strong> at risk. Fast approval of 5G migration incentives and Fibre bundle retention can protect ~<strong>CLP {protectable_arr_m:.1f}M</strong> this quarter.</div>
                <div class="cxo-snapshot-risk">⚠ Critical Watch: Mobile Portability + Fibre Competition in RM</div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">North Star, Guardrails, and Value</div>', unsafe_allow_html=True)
            st.markdown(dedent(f"""
            <div class="cxo-value-grid">
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #10B981, #34D399);">
                    <div class="cxo-value-label">North Star · Quarterly Revenue</div>
                    <div class="cxo-value-number">CLP {quarterly_revenue_m:.1f}M</div>
                    <div class="cxo-value-note">Run-rate aligned to growth target</div>
                </div>
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #3B82F6, #29B5E8);">
                    <div class="cxo-value-label">Value In Flight</div>
                    <div class="cxo-value-number">CLP {value_in_flight_m:.1f}M</div>
                    <div class="cxo-value-note">Initiatives in execution this quarter</div>
                </div>
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #F59E0B, #FBBF24);">
                    <div class="cxo-value-label">Guardrail · Churn</div>
                    <div class="cxo-value-number">{churn_rate:.1f}%</div>
                    <div class="cxo-value-note">Watchlist if above 2.3%</div>
                </div>
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #EF4444, #F87171);">
                    <div class="cxo-value-label">Value At Risk</div>
                    <div class="cxo-value-number">CLP {at_risk_revenue_m:.1f}M</div>
                    <div class="cxo-value-note urgent">Urgent containment required in 30 days</div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">Network Reliability & Customer Impact</div>', unsafe_allow_html=True)
            net_col1, net_col2 = st.columns(2)

            with net_col1:
                st.markdown('<div class="eo-mini-title">Major Incidents and MTTR Trend</div>', unsafe_allow_html=True)
                with st.container(border=True):
                    incidents_line = alt.Chart(db_incident_trend).mark_line(
                        point=True,
                        strokeWidth=3,
                        color="#EF4444",
                    ).encode(
                        x=alt.X("Week:N", title=None),
                        y=alt.Y("Major Incidents:Q", title="Major Incidents"),
                        tooltip=[alt.Tooltip("Week:N"), alt.Tooltip("Major Incidents:Q")],
                    )
                    mttr_line = alt.Chart(db_incident_trend).mark_line(
                        point=True,
                        strokeWidth=3,
                        color="#29B5E8",
                    ).encode(
                        x=alt.X("Week:N", title=None),
                        y=alt.Y("MTTR Minutes:Q", title="MTTR (min)"),
                        tooltip=[alt.Tooltip("Week:N"), alt.Tooltip("MTTR Minutes:Q")],
                    )
                    st.altair_chart(
                        style_exec_chart(
                            alt.layer(incidents_line, mttr_line).resolve_scale(y="independent"),
                            height=220,
                        ),
                        use_container_width=True,
                    )
                    incident_drop = db_incident_trend["Major Incidents"].iloc[0] - db_incident_trend["Major Incidents"].iloc[-1]
                    mttr_drop = db_incident_trend["MTTR Minutes"].iloc[0] - db_incident_trend["MTTR Minutes"].iloc[-1]
                    render_ai_recommendation(
                        "Network Operations",
                        f"Major incidents improved by {incident_drop} over 6 weeks; MTTR improved by {mttr_drop} minutes.",
                        "Scale proactive 5G/4G maintenance in Santiago metro and expand fiber NOC monitoring in Regiones.",
                        "Protect mobile NPS and reduce Fibre churn in affected comunas.",
                    )

            with net_col2:
                st.markdown('<div class="eo-mini-title">Region Network Score vs NPS</div>', unsafe_allow_html=True)
                with st.container(border=True):
                    net_scatter = alt.Chart(db_network_regions).mark_circle(
                        opacity=0.9,
                        stroke="#FFFFFF",
                        strokeWidth=1.4,
                    ).encode(
                        x=alt.X("Network Score:Q", title="Network Score", scale=alt.Scale(domain=[87, 96])),
                        y=alt.Y("NPS:Q", title="NPS", scale=alt.Scale(domain=[36, 56])),
                        size=alt.Size("Incidents:Q", scale=alt.Scale(range=[180, 900]), legend=None),
                        color=alt.Color("Incidents:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                        tooltip=[
                            alt.Tooltip("Region:N"),
                            alt.Tooltip("Network Score:Q", format=".1f"),
                            alt.Tooltip("NPS:Q"),
                            alt.Tooltip("Incidents:Q"),
                        ],
                    )
                    net_labels = alt.Chart(db_network_regions).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                        x="Network Score:Q",
                        y="NPS:Q",
                        text="Region:N",
                    )
                    st.altair_chart(style_exec_chart(net_scatter + net_labels, height=220), use_container_width=True)
                    weakest_region = db_network_regions.sort_values(["Network Score", "NPS"]).iloc[0]
                    render_ai_recommendation(
                        "Network Experience Link",
                        f"{weakest_region['Region']} is the weakest node with score {weakest_region['Network Score']:.1f} and NPS {int(weakest_region['NPS'])}.",
                        f"Prioritize 5G signal optimization and Fibre installation SLA in {weakest_region['Region']} this month.",
                        "Improve NPS by 2-3 points and reduce portability-out requests in the region.",
                        level="warning",
                    )

            st.markdown('<div class="eo-title">Plan vs Actual vs Forecast</div>', unsafe_allow_html=True)
            with st.container(border=True):
                paf_df = pd.DataFrame({
                    "Stage": ["Plan", "Actual to Date", "Forecast"],
                    "Revenue": [15.0, quarterly_revenue_m, 14.6],
                    "Type": ["Plan", "Actual", "Forecast"],
                })
                paf_bar = alt.Chart(paf_df).mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7, size=64).encode(
                    x=alt.X("Stage:N", title=None),
                    y=alt.Y("Revenue:Q", title="Revenue (CLP  M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Plan", "Actual", "Forecast"], range=["#94A3B8", "#29B5E8", "#10B981"]), legend=None),
                    tooltip=[alt.Tooltip("Stage:N"), alt.Tooltip("Revenue:Q", format=".1f")],
                )
                paf_text = alt.Chart(paf_df).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Stage:N",
                    y="Revenue:Q",
                    text=alt.Text("Revenue:Q", format=".1f"),
                )
                st.altair_chart(style_exec_chart(paf_bar + paf_text, height=220), use_container_width=True)
                variance = 15.0 - quarterly_revenue_m
                render_ai_recommendation(
                    "Plan Variance",
                    f"Current quarter is {variance:.1f}M below plan but forecast suggests partial recovery via 5G and Fibre growth.",
                    "Fast-track WOM Libre 5G migrations and Fibre+TV bundle campaigns to close remaining gap.",
                    "Recover up to CLP 0.6M against plan by quarter close.",
                    level="warning",
                )

            st.markdown('<div class="eo-title">Top Decisions for C-Level Approval</div>', unsafe_allow_html=True)
            st.markdown(dedent("""
            <div class="cxo-decision-grid">
                <div class="cxo-decision">
                    <span class="cxo-badge high">Immediate</span>
                    <div class="cxo-decision-title">Launch 5G migration campaign for WOM Libre users</div>
                    <div class="cxo-decision-meta"><strong>Impact:</strong> +CLP 0.9M ARR from ARPU uplift<br><strong>Confidence:</strong> 82%<br><strong>Owner:</strong> CMO · <strong>ETA:</strong> 30 days</div>
                </div>
                <div class="cxo-decision">
                    <span class="cxo-badge med">Priority</span>
                    <div class="cxo-decision-title">Approve Fibre + TV bundle discount for new FTTH zones</div>
                    <div class="cxo-decision-meta"><strong>Impact:</strong> +12K Fibre subs, CLP 0.7M ARR<br><strong>Confidence:</strong> 74%<br><strong>Owner:</strong> CRO · <strong>ETA:</strong> 45 days</div>
                </div>
                <div class="cxo-decision">
                    <span class="cxo-badge ok">Monitor</span>
                    <div class="cxo-decision-title">Prepago to Postpago conversion incentive program</div>
                    <div class="cxo-decision-meta"><strong>Impact:</strong> +8% conversion, +CLP 0.5M ARR<br><strong>Confidence:</strong> 68%<br><strong>Owner:</strong> CCO · <strong>ETA:</strong> 60 days</div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">Strategic Initiatives Tracker</div>', unsafe_allow_html=True)
            st.markdown(dedent("""
            <div class="cxo-initiatives">
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">5G Network Rollout (Santiago & Regiones)</div><span class="cxo-rag green">On Track</span></div>
                    <div class="cxo-init-meta">Owner: CTO · Budget used: 58% · Coverage: 68% → 85% target</div>
                    <div class="cxo-progress" style="--p: 72%;"><span style="--p: 72%;"></span></div>
                    <div class="cxo-init-foot">Progress: 72% · Next Milestone: Valparaíso & Concepción 5G activation</div>
                </div>
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">FTTH Fibre Expansion Program</div><span class="cxo-rag amber">At Risk</span></div>
                    <div class="cxo-init-meta">Owner: COO · Budget used: 67% · Homes passed: 1.2M → 1.8M target</div>
                    <div class="cxo-progress" style="--p: 54%;"><span style="--p: 54%;"></span></div>
                    <div class="cxo-init-foot">Progress: 54% · Next Milestone: Complete La Florida & Maipú deployment</div>
                </div>
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">Mobile Portability Retention</div><span class="cxo-rag red">Critical</span></div>
                    <div class="cxo-init-meta">Owner: CCO · Budget used: 44% · Save rate: 32% → 55% target</div>
                    <div class="cxo-progress" style="--p: 38%;"><span style="--p: 38%;"></span></div>
                    <div class="cxo-init-foot">Progress: 38% · Next Milestone: Launch proactive retention for high-value mobile</div>
                </div>
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">WOM TV + Triple Play Bundling</div><span class="cxo-rag green">On Track</span></div>
                    <div class="cxo-init-meta">Owner: CRO · Budget used: 51% · Bundle attach: 18% → 35% target</div>
                    <div class="cxo-progress" style="--p: 65%;"><span style="--p: 65%;"></span></div>
                    <div class="cxo-init-foot">Progress: 65% · Next Milestone: Launch Fibre + TV promo in 5 new comunas</div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">Board Narrative</div>', unsafe_allow_html=True)
            st.markdown(dedent(f"""
            <div class="cxo-board">
                <div class="cxo-board-grid">
                    <div class="cxo-board-cell">
                        <h5>What Changed</h5>
                        <p>Mobile ARPU grew 4.2% driven by 5G migrations, but Fibre churn spiked in competitive zones against VTR/Movistar.</p>
                    </div>
                    <div class="cxo-board-cell">
                        <h5>Why It Changed</h5>
                        <p>Entel's aggressive Prepago pricing and Movistar Fibre bundles are pressuring WOM in Santiago metro.</p>
                    </div>
                    <div class="cxo-board-cell">
                        <h5>Next 30 Days</h5>
                        <p>Accelerate 5G device subsidies, launch Fibre+TV retention offers, expand FTTH in high-demand comunas.</p>
                    </div>
                    <div class="cxo-board-cell">
                        <h5>Expected Impact</h5>
                        <p>Protect up to CLP {protectable_arr_m:.1f}M ARR, reduce mobile portability-out by 15%, grow Fibre base by 8K subs.</p>
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)

        with deep_dive_tab:
            st.markdown('<div class="eo-title">Scenario Outlook (Next 90 Days)</div>', unsafe_allow_html=True)
            sc_col1, sc_col2 = st.columns(2)

            with sc_col1:
                st.markdown('<div class="eo-mini-title">Revenue Scenarios</div>', unsafe_allow_html=True)
                scenario_df = pd.DataFrame({
                    "Scenario": ["Downside", "Base", "Upside"],
                    "Revenue": [13.9, 14.6, 15.4],
                    "Probability": ["25%", "50%", "25%"],
                })
                sc_bar = alt.Chart(scenario_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=52).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Revenue:Q", title="Projected Revenue (CLP  M)"),
                    color=alt.Color(
                        "Scenario:N",
                        scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip("Scenario:N"),
                        alt.Tooltip("Revenue:Q", format=".1f"),
                        alt.Tooltip("Probability:N"),
                    ],
                )
                sc_label = alt.Chart(scenario_df).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N",
                    y="Revenue:Q",
                    text=alt.Text("Revenue:Q", format=".1f"),
                )
                sc_prob = alt.Chart(scenario_df).mark_text(dy=16, fontSize=10, color="#475569").encode(
                    x="Scenario:N",
                    y=alt.value(0),
                    text="Probability:N",
                )
                st.altair_chart(style_exec_chart(sc_bar + sc_label + sc_prob, height=220), use_container_width=True)
                base_case = scenario_df.loc[scenario_df["Scenario"] == "Base"].iloc[0]
                render_ai_recommendation(
                    "Revenue Scenarios",
                    f"Base scenario projects CLP {base_case['Revenue']:.1f}M with highest probability ({base_case['Probability']}).",
                    "Commit budget to base-case plan while pre-authorizing contingency spend if downside signals trigger.",
                    "Improve forecast confidence and decision speed.",
                )

            with sc_col2:
                st.markdown('<div class="eo-mini-title">Churn Trend by Scenario</div>', unsafe_allow_html=True)
                churn_fcst = pd.DataFrame({
                    "Month": ["M+1", "M+2", "M+3", "M+1", "M+2", "M+3", "M+1", "M+2", "M+3"],
                    "Scenario": ["Downside", "Downside", "Downside", "Base", "Base", "Base", "Upside", "Upside", "Upside"],
                    "Churn": [2.4, 2.5, 2.6, 2.1, 2.0, 1.95, 1.9, 1.8, 1.7],
                })
                churn_line = alt.Chart(churn_fcst).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Churn:Q", title="Projected Churn %", scale=alt.Scale(domain=[1.6, 2.7])),
                    color=alt.Color(
                        "Scenario:N",
                        scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]),
                        legend=alt.Legend(title=None),
                    ),
                    tooltip=[
                        alt.Tooltip("Scenario:N"),
                        alt.Tooltip("Month:N"),
                        alt.Tooltip("Churn:Q", format=".2f"),
                    ],
                )
                st.altair_chart(style_exec_chart(churn_line, height=220), use_container_width=True)
                upside_m3 = churn_fcst[(churn_fcst["Scenario"] == "Upside") & (churn_fcst["Month"] == "M+3")]["Churn"].iloc[0]
                downside_m3 = churn_fcst[(churn_fcst["Scenario"] == "Downside") & (churn_fcst["Month"] == "M+3")]["Churn"].iloc[0]
                render_ai_recommendation(
                    "Churn Forecast",
                    f"M+3 churn ranges from {upside_m3:.2f}% (upside) to {downside_m3:.2f}% (downside).",
                    "Execute retention playbooks early to steer trajectory toward upside path.",
                    "Potentially avoid ~0.9pp churn deterioration in downside scenario.",
                    level="warning",
                )

            st.markdown('<div class="eo-title">Risk Radar and Leading Indicators</div>', unsafe_allow_html=True)
            rr_col1, rr_col2 = st.columns(2)

            with rr_col1:
                st.markdown('<div class="eo-mini-title">Risk Radar</div>', unsafe_allow_html=True)
                risk_radar_df = pd.DataFrame({
                    "Risk": ["Entel/Movistar price war", "Mobile portability loss", "5G spectrum costs", "FTTH competition (VTR)", "Subtel regulatory"],
                    "Likelihood": [4.4, 4.1, 3.5, 3.8, 2.9],
                    "Impact": [4.5, 4.3, 3.8, 4.0, 3.4],
                    "Exposure": [2.6, 2.1, 1.4, 1.8, 0.9],
                })
                risk_scatter = alt.Chart(risk_radar_df).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood (1-5)", scale=alt.Scale(domain=[2.2, 4.6])),
                    y=alt.Y("Impact:Q", title="Impact (1-5)", scale=alt.Scale(domain=[2.8, 4.9])),
                    size=alt.Size("Exposure:Q", title="Exposure (CLP  M)", scale=alt.Scale(range=[180, 1500])),
                    color=alt.Color("Exposure:Q", scale=alt.Scale(scheme="redpurple"), legend=None),
                    tooltip=[
                        alt.Tooltip("Risk:N"),
                        alt.Tooltip("Likelihood:Q", format=".1f"),
                        alt.Tooltip("Impact:Q", format=".1f"),
                        alt.Tooltip("Exposure:Q", title="Exposure (CLP  M)", format=".1f"),
                    ],
                )
                risk_labels = alt.Chart(risk_radar_df).mark_text(dy=-11, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q",
                    y="Impact:Q",
                    text="Risk:N",
                )
                st.altair_chart(style_exec_chart(risk_scatter + risk_labels, height=235), use_container_width=True)
                top_exposure = risk_radar_df.loc[risk_radar_df["Exposure"].idxmax()]
                render_ai_recommendation(
                    "Risk Radar",
                    f"Highest financial exposure is {top_exposure['Risk']} (CLP {top_exposure['Exposure']:.1f}M) with high impact/likelihood.",
                    f"Create executive mitigation track for {top_exposure['Risk']} with weekly progress checkpoints.",
                    "Reduce downside exposure and strengthen board-level risk posture.",
                    level="critical",
                )

            with rr_col2:
                st.markdown('<div class="eo-mini-title">Leading Indicators</div>', unsafe_allow_html=True)
                lead_df = pd.DataFrame({
                    "Indicator": ["Portability-out requests", "5G device activations", "Fibre install backlog", "WOM App engagement", "Prepago recharge drop"],
                    "Delta": [22, -15, 18, -12, 16],
                    "Status": ["Critical", "Watch", "Watch", "Watch", "Watch"],
                })
                lead_bar = alt.Chart(lead_df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=18).encode(
                    x=alt.X("Delta:Q", title="Change vs baseline (%)", scale=alt.Scale(domain=[0, 24])),
                    y=alt.Y("Indicator:N", sort="-x", title=None),
                    color=alt.Color(
                        "Status:N",
                        scale=alt.Scale(domain=["Stable", "Watch", "Critical"], range=["#10B981", "#F59E0B", "#EF4444"]),
                        legend=alt.Legend(title=None),
                    ),
                    tooltip=[
                        alt.Tooltip("Indicator:N"),
                        alt.Tooltip("Delta:Q", title="Change %"),
                        alt.Tooltip("Status:N"),
                    ],
                )
                lead_text = alt.Chart(lead_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Delta:Q",
                    y=alt.Y("Indicator:N", sort="-x"),
                    text=alt.Text("Delta:Q", format=".0f"),
                )
                st.altair_chart(style_exec_chart(lead_bar + lead_text, height=235), use_container_width=True)
                top_lead = lead_df.loc[lead_df["Delta"].idxmax()]
                render_ai_recommendation(
                    "Leading Indicators",
                    f"The fastest-deteriorating signal is {top_lead['Indicator']} (+{top_lead['Delta']:.0f}%).",
                    "Set an automated early-warning threshold and route alert to owner squad immediately.",
                    "Cut reaction time and prevent escalation into churn/revenue loss.",
                    level="warning" if top_lead["Status"] != "Critical" else "critical",
                )

# ---------------------------------------------------------------------------
# Page: Subscribers
# ---------------------------------------------------------------------------
elif selected_menu == "Subscribers":
    import pandas as pd
    import altair as alt

    SUB_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "title_color": "#0F172A",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
        "accent_blue": "#29B5E8",
        "accent_green": "#10B981",
        "accent_indigo": "#6366F1",
        "accent_amber": "#F59E0B",
        "accent_red": "#EF4444",
        "accent_purple": "#8B5CF6",
    }

    def style_sub_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(
                labelFont=SUB_CHART_THEME["font"],
                titleFont=SUB_CHART_THEME["font"],
                labelColor=SUB_CHART_THEME["label_color"],
                titleColor=SUB_CHART_THEME["label_color"],
                labelFontSize=11,
                titleFontSize=12,
                domain=False,
                gridColor=SUB_CHART_THEME["grid_color"],
                gridOpacity=0.75,
            )
            .configure_legend(
                labelFont=SUB_CHART_THEME["font"],
                titleFont=SUB_CHART_THEME["font"],
                labelColor=SUB_CHART_THEME["label_color"],
                titleColor=SUB_CHART_THEME["label_color"],
                orient="top",
                direction="horizontal",
                symbolType="circle",
                symbolSize=100,
            )
        )

    def render_sub_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        st.markdown(
            f"""<div class="sub-ai-card {level}"><div class="sub-ai-head">🤖 AI Recommendation · {headline}</div><div class="sub-ai-line"><strong>Insight:</strong> {insight}</div><div class="sub-ai-line"><strong>Action:</strong> {action}</div><div class="sub-ai-line"><strong>Expected Impact:</strong> {impact}</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("""<style>
@keyframes sub-fade-up { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes sub-shimmer { 0% { left: -40%; } 100% { left: 120%; } }
@keyframes sub-pulse-dot { 0%,100% { transform: scale(1); opacity: 0.7; } 50% { transform: scale(1.25); opacity: 1; } }
.sub-title { position: relative; overflow: hidden; display: flex; align-items: center; gap: 0.55rem; margin: 1.2rem 0 0.8rem; padding: 0.6rem 0.85rem; border-radius: 12px; border: 1px solid #DBEAFE; background: linear-gradient(135deg, #F0F8FF 0%, #EEF2FF 100%); color: #1B2A4E; font-size: 1rem; font-weight: 700; animation: sub-fade-up 0.4s ease-out both; }
.sub-title::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: linear-gradient(135deg, #29B5E8, #6366F1); animation: sub-pulse-dot 1.8s ease-in-out infinite; }
.sub-title::after { content: ""; position: absolute; top: 0; left: -40%; width: 34%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent); animation: sub-shimmer 3.2s ease-in-out infinite; }
.sub-mini-title { display: inline-flex; align-items: center; gap: 0.4rem; margin: 0.15rem 0 0.55rem; font-size: 0.9rem; font-weight: 700; color: #1E3A8A; }
.sub-mini-title::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: linear-gradient(135deg, #22C1EE, #8B5CF6); }
.sub-pulse { position: relative; overflow: hidden; border-radius: 14px; border: 1px solid #BFDBFE; background: linear-gradient(135deg, #EFF6FF 0%, #ECFEFF 100%); padding: 1rem 1.1rem; margin-bottom: 1rem; }
.sub-pulse::before { content: ""; position: absolute; top: 0; left: -50%; width: 40%; height: 100%; background: linear-gradient(90deg, transparent, rgba(41,181,232,0.2), transparent); animation: sub-shimmer 3s ease-in-out infinite; }
.sub-pulse-head { position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.sub-pulse-title { color: #1E3A8A; font-weight: 700; font-size: 0.92rem; }
.sub-pulse-live { color: #10B981; font-size: 0.74rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.35rem; }
.sub-pulse-live::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: #10B981; animation: sub-pulse-dot 1.2s ease-in-out infinite; }
.sub-pulse-grid { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.65rem; }
.sub-pulse-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.65rem 0.72rem; animation: sub-fade-up 0.4s ease-out both; }
.sub-pulse-card:nth-child(1) { animation-delay: 0.05s; } .sub-pulse-card:nth-child(2) { animation-delay: 0.12s; } .sub-pulse-card:nth-child(3) { animation-delay: 0.2s; } .sub-pulse-card:nth-child(4) { animation-delay: 0.28s; } .sub-pulse-card:nth-child(5) { animation-delay: 0.36s; }
.sub-pulse-label { color: #64748B; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.2rem; }
.sub-pulse-value { color: #0F172A; font-size: 1.28rem; font-weight: 800; line-height: 1.15; }
.sub-pulse-delta { margin-top: 0.2rem; color: #059669; font-size: 0.74rem; font-weight: 700; }
.sub-ai-card { margin-top: 0.6rem; border-radius: 10px; border: 1px solid #D1E9FF; background: linear-gradient(135deg, #F8FBFF 0%, #EEF6FF 100%); padding: 0.62rem 0.78rem; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05); animation: sub-fade-up 0.35s ease-out both; }
.sub-ai-card.warning { border-color: #FCD34D; background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); }
.sub-ai-card.critical { border-color: #FCA5A5; background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); }
.sub-ai-head { color: #1E3A8A; font-size: 0.78rem; font-weight: 700; margin-bottom: 0.28rem; }
.sub-ai-card.warning .sub-ai-head { color: #92400E; }
.sub-ai-card.critical .sub-ai-head { color: #991B1B; }
.sub-ai-line { color: #334155; font-size: 0.77rem; line-height: 1.34; margin: 0.12rem 0; }
.sub-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-bottom: 0.75rem; }
.sub-kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.55rem 0.62rem;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    animation: sub-fade-up 0.35s ease-out both;
}
.sub-kpi-card .k {
    color: #64748B;
    font-size: 0.64rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.sub-kpi-card .v {
    color: #0F172A;
    font-size: 1.02rem;
    font-weight: 800;
    margin-top: 0.12rem;
    line-height: 1.15;
}
.sub-kpi-card .d {
    color: #059669;
    font-size: 0.68rem;
    font-weight: 700;
    margin-top: 0.14rem;
}
.sub-kpi-card.warn .d { color: #B45309; }
.sub-kpi-card.crit .d { color: #B91C1C; }
@media (max-width: 980px) { .sub-pulse-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 980px) { .sub-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .sub-pulse-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .sub-kpi-grid { grid-template-columns: 1fr; } }
</style>""", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # WOM MÓVIL Data
    # -------------------------------------------------------------------
    movil_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Adds": [48500, 52100, 55800, 51200, 54600, 58200],
        "Churned": [32100, 33400, 34200, 35800, 34100, 33800],
        "Portability In": [18200, 19800, 21400, 19100, 20800, 22100],
        "Portability Out": [14600, 15200, 15800, 16400, 15100, 14800],
    })
    movil_monthly["Net Adds"] = movil_monthly["Adds"] - movil_monthly["Churned"]
    movil_monthly["Net Portability"] = movil_monthly["Portability In"] - movil_monthly["Portability Out"]
    movil_starting_base = 2680000
    movil_monthly["Base"] = movil_starting_base + movil_monthly["Net Adds"].cumsum()
    movil_monthly["Churn %"] = (movil_monthly["Churned"] / (movil_monthly["Base"] - movil_monthly["Net Adds"]) * 100).round(2)

    movil_plans = pd.DataFrame({
        "Plan": ["WOM Libre 30GB", "WOM Libre 50GB", "WOM Libre Ilimitado", "WOM Prepago", "WOM Empresas Móvil"],
        "Subscribers K": [680, 920, 540, 480, 232],
        "ARPU CLP": [9900, 12900, 18900, 5200, 24500],
        "5G Enabled %": [42, 68, 85, 12, 78],
    })
    movil_plans["Revenue M CLP"] = (movil_plans["Subscribers K"] * movil_plans["ARPU CLP"] / 1000).round(1)

    movil_network = pd.DataFrame({
        "Technology": ["5G", "4G LTE", "3G"],
        "Users K": [1945, 780, 127],
        "Avg Data GB": [24.8, 14.2, 6.1],
    })

    movil_churn_reasons = pd.DataFrame({
        "Reason": ["Portabilidad a Entel", "Portabilidad a Movistar", "Portabilidad a Claro", "No pago / Involuntario", "Otros"],
        "Volume": [5200, 4100, 2800, 8400, 3300],
    })

    movil_tenure = pd.DataFrame({
        "Tenure": ["0-3m", "4-6m", "7-12m", "13-24m", "25m+"],
        "Subscribers K": [420, 380, 620, 780, 652],
        "Churn %": [5.2, 3.8, 2.4, 1.6, 1.1],
    })

    movil_regions = pd.DataFrame({
        "Region": ["Metropolitana", "Valparaíso", "Biobío", "Maule", "Araucanía", "Otros"],
        "Subscribers K": [1480, 320, 280, 180, 140, 452],
        "5G Coverage %": [82, 68, 62, 45, 38, 42],
        "NPS": [48, 44, 42, 40, 38, 41],
    })

    movil_device_mix = pd.DataFrame({
        "Device Type": ["5G Smartphone", "4G Smartphone", "Feature Phone", "Mobile Router"],
        "Count K": [1420, 1180, 198, 54],
    })

    movil_data_trend = pd.DataFrame({
        "Month": movil_monthly["Month"],
        "Avg Data GB": [16.2, 16.8, 17.4, 17.9, 18.3, 18.7],
        "5G Users K": [1680, 1740, 1800, 1860, 1905, 1945],
    })

    movil_retention = pd.DataFrame({
        "Campaign": ["5G Upgrade Offer", "Loyalty Data Bonus", "Prepago→Postpago", "Win-back 30 días"],
        "Contacted": [12400, 8600, 6200, 4800],
        "Saved": [5580, 3440, 2480, 1440],
    })
    movil_retention["Save Rate %"] = (movil_retention["Saved"] / movil_retention["Contacted"] * 100).round(1)

    # -------------------------------------------------------------------
    # WOM FIBRA/HOGAR Data
    # -------------------------------------------------------------------
    fibra_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Adds": [8200, 8800, 9400, 8600, 9200, 9800],
        "Churned": [4100, 4300, 4500, 4800, 4400, 4200],
    })
    fibra_monthly["Net Adds"] = fibra_monthly["Adds"] - fibra_monthly["Churned"]
    fibra_starting_base = 432000
    fibra_monthly["Base"] = fibra_starting_base + fibra_monthly["Net Adds"].cumsum()
    fibra_monthly["Churn %"] = (fibra_monthly["Churned"] / (fibra_monthly["Base"] - fibra_monthly["Net Adds"]) * 100).round(2)

    fibra_plans = pd.DataFrame({
        "Plan": ["WOM Hogar 300 Mbps", "WOM Hogar 600 Mbps", "WOM Gamer 1 Gbps", "WOM Empresas Fibra"],
        "Subscribers K": [185, 168, 82, 50],
        "ARPU CLP": [18900, 24900, 34900, 48500],
        "Avg Speed Mbps": [298, 592, 945, 920],
    })
    fibra_plans["Revenue M CLP"] = (fibra_plans["Subscribers K"] * fibra_plans["ARPU CLP"] / 1000).round(1)

    fibra_speed_tiers = pd.DataFrame({
        "Speed Tier": ["300 Mbps", "600 Mbps", "1 Gbps"],
        "Subscribers K": [185, 168, 132],
        "Avg Actual Mbps": [298, 592, 945],
        "Speed Delivery %": [99.3, 98.7, 94.5],
    })

    fibra_churn_reasons = pd.DataFrame({
        "Reason": ["Competencia VTR/Movistar", "Precio", "Mudanza", "Calidad servicio", "Otros"],
        "Volume": [1420, 980, 720, 640, 440],
    })

    fibra_tenure = pd.DataFrame({
        "Tenure": ["0-3m", "4-6m", "7-12m", "13-24m", "25m+"],
        "Subscribers K": [68, 72, 118, 142, 85],
        "Churn %": [4.2, 2.8, 1.8, 1.2, 0.9],
    })

    fibra_regions = pd.DataFrame({
        "Region": ["Metropolitana", "Valparaíso", "Biobío", "O'Higgins", "Maule", "Otros"],
        "Subscribers K": [268, 62, 54, 38, 32, 31],
        "FTTH Coverage %": [78, 65, 58, 48, 42, 38],
        "NPS": [52, 48, 46, 44, 42, 40],
    })

    fibra_install_metrics = pd.DataFrame({
        "Metric": ["Install SLA Met", "First-Call Resolution", "Uptime SLA", "Tech NPS"],
        "Score": [94.2, 78.5, 99.4, 87.3],
    })

    fibra_tv_bundle = pd.DataFrame({
        "Bundle": ["Fibra Only", "Fibra + TV", "Fibra + TV + Móvil"],
        "Subscribers K": [312, 128, 45],
        "ARPU CLP": [22400, 32800, 48600],
        "Churn %": [1.8, 1.2, 0.8],
    })

    fibra_retention = pd.DataFrame({
        "Campaign": ["TV Bundle Upsell", "Speed Upgrade Offer", "Loyalty Discount", "Win-back"],
        "Contacted": [4200, 3800, 2600, 1800],
        "Saved": [1890, 1520, 1040, 540],
    })
    fibra_retention["Save Rate %"] = (fibra_retention["Saved"] / fibra_retention["Contacted"] * 100).round(1)

    fibra_complaint_df = pd.DataFrame({
        "Reason": ["Velocidad lenta", "Cortes de servicio", "WiFi inestable", "Instalación demorada", "Facturación"],
        "Volume": [380, 290, 260, 180, 150],
    })

    # Computed metrics - Móvil
    movil_total_subs = int(movil_plans["Subscribers K"].sum() * 1000)
    movil_latest = movil_monthly.iloc[-1]
    movil_prev = movil_monthly.iloc[-2]
    movil_net_adds = int(movil_latest["Net Adds"])
    movil_churn_rate = float(movil_latest["Churn %"])
    movil_5g_pct = round(movil_network.loc[movil_network["Technology"] == "5G", "Users K"].iloc[0] / (movil_network["Users K"].sum()) * 100, 1)
    movil_avg_data = round(movil_data_trend.iloc[-1]["Avg Data GB"], 1)
    movil_arpu = round((movil_plans["Subscribers K"] * movil_plans["ARPU CLP"]).sum() / movil_plans["Subscribers K"].sum(), 0)
    movil_portability_net = int(movil_latest["Net Portability"])

    # Computed metrics - Fibra
    fibra_total_subs = int(fibra_plans["Subscribers K"].sum() * 1000)
    fibra_latest = fibra_monthly.iloc[-1]
    fibra_prev = fibra_monthly.iloc[-2]
    fibra_net_adds = int(fibra_latest["Net Adds"])
    fibra_churn_rate = float(fibra_latest["Churn %"])
    fibra_avg_speed = round((fibra_plans["Subscribers K"] * fibra_plans["Avg Speed Mbps"]).sum() / fibra_plans["Subscribers K"].sum(), 0)
    fibra_arpu = round((fibra_plans["Subscribers K"] * fibra_plans["ARPU CLP"]).sum() / fibra_plans["Subscribers K"].sum(), 0)
    fibra_bundle_rate = round((fibra_tv_bundle.loc[fibra_tv_bundle["Bundle"] != "Fibra Only", "Subscribers K"].sum() / fibra_tv_bundle["Subscribers K"].sum()) * 100, 1)

    st.markdown(dedent(f"""
    <div class="sub-pulse">
        <div class="sub-pulse-head">
            <span class="sub-pulse-title">📱🏠 WOM Subscribers · Móvil + Fibra/Hogar</span>
            <span class="sub-pulse-live">Live</span>
        </div>
        <div class="sub-pulse-grid">
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">Total Móvil</div>
                <div class="sub-pulse-value">{movil_total_subs/1000000:.2f}M</div>
                <div class="sub-pulse-delta">↑ +{movil_net_adds:,} net adds</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">Total Fibra</div>
                <div class="sub-pulse-value">{fibra_total_subs/1000:.0f}K</div>
                <div class="sub-pulse-delta">↑ +{fibra_net_adds:,} net adds</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">Móvil Churn</div>
                <div class="sub-pulse-value">{movil_churn_rate:.2f}%</div>
                <div class="sub-pulse-delta">5G adoption helping</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">Fibra Churn</div>
                <div class="sub-pulse-value">{fibra_churn_rate:.2f}%</div>
                <div class="sub-pulse-delta">Bundles reduce churn</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">5G Adoption</div>
                <div class="sub-pulse-value">{movil_5g_pct:.1f}%</div>
                <div class="sub-pulse-delta">Growing fast</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    sub_tab_movil, sub_tab_fibra = st.tabs(
        ["📱 WOM Móvil", "🏠 WOM Fibra/Hogar"]
    )

    with sub_tab_movil:
        st.markdown('<div class="sub-title">WOM Móvil · Subscriber Analytics</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="sub-kpi-grid">
                <div class="sub-kpi-card"><div class="k">Total Suscriptores</div><div class="v">{movil_total_subs/1000000:.2f}M</div><div class="d">Base activa</div></div>
                <div class="sub-kpi-card"><div class="k">Net Adds (Mes)</div><div class="v">+{movil_net_adds:,}</div><div class="d">Crecimiento neto</div></div>
                <div class="sub-kpi-card"><div class="k">ARPU Móvil</div><div class="v">CLP {movil_arpu:,.0f}</div><div class="d">Promedio ponderado</div></div>
                <div class="sub-kpi-card"><div class="k">Churn Rate</div><div class="v">{movil_churn_rate:.2f}%</div><div class="d">Mensual</div></div>
                <div class="sub-kpi-card"><div class="k">5G Users</div><div class="v">{movil_5g_pct:.1f}%</div><div class="d">De la base total</div></div>
                <div class="sub-kpi-card"><div class="k">Avg Data Usage</div><div class="v">{movil_avg_data:.1f} GB</div><div class="d">Por usuario/mes</div></div>
                <div class="sub-kpi-card"><div class="k">Portabilidad Neta</div><div class="v">+{movil_portability_net:,}</div><div class="d">Ganancia vs competencia</div></div>
                <div class="sub-kpi-card warn"><div class="k">Portabilidad Out</div><div class="v">{int(movil_latest['Portability Out']):,}</div><div class="d">A Entel/Movistar/Claro</div></div>
            </div>
        """), unsafe_allow_html=True)

        mv_col1, mv_col2 = st.columns(2)
        with mv_col1:
            st.markdown('<div class="sub-mini-title">Altas vs Bajas y Base Móvil</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mv_bars = alt.Chart(movil_monthly).transform_fold(
                    ["Adds", "Churned"], as_=["Metric", "Count"]
                ).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Count:Q", title="Altas / Bajas"),
                    color=alt.Color("Metric:N", scale=alt.Scale(domain=["Adds", "Churned"], range=["#10B981", "#EF4444"]), legend=alt.Legend(title=None)),
                    xOffset="Metric:N",
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Metric:N"), alt.Tooltip("Count:Q", format=",")],
                )
                mv_base_line = alt.Chart(movil_monthly).mark_line(point=True, color="#29B5E8", strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Base:Q", title="Base Total"),
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Base:Q", format=",")],
                )
                st.altair_chart(style_sub_chart(alt.layer(mv_bars, mv_base_line).resolve_scale(y="independent"), height=230), use_container_width=True)
                mv_net_total = int(movil_monthly["Net Adds"].sum())
                render_sub_ai_reco(
                    "Crecimiento Móvil",
                    f"Base móvil creció +{mv_net_total:,} en los últimos 6 meses. Portabilidad neta positiva.",
                    "Acelerar campañas 5G para retener usuarios de alto valor y reducir portabilidad a Entel.",
                    "Mantener crecimiento neto y mejorar mix de usuarios 5G.",
                )

        with mv_col2:
            st.markdown('<div class="sub-mini-title">Distribución por Plan WOM</div>', unsafe_allow_html=True)
            with st.container(border=True):
                plan_bar = alt.Chart(movil_plans).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22).encode(
                    x=alt.X("Subscribers K:Q", title="Suscriptores (Miles)"),
                    y=alt.Y("Plan:N", sort="-x", title=None),
                    color=alt.Color("5G Enabled %:Q", scale=alt.Scale(domain=[10, 90], range=["#94A3B8", "#10B981"]), legend=alt.Legend(title="5G %")),
                    tooltip=["Plan:N", alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("ARPU CLP:Q", format=","), alt.Tooltip("5G Enabled %:Q", format=".0f")],
                )
                st.altair_chart(style_sub_chart(plan_bar, height=230), use_container_width=True)
                top_plan = movil_plans.loc[movil_plans["Subscribers K"].idxmax()]
                render_sub_ai_reco(
                    "Mix de Planes",
                    f"WOM Libre 50GB lidera con {top_plan['Subscribers K']:.0f}K suscriptores y {top_plan['5G Enabled %']:.0f}% en 5G.",
                    "Promover migración de Prepago a WOM Libre con ofertas de equipo 5G subsidiado.",
                    "Incrementar ARPU promedio +8% y adopción 5G +12%.",
                )

        st.markdown('<div class="sub-mini-title">Portabilidad: Origen de Bajas</div>', unsafe_allow_html=True)
        mv_col3, mv_col4 = st.columns(2)
        with mv_col3:
            with st.container(border=True):
                churn_bar = alt.Chart(movil_churn_reasons).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=18, color="#EF4444").encode(
                    x=alt.X("Volume:Q", title="Clientes Perdidos"),
                    y=alt.Y("Reason:N", sort="-x", title=None),
                    tooltip=["Reason:N", alt.Tooltip("Volume:Q", format=",")],
                )
                st.altair_chart(style_sub_chart(churn_bar, height=200), use_container_width=True)
                top_reason = movil_churn_reasons.sort_values("Volume", ascending=False).iloc[0]
                render_sub_ai_reco(
                    "Fuga Competitiva",
                    f"Principal destino de portabilidad: {top_reason['Reason']} ({top_reason['Volume']:,} clientes).",
                    "Lanzar campaña de retención proactiva para usuarios con señales de riesgo hacia Entel.",
                    "Reducir portabilidad-out 15% y proteger base de alto valor.",
                    level="critical",
                )

        with mv_col4:
            with st.container(border=True):
                tech_donut = alt.Chart(movil_network).mark_arc(innerRadius=55, outerRadius=95, cornerRadius=4, stroke="#FFFFFF", strokeWidth=2).encode(
                    theta=alt.Theta("Users K:Q", stack=True),
                    color=alt.Color("Technology:N", scale=alt.Scale(domain=["5G", "4G LTE", "3G"], range=["#10B981", "#29B5E8", "#94A3B8"]), legend=alt.Legend(title=None)),
                    tooltip=["Technology:N", alt.Tooltip("Users K:Q", format=","), alt.Tooltip("Avg Data GB:Q", format=".1f")],
                )
                st.altair_chart(style_sub_chart(tech_donut, height=200), use_container_width=True)
                render_sub_ai_reco(
                    "Mix Tecnológico",
                    f"5G representa {movil_5g_pct:.1f}% de usuarios con consumo promedio de {movil_network.loc[movil_network['Technology']=='5G', 'Avg Data GB'].iloc[0]:.1f} GB.",
                    "Incentivar upgrade de dispositivos 4G→5G con planes de financiamiento atractivos.",
                    "Aumentar adopción 5G y reducir churn en segmento premium.",
                )

        st.markdown('<div class="sub-mini-title">Tendencia de Consumo de Datos y Usuarios 5G</div>', unsafe_allow_html=True)
        with st.container(border=True):
            data_line = alt.Chart(movil_data_trend).mark_line(point=True, strokeWidth=3, color="#29B5E8").encode(
                x=alt.X("Month:N", title=None),
                y=alt.Y("Avg Data GB:Q", title="Consumo Promedio (GB)"),
                tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Avg Data GB:Q", format=".1f")],
            )
            users_5g = alt.Chart(movil_data_trend).mark_bar(opacity=0.6, color="#10B981").encode(
                x=alt.X("Month:N", title=None),
                y=alt.Y("5G Users K:Q", title="Usuarios 5G (K)"),
                tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("5G Users K:Q", format=",")],
            )
            st.altair_chart(style_sub_chart(alt.layer(users_5g, data_line).resolve_scale(y="independent"), height=220), use_container_width=True)

        st.markdown('<div class="sub-mini-title">Retención Móvil: Campañas Activas</div>', unsafe_allow_html=True)
        with st.container(border=True):
            ret_bars = alt.Chart(movil_retention).transform_fold(
                ["Contacted", "Saved"], as_=["Metric", "Value"]
            ).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x=alt.X("Campaign:N", title=None),
                y=alt.Y("Value:Q", title="Clientes"),
                color=alt.Color("Metric:N", scale=alt.Scale(domain=["Contacted", "Saved"], range=["#94A3B8", "#10B981"]), legend=alt.Legend(title=None)),
                xOffset="Metric:N",
                tooltip=["Campaign:N", "Metric:N", alt.Tooltip("Value:Q", format=",")],
            )
            st.altair_chart(style_sub_chart(ret_bars, height=220), use_container_width=True)
            best_camp = movil_retention.loc[movil_retention["Save Rate %"].idxmax()]
            render_sub_ai_reco(
                "Efectividad Retención",
                f"Mejor campaña: {best_camp['Campaign']} con {best_camp['Save Rate %']:.1f}% tasa de salvación.",
                "Escalar targeting de {best_camp['Campaign']} a usuarios de alto ARPU con señales de riesgo.",
                "Incrementar saves mensuales +25% y reducir churn 0.3pp.",
            )

        st.markdown('<div class="sub-mini-title">Cobertura Regional y NPS</div>', unsafe_allow_html=True)
        with st.container(border=True):
            region_scatter = alt.Chart(movil_regions).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                x=alt.X("5G Coverage %:Q", title="Cobertura 5G (%)", scale=alt.Scale(domain=[35, 90])),
                y=alt.Y("NPS:Q", title="NPS", scale=alt.Scale(domain=[35, 52])),
                size=alt.Size("Subscribers K:Q", scale=alt.Scale(range=[200, 1800]), legend=None),
                color=alt.Color("Region:N", legend=alt.Legend(title=None)),
                tooltip=["Region:N", alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("5G Coverage %:Q", format=".0f"), "NPS:Q"],
            )
            region_labels = alt.Chart(movil_regions).mark_text(dy=-14, fontSize=9, color="#1E293B").encode(
                x="5G Coverage %:Q", y="NPS:Q", text="Region:N"
            )
            st.altair_chart(style_sub_chart(region_scatter + region_labels, height=240), use_container_width=True)
            weakest = movil_regions.sort_values("NPS").iloc[0]
            render_sub_ai_reco(
                "Experiencia Regional",
                f"Región con menor NPS: {weakest['Region']} (NPS {weakest['NPS']}) con {weakest['5G Coverage %']:.0f}% cobertura 5G.",
                f"Priorizar expansión 5G en {weakest['Region']} y mejorar atención en tiendas WOM locales.",
                "Elevar NPS regional +4 puntos y reducir churn geográfico.",
                level="warning",
            )

    with sub_tab_fibra:
        st.markdown('<div class="sub-title">WOM Fibra/Hogar · Subscriber Analytics</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="sub-kpi-grid">
                <div class="sub-kpi-card"><div class="k">Total Suscriptores</div><div class="v">{fibra_total_subs/1000:.0f}K</div><div class="d">Base activa</div></div>
                <div class="sub-kpi-card"><div class="k">Net Adds (Mes)</div><div class="v">+{fibra_net_adds:,}</div><div class="d">Crecimiento neto</div></div>
                <div class="sub-kpi-card"><div class="k">ARPU Fibra</div><div class="v">CLP {fibra_arpu:,.0f}</div><div class="d">Promedio ponderado</div></div>
                <div class="sub-kpi-card"><div class="k">Churn Rate</div><div class="v">{fibra_churn_rate:.2f}%</div><div class="d">Mensual</div></div>
                <div class="sub-kpi-card"><div class="k">Avg Speed</div><div class="v">{fibra_avg_speed:.0f} Mbps</div><div class="d">Velocidad promedio</div></div>
                <div class="sub-kpi-card"><div class="k">FTTH Coverage</div><div class="v">72.3%</div><div class="d">Hogares pasados</div></div>
                <div class="sub-kpi-card"><div class="k">Bundle Rate</div><div class="v">{fibra_bundle_rate:.1f}%</div><div class="d">Con TV o Triple Play</div></div>
                <div class="sub-kpi-card warn"><div class="k">Competencia VTR</div><div class="v">1,420</div><div class="d">Bajas a VTR/Movistar</div></div>
            </div>
        """), unsafe_allow_html=True)

        fb_col1, fb_col2 = st.columns(2)
        with fb_col1:
            st.markdown('<div class="sub-mini-title">Altas vs Bajas y Base Fibra</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fb_bars = alt.Chart(fibra_monthly).transform_fold(
                    ["Adds", "Churned"], as_=["Metric", "Count"]
                ).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Count:Q", title="Altas / Bajas"),
                    color=alt.Color("Metric:N", scale=alt.Scale(domain=["Adds", "Churned"], range=["#10B981", "#EF4444"]), legend=alt.Legend(title=None)),
                    xOffset="Metric:N",
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Metric:N"), alt.Tooltip("Count:Q", format=",")],
                )
                fb_base_line = alt.Chart(fibra_monthly).mark_line(point=True, color="#6366F1", strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Base:Q", title="Base Total"),
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Base:Q", format=",")],
                )
                st.altair_chart(style_sub_chart(alt.layer(fb_bars, fb_base_line).resolve_scale(y="independent"), height=230), use_container_width=True)
                fb_net_total = int(fibra_monthly["Net Adds"].sum())
                render_sub_ai_reco(
                    "Crecimiento Fibra",
                    f"Base fibra creció +{fb_net_total:,} en los últimos 6 meses. Competencia VTR/Movistar presiona.",
                    "Acelerar instalaciones en comunas nuevas y promover bundles Fibra+TV para reducir churn.",
                    "Mantener crecimiento neto y mejorar rentabilidad por cliente.",
                )

        with fb_col2:
            st.markdown('<div class="sub-mini-title">Distribución por Plan Fibra</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fb_plan_bar = alt.Chart(fibra_plans).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22).encode(
                    x=alt.X("Subscribers K:Q", title="Suscriptores (Miles)"),
                    y=alt.Y("Plan:N", sort="-x", title=None),
                    color=alt.Color("Avg Speed Mbps:Q", scale=alt.Scale(domain=[200, 1000], range=["#29B5E8", "#6366F1"]), legend=alt.Legend(title="Velocidad")),
                    tooltip=["Plan:N", alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("ARPU CLP:Q", format=","), alt.Tooltip("Avg Speed Mbps:Q", format=".0f")],
                )
                st.altair_chart(style_sub_chart(fb_plan_bar, height=230), use_container_width=True)
                top_fb_plan = fibra_plans.loc[fibra_plans["Subscribers K"].idxmax()]
                render_sub_ai_reco(
                    "Mix de Planes Fibra",
                    f"WOM Hogar 300 Mbps lidera con {top_fb_plan['Subscribers K']:.0f}K suscriptores.",
                    "Promover upgrade a 600 Mbps y 1 Gbps con ofertas de instalación gratuita.",
                    "Incrementar ARPU promedio +12% y mejorar satisfacción.",
                )

        st.markdown('<div class="sub-mini-title">Razones de Baja Fibra</div>', unsafe_allow_html=True)
        fb_col3, fb_col4 = st.columns(2)
        with fb_col3:
            with st.container(border=True):
                fb_churn_bar = alt.Chart(fibra_churn_reasons).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=18, color="#EF4444").encode(
                    x=alt.X("Volume:Q", title="Clientes Perdidos"),
                    y=alt.Y("Reason:N", sort="-x", title=None),
                    tooltip=["Reason:N", alt.Tooltip("Volume:Q", format=",")],
                )
                st.altair_chart(style_sub_chart(fb_churn_bar, height=200), use_container_width=True)
                top_fb_reason = fibra_churn_reasons.sort_values("Volume", ascending=False).iloc[0]
                render_sub_ai_reco(
                    "Drivers de Churn",
                    f"Principal razón de baja: {top_fb_reason['Reason']} ({top_fb_reason['Volume']:,} clientes).",
                    "Lanzar campaña de retención con descuento y mejora de velocidad para usuarios en riesgo.",
                    "Reducir churn competitivo 20% y proteger base de alto valor.",
                    level="critical",
                )

        with fb_col4:
            with st.container(border=True):
                bundle_donut = alt.Chart(fibra_tv_bundle).mark_arc(innerRadius=55, outerRadius=95, cornerRadius=4, stroke="#FFFFFF", strokeWidth=2).encode(
                    theta=alt.Theta("Subscribers K:Q", stack=True),
                    color=alt.Color("Bundle:N", scale=alt.Scale(domain=["Fibra Only", "Fibra + TV", "Fibra + TV + Móvil"], range=["#94A3B8", "#6366F1", "#10B981"]), legend=alt.Legend(title=None)),
                    tooltip=["Bundle:N", alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("ARPU CLP:Q", format=","), alt.Tooltip("Churn %:Q", format=".1f")],
                )
                st.altair_chart(style_sub_chart(bundle_donut, height=200), use_container_width=True)
                render_sub_ai_reco(
                    "Bundles y Retención",
                    f"Clientes con bundle tienen {fibra_tv_bundle.loc[fibra_tv_bundle['Bundle']=='Fibra + TV + Móvil', 'Churn %'].iloc[0]:.1f}% churn vs {fibra_tv_bundle.loc[fibra_tv_bundle['Bundle']=='Fibra Only', 'Churn %'].iloc[0]:.1f}% sin bundle.",
                    "Promover Triple Play (Fibra+TV+Móvil) en base existente para reducir churn.",
                    "Incrementar bundle rate a 45% y reducir churn global 0.4pp.",
                )

        st.markdown('<div class="sub-mini-title">Calidad de Instalación y Servicio</div>', unsafe_allow_html=True)
        with st.container(border=True):
            install_bar = alt.Chart(fibra_install_metrics).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=18).encode(
                x=alt.X("Score:Q", title="Score %", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Metric:N", sort="-x", title=None),
                color=alt.Color("Score:Q", scale=alt.Scale(domain=[70, 100], range=["#F59E0B", "#10B981"]), legend=None),
                tooltip=[alt.Tooltip("Metric:N"), alt.Tooltip("Score:Q", title="Score %", format=".1f")],
            )
            st.altair_chart(style_sub_chart(install_bar, height=180), use_container_width=True)
            worst_metric = fibra_install_metrics.loc[fibra_install_metrics["Score"].idxmin()]
            render_sub_ai_reco(
                "Calidad Operacional",
                f"Métrica más débil: {worst_metric['Metric']} ({worst_metric['Score']:.1f}%).",
                f"Priorizar mejora en {worst_metric['Metric']} con capacitación técnicos y seguimiento proactivo.",
                "Elevar satisfacción post-instalación y reducir tickets de soporte.",
                level="warning",
            )

        st.markdown('<div class="sub-mini-title">Quejas Principales Fibra</div>', unsafe_allow_html=True)
        with st.container(border=True):
            complaint_bar = alt.Chart(fibra_complaint_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=18, color="#F59E0B").encode(
                x=alt.X("Volume:Q", title="Volumen de Quejas"),
                y=alt.Y("Reason:N", sort="-x", title=None),
                tooltip=["Reason:N", alt.Tooltip("Volume:Q", format=",")],
            )
            st.altair_chart(style_sub_chart(complaint_bar, height=200), use_container_width=True)
            top_complaint = fibra_complaint_df.sort_values("Volume", ascending=False).iloc[0]
            render_sub_ai_reco(
                "Drivers de Quejas",
                f"Principal queja: {top_complaint['Reason']} ({top_complaint['Volume']:,} casos).",
                f"Implementar monitoreo proactivo de velocidad y contacto automático cuando baja del SLA.",
                "Reducir quejas de velocidad 30% y mejorar NPS.",
                level="warning",
            )

        st.markdown('<div class="sub-mini-title">Retención Fibra: Campañas Activas</div>', unsafe_allow_html=True)
        with st.container(border=True):
            fb_ret_bars = alt.Chart(fibra_retention).transform_fold(
                ["Contacted", "Saved"], as_=["Metric", "Value"]
            ).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x=alt.X("Campaign:N", title=None),
                y=alt.Y("Value:Q", title="Clientes"),
                color=alt.Color("Metric:N", scale=alt.Scale(domain=["Contacted", "Saved"], range=["#94A3B8", "#10B981"]), legend=alt.Legend(title=None)),
                xOffset="Metric:N",
                tooltip=["Campaign:N", "Metric:N", alt.Tooltip("Value:Q", format=",")],
            )
            st.altair_chart(style_sub_chart(fb_ret_bars, height=220), use_container_width=True)
            best_fb_camp = fibra_retention.loc[fibra_retention["Save Rate %"].idxmax()]
            render_sub_ai_reco(
                "Efectividad Retención Fibra",
                f"Mejor campaña: {best_fb_camp['Campaign']} con {best_fb_camp['Save Rate %']:.1f}% tasa de salvación.",
                f"Escalar {best_fb_camp['Campaign']} a clientes con señales de riesgo hacia VTR.",
                "Incrementar saves mensuales +30% y reducir churn competitivo.",
            )

        st.markdown('<div class="sub-mini-title">Cobertura Regional Fibra y NPS</div>', unsafe_allow_html=True)
        with st.container(border=True):
            fb_region_scatter = alt.Chart(fibra_regions).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                x=alt.X("FTTH Coverage %:Q", title="Cobertura FTTH (%)", scale=alt.Scale(domain=[35, 85])),
                y=alt.Y("NPS:Q", title="NPS", scale=alt.Scale(domain=[38, 55])),
                size=alt.Size("Subscribers K:Q", scale=alt.Scale(range=[200, 1800]), legend=None),
                color=alt.Color("Region:N", legend=alt.Legend(title=None)),
                tooltip=["Region:N", alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("FTTH Coverage %:Q", format=".0f"), "NPS:Q"],
            )
            fb_region_labels = alt.Chart(fibra_regions).mark_text(dy=-14, fontSize=9, color="#1E293B").encode(
                x="FTTH Coverage %:Q", y="NPS:Q", text="Region:N"
            )
            st.altair_chart(style_sub_chart(fb_region_scatter + fb_region_labels, height=240), use_container_width=True)
            fb_weakest = fibra_regions.sort_values("NPS").iloc[0]
            render_sub_ai_reco(
                "Experiencia Regional Fibra",
                f"Región con menor NPS: {fb_weakest['Region']} (NPS {fb_weakest['NPS']}) con {fb_weakest['FTTH Coverage %']:.0f}% cobertura FTTH.",
                f"Priorizar expansión FTTH en {fb_weakest['Region']} y mejorar tiempos de instalación.",
                "Elevar NPS regional +5 puntos y aumentar penetración.",
                level="warning",
            )

elif selected_menu == "Revenue Analytics":
    import pandas as pd
    import altair as alt
    import pydeck as pdk

    REV_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
    }

    def style_rev_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(
                labelFont=REV_CHART_THEME["font"],
                titleFont=REV_CHART_THEME["font"],
                labelColor=REV_CHART_THEME["label_color"],
                titleColor=REV_CHART_THEME["label_color"],
                labelFontSize=11,
                titleFontSize=12,
                domain=False,
                gridColor=REV_CHART_THEME["grid_color"],
                gridOpacity=0.75,
            )
            .configure_legend(
                labelFont=REV_CHART_THEME["font"],
                titleFont=REV_CHART_THEME["font"],
                labelColor=REV_CHART_THEME["label_color"],
                titleColor=REV_CHART_THEME["label_color"],
                orient="top",
                direction="horizontal",
                symbolType="circle",
                symbolSize=100,
            )
        )

    def render_rev_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        st.markdown(
            f"""<div class="rev-ai-card {level}"><div class="rev-ai-head">🤖 AI Recommendation · {headline}</div><div class="rev-ai-line"><strong>Insight:</strong> {insight}</div><div class="rev-ai-line"><strong>Action:</strong> {action}</div><div class="rev-ai-line"><strong>Expected Impact:</strong> {impact}</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("""<style>
@keyframes rev-fade-up { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes rev-shimmer { 0% { left: -40%; } 100% { left: 120%; } }
@keyframes rev-pulse-dot { 0%,100% { transform: scale(1); opacity: 0.7; } 50% { transform: scale(1.25); opacity: 1; } }
.rev-title { position: relative; overflow: hidden; display: flex; align-items: center; gap: 0.55rem; margin: 1.2rem 0 0.8rem; padding: 0.6rem 0.85rem; border-radius: 12px; border: 1px solid #DBEAFE; background: linear-gradient(135deg, #F0F8FF 0%, #EEF2FF 100%); color: #1B2A4E; font-size: 1rem; font-weight: 700; animation: rev-fade-up 0.4s ease-out both; }
.rev-title::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: linear-gradient(135deg, #29B5E8, #6366F1); animation: rev-pulse-dot 1.8s ease-in-out infinite; }
.rev-title::after { content: ""; position: absolute; top: 0; left: -40%; width: 34%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent); animation: rev-shimmer 3.2s ease-in-out infinite; }
.rev-mini-title { display: inline-flex; align-items: center; gap: 0.4rem; margin: 0.15rem 0 0.55rem; font-size: 0.9rem; font-weight: 700; color: #1E3A8A; }
.rev-mini-title::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: linear-gradient(135deg, #22C1EE, #8B5CF6); }
.rev-pulse { position: relative; overflow: hidden; border-radius: 14px; border: 1px solid #BFDBFE; background: linear-gradient(135deg, #EFF6FF 0%, #ECFEFF 100%); padding: 1rem 1.1rem; margin-bottom: 1rem; }
.rev-pulse::before { content: ""; position: absolute; top: 0; left: -50%; width: 40%; height: 100%; background: linear-gradient(90deg, transparent, rgba(41,181,232,0.2), transparent); animation: rev-shimmer 3s ease-in-out infinite; }
.rev-pulse-head { position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.rev-pulse-title { color: #1E3A8A; font-weight: 700; font-size: 0.92rem; }
.rev-pulse-live { color: #10B981; font-size: 0.74rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.35rem; }
.rev-pulse-live::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: #10B981; animation: rev-pulse-dot 1.2s ease-in-out infinite; }
.rev-pulse-grid { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.6rem; }
.rev-pulse-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.62rem 0.7rem; animation: rev-fade-up 0.35s ease-out both; }
.rev-pulse-card:nth-child(1){animation-delay:.05s}.rev-pulse-card:nth-child(2){animation-delay:.1s}.rev-pulse-card:nth-child(3){animation-delay:.16s}.rev-pulse-card:nth-child(4){animation-delay:.22s}.rev-pulse-card:nth-child(5){animation-delay:.28s}.rev-pulse-card:nth-child(6){animation-delay:.34s}
.rev-pulse-label { color: #64748B; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.2rem; }
.rev-pulse-value { color: #0F172A; font-size: 1.2rem; font-weight: 800; line-height: 1.15; }
.rev-pulse-delta { margin-top: 0.2rem; color: #059669; font-size: 0.72rem; font-weight: 700; }
.rev-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-bottom: 0.75rem; }
.rev-kpi-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.55rem 0.62rem; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04); animation: rev-fade-up 0.35s ease-out both; }
.rev-kpi-card .k { color: #64748B; font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.04em; }
.rev-kpi-card .v { color: #0F172A; font-size: 1.02rem; font-weight: 800; margin-top: 0.12rem; line-height: 1.15; }
.rev-kpi-card .d { color: #059669; font-size: 0.68rem; font-weight: 700; margin-top: 0.14rem; }
.rev-kpi-card.warn .d { color: #B45309; }
.rev-kpi-card.crit .d { color: #B91C1C; }
.rev-ai-card { margin-top: 0.6rem; border-radius: 10px; border: 1px solid #D1E9FF; background: linear-gradient(135deg, #F8FBFF 0%, #EEF6FF 100%); padding: 0.62rem 0.78rem; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05); animation: rev-fade-up 0.35s ease-out both; }
.rev-ai-card.warning { border-color: #FCD34D; background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); }
.rev-ai-card.critical { border-color: #FCA5A5; background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); }
.rev-ai-head { color: #1E3A8A; font-size: 0.78rem; font-weight: 700; margin-bottom: 0.28rem; }
.rev-ai-card.warning .rev-ai-head { color: #92400E; }
.rev-ai-card.critical .rev-ai-head { color: #991B1B; }
.rev-ai-line { color: #334155; font-size: 0.77rem; line-height: 1.34; margin: 0.12rem 0; }
@media (max-width: 980px) { .rev-pulse-grid { grid-template-columns: repeat(3, 1fr); } .rev-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .rev-pulse-grid, .rev-kpi-grid { grid-template-columns: 1fr; } }
</style>""", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # WOM Revenue Data - Móvil + Fibra/Hogar Combined
    # -------------------------------------------------------------------
    rev_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Móvil Revenue M": [36.8, 37.4, 38.2, 37.9, 38.8, 39.6],
        "Fibra Revenue M": [11.2, 11.6, 12.1, 12.4, 12.9, 13.4],
        "TV Revenue M": [1.8, 1.9, 2.0, 2.1, 2.2, 2.3],
        "Collected M": [46.2, 47.1, 48.4, 48.6, 50.1, 51.2],
        "Discounts M": [2.8, 2.9, 3.0, 3.1, 3.2, 3.3],
    })
    rev_monthly["Total Revenue M"] = rev_monthly["Móvil Revenue M"] + rev_monthly["Fibra Revenue M"] + rev_monthly["TV Revenue M"]
    rev_monthly["Net Revenue M"] = rev_monthly["Total Revenue M"] - rev_monthly["Discounts M"]
    rev_monthly["Collection %"] = (rev_monthly["Collected M"] / rev_monthly["Total Revenue M"] * 100).round(1)

    rev_by_product = pd.DataFrame({
        "Product": ["WOM Móvil", "WOM Fibra", "WOM TV"],
        "Revenue M": [39.6, 13.4, 2.3],
        "Growth %": [7.6, 19.6, 27.8],
        "Margin %": [52.4, 48.2, 62.1],
        "Subscribers K": [2852, 485, 173],
    })

    movil_plans_rev = pd.DataFrame({
        "Plan": ["WOM Libre 30GB", "WOM Libre 50GB", "WOM Libre Ilimitado", "WOM Prepago", "WOM Empresas Móvil"],
        "Subscribers K": [680, 920, 540, 480, 232],
        "ARPU CLP K": [9.9, 12.9, 18.9, 5.2, 24.5],
        "Revenue M": [6.7, 11.9, 10.2, 2.5, 5.7],
        "Growth %": [4.2, 8.4, 12.1, -2.8, 15.4],
    })

    fibra_plans_rev = pd.DataFrame({
        "Plan": ["WOM Hogar 300 Mbps", "WOM Hogar 600 Mbps", "WOM Gamer 1 Gbps", "WOM Empresas Fibra"],
        "Subscribers K": [185, 168, 82, 50],
        "ARPU CLP K": [18.9, 24.9, 34.9, 48.5],
        "Revenue M": [3.5, 4.2, 2.9, 2.4],
        "Growth %": [12.4, 22.8, 34.2, 18.6],
    })

    rev_regions = pd.DataFrame({
        "Region": ["Metropolitana", "Valparaíso", "Biobío", "Maule", "Araucanía", "Otros"],
        "Móvil M": [23.8, 5.1, 4.5, 2.9, 2.2, 1.1],
        "Fibra M": [9.4, 1.8, 1.2, 0.5, 0.3, 0.2],
        "Total M": [33.2, 6.9, 5.7, 3.4, 2.5, 1.3],
        "Growth %": [8.2, 11.4, 14.2, 9.8, 12.1, 6.4],
    })

    rev_channels = pd.DataFrame({
        "Channel": ["WOM App / Web", "Tiendas WOM", "Call Center", "Distribuidores", "Empresas Directo"],
        "Móvil M": [14.2, 12.8, 6.4, 4.1, 2.1],
        "Fibra M": [4.8, 3.2, 2.1, 1.8, 1.5],
        "Total M": [19.0, 16.0, 8.5, 5.9, 3.6],
        "CAC K CLP": [8.2, 18.4, 12.6, 22.1, 32.4],
    })

    rev_aging = pd.DataFrame({
        "Bucket": ["Al día", "1-30 días", "31-60 días", "61-90 días", "90+ días"],
        "Móvil M": [34.2, 3.1, 1.4, 0.6, 0.3],
        "Fibra M": [11.8, 0.9, 0.4, 0.2, 0.1],
        "Total M": [46.0, 4.0, 1.8, 0.8, 0.4],
    })

    rev_risk = pd.DataFrame({
        "Risk Driver": ["Portabilidad Móvil", "Churn Fibra Competencia", "Morosidad Prepago", "Downgrades", "Disputas"],
        "Exposure M": [4.2, 2.1, 1.8, 1.2, 0.6],
        "Likelihood": [4.4, 3.8, 3.2, 2.8, 2.4],
        "Product": ["Móvil", "Fibra", "Móvil", "Ambos", "Ambos"],
    })

    arpu_trend = pd.DataFrame({
        "Month": rev_monthly["Month"],
        "Móvil ARPU K": [12.6, 12.7, 12.8, 12.8, 12.9, 12.85],
        "Fibra ARPU K": [23.8, 24.1, 24.4, 24.6, 24.8, 24.9],
    })

    bundle_revenue = pd.DataFrame({
        "Bundle Type": ["Móvil Only", "Fibra Only", "Fibra + TV", "Triple Play (Móvil+Fibra+TV)"],
        "Subscribers K": [2420, 312, 128, 45],
        "Revenue M": [28.4, 7.4, 4.2, 2.8],
        "ARPU K CLP": [11.7, 23.7, 32.8, 62.2],
        "Churn %": [1.4, 1.8, 1.2, 0.8],
    })

    sales_pipeline = pd.DataFrame({
        "Stage": ["Lead", "Calificado", "Propuesta", "Negociación", "Cerrado"],
        "Móvil K": [42.0, 28.0, 18.0, 12.0, 8.4],
        "Fibra K": [12.0, 8.0, 5.2, 3.4, 2.2],
        "Value M": [8.4, 6.2, 4.8, 3.6, 2.8],
    })

    competitor_impact = pd.DataFrame({
        "Competitor": ["Entel", "Movistar", "Claro", "VTR", "GTD"],
        "Lost Móvil K": [5.2, 4.1, 2.8, 0, 0],
        "Lost Fibra K": [0, 0.8, 0, 1.4, 0.6],
        "Revenue Impact M": [1.8, 1.4, 0.9, 0.5, 0.2],
    })

    geo_sales_data = pd.DataFrame({
        "City": [
            "Santiago Centro", "Providencia", "Las Condes", "Ñuñoa", "La Florida",
            "Maipú", "Puente Alto", "Vitacura", "Lo Barnechea", "San Bernardo",
            "Valparaíso", "Viña del Mar", "Concón", "Quilpué", "Villa Alemana",
            "Concepción", "Talcahuano", "Chillán", "Los Ángeles", "Coronel",
            "Temuco", "Villarrica", "Pucón", "Angol", "Victoria",
            "Talca", "Curicó", "Linares", "Constitución", "Cauquenes",
            "Antofagasta", "Calama", "Iquique", "Arica", "Copiapó",
            "Puerto Montt", "Osorno", "Valdivia", "Castro", "Ancud",
            "La Serena", "Coquimbo", "Ovalle", "Illapel", "Vicuña",
            "Rancagua", "San Fernando", "Santa Cruz", "Rengo", "Machalí",
        ],
        "Region": [
            "Metropolitana", "Metropolitana", "Metropolitana", "Metropolitana", "Metropolitana",
            "Metropolitana", "Metropolitana", "Metropolitana", "Metropolitana", "Metropolitana",
            "Valparaíso", "Valparaíso", "Valparaíso", "Valparaíso", "Valparaíso",
            "Biobío", "Biobío", "Biobío", "Biobío", "Biobío",
            "Araucanía", "Araucanía", "Araucanía", "Araucanía", "Araucanía",
            "Maule", "Maule", "Maule", "Maule", "Maule",
            "Antofagasta", "Antofagasta", "Tarapacá", "Arica y Parinacota", "Atacama",
            "Los Lagos", "Los Lagos", "Los Ríos", "Los Lagos", "Los Lagos",
            "Coquimbo", "Coquimbo", "Coquimbo", "Coquimbo", "Coquimbo",
            "O'Higgins", "O'Higgins", "O'Higgins", "O'Higgins", "O'Higgins",
        ],
        "lat": [
            -33.4489, -33.4264, -33.4103, -33.4569, -33.5167,
            -33.5100, -33.6117, -33.3833, -33.3500, -33.5928,
            -33.0458, -33.0153, -32.9283, -33.0475, -33.0419,
            -36.8270, -36.7249, -36.6066, -37.4693, -37.0292,
            -38.7359, -39.2856, -39.2726, -37.7947, -38.2333,
            -35.4264, -34.9833, -35.8467, -35.3333, -35.9667,
            -23.6509, -22.4560, -20.2133, -18.4783, -27.3668,
            -41.4693, -40.5740, -39.8142, -42.4800, -41.8667,
            -29.9027, -29.9533, -30.6017, -31.6333, -30.0333,
            -34.1708, -34.5858, -34.6333, -34.4167, -34.1500,
        ],
        "lon": [
            -70.6693, -70.6109, -70.5672, -70.5975, -70.5981,
            -70.7578, -70.5758, -70.5667, -70.5167, -70.6994,
            -71.6197, -71.5517, -71.5083, -71.4406, -71.3725,
            -73.0503, -73.1169, -72.1028, -72.3536, -73.1583,
            -72.5904, -72.2286, -71.9544, -72.7167, -72.3333,
            -71.6554, -71.2333, -71.5933, -72.4167, -72.3167,
            -70.3975, -68.9256, -70.1500, -70.3126, -70.3314,
            -72.9424, -73.1353, -73.2459, -73.7622, -73.8333,
            -71.2519, -71.3436, -71.2000, -71.1667, -70.7000,
            -70.7444, -71.0094, -71.4000, -70.8667, -70.4167,
        ],
        "Móvil Revenue M": [
            4.8, 3.2, 2.9, 2.1, 2.4, 1.9, 1.8, 1.6, 1.2, 0.9,
            1.4, 1.2, 0.6, 0.5, 0.4, 1.2, 0.8, 0.6, 0.5, 0.4,
            0.9, 0.4, 0.3, 0.2, 0.2, 0.8, 0.5, 0.3, 0.2, 0.1,
            0.9, 0.4, 0.6, 0.4, 0.3, 0.5, 0.3, 0.4, 0.2, 0.1,
            0.4, 0.3, 0.2, 0.1, 0.1, 0.6, 0.3, 0.2, 0.2, 0.1,
        ],
        "Fibra Revenue M": [
            2.1, 1.4, 1.2, 0.9, 0.8, 0.6, 0.5, 0.7, 0.5, 0.3,
            0.5, 0.4, 0.2, 0.2, 0.1, 0.4, 0.2, 0.1, 0.1, 0.1,
            0.2, 0.1, 0.05, 0.03, 0.02, 0.15, 0.1, 0.05, 0.03, 0.02,
            0.2, 0.1, 0.15, 0.1, 0.08, 0.12, 0.08, 0.1, 0.04, 0.02,
            0.1, 0.08, 0.04, 0.02, 0.01, 0.15, 0.08, 0.05, 0.04, 0.03,
        ],
        "Subscribers Móvil K": [
            142, 95, 86, 62, 71, 56, 53, 47, 35, 27,
            42, 35, 18, 15, 12, 35, 24, 18, 15, 12,
            27, 12, 9, 6, 6, 24, 15, 9, 6, 3,
            27, 12, 18, 12, 9, 15, 9, 12, 6, 3,
            12, 9, 6, 3, 3, 18, 9, 6, 6, 3,
        ],
        "Subscribers Fibra K": [
            52, 35, 30, 22, 20, 15, 12, 18, 12, 8,
            12, 10, 5, 5, 3, 10, 5, 3, 2, 2,
            5, 2, 1, 0.8, 0.5, 4, 2.5, 1.2, 0.8, 0.5,
            5, 2.5, 4, 2.5, 2, 3, 2, 2.5, 1, 0.5,
            2.5, 2, 1, 0.5, 0.3, 4, 2, 1.2, 1, 0.8,
        ],
        "Tiendas WOM": [
            8, 4, 3, 2, 3, 2, 2, 1, 1, 1,
            2, 2, 1, 1, 1, 2, 1, 1, 1, 0,
            1, 1, 0, 0, 0, 1, 1, 0, 0, 0,
            1, 1, 1, 1, 0, 1, 1, 1, 0, 0,
            1, 1, 0, 0, 0, 1, 0, 0, 0, 0,
        ],
        "FTTH Coverage %": [
            92, 95, 97, 88, 78, 72, 65, 98, 96, 58,
            82, 85, 78, 68, 62, 75, 68, 55, 48, 42,
            62, 45, 38, 32, 28, 58, 52, 38, 28, 22,
            68, 52, 72, 65, 48, 55, 48, 58, 35, 28,
            58, 52, 42, 32, 28, 62, 48, 42, 38, 35,
        ],
        "5G Coverage %": [
            88, 92, 95, 85, 72, 65, 58, 96, 94, 48,
            75, 78, 68, 55, 48, 68, 58, 42, 35, 28,
            52, 35, 28, 22, 18, 48, 42, 28, 18, 12,
            62, 48, 65, 58, 42, 45, 38, 48, 25, 18,
            48, 42, 32, 22, 18, 55, 42, 35, 28, 25,
        ],
        "Churn Móvil %": [
            1.2, 1.1, 1.0, 1.3, 1.5, 1.6, 1.8, 0.9, 0.8, 2.0,
            1.4, 1.3, 1.5, 1.6, 1.7, 1.5, 1.6, 1.8, 1.9, 2.0,
            1.6, 1.8, 1.9, 2.1, 2.2, 1.7, 1.8, 2.0, 2.2, 2.4,
            1.4, 1.6, 1.3, 1.5, 1.7, 1.7, 1.8, 1.6, 2.0, 2.2,
            1.5, 1.6, 1.8, 2.0, 2.1, 1.5, 1.7, 1.8, 1.9, 1.8,
        ],
        "Churn Fibra %": [
            1.5, 1.4, 1.3, 1.6, 1.8, 2.0, 2.2, 1.2, 1.1, 2.4,
            1.7, 1.6, 1.8, 2.0, 2.1, 1.9, 2.0, 2.2, 2.4, 2.5,
            2.0, 2.2, 2.4, 2.6, 2.8, 2.1, 2.2, 2.5, 2.7, 2.9,
            1.8, 2.0, 1.7, 1.9, 2.1, 2.1, 2.2, 2.0, 2.5, 2.7,
            1.9, 2.0, 2.2, 2.4, 2.5, 1.9, 2.1, 2.2, 2.3, 2.2,
        ],
        "ARPU Móvil K": [
            14.2, 15.8, 16.5, 13.8, 12.4, 11.8, 11.2, 17.2, 18.5, 10.5,
            13.2, 13.8, 14.5, 12.2, 11.8, 12.8, 12.2, 11.5, 11.0, 10.8,
            12.5, 11.8, 12.2, 10.8, 10.5, 12.2, 11.8, 10.8, 10.2, 9.8,
            13.5, 12.8, 13.8, 12.5, 11.2, 12.2, 11.5, 12.8, 10.8, 10.2,
            12.8, 12.2, 11.2, 10.5, 10.2, 13.2, 12.2, 11.5, 11.2, 10.8,
        ],
        "ARPU Fibra K": [
            26.5, 28.2, 30.5, 25.8, 23.2, 22.5, 21.8, 32.5, 35.2, 20.5,
            24.8, 25.5, 26.2, 22.8, 21.5, 24.2, 23.5, 21.2, 20.5, 19.8,
            23.5, 22.2, 23.8, 20.5, 19.8, 22.8, 22.2, 20.2, 19.2, 18.5,
            25.2, 24.2, 26.5, 24.8, 22.2, 23.2, 22.5, 24.8, 20.8, 19.5,
            24.2, 23.5, 21.8, 20.2, 19.5, 24.8, 23.2, 22.2, 21.5, 20.8,
        ],
        "Growth Móvil %": [
            8.5, 9.2, 7.8, 6.5, 5.8, 5.2, 4.8, 10.2, 11.5, 3.8,
            7.2, 7.8, 8.5, 6.2, 5.5, 6.8, 6.2, 5.2, 4.5, 4.0,
            8.2, 9.5, 10.2, 7.5, 6.8, 6.5, 6.0, 5.2, 4.2, 3.5,
            9.8, 8.5, 10.5, 9.2, 7.8, 7.5, 6.8, 8.2, 6.2, 5.5,
            7.8, 7.2, 6.2, 5.2, 4.8, 7.2, 6.5, 5.8, 5.2, 4.8,
        ],
        "Growth Fibra %": [
            18.5, 20.2, 22.5, 17.2, 15.8, 14.5, 13.2, 24.5, 26.8, 11.5,
            16.2, 17.5, 19.2, 14.5, 13.2, 15.8, 14.2, 12.5, 11.2, 10.5,
            18.5, 22.2, 25.5, 18.2, 16.5, 14.8, 13.8, 12.2, 10.8, 9.5,
            20.5, 18.2, 22.8, 20.2, 17.5, 16.8, 15.2, 18.5, 14.2, 12.8,
            17.2, 16.5, 14.2, 12.5, 11.2, 16.5, 15.2, 14.2, 13.2, 12.5,
        ],
        "Segment": [
            "Premium", "Premium", "Premium", "Mass", "Mass",
            "Mass", "Value", "Premium", "Premium", "Value",
            "Mass", "Mass", "Premium", "Mass", "Value",
            "Mass", "Mass", "Value", "Value", "Value",
            "Mass", "Value", "Premium", "Value", "Value",
            "Mass", "Mass", "Value", "Value", "Value",
            "Mass", "Value", "Mass", "Mass", "Value",
            "Mass", "Value", "Mass", "Value", "Value",
            "Mass", "Mass", "Value", "Value", "Value",
            "Mass", "Value", "Value", "Value", "Value",
        ],
        "Channel Mix": [
            "Digital", "Digital", "Digital", "Tienda", "Tienda",
            "Tienda", "Distribuidor", "Digital", "Digital", "Distribuidor",
            "Tienda", "Tienda", "Digital", "Distribuidor", "Distribuidor",
            "Tienda", "Tienda", "Distribuidor", "Distribuidor", "Distribuidor",
            "Tienda", "Distribuidor", "Digital", "Distribuidor", "Distribuidor",
            "Tienda", "Tienda", "Distribuidor", "Distribuidor", "Distribuidor",
            "Tienda", "Distribuidor", "Tienda", "Tienda", "Distribuidor",
            "Tienda", "Distribuidor", "Tienda", "Distribuidor", "Distribuidor",
            "Tienda", "Tienda", "Distribuidor", "Distribuidor", "Distribuidor",
            "Tienda", "Distribuidor", "Distribuidor", "Distribuidor", "Distribuidor",
        ],
    })
    geo_sales_data["Total Revenue M"] = geo_sales_data["Móvil Revenue M"] + geo_sales_data["Fibra Revenue M"]
    geo_sales_data["Total Subscribers K"] = geo_sales_data["Subscribers Móvil K"] + geo_sales_data["Subscribers Fibra K"]

    # Computed metrics
    latest = rev_monthly.iloc[-1]
    prev = rev_monthly.iloc[-2]
    total_mrr = float(latest["Net Revenue M"])
    total_arr = total_mrr * 12
    movil_mrr = float(latest["Móvil Revenue M"])
    fibra_mrr = float(latest["Fibra Revenue M"])
    tv_mrr = float(latest["TV Revenue M"])
    collection_rate = float(latest["Collection %"])
    mrr_growth = (latest["Net Revenue M"] - prev["Net Revenue M"]) / prev["Net Revenue M"] * 100
    movil_share = (movil_mrr / (movil_mrr + fibra_mrr + tv_mrr)) * 100
    fibra_share = (fibra_mrr / (movil_mrr + fibra_mrr + tv_mrr)) * 100
    at_risk_rev_m = rev_risk["Exposure M"].sum()
    movil_arpu = float(arpu_trend.iloc[-1]["Móvil ARPU K"])
    fibra_arpu = float(arpu_trend.iloc[-1]["Fibra ARPU K"])

    st.markdown(dedent(f"""
    <div class="rev-pulse">
        <div class="rev-pulse-head">
            <span class="rev-pulse-title">💰 WOM Revenue Pulse · Móvil + Fibra + TV</span>
            <span class="rev-pulse-live">Live</span>
        </div>
        <div class="rev-pulse-grid">
            <div class="rev-pulse-card"><div class="rev-pulse-label">MRR Total</div><div class="rev-pulse-value">CLP {total_mrr:.1f}M</div><div class="rev-pulse-delta">↑ {mrr_growth:.1f}% MoM</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Móvil MRR</div><div class="rev-pulse-value">CLP {movil_mrr:.1f}M</div><div class="rev-pulse-delta">{movil_share:.0f}% del total</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Fibra MRR</div><div class="rev-pulse-value">CLP {fibra_mrr:.1f}M</div><div class="rev-pulse-delta">{fibra_share:.0f}% del total</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Cobranza</div><div class="rev-pulse-value">{collection_rate:.1f}%</div><div class="rev-pulse-delta">Disciplina de caja</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">ARR Total</div><div class="rev-pulse-value">CLP {total_arr:.0f}M</div><div class="rev-pulse-delta">Run-rate anualizado</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Revenue at Risk</div><div class="rev-pulse-value">CLP {at_risk_rev_m:.1f}M</div><div class="rev-pulse-delta">Exposición watchlist</div></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    rev_tab_movil, rev_tab_fibra, rev_tab_map, rev_tab_channels, rev_tab_risk = st.tabs(
        ["📱 Revenue Móvil", "🏠 Revenue Fibra/Hogar", "🗺️ Mapa Geográfico", "🏪 Canales & Regiones", "⚠️ Riesgo & Cobranza"]
    )

    with rev_tab_movil:
        st.markdown('<div class="rev-title">WOM Móvil · Revenue Analytics</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Revenue Móvil</div><div class="v">CLP {movil_mrr:.1f}M</div><div class="d">MRR mensual</div></div>
                <div class="rev-kpi-card"><div class="k">ARPU Móvil</div><div class="v">CLP {movil_arpu:.2f}K</div><div class="d">Por suscriptor</div></div>
                <div class="rev-kpi-card"><div class="k">Crecimiento</div><div class="v">+7.6%</div><div class="d">vs. trimestre anterior</div></div>
                <div class="rev-kpi-card"><div class="k">Margen</div><div class="v">52.4%</div><div class="d">Margen bruto</div></div>
                <div class="rev-kpi-card"><div class="k">Suscriptores</div><div class="v">2.85M</div><div class="d">Base activa</div></div>
                <div class="rev-kpi-card"><div class="k">5G Revenue</div><div class="v">CLP 18.2M</div><div class="d">46% del móvil</div></div>
                <div class="rev-kpi-card warn"><div class="k">Prepago Decline</div><div class="v">-2.8%</div><div class="d">Migración a postpago</div></div>
                <div class="rev-kpi-card"><div class="k">Empresas Móvil</div><div class="v">CLP 5.7M</div><div class="d">+15.4% crecimiento</div></div>
            </div>
        """), unsafe_allow_html=True)

        mv_rev_col1, mv_rev_col2 = st.columns(2)
        with mv_rev_col1:
            st.markdown('<div class="rev-mini-title">Revenue por Plan Móvil</div>', unsafe_allow_html=True)
            with st.container(border=True):
                plan_bar = alt.Chart(movil_plans_rev).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=20).encode(
                    x=alt.X("Revenue M:Q", title="Revenue (CLP M)"),
                    y=alt.Y("Plan:N", sort="-x", title=None),
                    color=alt.Color("Growth %:Q", scale=alt.Scale(domain=[-5, 20], range=["#EF4444", "#10B981"]), legend=alt.Legend(title="Crecimiento %")),
                    tooltip=["Plan:N", alt.Tooltip("Revenue M:Q", format=".1f"), alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("ARPU CLP K:Q", format=".1f"), alt.Tooltip("Growth %:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(plan_bar, height=220), use_container_width=True)
                top_plan = movil_plans_rev.loc[movil_plans_rev["Revenue M"].idxmax()]
                render_rev_ai_reco(
                    "Revenue por Plan",
                    f"WOM Libre 50GB genera CLP {top_plan['Revenue M']:.1f}M con {top_plan['Growth %']:.1f}% crecimiento.",
                    "Promover migración de 30GB a 50GB con ofertas de equipo 5G.",
                    "Incrementar revenue +8% en segmento Libre.",
                )

        with mv_rev_col2:
            st.markdown('<div class="rev-mini-title">Tendencia Revenue Móvil</div>', unsafe_allow_html=True)
            with st.container(border=True):
                movil_trend = alt.Chart(rev_monthly).mark_area(
                    opacity=0.6,
                    color="#10B981",
                    line={"color": "#10B981", "strokeWidth": 2},
                ).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Móvil Revenue M:Q", title="Revenue (CLP M)"),
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Móvil Revenue M:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(movil_trend, height=220), use_container_width=True)
                growth_6m = ((rev_monthly.iloc[-1]["Móvil Revenue M"] - rev_monthly.iloc[0]["Móvil Revenue M"]) / rev_monthly.iloc[0]["Móvil Revenue M"] * 100)
                render_rev_ai_reco(
                    "Tendencia Móvil",
                    f"Revenue móvil creció {growth_6m:.1f}% en 6 meses, impulsado por 5G y Empresas.",
                    "Mantener momentum con campañas 5G device trade-in y bundles empresariales.",
                    "Alcanzar CLP 42M MRR móvil al cierre Q2.",
                )

        st.markdown('<div class="rev-mini-title">ARPU Móvil por Mes</div>', unsafe_allow_html=True)
        with st.container(border=True):
            arpu_line = alt.Chart(arpu_trend).mark_line(point=True, strokeWidth=3, color="#29B5E8").encode(
                x=alt.X("Month:N", title=None),
                y=alt.Y("Móvil ARPU K:Q", title="ARPU (CLP K)", scale=alt.Scale(domain=[12.4, 13.2])),
                tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Móvil ARPU K:Q", format=".2f")],
            )
            st.altair_chart(style_rev_chart(arpu_line, height=180), use_container_width=True)

        st.markdown('<div class="rev-mini-title">Impacto Competencia en Revenue Móvil</div>', unsafe_allow_html=True)
        with st.container(border=True):
            comp_bar = alt.Chart(competitor_impact).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=18, color="#EF4444").encode(
                x=alt.X("Revenue Impact M:Q", title="Impacto Revenue (CLP M)"),
                y=alt.Y("Competitor:N", sort="-x", title=None),
                tooltip=["Competitor:N", alt.Tooltip("Lost Móvil K:Q", format=","), alt.Tooltip("Revenue Impact M:Q", format=".1f")],
            )
            st.altair_chart(style_rev_chart(comp_bar, height=200), use_container_width=True)
            top_comp = competitor_impact.loc[competitor_impact["Revenue Impact M"].idxmax()]
            render_rev_ai_reco(
                "Fuga Competitiva",
                f"Entel genera mayor impacto con CLP {top_comp['Revenue Impact M']:.1f}M revenue perdido.",
                "Lanzar campaña anti-Entel con match de precio y beneficios 5G exclusivos.",
                "Recuperar CLP 0.6M revenue mensual de portabilidad.",
                level="critical",
            )

    with rev_tab_fibra:
        st.markdown('<div class="rev-title">WOM Fibra/Hogar · Revenue Analytics</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Revenue Fibra</div><div class="v">CLP {fibra_mrr:.1f}M</div><div class="d">MRR mensual</div></div>
                <div class="rev-kpi-card"><div class="k">ARPU Fibra</div><div class="v">CLP {fibra_arpu:.1f}K</div><div class="d">Por suscriptor</div></div>
                <div class="rev-kpi-card"><div class="k">Crecimiento</div><div class="v">+19.6%</div><div class="d">vs. trimestre anterior</div></div>
                <div class="rev-kpi-card"><div class="k">Margen</div><div class="v">48.2%</div><div class="d">Margen bruto</div></div>
                <div class="rev-kpi-card"><div class="k">Suscriptores</div><div class="v">485K</div><div class="d">Base activa</div></div>
                <div class="rev-kpi-card"><div class="k">TV Revenue</div><div class="v">CLP {tv_mrr:.1f}M</div><div class="d">+27.8% crecimiento</div></div>
                <div class="rev-kpi-card"><div class="k">Bundle ARPU</div><div class="v">CLP 32.8K</div><div class="d">Fibra + TV</div></div>
                <div class="rev-kpi-card warn"><div class="k">Empresas Fibra</div><div class="v">CLP 2.4M</div><div class="d">+18.6% crecimiento</div></div>
            </div>
        """), unsafe_allow_html=True)

        fb_rev_col1, fb_rev_col2 = st.columns(2)
        with fb_rev_col1:
            st.markdown('<div class="rev-mini-title">Revenue por Plan Fibra</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fb_plan_bar = alt.Chart(fibra_plans_rev).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=20).encode(
                    x=alt.X("Revenue M:Q", title="Revenue (CLP M)"),
                    y=alt.Y("Plan:N", sort="-x", title=None),
                    color=alt.Color("Growth %:Q", scale=alt.Scale(domain=[10, 40], range=["#29B5E8", "#10B981"]), legend=alt.Legend(title="Crecimiento %")),
                    tooltip=["Plan:N", alt.Tooltip("Revenue M:Q", format=".1f"), alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("ARPU CLP K:Q", format=".1f"), alt.Tooltip("Growth %:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(fb_plan_bar, height=220), use_container_width=True)
                top_fb_plan = fibra_plans_rev.loc[fibra_plans_rev["Growth %"].idxmax()]
                render_rev_ai_reco(
                    "Crecimiento Fibra",
                    f"WOM Gamer 1 Gbps lidera crecimiento con +{top_fb_plan['Growth %']:.1f}%.",
                    "Expandir marketing de Gamer 1G en segmento gamer y streaming.",
                    "Incrementar penetración de planes premium +15%.",
                )

        with fb_rev_col2:
            st.markdown('<div class="rev-mini-title">Tendencia Revenue Fibra + TV</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fibra_area = alt.Chart(rev_monthly).mark_area(opacity=0.5, color="#6366F1").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Fibra Revenue M:Q", title="Revenue (CLP M)"),
                )
                tv_area = alt.Chart(rev_monthly).mark_area(opacity=0.5, color="#F59E0B").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("TV Revenue M:Q", title="Revenue (CLP M)"),
                )
                st.altair_chart(style_rev_chart(fibra_area + tv_area, height=220), use_container_width=True)
                fb_growth = ((rev_monthly.iloc[-1]["Fibra Revenue M"] - rev_monthly.iloc[0]["Fibra Revenue M"]) / rev_monthly.iloc[0]["Fibra Revenue M"] * 100)
                render_rev_ai_reco(
                    "Tendencia Fibra",
                    f"Revenue Fibra creció {fb_growth:.1f}% en 6 meses. TV crece aún más rápido.",
                    "Potenciar bundles Fibra+TV con promociones de instalación gratuita.",
                    "Alcanzar CLP 16M MRR Fibra+TV al cierre Q2.",
                )

        st.markdown('<div class="rev-mini-title">Revenue por Tipo de Bundle</div>', unsafe_allow_html=True)
        with st.container(border=True):
            bundle_bar = alt.Chart(bundle_revenue).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=32).encode(
                x=alt.X("Bundle Type:N", title=None),
                y=alt.Y("Revenue M:Q", title="Revenue (CLP M)"),
                color=alt.Color("ARPU K CLP:Q", scale=alt.Scale(domain=[10, 65], range=["#94A3B8", "#10B981"]), legend=alt.Legend(title="ARPU (K)")),
                tooltip=["Bundle Type:N", alt.Tooltip("Revenue M:Q", format=".1f"), alt.Tooltip("Subscribers K:Q", format=","), alt.Tooltip("ARPU K CLP:Q", format=".1f"), alt.Tooltip("Churn %:Q", format=".1f")],
            )
            st.altair_chart(style_rev_chart(bundle_bar, height=220), use_container_width=True)
            triple_play = bundle_revenue.loc[bundle_revenue["Bundle Type"] == "Triple Play (Móvil+Fibra+TV)"].iloc[0]
            render_rev_ai_reco(
                "Valor de Bundles",
                f"Triple Play tiene ARPU de CLP {triple_play['ARPU K CLP']:.1f}K y churn de solo {triple_play['Churn %']:.1f}%.",
                "Promover agresivamente Triple Play en base existente de Fibra y Móvil.",
                "Incrementar penetración Triple Play a 80K subs y revenue +CLP 1.5M.",
            )

        st.markdown('<div class="rev-mini-title">ARPU Fibra por Mes</div>', unsafe_allow_html=True)
        with st.container(border=True):
            fb_arpu_line = alt.Chart(arpu_trend).mark_line(point=True, strokeWidth=3, color="#6366F1").encode(
                x=alt.X("Month:N", title=None),
                y=alt.Y("Fibra ARPU K:Q", title="ARPU (CLP K)", scale=alt.Scale(domain=[23.5, 25.5])),
                tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Fibra ARPU K:Q", format=".2f")],
            )
            st.altair_chart(style_rev_chart(fb_arpu_line, height=180), use_container_width=True)

    with rev_tab_map:
        st.markdown('<div class="rev-title">🗺️ Mapa de Revenue & Ventas por Ciudad</div>', unsafe_allow_html=True)

        map_filter_col1, map_filter_col2, map_filter_col3, map_filter_col4 = st.columns(4)

        with map_filter_col1:
            selected_regions = st.multiselect(
                "Región",
                options=sorted(geo_sales_data["Region"].unique()),
                default=[],
                placeholder="Todas las regiones",
                key="rev_map_region",
            )

        with map_filter_col2:
            selected_product = st.selectbox(
                "Producto",
                options=["Todos", "Móvil", "Fibra"],
                index=0,
                key="rev_map_product",
            )

        with map_filter_col3:
            selected_segment = st.multiselect(
                "Segmento",
                options=sorted(geo_sales_data["Segment"].unique()),
                default=[],
                placeholder="Todos los segmentos",
                key="rev_map_segment",
            )

        with map_filter_col4:
            selected_channel = st.multiselect(
                "Canal Principal",
                options=sorted(geo_sales_data["Channel Mix"].unique()),
                default=[],
                placeholder="Todos los canales",
                key="rev_map_channel",
            )

        map_filter_col5, map_filter_col6, map_filter_col7, map_filter_col8 = st.columns(4)

        with map_filter_col5:
            min_revenue = st.slider(
                "Revenue Mínimo (CLP M)",
                min_value=0.0,
                max_value=float(geo_sales_data["Total Revenue M"].max()),
                value=0.0,
                step=0.1,
                key="rev_map_min_rev",
            )

        with map_filter_col6:
            color_metric = st.selectbox(
                "Colorear por",
                options=["Total Revenue M", "Móvil Revenue M", "Fibra Revenue M", "Growth Móvil %", "Growth Fibra %", "Churn Móvil %", "Churn Fibra %", "5G Coverage %", "FTTH Coverage %", "ARPU Móvil K", "ARPU Fibra K"],
                index=0,
                key="rev_map_color",
            )

        with map_filter_col7:
            size_metric = st.selectbox(
                "Tamaño por",
                options=["Total Subscribers K", "Subscribers Móvil K", "Subscribers Fibra K", "Total Revenue M", "Tiendas WOM"],
                index=0,
                key="rev_map_size",
            )

        with map_filter_col8:
            has_store_filter = st.checkbox("Solo con Tienda WOM", value=False, key="rev_map_store")

        filtered_geo = geo_sales_data.copy()
        if selected_regions:
            filtered_geo = filtered_geo[filtered_geo["Region"].isin(selected_regions)]
        if selected_segment:
            filtered_geo = filtered_geo[filtered_geo["Segment"].isin(selected_segment)]
        if selected_channel:
            filtered_geo = filtered_geo[filtered_geo["Channel Mix"].isin(selected_channel)]
        if min_revenue > 0:
            filtered_geo = filtered_geo[filtered_geo["Total Revenue M"] >= min_revenue]
        if has_store_filter:
            filtered_geo = filtered_geo[filtered_geo["Tiendas WOM"] > 0]

        if selected_product == "Móvil":
            filtered_geo["Display Revenue M"] = filtered_geo["Móvil Revenue M"]
            filtered_geo["Display Subs K"] = filtered_geo["Subscribers Móvil K"]
        elif selected_product == "Fibra":
            filtered_geo["Display Revenue M"] = filtered_geo["Fibra Revenue M"]
            filtered_geo["Display Subs K"] = filtered_geo["Subscribers Fibra K"]
        else:
            filtered_geo["Display Revenue M"] = filtered_geo["Total Revenue M"]
            filtered_geo["Display Subs K"] = filtered_geo["Total Subscribers K"]

        total_filtered_rev = filtered_geo["Display Revenue M"].sum()
        total_filtered_subs = filtered_geo["Display Subs K"].sum()
        avg_filtered_growth = filtered_geo["Growth Móvil %"].mean() if selected_product != "Fibra" else filtered_geo["Growth Fibra %"].mean()
        num_cities = len(filtered_geo)

        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Ciudades</div><div class="v">{num_cities}</div><div class="d">En filtro actual</div></div>
                <div class="rev-kpi-card"><div class="k">Revenue Total</div><div class="v">CLP {total_filtered_rev:.1f}M</div><div class="d">Filtrado</div></div>
                <div class="rev-kpi-card"><div class="k">Suscriptores</div><div class="v">{total_filtered_subs:.0f}K</div><div class="d">Base filtrada</div></div>
                <div class="rev-kpi-card"><div class="k">Crecimiento Prom</div><div class="v">{avg_filtered_growth:.1f}%</div><div class="d">Ciudades filtradas</div></div>
            </div>
        """), unsafe_allow_html=True)

        if len(filtered_geo) > 0:
            color_val = filtered_geo[color_metric]
            color_min, color_max = color_val.min(), color_val.max()
            if "Churn" in color_metric:
                filtered_geo["r"] = ((color_val - color_min) / (color_max - color_min + 0.001) * 200 + 55).astype(int)
                filtered_geo["g"] = (200 - (color_val - color_min) / (color_max - color_min + 0.001) * 150).astype(int)
                filtered_geo["b"] = 80
            else:
                filtered_geo["r"] = (80 - (color_val - color_min) / (color_max - color_min + 0.001) * 40).astype(int)
                filtered_geo["g"] = ((color_val - color_min) / (color_max - color_min + 0.001) * 150 + 100).astype(int)
                filtered_geo["b"] = ((color_val - color_min) / (color_max - color_min + 0.001) * 100 + 130).astype(int)

            size_val = filtered_geo[size_metric]
            size_min, size_max = size_val.min(), size_val.max()
            filtered_geo["radius"] = ((size_val - size_min) / (size_max - size_min + 0.001) * 18000 + 3000).astype(int)

            center_lat = filtered_geo["lat"].mean()
            center_lon = filtered_geo["lon"].mean()
            zoom = 5 if len(selected_regions) == 0 else (7 if len(selected_regions) <= 2 else 6)
            if num_cities <= 10:
                zoom = 8

            map_data = filtered_geo.to_dict("records")

            map_col, table_col = st.columns([2, 1])

            with map_col:
                st.pydeck_chart(
                    pdk.Deck(
                        initial_view_state=pdk.ViewState(
                            latitude=center_lat,
                            longitude=center_lon,
                            zoom=zoom,
                            pitch=35,
                        ),
                        layers=[
                            pdk.Layer(
                                "ScatterplotLayer",
                                data=map_data,
                                get_position=["lon", "lat"],
                                get_radius="radius",
                                get_fill_color=["r", "g", "b", 180],
                                pickable=True,
                                auto_highlight=True,
                            ),
                        ],
                        tooltip={
                            "html": "<b>{City}</b><br/>Región: {Region}<br/>Revenue: CLP {Total Revenue M}M<br/>Subs Móvil: {Subscribers Móvil K}K<br/>Subs Fibra: {Subscribers Fibra K}K<br/>5G: {5G Coverage %}%<br/>FTTH: {FTTH Coverage %}%<br/>Tiendas: {Tiendas WOM}",
                            "style": {"backgroundColor": "#1E3A8A", "color": "white", "fontSize": "12px", "padding": "8px", "borderRadius": "6px"},
                        },
                        map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                    ),
                    use_container_width=True,
                    height=480,
                    key=f"rev_map_{len(map_data)}_{selected_product}_{'-'.join(selected_segment) if selected_segment else 'all'}",
                )

            with table_col:
                st.markdown('<div class="rev-mini-title">Top Ciudades (Filtradas)</div>', unsafe_allow_html=True)
                top_cities = filtered_geo.nlargest(10, "Display Revenue M")[["City", "Region", "Display Revenue M", "Display Subs K"]].copy()
                top_cities.columns = ["Ciudad", "Región", "Revenue M", "Subs K"]
                st.dataframe(top_cities, use_container_width=True, hide_index=True, height=420)

            st.markdown('<div class="rev-mini-title">Análisis por Región (Filtradas)</div>', unsafe_allow_html=True)
            region_agg = filtered_geo.groupby("Region").agg({
                "Display Revenue M": "sum",
                "Display Subs K": "sum",
                "Tiendas WOM": "sum",
                "5G Coverage %": "mean",
                "FTTH Coverage %": "mean",
                "Churn Móvil %": "mean",
                "Growth Móvil %": "mean",
            }).reset_index()
            region_agg.columns = ["Región", "Revenue M", "Subs K", "Tiendas", "5G %", "FTTH %", "Churn %", "Growth %"]
            region_agg = region_agg.sort_values("Revenue M", ascending=False)

            agg_col1, agg_col2 = st.columns(2)
            with agg_col1:
                with st.container(border=True):
                    region_bar = alt.Chart(region_agg).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22).encode(
                        x=alt.X("Revenue M:Q", title="Revenue (CLP M)"),
                        y=alt.Y("Región:N", sort="-x", title=None),
                        color=alt.Color("Growth %:Q", scale=alt.Scale(domain=[0, 15], range=["#F59E0B", "#10B981"]), legend=alt.Legend(title="Growth %")),
                        tooltip=["Región:N", alt.Tooltip("Revenue M:Q", format=".1f"), alt.Tooltip("Subs K:Q", format=",.0f"), alt.Tooltip("Growth %:Q", format=".1f")],
                    )
                    st.altair_chart(style_rev_chart(region_bar, height=220), use_container_width=True)

            with agg_col2:
                with st.container(border=True):
                    coverage_scatter = alt.Chart(region_agg).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.5).encode(
                        x=alt.X("5G %:Q", title="Cobertura 5G (%)"),
                        y=alt.Y("FTTH %:Q", title="Cobertura FTTH (%)"),
                        size=alt.Size("Revenue M:Q", scale=alt.Scale(range=[200, 1200]), legend=None),
                        color=alt.Color("Región:N", legend=alt.Legend(title=None)),
                        tooltip=["Región:N", alt.Tooltip("5G %:Q", format=".0f"), alt.Tooltip("FTTH %:Q", format=".0f"), alt.Tooltip("Revenue M:Q", format=".1f")],
                    )
                    st.altair_chart(style_rev_chart(coverage_scatter, height=220), use_container_width=True)

            if len(filtered_geo) > 0:
                best_city = filtered_geo.loc[filtered_geo["Display Revenue M"].idxmax()]
                low_coverage_cities = filtered_geo[filtered_geo["FTTH Coverage %"] < 50]
                render_rev_ai_reco(
                    "Análisis Geográfico",
                    f"{best_city['City']} lidera con CLP {best_city['Total Revenue M']:.1f}M. {len(low_coverage_cities)} ciudades tienen FTTH <50%.",
                    "Priorizar expansión de cobertura en ciudades con alto potencial y baja penetración.",
                    "Incrementar revenue +12% en ciudades de expansión.",
                )
        else:
            st.warning("No hay datos con los filtros seleccionados. Ajusta los filtros para ver resultados.")

    with rev_tab_channels:
        st.markdown('<div class="rev-title">Canales de Venta & Regiones</div>', unsafe_allow_html=True)

        best_channel = rev_channels.loc[rev_channels["Total M"].idxmax()]
        best_region = rev_regions.loc[rev_regions["Total M"].idxmax()]
        digital_pct = (rev_channels.loc[rev_channels["Channel"] == "WOM App / Web", "Total M"].iloc[0] / rev_channels["Total M"].sum() * 100)

        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Top Canal</div><div class="v">{best_channel['Channel']}</div><div class="d">CLP {best_channel['Total M']:.1f}M</div></div>
                <div class="rev-kpi-card"><div class="k">Top Región</div><div class="v">{best_region['Region']}</div><div class="d">CLP {best_region['Total M']:.1f}M</div></div>
                <div class="rev-kpi-card"><div class="k">Digital %</div><div class="v">{digital_pct:.1f}%</div><div class="d">App + Web</div></div>
                <div class="rev-kpi-card"><div class="k">CAC Promedio</div><div class="v">CLP {rev_channels['CAC K CLP'].mean():.1f}K</div><div class="d">Por adquisición</div></div>
            </div>
        """), unsafe_allow_html=True)

        ch_col1, ch_col2 = st.columns(2)
        with ch_col1:
            st.markdown('<div class="rev-mini-title">Revenue por Canal (Móvil vs Fibra)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                ch_long = rev_channels.melt(id_vars=["Channel"], value_vars=["Móvil M", "Fibra M"], var_name="Producto", value_name="Revenue M")
                ch_bar = alt.Chart(ch_long).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Channel:N", title=None),
                    y=alt.Y("Revenue M:Q", title="Revenue (CLP M)"),
                    color=alt.Color("Producto:N", scale=alt.Scale(domain=["Móvil M", "Fibra M"], range=["#10B981", "#6366F1"]), legend=alt.Legend(title=None)),
                    xOffset="Producto:N",
                    tooltip=["Channel:N", "Producto:N", alt.Tooltip("Revenue M:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(ch_bar, height=230), use_container_width=True)
                render_rev_ai_reco(
                    "Canales de Venta",
                    f"WOM App/Web genera CLP {best_channel['Total M']:.1f}M con menor CAC.",
                    "Incrementar inversión en app marketing y optimizar UX de conversión.",
                    "Aumentar digital a 40% del mix total.",
                )

        with ch_col2:
            st.markdown('<div class="rev-mini-title">Revenue por Región</div>', unsafe_allow_html=True)
            with st.container(border=True):
                reg_long = rev_regions.melt(id_vars=["Region"], value_vars=["Móvil M", "Fibra M"], var_name="Producto", value_name="Revenue M")
                reg_bar = alt.Chart(reg_long).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Region:N", title=None, sort="-y"),
                    y=alt.Y("Revenue M:Q", title="Revenue (CLP M)"),
                    color=alt.Color("Producto:N", scale=alt.Scale(domain=["Móvil M", "Fibra M"], range=["#10B981", "#6366F1"]), legend=alt.Legend(title=None)),
                    xOffset="Producto:N",
                    tooltip=["Region:N", "Producto:N", alt.Tooltip("Revenue M:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(reg_bar, height=230), use_container_width=True)
                metro_pct = (rev_regions.loc[rev_regions["Region"] == "Metropolitana", "Total M"].iloc[0] / rev_regions["Total M"].sum() * 100)
                render_rev_ai_reco(
                    "Concentración Regional",
                    f"Metropolitana representa {metro_pct:.0f}% del revenue total.",
                    "Expandir cobertura en Valparaíso y Biobío con promociones regionales.",
                    "Reducir dependencia de RM a <55% del revenue.",
                    level="warning",
                )

        st.markdown('<div class="rev-mini-title">Pipeline de Ventas (Móvil + Fibra)</div>', unsafe_allow_html=True)
        with st.container(border=True):
            pipe_long = sales_pipeline.melt(id_vars=["Stage"], value_vars=["Móvil K", "Fibra K"], var_name="Producto", value_name="Leads K")
            pipe_bar = alt.Chart(pipe_long).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=28).encode(
                x=alt.X("Stage:N", title=None, sort=["Lead", "Calificado", "Propuesta", "Negociación", "Cerrado"]),
                y=alt.Y("Leads K:Q", title="Leads (K)"),
                color=alt.Color("Producto:N", scale=alt.Scale(domain=["Móvil K", "Fibra K"], range=["#10B981", "#6366F1"]), legend=alt.Legend(title=None)),
                xOffset="Producto:N",
                tooltip=["Stage:N", "Producto:N", alt.Tooltip("Leads K:Q", format=".1f")],
            )
            st.altair_chart(style_rev_chart(pipe_bar, height=200), use_container_width=True)
            conversion = (sales_pipeline.iloc[-1]["Móvil K"] / sales_pipeline.iloc[0]["Móvil K"]) * 100
            render_rev_ai_reco(
                "Conversión Pipeline",
                f"Conversión Lead-to-Close de {conversion:.0f}% en móvil.",
                "Optimizar etapa Propuesta con ofertas personalizadas por segmento.",
                "Incrementar tasa de cierre +3pp.",
            )

    with rev_tab_risk:
        st.markdown('<div class="rev-title">Riesgo de Revenue & Cobranza</div>', unsafe_allow_html=True)

        over_30 = rev_aging.loc[rev_aging["Bucket"].isin(["31-60 días", "61-90 días", "90+ días"]), "Total M"].sum()
        delinquency_pct = (over_30 / rev_aging["Total M"].sum()) * 100

        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Cobranza</div><div class="v">{collection_rate:.1f}%</div><div class="d">Tasa de cobro</div></div>
                <div class="rev-kpi-card warn"><div class="k">Revenue at Risk</div><div class="v">CLP {at_risk_rev_m:.1f}M</div><div class="d">Exposición total</div></div>
                <div class="rev-kpi-card crit"><div class="k">Morosidad 30+</div><div class="v">{delinquency_pct:.1f}%</div><div class="d">Del revenue facturado</div></div>
                <div class="rev-kpi-card"><div class="k">Al día</div><div class="v">CLP {rev_aging.iloc[0]['Total M']:.1f}M</div><div class="d">Cartera sana</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="rev-mini-title">Aging de Cartera (Móvil vs Fibra)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                aging_long = rev_aging.melt(id_vars=["Bucket"], value_vars=["Móvil M", "Fibra M"], var_name="Producto", value_name="Amount M")
                aging_bar = alt.Chart(aging_long).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=18).encode(
                    y=alt.Y("Bucket:N", title=None, sort=["Al día", "1-30 días", "31-60 días", "61-90 días", "90+ días"]),
                    x=alt.X("Amount M:Q", title="Monto (CLP M)"),
                    color=alt.Color("Producto:N", scale=alt.Scale(domain=["Móvil M", "Fibra M"], range=["#10B981", "#6366F1"]), legend=alt.Legend(title=None)),
                    yOffset="Producto:N",
                    tooltip=["Bucket:N", "Producto:N", alt.Tooltip("Amount M:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(aging_bar, height=230), use_container_width=True)
                render_rev_ai_reco(
                    "Salud de Cartera",
                    f"Cartera 90+ días suma CLP {rev_aging.iloc[-1]['Total M']:.1f}M en riesgo de incobrabilidad.",
                    "Activar gestión de cobranza intensiva y ofertas de regularización.",
                    "Recuperar 40% de cartera morosa en próximos 60 días.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="rev-mini-title">Drivers de Riesgo de Revenue</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_bar = alt.Chart(rev_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20, color="#EF4444").encode(
                    x=alt.X("Exposure M:Q", title="Exposición (CLP M)"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Product:N", scale=alt.Scale(domain=["Móvil", "Fibra", "Ambos"], range=["#10B981", "#6366F1", "#F59E0B"]), legend=alt.Legend(title="Producto")),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure M:Q", format=".1f"), alt.Tooltip("Likelihood:Q", format=".1f"), "Product:N"],
                )
                st.altair_chart(style_rev_chart(risk_bar, height=230), use_container_width=True)
                top_risk = rev_risk.loc[rev_risk["Exposure M"].idxmax()]
                render_rev_ai_reco(
                    "Principal Riesgo",
                    f"Portabilidad Móvil genera CLP {top_risk['Exposure M']:.1f}M en riesgo.",
                    "Lanzar programa de retención proactiva pre-portabilidad.",
                    "Reducir fuga por portabilidad 25%.",
                    level="critical",
                )

        st.markdown('<div class="rev-mini-title">Impacto Competitivo en Revenue</div>', unsafe_allow_html=True)
        with st.container(border=True):
            comp_total = competitor_impact.copy()
            comp_total["Total Lost K"] = comp_total["Lost Móvil K"] + comp_total["Lost Fibra K"]
            comp_bar = alt.Chart(comp_total).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=32).encode(
                x=alt.X("Competitor:N", title=None, sort="-y"),
                y=alt.Y("Revenue Impact M:Q", title="Impacto Revenue (CLP M)"),
                color=alt.Color("Revenue Impact M:Q", scale=alt.Scale(domain=[0, 2], range=["#FCD34D", "#EF4444"]), legend=None),
                tooltip=["Competitor:N", alt.Tooltip("Lost Móvil K:Q", format=","), alt.Tooltip("Lost Fibra K:Q", format=","), alt.Tooltip("Revenue Impact M:Q", format=".1f")],
            )
            st.altair_chart(style_rev_chart(comp_bar, height=200), use_container_width=True)
            total_impact = competitor_impact["Revenue Impact M"].sum()
            render_rev_ai_reco(
                "Fuga Competitiva Total",
                f"Competidores capturan CLP {total_impact:.1f}M mensual en revenue WOM.",
                "Desarrollar ofertas win-back y campañas anti-competencia por segmento.",
                "Recuperar CLP 1.2M de revenue perdido en próximo trimestre.",
                level="warning",
            )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Alerta: CLP {at_risk_rev_m:.1f}M revenue en riesgo</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Principal driver: {rev_risk.loc[rev_risk['Exposure M'].idxmax(), 'Risk Driver']} · priorizar mitigación en próximo ciclo</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "Network Status":
    import pandas as pd
    import altair as alt
    import pydeck as pdk
    import math
    import random
    import time

    NET_CHART_THEME = {
        "bg": "#F8FAFF",
        "title": "#1E3A8A",
        "axis": "#334155",
        "grid": "#E2E8F0",
        "font": "Inter",
    }

    def style_net_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 10, "right": 10, "top": 8, "bottom": 4})
            .configure(background=NET_CHART_THEME["bg"])
            .configure_view(stroke=None, cornerRadius=10)
            .configure_title(color=NET_CHART_THEME["title"], fontSize=13, font=NET_CHART_THEME["font"], anchor="start")
            .configure_axis(
                labelColor=NET_CHART_THEME["axis"],
                titleColor=NET_CHART_THEME["axis"],
                gridColor=NET_CHART_THEME["grid"],
                labelFont=NET_CHART_THEME["font"],
                titleFont=NET_CHART_THEME["font"],
            )
            .configure_legend(
                labelColor=NET_CHART_THEME["axis"],
                titleColor=NET_CHART_THEME["axis"],
                labelFont=NET_CHART_THEME["font"],
                titleFont=NET_CHART_THEME["font"],
            )
        )

    def render_net_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        level_class = "crit" if level == "critical" else "warn" if level == "warning" else ""
        icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "🤖"
        st.markdown(dedent(f"""
            <div class="net-ai-card {level_class}">
                <div class="h">{icon} {headline}</div>
                <div class="b"><strong>Insight:</strong> {insight}</div>
                <div class="b"><strong>Action:</strong> {action}</div>
                <div class="b"><strong>Expected Impact:</strong> {impact}</div>
            </div>
        """), unsafe_allow_html=True)

    st.markdown(dedent("""
        <style>
            @keyframes net-fade-up {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes net-pulse-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.12); }
                50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.03); }
            }
            .net-title {
                font-size: 1.08rem;
                font-weight: 800;
                color: #1E3A8A;
                letter-spacing: 0.01em;
                margin: 0.3rem 0 0.6rem 0;
                animation: net-fade-up 0.45s ease-out both;
            }
            .net-mini-title {
                font-size: 0.92rem;
                font-weight: 700;
                color: #334155;
                margin: 0.12rem 0 0.5rem 0;
                animation: net-fade-up 0.45s ease-out both;
            }
            .net-pulse {
                border-radius: 12px;
                border: 1px solid #DBEAFE;
                background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
                padding: 0.8rem 0.95rem;
                margin-bottom: 0.65rem;
                animation: net-fade-up 0.45s ease-out both, net-pulse-glow 2.8s ease-in-out infinite;
            }
            .net-pulse-grid, .net-kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.48rem;
            }
            .net-pulse-card, .net-kpi-card {
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #E2E8F0;
                padding: 0.52rem 0.62rem;
            }
            .net-pulse-card .k, .net-kpi-card .k {
                font-size: 0.69rem;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                font-weight: 700;
            }
            .net-pulse-card .v, .net-kpi-card .v {
                font-size: 1.04rem;
                color: #0F172A;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.08rem;
            }
            .net-pulse-card .d, .net-kpi-card .d {
                font-size: 0.74rem;
                color: #475569;
                margin-top: 0.12rem;
            }
            .net-kpi-card.warn { border-left: 4px solid #F59E0B; }
            .net-kpi-card.crit { border-left: 4px solid #EF4444; }
            .net-ai-card {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
                background: #EFF6FF;
                padding: 0.62rem 0.72rem;
                margin-top: 0.46rem;
                animation: net-fade-up 0.42s ease-out both;
            }
            .net-ai-card.warn { border-left-color: #F59E0B; background: #FFFBEB; }
            .net-ai-card.crit { border-left-color: #EF4444; background: #FEF2F2; }
            .net-ai-card .h {
                font-size: 0.83rem;
                font-weight: 800;
                color: #1E293B;
                margin-bottom: 0.28rem;
            }
            .net-ai-card .b {
                font-size: 0.78rem;
                color: #334155;
                line-height: 1.42;
            }
            @media (max-width: 1200px) {
                .net-pulse-grid, .net-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
        </style>
    """), unsafe_allow_html=True)

    net_hourly = pd.DataFrame({
        "Hour": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
        "Latency ms": [19, 21, 23, 27, 25, 22],
        "Utilization %": [54, 58, 69, 82, 76, 63],
        "Packet Loss %": [0.18, 0.21, 0.27, 0.36, 0.31, 0.24],
        "Availability %": [99.96, 99.95, 99.93, 99.88, 99.90, 99.94],
        "Incidents": [1, 1, 2, 4, 3, 2],
    })
    net_regions = pd.DataFrame({
        "Region": ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "O'Higgins", "Antofagasta"],
        "Availability %": [99.94, 99.91, 99.90, 99.86, 99.88, 99.84],
        "NPS": [58, 55, 53, 50, 51, 48],
        "Active OLTs": [124, 68, 54, 38, 32, 28],
        "MTTR Min": [42, 46, 49, 54, 51, 58],
        "Tiendas WOM": [45, 18, 14, 12, 8, 6],
        "5G Sites": [186, 72, 48, 34, 28, 22],
        "FTTH Homes Passed K": [1420, 580, 440, 320, 260, 180],
    })
    net_incident_trend = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Incidents": [62, 58, 55, 51, 49, 46],
        "MTTR Min": [56, 54, 52, 50, 48, 46],
    })
    net_queue = pd.DataFrame({
        "Queue": ["Core WOM", "Acceso FTTH", "Field Ops", "Backbone 5G", "CPE Hogar"],
        "Open Tickets": [22, 34, 31, 17, 28],
        "SLA Breach %": [7.5, 10.4, 9.8, 5.1, 8.9],
        "Avg Age Hr": [9.2, 12.1, 10.8, 7.4, 9.9],
    })
    net_risk = pd.DataFrame({
        "Risk Driver": ["Saturación 5G", "Cortes Fibra FTTH", "Inestabilidad Energía", "Delay Proveedores", "Congestión HFC"],
        "Exposure Hr": [94, 86, 71, 49, 44],
        "Likelihood": [3.8, 3.6, 3.1, 2.9, 2.7],
    })
    net_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Availability %": [99.80, 99.91, 99.96],
        "Avoided Churn K": [1.8, 2.4, 3.1],
        "Recovery Cost K": [102, 88, 76],
        "Probability": ["25%", "50%", "25%"],
    })
    net_map_nodes = pd.DataFrame({
        "Node": ["WOM Santiago Centro", "WOM Providencia", "WOM Maipú", "WOM Valparaíso", "WOM Concepción", "WOM Temuco", "WOM Antofagasta", "WOM Rancagua"],
        "lat": [-33.45, -33.43, -33.51, -33.05, -36.82, -38.74, -23.65, -34.17],
        "lon": [-70.65, -70.61, -70.76, -71.62, -73.05, -72.60, -70.40, -70.74],
        "Availability %": [99.94, 99.92, 99.90, 99.86, 99.88, 99.84, 99.87, 99.89],
        "Utilization %": [72, 76, 74, 68, 66, 71, 67, 64],
        "Open Incidents": [5, 7, 6, 9, 8, 10, 7, 6],
        "Status": ["Healthy", "Watch", "Watch", "At Risk", "Watch", "At Risk", "Watch", "Healthy"],
        "5G Coverage %": [92, 94, 88, 78, 72, 65, 70, 75],
        "FTTH Homes K": [320, 280, 240, 160, 140, 95, 85, 110],
    })
    net_incident_points = pd.DataFrame({
        "lat": [-33.44, -33.46, -33.40, -33.51, -33.04, -33.06, -36.81, -36.83, -38.73, -38.75, -23.64, -34.16],
        "lon": [-70.64, -70.66, -70.63, -70.67, -71.61, -71.63, -73.04, -73.06, -72.59, -72.61, -70.39, -70.73],
        "weight": [4, 3, 3, 2, 5, 4, 3, 2, 5, 4, 3, 2],
        "Type": ["Corte Fibra", "Falla Energía", "Congestión 5G", "Config", "Corte Fibra", "Falla Energía", "Congestión", "Config", "Corte Fibra", "Falla Energía", "Congestión", "Config"],
    })
    # Expand sparse map points into realistic synthetic clusters for richer visuals.
    rng = random.Random(17)
    net_node_density_records = []
    node_offsets = [(0.00, 0.00), (0.06, 0.02), (-0.05, 0.03), (0.03, -0.05), (-0.04, -0.04), (0.07, -0.01), (-0.07, 0.00)]
    for _, row in net_map_nodes.iterrows():
        cluster_size = min(13, 4 + int(row["Open Incidents"]))
        base_color = {
            "Healthy": (16, 185, 129),
            "Watch": (245, 158, 11),
            "At Risk": (239, 68, 68),
        }[row["Status"]]
        for i in range(cluster_size):
            off_lon, off_lat = node_offsets[i % len(node_offsets)]
            scale = 0.35 + 0.08 * (i // len(node_offsets))
            net_node_density_records.append({
                "Node": row["Node"],
                "Status": row["Status"],
                "lat": row["lat"] + off_lat * scale + rng.uniform(-0.004, 0.004),
                "lon": row["lon"] + off_lon * scale + rng.uniform(-0.004, 0.004),
                "r": base_color[0],
                "g": base_color[1],
                "b": base_color[2],
                "radius": 2000 + (220 * i),
            })
    net_node_density = pd.DataFrame(net_node_density_records)

    net_incident_density_records = []
    incident_offsets = [(0.00, 0.00), (0.04, 0.02), (-0.04, 0.02), (0.03, -0.03), (-0.03, -0.03), (0.06, -0.01), (-0.06, -0.01), (0.00, 0.05)]
    for _, row in net_incident_points.iterrows():
        cluster_size = int(row["weight"] * 3)
        for i in range(cluster_size):
            off_lon, off_lat = incident_offsets[i % len(incident_offsets)]
            scale = 0.28 + 0.08 * (i // len(incident_offsets))
            net_incident_density_records.append({
                "Type": row["Type"],
                "lat": row["lat"] + off_lat * scale + rng.uniform(-0.003, 0.003),
                "lon": row["lon"] + off_lon * scale + rng.uniform(-0.003, 0.003),
                "weight": max(1.0, row["weight"] - 0.15 * (i % 3)),
            })
    net_incident_density = pd.DataFrame(net_incident_density_records)
    net_access_points_records = []
    for _, row in net_map_nodes.iterrows():
        site_count = 24 + int(row["Utilization %"] / 4)
        for _ in range(site_count):
            theta = rng.uniform(0, 2 * math.pi)
            radius = rng.uniform(0.008, 0.11)
            lat = row["lat"] + radius * math.sin(theta)
            lon = row["lon"] + radius * math.cos(theta) * 0.92
            traffic = max(22.0, min(95.0, row["Utilization %"] + rng.uniform(-20, 16)))
            net_access_points_records.append({
                "Node": row["Node"],
                "lat": lat,
                "lon": lon,
                "Traffic": traffic,
            })
    net_access_points = pd.DataFrame(net_access_points_records)
    net_access_points["r"] = net_access_points["Traffic"].apply(lambda v: 239 if v >= 82 else 245 if v >= 66 else 37)
    net_access_points["g"] = net_access_points["Traffic"].apply(lambda v: 68 if v >= 82 else 158 if v >= 66 else 99)
    net_access_points["b"] = net_access_points["Traffic"].apply(lambda v: 68 if v >= 82 else 11 if v >= 66 else 235)
    net_access_points["radius"] = net_access_points["Traffic"].apply(lambda v: 500 if v >= 82 else 420 if v >= 66 else 360)
    net_access_points["Tier"] = net_access_points["Traffic"].apply(lambda v: "Critical" if v >= 82 else "Watch" if v >= 66 else "Stable")
    node_sites = net_access_points.groupby("Node", as_index=False).size().rename(columns={"size": "Access Sites"})
    net_node_labels = net_map_nodes.merge(node_sites, on="Node", how="left")
    net_node_labels["Label"] = net_node_labels["Node"] + " • " + net_node_labels["Access Sites"].astype(int).astype(str) + " sites"
    net_fiber_paths = pd.DataFrame({
        "from_lon": [-70.65, -70.65, -70.65, -70.65, -73.05],
        "from_lat": [-33.45, -33.45, -33.45, -33.45, -36.82],
        "to_lon": [-73.05, -71.62, -72.60, -70.74, -70.40],
        "to_lat": [-36.82, -33.05, -38.74, -34.17, -23.65],
        "Cuts": [7, 9, 8, 6, 5],
    })
    net_backbone_flows = pd.DataFrame({
        "source_lon": [-70.65, -70.65, -70.65, -70.65, -70.65],
        "source_lat": [-33.45, -33.45, -33.45, -33.45, -33.45],
        "target_lon": [-73.05, -71.62, -72.60, -70.40, -70.74],
        "target_lat": [-36.82, -33.05, -38.74, -23.65, -34.17],
        "Utilization %": [77, 71, 83, 68, 64],
    })
    net_sla_geo = pd.DataFrame({
        "City": ["Metropolitana", "Biobío", "Valparaíso", "Araucanía", "Antofagasta", "O'Higgins"],
        "lat": [-33.45, -36.82, -33.05, -38.74, -23.65, -34.17],
        "lon": [-70.65, -73.05, -71.62, -72.60, -70.40, -70.74],
        "SLA Risk": [28, 38, 42, 48, 34, 32],
    })
    net_opportunity_geo = pd.DataFrame({
        "Zone": ["Metropolitana Este", "Metropolitana Norte", "Metropolitana Sur", "Biobío Sur", "Araucanía Norte", "Valparaíso Norte", "Antofagasta Centro", "O'Higgins Valle"],
        "lat": [-33.40, -33.38, -33.52, -36.85, -38.76, -33.02, -23.68, -34.14],
        "lon": [-70.58, -70.62, -70.68, -73.08, -72.62, -71.58, -70.42, -70.70],
        "Demand Index": [88, 76, 72, 70, 78, 68, 66, 64],
        "Coverage Gap %": [16, 14, 12, 18, 20, 13, 11, 10],
        "ARR Risk M": [1.60, 1.15, 0.98, 0.92, 1.32, 0.84, 0.72, 0.62],
        "Capex M": [1.20, 0.92, 0.82, 0.78, 1.12, 0.74, 0.66, 0.58],
        "Payback Mo": [14, 12, 11, 14, 15, 11, 10, 9],
        "Priority Score": [92, 84, 80, 82, 88, 76, 74, 72],
        "FTTH Potential K": [48, 32, 28, 24, 36, 22, 18, 16],
        "5G Sites Planned": [24, 16, 14, 12, 18, 10, 8, 8],
    })
    net_major_cities_geo = pd.DataFrame({
        "City": [
            "Santiago Centro", "Providencia", "Las Condes", "Maipú", "Valparaíso", "Viña del Mar", "Concepción", "Temuco",
            "Antofagasta", "Rancagua", "Talca", "Chillán", "Puerto Montt", "Iquique", "La Serena", "Osorno",
            "Copiapó", "Punta Arenas", "Curicó", "Los Ángeles", "Talcahuano", "Arica", "Quilpué", "San Bernardo",
        ],
        "lat": [
            -33.45, -33.43, -33.42, -33.51, -33.05, -33.02, -36.82, -38.74,
            -23.65, -34.17, -35.43, -36.61, -41.47, -20.21, -29.90, -40.57,
            -27.37, -53.16, -34.98, -37.47, -36.72, -18.48, -33.05, -33.60,
        ],
        "lon": [
            -70.65, -70.61, -70.59, -70.76, -71.62, -71.55, -73.05, -72.60,
            -70.40, -70.74, -71.67, -72.10, -72.94, -70.15, -71.25, -73.13,
            -70.33, -70.91, -71.24, -72.35, -73.12, -70.32, -71.44, -70.70,
        ],
        "City Tier": [
            "Core Hub", "Core Hub", "Core Hub", "Core Hub", "Core Hub", "Core Hub", "Core Hub", "Growth Node",
            "Growth Node", "Growth Node", "Growth Node", "Growth Node", "Growth Node", "Growth Node", "Growth Node", "Emerging Node",
            "Emerging Node", "Emerging Node", "Emerging Node", "Emerging Node", "Growth Node", "Growth Node", "Emerging Node", "Emerging Node",
        ],
        "Investment Signal": [98, 95, 94, 91, 92, 90, 89, 86, 85, 84, 82, 80, 81, 83, 79, 77, 75, 73, 76, 74, 84, 82, 78, 77],
        "5G Priority": ["Alta", "Alta", "Alta", "Alta", "Alta", "Alta", "Alta", "Media", "Media", "Media", "Media", "Media", "Media", "Media", "Media", "Baja", "Baja", "Baja", "Baja", "Baja", "Media", "Media", "Baja", "Baja"],
        "FTTH Status": ["Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "Activo", "En Expansión", "Activo", "Activo", "En Expansión", "Planificado", "Planificado", "Activo", "En Expansión", "Activo", "Activo", "Activo", "Activo"],
    })
    net_major_cities_geo["r"] = net_major_cities_geo["City Tier"].apply(lambda v: 37 if v == "Core Hub" else 16 if v == "Growth Node" else 245)
    net_major_cities_geo["g"] = net_major_cities_geo["City Tier"].apply(lambda v: 99 if v == "Core Hub" else 185 if v == "Growth Node" else 158)
    net_major_cities_geo["b"] = net_major_cities_geo["City Tier"].apply(lambda v: 235 if v == "Core Hub" else 129 if v == "Growth Node" else 11)
    net_major_cities_geo["radius"] = net_major_cities_geo["City Tier"].apply(lambda v: 13500 if v == "Core Hub" else 11000 if v == "Growth Node" else 9500)
    net_infra_assets = pd.DataFrame({
        "Domain": ["Core Network", "5G Radio", "FTTH OLT", "Backbone Fibra", "CPE Hogar/Móvil"],
        "Sites": [22, 486, 324, 1280, 720],
        "Capacity Gbps": [680, 920, 1100, 780, 540],
        "Utilization %": [68, 76, 79, 66, 61],
        "Redundancy %": [96, 88, 92, 81, 76],
        "Health Score": [91, 85, 87, 79, 82],
    })
    net_maintenance = pd.DataFrame({
        "Asset Type": ["Core Routers WOM", "5G eNodeB", "OLT FTTH", "Nodos Fibra", "Unidades Energía"],
        "Open Workorders": [16, 32, 38, 45, 29],
        "Critical %": [14, 19, 20, 23, 17],
        "Avg Delay Hr": [6.2, 7.8, 8.6, 9.1, 7.4],
    })
    net_upgrade_program = pd.DataFrame({
        "Initiative": ["WOM 5G SA Rollout Fase 2", "WOM FTTH Expansion Norte", "WOM Core Upgrade Santiago", "WOM Backbone Sur Redundancia", "WOM Power Backup Crítico"],
        "Domain": ["5G Radio", "FTTH Access", "Core Network", "Backbone", "Infrastructure"],
        "Capex M": [2.4, 1.9, 1.6, 1.5, 1.1],
        "Impact Score": [94, 92, 89, 84, 78],
        "Delivery Risk": [2.8, 2.4, 2.1, 2.6, 2.2],
        "Quarter": ["Q1", "Q2", "Q1", "Q3", "Q1"],
    })
    net_spof = pd.DataFrame({
        "Region": ["Metropolitana Norte", "Metropolitana Sur", "Valparaíso", "Biobío", "Araucanía"],
        "SPOF Count": [4, 3, 5, 4, 6],
        "Subscribers K": [62, 54, 38, 34, 29],
        "Criticality": [3.2, 2.9, 3.5, 3.1, 3.8],
    })
    net_resilience_sites = pd.DataFrame({
        "Region": ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "O'Higgins", "Antofagasta"],
        "Backup Autonomy Hr": [8.8, 7.2, 6.8, 5.8, 6.5, 7.1],
        "Power Events / Mo": [2.3, 3.2, 3.4, 3.8, 3.1, 2.6],
        "Critical Sites": [28, 14, 12, 10, 9, 8],
    })
    net_enterprise_geo = pd.DataFrame({
        "City": ["Santiago", "Providencia", "Concepción", "Temuco", "Valparaíso", "Rancagua", "Antofagasta", "Talca"],
        "lat": [-33.45, -33.43, -36.82, -38.74, -33.05, -34.17, -23.65, -35.01],
        "lon": [-70.65, -70.61, -73.05, -72.60, -71.62, -70.74, -70.40, -71.13],
        "Accounts": [210, 145, 82, 68, 62, 52, 48, 38],
        "Priority": ["Tier 1", "Tier 1", "Tier 2", "Tier 2", "Tier 2", "Tier 3", "Tier 3", "Tier 3"],
        "Product Mix": ["Móvil+Fibra", "Móvil+Fibra", "Móvil", "Móvil", "Móvil+Fibra", "Móvil", "Móvil", "Móvil"],
    })
    net_enterprise_geo["radius"] = (net_enterprise_geo["Accounts"] * 30).clip(lower=1200, upper=7200)
    net_weather_risk_geo = pd.DataFrame({
        "Zone": ["Metropolitana Norte", "Metropolitana Sur", "Biobío Costa", "Araucanía Costa", "Valparaíso Valle", "O'Higgins Sierra"],
        "lat": [-33.38, -33.52, -36.85, -38.76, -33.04, -34.18],
        "lon": [-70.62, -70.68, -73.08, -72.62, -71.60, -70.76],
        "Weather Risk": [68, 64, 78, 84, 62, 56],
    })
    net_weather_risk_geo["radius"] = net_weather_risk_geo["Weather Risk"] * 150
    net_build_corridors = pd.DataFrame({
        "from_lon": [-70.65, -70.65, -70.65, -70.65],
        "from_lat": [-33.45, -33.45, -33.45, -33.45],
        "to_lon": [-73.05, -72.60, -71.62, -70.74],
        "to_lat": [-36.82, -38.74, -33.05, -34.17],
        "Phase": ["Wave 1", "Wave 1", "Wave 2", "Wave 2"],
        "Capex M": [0.88, 1.04, 0.96, 0.74],
    })
    net_build_corridors["width"] = net_build_corridors["Phase"].map({"Wave 1": 4.8, "Wave 2": 3.6})
    net_service_impact = pd.DataFrame({
        "Incident Type": ["Corte Fibra", "Falla Energía", "Congestión 5G", "Config Drift", "Falla Proveedor"],
        "Subs Impacted K": [3.8, 2.9, 2.4, 1.4, 1.1],
        "ARR at Risk M": [0.42, 0.34, 0.28, 0.18, 0.13],
        "Enterprise Accounts": [14, 11, 8, 5, 4],
        "Avg Restore Hr": [3.6, 2.9, 2.3, 1.8, 2.2],
        "Product Impact": ["FTTH+Móvil", "Todos", "Móvil", "FTTH", "Móvil"],
    })
    net_sla_command = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "SLA Actual %": [98.9, 99.1, 98.8, 99.0, 98.7, 99.2, 99.0],
        "SLA Forecast %": [98.9, 99.1, 98.8, 99.0, 98.7, 98.9, 98.8],
        "SLA Target %": [99.2, 99.2, 99.2, 99.2, 99.2, 99.2, 99.2],
    })
    net_change_monitor = pd.DataFrame({
        "Week": ["W1", "W2", "W3", "W4", "W5", "W6"],
        "Planned Changes": [26, 31, 28, 35, 33, 29],
        "Failed Changes": [2, 3, 2, 4, 3, 2],
        "Incidents": [11, 13, 12, 16, 14, 12],
    })
    net_capacity_forecast = pd.DataFrame({
        "Horizon": ["30d", "60d", "90d"] * 4,
        "Corridor": ["North Backbone"] * 3 + ["South Backbone"] * 3 + ["Metro Core"] * 3 + ["Regional Edge"] * 3,
        "Projected Util %": [74, 79, 84, 69, 73, 77, 81, 86, 91, 66, 70, 74],
    })
    net_critical_sites = pd.DataFrame({
        "Site": ["WOM-CORE-01", "WOM-5G-STG-04", "WOM-OLT-VLP-02", "WOM-5G-CNC-05", "WOM-OLT-STG-09", "WOM-5G-RCG-01", "WOM-OLT-ANT-03", "WOM-CORE-07", "WOM-5G-TMC-02", "WOM-OLT-BIO-06"],
        "Region": ["Metropolitana", "Metropolitana", "Valparaíso", "Biobío", "Metropolitana", "O'Higgins", "Antofagasta", "Metropolitana", "Araucanía", "Biobío"],
        "Criticality": [94, 92, 90, 88, 87, 85, 84, 83, 82, 81],
        "Subscribers Impact K": [46, 38, 29, 27, 25, 22, 20, 19, 18, 17],
        "MTTR Min": [62, 68, 58, 56, 54, 52, 50, 49, 48, 47],
        "Owner": ["Core Ops", "Field Ops", "Transport", "Access", "Access", "Transport", "Access", "Transport", "Field Ops", "Access"],
    })
    net_mitigation_tracker = pd.DataFrame({
        "Initiative": ["Redundancia Backbone Sur", "Hardening Energía Norte", "Diversificación Rutas Fibra", "Config Guardrails 5G", "Automatización Cola Prioridad"],
        "Owner": ["Backbone WOM", "Field Ops", "Core Network", "NOC WOM", "Service Ops"],
        "ETA": ["Q2", "Q2", "Q3", "Q1", "Q1"],
        "Progress %": [58, 46, 34, 72, 64],
        "Risk Reduced %": [26, 18, 21, 14, 12],
        "Status": ["On Track", "Watch", "Watch", "On Track", "On Track"],
    })
    net_customer_link = pd.DataFrame({
        "Region": ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "O'Higgins", "Antofagasta"],
        "Latency ms": [18.5, 22.4, 24.1, 26.2, 23.8, 21.2],
        "Packet Loss %": [0.17, 0.26, 0.28, 0.34, 0.27, 0.22],
        "NPS": [58, 53, 51, 48, 52, 50],
        "Churn %": [1.8, 2.4, 2.6, 3.2, 2.5, 2.2],
    })
    net_outage_timeline = pd.DataFrame({
        "Hour": list(range(24)),
        "Incidents": [1, 1, 1, 1, 1, 2, 2, 3, 4, 4, 5, 6, 5, 5, 4, 4, 5, 6, 5, 4, 3, 2, 2, 1],
        "Subs Impacted K": [1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 7, 7, 6, 6, 7, 8, 7, 6, 4, 3, 2, 1],
    })
    net_resilience_score = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Core Score": [82, 84, 85, 86, 87, 88],
        "Access Score": [74, 75, 76, 78, 79, 80],
        "Field Score": [71, 72, 73, 74, 75, 77],
    })

    active_olts = int(net_regions["Active OLTs"].sum())
    avg_availability = net_hourly["Availability %"].mean()
    avg_latency = net_hourly["Latency ms"].mean()
    open_tickets = int(net_queue["Open Tickets"].sum())
    p95_utilization = net_hourly["Utilization %"].quantile(0.95)
    mttr_current = net_incident_trend.iloc[-1]["MTTR Min"]
    packet_loss_avg = net_hourly["Packet Loss %"].mean()
    breach_rate = net_queue["SLA Breach %"].mean()
    highest_risk = net_risk.loc[net_risk["Exposure Hr"].idxmax()]
    weakest_region = net_regions.loc[net_regions["Availability %"].idxmin()]
    infra_total_capacity = net_infra_assets["Capacity Gbps"].sum()
    infra_weighted_util = (net_infra_assets["Capacity Gbps"] * net_infra_assets["Utilization %"]).sum() / infra_total_capacity
    infra_health_avg = net_infra_assets["Health Score"].mean()
    infra_redundancy_avg = net_infra_assets["Redundancy %"].mean()

    st.markdown('<div class="net-title">WOM Network Pulse - Estado Red Móvil & Fibra</div>', unsafe_allow_html=True)
    st.markdown(dedent(f"""
        <div class="net-pulse">
            <div class="net-pulse-grid">
                <div class="net-pulse-card"><div class="k">Red Disponibilidad</div><div class="v">{avg_availability:.2f}%</div><div class="d">Uptime 24h (Móvil + Fibra)</div></div>
                <div class="net-pulse-card"><div class="k">OLTs FTTH Activos</div><div class="v">{active_olts:,}</div><div class="d">Nodos acceso fibra</div></div>
                <div class="net-pulse-card"><div class="k">Latencia Promedio</div><div class="v">{avg_latency:.1f} ms</div><div class="d">Core-to-edge performance</div></div>
                <div class="net-pulse-card"><div class="k">Tickets Abiertos</div><div class="v">{open_tickets}</div><div class="d">Carga operaciones</div></div>
                <div class="net-pulse-card"><div class="k">P95 Utilización</div><div class="v">{p95_utilization:.1f}%</div><div class="d">Presión capacidad</div></div>
                <div class="net-pulse-card"><div class="k">MTTR Actual</div><div class="v">{mttr_current:.0f} min</div><div class="d">Velocidad recuperación</div></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    net_tab_overview, net_tab_map, net_tab_ops, net_tab_impact, net_tab_exec, net_tab_risk = st.tabs([
        "📈 Vista General Red",
        "🗺️ Mapa Cobertura WOM",
        "🧭 Operaciones Red",
        "💼 Impacto Servicio",
        "🧩 Ejecución & Playbooks",
        "⚠️ Riesgo & Estrategia",
    ])

    with net_tab_overview:
        st.markdown('<div class="net-title">Rendimiento Red WOM</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Disponibilidad</div><div class="v">{avg_availability:.2f}%</div><div class="d">Baseline confiabilidad</div></div>
                <div class="net-kpi-card {'warn' if avg_latency > 24 else ''}"><div class="k">Latencia Promedio</div><div class="v">{avg_latency:.1f} ms</div><div class="d">Proxy experiencia cliente</div></div>
                <div class="net-kpi-card {'warn' if packet_loss_avg > 0.28 else ''}"><div class="k">Pérdida Paquetes</div><div class="v">{packet_loss_avg:.2f}%</div><div class="d">Consistencia calidad</div></div>
                <div class="net-kpi-card {'crit' if weakest_region['Availability %'] < 99.86 else 'warn'}"><div class="k">Región Menor Uptime</div><div class="v">{weakest_region['Region']}</div><div class="d">{weakest_region['Availability %']:.2f}% disponibilidad</div></div>
            </div>
        """), unsafe_allow_html=True)

        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="net-mini-title">Latencia y Utilización por Hora</div>', unsafe_allow_html=True)
            with st.container(border=True):
                lat_line = alt.Chart(net_hourly).mark_line(point=True, strokeWidth=3, color="#2563EB").encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Latency ms:Q", title="Latency (ms)"),
                    tooltip=["Hour:N", alt.Tooltip("Latency ms:Q", format=".1f"), alt.Tooltip("Utilization %:Q", format=".1f"), alt.Tooltip("Incidents:Q", format=".0f")],
                )
                util_line = alt.Chart(net_hourly).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Utilization %:Q", title="Utilization (%)"),
                )
                st.altair_chart(style_net_chart(alt.layer(lat_line, util_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_net_ai_reco(
                    "Load Pattern",
                    f"Peak utilization reaches {p95_utilization:.1f}% around demand-heavy windows, while latency expands in the same periods.",
                    "Apply dynamic traffic steering and pre-scale transport capacity before the midday peak.",
                    "Reduce congestion events and stabilize customer experience in peak windows.",
                )

        with ov_col2:
            st.markdown('<div class="net-mini-title">Disponibilidad Regional vs NPS</div>', unsafe_allow_html=True)
            with st.container(border=True):
                regional_scatter = alt.Chart(net_regions).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.3).encode(
                    x=alt.X("Availability %:Q", title="Availability (%)"),
                    y=alt.Y("NPS:Q", title="NPS"),
                    size=alt.Size("Active OLTs:Q", scale=alt.Scale(range=[260, 1400]), legend=None),
                    color=alt.Color("MTTR Min:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="MTTR (min)")),
                    tooltip=["Region:N", alt.Tooltip("Availability %:Q", format=".2f"), alt.Tooltip("NPS:Q", format=".0f"), alt.Tooltip("MTTR Min:Q", format=".0f"), alt.Tooltip("Active OLTs:Q", format=",")],
                )
                region_label = alt.Chart(net_regions).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Availability %:Q", y="NPS:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(regional_scatter + region_label, height=235), use_container_width=True)
                render_net_ai_reco(
                    "Regional Reliability",
                    f"{weakest_region['Region']} shows the weakest uptime at {weakest_region['Availability %']:.2f}% with visible NPS drag.",
                    f"Prioritize preventive maintenance and redundancy hardening in {weakest_region['Region']} corridors.",
                    "Lift regional service quality and protect customer sentiment in vulnerable zones.",
                    level="warning",
                )

        ov_col3, ov_col4 = st.columns(2)
        with ov_col3:
            st.markdown('<div class="net-mini-title">Pérdida Paquetes y Presión Incidentes</div>', unsafe_allow_html=True)
            with st.container(border=True):
                loss_line = alt.Chart(net_hourly).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Packet Loss %:Q", title="Packet Loss (%)"),
                    tooltip=["Hour:N", alt.Tooltip("Packet Loss %:Q", format=".2f"), alt.Tooltip("Incidents:Q", format=".0f"), alt.Tooltip("Latency ms:Q", format=".1f")],
                )
                inc_bar_hourly = alt.Chart(net_hourly).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, opacity=0.45, color="#EF4444", size=24).encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Incidents:Q", title="Incidents"),
                )
                st.altair_chart(style_net_chart(alt.layer(inc_bar_hourly, loss_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                peak_loss_hour = net_hourly.loc[net_hourly["Packet Loss %"].idxmax()]
                render_net_ai_reco(
                    "Quality Degradation Window",
                    f"Highest packet loss appears at {peak_loss_hour['Hour']} ({peak_loss_hour['Packet Loss %']:.2f}%) alongside elevated incident pressure.",
                    "Pre-stage troubleshooting teams during this window and trigger proactive congestion balancing.",
                    "Reduce visible quality dips and prevent avoidable complaint spikes.",
                    level="warning",
                )

        with ov_col4:
            st.markdown('<div class="net-mini-title">Índice Resiliencia Regional</div>', unsafe_allow_html=True)
            with st.container(border=True):
                resilience_df = net_regions.copy()
                resilience_df["Resilience Index"] = (
                    (resilience_df["Availability %"] - 99.70) * 320
                    + (60 - resilience_df["MTTR Min"]) * 0.9
                    + (resilience_df["NPS"] - 45) * 0.8
                ).clip(lower=45, upper=98)
                res_bar = alt.Chart(resilience_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Resilience Index:Q", title="Resilience Index"),
                    y=alt.Y("Region:N", sort="-x", title=None),
                    color=alt.Color("Resilience Index:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Region:N", alt.Tooltip("Resilience Index:Q", format=".1f"), alt.Tooltip("Availability %:Q", format=".2f"), alt.Tooltip("MTTR Min:Q", format=".0f"), alt.Tooltip("NPS:Q", format=".0f")],
                )
                res_text = alt.Chart(resilience_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Resilience Index:Q",
                    y=alt.Y("Region:N", sort="-x"),
                    text=alt.Text("Resilience Index:Q", format=".1f"),
                )
                st.altair_chart(style_net_chart(res_bar + res_text, height=235), use_container_width=True)
                weakest_res = resilience_df.loc[resilience_df["Resilience Index"].idxmin()]
                render_net_ai_reco(
                    "Resilience Benchmark",
                    f"{weakest_res['Region']} has the lowest resilience score at {weakest_res['Resilience Index']:.1f}.",
                    f"Bundle reliability and recovery initiatives in {weakest_res['Region']} under a single recovery OKR.",
                    "Lift structural reliability and narrow regional performance dispersion.",
                    level="warning",
                )

        st.markdown('<div class="net-title">Infraestructura WOM & Capacidad</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Capacidad Total Red</div><div class="v">{infra_total_capacity:,.0f} Gbps</div><div class="d">Core, 5G, FTTH, backbone</div></div>
                <div class="net-kpi-card {'warn' if infra_weighted_util > 75 else ''}"><div class="k">Utilización Ponderada</div><div class="v">{infra_weighted_util:.1f}%</div><div class="d">Perfil carga capacidad</div></div>
                <div class="net-kpi-card {'warn' if infra_redundancy_avg < 85 else ''}"><div class="k">Redundancia Promedio</div><div class="v">{infra_redundancy_avg:.1f}%</div><div class="d">Preparación failover</div></div>
                <div class="net-kpi-card {'warn' if infra_health_avg < 84 else ''}"><div class="k">Salud Infraestructura</div><div class="v">{infra_health_avg:.1f}</div><div class="d">Score calidad activos</div></div>
            </div>
        """), unsafe_allow_html=True)

        inf_col1, inf_col2 = st.columns(2)
        with inf_col1:
            st.markdown('<div class="net-mini-title">Capacidad y Utilización por Dominio</div>', unsafe_allow_html=True)
            with st.container(border=True):
                infra_cap = net_infra_assets.copy()
                infra_cap["Used Gbps"] = (infra_cap["Capacity Gbps"] * infra_cap["Utilization %"] / 100).round(1)
                cap_bar = alt.Chart(infra_cap).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=32, color="#60A5FA").encode(
                    x=alt.X("Domain:N", title=None),
                    y=alt.Y("Capacity Gbps:Q", title="Capacity (Gbps)"),
                    tooltip=["Domain:N", alt.Tooltip("Capacity Gbps:Q", format=".0f"), alt.Tooltip("Used Gbps:Q", format=".1f"), alt.Tooltip("Utilization %:Q", format=".1f")],
                )
                used_line = alt.Chart(infra_cap).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x="Domain:N",
                    y=alt.Y("Used Gbps:Q", title="Used (Gbps)"),
                )
                st.altair_chart(style_net_chart(alt.layer(cap_bar, used_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                hottest_domain = infra_cap.loc[infra_cap["Utilization %"].idxmax()]
                render_net_ai_reco(
                    "Capacity Load Balance",
                    f"{hottest_domain['Domain']} is the hottest domain at {hottest_domain['Utilization %']:.1f}% utilization.",
                    f"Prioritize near-term capacity augmentation in {hottest_domain['Domain']} to avoid saturation spillover.",
                    "Preserves headroom for growth and reduces performance degradation risk.",
                    level="warning",
                )

        with inf_col2:
            st.markdown('<div class="net-mini-title">Salud Activos vs Redundancia</div>', unsafe_allow_html=True)
            with st.container(border=True):
                infra_health = alt.Chart(net_infra_assets).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Redundancy %:Q", title="Redundancy (%)"),
                    y=alt.Y("Health Score:Q", title="Health Score"),
                    size=alt.Size("Sites:Q", scale=alt.Scale(range=[280, 1400]), legend=None),
                    color=alt.Color("Domain:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1"])),
                    tooltip=["Domain:N", alt.Tooltip("Sites:Q", format=","), alt.Tooltip("Redundancy %:Q", format=".1f"), alt.Tooltip("Health Score:Q", format=".1f")],
                )
                infra_label = alt.Chart(net_infra_assets).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Redundancy %:Q", y="Health Score:Q", text="Domain:N"
                )
                st.altair_chart(style_net_chart(infra_health + infra_label, height=235), use_container_width=True)
                weakest_domain = net_infra_assets.sort_values(["Health Score", "Redundancy %"]).iloc[0]
                render_net_ai_reco(
                    "Infrastructure Quality Focus",
                    f"{weakest_domain['Domain']} is the lowest combined health/redundancy domain.",
                    f"Bundle lifecycle refresh and failover reinforcement in {weakest_domain['Domain']}.",
                    "Improves resilience and lowers restoration pressure during faults.",
                    level="warning",
                )

    with net_tab_map:
        st.markdown('<div class="net-title">Mapa Estado Red WOM</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Nodos Mapeados</div><div class="v">{len(net_map_nodes)}</div><div class="d">Ciudades con telemetría</div></div>
                <div class="net-kpi-card {'warn' if (net_map_nodes['Status'] == 'Watch').sum() > 2 else ''}"><div class="k">Nodos Watch</div><div class="v">{(net_map_nodes['Status'] == 'Watch').sum()}</div><div class="d">Requiere acción preventiva</div></div>
                <div class="net-kpi-card {'crit' if (net_map_nodes['Status'] == 'At Risk').sum() > 1 else 'warn'}"><div class="k">Nodos En Riesgo</div><div class="v">{(net_map_nodes['Status'] == 'At Risk').sum()}</div><div class="d">Mitigación inmediata</div></div>
                <div class="net-kpi-card"><div class="k">Hotspots Incidentes</div><div class="v">{net_incident_points['weight'].gt(3).sum()}</div><div class="d">Clusters alta intensidad</div></div>
            </div>
        """), unsafe_allow_html=True)

        st.markdown('<div class="net-mini-title">Mejoras de Mapa</div>', unsafe_allow_html=True)
        enh_col1, enh_col2, enh_col3, enh_col4 = st.columns([1.25, 1.25, 1.25, 1.4])
        with enh_col1:
            enh_demand = st.checkbox("Footprint Demanda", value=True, key="net_map_enh_demand")
            enh_enterprise = st.checkbox("Sitios Empresariales", value=True, key="net_map_enh_enterprise")
        with enh_col2:
            enh_weather = st.checkbox("Riesgo Clima", value=True, key="net_map_enh_weather")
            enh_build = st.checkbox("Corredores Planificados", value=True, key="net_map_enh_build")
        with enh_col3:
            enh_labels = st.checkbox("Etiquetas Nodos", value=True, key="net_map_enh_labels")
            enh_hotspots = st.checkbox("Hotspots Densos", value=True, key="net_map_enh_hotspots")
        with enh_col4:
            lens = st.selectbox(
                "Lente Geográfico",
                ["Nacional Chile", "Metropolitana", "Corredor Norte", "Corredor Sur"],
                index=0,
                key="net_map_geo_lens",
            )

        lens_view = {
            "Nacional Chile": {"lat": -35.0, "lon": -71.5, "zoom": 5.35, "pitch": 33},
            "Metropolitana": {"lat": -33.45, "lon": -70.65, "zoom": 9.2, "pitch": 38},
            "Corredor Norte": {"lat": -23.0, "lon": -70.0, "zoom": 6.25, "pitch": 34},
            "Corredor Sur": {"lat": -40.0, "lon": -73.0, "zoom": 5.95, "pitch": 34},
        }[lens]

        st.markdown(dedent("""
            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.2rem 0 0.55rem 0;">
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Watch Pulse (Yellow)</span>
                <span style="background:#FEE2E2; border:1px solid #FCA5A5; color:#991B1B; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Critical Pulse (Red)</span>
                <span style="background:#DBEAFE; border:1px solid #93C5FD; color:#1E3A8A; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Enterprise Footprint (Blue)</span>
                <span style="background:#ECFDF5; border:1px solid #6EE7B7; color:#065F46; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Planned Build Corridors (Blue-Green)</span>
                <span style="background:#FFF7ED; border:1px solid #FDBA74; color:#9A3412; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Weather Risk (Orange-Red Heat)</span>
            </div>
        """), unsafe_allow_html=True)

        map_col1, map_col2 = st.columns(2)
        with map_col1:
            st.markdown('<div class="net-mini-title">Mapa Salud Nodos WOM en Vivo</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pulse_factor = 1.0 + (0.25 * (0.5 + 0.5 * math.sin(time.time() * 2.4)))
                pulse_wave = 0.5 + 0.5 * math.sin(time.time() * 3.2)
                node_df = net_map_nodes.copy()
                node_df["radius"] = node_df["Open Incidents"] * 650
                node_df["pulse_radius"] = node_df["radius"] * pulse_factor
                node_df["r"] = node_df["Status"].map({"Healthy": 16, "Watch": 245, "At Risk": 239})
                node_df["g"] = node_df["Status"].map({"Healthy": 185, "Watch": 158, "At Risk": 68})
                node_df["b"] = node_df["Status"].map({"Healthy": 129, "Watch": 11, "At Risk": 68})
                watch_points = net_access_points[net_access_points["Tier"] == "Watch"].copy()
                critical_points = net_access_points[net_access_points["Tier"] == "Critical"].copy()
                watch_points["pulse_radius"] = watch_points["radius"] * (2.6 + 0.7 * pulse_wave)
                critical_points["pulse_radius"] = critical_points["radius"] * (3.0 + 0.9 * pulse_wave)
                watch_alpha = int(32 + 38 * pulse_wave)
                crit_alpha = int(44 + 54 * pulse_wave)

                base_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=node_df,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 190]",
                    pickable=True,
                )
                pulse_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=node_df,
                    get_position="[lon, lat]",
                    get_radius="pulse_radius",
                    get_fill_color="[r, g, b, 70]",
                    stroked=True,
                    get_line_color="[r, g, b, 140]",
                    line_width_min_pixels=1,
                    pickable=False,
                )
                density_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_node_density,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 85]",
                    pickable=False,
                )
                access_heat_layer = pdk.Layer(
                    "HeatmapLayer",
                    data=net_access_points,
                    get_position="[lon, lat]",
                    get_weight="Traffic",
                    radiusPixels=45,
                    intensity=1.05,
                    threshold=0.03,
                    pickable=False,
                )
                access_sites_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_access_points,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 80]",
                    pickable=False,
                )
                watch_pulse_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=watch_points,
                    get_position="[lon, lat]",
                    get_radius="pulse_radius",
                    get_fill_color=[245, 158, 11, watch_alpha],
                    stroked=True,
                    get_line_color=[245, 158, 11, min(180, watch_alpha + 70)],
                    line_width_min_pixels=1,
                    pickable=False,
                )
                critical_pulse_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=critical_points,
                    get_position="[lon, lat]",
                    get_radius="pulse_radius",
                    get_fill_color=[239, 68, 68, crit_alpha],
                    stroked=True,
                    get_line_color=[239, 68, 68, min(210, crit_alpha + 70)],
                    line_width_min_pixels=1,
                    pickable=False,
                )
                enterprise_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_enterprise_geo,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color=[59, 130, 246, 130],
                    stroked=True,
                    get_line_color=[29, 78, 216, 220],
                    line_width_min_pixels=1,
                    pickable=True,
                )
                weather_heat_layer = pdk.Layer(
                    "HeatmapLayer",
                    data=net_weather_risk_geo,
                    get_position="[lon, lat]",
                    get_weight="Weather Risk",
                    radiusPixels=52,
                    intensity=1.25,
                    threshold=0.06,
                    pickable=False,
                )
                weather_sites_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_weather_risk_geo,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color=[239, 68, 68, 95],
                    stroked=True,
                    get_line_color=[245, 158, 11, 200],
                    line_width_min_pixels=1,
                    pickable=True,
                )
                build_corridor_layer = pdk.Layer(
                    "ArcLayer",
                    data=net_build_corridors,
                    get_source_position="[from_lon, from_lat]",
                    get_target_position="[to_lon, to_lat]",
                    get_source_color=[37, 99, 235, 145],
                    get_target_color=[16, 185, 129, 210],
                    get_width="width",
                    pickable=True,
                )
                node_label_layer = pdk.Layer(
                    "TextLayer",
                    data=net_node_labels,
                    get_position="[lon, lat]",
                    get_text="Label",
                    get_size=12,
                    get_color=[30, 41, 59, 220],
                    get_alignment_baseline="'top'",
                    get_pixel_offset=[0, 10],
                    pickable=False,
                )
                live_layers = []
                if enh_demand:
                    live_layers.extend([access_heat_layer, access_sites_layer])
                if enh_hotspots:
                    live_layers.append(density_layer)
                if enh_weather:
                    live_layers.extend([weather_heat_layer, weather_sites_layer])
                if enh_build:
                    live_layers.append(build_corridor_layer)
                if enh_enterprise:
                    live_layers.append(enterprise_layer)
                live_layers.extend([pulse_layer, base_layer, watch_pulse_layer, critical_pulse_layer])
                if enh_labels:
                    live_layers.append(node_label_layer)
                node_deck = pdk.Deck(
                    layers=live_layers,
                    initial_view_state=pdk.ViewState(latitude=lens_view["lat"], longitude=lens_view["lon"], zoom=lens_view["zoom"], pitch=lens_view["pitch"]),
                    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                    tooltip={"html": "<b>{Node}{City}{Zone}</b><br/>Status: {Status}<br/>Availability: {Availability %}%<br/>Utilization: {Utilization %}%<br/>Open Incidents: {Open Incidents}<br/>Accounts: {Accounts}<br/>Weather Risk: {Weather Risk}<br/>Phase: {Phase}<br/>Capex: CLP {Capex M}M"},
                )
                st.pydeck_chart(node_deck, use_container_width=True)
                st.caption("Watch (yellow) and critical (red) hotspots use pulsing rings, with access-footprint heat and micro-site density layered underneath.")
                weakest_node = net_map_nodes.loc[net_map_nodes["Availability %"].idxmin()]
                render_net_ai_reco(
                    "Geo Reliability Focus",
                    f"{weakest_node['Node']} is the most vulnerable mapped node at {weakest_node['Availability %']:.2f}% availability.",
                    f"Prioritize route hardening and preventive field sweeps in {weakest_node['Node']}.",
                    "Reduce outage concentration in the most exposed geography.",
                    level="warning",
                )

        with map_col2:
            st.markdown('<div class="net-mini-title">Heatmap Hotspots Incidentes</div>', unsafe_allow_html=True)
            with st.container(border=True):
                heat_layer = pdk.Layer(
                    "HeatmapLayer",
                    data=net_incident_density,
                    get_position="[lon, lat]",
                    get_weight="weight",
                    radiusPixels=70,
                    intensity=1.8,
                    threshold=0.08,
                    pickable=False,
                )
                hex_layer = pdk.Layer(
                    "HexagonLayer",
                    data=net_incident_density,
                    get_position="[lon, lat]",
                    get_weight="weight",
                    radius=14000,
                    elevation_scale=35,
                    elevation_range=[0, 1600],
                    extruded=True,
                    pickable=True,
                    auto_highlight=True,
                )
                scatter_overlay = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_incident_density,
                    get_position="[lon, lat]",
                    get_radius=2800,
                    get_fill_color=[239, 68, 68, 95],
                    pickable=True,
                )
                heat_deck = pdk.Deck(
                    layers=[heat_layer, hex_layer, scatter_overlay],
                    initial_view_state=pdk.ViewState(latitude=lens_view["lat"], longitude=lens_view["lon"], zoom=max(4.8, lens_view["zoom"] - 0.2), pitch=min(40, lens_view["pitch"] + 5)),
                    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                    tooltip={"html": "Incident Type: {Type}<br/>Intensity: {weight}"},
                )
                st.pydeck_chart(heat_deck, use_container_width=True)
                top_hotspot_type = net_incident_points.groupby("Type", as_index=False)["weight"].sum().sort_values("weight", ascending=False).iloc[0]
                render_net_ai_reco(
                    "Hotspot Risk Pattern",
                    f"{top_hotspot_type['Type']} is the dominant hotspot pattern on the map by aggregate intensity.",
                    f"Deploy preventive controls for {top_hotspot_type['Type']} clusters before peak utilization windows.",
                    "Lower repeat incidents and improve uptime consistency in hotspot corridors.",
                    level="critical" if top_hotspot_type["weight"] >= 13 else "warning",
                )

        st.markdown('<div class="net-mini-title">Centro Comando Red WOM (Toggles Capas)</div>', unsafe_allow_html=True)
        st.markdown(dedent("""
            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.1rem 0 0.5rem 0;">
                <span style="background:#DBEAFE; border:1px solid #93C5FD; color:#1E3A8A; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Node Health</span>
                <span style="background:#FFF7ED; border:1px solid #FDBA74; color:#9A3412; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Incident Hotspots</span>
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Fiber Cut Corridors</span>
                <span style="background:#DCFCE7; border:1px solid #86EFAC; color:#166534; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Backbone Load Flows</span>
                <span style="background:#E0E7FF; border:1px solid #A5B4FC; color:#3730A3; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">SLA Risk Towers</span>
            </div>
        """), unsafe_allow_html=True)
        ctl_col1, ctl_col2, ctl_col3 = st.columns([1.6, 1.6, 1.2])
        with ctl_col1:
            show_nodes = st.checkbox("Salud Nodos", value=True, key="net_map_toggle_nodes")
            show_hotspots = st.checkbox("Hotspots Incidentes", value=True, key="net_map_toggle_hotspots")
        with ctl_col2:
            show_fiber_cuts = st.checkbox("Corredores Cortes Fibra", value=True, key="net_map_toggle_fiber")
            show_backbone = st.checkbox("Flujos Carga Backbone", value=True, key="net_map_toggle_backbone")
        with ctl_col3:
            show_sla = st.checkbox("Torres Riesgo SLA", value=True, key="net_map_toggle_sla")
            basemap_choice = st.selectbox(
                "Basemap",
                ["CARTO Voyager", "CARTO Dark Matter", "CARTO Positron"],
                index=0,
                key="net_map_basemap_choice",
            )

        basemap_url = {
            "CARTO Voyager": "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
            "CARTO Dark Matter": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            "CARTO Positron": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        }[basemap_choice]

        with st.container(border=True):
            big_layers = []
            pulse_factor_big = 1.0 + (0.28 * (0.5 + 0.5 * math.sin(time.time() * 2.8)))

            if show_hotspots:
                big_layers.append(
                    pdk.Layer(
                        "HeatmapLayer",
                        data=net_incident_points,
                        get_position="[lon, lat]",
                        get_weight="weight",
                        radiusPixels=45,
                        intensity=1.2,
                        threshold=0.1,
                    )
                )

            if show_fiber_cuts:
                big_layers.append(
                    pdk.Layer(
                        "LineLayer",
                        data=net_fiber_paths,
                        get_source_position="[from_lon, from_lat]",
                        get_target_position="[to_lon, to_lat]",
                        get_width="Cuts",
                        width_scale=2,
                        get_color=[245, 158, 11, 170],
                        pickable=True,
                    )
                )

            if show_backbone:
                flow_df = net_backbone_flows.copy()
                flow_df["r"] = flow_df["Utilization %"].apply(lambda v: 239 if v >= 80 else 245 if v >= 70 else 16)
                flow_df["g"] = flow_df["Utilization %"].apply(lambda v: 68 if v >= 80 else 158 if v >= 70 else 185)
                flow_df["b"] = flow_df["Utilization %"].apply(lambda v: 68 if v >= 80 else 11 if v >= 70 else 129)
                big_layers.append(
                    pdk.Layer(
                        "ArcLayer",
                        data=flow_df,
                        get_source_position="[source_lon, source_lat]",
                        get_target_position="[target_lon, target_lat]",
                        get_source_color="[r, g, b, 150]",
                        get_target_color="[r, g, b, 200]",
                        get_width=2.8,
                        pickable=True,
                    )
                )

            if show_sla:
                big_layers.append(
                    pdk.Layer(
                        "ColumnLayer",
                        data=net_sla_geo,
                        get_position="[lon, lat]",
                        get_elevation="SLA Risk * 120",
                        elevation_scale=1,
                        radius=9000,
                        get_fill_color=[59, 130, 246, 140],
                        pickable=True,
                        extruded=True,
                    )
                )

            if show_nodes:
                node_big = net_map_nodes.copy()
                node_big["radius"] = node_big["Open Incidents"] * 1200
                node_big["pulse_radius"] = node_big["radius"] * pulse_factor_big
                node_big["r"] = node_big["Status"].map({"Healthy": 16, "Watch": 245, "At Risk": 239})
                node_big["g"] = node_big["Status"].map({"Healthy": 185, "Watch": 158, "At Risk": 68})
                node_big["b"] = node_big["Status"].map({"Healthy": 129, "Watch": 11, "At Risk": 68})
                big_layers.extend([
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=node_big,
                        get_position="[lon, lat]",
                        get_radius="pulse_radius",
                        get_fill_color="[r, g, b, 60]",
                        get_line_color="[r, g, b, 120]",
                        stroked=True,
                        line_width_min_pixels=1,
                        pickable=False,
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=node_big,
                        get_position="[lon, lat]",
                        get_radius="radius",
                        get_fill_color="[r, g, b, 195]",
                        pickable=True,
                    ),
                ])

            command_center = pdk.Deck(
                layers=big_layers,
                initial_view_state=pdk.ViewState(latitude=-35.0, longitude=-71.5, zoom=4.6, pitch=38),
                map_style=basemap_url,
                tooltip={
                    "html": "<b>{Node}{City}</b><br/>Status: {Status}<br/>Availability: {Availability %}%<br/>Incidents: {Open Incidents}<br/>SLA Risk: {SLA Risk}<br/>Flow Utilization: {Utilization %}%<br/>Cuts: {Cuts}<br/>Type: {Type}"
                },
            )
            st.pydeck_chart(command_center, use_container_width=True)
            st.caption("Use toggles to compose executive narratives: capacity stress, outage concentration, SLA exposure, and geographic risk.")
            highest_sla_city = net_sla_geo.loc[net_sla_geo["SLA Risk"].idxmax()]
            render_net_ai_reco(
                "Command Center Readout",
                f"Highest SLA risk tower is {highest_sla_city['City']} at {highest_sla_city['SLA Risk']:.0f}, while map overlays show concentrated stress corridors.",
                "Lead with corridor hardening and targeted field dispatch in high-risk cities before peak traffic windows.",
                "Improves board-level confidence with visible control of geographic reliability risk.",
                level="critical" if highest_sla_city["SLA Risk"] >= 45 else "warning",
            )

        st.markdown('<div class="net-mini-title">Atlas Oportunidad Expansión Estratégica WOM</div>', unsafe_allow_html=True)
        st.markdown(dedent("""
            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.1rem 0 0.5rem 0;">
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Coverage Gap Grid</span>
                <span style="background:#FEE2E2; border:1px solid #FCA5A5; color:#991B1B; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Revenue-at-Risk Bubbles</span>
                <span style="background:#FFEDD5; border:1px solid #FDBA74; color:#9A3412; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Expansion Priority Towers</span>
                <span style="background:#DBEAFE; border:1px solid #93C5FD; color:#1E3A8A; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Top Expansion Corridors</span>
                <span style="background:#ECFDF5; border:1px solid #6EE7B7; color:#065F46; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Where to Invest Rings</span>
                <span style="background:#DBEAFE; border:1px solid #60A5FA; color:#1E3A8A; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Core Hub Cities</span>
                <span style="background:#DCFCE7; border:1px solid #86EFAC; color:#166534; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Growth Node Cities</span>
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Emerging Node Cities</span>
            </div>
        """), unsafe_allow_html=True)
        exp_col1, exp_col2, exp_col3 = st.columns([1.35, 1.35, 1.3])
        with exp_col1:
            show_cov_gap = st.checkbox("Grid Gaps Cobertura", value=True, key="net_exp_toggle_gap")
            show_arr_risk = st.checkbox("Burbujas Revenue en Riesgo", value=True, key="net_exp_toggle_arr")
        with exp_col2:
            show_exp_towers = st.checkbox("Torres Prioridad Expansión", value=True, key="net_exp_toggle_towers")
            show_corridors = st.checkbox("Top Corredores Expansión", value=True, key="net_exp_toggle_corridors")
        with exp_col3:
            show_targets = st.checkbox("Dónde Invertir (Ranking)", value=True, key="net_exp_toggle_targets")
            horizon = st.selectbox("Horizonte Planificación", ["6M", "12M", "18M"], index=1, key="net_exp_horizon")

        horizon_profile = {
            "6M": {"priority": 0.93, "gap": 0.88, "arr": 0.78, "capex": 0.82, "tower": 0.86, "corr": 0.84, "target_radius": 0.80, "cell_size": 22000, "payback": 1.08},
            "12M": {"priority": 1.00, "gap": 1.00, "arr": 1.00, "capex": 1.00, "tower": 1.00, "corr": 1.00, "target_radius": 1.00, "cell_size": 28000, "payback": 1.00},
            "18M": {"priority": 1.12, "gap": 1.15, "arr": 1.30, "capex": 1.24, "tower": 1.25, "corr": 1.22, "target_radius": 1.28, "cell_size": 34000, "payback": 0.92},
        }[horizon]
        # Build a denser synthetic opportunity field so national investment coverage
        # looks richer in executive demos.
        opp_seed = net_opportunity_geo.copy()
        synth_rng = random.Random(29)
        synth_offsets = [
            (0.00, 0.00), (0.08, 0.03), (-0.08, 0.03), (0.06, -0.05),
            (-0.06, -0.05), (0.11, 0.00), (-0.11, 0.00), (0.03, 0.08),
        ]
        synth_records = []
        for _, row in opp_seed.iterrows():
            cluster_size = 5 if row["Demand Index"] >= 74 else 4
            for i in range(cluster_size):
                off_lon, off_lat = synth_offsets[i % len(synth_offsets)]
                scale = 0.42 + 0.12 * (i // len(synth_offsets))
                synth_records.append({
                    "Zone": f"{row['Zone']} · Growth Cluster {i + 1}",
                    "lat": row["lat"] + off_lat * scale + synth_rng.uniform(-0.013, 0.013),
                    "lon": row["lon"] + off_lon * scale + synth_rng.uniform(-0.013, 0.013),
                    "Demand Index": min(96, row["Demand Index"] + synth_rng.randint(2, 11)),
                    "Coverage Gap %": min(29, row["Coverage Gap %"] + synth_rng.randint(1, 8)),
                    "ARR Risk M": round(row["ARR Risk M"] * synth_rng.uniform(1.06, 1.36), 2),
                    "Capex M": round(row["Capex M"] * synth_rng.uniform(0.94, 1.14), 2),
                    "Payback Mo": round(max(7.0, row["Payback Mo"] - synth_rng.uniform(0.9, 3.2)), 1),
                    "Priority Score": min(97, row["Priority Score"] + synth_rng.randint(3, 10)),
                })
        opp_df = pd.concat([opp_seed, pd.DataFrame(synth_records)], ignore_index=True)
        opp_df["Priority Adj"] = (opp_df["Priority Score"] * horizon_profile["priority"]).round(1)
        opp_df["Coverage Gap Horizon %"] = (opp_df["Coverage Gap %"] * horizon_profile["gap"]).round(1)
        opp_df["ARR Horizon M"] = (opp_df["ARR Risk M"] * horizon_profile["arr"]).round(2)
        opp_df["Capex Horizon M"] = (opp_df["Capex M"] * horizon_profile["capex"]).round(2)
        opp_df["Payback Horizon Mo"] = (opp_df["Payback Mo"] * horizon_profile["payback"]).round(1)
        opp_df["Gap Elev"] = opp_df["Coverage Gap Horizon %"] * 95
        opp_df["ARR Radius"] = opp_df["ARR Horizon M"] * 42000 * (0.9 + 0.18 * (0.5 + 0.5 * math.sin(time.time() * 2.2)))
        opp_df["Tower Elev"] = opp_df["Priority Adj"] * 135 * horizon_profile["tower"]
        opp_df["r"] = opp_df["Priority Adj"].apply(lambda v: 239 if v >= 84 else 245 if v >= 76 else 16)
        opp_df["g"] = opp_df["Priority Adj"].apply(lambda v: 68 if v >= 84 else 158 if v >= 76 else 185)
        opp_df["b"] = opp_df["Priority Adj"].apply(lambda v: 68 if v >= 84 else 11 if v >= 76 else 129)
        opp_df = opp_df.sort_values("Priority Adj", ascending=False).reset_index(drop=True)
        opp_df["Rank"] = opp_df.index + 1
        opp_df["Invest Label"] = opp_df["Rank"].apply(lambda r: f"{horizon} INVEST #{r}") + " - " + opp_df["Zone"]
        top3 = opp_df.head(3).copy()
        top5 = opp_df.head(5).copy()
        top5["hub_lon"] = -70.65
        top5["hub_lat"] = -33.45
        top5["Corridor Width"] = (2.6 + (top5["Priority Adj"] - 70) / 14).clip(lower=2.2, upper=6.0) * horizon_profile["corr"]
        top5["Target Radius"] = (42000 * horizon_profile["target_radius"] * (top5["Priority Adj"] / 90)).round(0)
        city_map_df = net_major_cities_geo.copy()

        st.markdown(dedent(f"""
            <div class="net-kpi-grid" style="margin-bottom: 0.42rem;">
                <div class="net-kpi-card crit"><div class="k">#1 Invest</div><div class="v">{top3.iloc[0]['Zone']}</div><div class="d">Priority {top3.iloc[0]['Priority Adj']:.1f} · Payback {top3.iloc[0]['Payback Horizon Mo']:.1f} mo</div></div>
                <div class="net-kpi-card warn"><div class="k">#2 Invest</div><div class="v">{top3.iloc[1]['Zone']}</div><div class="d">Priority {top3.iloc[1]['Priority Adj']:.1f} · Payback {top3.iloc[1]['Payback Horizon Mo']:.1f} mo</div></div>
                <div class="net-kpi-card"><div class="k">#3 Invest</div><div class="v">{top3.iloc[2]['Zone']}</div><div class="d">Priority {top3.iloc[2]['Priority Adj']:.1f} · Payback {top3.iloc[2]['Payback Horizon Mo']:.1f} mo</div></div>
                <div class="net-kpi-card"><div class="k">Top-3 CAPEX</div><div class="v">CLP {top3['Capex Horizon M'].sum():.2f}M</div><div class="d">{horizon} targeted build plan</div></div>
            </div>
        """), unsafe_allow_html=True)
        st.caption(f"Horizon profile active: {horizon} - map geometry and investment economics are scaled for this planning window.")

        with st.container(border=True):
            atlas_layers = []
            if show_cov_gap:
                atlas_layers.append(
                    pdk.Layer(
                        "GridCellLayer",
                        data=opp_df,
                        get_position="[lon, lat]",
                        cell_size=horizon_profile["cell_size"],
                        get_elevation="Gap Elev",
                        elevation_scale=1,
                        extruded=True,
                        get_fill_color="[245, 158, 11, 135]",
                        pickable=True,
                    )
                )
            if show_arr_risk:
                atlas_layers.append(
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=opp_df,
                        get_position="[lon, lat]",
                        get_radius="ARR Radius",
                        get_fill_color="[239, 68, 68, 120]",
                        stroked=True,
                        get_line_color="[239, 68, 68, 180]",
                        line_width_min_pixels=1,
                        pickable=True,
                    )
                )
            if show_exp_towers:
                atlas_layers.append(
                    pdk.Layer(
                        "ColumnLayer",
                        data=opp_df,
                        get_position="[lon, lat]",
                        get_elevation="Tower Elev",
                        elevation_scale=1,
                        radius=14000,
                        get_fill_color="[r, g, b, 185]",
                        pickable=True,
                        extruded=True,
                    )
                )
            if show_corridors:
                atlas_layers.append(
                    pdk.Layer(
                        "ArcLayer",
                        data=top5,
                        get_source_position="[hub_lon, hub_lat]",
                        get_target_position="[lon, lat]",
                        get_source_color="[37, 99, 235, 130]",
                        get_target_color="[16, 185, 129, 190]",
                        get_width="Corridor Width",
                        pickable=True,
                    )
                )
            if show_targets:
                atlas_layers.extend([
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=top5,
                        get_position="[lon, lat]",
                        get_radius="Target Radius",
                        get_fill_color=[16, 185, 129, 55],
                        stroked=True,
                        get_line_color=[16, 185, 129, 220],
                        line_width_min_pixels=2,
                        pickable=True,
                    ),
                    pdk.Layer(
                        "TextLayer",
                        data=top5,
                        get_position="[lon, lat]",
                        get_text="Invest Label",
                        get_size=14,
                        get_color=[15, 23, 42, 230],
                        get_alignment_baseline="'top'",
                        get_pixel_offset=[0, 18],
                        pickable=False,
                    ),
                ])
            atlas_layers.extend([
                pdk.Layer(
                    "ScatterplotLayer",
                    data=city_map_df,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 170]",
                    stroked=True,
                    get_line_color="[255, 255, 255, 220]",
                    line_width_min_pixels=1.5,
                    pickable=True,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=city_map_df,
                    get_position="[lon, lat]",
                    get_text="City",
                    get_size=13,
                    get_color=[15, 23, 42, 235],
                    get_alignment_baseline="'bottom'",
                    get_pixel_offset=[0, -10],
                    pickable=False,
                ),
            ])

            atlas_deck = pdk.Deck(
                layers=atlas_layers,
                initial_view_state=pdk.ViewState(latitude=-35.0, longitude=-71.5, zoom=5.0, pitch=40),
                map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                tooltip={
                    "html": "<b>{Zone}{City}</b><br/>Tier: {City Tier}<br/>Signal: {Investment Signal}<br/>Invest Rank: #{Rank}<br/>Demand: {Demand Index}<br/>Coverage Gap ({horizon}): {Coverage Gap Horizon %}%<br/>ARR Risk ({horizon}): CLP {ARR Horizon M}M<br/>Capex ({horizon}): CLP {Capex Horizon M}M<br/>Payback ({horizon}): {Payback Horizon Mo} mo<br/>Priority: {Priority Adj}"
                },
            )
            st.pydeck_chart(atlas_deck, use_container_width=True)
            st.markdown(dedent("""
                <div style="margin-top:0.45rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#2563EB; display:inline-block;"></span> Core Hub Cities
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#10B981; display:inline-block;"></span> Growth Node Cities
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#F59E0B; display:inline-block;"></span> Emerging Node Cities
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#EF4444; display:inline-block;"></span> Revenue-at-Risk Bubbles
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:14px; height:3px; border-radius:2px; background:#2563EB; display:inline-block;"></span> Expansion Corridors
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; border:2px solid #10B981; background:transparent; display:inline-block;"></span> Ranked Investment Rings
                    </span>
                </div>
            """), unsafe_allow_html=True)
            st.caption("Executive lens: combine demand, coverage gap, revenue-at-risk, and payback to prioritize expansion corridors.")
            top_zone = opp_df.sort_values("Priority Adj", ascending=False).iloc[0]
            render_net_ai_reco(
                "Expansion Prioritization Signal",
                f"Top zone for {horizon} is {top_zone['Zone']} with priority {top_zone['Priority Adj']:.1f}, coverage gap {top_zone['Coverage Gap Horizon %']:.1f}%, and ARR risk CLP {top_zone['ARR Horizon M']:.2f}M.",
                f"Prioritize phased build in {top_zone['Zone']} and lock field capacity for first-wave execution.",
                "Improves growth quality by concentrating CAPEX on highest-value, fastest-payback opportunities.",
                level="critical" if top_zone["Priority Adj"] >= 85 else "warning",
            )

    with net_tab_ops:
        st.markdown('<div class="net-title">Network Operations Control Tower</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Incident Run-Rate</div><div class="v">{net_incident_trend.iloc[-1]['Incidents']:.0f}</div><div class="d">Latest month incidents</div></div>
                <div class="net-kpi-card"><div class="k">MTTR Trend</div><div class="v">{net_incident_trend.iloc[0]['MTTR Min']-mttr_current:.0f} min</div><div class="d">Improvement vs period start</div></div>
                <div class="net-kpi-card {'warn' if breach_rate > 9 else ''}"><div class="k">SLA Breach Rate</div><div class="v">{breach_rate:.1f}%</div><div class="d">Cross-queue average</div></div>
                <div class="net-kpi-card {'warn' if net_queue['Avg Age Hr'].mean() > 10 else ''}"><div class="k">Ticket Aging</div><div class="v">{net_queue['Avg Age Hr'].mean():.1f} h</div><div class="d">Average open ticket age</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="net-mini-title">Incident Volume and MTTR Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                inc_bar = alt.Chart(net_incident_trend).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=36, color="#60A5FA").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Incidents:Q", title="Incidents"),
                    tooltip=["Month:N", alt.Tooltip("Incidents:Q", format=".0f"), alt.Tooltip("MTTR Min:Q", format=".0f")],
                )
                mttr_line = alt.Chart(net_incident_trend).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x="Month:N",
                    y=alt.Y("MTTR Min:Q", title="MTTR (min)"),
                )
                st.altair_chart(style_net_chart(alt.layer(inc_bar, mttr_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_net_ai_reco(
                    "Operational Discipline",
                    f"Incidents dropped from {net_incident_trend.iloc[0]['Incidents']:.0f} to {net_incident_trend.iloc[-1]['Incidents']:.0f}, with MTTR down to {mttr_current:.0f} min.",
                    "Sustain weekly RCA cadence and keep fast-response playbooks active for repeat patterns.",
                    "Continue improving restoration speed while keeping outage volume on a downward track.",
                )

        with op_col2:
            st.markdown('<div class="net-mini-title">Queue Pressure and SLA Risk</div>', unsafe_allow_html=True)
            with st.container(border=True):
                queue_bar = alt.Chart(net_queue).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Open Tickets:Q", title="Open Tickets"),
                    y=alt.Y("Queue:N", sort="-x", title=None),
                    color=alt.Color("SLA Breach %:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="SLA Breach %")),
                    tooltip=["Queue:N", alt.Tooltip("Open Tickets:Q", format=".0f"), alt.Tooltip("SLA Breach %:Q", format=".1f"), alt.Tooltip("Avg Age Hr:Q", format=".1f")],
                )
                queue_label = alt.Chart(net_queue).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Open Tickets:Q", y=alt.Y("Queue:N", sort="-x"), text=alt.Text("Avg Age Hr:Q", format=".1f")
                )
                st.altair_chart(style_net_chart(queue_bar + queue_label, height=235), use_container_width=True)
                top_queue = net_queue.loc[net_queue["Open Tickets"].idxmax()]
                render_net_ai_reco(
                    "Workflow Balancing",
                    f"{top_queue['Queue']} queue carries the highest open load with elevated SLA pressure.",
                    f"Reallocate dispatch capacity toward {top_queue['Queue']} and enforce 24-hour breach recovery goals.",
                    "Lower backlog, improve SLA compliance, and stabilize operations workload.",
                    level="warning",
                )

        op_col3, op_col4 = st.columns(2)
        with op_col3:
            st.markdown('<div class="net-mini-title">Queue Aging vs SLA Breach Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                queue_scatter = alt.Chart(net_queue).mark_circle(opacity=0.86, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Avg Age Hr:Q", title="Average Ticket Age (hours)"),
                    y=alt.Y("SLA Breach %:Q", title="SLA Breach (%)"),
                    size=alt.Size("Open Tickets:Q", scale=alt.Scale(range=[320, 1400]), legend=None),
                    color=alt.Color("Queue:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1"])),
                    tooltip=["Queue:N", alt.Tooltip("Open Tickets:Q", format=".0f"), alt.Tooltip("Avg Age Hr:Q", format=".1f"), alt.Tooltip("SLA Breach %:Q", format=".1f")],
                )
                queue_names = alt.Chart(net_queue).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Avg Age Hr:Q", y="SLA Breach %:Q", text="Queue:N"
                )
                st.altair_chart(style_net_chart(queue_scatter + queue_names, height=235), use_container_width=True)
                risk_queue = net_queue.sort_values(["SLA Breach %", "Avg Age Hr"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Queue Risk Hotspot",
                    f"{risk_queue['Queue']} sits at the highest combined ticket age and SLA breach risk.",
                    f"Deploy surge capacity and stricter triage thresholds for {risk_queue['Queue']} backlog items.",
                    "Shrink breach exposure and accelerate queue normalization.",
                    level="warning",
                )

        with op_col4:
            st.markdown('<div class="net-mini-title">Backlog Mix by Queue</div>', unsafe_allow_html=True)
            with st.container(border=True):
                queue_mix = net_queue.copy()
                queue_mix["Share %"] = (queue_mix["Open Tickets"] / queue_mix["Open Tickets"].sum() * 100).round(1)
                mix_arc = alt.Chart(queue_mix).mark_arc(innerRadius=62, outerRadius=104).encode(
                    theta=alt.Theta("Open Tickets:Q"),
                    color=alt.Color("Queue:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1"])),
                    tooltip=["Queue:N", alt.Tooltip("Open Tickets:Q", format=".0f"), alt.Tooltip("Share %:Q", format=".1f"), alt.Tooltip("SLA Breach %:Q", format=".1f")],
                )
                mix_text = alt.Chart(pd.DataFrame({"t": [f"{queue_mix['Open Tickets'].sum():.0f}"]})).mark_text(fontSize=22, fontWeight="bold", color="#0F172A").encode(text="t:N")
                mix_sub = alt.Chart(pd.DataFrame({"t": ["Open Tickets"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
                st.altair_chart(style_net_chart(mix_arc + mix_text + mix_sub, height=235), use_container_width=True)
                dominant_queue = queue_mix.loc[queue_mix["Open Tickets"].idxmax()]
                render_net_ai_reco(
                    "Workload Composition",
                    f"{dominant_queue['Queue']} represents the largest backlog share at {dominant_queue['Share %']:.1f}%.",
                    "Set queue-specific closure targets and enforce daily burn-down governance.",
                    "Improve throughput predictability and stabilize incident closure cadence.",
                )

        st.markdown('<div class="net-title">Infrastructure Operations Pipeline</div>', unsafe_allow_html=True)
        op_inf_col1, op_inf_col2 = st.columns(2)
        with op_inf_col1:
            st.markdown('<div class="net-mini-title">Maintenance Backlog by Asset Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                maint_df = net_maintenance.copy()
                maint_df["Critical Workorders"] = (maint_df["Open Workorders"] * maint_df["Critical %"] / 100).round(1)
                maint_bar = alt.Chart(maint_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Open Workorders:Q", title="Open Workorders"),
                    y=alt.Y("Asset Type:N", sort="-x", title=None),
                    color=alt.Color("Critical %:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Critical %")),
                    tooltip=["Asset Type:N", alt.Tooltip("Open Workorders:Q", format=".0f"), alt.Tooltip("Critical %:Q", format=".1f"), alt.Tooltip("Avg Delay Hr:Q", format=".1f")],
                )
                maint_label = alt.Chart(maint_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Open Workorders:Q", y=alt.Y("Asset Type:N", sort="-x"), text=alt.Text("Critical Workorders:Q", format=".1f")
                )
                st.altair_chart(style_net_chart(maint_bar + maint_label, height=235), use_container_width=True)
                top_maint = maint_df.loc[maint_df["Open Workorders"].idxmax()]
                render_net_ai_reco(
                    "Maintenance Bottleneck",
                    f"{top_maint['Asset Type']} has the highest workorder backlog with elevated critical exposure.",
                    f"Prioritize additional field windows for {top_maint['Asset Type']} and enforce max-age policy.",
                    "Reduces deferred maintenance risk and improves asset reliability trajectory.",
                    level="warning",
                )

        with op_inf_col2:
            st.markdown('<div class="net-mini-title">Upgrade Program Impact vs CAPEX</div>', unsafe_allow_html=True)
            with st.container(border=True):
                upg_scatter = alt.Chart(net_upgrade_program).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Capex M:Q", title="CAPEX (CLP  M)"),
                    y=alt.Y("Impact Score:Q", title="Impact Score"),
                    size=alt.Size("Delivery Risk:Q", scale=alt.Scale(range=[260, 1300]), legend=alt.Legend(title="Delivery Risk")),
                    color=alt.Color("Quarter:N", legend=alt.Legend(title="Execution Quarter"), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B"])),
                    tooltip=["Initiative:N", "Domain:N", alt.Tooltip("Capex M:Q", format=".2f"), alt.Tooltip("Impact Score:Q", format=".0f"), alt.Tooltip("Delivery Risk:Q", format=".1f"), "Quarter:N"],
                )
                upg_labels = alt.Chart(net_upgrade_program).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Capex M:Q", y="Impact Score:Q", text="Initiative:N"
                )
                st.altair_chart(style_net_chart(upg_scatter + upg_labels, height=235), use_container_width=True)
                top_program = net_upgrade_program.sort_values(["Impact Score", "Delivery Risk"], ascending=[False, True]).iloc[0]
                render_net_ai_reco(
                    "Upgrade Sequencing",
                    f"{top_program['Initiative']} offers the best impact-to-risk profile for the current pipeline.",
                    f"Pull forward {top_program['Initiative']} and protect delivery resources in {top_program['Quarter']}.",
                    "Accelerates infrastructure value realization with controlled execution risk.",
                )

    with net_tab_impact:
        st.markdown('<div class="net-title">Service Impact and Customer Exposure</div>', unsafe_allow_html=True)
        service_subs_k = net_service_impact["Subs Impacted K"].sum()
        service_arr_m = net_service_impact["ARR at Risk M"].sum()
        service_enterprise = int(net_service_impact["Enterprise Accounts"].sum())
        sla_target_week = net_sla_command["SLA Target %"].iloc[-1]
        sla_forecast_week = net_sla_command["SLA Forecast %"].iloc[-1]
        sla_gap_pp = sla_target_week - sla_forecast_week

        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card {'crit' if service_subs_k > 8 else 'warn'}"><div class="k">Subscribers Impacted</div><div class="v">{service_subs_k:.1f}K</div><div class="d">Current service exposure</div></div>
                <div class="net-kpi-card {'crit' if service_arr_m > 3.5 else 'warn'}"><div class="k">ARR at Risk</div><div class="v">CLP {service_arr_m:.2f}M</div><div class="d">Business impact footprint</div></div>
                <div class="net-kpi-card"><div class="k">Enterprise Accounts</div><div class="v">{service_enterprise}</div><div class="d">High-value accounts affected</div></div>
                <div class="net-kpi-card {'crit' if sla_gap_pp > 0.3 else 'warn' if sla_gap_pp > 0.1 else ''}"><div class="k">SLA Forecast Gap</div><div class="v">{sla_gap_pp:+.2f}pp</div><div class="d">vs weekly target</div></div>
            </div>
        """), unsafe_allow_html=True)

        imp_col1, imp_col2 = st.columns(2)
        with imp_col1:
            st.markdown('<div class="net-mini-title">Incident Business Impact by Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                impact_bar = alt.Chart(net_service_impact).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=28, color="#60A5FA").encode(
                    x=alt.X("Incident Type:N", title=None),
                    y=alt.Y("Subs Impacted K:Q", title="Impacted Subscribers (K)"),
                    tooltip=["Incident Type:N", alt.Tooltip("Subs Impacted K:Q", format=".0f"), alt.Tooltip("ARR at Risk M:Q", format=".2f"), alt.Tooltip("Avg Restore Hr:Q", format=".1f")],
                )
                impact_line = alt.Chart(net_service_impact).mark_line(point=True, strokeWidth=3, color="#EF4444").encode(
                    x="Incident Type:N",
                    y=alt.Y("ARR at Risk M:Q", title="ARR at Risk (CLP  M)"),
                )
                st.altair_chart(style_net_chart(alt.layer(impact_bar, impact_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                top_impact = net_service_impact.loc[net_service_impact["ARR at Risk M"].idxmax()]
                render_net_ai_reco(
                    "Business Impact Prioritization",
                    f"{top_impact['Incident Type']} drives the highest ARR exposure at CLP {top_impact['ARR at Risk M']:.2f}M.",
                    f"Prioritize fast-response and prevention controls for {top_impact['Incident Type']} failure patterns.",
                    "Directly protects revenue continuity and enterprise customer confidence.",
                    level="critical",
                )

        with imp_col2:
            st.markdown('<div class="net-mini-title">Network Quality vs Customer Outcomes</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cust_corr = alt.Chart(net_customer_link).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Latency ms:Q", title="Latency (ms)"),
                    y=alt.Y("Churn %:Q", title="Churn (%)"),
                    size=alt.Size("Packet Loss %:Q", scale=alt.Scale(range=[300, 1600]), legend=alt.Legend(title="Packet Loss %")),
                    color=alt.Color("NPS:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="NPS")),
                    tooltip=["Region:N", alt.Tooltip("Latency ms:Q", format=".1f"), alt.Tooltip("Packet Loss %:Q", format=".2f"), alt.Tooltip("NPS:Q", format=".0f"), alt.Tooltip("Churn %:Q", format=".1f")],
                )
                corr_label = alt.Chart(net_customer_link).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Latency ms:Q", y="Churn %:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(cust_corr + corr_label, height=235), use_container_width=True)
                worst_exp = net_customer_link.sort_values(["Churn %", "Latency ms"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Customer Impact Link",
                    f"{worst_exp['Region']} combines high latency/churn pressure and should be treated as a priority quality zone.",
                    f"Pair network remediation with proactive customer retention campaigns in {worst_exp['Region']}.",
                    "Improves technical quality and reduces preventable churn in exposed cohorts.",
                    level="warning",
                )

        imp_col3, imp_col4 = st.columns(2)
        with imp_col3:
            st.markdown('<div class="net-mini-title">SLA Command Widget (Target vs Forecast)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sla_actual = alt.Chart(net_sla_command).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Day:N", title=None),
                    y=alt.Y("SLA Actual %:Q", title="SLA (%)"),
                    tooltip=["Day:N", alt.Tooltip("SLA Actual %:Q", format=".2f"), alt.Tooltip("SLA Forecast %:Q", format=".2f"), alt.Tooltip("SLA Target %:Q", format=".2f")],
                )
                sla_forecast = alt.Chart(net_sla_command).mark_line(point=True, strokeWidth=2.6, color="#10B981", strokeDash=[6, 3]).encode(
                    x="Day:N", y="SLA Forecast %:Q"
                )
                sla_target = alt.Chart(net_sla_command).mark_line(strokeWidth=2.2, color="#EF4444").encode(
                    x="Day:N", y="SLA Target %:Q"
                )
                st.altair_chart(style_net_chart(alt.layer(sla_actual, sla_forecast, sla_target), height=235), use_container_width=True)
                render_net_ai_reco(
                    "SLA Early Warning",
                    f"Week-end SLA is forecast at {sla_forecast_week:.2f}% vs target {sla_target_week:.2f}% ({sla_gap_pp:+.2f}pp).",
                    "Trigger service stabilization measures before week close and protect high-value circuits first.",
                    "Improves probability of SLA target attainment and lowers penalty exposure.",
                    level="warning" if sla_gap_pp > 0.1 else "info",
                )

        with imp_col4:
            st.markdown('<div class="net-mini-title">Outage Timeline Playback</div>', unsafe_allow_html=True)
            with st.container(border=True):
                selected_hour = st.slider("Playback Hour", 0, 23, 12, key="net_outage_playback_hour")
                timeline_df = net_outage_timeline.copy()
                selected_point = timeline_df[timeline_df["Hour"] == selected_hour]
                timeline_bar = alt.Chart(timeline_df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#93C5FD").encode(
                    x=alt.X("Hour:O", title="Hour of Day"),
                    y=alt.Y("Subs Impacted K:Q", title="Impacted Subs (K)"),
                    tooltip=[alt.Tooltip("Hour:O", title="Hour"), alt.Tooltip("Subs Impacted K:Q", format=".0f"), alt.Tooltip("Incidents:Q", format=".0f")],
                )
                select_rule = alt.Chart(selected_point).mark_rule(color="#EF4444", strokeWidth=2).encode(x=alt.X("Hour:O"))
                inc_line = alt.Chart(timeline_df).mark_line(point=True, strokeWidth=2.4, color="#F59E0B").encode(
                    x=alt.X("Hour:O", title=None), y=alt.Y("Incidents:Q", title="Incidents")
                )
                st.altair_chart(style_net_chart(alt.layer(timeline_bar, inc_line, select_rule).resolve_scale(y="independent"), height=235), use_container_width=True)
                playback = selected_point.iloc[0]
                render_net_ai_reco(
                    "Timeline Snapshot",
                    f"At {int(playback['Hour']):02d}:00, estimated impact is {playback['Subs Impacted K']:.1f}K subscribers across {playback['Incidents']:.0f} incidents.",
                    "Use hourly playback to align dispatch windows and proactive communication timing.",
                    "Improves incident response pacing and stakeholder situational awareness.",
                    level="warning" if playback["Subs Impacted K"] >= 6 else "info",
                )

    with net_tab_exec:
        st.markdown('<div class="net-title">Execution and Playbook Control</div>', unsafe_allow_html=True)
        on_track_pct = (net_mitigation_tracker["Status"] == "On Track").mean() * 100
        total_capex_exec = net_upgrade_program["Capex M"].sum()
        high_critical_sites = int((net_critical_sites["Criticality"] >= 88).sum())
        max_forecast_util = net_capacity_forecast["Projected Util %"].max()

        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Program CAPEX</div><div class="v">CLP {total_capex_exec:.1f}M</div><div class="d">Active infrastructure initiatives</div></div>
                <div class="net-kpi-card {'warn' if max_forecast_util >= 85 else ''}"><div class="k">Peak Forecast Utilization</div><div class="v">{max_forecast_util:.0f}%</div><div class="d">90-day projection ceiling</div></div>
                <div class="net-kpi-card {'warn' if on_track_pct < 70 else ''}"><div class="k">Mitigation On-Track</div><div class="v">{on_track_pct:.0f}%</div><div class="d">Execution confidence</div></div>
                <div class="net-kpi-card {'crit' if high_critical_sites > 3 else 'warn'}"><div class="k">High-Critical Sites</div><div class="v">{high_critical_sites}</div><div class="d">Requires executive oversight</div></div>
            </div>
        """), unsafe_allow_html=True)

        ex_col1, ex_col2 = st.columns(2)
        with ex_col1:
            st.markdown('<div class="net-mini-title">Capacity Forecast by Corridor (30/60/90d)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cap_fcst = alt.Chart(net_capacity_forecast).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Horizon:N", title=None),
                    y=alt.Y("Projected Util %:Q", title="Projected Utilization (%)"),
                    color=alt.Color("Corridor:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444"])),
                    tooltip=["Corridor:N", "Horizon:N", alt.Tooltip("Projected Util %:Q", format=".0f")],
                )
                threshold = alt.Chart(pd.DataFrame({"y": [80]})).mark_rule(color="#94A3B8", strokeDash=[5, 4]).encode(y="y:Q")
                st.altair_chart(style_net_chart(threshold + cap_fcst, height=235), use_container_width=True)
                top_corridor = net_capacity_forecast.sort_values("Projected Util %", ascending=False).iloc[0]
                render_net_ai_reco(
                    "Capacity Forecast Alert",
                    f"{top_corridor['Corridor']} reaches {top_corridor['Projected Util %']:.0f}% in the {top_corridor['Horizon']} horizon.",
                    "Pre-authorize expansion capacity in this corridor before demand breaches operating thresholds.",
                    "Avoids saturation-driven quality degradation and emergency expansion costs.",
                    level="warning",
                )

        with ex_col2:
            st.markdown('<div class="net-mini-title">Change Risk Monitor</div>', unsafe_allow_html=True)
            with st.container(border=True):
                change_bar = alt.Chart(net_change_monitor).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=24, color="#93C5FD").encode(
                    x=alt.X("Week:N", title=None),
                    y=alt.Y("Planned Changes:Q", title="Planned Changes"),
                    tooltip=["Week:N", alt.Tooltip("Planned Changes:Q", format=".0f"), alt.Tooltip("Failed Changes:Q", format=".0f"), alt.Tooltip("Incidents:Q", format=".0f")],
                )
                inc_line = alt.Chart(net_change_monitor).mark_line(point=True, strokeWidth=2.8, color="#EF4444").encode(
                    x="Week:N", y=alt.Y("Incidents:Q", title="Incidents")
                )
                failed_line = alt.Chart(net_change_monitor).mark_line(point=True, strokeWidth=2.2, color="#F59E0B", strokeDash=[5, 3]).encode(
                    x="Week:N", y=alt.Y("Failed Changes:Q", title="Failed Changes")
                )
                st.altair_chart(style_net_chart(alt.layer(change_bar, inc_line, failed_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                riskiest_week = net_change_monitor.sort_values(["Failed Changes", "Incidents"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Change Governance",
                    f"{riskiest_week['Week']} shows the highest failed-change and incident concentration.",
                    "Apply stricter change windows, rollback readiness, and pre-deployment validation in high-risk periods.",
                    "Reduces change-induced incidents and improves release reliability.",
                    level="warning",
                )

        ex_col3, ex_col4 = st.columns(2)
        with ex_col3:
            st.markdown('<div class="net-mini-title">Mitigation Tracker (Progress vs Risk Reduced)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mit_bar = alt.Chart(net_mitigation_tracker).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=26, color="#3B82F6").encode(
                    x=alt.X("Initiative:N", sort="-y", title=None),
                    y=alt.Y("Progress %:Q", title="Progress (%)"),
                    tooltip=["Initiative:N", "Owner:N", "ETA:N", alt.Tooltip("Progress %:Q", format=".0f"), alt.Tooltip("Risk Reduced %:Q", format=".0f"), "Status:N"],
                )
                risk_line = alt.Chart(net_mitigation_tracker).mark_line(point=True, strokeWidth=2.8, color="#10B981").encode(
                    x=alt.X("Initiative:N", sort="-y"), y=alt.Y("Risk Reduced %:Q", title="Risk Reduced (%)")
                )
                st.altair_chart(style_net_chart(alt.layer(mit_bar, risk_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                lagging = net_mitigation_tracker.sort_values("Progress %").iloc[0]
                render_net_ai_reco(
                    "Execution Tracker",
                    f"{lagging['Initiative']} is the slowest initiative at {lagging['Progress %']:.0f}% completion.",
                    f"Escalate owner support for {lagging['Initiative']} to protect planned risk-reduction outcomes.",
                    "Improves delivery certainty for the resilience roadmap.",
                    level="warning",
                )

        with ex_col4:
            st.markdown('<div class="net-mini-title">Resilience Scorecard Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                res_long = net_resilience_score.melt("Month", var_name="Domain", value_name="Score")
                res_line = alt.Chart(res_long).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Score:Q", title="Resilience Score"),
                    color=alt.Color("Domain:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B"])),
                    tooltip=["Month:N", "Domain:N", alt.Tooltip("Score:Q", format=".0f")],
                )
                st.altair_chart(style_net_chart(res_line, height=235), use_container_width=True)
                latest_core = net_resilience_score.iloc[-1]["Core Score"]
                render_net_ai_reco(
                    "Resilience Trajectory",
                    f"Core resilience reaches {latest_core:.0f} in the latest month with broad upward trend across domains.",
                    "Sustain current program cadence and add targeted support to lagging field domains.",
                    "Builds durable reliability gains and improves crisis absorption capacity.",
                )

        st.markdown('<div class="net-mini-title">Top 10 Critical Sites and Scenario Playbooks</div>', unsafe_allow_html=True)
        ex_col5, ex_col6 = st.columns([1.4, 1.1])
        with ex_col5:
            with st.container(border=True):
                critical_view = net_critical_sites[["Site", "Region", "Criticality", "Subscribers Impact K", "MTTR Min", "Owner"]].sort_values("Criticality", ascending=False)
                st.dataframe(critical_view, use_container_width=True, hide_index=True)
                top_site = critical_view.iloc[0]
                render_net_ai_reco(
                    "Critical Site Governance",
                    f"{top_site['Site']} is currently the highest-criticality site with broad customer impact.",
                    "Assign weekly executive checkpoint on top critical sites with clear owner accountability.",
                    "Reduces probability of severe single-site service disruption.",
                    level="critical",
                )

        with ex_col6:
            with st.container(border=True):
                playbook = st.selectbox(
                    "Scenario Playbook",
                    ["Power Failure Cluster", "Backbone Fiber Cut", "Peak Congestion Event"],
                    index=0,
                    key="net_playbook_selector",
                )
                playbook_data = {
                    "Power Failure Cluster": {
                        "impact": "Availability -0.42pp, 18K subs impacted, ARR risk CLP 0.74M",
                        "actions": "Activate backup chain, dispatch power crews, prioritize enterprise circuits.",
                        "window": "First 90 minutes critical",
                    },
                    "Backbone Fiber Cut": {
                        "impact": "Latency +6.8ms, 24K subs impacted, ARR risk CLP 1.05M",
                        "actions": "Reroute traffic, trigger field splice teams, apply congestion controls.",
                        "window": "First 60 minutes critical",
                    },
                    "Peak Congestion Event": {
                        "impact": "Packet loss +0.14pp, NPS pressure in two regions",
                        "actions": "Traffic shaping, temporary capacity bump, proactive customer comms.",
                        "window": "First 45 minutes critical",
                    },
                }[playbook]
                st.markdown(dedent(f"""
                    <div class="net-ai-card warn" style="margin-top: 0.2rem;">
                        <div class="h">🧭 {playbook}</div>
                        <div class="b"><strong>Expected Impact:</strong> {playbook_data['impact']}</div>
                        <div class="b"><strong>Playbook Actions:</strong> {playbook_data['actions']}</div>
                        <div class="b"><strong>Response Window:</strong> {playbook_data['window']}</div>
                    </div>
                """), unsafe_allow_html=True)

    with net_tab_risk:
        st.markdown('<div class="net-title">Network Risk and Resilience Strategy</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card crit"><div class="k">Top Risk Driver</div><div class="v">{highest_risk['Risk Driver']}</div><div class="d">{highest_risk['Exposure Hr']:.0f} exposure hours</div></div>
                <div class="net-kpi-card warn"><div class="k">Risk Exposure</div><div class="v">{net_risk['Exposure Hr'].sum():.0f} h</div><div class="d">Total mapped exposure</div></div>
                <div class="net-kpi-card"><div class="k">Base Availability</div><div class="v">{net_scenario.loc[net_scenario['Scenario']=='Base', 'Availability %'].iloc[0]:.2f}%</div><div class="d">Most probable scenario</div></div>
                <div class="net-kpi-card"><div class="k">Upside Churn Save</div><div class="v">{net_scenario.loc[net_scenario['Scenario']=='Upside', 'Avoided Churn K'].iloc[0]:.1f}K</div><div class="d">Potential retained value</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="net-mini-title">Risk Exposure by Driver</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_bar = alt.Chart(net_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure Hr:Q", title="Exposure (hours)"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure Hr:Q", format=".0f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                risk_text = alt.Chart(net_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure Hr:Q", y=alt.Y("Risk Driver:N", sort="-x"), text=alt.Text("Exposure Hr:Q", format=".0f")
                )
                st.altair_chart(style_net_chart(risk_bar + risk_text, height=235), use_container_width=True)
                render_net_ai_reco(
                    "Risk Prioritization",
                    f"{highest_risk['Risk Driver']} has the highest exposure at {highest_risk['Exposure Hr']:.0f} hours.",
                    "Launch a focused resilience sprint for this driver with weekly board-level tracking.",
                    "Reduce service disruption probability in the highest-impact failure mode.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="net-mini-title">Resilience Scenario Outlook</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sc_bar = alt.Chart(net_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Availability %:Q", title="Availability (%)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Availability %:Q", format=".2f"), alt.Tooltip("Avoided Churn K:Q", format=".1f"), "Probability:N"],
                )
                sc_text = alt.Chart(net_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N", y="Availability %:Q", text=alt.Text("Availability %:Q", format=".2f")
                )
                st.altair_chart(style_net_chart(sc_bar + sc_text, height=235), use_container_width=True)
                base_av = net_scenario.loc[net_scenario["Scenario"] == "Base", "Availability %"].iloc[0]
                render_net_ai_reco(
                    "Scenario Planning",
                    f"Base case targets {base_av:.2f}% availability with clear upside through resilience investments.",
                    "Pre-approve downside playbooks and protect budget for targeted redundancy upgrades.",
                    "Improve forecast confidence and secure customer experience under volatility.",
                )

        rk_col3, rk_col4 = st.columns(2)
        with rk_col3:
            st.markdown('<div class="net-mini-title">Risk Heat Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_heat = alt.Chart(net_risk).mark_circle(opacity=0.86, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood"),
                    y=alt.Y("Exposure Hr:Q", title="Exposure (hours)"),
                    size=alt.Size("Exposure Hr:Q", scale=alt.Scale(range=[300, 1900]), legend=None),
                    color=alt.Color("Risk Driver:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#EF4444", "#F59E0B", "#3B82F6", "#10B981", "#6366F1"])),
                    tooltip=["Risk Driver:N", alt.Tooltip("Likelihood:Q", format=".1f"), alt.Tooltip("Exposure Hr:Q", format=".0f")],
                )
                risk_name = alt.Chart(net_risk).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q", y="Exposure Hr:Q", text="Risk Driver:N"
                )
                st.altair_chart(style_net_chart(risk_heat + risk_name, height=235), use_container_width=True)
                high_quadrant = net_risk.sort_values(["Likelihood", "Exposure Hr"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Risk Concentration",
                    f"{high_quadrant['Risk Driver']} is in the highest likelihood-exposure quadrant.",
                    "Escalate this risk into weekly executive review with pre-agreed containment triggers.",
                    "Cuts the probability of high-severity service disruption.",
                    level="critical",
                )

        with rk_col4:
            st.markdown('<div class="net-mini-title">Mitigation Value vs Cost</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mitigation_df = net_risk.copy()
                mitigation_df["Mitigation Cost K"] = (mitigation_df["Exposure Hr"] * 0.85).round(1)
                mitigation_df["Avoided Loss K"] = (mitigation_df["Exposure Hr"] * mitigation_df["Likelihood"] * 0.62).round(1)
                mitigation_df["ROI x"] = (mitigation_df["Avoided Loss K"] / mitigation_df["Mitigation Cost K"]).round(2)
                roi_bar = alt.Chart(mitigation_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#10B981").encode(
                    x=alt.X("Risk Driver:N", sort="-y", title=None),
                    y=alt.Y("ROI x:Q", title="Mitigation ROI (x)"),
                    tooltip=["Risk Driver:N", alt.Tooltip("ROI x:Q", format=".2f"), alt.Tooltip("Mitigation Cost K:Q", format=".1f"), alt.Tooltip("Avoided Loss K:Q", format=".1f")],
                )
                roi_target = alt.Chart(pd.DataFrame({"y": [1.3]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                roi_text = alt.Chart(mitigation_df).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Risk Driver:N", sort="-y"),
                    y="ROI x:Q",
                    text=alt.Text("ROI x:Q", format=".2f"),
                )
                st.altair_chart(style_net_chart(roi_target + roi_bar + roi_text, height=235), use_container_width=True)
                top_roi = mitigation_df.loc[mitigation_df["ROI x"].idxmax()]
                render_net_ai_reco(
                    "Mitigation Capital Allocation",
                    f"{top_roi['Risk Driver']} shows the strongest mitigation ROI at {top_roi['ROI x']:.2f}x.",
                    f"Prioritize budget release for {top_roi['Risk Driver']} and phase lower-ROI initiatives.",
                    "Increases resilience returns per unit of mitigation spend.",
                )

        st.markdown('<div class="net-title">Infrastructure Risk Exposure</div>', unsafe_allow_html=True)
        rk_inf_col1, rk_inf_col2 = st.columns(2)
        with rk_inf_col1:
            st.markdown('<div class="net-mini-title">Single Points of Failure by Region</div>', unsafe_allow_html=True)
            with st.container(border=True):
                spof_bar = alt.Chart(net_spof).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("SPOF Count:Q", title="Single Points of Failure"),
                    y=alt.Y("Region:N", sort="-x", title=None),
                    color=alt.Color("Criticality:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Criticality")),
                    tooltip=["Region:N", alt.Tooltip("SPOF Count:Q", format=".0f"), alt.Tooltip("Subscribers K:Q", format=".0f"), alt.Tooltip("Criticality:Q", format=".1f")],
                )
                spof_text = alt.Chart(net_spof).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="SPOF Count:Q", y=alt.Y("Region:N", sort="-x"), text=alt.Text("Subscribers K:Q", format=".0f")
                )
                st.altair_chart(style_net_chart(spof_bar + spof_text, height=235), use_container_width=True)
                top_spof = net_spof.loc[net_spof["SPOF Count"].idxmax()]
                render_net_ai_reco(
                    "SPOF Exposure",
                    f"{top_spof['Region']} has the highest single-point-of-failure count with high customer impact potential.",
                    f"Deploy redundancy projects in {top_spof['Region']} and sequence high-risk circuits first.",
                    "Lowers catastrophic outage probability and protects subscriber experience.",
                    level="critical",
                )

        with rk_inf_col2:
            st.markdown('<div class="net-mini-title">Backup Autonomy vs Power Instability</div>', unsafe_allow_html=True)
            with st.container(border=True):
                power_scatter = alt.Chart(net_resilience_sites).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Backup Autonomy Hr:Q", title="Backup Autonomy (hours)"),
                    y=alt.Y("Power Events / Mo:Q", title="Power Events / Month"),
                    size=alt.Size("Critical Sites:Q", scale=alt.Scale(range=[260, 1400]), legend=None),
                    color=alt.Color("Region:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                    tooltip=["Region:N", alt.Tooltip("Backup Autonomy Hr:Q", format=".1f"), alt.Tooltip("Power Events / Mo:Q", format=".1f"), alt.Tooltip("Critical Sites:Q", format=".0f")],
                )
                power_label = alt.Chart(net_resilience_sites).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Backup Autonomy Hr:Q", y="Power Events / Mo:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(power_scatter + power_label, height=235), use_container_width=True)
                weakest_power = net_resilience_sites.sort_values(["Backup Autonomy Hr", "Power Events / Mo"], ascending=[True, False]).iloc[0]
                render_net_ai_reco(
                    "Power Resilience Priority",
                    f"{weakest_power['Region']} has the weakest backup autonomy under high power-event volatility.",
                    f"Increase backup autonomy and power hardening at critical sites in {weakest_power['Region']}.",
                    "Strengthens continuity for infrastructure nodes exposed to utility instability.",
                    level="warning",
                )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {highest_risk['Risk Driver']} at {highest_risk['Exposure Hr']:.0f} exposure hours</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Most vulnerable region: {weakest_region['Region']} ({weakest_region['Availability %']:.2f}% uptime) · execute mitigation in next operating cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "Marketing":
    import pandas as pd
    import altair as alt

    MKT_CHART_THEME = {
        "bg": "#F8FAFF",
        "title": "#1E3A8A",
        "axis": "#334155",
        "grid": "#E2E8F0",
        "font": "Inter",
    }

    def style_mkt_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 10, "right": 10, "top": 8, "bottom": 4})
            .configure(background=MKT_CHART_THEME["bg"])
            .configure_view(stroke=None, cornerRadius=10)
            .configure_title(color=MKT_CHART_THEME["title"], fontSize=13, font=MKT_CHART_THEME["font"], anchor="start")
            .configure_axis(
                labelColor=MKT_CHART_THEME["axis"],
                titleColor=MKT_CHART_THEME["axis"],
                gridColor=MKT_CHART_THEME["grid"],
                labelFont=MKT_CHART_THEME["font"],
                titleFont=MKT_CHART_THEME["font"],
            )
            .configure_legend(
                labelColor=MKT_CHART_THEME["axis"],
                titleColor=MKT_CHART_THEME["axis"],
                labelFont=MKT_CHART_THEME["font"],
                titleFont=MKT_CHART_THEME["font"],
            )
        )

    def render_mkt_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        level_class = "crit" if level == "critical" else "warn" if level == "warning" else ""
        icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "🤖"
        st.markdown(dedent(f"""
            <div class="mkt-ai-card {level_class}">
                <div class="h">{icon} {headline}</div>
                <div class="b"><strong>Insight:</strong> {insight}</div>
                <div class="b"><strong>Action:</strong> {action}</div>
                <div class="b"><strong>Expected Impact:</strong> {impact}</div>
            </div>
        """), unsafe_allow_html=True)

    st.markdown(dedent("""
        <style>
            @keyframes mkt-fade-up {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes mkt-pulse-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.1); }
                50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.03); }
            }
            .mkt-title {
                font-size: 1.08rem;
                font-weight: 800;
                color: #1E3A8A;
                letter-spacing: 0.01em;
                margin: 0.3rem 0 0.6rem 0;
                animation: mkt-fade-up 0.45s ease-out both;
            }
            .mkt-mini-title {
                font-size: 0.92rem;
                font-weight: 700;
                color: #334155;
                margin: 0.12rem 0 0.5rem 0;
                animation: mkt-fade-up 0.45s ease-out both;
            }
            .mkt-pulse {
                border-radius: 12px;
                border: 1px solid #DBEAFE;
                background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
                padding: 0.8rem 0.95rem;
                margin-bottom: 0.65rem;
                animation: mkt-fade-up 0.45s ease-out both, mkt-pulse-glow 2.8s ease-in-out infinite;
            }
            .mkt-pulse-grid, .mkt-kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.48rem;
            }
            .mkt-pulse-card, .mkt-kpi-card {
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #E2E8F0;
                padding: 0.52rem 0.62rem;
            }
            .mkt-pulse-card .k, .mkt-kpi-card .k {
                font-size: 0.69rem;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                font-weight: 700;
            }
            .mkt-pulse-card .v, .mkt-kpi-card .v {
                font-size: 1.04rem;
                color: #0F172A;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.08rem;
            }
            .mkt-pulse-card .d, .mkt-kpi-card .d {
                font-size: 0.74rem;
                color: #475569;
                margin-top: 0.12rem;
            }
            .mkt-kpi-card.warn { border-left: 4px solid #F59E0B; }
            .mkt-kpi-card.crit { border-left: 4px solid #EF4444; }
            .mkt-ai-card {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
                background: #EFF6FF;
                padding: 0.62rem 0.72rem;
                margin-top: 0.46rem;
                animation: mkt-fade-up 0.42s ease-out both;
            }
            .mkt-ai-card.warn { border-left-color: #F59E0B; background: #FFFBEB; }
            .mkt-ai-card.crit { border-left-color: #EF4444; background: #FEF2F2; }
            .mkt-ai-card .h {
                font-size: 0.83rem;
                font-weight: 800;
                color: #1E293B;
                margin-bottom: 0.28rem;
            }
            .mkt-ai-card .b {
                font-size: 0.78rem;
                color: #334155;
                line-height: 1.42;
            }
            @media (max-width: 1200px) {
                .mkt-pulse-grid, .mkt-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
        </style>
    """), unsafe_allow_html=True)

    mkt_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Spend M": [0.38, 0.40, 0.43, 0.45, 0.47, 0.49],
        "Leads K": [3.8, 4.0, 4.2, 4.5, 4.7, 5.0],
        "MQL K": [1.9, 2.0, 2.2, 2.4, 2.5, 2.7],
        "SQL K": [0.82, 0.88, 0.95, 1.03, 1.10, 1.18],
        "New Subs K": [0.28, 0.31, 0.34, 0.37, 0.40, 0.43],
        "Pipeline M": [1.6, 1.7, 1.9, 2.1, 2.3, 2.5],
        "Revenue M": [0.58, 0.63, 0.69, 0.76, 0.84, 0.92],
    })
    mkt_channels = pd.DataFrame({
        "Channel": ["WOM Google Ads", "WOM Meta/Social", "WOM SEO Orgánico", "WOM Afiliados", "WOM Tiendas", "WOM CRM/Email"],
        "Spend M": [0.72, 0.52, 0.42, 0.38, 0.56, 0.42],
        "Leads K": [9.4, 7.8, 5.2, 4.4, 4.8, 3.2],
        "New Subs K": [0.62, 0.48, 0.38, 0.34, 0.42, 0.28],
        "Revenue M": [1.58, 1.12, 0.92, 0.78, 1.24, 0.74],
        "Product Focus": ["Móvil+Fibra", "Móvil", "Fibra Hogar", "Móvil", "Todos", "Retención"],
    })
    mkt_channels["CAC"] = (mkt_channels["Spend M"] * 1_000_000 / (mkt_channels["New Subs K"] * 1_000)).round(0)
    mkt_channels["CVR %"] = (mkt_channels["New Subs K"] / mkt_channels["Leads K"] * 100).round(1)
    mkt_channels["ROAS"] = (mkt_channels["Revenue M"] / mkt_channels["Spend M"]).round(2)

    mkt_campaigns = pd.DataFrame({
        "Campaign": ["WOM Fibra 600 Mbps", "WOM Vuelta a Clases", "WOM Empresas 5G", "WOM Referidos Móvil", "WOM Winback Fibra", "WOM Upgrade Plan"],
        "Stage": ["Adquisición Fibra", "Adquisición Móvil", "B2B", "Referidos", "Retención", "Upsell"],
        "Spend M": [0.42, 0.38, 0.44, 0.32, 0.26, 0.24],
        "Clicks K": [92, 84, 76, 62, 54, 48],
        "Leads K": [5.8, 5.4, 4.8, 4.2, 3.4, 3.0],
        "Revenue M": [1.12, 0.98, 1.14, 0.82, 0.64, 0.58],
        "Product": ["Fibra Hogar", "Móvil Prepago", "Móvil Empresa", "Móvil", "Fibra", "Móvil+Fibra"],
    })
    mkt_campaigns["CTR %"] = (mkt_campaigns["Clicks K"] / 4_600 * 100).round(2)
    mkt_campaigns["CVR %"] = (mkt_campaigns["Leads K"] / mkt_campaigns["Clicks K"] * 100).round(2)
    mkt_campaigns["CPA"] = (mkt_campaigns["Spend M"] * 1_000_000 / (mkt_campaigns["Leads K"] * 1_000)).round(0)
    mkt_campaigns["ROI %"] = ((mkt_campaigns["Revenue M"] - mkt_campaigns["Spend M"]) / mkt_campaigns["Spend M"] * 100).round(1)

    mkt_funnel = pd.DataFrame({
        "Stage": ["Visitas Web", "Leads", "MQL", "SQL", "Wins"],
        "Volume K": [340, mkt_monthly.iloc[-1]["Leads K"], mkt_monthly.iloc[-1]["MQL K"], mkt_monthly.iloc[-1]["SQL K"], mkt_monthly.iloc[-1]["New Subs K"]],
    })
    mkt_funnel["Conversion %"] = (mkt_funnel["Volume K"] / mkt_funnel["Volume K"].shift(1) * 100).round(1)
    mkt_funnel.loc[0, "Conversion %"] = 100.0

    mkt_risk = pd.DataFrame({
        "Risk Driver": ["Inflación CAC Canales", "Puntos Ciegos Atribución", "Volatilidad Leads Partners", "Fatiga Creativa", "Delay Compliance"],
        "Exposure M": [1.52, 1.24, 1.08, 0.92, 0.64],
        "Likelihood": [4.0, 3.5, 3.3, 3.2, 2.7],
    })
    mkt_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Quarter Revenue M": [2.2, 2.5, 2.9],
        "New Subs K": [1.9, 2.2, 2.5],
        "Probability": ["25%", "50%", "25%"],
    })

    total_spend_m = mkt_monthly["Spend M"].sum()
    total_revenue_m = mkt_monthly["Revenue M"].sum()
    blended_roas = total_revenue_m / total_spend_m
    total_new_subs_k = mkt_monthly["New Subs K"].sum()
    blended_cac = total_spend_m * 1_000_000 / (total_new_subs_k * 1_000)
    lead_to_mql = mkt_monthly["MQL K"].sum() / mkt_monthly["Leads K"].sum()
    sql_to_win = mkt_monthly["New Subs K"].sum() / mkt_monthly["SQL K"].sum()
    pipeline_latest = mkt_monthly.iloc[-1]["Pipeline M"]
    revenue_growth = (mkt_monthly.iloc[-1]["Revenue M"] / mkt_monthly.iloc[0]["Revenue M"] - 1) * 100
    top_risk_mkt = mkt_risk.loc[mkt_risk["Exposure M"].idxmax()]

    st.markdown('<div class="mkt-title">WOM Marketing Pulse - Rendimiento Campañas</div>', unsafe_allow_html=True)
    st.markdown(dedent(f"""
        <div class="mkt-pulse">
            <div class="mkt-pulse-grid">
                <div class="mkt-pulse-card"><div class="k">Revenue Influenciado</div><div class="v">CLP {total_revenue_m:.2f}M</div><div class="d">Revenue atribuible 6 meses</div></div>
                <div class="mkt-pulse-card"><div class="k">Pipeline</div><div class="v">CLP {pipeline_latest:.2f}M</div><div class="d">Pipeline último mes</div></div>
                <div class="mkt-pulse-card"><div class="k">ROAS Blended</div><div class="v">{blended_roas:.2f}x</div><div class="d">Revenue por CLP invertido</div></div>
                <div class="mkt-pulse-card"><div class="k">CAC Blended</div><div class="v">CLP {blended_cac:,.0f}</div><div class="d">Eficiencia adquisición</div></div>
                <div class="mkt-pulse-card"><div class="k">Lead → MQL</div><div class="v">{lead_to_mql:.1%}</div><div class="d">Calidad calificación</div></div>
                <div class="mkt-pulse-card"><div class="k">Crecimiento Revenue</div><div class="v">{revenue_growth:+.1f}%</div><div class="d">Trayectoria 6 meses</div></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    mkt_tab_overview, mkt_tab_ops, mkt_tab_channels, mkt_tab_risk = st.tabs([
        "📈 Vista General Marketing",
        "🧭 Operaciones & Funnel",
        "📱 Canales & Productos",
        "⚠️ Riesgo & Estrategia",
    ])

    with mkt_tab_overview:
        st.markdown('<div class="mkt-title">Rendimiento Marketing WOM</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card"><div class="k">Inversión Total</div><div class="v">CLP {total_spend_m:.2f}M</div><div class="d">Inversión 6 meses</div></div>
                <div class="mkt-kpi-card"><div class="k">Nuevos Suscriptores</div><div class="v">{total_new_subs_k:.1f}K</div><div class="d">Wins driven by marketing</div></div>
                <div class="mkt-kpi-card {'warn' if blended_cac > 140 else ''}"><div class="k">CAC Blended</div><div class="v">CLP {blended_cac:,.0f}</div><div class="d">Benchmark eficiencia</div></div>
                <div class="mkt-kpi-card"><div class="k">SQL a Win</div><div class="v">{sql_to_win:.1%}</div><div class="d">Calidad conversión ventas</div></div>
            </div>
        """), unsafe_allow_html=True)

        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="mkt-mini-title">Tendencia Inversión y Revenue</div>', unsafe_allow_html=True)
            with st.container(border=True):
                spend_bar = alt.Chart(mkt_monthly).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=34, color="#93C5FD").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Spend M:Q", title="Spend (CLP  M)"),
                    tooltip=["Month:N", alt.Tooltip("Spend M:Q", format=".2f"), alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("New Subs K:Q", format=".1f")],
                )
                rev_line = alt.Chart(mkt_monthly).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x="Month:N",
                    y=alt.Y("Revenue M:Q", title="Revenue (CLP  M)"),
                )
                st.altair_chart(style_mkt_chart(alt.layer(spend_bar, rev_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Investment Efficiency",
                    f"Revenue trend outpaces spend growth, delivering blended ROAS of {blended_roas:.2f}x.",
                    "Sustain high-performing campaign mix and shift budget away from low-ROI cohorts.",
                    "Improves marginal returns while preserving volume growth.",
                )

        with ov_col2:
            st.markdown('<div class="mkt-mini-title">Matriz Eficiencia Canales</div>', unsafe_allow_html=True)
            with st.container(border=True):
                ch_scatter = alt.Chart(mkt_channels).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("CAC:Q", title="CAC (CLP )"),
                    y=alt.Y("CVR %:Q", title="Conversion (%)"),
                    size=alt.Size("Spend M:Q", scale=alt.Scale(range=[260, 1500]), legend=None),
                    color=alt.Color("ROAS:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="ROAS")),
                    tooltip=["Channel:N", alt.Tooltip("CAC:Q", format=".0f"), alt.Tooltip("CVR %:Q", format=".1f"), alt.Tooltip("ROAS:Q", format=".2f"), alt.Tooltip("Spend M:Q", format=".2f")],
                )
                ch_label = alt.Chart(mkt_channels).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="CAC:Q", y="CVR %:Q", text="Channel:N"
                )
                st.altair_chart(style_mkt_chart(ch_scatter + ch_label, height=235), use_container_width=True)
                best_channel = mkt_channels.sort_values(["ROAS", "CVR %"], ascending=False).iloc[0]
                render_mkt_ai_reco(
                    "Channel Prioritization",
                    f"{best_channel['Channel']} is currently the strongest efficiency channel with ROAS {best_channel['ROAS']:.2f}x.",
                    f"Increase budget elasticity for {best_channel['Channel']} while capping high-CAC channels.",
                    "Raises qualified volume with controlled acquisition cost inflation.",
                )

        ov_col3, ov_col4 = st.columns(2)
        with ov_col3:
            st.markdown('<div class="mkt-mini-title">Momentum Leads y Pipeline</div>', unsafe_allow_html=True)
            with st.container(border=True):
                lead_line = alt.Chart(mkt_monthly).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Leads K:Q", title="Leads (K)"),
                    tooltip=["Month:N", alt.Tooltip("Leads K:Q", format=".1f"), alt.Tooltip("MQL K:Q", format=".1f"), alt.Tooltip("Pipeline M:Q", format=".2f")],
                )
                pipe_line = alt.Chart(mkt_monthly).mark_line(point=True, strokeWidth=2.8, color="#10B981").encode(
                    x="Month:N",
                    y=alt.Y("Pipeline M:Q", title="Pipeline (CLP  M)"),
                )
                st.altair_chart(style_mkt_chart(alt.layer(lead_line, pipe_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                pipeline_growth = (mkt_monthly.iloc[-1]["Pipeline M"] / mkt_monthly.iloc[0]["Pipeline M"] - 1) * 100
                render_mkt_ai_reco(
                    "Demand Momentum",
                    f"Pipeline expanded {pipeline_growth:.1f}% across the period with steady lead growth.",
                    "Reinforce high-intent nurture flows to protect lead quality while scaling volume.",
                    "Supports durable top-funnel growth and stronger quarter-close confidence.",
                )

        with ov_col4:
            st.markdown('<div class="mkt-mini-title">ROAS por Canal</div>', unsafe_allow_html=True)
            with st.container(border=True):
                roas_bar = alt.Chart(mkt_channels).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=26).encode(
                    x=alt.X("Channel:N", sort="-y", title=None),
                    y=alt.Y("ROAS:Q", title="ROAS (x)"),
                    color=alt.Color("ROAS:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Channel:N", alt.Tooltip("ROAS:Q", format=".2f"), alt.Tooltip("Spend M:Q", format=".2f"), alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("CAC:Q", format=".0f")],
                )
                roas_target = alt.Chart(pd.DataFrame({"y": [3.0]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                roas_text = alt.Chart(mkt_channels).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Channel:N", sort="-y"),
                    y="ROAS:Q",
                    text=alt.Text("ROAS:Q", format=".2f"),
                )
                st.altair_chart(style_mkt_chart(roas_target + roas_bar + roas_text, height=235), use_container_width=True)
                low_roas = mkt_channels.loc[mkt_channels["ROAS"].idxmin()]
                render_mkt_ai_reco(
                    "Channel Return Mix",
                    f"{low_roas['Channel']} is the lowest-return channel at {low_roas['ROAS']:.2f}x.",
                    f"Refine targeting and creative on {low_roas['Channel']} before additional spend increases.",
                    "Lifts blended ROAS and protects marketing efficiency under scale.",
                    level="warning",
                )

    with mkt_tab_ops:
        st.markdown('<div class="mkt-title">Operaciones Marketing y Journey Cliente</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card"><div class="k">Base Leads Funnel Actual</div><div class="v">{mkt_funnel.loc[mkt_funnel['Stage']=='Leads', 'Volume K'].iloc[0]:.0f}K</div><div class="d">Demanda último mes</div></div>
                <div class="mkt-kpi-card {'warn' if mkt_funnel.loc[mkt_funnel['Stage']=='SQL', 'Conversion %'].iloc[0] < 55 else ''}"><div class="k">MQL → SQL</div><div class="v">{mkt_funnel.loc[mkt_funnel['Stage']=='SQL', 'Conversion %'].iloc[0]:.1f}%</div><div class="d">Conversión mid-funnel</div></div>
                <div class="mkt-kpi-card"><div class="k">Mejor ROI Campaña</div><div class="v">{mkt_campaigns['ROI %'].max():.0f}%</div><div class="d">Top performer portafolio</div></div>
                <div class="mkt-kpi-card"><div class="k">Mix Campañas</div><div class="v">{mkt_campaigns['Campaign'].nunique()}</div><div class="d">Iniciativas activas</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="mkt-mini-title">Conversión Funnel por Etapa</div>', unsafe_allow_html=True)
            with st.container(border=True):
                funnel_bar = alt.Chart(mkt_funnel).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=24).encode(
                    x=alt.X("Volume K:Q", title="Volumen (K)"),
                    y=alt.Y("Stage:N", sort=["Visitas Web", "Leads", "MQL", "SQL", "Wins"], title=None),
                    color=alt.Color("Conversion %:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Stage:N", alt.Tooltip("Volume K:Q", format=".1f"), alt.Tooltip("Conversion %:Q", format=".1f")],
                )
                funnel_label = alt.Chart(mkt_funnel).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Volume K:Q", y=alt.Y("Stage:N", sort=["Visitas Web", "Leads", "MQL", "SQL", "Wins"]), text=alt.Text("Conversion %:Q", format=".1f")
                )
                st.altair_chart(style_mkt_chart(funnel_bar + funnel_label, height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Funnel Health",
                    f"Lead-to-win conversion currently lands at {mkt_funnel.loc[mkt_funnel['Stage']=='Wins', 'Conversion %'].iloc[0]:.1f}% from SQL stage.",
                    "Tighten scoring model and sales handoff SLAs at MQL and SQL transition points.",
                    "Improves yield from acquired demand without proportional spend increase.",
                    level="warning",
                )

        with op_col2:
            st.markdown('<div class="mkt-mini-title">Portafolio ROI Campañas</div>', unsafe_allow_html=True)
            with st.container(border=True):
                camp_bar = alt.Chart(mkt_campaigns).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#60A5FA").encode(
                    x=alt.X("Campaign:N", sort="-y", title=None),
                    y=alt.Y("ROI %:Q", title="ROI (%)"),
                    tooltip=["Campaign:N", "Stage:N", alt.Tooltip("ROI %:Q", format=".1f"), alt.Tooltip("Spend M:Q", format=".2f"), alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("CPA:Q", format=".0f")],
                )
                roi_target = alt.Chart(pd.DataFrame({"y": [180]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                st.altair_chart(style_mkt_chart(roi_target + camp_bar, height=235), use_container_width=True)
                top_campaign = mkt_campaigns.loc[mkt_campaigns["ROI %"].idxmax()]
                render_mkt_ai_reco(
                    "Campaign Optimization",
                    f"{top_campaign['Campaign']} leads portfolio ROI at {top_campaign['ROI %']:.1f}%.",
                    f"Scale creative and audience variants from {top_campaign['Campaign']} into adjacent segments.",
                    "Improves campaign-level return while keeping execution risk low.",
                )

        st.markdown('<div class="mkt-mini-title">Mix Atribución por Revenue Canal</div>', unsafe_allow_html=True)
        with st.container(border=True):
            mix_df = mkt_channels.copy()
            mix_df["Revenue Share %"] = (mix_df["Revenue M"] / mix_df["Revenue M"].sum() * 100).round(1)
            mix_arc = alt.Chart(mix_df).mark_arc(innerRadius=64, outerRadius=102).encode(
                theta=alt.Theta("Revenue M:Q"),
                color=alt.Color("Channel:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                tooltip=["Channel:N", alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("Revenue Share %:Q", format=".1f"), alt.Tooltip("ROAS:Q", format=".2f")],
            )
            center_txt = alt.Chart(pd.DataFrame({"t": [f"{mix_df['Revenue Share %'].max():.1f}%"]})).mark_text(fontSize=22, fontWeight="bold", color="#0F172A").encode(text="t:N")
            center_sub = alt.Chart(pd.DataFrame({"t": ["Top Share"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
            st.altair_chart(style_mkt_chart(mix_arc + center_txt + center_sub, height=235), use_container_width=True)
            dominant_channel = mix_df.loc[mix_df["Revenue Share %"].idxmax()]
            render_mkt_ai_reco(
                "Attribution Concentration",
                f"{dominant_channel['Channel']} contributes the largest revenue share at {dominant_channel['Revenue Share %']:.1f}%.",
                "Maintain diversification guardrails to avoid dependency on a single channel.",
                "Protects growth resilience under channel volatility.",
                level="warning",
            )

        st.markdown('<div class="mkt-mini-title">Matriz Calidad Campañas (CTR vs CVR)</div>', unsafe_allow_html=True)
        with st.container(border=True):
            camp_matrix = alt.Chart(mkt_campaigns).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                x=alt.X("CTR %:Q", title="CTR (%)"),
                y=alt.Y("CVR %:Q", title="CVR (%)"),
                size=alt.Size("Spend M:Q", scale=alt.Scale(range=[260, 1600]), legend=None),
                color=alt.Color("ROI %:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="ROI %")),
                tooltip=["Campaign:N", "Stage:N", alt.Tooltip("CTR %:Q", format=".2f"), alt.Tooltip("CVR %:Q", format=".2f"), alt.Tooltip("CPA:Q", format=".0f"), alt.Tooltip("ROI %:Q", format=".1f")],
            )
            camp_label = alt.Chart(mkt_campaigns).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                x="CTR %:Q", y="CVR %:Q", text="Campaign:N"
            )
            st.altair_chart(style_mkt_chart(camp_matrix + camp_label, height=235), use_container_width=True)
            weak_creative = mkt_campaigns.sort_values(["CTR %", "ROI %"]).iloc[0]
            render_mkt_ai_reco(
                "Creative and Targeting Quality",
                f"{weak_creative['Campaign']} shows the weakest CTR/ROI combination in the active mix.",
                f"Refresh creative and audience segmentation strategy for {weak_creative['Campaign']}.",
                "Improves campaign quality and reduces inefficient spend pockets.",
                level="warning",
            )

    with mkt_tab_channels:
        st.markdown('<div class="mkt-title">Canales & Productos WOM</div>', unsafe_allow_html=True)
        
        mkt_products = pd.DataFrame({
            "Producto": ["Móvil Prepago", "Móvil Postpago", "Fibra Hogar 300", "Fibra Hogar 600", "Combo Móvil+Fibra", "WOM Empresas"],
            "Leads K": [4.2, 3.8, 2.4, 2.8, 1.8, 1.6],
            "Conversión %": [8.2, 12.4, 18.6, 22.4, 28.2, 15.8],
            "Revenue M": [0.86, 1.24, 0.78, 1.12, 1.48, 0.92],
            "ARPU CLP": [8500, 18500, 22000, 32000, 42000, 68000],
        })
        mkt_products["CAC"] = ((mkt_products["Leads K"] * 1000 * 0.12) / (mkt_products["Leads K"] * mkt_products["Conversión %"] / 100)).round(0)
        
        mkt_regions_mkt = pd.DataFrame({
            "Región": ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "O'Higgins", "Antofagasta"],
            "Leads K": [12.4, 4.2, 3.6, 2.4, 1.8, 1.6],
            "Conversión %": [14.2, 12.8, 11.6, 10.4, 11.2, 9.8],
            "Top Producto": ["Móvil Postpago", "Fibra 600", "Móvil Prepago", "Combo", "Fibra 300", "Móvil Prepago"],
            "Revenue M": [3.24, 1.12, 0.94, 0.68, 0.52, 0.48],
        })
        
        total_product_rev = mkt_products["Revenue M"].sum()
        top_product = mkt_products.loc[mkt_products["Revenue M"].idxmax()]
        avg_conversion = mkt_products["Conversión %"].mean()
        
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card"><div class="k">Revenue Productos</div><div class="v">CLP {total_product_rev:.2f}M</div><div class="d">Total mix productos</div></div>
                <div class="mkt-kpi-card"><div class="k">Top Producto</div><div class="v">{top_product['Producto']}</div><div class="d">CLP {top_product['Revenue M']:.2f}M revenue</div></div>
                <div class="mkt-kpi-card"><div class="k">Conversión Promedio</div><div class="v">{avg_conversion:.1f}%</div><div class="d">Across all products</div></div>
                <div class="mkt-kpi-card"><div class="k">Mejor ARPU</div><div class="v">CLP {mkt_products['ARPU CLP'].max():,.0f}</div><div class="d">{mkt_products.loc[mkt_products['ARPU CLP'].idxmax(), 'Producto']}</div></div>
            </div>
        """), unsafe_allow_html=True)
        
        ch_col1, ch_col2 = st.columns(2)
        with ch_col1:
            st.markdown('<div class="mkt-mini-title">Performance por Producto WOM</div>', unsafe_allow_html=True)
            with st.container(border=True):
                prod_bar = alt.Chart(mkt_products).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=22).encode(
                    x=alt.X("Producto:N", sort="-y", title=None),
                    y=alt.Y("Revenue M:Q", title="Revenue (CLP M)"),
                    color=alt.Color("Conversión %:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Producto:N", alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("Conversión %:Q", format=".1f"), alt.Tooltip("ARPU CLP:Q", format=",.0f")],
                )
                prod_txt = alt.Chart(mkt_products).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Producto:N", sort="-y"),
                    y="Revenue M:Q",
                    text=alt.Text("Revenue M:Q", format=".2f"),
                )
                st.altair_chart(style_mkt_chart(prod_bar + prod_txt, height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Mix Productos",
                    f"{top_product['Producto']} lidera revenue con CLP {top_product['Revenue M']:.2f}M y conversión {top_product['Conversión %']:.1f}%.",
                    "Escalar inversión en productos de alta conversión, optimizar funnel en productos bajo rendimiento.",
                    "Mejora mix de revenue y lifetime value del portafolio.",
                )
        
        with ch_col2:
            st.markdown('<div class="mkt-mini-title">Conversión vs CAC por Producto</div>', unsafe_allow_html=True)
            with st.container(border=True):
                prod_scatter = alt.Chart(mkt_products).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("CAC:Q", title="CAC (CLP)"),
                    y=alt.Y("Conversión %:Q", title="Conversión (%)"),
                    size=alt.Size("Revenue M:Q", scale=alt.Scale(range=[200, 1200]), legend=None),
                    color=alt.Color("ARPU CLP:Q", scale=alt.Scale(scheme="greens"), legend=alt.Legend(title="ARPU")),
                    tooltip=["Producto:N", alt.Tooltip("CAC:Q", format=",.0f"), alt.Tooltip("Conversión %:Q", format=".1f"), alt.Tooltip("ARPU CLP:Q", format=",.0f")],
                )
                prod_lbl = alt.Chart(mkt_products).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                    x="CAC:Q", y="Conversión %:Q", text="Producto:N"
                )
                st.altair_chart(style_mkt_chart(prod_scatter + prod_lbl, height=235), use_container_width=True)
                best_efficiency = mkt_products.sort_values(["Conversión %"], ascending=False).iloc[0]
                render_mkt_ai_reco(
                    "Eficiencia Adquisición",
                    f"{best_efficiency['Producto']} tiene mejor ratio conversión/CAC con {best_efficiency['Conversión %']:.1f}% CVR.",
                    "Replicar estrategia de adquisición de productos eficientes en categorías similares.",
                    "Reduce CAC blended manteniendo volumen de leads.",
                )
        
        st.markdown('<div class="mkt-mini-title">Performance Marketing por Región Chile</div>', unsafe_allow_html=True)
        with st.container(border=True):
            region_bar = alt.Chart(mkt_regions_mkt).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=32).encode(
                x=alt.X("Región:N", sort="-y", title=None),
                y=alt.Y("Revenue M:Q", title="Revenue (CLP M)"),
                color=alt.Color("Conversión %:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="CVR %")),
                tooltip=["Región:N", alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("Leads K:Q", format=".1f"), alt.Tooltip("Conversión %:Q", format=".1f"), "Top Producto:N"],
            )
            region_txt = alt.Chart(mkt_regions_mkt).mark_text(dy=-8, fontSize=10, color="#0F172A").encode(
                x=alt.X("Región:N", sort="-y"),
                y="Revenue M:Q",
                text=alt.Text("Revenue M:Q", format=".2f"),
            )
            st.altair_chart(style_mkt_chart(region_bar + region_txt, height=220), use_container_width=True)
            top_region = mkt_regions_mkt.loc[mkt_regions_mkt["Revenue M"].idxmax()]
            render_mkt_ai_reco(
                "Concentración Regional",
                f"Región {top_region['Región']} genera CLP {top_region['Revenue M']:.2f}M con {top_region['Conversión %']:.1f}% conversión.",
                "Expandir campañas localizadas en regiones de alto potencial con bajo share actual.",
                "Diversifica revenue geográfico y reduce dependencia de RM.",
            )
        
        ch_col3, ch_col4 = st.columns(2)
        with ch_col3:
            st.markdown('<div class="mkt-mini-title">ARPU por Producto</div>', unsafe_allow_html=True)
            with st.container(border=True):
                arpu_bar = alt.Chart(mkt_products).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("ARPU CLP:Q", title="ARPU (CLP)"),
                    y=alt.Y("Producto:N", sort="-x", title=None),
                    color=alt.Color("ARPU CLP:Q", scale=alt.Scale(scheme="greens"), legend=None),
                    tooltip=["Producto:N", alt.Tooltip("ARPU CLP:Q", format=",.0f"), alt.Tooltip("Revenue M:Q", format=".2f")],
                )
                arpu_txt = alt.Chart(mkt_products).mark_text(align="left", dx=6, fontSize=9, color="#0F172A").encode(
                    x="ARPU CLP:Q", y=alt.Y("Producto:N", sort="-x"), text=alt.Text("ARPU CLP:Q", format=",.0f")
                )
                st.altair_chart(style_mkt_chart(arpu_bar + arpu_txt, height=220), use_container_width=True)
        
        with ch_col4:
            st.markdown('<div class="mkt-mini-title">Share Revenue por Canal</div>', unsafe_allow_html=True)
            with st.container(border=True):
                channel_share = mkt_channels.copy()
                channel_share["Share %"] = (channel_share["Revenue M"] / channel_share["Revenue M"].sum() * 100).round(1)
                ch_arc = alt.Chart(channel_share).mark_arc(innerRadius=58, outerRadius=95).encode(
                    theta=alt.Theta("Revenue M:Q"),
                    color=alt.Color("Channel:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                    tooltip=["Channel:N", alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("Share %:Q", format=".1f")],
                )
                st.altair_chart(style_mkt_chart(ch_arc, height=220), use_container_width=True)

    with mkt_tab_risk:
        st.markdown('<div class="mkt-title">Riesgo Marketing y Estrategia</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card crit"><div class="k">Top Driver Riesgo</div><div class="v">{top_risk_mkt['Risk Driver']}</div><div class="d">Mayor línea exposición</div></div>
                <div class="mkt-kpi-card warn"><div class="k">Exposición Total</div><div class="v">CLP {mkt_risk['Exposure M'].sum():.2f}M</div><div class="d">Downside mapeado</div></div>
                <div class="mkt-kpi-card"><div class="k">Revenue Q Base</div><div class="v">CLP {mkt_scenario.loc[mkt_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0]:.1f}M</div><div class="d">Escenario más probable</div></div>
                <div class="mkt-kpi-card {'warn' if (mkt_scenario.loc[mkt_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0] - mkt_scenario.loc[mkt_scenario['Scenario']=='Downside', 'Quarter Revenue M'].iloc[0]) > 0.6 else ''}"><div class="k">Gap Downside</div><div class="v">CLP {(mkt_scenario.loc[mkt_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0] - mkt_scenario.loc[mkt_scenario['Scenario']=='Downside', 'Quarter Revenue M'].iloc[0]):.1f}M</div><div class="d">vs caso base</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="mkt-mini-title">Exposición Riesgo Marketing por Driver</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_bar = alt.Chart(mkt_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure M:Q", title="Exposure (CLP  M)"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure M:Q", format=".2f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                risk_txt = alt.Chart(mkt_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure M:Q", y=alt.Y("Risk Driver:N", sort="-x"), text=alt.Text("Exposure M:Q", format=".2f")
                )
                st.altair_chart(style_mkt_chart(risk_bar + risk_txt, height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Risk Prioritization",
                    f"{top_risk_mkt['Risk Driver']} has the highest exposure at CLP {top_risk_mkt['Exposure M']:.2f}M.",
                    f"Launch mitigation sprint against {top_risk_mkt['Risk Driver']} with weekly executive tracking.",
                    "Improves forecast reliability and reduces downside variance.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="mkt-mini-title">Escenarios Marketing Trimestre</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sc_bar = alt.Chart(mkt_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Quarter Revenue M:Q", title="Revenue (CLP  M)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Quarter Revenue M:Q", format=".1f"), alt.Tooltip("New Subs K:Q", format=".1f"), "Probability:N"],
                )
                sc_label = alt.Chart(mkt_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N", y="Quarter Revenue M:Q", text=alt.Text("Quarter Revenue M:Q", format=".1f")
                )
                st.altair_chart(style_mkt_chart(sc_bar + sc_label, height=235), use_container_width=True)
                base_rev = mkt_scenario.loc[mkt_scenario["Scenario"] == "Base", "Quarter Revenue M"].iloc[0]
                render_mkt_ai_reco(
                    "Scenario Planning",
                    f"Base case is CLP {base_rev:.1f}M with balanced probability and controlled upside/downside ranges.",
                    "Pre-approve tactical budget shifts for downside protection and upside acceleration.",
                    "Shortens reaction cycles and stabilizes quarter outcomes.",
                )

        rk_col3, rk_col4 = st.columns(2)
        with rk_col3:
            st.markdown('<div class="mkt-mini-title">Matriz Heat Riesgo</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_matrix = alt.Chart(mkt_risk).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood"),
                    y=alt.Y("Exposure M:Q", title="Exposure (CLP  M)"),
                    size=alt.Size("Exposure M:Q", scale=alt.Scale(range=[300, 1800]), legend=None),
                    color=alt.Color("Risk Driver:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#EF4444", "#F59E0B", "#3B82F6", "#10B981", "#6366F1"])),
                    tooltip=["Risk Driver:N", alt.Tooltip("Likelihood:Q", format=".1f"), alt.Tooltip("Exposure M:Q", format=".2f")],
                )
                risk_lbl = alt.Chart(mkt_risk).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q", y="Exposure M:Q", text="Risk Driver:N"
                )
                st.altair_chart(style_mkt_chart(risk_matrix + risk_lbl, height=235), use_container_width=True)
                max_quad = mkt_risk.sort_values(["Likelihood", "Exposure M"], ascending=False).iloc[0]
                render_mkt_ai_reco(
                    "Risk Concentration",
                    f"{max_quad['Risk Driver']} sits in the highest likelihood-exposure quadrant.",
                    "Elevate this driver to executive watchlist with pre-defined trigger actions.",
                    "Reduces probability of abrupt quarter underperformance.",
                    level="critical",
                )

        with rk_col4:
            st.markdown('<div class="mkt-mini-title">Retorno Canal Ajustado por Riesgo</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_adj = mkt_channels.copy()
                risk_adj["Risk Factor"] = (risk_adj["CAC"] / risk_adj["CAC"].max() * 0.7 + (1 - risk_adj["CVR %"] / risk_adj["CVR %"].max()) * 0.3)
                risk_adj["Risk-Adjusted ROAS"] = (risk_adj["ROAS"] * (1 - 0.35 * risk_adj["Risk Factor"])).round(2)
                ra_bar = alt.Chart(risk_adj).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#10B981").encode(
                    x=alt.X("Channel:N", sort="-y", title=None),
                    y=alt.Y("Risk-Adjusted ROAS:Q", title="Risk-Adjusted ROAS (x)"),
                    tooltip=["Channel:N", alt.Tooltip("ROAS:Q", format=".2f"), alt.Tooltip("Risk-Adjusted ROAS:Q", format=".2f"), alt.Tooltip("CAC:Q", format=".0f"), alt.Tooltip("CVR %:Q", format=".1f")],
                )
                ra_target = alt.Chart(pd.DataFrame({"y": [2.6]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                ra_text = alt.Chart(risk_adj).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Channel:N", sort="-y"),
                    y="Risk-Adjusted ROAS:Q",
                    text=alt.Text("Risk-Adjusted ROAS:Q", format=".2f"),
                )
                st.altair_chart(style_mkt_chart(ra_target + ra_bar + ra_text, height=235), use_container_width=True)
                weakest_ra = risk_adj.loc[risk_adj["Risk-Adjusted ROAS"].idxmin()]
                render_mkt_ai_reco(
                    "Defensive Budget Allocation",
                    f"{weakest_ra['Channel']} has the weakest risk-adjusted return at {weakest_ra['Risk-Adjusted ROAS']:.2f}x.",
                    f"Apply stricter guardrails and optimization sprints on {weakest_ra['Channel']} before scaling budget.",
                    "Improves downside protection while preserving growth trajectory.",
                    level="warning",
                )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {top_risk_mkt['Risk Driver']} exposure at CLP {top_risk_mkt['Exposure M']:.2f}M</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Highest likelihood-impact concentration in current marketing risk portfolio · trigger mitigation in next planning cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "HR & Workforce":
    import pandas as pd
    import altair as alt

    HR_CHART_THEME = {
        "bg": "#F8FAFF",
        "title": "#1E3A8A",
        "axis": "#334155",
        "grid": "#E2E8F0",
        "font": "Inter",
    }

    def style_hr_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 10, "right": 10, "top": 8, "bottom": 4})
            .configure(background=HR_CHART_THEME["bg"])
            .configure_view(stroke=None, cornerRadius=10)
            .configure_title(color=HR_CHART_THEME["title"], fontSize=13, font=HR_CHART_THEME["font"], anchor="start")
            .configure_axis(
                labelColor=HR_CHART_THEME["axis"],
                titleColor=HR_CHART_THEME["axis"],
                gridColor=HR_CHART_THEME["grid"],
                labelFont=HR_CHART_THEME["font"],
                titleFont=HR_CHART_THEME["font"],
            )
            .configure_legend(
                labelColor=HR_CHART_THEME["axis"],
                titleColor=HR_CHART_THEME["axis"],
                labelFont=HR_CHART_THEME["font"],
                titleFont=HR_CHART_THEME["font"],
            )
        )

    def render_hr_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        level_class = "crit" if level == "critical" else "warn" if level == "warning" else ""
        icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "🤖"
        st.markdown(dedent(f"""
            <div class="hr-ai-card {level_class}">
                <div class="h">{icon} {headline}</div>
                <div class="b"><strong>Insight:</strong> {insight}</div>
                <div class="b"><strong>Action:</strong> {action}</div>
                <div class="b"><strong>Expected Impact:</strong> {impact}</div>
            </div>
        """), unsafe_allow_html=True)

    st.markdown(dedent("""
        <style>
            @keyframes hr-fade-up {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes hr-pulse-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.1); }
                50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.03); }
            }
            .hr-title {
                font-size: 1.08rem;
                font-weight: 800;
                color: #1E3A8A;
                letter-spacing: 0.01em;
                margin: 0.3rem 0 0.6rem 0;
                animation: hr-fade-up 0.45s ease-out both;
            }
            .hr-mini-title {
                font-size: 0.92rem;
                font-weight: 700;
                color: #334155;
                margin: 0.12rem 0 0.5rem 0;
                animation: hr-fade-up 0.45s ease-out both;
            }
            .hr-pulse {
                border-radius: 12px;
                border: 1px solid #DBEAFE;
                background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
                padding: 0.8rem 0.95rem;
                margin-bottom: 0.65rem;
                animation: hr-fade-up 0.45s ease-out both, hr-pulse-glow 2.8s ease-in-out infinite;
            }
            .hr-pulse-grid, .hr-kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.48rem;
            }
            .hr-pulse-card, .hr-kpi-card {
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #E2E8F0;
                padding: 0.52rem 0.62rem;
            }
            .hr-pulse-card .k, .hr-kpi-card .k {
                font-size: 0.69rem;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                font-weight: 700;
            }
            .hr-pulse-card .v, .hr-kpi-card .v {
                font-size: 1.04rem;
                color: #0F172A;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.08rem;
            }
            .hr-pulse-card .d, .hr-kpi-card .d {
                font-size: 0.74rem;
                color: #475569;
                margin-top: 0.12rem;
            }
            .hr-kpi-card.warn { border-left: 4px solid #F59E0B; }
            .hr-kpi-card.crit { border-left: 4px solid #EF4444; }
            .hr-ai-card {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
                background: #EFF6FF;
                padding: 0.62rem 0.72rem;
                margin-top: 0.46rem;
                animation: hr-fade-up 0.42s ease-out both;
            }
            .hr-ai-card.warn { border-left-color: #F59E0B; background: #FFFBEB; }
            .hr-ai-card.crit { border-left-color: #EF4444; background: #FEF2F2; }
            .hr-ai-card .h {
                font-size: 0.83rem;
                font-weight: 800;
                color: #1E293B;
                margin-bottom: 0.28rem;
            }
            .hr-ai-card .b {
                font-size: 0.78rem;
                color: #334155;
                line-height: 1.42;
            }
            @media (max-width: 1200px) {
                .hr-pulse-grid, .hr-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
        </style>
    """), unsafe_allow_html=True)

    hr_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Headcount": [680, 692, 698, 708, 716, 724],
        "Hiring": [22, 20, 18, 24, 22, 20],
        "Attrition": [12, 11, 14, 13, 15, 14],
        "Absenteeism %": [3.0, 2.9, 3.2, 3.1, 3.4, 3.3],
        "Engagement": [76, 77, 78, 78, 79, 80],
        "Productivity Index": [100, 102, 104, 106, 108, 110],
    })
    hr_dept = pd.DataFrame({
        "Department": ["Operaciones Red", "Atención Cliente", "Ventas", "Marketing", "Tech & Data", "Corporativo"],
        "Headcount": [168, 142, 128, 62, 108, 92],
        "Turnover %": [8.4, 12.2, 11.4, 8.8, 7.2, 6.4],
        "eNPS": [38, 26, 30, 35, 42, 38],
        "Time to Fill": [44, 36, 32, 30, 52, 38],
        "Training Hrs": [20, 16, 14, 12, 24, 16],
        "Quality of Hire": [80, 74, 76, 78, 84, 80],
    })
    hr_recruit = pd.DataFrame({
        "Stage": ["Postulantes", "Filtrados", "Entrevistados", "Ofertas", "Contratados"],
        "Volume": [1580, 524, 238, 98, 36],
    })
    hr_recruit["Conversion %"] = (hr_recruit["Volume"] / hr_recruit["Volume"].shift(1) * 100).round(1)
    hr_recruit.loc[0, "Conversion %"] = 100.0

    hr_training = pd.DataFrame({
        "Program": ["Liderazgo WOM", "Certificación 5G/Fibra", "Ventas Consultivas", "Excelencia Cliente", "Data & Analytics"],
        "Participants": [52, 72, 78, 92, 64],
        "Hours": [20, 28, 16, 14, 18],
        "Post Performance Lift %": [9.2, 12.6, 10.4, 8.8, 11.6],
    })
    hr_risk = pd.DataFrame({
        "Risk Driver": ["Fuga Talento Crítico", "Demora Contratación", "Cohortes Bajo Engagement", "Pico Ausentismo", "Brecha Liderazgo"],
        "Exposure Score": [92, 82, 74, 68, 62],
        "Likelihood": [4.0, 3.6, 3.4, 3.2, 2.9],
    })
    hr_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Headcount EoQ": [638, 652, 666],
        "Productivity Index": [102, 107, 112],
        "Voluntary Attrition %": [11.8, 10.3, 8.9],
        "Probability": ["25%", "50%", "25%"],
    })

    current_headcount = hr_monthly.iloc[-1]["Headcount"]
    attrition_rate = hr_monthly["Attrition"].sum() / ((hr_monthly["Headcount"].iloc[0] + current_headcount) / 2) * 100
    net_hiring = hr_monthly["Hiring"].sum() - hr_monthly["Attrition"].sum()
    avg_engagement = hr_monthly["Engagement"].mean()
    avg_absent = hr_monthly["Absenteeism %"].mean()
    productivity_gain = hr_monthly.iloc[-1]["Productivity Index"] - hr_monthly.iloc[0]["Productivity Index"]
    top_hr_risk = hr_risk.loc[hr_risk["Exposure Score"].idxmax()]

    st.markdown('<div class="hr-title">WOM Workforce Pulse - Capital Humano</div>', unsafe_allow_html=True)
    st.markdown(dedent(f"""
        <div class="hr-pulse">
            <div class="hr-pulse-grid">
                <div class="hr-pulse-card"><div class="k">Dotación Actual</div><div class="v">{current_headcount:.0f}</div><div class="d">Total fuerza laboral activa</div></div>
                <div class="hr-pulse-card"><div class="k">Contratación Neta</div><div class="v">{net_hiring:+.0f}</div><div class="d">Movimiento neto 6 meses</div></div>
                <div class="hr-pulse-card"><div class="k">Tasa Rotación</div><div class="v">{attrition_rate:.1f}%</div><div class="d">Presión de rotación</div></div>
                <div class="hr-pulse-card"><div class="k">Engagement</div><div class="v">{avg_engagement:.1f}</div><div class="d">Score promedio mensual</div></div>
                <div class="hr-pulse-card"><div class="k">Ausentismo</div><div class="v">{avg_absent:.2f}%</div><div class="d">Confiabilidad asistencia</div></div>
                <div class="hr-pulse-card"><div class="k">Lift Productividad</div><div class="v">{productivity_gain:+.0f}</div><div class="d">Puntos índice vs inicio</div></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    hr_tab_overview, hr_tab_ops, hr_tab_risk = st.tabs([
        "📈 Vista General Dotación",
        "🧭 Operaciones & Talento",
        "⚠️ Riesgo & Estrategia",
    ])

    with hr_tab_overview:
        st.markdown('<div class="hr-title">Rendimiento Dotación WOM</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="hr-kpi-grid">
                <div class="hr-kpi-card"><div class="k">Dotación</div><div class="v">{current_headcount:.0f}</div><div class="d">Cierre período actual</div></div>
                <div class="hr-kpi-card {'warn' if attrition_rate > 10.5 else ''}"><div class="k">Rotación</div><div class="v">{attrition_rate:.1f}%</div><div class="d">Tasa período rolling</div></div>
                <div class="hr-kpi-card"><div class="k">Score Engagement</div><div class="v">{avg_engagement:.1f}</div><div class="d">Sentimiento empleados</div></div>
                <div class="hr-kpi-card {'warn' if avg_absent > 3.4 else ''}"><div class="k">Ausentismo</div><div class="v">{avg_absent:.2f}%</div><div class="d">Tendencia asistencia</div></div>
            </div>
        """), unsafe_allow_html=True)

        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="hr-mini-title">Dotación vs Contratación y Rotación</div>', unsafe_allow_html=True)
            with st.container(border=True):
                hc_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Headcount:Q", title="Headcount"),
                    tooltip=["Month:N", alt.Tooltip("Headcount:Q", format=".0f"), alt.Tooltip("Hiring:Q", format=".0f"), alt.Tooltip("Attrition:Q", format=".0f")],
                )
                hiring_bar = alt.Chart(hr_monthly).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=20, color="#10B981", opacity=0.55).encode(
                    x=alt.X("Month:N", title=None), y=alt.Y("Hiring:Q", title="Hiring")
                )
                attr_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=2.5, color="#EF4444").encode(
                    x="Month:N", y=alt.Y("Attrition:Q", title="Attrition")
                )
                st.altair_chart(style_hr_chart(alt.layer(hiring_bar, hc_line, attr_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Workforce Balance",
                    f"Headcount closed at {current_headcount:.0f} with net hiring {net_hiring:+.0f} across the period.",
                    "Maintain selective hiring in high-productivity teams while reducing avoidable attrition.",
                    "Stabilizes capacity and improves labor productivity trajectory.",
                )

        with ov_col2:
            st.markdown('<div class="hr-mini-title">Matriz Salud Departamentos</div>', unsafe_allow_html=True)
            with st.container(border=True):
                dep_scatter = alt.Chart(hr_dept).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Turnover %:Q", title="Turnover (%)"),
                    y=alt.Y("eNPS:Q", title="eNPS"),
                    size=alt.Size("Headcount:Q", scale=alt.Scale(range=[280, 1700]), legend=None),
                    color=alt.Color("Quality of Hire:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="Quality of Hire")),
                    tooltip=["Department:N", alt.Tooltip("Headcount:Q", format=".0f"), alt.Tooltip("Turnover %:Q", format=".1f"), alt.Tooltip("eNPS:Q", format=".0f"), alt.Tooltip("Quality of Hire:Q", format=".0f")],
                )
                dep_lbl = alt.Chart(hr_dept).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(x="Turnover %:Q", y="eNPS:Q", text="Department:N")
                st.altair_chart(style_hr_chart(dep_scatter + dep_lbl, height=235), use_container_width=True)
                weak_dep = hr_dept.sort_values(["Turnover %", "eNPS"], ascending=[False, True]).iloc[0]
                render_hr_ai_reco(
                    "Department Retention Focus",
                    f"{weak_dep['Department']} shows the highest retention pressure with weaker sentiment profile.",
                    f"Prioritize manager coaching, career-pathing, and engagement actions in {weak_dep['Department']}.",
                    "Reduces avoidable exits in high-impact teams.",
                    level="warning",
                )

        ov_col3, ov_col4 = st.columns(2)
        with ov_col3:
            st.markdown('<div class="hr-mini-title">Tendencia Engagement y Ausentismo</div>', unsafe_allow_html=True)
            with st.container(border=True):
                eng_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Engagement:Q", title="Engagement Score"),
                    tooltip=["Month:N", alt.Tooltip("Engagement:Q", format=".0f"), alt.Tooltip("Absenteeism %:Q", format=".2f"), alt.Tooltip("Productivity Index:Q", format=".0f")],
                )
                abs_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=2.6, color="#F59E0B").encode(
                    x="Month:N",
                    y=alt.Y("Absenteeism %:Q", title="Absenteeism (%)"),
                )
                st.altair_chart(style_hr_chart(alt.layer(eng_line, abs_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_hr_ai_reco(
                    "People Experience Signal",
                    f"Engagement improved to {hr_monthly.iloc[-1]['Engagement']:.0f} while absenteeism remains elevated at {hr_monthly.iloc[-1]['Absenteeism %']:.2f}%.",
                    "Pair engagement initiatives with attendance coaching in teams above absenteeism threshold.",
                    "Supports stronger morale while protecting operational continuity.",
                    level="warning" if hr_monthly.iloc[-1]["Absenteeism %"] > 3.4 else "info",
                )

        with ov_col4:
            st.markdown('<div class="hr-mini-title">Índice Capacidad Departamentos</div>', unsafe_allow_html=True)
            with st.container(border=True):
                capability_df = hr_dept.copy()
                capability_df["Capability Index"] = (
                    capability_df["Quality of Hire"] * 0.45
                    + capability_df["eNPS"] * 0.35
                    + capability_df["Training Hrs"] * 0.9
                    - capability_df["Turnover %"] * 1.2
                ).round(1)
                cap_bar = alt.Chart(capability_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Capability Index:Q", title="Capability Index"),
                    y=alt.Y("Department:N", sort="-x", title=None),
                    color=alt.Color("Capability Index:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Department:N", alt.Tooltip("Capability Index:Q", format=".1f"), alt.Tooltip("Quality of Hire:Q", format=".0f"), alt.Tooltip("eNPS:Q", format=".0f"), alt.Tooltip("Training Hrs:Q", format=".0f"), alt.Tooltip("Turnover %:Q", format=".1f")],
                )
                cap_text = alt.Chart(capability_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Capability Index:Q", y=alt.Y("Department:N", sort="-x"), text=alt.Text("Capability Index:Q", format=".1f")
                )
                st.altair_chart(style_hr_chart(cap_bar + cap_text, height=235), use_container_width=True)
                low_cap = capability_df.loc[capability_df["Capability Index"].idxmin()]
                render_hr_ai_reco(
                    "Capability Development Focus",
                    f"{low_cap['Department']} has the weakest capability index and needs accelerated support.",
                    f"Increase targeted upskilling and retention interventions in {low_cap['Department']}.",
                    "Improves bench strength in teams with higher delivery risk.",
                    level="warning",
                )

    with hr_tab_ops:
        st.markdown('<div class="hr-title">Operaciones Workforce y Journey Talento</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="hr-kpi-grid">
                <div class="hr-kpi-card"><div class="k">Postulantes</div><div class="v">{hr_recruit.loc[hr_recruit['Stage']=='Postulantes', 'Volume'].iloc[0]:,.0f}</div><div class="d">Volumen funnel contratación</div></div>
                <div class="hr-kpi-card"><div class="k">Ofertas</div><div class="v">{hr_recruit.loc[hr_recruit['Stage']=='Ofertas', 'Volume'].iloc[0]:.0f}</div><div class="d">Candidatos etapa oferta</div></div>
                <div class="hr-kpi-card {'warn' if hr_dept['Time to Fill'].mean() > 42 else ''}"><div class="k">Tiempo Promedio Llenado</div><div class="v">{hr_dept['Time to Fill'].mean():.1f} d</div><div class="d">Eficiencia ciclo contratación</div></div>
                <div class="hr-kpi-card"><div class="k">Lift Capacitación</div><div class="v">{hr_training['Post Performance Lift %'].mean():.1f}%</div><div class="d">Impacto post-training</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="hr-mini-title">Conversión Funnel Reclutamiento</div>', unsafe_allow_html=True)
            with st.container(border=True):
                rec_bar = alt.Chart(hr_recruit).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=24).encode(
                    x=alt.X("Volume:Q", title="Candidatos"),
                    y=alt.Y("Stage:N", sort=["Postulantes", "Filtrados", "Entrevistados", "Ofertas", "Contratados"], title=None),
                    color=alt.Color("Conversion %:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Stage:N", alt.Tooltip("Volume:Q", format=".0f"), alt.Tooltip("Conversion %:Q", format=".1f")],
                )
                rec_txt = alt.Chart(hr_recruit).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Volume:Q", y=alt.Y("Stage:N", sort=["Postulantes", "Filtrados", "Entrevistados", "Ofertas", "Contratados"]), text=alt.Text("Conversion %:Q", format=".1f")
                )
                st.altair_chart(style_hr_chart(rec_bar + rec_txt, height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Talent Funnel Quality",
                    f"Interview-to-offer conversion is {hr_recruit.loc[hr_recruit['Stage']=='Ofertas', 'Conversion %'].iloc[0]:.1f}%, indicating mid-funnel selectivity.",
                    "Improve sourcing fit and screening quality to increase interview efficiency.",
                    "Shortens hiring cycle and lowers hiring cost per role.",
                )

        with op_col2:
            st.markdown('<div class="hr-mini-title">Tiempo Llenado vs Calidad Contratación</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fill_scatter = alt.Chart(hr_dept).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Time to Fill:Q", title="Time to Fill (days)"),
                    y=alt.Y("Quality of Hire:Q", title="Quality of Hire"),
                    size=alt.Size("Headcount:Q", scale=alt.Scale(range=[280, 1500]), legend=None),
                    color=alt.Color("Department:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                    tooltip=["Department:N", alt.Tooltip("Time to Fill:Q", format=".0f"), alt.Tooltip("Quality of Hire:Q", format=".0f"), alt.Tooltip("Headcount:Q", format=".0f")],
                )
                fill_lbl = alt.Chart(hr_dept).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(x="Time to Fill:Q", y="Quality of Hire:Q", text="Department:N")
                st.altair_chart(style_hr_chart(fill_scatter + fill_lbl, height=235), use_container_width=True)
                slow_dep = hr_dept.loc[hr_dept["Time to Fill"].idxmax()]
                render_hr_ai_reco(
                    "Hiring Cycle Optimization",
                    f"{slow_dep['Department']} has the slowest time-to-fill at {slow_dep['Time to Fill']:.0f} days.",
                    f"Activate specialized talent pools and faster panel scheduling for {slow_dep['Department']}.",
                    "Improves capacity fill-rate in constrained skill areas.",
                    level="warning",
                )

        st.markdown('<div class="hr-mini-title">Programas Capacitación vs Lift Performance</div>', unsafe_allow_html=True)
        with st.container(border=True):
            train_bar = alt.Chart(hr_training).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#60A5FA").encode(
                x=alt.X("Program:N", title=None),
                y=alt.Y("Participants:Q", title="Participants"),
                tooltip=["Program:N", alt.Tooltip("Participants:Q", format=".0f"), alt.Tooltip("Hours:Q", format=".0f"), alt.Tooltip("Post Performance Lift %:Q", format=".1f")],
            )
            lift_line = alt.Chart(hr_training).mark_line(point=True, strokeWidth=2.8, color="#10B981").encode(
                x="Program:N", y=alt.Y("Post Performance Lift %:Q", title="Performance Lift (%)")
            )
            st.altair_chart(style_hr_chart(alt.layer(train_bar, lift_line).resolve_scale(y="independent"), height=235), use_container_width=True)
            top_prog = hr_training.loc[hr_training["Post Performance Lift %"].idxmax()]
            render_hr_ai_reco(
                "Capability Building",
                f"{top_prog['Program']} shows the strongest post-training lift at {top_prog['Post Performance Lift %']:.1f}%.",
                f"Scale enrollment for {top_prog['Program']} and replicate its learning model in adjacent tracks.",
                "Raises workforce capability and measurable productivity outcomes.",
            )

        op_col3, op_col4 = st.columns(2)
        with op_col3:
            st.markdown('<div class="hr-mini-title">Drop-Off por Etapa Reclutamiento</div>', unsafe_allow_html=True)
            with st.container(border=True):
                drop_df = hr_recruit.copy()
                drop_df["Drop-Off"] = (drop_df["Volume"].shift(1) - drop_df["Volume"]).fillna(0)
                drop_chart = alt.Chart(drop_df[drop_df["Stage"] != "Postulantes"]).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=30, color="#EF4444").encode(
                    x=alt.X("Stage:N", title=None),
                    y=alt.Y("Drop-Off:Q", title="Drop-Off Volume"),
                    tooltip=["Stage:N", alt.Tooltip("Drop-Off:Q", format=".0f"), alt.Tooltip("Conversion %:Q", format=".1f")],
                )
                drop_text = alt.Chart(drop_df[drop_df["Stage"] != "Postulantes"]).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x="Stage:N", y="Drop-Off:Q", text=alt.Text("Drop-Off:Q", format=".0f")
                )
                st.altair_chart(style_hr_chart(drop_chart + drop_text, height=235), use_container_width=True)
                top_drop = drop_df[drop_df["Stage"] != "Postulantes"].sort_values("Drop-Off", ascending=False).iloc[0]
                render_hr_ai_reco(
                    "Funnel Leakage",
                    f"Largest drop-off occurs at {top_drop['Stage']} stage ({top_drop['Drop-Off']:.0f} candidates).",
                    "Audit stage criteria and interviewer calibration to reduce avoidable candidate loss.",
                    "Improves hire yield without expanding sourcing spend.",
                    level="warning",
                )

        with op_col4:
            st.markdown('<div class="hr-mini-title">Horas Capacitación vs Calidad Contratación</div>', unsafe_allow_html=True)
            with st.container(border=True):
                train_scatter = alt.Chart(hr_dept).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Training Hrs:Q", title="Training Hours"),
                    y=alt.Y("Quality of Hire:Q", title="Quality of Hire"),
                    size=alt.Size("Headcount:Q", scale=alt.Scale(range=[260, 1500]), legend=None),
                    color=alt.Color("Turnover %:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Turnover %")),
                    tooltip=["Department:N", alt.Tooltip("Training Hrs:Q", format=".0f"), alt.Tooltip("Quality of Hire:Q", format=".0f"), alt.Tooltip("Turnover %:Q", format=".1f"), alt.Tooltip("Headcount:Q", format=".0f")],
                )
                train_lbl = alt.Chart(hr_dept).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Training Hrs:Q", y="Quality of Hire:Q", text="Department:N"
                )
                st.altair_chart(style_hr_chart(train_scatter + train_lbl, height=235), use_container_width=True)
                undertrained = hr_dept.sort_values(["Training Hrs", "Quality of Hire"]).iloc[0]
                render_hr_ai_reco(
                    "Upskilling Priority",
                    f"{undertrained['Department']} combines lower training hours with weaker quality-of-hire outcomes.",
                    f"Increase structured development hours and mentorship in {undertrained['Department']}.",
                    "Strengthens role readiness and reduces early-performance variability.",
                    level="warning",
                )

    with hr_tab_risk:
        st.markdown('<div class="hr-title">Riesgo Workforce y Estrategia</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="hr-kpi-grid">
                <div class="hr-kpi-card crit"><div class="k">Top Driver Riesgo</div><div class="v">{top_hr_risk['Risk Driver']}</div><div class="d">Mayor riesgo exposición</div></div>
                <div class="hr-kpi-card warn"><div class="k">Exposición Riesgo</div><div class="v">{hr_risk['Exposure Score'].sum():.0f}</div><div class="d">Índice riesgo portafolio</div></div>
                <div class="hr-kpi-card"><div class="k">Dotación Base EoQ</div><div class="v">{hr_scenario.loc[hr_scenario['Scenario']=='Base', 'Headcount EoQ'].iloc[0]:.0f}</div><div class="d">Escenario más probable</div></div>
                <div class="hr-kpi-card {'warn' if hr_scenario.loc[hr_scenario['Scenario']=='Downside', 'Voluntary Attrition %'].iloc[0] > 11 else ''}"><div class="k">Rotación Downside</div><div class="v">{hr_scenario.loc[hr_scenario['Scenario']=='Downside', 'Voluntary Attrition %'].iloc[0]:.1f}%</div><div class="d">Señal caso stress</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="hr-mini-title">Exposición Riesgo por Driver</div>', unsafe_allow_html=True)
            with st.container(border=True):
                hr_risk_bar = alt.Chart(hr_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure Score:Q", title="Exposure Score"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure Score:Q", format=".0f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                hr_risk_txt = alt.Chart(hr_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure Score:Q", y=alt.Y("Risk Driver:N", sort="-x"), text=alt.Text("Exposure Score:Q", format=".0f")
                )
                st.altair_chart(style_hr_chart(hr_risk_bar + hr_risk_txt, height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Risk Prioritization",
                    f"{top_hr_risk['Risk Driver']} has the highest workforce risk exposure score ({top_hr_risk['Exposure Score']:.0f}).",
                    f"Create mitigation sprint with retention and capability interventions focused on {top_hr_risk['Risk Driver']}.",
                    "Reduces execution risk in critical workforce capabilities.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="hr-mini-title">Escenarios Workforce Outlook</div>', unsafe_allow_html=True)
            with st.container(border=True):
                hr_sc_bar = alt.Chart(hr_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Headcount EoQ:Q", title="Headcount EoQ"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Headcount EoQ:Q", format=".0f"), alt.Tooltip("Productivity Index:Q", format=".0f"), alt.Tooltip("Voluntary Attrition %:Q", format=".1f"), "Probability:N"],
                )
                hr_sc_txt = alt.Chart(hr_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N", y="Headcount EoQ:Q", text=alt.Text("Headcount EoQ:Q", format=".0f")
                )
                st.altair_chart(style_hr_chart(hr_sc_bar + hr_sc_txt, height=235), use_container_width=True)
                base_head = hr_scenario.loc[hr_scenario["Scenario"] == "Base", "Headcount EoQ"].iloc[0]
                render_hr_ai_reco(
                    "Scenario Planning",
                    f"Base scenario closes at {base_head:.0f} headcount with balanced productivity trajectory.",
                    "Pre-approve contingency levers for downside attrition and upside hiring acceleration.",
                    "Improves workforce planning agility and delivery predictability.",
                )

        rk_col3, rk_col4 = st.columns(2)
        with rk_col3:
            st.markdown('<div class="hr-mini-title">Matriz Heat Riesgo</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_heat = alt.Chart(hr_risk).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood"),
                    y=alt.Y("Exposure Score:Q", title="Exposure Score"),
                    size=alt.Size("Exposure Score:Q", scale=alt.Scale(range=[300, 1800]), legend=None),
                    color=alt.Color("Risk Driver:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#EF4444", "#F59E0B", "#3B82F6", "#10B981", "#6366F1"])),
                    tooltip=["Risk Driver:N", alt.Tooltip("Likelihood:Q", format=".1f"), alt.Tooltip("Exposure Score:Q", format=".0f")],
                )
                risk_lbl = alt.Chart(hr_risk).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q", y="Exposure Score:Q", text="Risk Driver:N"
                )
                st.altair_chart(style_hr_chart(risk_heat + risk_lbl, height=235), use_container_width=True)
                max_risk = hr_risk.sort_values(["Likelihood", "Exposure Score"], ascending=False).iloc[0]
                render_hr_ai_reco(
                    "Risk Concentration",
                    f"{max_risk['Risk Driver']} is the highest-likelihood, highest-exposure risk in the matrix.",
                    "Escalate this risk to monthly executive governance with clear trigger thresholds.",
                    "Improves proactive control of people-related delivery risk.",
                    level="critical",
                )

        with rk_col4:
            st.markdown('<div class="hr-mini-title">Trade-off Rotación vs Productividad</div>', unsafe_allow_html=True)
            with st.container(border=True):
                trade_scatter = alt.Chart(hr_scenario).mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.3).encode(
                    x=alt.X("Voluntary Attrition %:Q", title="Voluntary Attrition (%)"),
                    y=alt.Y("Productivity Index:Q", title="Productivity Index"),
                    size=alt.Size("Headcount EoQ:Q", scale=alt.Scale(range=[420, 1700]), legend=None),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Headcount EoQ:Q", format=".0f"), alt.Tooltip("Productivity Index:Q", format=".0f"), alt.Tooltip("Voluntary Attrition %:Q", format=".1f"), "Probability:N"],
                )
                trade_lbl = alt.Chart(hr_scenario).mark_text(dy=-10, fontSize=10, color="#1E293B").encode(
                    x="Voluntary Attrition %:Q", y="Productivity Index:Q", text="Scenario:N"
                )
                st.altair_chart(style_hr_chart(trade_scatter + trade_lbl, height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Strategic Workforce Trade-off",
                    "Lower attrition scenarios align with materially higher productivity outcomes.",
                    "Concentrate retention investments in critical roles where productivity elasticity is strongest.",
                    "Improves both service capacity and workforce efficiency in parallel.",
                    level="warning",
                )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {top_hr_risk['Risk Driver']} is the top workforce risk</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Exposure score {top_hr_risk['Exposure Score']:.0f} with high likelihood ({top_hr_risk['Likelihood']:.1f}) · prioritize mitigation in next HR operating cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "Conclusion":
    st.image(
        "https://raw.githubusercontent.com/pmjose/WOM/main/image/gemini.png",
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# Footer (matches wom.cl footer)
# ---------------------------------------------------------------------------
st.markdown(dedent(f"""
    <div class="mf-footer">
        <div class="mf-footer-brand">WOM <span>Chile</span></div>
        <div style="max-width:760px; margin:16px auto 0; padding:14px 16px; border-radius:12px; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.18); color:#E2E8F0;">
            <div style="font-size:0.9rem; font-weight:800; letter-spacing:0.2px;">WOM + Snowflake: partnership for scalable telecom growth</div>
            <div style="font-size:0.82rem; line-height:1.45; margin-top:6px; color:rgba(255,255,255,0.82);">
                Unified data, AI-driven decisions, and faster execution from network operations to subscriber retention.
            </div>
            <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-top:9px; font-size:0.74rem; color:rgba(255,255,255,0.78);">
                <span>Real-time analytics</span>
                <span>Predictive churn prevention</span>
                <span>CAPEX prioritization intelligence</span>
            </div>
        </div>
        <hr class="mf-footer-divider">
        <div class="mf-footer-copy" style="display:flex; flex-direction:column; align-items:center; gap:0.32rem;">
            <div style="display:inline-flex; align-items:center; gap:0.46rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.22); border-radius:999px; padding:0.24rem 0.68rem; color:#E2E8F0; font-weight:700;">Build with &#10084;&#65039; by Snowflake for WOM - MWC 2026</div>
        </div>
    </div>
"""), unsafe_allow_html=True)
