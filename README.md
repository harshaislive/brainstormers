# 🧠 Brainstormers

An AI-powered brainstorming tool featuring three distinct scientific personalities that engage in dynamic debates about any hypothesis. Built with CrewAI and Azure OpenAI.

## 🎭 Meet The Team

- **Alpha 🔬 (The Humorous Skeptic)**: A witty scientist who tries to disprove hypotheses using humor and rigorous analysis
- **Beta ⚡ (The Serious Advocate)**: An intensely serious researcher who builds strong cases supporting hypotheses  
- **Gamma 🧠 (The Zen Synthesizer)**: A wise scientific mind who provides balanced analysis with zen-like insight

All three agents possess Einstein-level intellect across all scientific disciplines and use first-principles thinking.

## 🚀 Features

- **Interactive Debates**: Watch three AI scientists argue, agree, and build on each other's ideas
- **@ Mentions**: Agents can call each other out directly (@Alpha, @Beta, @Gamma, @You)
- **Scientific Rigor**: All responses grounded in real scientific principles and evidence
- **Two Interfaces**: Terminal CLI or simple GUI
- **Real-time Flow**: You → Alpha → Beta → Gamma → repeat

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/harshaislive/brainstormers.git
cd brainstormers
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI
Create a `.env` file (copy from `.env.example`):
```env
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_API_BASE=https://your-resource.cognitiveservices.azure.com/
AZURE_API_VERSION=2024-08-01-preview
AZURE_MODEL_NAME=your-deployment-name
```

## 🎮 Usage

### Terminal Interface (Recommended)
```bash
python brainstorm_crew.py
```

### GUI Interface (Local only)
```bash
python brainstorm_gui.py
```

### Web Deployment
```bash
python app.py
```
*Note: Web deployments use the terminal interface. GUI is only available locally.*

## 💬 Example Session

```
💭 Hypothesis: "Time travel is possible"

💬 You: What do you all think?

💬 Alpha 🔬: Well, that's about as likely as a penguin becoming a ballet dancer! 🐧 
From a thermodynamics perspective, we'd need to violate causality...

💬 Beta ⚡: @Alpha, while you jest, recent developments in closed timelike curves 
and Gödel's solutions to Einstein's field equations suggest...

💬 Gamma 🧠: Like two rivers flowing in opposite directions, perhaps time itself 
is more fluid than our linear minds perceive...
```

## 🔧 Configuration Options

Environment variables you can customize:

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key (required)
- `AZURE_API_BASE`: Your Azure OpenAI endpoint
- `AZURE_API_VERSION`: API version to use
- `AZURE_MODEL_NAME`: Your deployment name
- `TEMPERATURE`: Response creativity (0.0-2.0, default: 1.0)
- `MAX_TOKENS`: Maximum response length (default: 16384)
- `TOP_P`: Nucleus sampling parameter (default: 1.0)

## 🌐 Web Deployment Ready

This project is configured for easy deployment to platforms like:
- Heroku
- Railway
- Render
- DigitalOcean App Platform

All sensitive configuration is handled via environment variables.

## 📁 Project Structure

```
brainstormers/
├── brainstorm_crew.py    # Terminal interface
├── brainstorm_gui.py     # GUI interface  
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Use Cases

- **Research**: Explore complex scientific hypotheses from multiple angles
- **Education**: Learn through Socratic dialogue with AI experts
- **Brainstorming**: Generate ideas through structured debate
- **Decision Making**: See pros/cons through different scientific lenses
- **Entertainment**: Watch AI personalities clash over interesting topics

## 🔮 Future Features

- [ ] Voice interface
- [ ] Memory across sessions
- [ ] Export conversations
- [ ] Custom agent personalities
- [ ] Multi-language support
- [ ] Web interface
- [ ] Integration with research databases

---

Built with ❤️ using [CrewAI](https://github.com/joaomdmoura/crewai) and Azure OpenAI