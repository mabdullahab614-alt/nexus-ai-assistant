# ⚡ NEXUS AI — Live Intelligence Hub

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.x-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Powered-00A67E?style=for-the-badge&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### A cyberpunk-themed AI assistant with real-time web search, vision, multilingual support, and more.

**[🚀 Try Live Demo](https://huggingface.co/spaces/BUDDDY2894830/nexus-ai-assistant)** &nbsp;·&nbsp; **[📋 LinkedIn Post](https://www.linkedin.com/in/abdullah-javid-b217a2384/)** &nbsp;·&nbsp; **[👨‍💻 Author](#author)**

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| ⚡ **4 AI Models** | LLaMA 3.3 70B, LLaMA 3.1 8B, Mixtral 8x7B, Gemma 2 9B |
| 🌐 **Live Web Search** | Real-time answers via Groq Compound Beta |
| 📁 **Image Analysis** | Upload any image — auto-activates LLaMA 4 Scout vision model |
| 🌍 **10 Languages** | English, Urdu, Arabic, French, German, Spanish, Chinese, Japanese, Russian, Hindi |
| 🎨 **5 UI Themes** | Cyberpunk, Ocean Deep, Matrix, Sunset, Sakura |
| 🎭 **5 AI Personas** | Default Assistant, Expert Researcher, Coding Expert, Creative Writer, Career Coach |
| 💾 **Save & Load Chats** | Export conversations as `.json` and reload them later |
| 📋 **Export History** | Download your full chat as a formatted `.txt` file |
| 🔊 **Text-to-Speech** | Hear the last AI reply read aloud via browser TTS |
| 🌡️ **Creativity Slider** | Adjust model temperature from 0.1 to 1.5 |

---

## 🖼️ Preview

> **Cyberpunk UI** with animated neon grid, glowing buttons, and real-time stats

```
⚡ NEXUS AI
▸ LIVE INTELLIGENCE · GROQ POWERED · REAL-TIME WEB ACCESS ◂
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **UI Framework:** Gradio 4.x
- **LLM Provider:** [Groq API](https://groq.com) (ultra-fast inference)
- **Models:** LLaMA 3.3 70B · LLaMA 3.1 8B · Mixtral 8x7B · Gemma 2 9B · LLaMA 4 Scout (vision)
- **Web Search:** Groq Compound Beta (built-in tool use)
- **Deployment:** Hugging Face Spaces

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/nexus-ai-assistant.git
cd nexus-ai-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key
```bash
# Option A: environment variable (recommended)
export GROQ_API_KEY=your_key_here

# Option B: edit app.py directly (not recommended for production)
```

Get a free Groq API key at → [console.groq.com](https://console.groq.com)

### 4. Run
```bash
python app.py
```

Open `http://localhost:7860` in your browser.

---

## ☁️ Deploy on Hugging Face Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space) (select **Gradio** SDK)
2. Upload `app.py` and `requirements.txt`
3. Go to **Settings → Variables and Secrets** → add `GROQ_API_KEY`
4. Your app goes live automatically ✅

---

## 📁 Project Structure

```
nexus-ai-assistant/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🤖 Available Models

| Model | Best For | Speed |
|---|---|---|
| LLaMA 3.3 70B | General quality, complex tasks | Fast |
| LLaMA 3.1 8B | Quick replies, simple tasks | Ultra Fast |
| Mixtral 8x7B | Deep reasoning, analysis | Fast |
| Gemma 2 9B | Creative writing, storytelling | Fast |
| LLaMA 4 Scout *(auto)* | Image analysis (vision) | Auto |

---

## 🎭 AI Personas

| Persona | Description |
|---|---|
| 🤖 Default Assistant | Helpful, smart, friendly — all-rounder |
| 🔬 Expert Researcher | Deep analysis with structured answers |
| 💻 Coding Expert | Production-ready code with explanations |
| ✍️ Creative Writer | Vivid, imaginative storytelling |
| 🎯 Career Coach | CV, LinkedIn, interview prep |

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq API key from [console.groq.com](https://console.groq.com) |

---

## 👨‍💻 Author

**Abdullah Javid**
BS Artificial Intelligence — University of Management and Technology (UMT), Lahore, Pakistan

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Abdullah_Javid-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/abdullah-javid-b217a2384/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-BUDDDY2894830-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/BUDDDY2894830)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and share.

---

<div align="center">
  <sub>Built with ⚡ by Abdullah Javid &nbsp;·&nbsp; UMT Lahore &nbsp;·&nbsp; Powered by Groq</sub>
</div>
