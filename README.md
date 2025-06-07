# RuPunctuation

> **Automatic Russian Punctuation Restoration**

---

## Overview
RuPunctNet is a project dedicated to automatic punctuation correction in Russian texts. The main goal is to create a service (e.g., a Telegram bot) that processes user sentences and returns the same text with correct punctuation marks (`.`, `,`, `?`, `!`) according to Russian language rules.

The correction is performed by a machine learning model, selected based on research conducted within this project. The punctuation restoration task is typically approached as a Named Entity Recognition (NER) classification problem.

---

## Features
- **Data Collection & EDA:** Extensive exploratory data analysis and cleaning of Russian texts from Wikipedia and books.
- **Baselines & Deep Learning:** Rule-based, classical ML, and deep learning (Transformers) models for punctuation restoration.
---

## Project Structure
- `data/` — Data collection, cleaning scripts, and annotated datasets.
- `EDA/` — Notebooks and scripts for exploratory data analysis and markup creation.
- `experiments/` — Deep learning experiments (BERT, XLM-Roberta, CRF, etc.).
- `requirements.txt` — Main Python dependencies.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KozlovKY/RuPunctuation.git
   cd RuPunctNet
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

