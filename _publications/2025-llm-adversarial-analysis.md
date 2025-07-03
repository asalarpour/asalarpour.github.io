---
title: "WIP: From Detection to Explanation: Using LLMs for Adversarial Scenario Analysis in Vehicles"
collection: publications
permalink: /publications/2025-llm-adversarial-analysis/
date: 2025-08-10
authors:
  - David Fernandez
  - Pedram MohajerAnsari
  - Cigdem Kokenoz
  - Amir Salarpour
  - Bing Li
  - Mert D Pesé
venue: "The 3rd USENIX Symposium on Vehicle Security and Privacy (VehicleSec '25)"
category: conference
pdf: /publications/pdfs/2025-llm-adversarial-analysis.pdf
citation: "David Fernandez, Pedram MohajerAnsari, Cigdem Kokenoz, Amir Salarpour, Bing Li, Mert D Pesé. <i>WIP: From Detection to Explanation: Using LLMs for Adversarial Scenario Analysis in Vehicles</i>. In Proceedings of the 3rd USENIX Symposium on Vehicle Security and Privacy (VehicleSec '25), August 2025."
excerpt: "A zero-shot LLM-based reasoning framework for adversarial scenario analysis in autonomous vehicles, using formal traffic rules and chain-of-thought prompting."

---

We propose a framework that leverages Large Language Models (LLMs) for adversarial scenario analysis in autonomous vehicles (AVs), generating interpretable explanations for anomalies and bridging the gap between detection and semantic understanding.

To address the limitations of traditional deep neural networks (DNNs) in robustness and interpretability, we introduce a zero-shot chain-of-thought (CoT) reasoning system that uses a domain-specific language (DSL) and incorporates formal traffic knowledge from the MUTCD.

We introduce AutoSec-X, a dataset of 40 driving scenarios (benign and adversarial); evaluate zero-shot CoT prompting with LLMs (e.g., Gemini, LLaMA, Qwen); and benchmark performance using BLEU, ROUGE, and SBERT. Our results show that Gemini 1.5-Pro delivers stronger semantic reasoning and rule-based interpretation of adversarial conditions.

👉 [Read the full paper (PDF)](/files/2025-llm-adversarial-analysis.pdf)
