---
title: "On the Natural Robustness of Vision-Language Models Against Visual Perception Attacks in Autonomous Driving"
collection: publications
permalink: /publications/2025-v2lm-robustness/
date: 2025-06-13
authors:
  - Pedram MohajerAnsari
  - Amir Salarpour
  - Michael Kühr
  - Siyu Huang
  - Mohammad Hamad
  - Sebastian Steinhorst
  - Habeeb Olufowobi
  - Mert D Pesé
venue: "arXiv preprint arXiv:2506.11472"
category: manuscripts
pdf: https://arxiv.org/pdf/2506.11472.pdf
citation: "Pedram MohajerAnsari, Amir Salarpour, Michael Kühr, Siyu Huang, Mohammad Hamad, Sebastian Steinhorst, Habeeb Olufowobi, Mert D Pesé. <i>On the Natural Robustness of Vision-Language Models Against Visual Perception Attacks in Autonomous Driving</i>. arXiv preprint arXiv:2506.11472, 2025."
excerpt: "Demonstrates the inherent adversarial robustness of vision-language models for autonomous vehicle perception without adversarial training."

---

Autonomous vehicles (AVs) rely on deep neural networks (DNNs) for critical tasks such as traffic sign recognition (TSR), automated lane centering (ALC), and vehicle detection (VD). However, these models are vulnerable to attacks that can cause misclassifications and compromise safety. Traditional defense mechanisms, including adversarial training, often degrade benign accuracy and fail to generalize against unseen attacks.

In this work, we introduce **Vehicle Vision Language Models (V2LMs)**, fine-tuned vision-language models specialized for AV perception. Our findings demonstrate that V2LMs inherently exhibit superior robustness against unseen attacks without requiring adversarial training, maintaining significantly higher accuracy than conventional DNNs under adversarial conditions.

We evaluate two deployment strategies: **Solo Mode**, where individual V2LMs handle specific perception tasks, and **Tandem Mode**, where a single unified V2LM is fine-tuned for multiple tasks simultaneously.

Experimental results show that DNNs suffer performance drops of 33% to 46% under attacks, whereas V2LMs maintain adversarial accuracy with reductions of less than 8% on average. Tandem Mode further offers a memory-efficient alternative with comparable robustness.

We also explore using V2LMs as parallel components in AV perception stacks to enhance resilience. Our results suggest that V2LMs are a promising direction for secure and resilient AV systems.

👉 [Read the full paper (PDF)](/files/2025-v2lm-robustness.pdf)
