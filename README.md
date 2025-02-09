# README

This repository contains a **fully automated** pipeline for data analysis and prediction using a large language model (LLM). We assume you’ll be using **Ollama** (an LLM runtime) and the **deepseek-32b** model. Below are the steps to set everything up—covering **hardware requirements**, **model installation**, **Python environment configuration**, and **running** the application.

---

## 1. Hardware Requirements

Because **deepseek-32b** is a large model, you should ideally have:

- **64 GB** of system RAM (minimum recommended: 32 GB).
- A modern CPU with multiple cores (the more, the better).
- **(Optional for GPU acceleration)** A GPU with at least 24–32 GB of VRAM if you plan to run GPU-accelerated inference. Otherwise, the CPU fallback may be extremely slow.

> **Note**: Exact requirements depend on your specific environment and how Ollama loads the model. For smaller models, you can get away with less RAM/VRAM.

---

## 2. Installing Ollama

Ollama is a self-contained LLM runner. Follow these steps:

1. **Clone or download** the Ollama repository:
   ```bash
   git clone https://github.com/jmorganca/ollama.git
2. **Install Ollama** by following the instructions in the official repository’s README or docs:
   
   [Ollama Installation Docs](https://github.com/ollama/ollama#installation)
   Depending on your OS (e.g., macOS or Linux), you may need additional prerequisites. Check the repository for the latest setup details.

3. **Pulling the deepseek-32b Model**:
   Once Ollama is installed, pull the deepseek-32b model locally:
   ```bash
   ollama pull deepseek-r1:32b
      This will download the model weights so Ollama can use them. The download size can be several tens of gigabytes.

