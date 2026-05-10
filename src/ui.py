"""UI helper functions and styling for the PesoLens Streamlit app."""

from __future__ import annotations

from typing import Optional

import streamlit as st

from src.detector import DetectionSummary

APP_NAME = "PesoLens"
APP_TITLE = "PesoLens ₱1000 Bill Scanner"
APP_SUBTITLE = "AI-powered scanner for old and new Philippine ₱1000 bills"


def apply_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #f4f7fb;
            --surface: #ffffff;
            --surface-soft: #fbfdff;
            --border: #e2e8f0;
            --border-strong: #d4dfec;
            --text: #0f172a;
            --soft-text: #475569;
            --muted: #64748b;
            --blue: #2563eb;
            --blue-dark: #1d4ed8;
            --blue-soft: #eff6ff;
            --red: #dc2626;
            --green: #15803d;
            --green-bg: #ecfdf3;
            --green-border: #86efac;
            --red-bg: #fff1f2;
            --red-border: #fecdd3;
            --sidebar: #06111f;
            --sidebar-card: rgba(255, 255, 255, 0.07);
            --sidebar-text: #e5edf7;
            --sidebar-muted: #94a3b8;
            --shadow: 0 16px 42px rgba(15, 23, 42, 0.09);
            --shadow-soft: 0 10px 28px rgba(15, 23, 42, 0.06);
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 14px;
        }

        html, body, .stApp, [class*="css"] {
            font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        .stApp {
            background: radial-gradient(circle at top left, #ffffff 0%, var(--bg) 42%, #eef3fb 100%);
            color: var(--text);
        }

        h1, h2, h3, h4, h5, h6, p, label, span, li,
        div[data-testid="stMarkdownContainer"] {
            color: var(--text) !important;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1.4rem;
            padding-bottom: 2.2rem;
        }

        [data-testid="stHeader"] {
            background: rgba(244, 247, 251, 0.86);
            border-bottom: 1px solid rgba(226, 232, 240, 0.9);
            backdrop-filter: blur(10px);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 30% 0%, rgba(37, 99, 235, 0.22) 0%, rgba(37, 99, 235, 0.02) 35%, transparent 55%),
                linear-gradient(180deg, var(--sidebar) 0%, #03101d 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 12px 0 30px rgba(15, 23, 42, 0.18);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 0.55rem 1.1rem 1.2rem 1.1rem;
        }

        [data-testid="stSidebar"] * {
            color: var(--sidebar-text) !important;
        }

        .brand-row {
            display: flex;
            align-items: center;
            gap: 0.78rem;
            margin-top: 0.15rem;
            margin-bottom: 1.6rem;
        }

        .brand-mark {
            width: 54px;
            height: 54px;
            border-radius: 16px;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: #ffffff !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.65rem;
            font-weight: 900;
            box-shadow: 0 16px 28px rgba(37, 99, 235, 0.36);
            position: relative;
            flex-shrink: 0;
        }

        .brand-mark::before {
            content: "";
            position: absolute;
            inset: 7px;
            border: 2px solid rgba(255, 255, 255, 0.70);
            border-radius: 11px;
        }

        .brand-name {
            color: #ffffff !important;
            font-size: 1.34rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            line-height: 1.05;
        }

        .brand-tagline {
            color: #cbd5e1 !important;
            font-size: 0.78rem;
            margin-top: 0.24rem;
            line-height: 1.35;
            font-weight: 600;
        }

        .sidebar-menu-label {
            color: var(--sidebar-muted) !important;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-size: 0.72rem;
            font-weight: 900;
            margin: 0.4rem 0 0.75rem 0;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 0.42rem;
            width: 100%;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label {
            width: 100% !important;
            min-height: 56px !important;
            border-radius: 14px !important;
            padding: 0.82rem 0.95rem !important;
            transition: all 0.18s ease;
            background: transparent !important;
            border: 1px solid transparent !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.85rem !important;
            box-sizing: border-box !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.06) !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            width: 100% !important;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            border-color: rgba(255, 255, 255, 0.16) !important;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.28);
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {
            display: none !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label p,
        [data-testid="stSidebar"] div[role="radiogroup"] label span {
            color: #dbeafe !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {
            color: #ffffff !important;
            font-weight: 900 !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label::before {
            content: "";
            width: 19px;
            height: 19px;
            flex: 0 0 19px;
            background: #cbd5e1;
            opacity: 0.95;
            -webkit-mask-repeat: no-repeat;
            -webkit-mask-position: center;
            -webkit-mask-size: contain;
            mask-repeat: no-repeat;
            mask-position: center;
            mask-size: contain;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked)::before {
            background: #ffffff;
            opacity: 1;
        }

        /* Sidebar icons */
        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(1)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M4 8V5a1 1 0 0 1 1-1h3'/%3E%3Cpath d='M16 4h3a1 1 0 0 1 1 1v3'/%3E%3Cpath d='M20 16v3a1 1 0 0 1-1 1h-3'/%3E%3Cpath d='M8 20H5a1 1 0 0 1-1-1v-3'/%3E%3Cpath d='M7 12h10'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M4 8V5a1 1 0 0 1 1-1h3'/%3E%3Cpath d='M16 4h3a1 1 0 0 1 1 1v3'/%3E%3Cpath d='M20 16v3a1 1 0 0 1-1 1h-3'/%3E%3Cpath d='M8 20H5a1 1 0 0 1-1-1v-3'/%3E%3Cpath d='M7 12h10'/%3E%3C/svg%3E");
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(2)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M12 8v5l3 2'/%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M12 8v5l3 2'/%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3C/svg%3E");
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(3)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M12 17h.01M12 14a3 3 0 1 0-3-3'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M12 17h.01M12 14a3 3 0 1 0-3-3'/%3E%3C/svg%3E");
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(4)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M12 8h.01M11 12h1v5h1'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M12 8h.01M11 12h1v5h1'/%3E%3C/svg%3E");
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(5)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3V4Z'/%3E%3Cpath d='M8 4v13a3 3 0 0 0 3 3'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3V4Z'/%3E%3Cpath d='M8 4v13a3 3 0 0 0 3 3'/%3E%3C/svg%3E");
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(6)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z'/%3E%3Cpath d='M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6 1.7 1.7 0 0 0-.4 1.1V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-.4-1.1 1.7 1.7 0 0 0-1-.6 1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1 1.7 1.7 0 0 0-1.1-.4H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.1-.4 1.7 1.7 0 0 0 .6-1 1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6 1.7 1.7 0 0 0 .4-1.1V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 .4 1.1 1.7 1.7 0 0 0 1 .6 1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.2.4.4.7.6 1 .3.3.7.4 1.1.4h.1a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.1.4 1.7 1.7 0 0 0-.6.6Z'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath d='M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z'/%3E%3Cpath d='M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6 1.7 1.7 0 0 0-.4 1.1V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-.4-1.1 1.7 1.7 0 0 0-1-.6 1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1 1.7 1.7 0 0 0-1.1-.4H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.1-.4 1.7 1.7 0 0 0 .6-1 1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6 1.7 1.7 0 0 0 .4-1.1V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 .4 1.1 1.7 1.7 0 0 0 1 .6 1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.2.4.4.7.6 1 .3.3.7.4 1.1.4h.1a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.1.4 1.7 1.7 0 0 0-.6.6Z'/%3E%3C/svg%3E");
        }

        .sidebar-tip {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 16px;
            background: var(--sidebar-card);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }

        .sidebar-tip-title {
            color: #ffffff !important;
            font-size: 0.9rem;
            font-weight: 900;
            margin-bottom: 0.45rem;
        }

        .sidebar-tip-text {
            color: #cbd5e1 !important;
            font-size: 0.82rem;
            line-height: 1.55;
            font-weight: 500;
        }

        .sidebar-footer {
            position: static;
            margin-top: 1rem;
            padding-bottom: 0.7rem;
            color: #94a3b8 !important;
            font-size: 0.74rem;
            line-height: 1.45;
        }

        /* Top header */
        .topbar {
            background: rgba(255, 255, 255, 0.97);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: var(--shadow-soft);
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
            min-height: 118px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.2rem;
        }

        .topbar-title {
            flex: 1;
        }

        .topbar h1 {
            margin: 0;
            font-size: clamp(1.55rem, 3vw, 2.35rem);
            line-height: 1.12;
            letter-spacing: -0.045em;
            font-weight: 900;
        }

        .topbar p {
            color: var(--muted) !important;
            margin: 0.55rem 0 0 0;
            font-weight: 600;
        }

        .topbar-tagline {
            color: var(--blue) !important;
            margin-top: 0.45rem;
            font-weight: 900;
            font-size: 0.95rem;
        }

        .topbar-action {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 176px;
            height: 54px;
            border-radius: 12px;
            text-decoration: none !important;
            background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 100%);
            color: #ffffff !important;
            font-size: 0.98rem;
            font-weight: 900;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.25);
            transition: all 0.16s ease;
        }

        .topbar-action:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 30px rgba(37, 99, 235, 0.32);
        }

        .topbar-action span {
            color: #ffffff !important;
            font-weight: 900;
            margin-right: 0.45rem;
            font-size: 1.2rem;
        }

        .scan-shell, .soft-panel {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-soft);
            padding: 1.2rem;
            margin-bottom: 1.15rem;
        }

        .empty-state {
            min-height: 330px;
            border: 1.5px dashed var(--border-strong);
            border-radius: var(--radius-lg);
            background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            text-align: center;
        }

        .empty-state .icon {
            font-size: 2.6rem;
            color: #98a2b3 !important;
            margin-bottom: 0.75rem;
        }

        .empty-state h3 {
            margin: 0.1rem 0 0.35rem 0;
            font-weight: 900;
        }

        .empty-state p {
            margin: 0;
            color: var(--soft-text) !important;
            font-weight: 600;
        }

        .section-title {
            font-size: 1.14rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            margin: 1.15rem 0 0.85rem 0;
        }

        .compact-title {
            margin-bottom: 0.55rem !important;
        }

        /* Detection mode selector: clean no-icon card style */
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: 1rem !important;
            width: 100% !important;
            margin-bottom: 1.15rem !important;
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label {
            min-height: 86px !important;
            background: #ffffff !important;
            border: 1px solid var(--border-strong) !important;
            border-radius: 14px !important;
            padding: 1.05rem 1.25rem !important;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
            cursor: pointer;
            transition: all 0.18s ease;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            text-align: left !important;
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            border-color: var(--blue) !important;
            background: #f8fbff !important;
            transform: translateY(-1px);
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] {
            display: none !important;
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label p,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label span {
            color: var(--soft-text) !important;
            font-weight: 700 !important;
            white-space: pre-line !important;
            line-height: 1.38 !important;
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label p::first-line,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label span::first-line {
            color: var(--text) !important;
            font-weight: 900 !important;
            font-size: 1rem !important;
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked),
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has([aria-checked="true"]) {
            background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 100%) !important;
            border-color: var(--blue-dark) !important;
            box-shadow: 0 14px 28px rgba(37, 99, 235, 0.25);
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has([aria-checked="true"]) p,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has([aria-checked="true"]) span {
            color: #dbeafe !important;
            font-weight: 700 !important;
        }

        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p::first-line,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span::first-line,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has([aria-checked="true"]) p::first-line,
        section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] label:has([aria-checked="true"]) span::first-line {
            color: #ffffff !important;
            font-weight: 900 !important;
        }

        .breakdown-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
            padding: 1rem;
            min-height: 137px;
            margin-bottom: 0.85rem;
        }

        .card-title {
            color: #475569 !important;
            font-size: 0.9rem;
            font-weight: 900;
            margin-bottom: 0.65rem;
        }

        .thin-line {
            height: 4px;
            width: 34px;
            border-radius: 999px;
            background: var(--blue);
            margin-bottom: 0.7rem;
        }

        .card-value {
            color: var(--blue) !important;
            font-size: 2.05rem;
            line-height: 1.02;
            font-weight: 900;
            letter-spacing: -0.045em;
            overflow-wrap: anywhere;
        }

        .card-value.red { color: var(--red) !important; }
        .card-value.dark { color: var(--text) !important; }

        .card-help {
            color: var(--muted) !important;
            font-size: 0.79rem;
            line-height: 1.4;
            margin-top: 0.55rem;
            font-weight: 600;
        }

        .result-summary {
            padding: 1rem;
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            background: var(--surface-soft);
        }

        .result-summary p {
            color: var(--soft-text) !important;
            font-size: 0.9rem;
            margin: 0.38rem 0;
            font-weight: 600;
        }

        .status-pill {
            display: inline-flex;
            font-size: 0.82rem;
            font-weight: 900;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            margin-bottom: 0.65rem;
            color: var(--blue) !important;
            background: var(--blue-soft);
            border: 1px solid #cfe0ff;
        }

        .status-pill.good {
            color: var(--green) !important;
            background: var(--green-bg);
            border-color: var(--green-border);
        }

        .status-pill.none {
            color: var(--red) !important;
            background: var(--red-bg);
            border-color: var(--red-border);
        }

        .guide-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1rem;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
            min-height: 145px;
            margin-bottom: 0.85rem;
        }

        .guide-card h4 {
            margin: 0 0 0.35rem 0;
            font-size: 1rem;
            font-weight: 900;
        }

        .guide-card p {
            margin: 0;
            color: var(--muted) !important;
            font-size: 0.88rem;
            line-height: 1.48;
            font-weight: 600;
        }

        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 100%);
            color: #ffffff !important;
            border: 1px solid var(--blue);
            border-radius: 12px;
            padding: 0.62rem 1.05rem;
            font-weight: 900;
            box-shadow: 0 8px 16px rgba(37, 99, 235, 0.22);
            transition: all 0.16s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-1px);
            background: linear-gradient(135deg, var(--blue-dark) 0%, #174fae 100%);
            border-color: var(--blue-dark);
        }

        .stButton > button p,
        .stDownloadButton > button p,
        .stButton > button span,
        .stDownloadButton > button span {
            color: #ffffff !important;
            font-weight: 900 !important;
        }

        div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
            background: var(--surface-soft);
            border: 1.5px dashed var(--border-strong);
            border-radius: var(--radius-md);
            padding: 0.7rem;
        }

        code {
            background: #eef2f7 !important;
            color: #344054 !important;
            border-radius: 6px;
            padding: 0.12rem 0.28rem;
        }

        div[data-testid="stImage"] img {
            max-height: 650px !important;
            object-fit: contain !important;
            border-radius: 16px !important;
        }

        div[data-testid="stCameraInput"] video,
        div[data-testid="stCameraInput"] img {
            max-height: 480px !important;
            object-fit: contain !important;
            border-radius: 16px !important;
        }

        .floating-notification {
            position: fixed;
            top: 5.2rem;
            left: 50%;
            transform: translateX(-50%);
            z-index: 999999;
            min-width: 360px;
            max-width: 620px;
            padding: 0.95rem 1.25rem;
            border-radius: 16px;
            font-weight: 900;
            text-align: center;
            box-shadow: 0 16px 42px rgba(15, 23, 42, 0.16);
            animation: fade-notification 4.2s ease forwards;
            pointer-events: none;
        }

        .floating-notification.success {
            background: #ecfdf3;
            border: 1px solid #86efac;
            color: #166534 !important;
        }

        .floating-notification.error {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            color: #be123c !important;
        }

        @keyframes fade-notification {
            0% {
                opacity: 0;
                transform: translate(-50%, -8px);
            }

            12% {
                opacity: 1;
                transform: translate(-50%, 0);
            }

            75% {
                opacity: 1;
                transform: translate(-50%, 0);
            }

            100% {
                opacity: 0;
                transform: translate(-50%, -8px);
                visibility: hidden;
            }
        }

        @media (max-width: 900px) {
            .topbar {
                flex-direction: column;
                align-items: flex-start;
            }

            .topbar-action {
                width: 100%;
            }

            section[data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] {
                grid-template-columns: 1fr !important;
            }
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand() -> None:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-mark">₱</div>
            <div>
                <div class="brand-name">PesoLens</div>
                <div class="brand-tagline">₱1000 Bill Scanner</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_scan_tip() -> None:
    st.markdown(
        """
        <div class="sidebar-tip">
            <div class="sidebar-tip-title">Tip</div>
            <div class="sidebar-tip-text">
                For best results, use clear images and good lighting.
            </div>
        </div>
        <div class="sidebar-footer">
            © 2026 PesoLens<br>
            All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar() -> None:
    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-title">
                <h1>{APP_TITLE}</h1>
                <p>{APP_SUBTITLE}</p>
                <div class="topbar-tagline">Detect. Classify. Count. Compute.</div>
            </div>
            <a href="?new_scan=1" target="_self" class="topbar-action">
                <span>+</span> New Scan
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_floating_model_notification(is_loaded: bool) -> None:
    if is_loaded:
        st.markdown(
            """
            <div class="floating-notification success">
                Model ready. PesoLens can now scan ₱1000 bills.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="floating-notification error">
                Model not found. Add the trained model inside the models folder.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">▧</div>
            <h3>No image uploaded</h3>
            <p>Upload an image or start camera detection to begin scanning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary(summary: DetectionSummary) -> None:
    status_class = "none" if summary.total_bills == 0 else "good"

    st.markdown(
        f"""
        <div class="result-summary">
            <div class="status-pill {status_class}">● {summary.status}</div>
            <p><strong>Old ₱1000 bills:</strong> {summary.old_count}</p>
            <p><strong>New ₱1000 bills:</strong> {summary.new_count}</p>
            <p><strong>Total ₱1000 bills:</strong> {summary.total_bills}</p>
            <p><strong>Total monetary amount:</strong> ₱{summary.total_amount:,}</p>
            <p><strong>Average confidence:</strong> {summary.average_confidence * 100:.2f}%</p>
            <p><strong>Scan time:</strong> {summary.scan_time}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, value: str, help_text: str, value_class: str = "") -> None:
    st.markdown(
        f"""
        <div class="breakdown-card">
            <div class="card-title">{title}</div>
            <div class="thin-line"></div>
            <div class="card-value {value_class}">{value}</div>
            <div class="card-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_breakdown(summary: Optional[DetectionSummary]) -> None:
    st.markdown("<div class='section-title'>Scan Breakdown</div>", unsafe_allow_html=True)

    if summary is None:
        old, new, total, amount, conf, status = "—", "—", "—", "—", "—", "Waiting"
        old_help = "Run a scan to count old ₱1000 bills."
        new_help = "Run a scan to count new ₱1000 bills."
        total_help = "Total detected bills will appear here."
        amount_help = "Computed total value will appear here."
        conf_help = "Average detection confidence."
        status_help = "Waiting for image or camera capture."
    else:
        old = str(summary.old_count)
        new = str(summary.new_count)
        total = str(summary.total_bills)
        amount = f"₱{summary.total_amount:,}"
        conf = f"{summary.average_confidence * 100:.1f}%"
        status = summary.status
        old_help = "Number of old Philippine ₱1000 bills detected."
        new_help = "Number of new Philippine ₱1000 bills detected."
        total_help = "Old and new ₱1000 bills combined."
        amount_help = "Total bills multiplied by ₱1,000."
        conf_help = "Average confidence of valid detections."
        status_help = "Final scan result."

    row1 = st.columns(3)

    with row1[0]:
        render_card("Old ₱1000 Bill Detection", old, old_help, "red")

    with row1[1]:
        render_card("New ₱1000 Bill Detection", new, new_help)

    with row1[2]:
        render_card("Total Bill Count", total, total_help, "dark")

    row2 = st.columns(3)

    with row2[0]:
        render_card("Total Amount", amount, amount_help, "dark")

    with row2[1]:
        render_card("Confidence Score", conf, conf_help)

    with row2[2]:
        render_card("Detection Status", status, status_help, "dark")