# README

This repository contains a **fully automated** pipeline for data analysis and prediction using a large language model (LLM). The pipeline leverages **Ollama** (an LLM runtime) and the **deepseek-32b** model. Below are the steps to set up and run the application.

---

## Table of Contents
1. [Hardware Requirements](#1-hardware-requirements)
2. [Installing Ollama](#2-installing-ollama)
3. [Pulling the Model](#3-pulling-the-model)
4. [Python Environment Setup](#4-python-environment-setup)
5. [Running the Pipeline](#6-running-the-pipeline)

---

## 1. Hardware Requirements

For optimal performance with **deepseek-r1:32b**:
- **64 GB** of system RAM (minimum: 32 GB).
- A modern multi-core CPU (the more cores, the better).
- **(Optional for GPU acceleration)** A GPU with 24–32 GB VRAM. CPU-only inference may be slow.

---

## 2. Installing Ollama

Follow the official installation guide for your OS:
1. Visit [Ollama Installation Docs](https://github.com/jmorganca/ollama).
2. Download and install the appropriate binary for your system.

---

## 3. Pulling the Model

After installing Ollama, download the model:
```bash
ollama pull deepseek-r1:32b
```

## 4. Python environment setup

1. Install [Python 3.12](https://www.python.org/downloads/).
2. Create a virtual environment (e.g., .venv) in the project directory:
```bash
python3 -m venv .venv
```
3. Activate the virtual environment:
  - On Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```
  - On Windows:
   ```
    .venv\Scripts\activate
   ```
4. Install requirements:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 5. Running the Pipeline

Run the main.py script:
```bash
python main.py
```
