# 🚀 AI Financial Analyst - Easy Edition

A powerful financial analysis system powered by AI agents, optimized for **small PCs** with limited resources.

## ✨ Features

- 📊 **Multi-Agent Analysis**: Query analyzer, data fetcher, and code generator working together
- 💻 **Easy-to-Use UI**: Beautiful Streamlit interface - just click and run!
- 🎯 **Smart Stock Analysis**: Analyze any stock with natural language queries
- 🔧 **Flexible AI Backend**: Use Ollama, OpenAI, or train your own small model
- 📈 **Automated Visualizations**: Generate charts and insights automatically

---

## 🎯 Quick Start (3 Steps!)

### 1. Install Dependencies

First, install [uv](https://github.com/astral-sh/uv) (fast Python package manager):

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install project dependencies:

```bash
uv sync
```

### 2. Choose Your AI Backend

**Option A: Use Ollama (Recommended for local use)**

```bash
# Install Ollama from: https://ollama.com/download
# Then pull a model:
ollama pull deepseek-r1:7b
```

**Option B: Use OpenAI**

Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=openai/gpt-4o
```

**Option C: Train Your Own Model** (see Training section below)

### 3. Run the App

**Windows**: Just double-click `run.bat`

**Or manually**:
```bash
uv run streamlit run app.py
```

That's it! 🎉 The app will open in your browser.

---

## 🎓 Training Your Own Model (For Small PCs)

Want to fine-tune a small AI model for financial analysis? This script is optimized for PCs with limited GPU memory (even 4GB works!).

### Prerequisites

- **GPU**: NVIDIA GPU with 4GB+ VRAM (or use Google Colab for free GPU)
- **CUDA**: Install from [NVIDIA](https://developer.nvidia.com/cuda-downloads)

### Training Steps

1. **Prepare your data** (create `financial_data.json`):

```json
[
  {
    "text": "<|im_start|>system\nYou are a financial analyst.<|im_end|>\n<|im_start|>user\nAnalyze TSLA<|im_end|>\n<|im_start|>assistant\nI'll analyze TSLA stock data...<|im_end|>"
  }
]
```

2. **Run training**:

```bash
uv run python train.py
```

The script uses:
- 🔹 **Small models**: Llama-3.2-1B or Qwen2.5-1.5B (only ~1.5GB!)
- 🔹 **4-bit quantization**: Reduces memory by 75%
- 🔹 **LoRA**: Trains only 1% of parameters
- 🔹 **Optimized with Unsloth**: 2x faster training

3. **Use your trained model**:

Create `.env`:
```
MODEL_NAME=local
LOCAL_MODEL_PATH=./trained_model
```

---

## 📖 Usage Examples

### Using the Streamlit UI

1. Run `run.bat` (Windows) or `uv run streamlit run app.py`
2. Enter your query: *"Analyze TSLA stock for the last 3 months"*
3. Click **Analyze**
4. View the generated code and results!

### Using as MCP Server (Advanced)

Add to Cursor Settings > MCP:

```json
{
  "mcpServers": {
    "financial-analyst": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\PC\\Documents\\ai-engineering-hub\\financial-analyst-deepseek",
        "run",
        "mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

Then use the `analyze_stock` tool in Cursor!

---

## 🎨 Example Queries

- *"What's the current trend for TSLA?"*
- *"Compare AAPL and MSFT performance over the last year"*
- *"Show me NVDA's price and volume for the last month"*
- *"Analyze the correlation between TSLA and NVDA"*

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file to customize:

```bash
# AI Model Configuration
MODEL_NAME=ollama/deepseek-r1:7b  # or openai/gpt-4o, or local
LLM_BASE_URL=http://localhost:11434  # for Ollama

# OpenAI (if using)
OPENAI_API_KEY=your_key_here

# Local Model (if trained)
LOCAL_MODEL_PATH=./trained_model
```

---

## 💡 Tips for Small PCs

1. **Use Ollama with smaller models**: `ollama pull deepseek-r1:7b` (not the 14B version)
2. **Train on Google Colab**: Free GPU access for training
3. **Close other apps**: When running training or analysis
4. **Use 4-bit models**: The training script does this automatically

---

## 📁 Project Structure

```
financial-analyst-deepseek/
├── app.py                 # Streamlit UI (easy mode!)
├── run.bat               # One-click launcher
├── finance_crew.py       # Multi-agent system
├── train.py              # Model training script
├── server.py             # MCP server
├── pyproject.toml        # Dependencies
└── README.md             # You are here!
```

---

## 🐛 Troubleshooting

**"uv not found"**: Install uv first (see Quick Start)

**"Ollama connection failed"**: Make sure Ollama is running (`ollama serve`)

**"Out of memory" during training**: 
- Use smaller batch size in `train.py`
- Try Google Colab instead
- Close other applications

**"Model not found"**: Pull the model first (`ollama pull deepseek-r1:7b`)

---

## 📬 Credits

Built with CrewAI, Streamlit, and Unsloth for efficient AI training.
