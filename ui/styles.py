import streamlit as st


def apply_styles() -> None:
    """Apply the Juriscloud reference UI to the Streamlit application."""

    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --jc-page: #f5fbff;
    --jc-sidebar: #f0f9ff;
    --jc-card: #fdfcff;
    --jc-border: #d8e7f4;
    --jc-primary: #2563eb;
    --jc-primary-dark: #1d4ed8;
    --jc-heading: #0f172a;
    --jc-text: #475569;
    --jc-muted: #64748b;
    --jc-faint: #94a3b8;
    --jc-success: #10b981;
}

html { scroll-behavior: auto !important; }

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif !important;
}

.stApp {
    color: var(--jc-text);
    background: var(--jc-page);
}

/* Remove Streamlit's blank application header. It remains after deployment
   unless it is explicitly collapsed. */
[data-testid="stHeader"] {
    height: 2.6rem !important;
    min-height: 2.6rem !important;
    background: transparent !important;
    pointer-events: none !important;
    overflow: visible !important;
}

[data-testid="stHeader"] button,
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] {
    pointer-events: auto !important;
}

/* Keep the reopen control available after the sidebar is collapsed. */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    position: fixed !important;
    top: 0.72rem !important;
    left: 0.72rem !important;
    z-index: 1000000 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.3rem !important;
    height: 2.3rem !important;
    border: 1px solid rgba(186, 230, 253, 0.92) !important;
    border-radius: 0.72rem !important;
    background: rgba(255, 255, 255, 0.96) !important;
    box-shadow: 0 6px 18px rgba(71, 85, 105, 0.12) !important;
}

[data-testid="stDecoration"],
#MainMenu,
footer { display: none !important; }

/* Current Streamlit renders the reopen control inside stToolbar. */
[data-testid="stToolbar"] {
    display: flex !important;
    visibility: visible !important;
    background: transparent !important;
    pointer-events: auto !important;
}

[data-testid="stToolbar"] [data-testid="stAppDeployButton"],
[data-testid="stToolbar"] [data-testid="stStatusWidget"],
[data-testid="stToolbar"] [data-testid="stMainMenu"] {
    display: none !important;
}

[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}

[data-testid="stExpandSidebarButton"] {
    position: fixed !important;
    top: 0.72rem !important;
    left: 0.72rem !important;
    z-index: 1000001 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.3rem !important;
    height: 2.3rem !important;
    border: 1px solid rgba(186, 230, 253, 0.92) !important;
    border-radius: 0.72rem !important;
    background: rgba(255, 255, 255, 0.97) !important;
    box-shadow: 0 6px 18px rgba(71, 85, 105, 0.12) !important;
}

[data-testid="stExpandSidebarButton"] button,
[data-testid="stSidebarCollapseButton"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.3rem !important;
    height: 2.3rem !important;
    min-height: 2.3rem !important;
    padding: 0 !important;
    overflow: visible !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background: var(--jc-page) !important; }

.block-container {
    width: min(100%, 52rem);
    max-width: 52rem;
    min-height: auto;
    padding: 1.45rem 1.65rem 2rem;
}

[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
    gap: 0.86rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    width: 17rem !important;
    min-width: 17rem !important;
    background: rgba(224, 242, 254, 0.5) !important;
    border-right: 1px solid rgba(186, 230, 253, 0.8);
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    position: absolute !important;
    top: 0.45rem !important;
    right: 0.45rem !important;
    z-index: 10 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    width: 2.3rem !important;
    height: 2.3rem !important;
    min-height: 2.3rem !important;
    padding: 0 !important;
    overflow: visible !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.3rem !important;
    height: 2.3rem !important;
    min-height: 2.3rem !important;
    padding: 0 !important;
    border: 1px solid rgba(186, 230, 253, 0.9) !important;
    border-radius: 0.72rem !important;
    background: rgba(255, 255, 255, 0.9) !important;
    overflow: visible !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.3rem !important;
    height: 2.3rem !important;
    overflow: visible !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding: 1rem 1rem 1rem !important;
    transform: none !important;
}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.82rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    margin: 0;
    padding: 0;
    color: #334155;
    font-size: 0.83rem;
    font-weight: 700;
    line-height: 1.35;
    letter-spacing: 0.045em;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--jc-muted);
    font-size: 0.81rem;
    line-height: 1.5;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
section[data-testid="stSidebar"] .stMarkdown p {
    font-size: 0.81rem !important;
    line-height: 1.5 !important;
}

section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] [role="radiogroup"] p {
    color: #526176 !important;
    font-size: 0.79rem !important;
    font-weight: 500 !important;
    line-height: 1.45 !important;
}

section[data-testid="stSidebar"] hr {
    margin: 0.7rem 0;
    border-color: rgba(186, 230, 253, 0.78);
}

.jurisource-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 0 0 0.5rem;
    padding: 0.15rem 0 1.15rem;
    border-bottom: 1px solid rgba(186, 230, 253, 0.78);
}

.jurisource-logo {
    display: inline-flex;
    flex: 0 0 auto;
    align-items: center;
    justify-content: center;
    width: auto;
    height: auto;
    padding: 0;
    border: 0;
    border-radius: 0;
    background: transparent;
    color: inherit;
    font-size: 1.65rem;
    line-height: 1;
    box-shadow: none;
}

.jurisource-brand-name {
    margin: 0;
    color: var(--jc-heading) !important;
    font-size: 2rem !important;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.018em;
}

.jurisource-brand-description {
    margin: 0.22rem 0 0;
    color: var(--jc-muted) !important;
    font-size: 0.81rem;
    font-weight: 500;
    line-height: 1.3;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] {
    border: 1px solid #a7f3d0 !important;
    border-radius: 0.75rem;
    background: #ecfdf5 !important;
    color: #087b58 !important;
    padding: 0.85rem 0.9rem !important;
    font-size: 0.79rem;
    line-height: 1.5;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] *,
section[data-testid="stSidebar"] [role="alert"] * {
    color: #087b58 !important;
    font-size: 0.79rem !important;
    line-height: 1.5 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    margin-top: -0.15rem;
    padding: 0;
    border-radius: 0.8rem;
    background: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    padding: 0.75rem !important;
    border: 1px solid rgba(186, 230, 253, 0.78) !important;
    border-radius: 0.8rem !important;
    background: #ffffff !important;
}

section[data-testid="stSidebar"]
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}

.juriscloud-upload-formats {
    margin: -0.35rem 0 0.2rem !important;
    color: #718198 !important;
    font-size: 0.76rem !important;
    font-weight: 400 !important;
    line-height: 1.35 !important;
    white-space: nowrap;
}

section[data-testid="stSidebar"] button {
    border-color: rgba(186, 230, 253, 0.78);
    border-radius: 0.72rem;
    background: rgba(255, 255, 255, 0.82);
    color: #475569;
    font-size: 0.79rem;
}

section[data-testid="stSidebar"] button p {
    font-size: 0.79rem !important;
    line-height: 1.35 !important;
}

.jurisource-file {
    margin-bottom: 0.46rem;
    padding: 0.7rem 0.72rem;
    border: 1px solid rgba(186, 230, 253, 0.72);
    border-left: 3px solid #90c9ff;
    border-radius: 0.72rem;
    background: rgba(255, 255, 255, 0.84);
    color: #475569;
    font-size: 0.72rem;
}

.jurisource-file-meta {
    margin-top: 0.2rem;
    color: var(--jc-faint);
    font-size: 0.62rem;
    line-height: 1.45;
}

.jurisource-system-status {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 0.4rem;
    padding: 0.52rem 0.68rem;
    border: 1px solid rgba(186, 230, 253, 0.78);
    border-radius: 0.72rem;
    background: rgba(255, 255, 255, 0.72);
    color: #64748b;
    font-size: 0.69rem;
    font-weight: 700;
    letter-spacing: 0.055em;
    text-transform: uppercase;
}

.jurisource-status-dot {
    display: inline-block;
    width: 0.46rem;
    height: 0.46rem;
    flex: 0 0 0.46rem;
    border-radius: 999px;
    background: var(--jc-success);
    box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
}

/* Language selector */
[data-testid="stMainBlockContainer"] [data-baseweb="select"] > div {
    border-color: transparent;
    border-radius: 0.72rem;
    background: rgba(255, 255, 255, 0.68);
    color: #475569;
    box-shadow: none;
}

/* Hero */
.juriscloud-hero {
    margin: 0 auto 1.55rem;
    text-align: center;
}

.juriscloud-hero-title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.7rem;
}

.juriscloud-hero-cloud {
    font-size: 2.15rem;
    line-height: 1;
}

.juriscloud-hero h1 {
    margin: 0;
    color: var(--jc-heading);
    font-family: "Newsreader", Georgia, serif !important;
    font-size: clamp(2.25rem, 3.2vw, 2.85rem);
    font-weight: 500;
    letter-spacing: -0.045em;
    line-height: 1.02;
}

.juriscloud-hero p {
    max-width: 34rem;
    margin: 0.75rem auto 0;
    color: #718198;
    font-family: "Plus Jakarta Sans", sans-serif !important;
    font-size: 0.82rem;
    font-weight: 400;
    line-height: 1.55;
}

/* Prompt composer */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker) {
    border: 1px solid rgba(199, 220, 243, 0.92) !important;
    border-radius: 1.05rem !important;
    background: #ffffff !important;
    box-shadow:
        0 22px 48px -16px rgba(99, 102, 241, 0.29),
        0 12px 34px -8px rgba(14, 165, 233, 0.18),
        0 0 0 1px rgba(216, 208, 252, 0.62);
    transition: border-color 160ms ease, box-shadow 160ms ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker):focus-within {
    border-color: rgba(147, 197, 253, 0.9) !important;
    box-shadow:
        0 22px 48px -16px rgba(99, 102, 241, 0.28),
        0 12px 34px -8px rgba(14, 165, 233, 0.18),
        0 0 0 2px rgba(191, 219, 254, 0.62);
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker) > div {
    padding: 1rem 1.05rem 0.95rem !important;
    background: #ffffff !important;
}

.juriscloud-composer-marker { display: none; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stTextArea"] { margin: 0; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stTextArea"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stTextArea"] > div,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stTextArea"] > div > div,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-baseweb="textarea"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-baseweb="base-input"] {
    border: 0 !important;
    background: #ffffff !important;
    background-color: #ffffff !important;
    box-shadow: none !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
textarea {
    min-height: 6.4rem !important;
    padding: 0.45rem 0.3rem 0.7rem !important;
    border: 0 !important;
    outline: 0 !important;
    background: #ffffff !important;
    color: #334155 !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
    box-shadow: none !important;
    resize: none !important;
}

/* Override Streamlit/BaseWeb's tinted textarea surface. */
[data-testid="stMainBlockContainer"] [data-testid="stTextArea"],
[data-testid="stMainBlockContainer"] [data-testid="stTextArea"] > div,
[data-testid="stMainBlockContainer"] [data-testid="stTextArea"] [data-baseweb="base-input"],
[data-testid="stMainBlockContainer"] [data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    background-color: #ffffff !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stHorizontalBlock"] {
    align-items: center;
    gap: 0.4rem;
    padding-top: 0.72rem;
    border-top: 1px solid #edf2f7;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    width: auto !important;
    min-width: 0 !important;
    flex: 0 0 auto !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
    width: 5.8rem !important;
    min-width: 5.8rem !important;
    flex: 0 0 5.8rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child button {
    width: 100% !important;
    padding-right: 0.4rem !important;
    padding-left: 0.4rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(4) {
    flex: 1 1 auto !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(4) button {
    width: 100% !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
button {
    min-height: 2rem;
    padding-right: 0.65rem;
    padding-left: 0.65rem;
    border-color: rgba(226, 232, 240, 0.95);
    border-radius: 0.65rem;
    background: #f8fafc;
    color: #526176;
    font-size: 0.68rem;
    font-weight: 600;
    white-space: nowrap;
    box-shadow: none;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
button:hover {
    border-color: #bae6fd;
    background: #f0f9ff;
    color: #0369a1;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stBaseButton-primary"] {
    min-width: 2.1rem;
    border-color: var(--jc-primary);
    border-radius: 0.7rem;
    background: var(--jc-primary);
    color: white;
    font-size: 0.98rem;
    box-shadow: 0 7px 16px rgba(37, 99, 235, 0.22);
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
[data-testid="stBaseButton-primary"]:hover {
    border-color: var(--jc-primary-dark);
    background: var(--jc-primary-dark);
    color: white;
}

/* Suggestion chips */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
> [data-testid="stHorizontalBlock"] .stButton > button {
    min-height: 2rem;
    border-color: rgba(186, 230, 253, 0.85);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.9);
    color: #53657b;
    font-size: 0.67rem;
    font-weight: 500;
    box-shadow: 0 3px 12px rgba(14, 165, 233, 0.04);
}

[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]
> [data-testid="stHorizontalBlock"] .stButton > button:hover {
    border-color: #bae6fd;
    background: #f8fcff;
    color: #0369a1;
}

.jurisource-disclaimer {
    margin: 0.05rem 0 0.3rem;
    padding: 0.48rem 0.72rem;
    border: 1px solid rgba(186, 230, 253, 0.72);
    border-radius: 0.72rem;
    background: rgba(224, 242, 254, 0.58);
    color: #315e7f;
    font-size: 0.68rem;
    line-height: 1.45;
    text-align: center;
}

/* Chat and retrieval output */
[data-testid="stChatMessage"] {
    margin-bottom: 0.65rem;
    padding: 0.9rem 1rem;
    border: 1px solid rgba(186, 230, 253, 0.72);
    border-radius: 0.9rem;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 7px 20px rgba(14, 165, 233, 0.045);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #475569;
    font-size: 0.78rem;
    line-height: 1.7;
}

.jurisource-thinking {
    min-height: 90px;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.15rem;
    border: 1px solid rgba(186, 230, 253, 0.72);
    border-radius: 0.9rem;
    background: rgba(240, 249, 255, 0.88);
    color: #315e7f;
}

.jurisource-thinking-text {
    color: var(--jc-muted);
    font-size: 0.76rem;
}

@media (max-width: 900px) {
    .block-container { padding: 1rem 1.1rem 2rem; }
    .juriscloud-hero { margin-bottom: 1.4rem; }
    .juriscloud-hero h1 { font-size: 2.1rem; }
    .juriscloud-hero-cloud { font-size: 1.75rem; }
}

/* Preserve the one-screen layout on shorter laptop viewports. */
@media (max-height: 850px) and (min-width: 901px) {
    .block-container { padding-top: 0.85rem; padding-bottom: 1rem; }
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
        gap: 0.62rem;
    }
    .juriscloud-hero { margin-bottom: 0.95rem; }
    .juriscloud-hero p { margin-top: 0.5rem; }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.juriscloud-composer-marker)
    textarea { min-height: 5.45rem !important; }
    .jurisource-disclaimer { margin-bottom: 0.15rem; }
}
</style>
        """,
        unsafe_allow_html=True,
    )
