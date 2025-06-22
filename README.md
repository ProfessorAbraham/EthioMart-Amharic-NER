# EthioMart - Amharic NER & FinTech Scorecard System

This project focuses on building an Amharic Named Entity Recognition (NER) system that extracts key business entities such as product names, prices, and locations from Ethiopian Telegram e-commerce channels.

The extracted information is used to build a centralized database and a **FinTech Vendor Scorecard Engine** that helps identify promising vendors for micro-lending opportunities.

## 📁 Folder Structure
── data/ # Raw and labeled datasets
├── models/ # Trained NER models
├── results/ # Evaluation and vendor scorecards
├── src/ # Python scripts
├── notebooks/ # Jupyter Notebooks for analysis
├── reports/ # Final PDF report
└── README.md # This file

## 🛠️ Tasks Covered

- Data Collection from Telegram
- Amharic Text Preprocessing
- CoNLL Format Labeling
- Fine-Tuning Transformer Models (XLM-Roberta, mBERT, bert-tiny-amharic)
- Model Comparison (F1-score, Precision, Recall)
- Model Interpretability (SHAP/LIME)
- Vendor Scorecard for Micro-Lending

---

Developed during the **Artificial Intelligence Mastery Bootcamp** (June 2025).