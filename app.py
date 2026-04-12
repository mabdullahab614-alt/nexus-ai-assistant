import gradio as gr
from groq import Groq
import datetime
import os

# ✅ API key is read from environment variable
# For local use: set GROQ_API_KEY in your system
# For Hugging Face: add GROQ_API_KEY in Settings → Secrets
API_KEY = os.environ.get("GROQ_API_KEY", "")
if not API_KEY:
    raise ValueError("Please set your GROQ_API_KEY environment variable!")

client = Groq(api_key=API_KEY)

MODELS = {
    "⚡ LLaMA 3.3 70B — Best Quality": "llama-3.3-70b-versatile",
    "🚀 LLaMA 3.1 8B — Ultra Fast": "llama-3.1-8b-instant",
    "🧩 Mixtral 8x7B — Best Reasoning": "mixtral-8x7b-32768",
    "🎨 Gemma 2 9B — Creative Tasks": "gemma2-9b-it",
}

PERSONAS = {
    "🤖 Default Assistant": "You are a helpful, smart, and friendly AI assistant. Answer clearly and concisely.",
    "🔬 Expert Researcher": "You are an expert researcher. Provide detailed, analytical, well-structured answers with citations where possible.",
    "💻 Coding Expert": "You are a senior software engineer. Write clean, well-commented, production-ready code and always explain it step by step.",
    "✍️ Creative Writer": "You are a creative writing expert. Be imaginative, vivid, and expressive in your writing.",
    "🎯 Career Coach": "You are a professional career coach. Help with CVs, LinkedIn bios, interview preparation, and career strategies.",
}

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

:root {
    --neon-cyan: #00f5ff;
    --neon-purple: #bf00ff;
    --neon-pink: #ff006e;
    --neon-green: #00ff88;
    --dark-bg: #020408;
    --border-glow: rgba(0, 245, 255, 0.3);
}

body, .gradio-container {
    background: var(--dark-bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(0, 245, 255, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(191, 0, 255, 0.08) 0%, transparent 50%),
        linear-gradient(180deg, #020408 0%, #040d1a 50%, #020408 100%) !important;
    min-height: 100vh !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.gradio-container::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0, 245, 255, 0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 245, 255, 0.025) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridMove 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes gridMove {
    0% { transform: translateY(0); }
    100% { transform: translateY(60px); }
}

.app-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 3em !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 50%, var(--neon-pink) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: 4px !important;
    animation: titlePulse 3s ease-in-out infinite;
}

@keyframes titlePulse {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(0, 245, 255, 0.5)); }
    50% { filter: drop-shadow(0 0 40px rgba(191, 0, 255, 0.8)); }
}

.neon-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-purple), var(--neon-pink), transparent);
    margin: 16px 0;
    animation: dividerFlow 3s linear infinite;
    background-size: 200% 100%;
}

@keyframes dividerFlow {
    0% { background-position: 0% 0%; }
    100% { background-position: 200% 0%; }
}

label {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.68em !important;
    color: var(--neon-cyan) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

textarea, input[type="text"] {
    background: rgba(0, 15, 30, 0.95) !important;
    border: 1px solid rgba(0, 245, 255, 0.2) !important;
    color: #e0f8ff !important;
    border-radius: 12px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05em !important;
    transition: all 0.3s ease !important;
    caret-color: var(--neon-cyan) !important;
}

textarea:focus, input[type="text"]:focus {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.2) !important;
    outline: none !important;
}

button.primary {
    background: linear-gradient(135deg, #00c4ff, #bf00ff) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(0, 196, 255, 0.4) !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0, 196, 255, 0.6) !important;
}

button.secondary {
    background: transparent !important;
    border: 1px solid rgba(255, 0, 110, 0.4) !important;
    border-radius: 12px !important;
    color: var(--neon-pink) !important;
    font-family: 'Orbitron', monospace !important;
    transition: all 0.3s ease !important;
}

button.secondary:hover {
    background: rgba(255, 0, 110, 0.1) !important;
    border-color: var(--neon-pink) !important;
    box-shadow: 0 0 15px rgba(255, 0, 110, 0.3) !important;
}

.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--neon-green);
    border-radius: 50%;
    margin-right: 6px;
    animation: statusPulse 2s ease-in-out infinite;
    box-shadow: 0 0 8px var(--neon-green);
}

@keyframes statusPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.6; }
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: rgba(0, 10, 20, 0.5); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple));
    border-radius: 3px;
}

footer { display: none !important; }
"""

def chat(message, history, model_name, persona, use_search, temperature):
    if not message.strip():
        return "", history

    model_id = MODELS.get(model_name, "llama-3.3-70b-versatile")
    persona_prompt = PERSONAS.get(persona, list(PERSONAS.values())[0])
    now = datetime.datetime.now().strftime("%A, %B %d, %Y at %H:%M")

    system = f"""{persona_prompt}

Today is: {now}.
You are a powerful AI assistant with access to real-time information.
Always give direct, accurate, and helpful answers.
If you have web search results, use them — never say you lack real-time access."""

    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})

    try:
        chosen_model = "compound-beta" if use_search else model_id
        response = client.chat.completions.create(
            model=chosen_model,
            messages=messages,
            temperature=temperature,
            max_tokens=2048,
        )
        reply = response.choices[0].message.content
        executed_tools = getattr(response.choices[0].message, 'executed_tools', None)
        if executed_tools and use_search:
            reply = "🌐 *Live web search used*\n\n" + reply
        history.append((message, reply))
        return "", history

    except Exception as e:
        try:
            response2 = client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temperature,
                max_tokens=2048,
            )
            reply = response2.choices[0].message.content
            history.append((message, f"🧠 *Using {model_name}*\n\n{reply}"))
            return "", history
        except Exception as e2:
            history.append((message, f"❌ Error: {str(e2)}"))
            return "", history

def clear_chat():
    return [], ""

def get_stats(history):
    if not history:
        return "_Awaiting transmission..._"
    words = sum(len(h[1].split()) for h in history)
    return f"<span class='status-dot'></span> **{len(history)}** messages &nbsp;·&nbsp; **{words:,}** words processed"

with gr.Blocks(
    title="⚡ NEXUS AI — Live Intelligence",
    theme=gr.themes.Base(),
    css=CUSTOM_CSS,
) as app:

    gr.HTML("""
    <div style="text-align:center; padding:36px 20px 10px; position:relative; z-index:1;">
        <div class="app-title">⚡ NEXUS AI</div>
        <div style="font-family:'Share Tech Mono',monospace; color:#00ff88; font-size:0.85em;
                    letter-spacing:3px; margin-top:6px;">
            ▸ LIVE INTELLIGENCE · GROQ POWERED · REAL-TIME WEB ACCESS ◂
        </div>
        <div class="neon-divider" style="margin-top:18px;"></div>
    </div>
    """)

    with gr.Row(equal_height=False):

        with gr.Column(scale=1):

            gr.HTML("""
            <div style="background:rgba(5,15,30,0.9); border:1px solid rgba(0,245,255,0.25);
                        border-radius:16px; padding:16px; margin-bottom:8px;">
            <h3 style="font-family:'Orbitron',monospace; color:#00f5ff; font-size:0.72em;
                       letter-spacing:3px; margin:0; border-bottom:1px solid rgba(0,245,255,0.2);
                       padding-bottom:8px;">
                ⚙ CONTROL PANEL
            </h3>
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

            use_search = gr.Checkbox(
                label="🌐 LIVE WEB INTELLIGENCE",
                value=True,
                info="ON = real-time web  |  OFF = pure model speed"
            )

            temperature = gr.Slider(
                label="🌡 CREATIVITY INDEX",
                minimum=0.1, maximum=1.5, value=0.7, step=0.1
            )

            gr.HTML('<div class="neon-divider"></div>')
            clear_btn = gr.Button("⚠ CLEAR TRANSMISSION", variant="secondary", size="sm")
            stats_box = gr.Markdown("_Awaiting transmission..._")
            gr.HTML('<div class="neon-divider"></div>')

            gr.Markdown("""
### 🧠 ENGINES
- **LLaMA 3.3 70B** — Maximum quality
- **LLaMA 3.1 8B** — Hyperspeed
- **Mixtral 8x7B** — Deep reasoning
- **Gemma 2 9B** — Creative mode

### 🎭 OPERATIVE MODES
- **Default** — General intelligence
- **Researcher** — Deep analysis
- **Coding Expert** — Build anything
- **Creative Writer** — Storytelling
- **Career Coach** — LinkedIn & CV

### 💡 PRO TIPS
- 🌐 **Search ON** → Real-time live data
- 🔒 **Search OFF** → Pure model speed
- News / prices / scores → **turn ON**
- Code / stories / CV → **turn OFF**
            """)

        with gr.Column(scale=2):

            gr.HTML("""
            <div style="background:rgba(5,15,30,0.9); border:1px solid rgba(0,245,255,0.2);
                        border-radius:16px; padding:6px 22px 10px; margin-bottom:8px;">
            <h3 style="font-family:'Orbitron',monospace; color:#00f5ff; font-size:0.72em;
                       letter-spacing:3px; margin:12px 0 2px 0;">
                💬 NEURAL INTERFACE
            </h3>
            </div>
            """)

            chatbot = gr.Chatbot(
                label="CHATBOT",
                height=500,
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    label="",
                    placeholder="⟩ Transmit your query... Bitcoin price · AI news · Write Python code · LinkedIn bio",
                    lines=3,
                    scale=4,
                    container=False,
                )
                send_btn = gr.Button("SEND ➤", variant="primary", scale=1)

            gr.HTML("""
            <div style="margin-top:10px; padding:10px 16px;
                        background:rgba(0,245,255,0.03);
                        border-left:3px solid rgba(0,245,255,0.35);
                        border-radius:0 8px 8px 0;">
                <span style="font-family:'Share Tech Mono',monospace; color:rgba(0,245,255,0.55);
                             font-size:0.8em; letter-spacing:1px;">
                ⟩ TRY:
                <span style="color:#00ff88;">Bitcoin price today</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">PSL 2026 results</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">Write Python face detector</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">Latest AI news 2026</span> &nbsp;|&nbsp;
                <span style="color:#00ff88;">Write my LinkedIn bio</span>
                </span>
            </div>
            """)

    gr.HTML("""
    <div style="text-align:center; padding:16px 0 8px;">
        <div class="neon-divider"></div>
        <p style="font-family:'Share Tech Mono',monospace; color:rgba(0,245,255,0.25);
                  font-size:0.72em; letter-spacing:2px; margin-top:10px;">
            NEXUS AI &nbsp;·&nbsp; POWERED BY GROQ &nbsp;·&nbsp;
            BUILT WITH ⚡ BY ABDULLAH &nbsp;·&nbsp; UMT LAHORE
        </p>
    </div>
    """)

    send_btn.click(
        fn=chat,
        inputs=[msg_input, chatbot, model_dd, persona_dd, use_search, temperature],
        outputs=[msg_input, chatbot],
    ).then(fn=get_stats, inputs=[chatbot], outputs=[stats_box])

    msg_input.submit(
        fn=chat,
        inputs=[msg_input, chatbot, model_dd, persona_dd, use_search, temperature],
        outputs=[msg_input, chatbot],
    ).then(fn=get_stats, inputs=[chatbot], outputs=[stats_box])

    clear_btn.click(fn=clear_chat, outputs=[chatbot, msg_input])

app.launch()