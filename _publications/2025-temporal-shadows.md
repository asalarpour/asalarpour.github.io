---
title: "Attention-Aware Temporal Adversarial Shadows on Traffic Sign Sequences"
collection: publications
permalink: /publications/2025-temporal-shadows/
date: 2025-06-10
authors:
  - Pedram MohajerAnsari
  - Amir Salarpour
  - David Fernandez
  - Cigdem Kokenoz
  - Bing Li
  - Mert D Pesé
venue: "CVPR 2025 – IEEE/CVF Conference on Computer Vision and Pattern Recognition"
pages: 3591–3599
category: conference
pdf: https://openaccess.thecvf.com/content/CVPR2025/papers/MohajerAnsari_Attention-Aware_Temporal_Adversarial_Shadows_on_Traffic_Sign_Sequences_CVPR_2025_paper.pdf
# citation: "MohajerAnsari, P., Salarpour, A., Fernandez, D., Kokenoz, C., Li, B., Pesé, M. D. <i>Attention-Aware Temporal Adversarial Shadows on Traffic Sign Sequences</i>. In CVPR 2025 – IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 3591–3599."
excerpt: "Proposes temporally coherent shadow-based adversarial attacks on traffic sign recognition systems, leveraging attention maps and evolutionary optimization."

---

We present a framework for black-box adversarial attacks on traffic signs using **temporally coherent shadows**. Unlike previous methods that target isolated frames, our approach attacks entire traffic sign **sequences**, mimicking real-world autonomous vehicle (AV) observation behavior.

Our method uses a **non-differentiable shadow generator** with fixed geometry and opacity, whose spatial scale evolves over time. A **genetic algorithm** is employed to optimize shadow parameters under a dual-loss objective that maximizes both classification error and attention disruption, using DINO ViT attention maps.

Evaluated on GTSRB, our method achieves a **sequence-level attack success rate (SL-ASR)** of up to **87.5%**, and **attention supervision** improves attack effectiveness by **11–18%** compared to baseline strategies.

👉 [Read the full paper (PDF)](/files/2025-temporal-shadows.pdf)
