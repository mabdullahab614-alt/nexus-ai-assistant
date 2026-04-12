import gradio as gr
from groq import Groq
import datetime
import os
import json
import base64
import tempfile

# ── API ──────────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("GROQ_API_KEY", "")
client  = Groq(api_key=API_KEY)

# ── MODELS ───────────────────────────────────────────────────────────────────
MODELS = {
    "⚡ LLaMA 3.3 70B — Best Quality":  "llama-3.3-70b-versatile",
    "🚀 LLaMA 3.1 8B — Ultra Fast":     "llama-3.1-8b-instant",
    "🧩 Mixtral 8x7B — Best Reasoning": "mixtral-8x7b-32768",
    "🎨 Gemma 2 9B — Creative Tasks":   "gemma2-9b-it",
}
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ── PERSONAS ─────────────────────────────────────────────────────────────────
PERSONAS = {
    "🤖 Default Assistant": "You are a helpful, smart, and friendly AI assistant. Answer clearly and concisely.",
    "🔬 Expert Researcher":  "You are an expert researcher. Provide detailed, analytical, well-structured answers with citations where possible.",
    "💻 Coding Expert":      "You are a senior software engineer. Write clean, well-commented, production-ready code and always explain it step by step.",
    "✍️ Creative Writer":    "You are a creative writing expert. Be imaginative, vivid, and expressive in your writing.",
    "🎯 Career Coach":       "You are a professional career coach. Help with CVs, LinkedIn bios, interview preparation, and career strategies.",
}

# ── LANGUAGES ────────────────────────────────────────────────────────────────
LANGUAGES = {
    "🇺🇸 English":   "English",
    "🇵🇰 Urdu":      "Urdu",
    "🇸🇦 Arabic":    "Arabic",
    "🇫🇷 French":    "French",
    "🇩🇪 German":    "German",
    "🇪🇸 Spanish":   "Spanish",
    "🇨🇳 Chinese":   "Chinese",
    "🇯🇵 Japanese":  "Japanese",
    "🇷🇺 Russian":   "Russian",
    "🇮🇳 Hindi":     "Hindi",
}

# ── THEMES ───────────────────────────────────────────────────────────────────
THEMES_JS = {
    "⚡ Cyberpunk":   {"--neon-cyan":"#00f5ff","--neon-purple":"#bf00ff","--neon-pink":"#ff006e","--neon-green":"#00ff88","--dark-bg":"#020408"},
    "🌊 Ocean Deep":  {"--neon-cyan":"#00cfff","--neon-purple":"#0055ff","--neon-pink":"#00ffcc","--neon-green":"#00ffaa","--dark-bg":"#020d1a"},
    "🌿 Matrix":      {"--neon-cyan":"#00ff41","--neon-purple":"#008f11","--neon-pink":"#00cc33","--neon-green":"#00ff41","--dark-bg":"#000300"},
    "🌅 Sunset":      {"--neon-cyan":"#ff6b35","--neon-purple":"#f7931e","--neon-pink":"#ff006e","--neon-green":"#ffbe0b","--dark-bg":"#0a0005"},
    "🌸 Sakura":      {"--neon-cyan":"#ff79c6","--neon-purple":"#bd93f9","--neon-pink":"#ff5555","--neon-green":"#50fa7b","--dark-bg":"#0d0014"},
}
THEME_SWITCH_JS = f"""
(theme) => {{
    const themes = {json.dumps(THEMES_JS)};
    const vars = themes[theme];
    if (vars) Object.entries(vars).forEach(([k,v]) => document.documentElement.style.setProperty(k, v));
}}
"""
TTS_JS = """
(history) => {
    if (!history || history.length === 0) return;
    const raw = history[history.length - 1][1] || "";
    const chars = ["*","_","`","#",">","~","[","]","\\n"];
    let text = raw;
    chars.forEach(c => { text = text.split(c).join(" "); });
    text = text.replace(/  +/g, " ").trim();
    if (!text) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 0.92; u.pitch = 1.05;
    window.speechSynthesis.speak(u);
}
"""
TTS_STOP_JS = "() => { window.speechSynthesis.cancel(); }"

# ── CSS ───────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

:root {
    --neon-cyan:   #00f5ff;
    --neon-purple: #bf00ff;
    --neon-pink:   #ff006e;
    --neon-green:  #00ff88;
    --dark-bg:     #020408;
    --border-glow: rgba(0,245,255,0.3);
}

body, .gradio-container {
    background: var(--dark-bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(0,245,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(191,0,255,0.08) 0%, transparent 50%),
        linear-gradient(180deg,#020408 0%,#040d1a 50%,#020408 100%) !important;
    min-height:100vh !important;
    font-family:'Rajdhani',sans-serif !important;
}

.gradio-container::before {
    content:''; position:fixed; top:0; left:0; width:100%; height:100%;
    background-image:
        linear-gradient(rgba(0,245,255,0.025) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,245,255,0.025) 1px,transparent 1px);
    background-size:60px 60px;
    animation:gridMove 20s linear infinite;
    pointer-events:none; z-index:0;
}
@keyframes gridMove { 0%{transform:translateY(0)} 100%{transform:translateY(60px)} }

.app-title {
    font-family:'Orbitron',monospace !important; font-size:3em !important; font-weight:900 !important;
    background:linear-gradient(135deg,var(--neon-cyan) 0%,var(--neon-purple) 50%,var(--neon-pink) 100%) !important;
    -webkit-background-clip:text !important; -webkit-text-fill-color:transparent !important;
    background-clip:text !important; letter-spacing:4px !important;
    animation:titlePulse 3s ease-in-out infinite;
}
@keyframes titlePulse {
    0%,100%{filter:drop-shadow(0 0 20px rgba(0,245,255,0.5))}
    50%{filter:drop-shadow(0 0 40px rgba(191,0,255,0.8))}
}

.neon-divider {
    height:2px;
    background:linear-gradient(90deg,transparent,var(--neon-cyan),var(--neon-purple),var(--neon-pink),transparent);
    margin:16px 0; animation:dividerFlow 3s linear infinite; background-size:200% 100%;
}
@keyframes dividerFlow { 0%{background-position:0% 0%} 100%{background-position:200% 0%} }

label {
    font-family:'Orbitron',monospace !important; font-size:0.68em !important;
    color:var(--neon-cyan) !important; letter-spacing:2px !important; text-transform:uppercase !important;
}

textarea, input[type="text"] {
    background:rgba(0,15,30,0.95) !important; border:1px solid rgba(0,245,255,0.2) !important;
    color:#e0f8ff !important; border-radius:12px !important; font-family:'Rajdhani',sans-serif !important;
    font-size:1.05em !important; transition:all 0.3s ease !important; caret-color:var(--neon-cyan) !important;
}
textarea:focus, input[type="text"]:focus {
    border-color:var(--neon-cyan) !important;
    box-shadow:0 0 20px rgba(0,245,255,0.2) !important; outline:none !important;
}

button.primary {
    background:linear-gradient(135deg,#00c4ff,#bf00ff) !important; border:none !important;
    border-radius:12px !important; color:white !important;
    font-family:'Orbitron',monospace !important; font-weight:700 !important;
    letter-spacing:2px !important; transition:all 0.3s ease !important;
    box-shadow:0 0 20px rgba(0,196,255,0.4) !important;
}
button.primary:hover { transform:translateY(-2px) !important; box-shadow:0 8px 30px rgba(0,196,255,0.6) !important; }

button.secondary {
    background:transparent !important; border:1px solid rgba(255,0,110,0.4) !important;
    border-radius:12px !important; color:var(--neon-pink) !important;
    font-family:'Orbitron',monospace !important; transition:all 0.3s ease !important;
}
button.secondary:hover {
    background:rgba(255,0,110,0.1) !important; border-color:var(--neon-pink) !important;
    box-shadow:0 0 15px rgba(255,0,110,0.3) !important;
}

.status-dot {
    display:inline-block; width:8px; height:8px; background:var(--neon-green);
    border-radius:50%; margin-right:6px; animation:statusPulse 2s ease-in-out infinite;
    box-shadow:0 0 8px var(--neon-green);
}
@keyframes statusPulse {
    0%,100%{transform:scale(1);opacity:1} 50%{transform:scale(1.5);opacity:0.6}
}

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:rgba(0,10,20,0.5)}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--neon-cyan),var(--neon-purple));border-radius:3px}

footer{display:none !important}
"""

# ── HELPERS ───────────────────────────────────────────────────────────────────
def get_stats(history):
    if not history:
        return "_Awaiting transmission..._"
    words = sum(len((h[1] or "").split()) for h in history)
    return f"<span class='status-dot'></span> **{len(history)}** messages &nbsp;·&nbsp; **{words:,}** words processed"

def clear_chat():
    return [], "", None

def export_txt(history):
    if not history:
        return None
    lines = ["╔══════════════════════════════════════════╗\n",
             "║         NEXUS AI — CHAT EXPORT           ║\n",
             f"║  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}                          ║\n",
             "╚══════════════════════════════════════════╝\n\n"]
    for i, (u, b) in enumerate(history, 1):
        lines.append(f"[MSG {i}] YOU:\n{u or ''}\n\n")
        lines.append(f"[MSG {i}] NEXUS:\n{b or ''}\n\n")
        lines.append("─" * 50 + "\n\n")
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.writelines(lines)
    tmp.close()
    return tmp.name

def save_json(history):
    if not history:
        return None
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(history, tmp, ensure_ascii=False, indent=2)
    tmp.close()
    return tmp.name

def load_json(file):
    if file is None:
        return []
    try:
        if isinstance(file, dict):
            path = file.get("name", "")
        elif hasattr(file, "name"):
            path = file.name
        else:
            path = str(file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []

# ── CHAT ─────────────────────────────────────────────────────────────────────
def chat(message, history, model_name, persona, use_search, temperature, language, image_file):
    message = message or ""
    if not message.strip() and image_file is None:
        return "", history, None

    model_id      = MODELS.get(model_name, "llama-3.3-70b-versatile")
    persona_prompt = PERSONAS.get(persona, list(PERSONAS.values())[0])
    lang           = LANGUAGES.get(language, "English")
    now            = datetime.datetime.now().strftime("%A, %B %d, %Y at %H:%M")

    system = f"""{persona_prompt}

Today is: {now}.
IMPORTANT: Always respond in {lang} language only, unless the user explicitly asks you to switch.
You are a powerful AI assistant with access to real-time information.
Always give direct, accurate, and helpful answers."""

    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append({"role": "user",      "content": h[0] or ""})
        messages.append({"role": "assistant", "content": h[1] or ""})

    use_vision = False
    if image_file is not None:
        try:
            with open(image_file, "rb") as f:
                img_bytes = f.read()
            img_b64  = base64.b64encode(img_bytes).decode("utf-8")
            ext      = image_file.split(".")[-1].lower()
            mime     = {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png",
                        "gif":"image/gif","webp":"image/webp"}.get(ext, "image/jpeg")
            user_content = [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                {"type": "text",      "text": message.strip() or "Please analyse this image in detail."},
            ]
            messages.append({"role": "user", "content": user_content})
            use_vision = True
        except Exception as img_err:
            messages.append({"role": "user", "content": f"{message}\n\n[Image could not be loaded: {img_err}]"})
    else:
        messages.append({"role": "user", "content": message})

    try:
        if use_vision:
            chosen = VISION_MODEL
        elif use_search:
            chosen = "compound-beta"
        else:
            chosen = model_id

        response = client.chat.completions.create(
            model=chosen, messages=messages, temperature=temperature, max_tokens=2048,
        )
        reply = response.choices[0].message.content or "⚠️ No response content received."

        if use_search and not use_vision:
            executed_tools = getattr(response.choices[0].message, "executed_tools", None)
            if executed_tools:
                reply = "🌐 *Live web search used*\n\n" + reply

        display_user = message.strip() if message.strip() else "📷 [Image uploaded for analysis]"
        history.append((display_user, reply))
        return "", history, None

    except Exception:
        try:
            safe_msgs = []
            for m in messages:
                content = m.get("content")
                if isinstance(content, str):
                    safe_msgs.append(m)
                elif isinstance(content, list):
                    # Extract text parts from multimodal message (image + text)
                    text_parts = [p["text"] for p in content if isinstance(p, dict) and p.get("type") == "text"]
                    if text_parts:
                        safe_msgs.append({"role": m["role"], "content": " ".join(text_parts)})
            r2 = client.chat.completions.create(
                model=model_id, messages=safe_msgs, temperature=temperature, max_tokens=2048,
            )
            reply = r2.choices[0].message.content or "⚠️ No response content received."
            display_user = message.strip() if message.strip() else "📷 [Image uploaded]"
            history.append((display_user, f"🧠 *Using {model_name}*\n\n{reply}"))
            return "", history, None
        except Exception as e2:
            history.append((message or "[image]", f"❌ Error: {str(e2)}"))
            return "", history, None

# ── UI ────────────────────────────────────────────────────────────────────────
with gr.Blocks(
    title="⚡ NEXUS AI — Live Intelligence",
    theme=gr.themes.Base(),
    css=CUSTOM_CSS,
) as app:

    # ── Header ──
    gr.HTML("""
    <div style="text-align:center;padding:36px 20px 10px;position:relative;z-index:1;">
        <div class="app-title">⚡ NEXUS AI</div>
        <div style="font-family:'Share Tech Mono',monospace;color:#00ff88;font-size:0.85em;
                    letter-spacing:3px;margin-top:6px;">
            ▸ LIVE INTELLIGENCE · GROQ POWERED · REAL-TIME WEB ACCESS ◂
        </div>
        <div class="neon-divider" style="margin-top:18px;"></div>
    </div>
    """)

    with gr.Row(equal_height=False):

        # ── Left Sidebar ──
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background:rgba(5,15,30,0.9);border:1px solid rgba(0,245,255,0.25);
                        border-radius:16px;padding:16px;margin-bottom:8px;">
            <h3 style="font-family:'Orbitron',monospace;color:#00f5ff;font-size:0.72em;
                       letter-spacing:3px;margin:0;border-bottom:1px solid rgba(0,245,255,0.2);
                       padding-bottom:8px;">⚙ CONTROL PANEL</h3>
            </div>
            """)

            model_dd = gr.Dropdown(
                label="🧠 AI ENGINE",
                choices=list(MODELS.keys()),
                value=list(MODELS.keys())[0],
            )
            persona_dd = gr.Dropdown(
                label="🎭 OPERATIVE MODE",
                choices=list(PERSONAS.keys()),
                value=list(PERSONAS.keys())[0],
            )

            # ── NEW: Language ──
            language_dd = gr.Dropdown(
                label="🌍 RESPONSE LANGUAGE",
                choices=list(LANGUAGES.keys()),
                value="🇺🇸 English",
            )

            # ── NEW: Theme ──
            theme_dd = gr.Dropdown(
                label="🎨 INTERFACE THEME",
                choices=list(THEMES_JS.keys()),
                value="⚡ Cyberpunk",
            )

            use_search = gr.Checkbox(
                label="🌐 LIVE WEB INTELLIGENCE",
                value=True,
                info="ON = real-time web  |  OFF = pure model speed",
            )
            temperature = gr.Slider(
                label="🌡 CREATIVITY INDEX",
                minimum=0.1, maximum=1.5, value=0.7, step=0.1,
            )

            gr.HTML('<div class="neon-divider"></div>')
            clear_btn = gr.Button("⚠ CLEAR TRANSMISSION", variant="secondary", size="sm")
            stats_box = gr.Markdown("_Awaiting transmission..._")
            gr.HTML('<div class="neon-divider"></div>')

            # ── NEW: Save / Load / Export ──
            gr.HTML("""<p style="font-family:'Orbitron',monospace;color:#00f5ff;
                                  font-size:0.65em;letter-spacing:2px;">💾 CONVERSATION VAULT</p>""")
            with gr.Row():
                save_btn   = gr.Button("💾 Save",   variant="secondary", size="sm")
                export_btn = gr.Button("📋 Export", variant="secondary", size="sm")
            load_file   = gr.File(label="📂 Load Conversation (.json)", file_types=[".json"])
            save_output = gr.File(label="📥 Download File", visible=True)

            # ── NEW: TTS ──
            gr.HTML('<div class="neon-divider"></div>')
            gr.HTML("""<p style="font-family:'Orbitron',monospace;color:#00f5ff;
                                  font-size:0.65em;letter-spacing:2px;">🔊 VOICE OUTPUT</p>""")
            with gr.Row():
                tts_btn      = gr.Button("🔊 Speak Last", variant="secondary", size="sm")
                tts_stop_btn = gr.Button("⏹ Stop",        variant="secondary", size="sm")

            gr.HTML('<div class="neon-divider"></div>')
            gr.Markdown("""
### 🧠 ENGINES
- **LLaMA 3.3 70B** — Maximum quality
- **LLaMA 3.1 8B** — Hyperspeed
- **Mixtral 8x7B** — Deep reasoning
- **Gemma 2 9B** — Creative mode

### ✨ NEW FEATURES
- 📁 **Image Upload** — Analyse any image
- 🌍 **10 Languages** — Reply in your language
- 🎨 **5 Themes** — Change the look
- 💾 **Save / Load** — Keep your chats
- 📋 **Export TXT** — Download history
- 🔊 **TTS** — Hear the last reply
            """)

        # ── Main Chat ──
        with gr.Column(scale=2):
            gr.HTML("""
            <div style="background:rgba(5,15,30,0.9);border:1px solid rgba(0,245,255,0.2);
                        border-radius:16px;padding:6px 22px 10px;margin-bottom:8px;">
            <h3 style="font-family:'Orbitron',monospace;color:#00f5ff;font-size:0.72em;
                       letter-spacing:3px;margin:12px 0 2px 0;">💬 NEURAL INTERFACE</h3>
            </div>
            """)

            chatbot = gr.Chatbot(label="CHATBOT", height=460, type="tuples")

            # ── NEW: Image Upload ──
            image_input = gr.Image(
                label="📁 ATTACH IMAGE (optional — auto-activates vision model)",
                type="filepath",
                sources=["upload"],
                height=120,
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    label="",
                    placeholder="⟩ Transmit your query... Bitcoin price · AI news · Write Python code · LinkedIn bio",
                    lines=3, scale=4, container=False,
                )
                send_btn = gr.Button("SEND ➤", variant="primary", scale=1)

            gr.HTML("""
            <div style="margin-top:10px;padding:10px 16px;
                        background:rgba(0,245,255,0.03);
                        border-left:3px solid rgba(0,245,255,0.35);
                        border-radius:0 8px 8px 0;">
                <span style="font-family:'Share Tech Mono',monospace;color:rgba(0,245,255,0.55);
                             font-size:0.8em;letter-spacing:1px;">
                ⟩ TRY:
                <span style="color:#00ff88;">Bitcoin price today</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">PSL 2026 results</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">Write Python face detector</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">Latest AI news 2026</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">Upload an image to analyse it</span>
                </span>
            </div>
            """)

    # ── Footer ──
    gr.HTML("""
    <div style="text-align:center;padding:16px 0 8px;">
        <div class="neon-divider"></div>
        <p style="font-family:'Share Tech Mono',monospace;color:rgba(0,245,255,0.25);
                  font-size:0.72em;letter-spacing:2px;margin-top:10px;">
            NEXUS AI &nbsp;·&nbsp; POWERED BY GROQ &nbsp;·&nbsp;
            BUILT WITH ⚡ BY ABDULLAH &nbsp;·&nbsp; UMT LAHORE
        </p>
    </div>
    """)

    # ── Event Wiring ──────────────────────────────────────────────────────────
    chat_inputs  = [msg_input, chatbot, model_dd, persona_dd, use_search, temperature, language_dd, image_input]
    chat_outputs = [msg_input, chatbot, image_input]

    send_btn.click(fn=chat, inputs=chat_inputs, outputs=chat_outputs).then(
        fn=get_stats, inputs=[chatbot], outputs=[stats_box]
    )
    msg_input.submit(fn=chat, inputs=chat_inputs, outputs=chat_outputs).then(
        fn=get_stats, inputs=[chatbot], outputs=[stats_box]
    )
    clear_btn.click(fn=clear_chat, outputs=[chatbot, msg_input, image_input])

    # Theme switching (pure JS — no server round-trip)
    theme_dd.change(fn=None, inputs=[theme_dd], outputs=[], js=THEME_SWITCH_JS)

    # TTS (pure JS)
    tts_btn.click(fn=None, inputs=[chatbot], outputs=[], js=TTS_JS)
    tts_stop_btn.click(fn=None, inputs=[], outputs=[], js=TTS_STOP_JS)

    # Save / Export
    save_btn.click(fn=save_json,    inputs=[chatbot], outputs=[save_output])
    export_btn.click(fn=export_txt, inputs=[chatbot], outputs=[save_output])

    # Load conversation
    load_file.change(fn=load_json, inputs=[load_file], outputs=[chatbot]).then(
        fn=get_stats, inputs=[chatbot], outputs=[stats_box]
    )

app.launch()
