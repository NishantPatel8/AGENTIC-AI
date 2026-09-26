# SESSION 13 – Advanced Agentic Concepts (Part 2)

This repository contains the complete implementation, multi-modal scripts, automation workflows, API integrations, mathematical calculations, and agent evaluation reports for **Session 13: Advanced Agentic Concepts (Part 2)**.

---

## Overview of Tasks & Files Created

| Task | Topic | Files Created | Description |
| :--- | :--- | :--- | :--- |
| **Task 1** | Multi-Modal Agent | [`task1_multimodal_agent.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task1_multimodal_agent.py)<br>[`task1.ipynb`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task1.ipynb)<br>[`sample.jpg`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/sample.jpg) | Multi-modal agent script & notebook receiving a text prompt and image path, verifying inputs and confirming receipt. |
| **Task 2** | Zapier Gmail to Drive Automation | [`task2_zapier_gmail_gdrive_workflow.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task2_zapier_gmail_gdrive_workflow.md)<br>[`task2_gmail_to_gdrive_simulation.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task2_gmail_to_gdrive_simulation.py) | Complete Zapier integration guide + executable Python simulation saving assignment attachments to Google Drive. |
| **Task 3** | Spotify Web API Integration | [`task3_spotify_fetch_song.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task3_spotify_fetch_song.py) | Implements `fetch_song_info(song_name)` using the Spotify Web API search endpoint with test token support. |
| **Task 4** | Task Completion Rate Calculation | [`task4_task_completion_rate.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task4_task_completion_rate.md)<br>[`task4_calculate_tcr.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task4_calculate_tcr.py) | Mathematical derivation and calculation of Task Completion Rate (Strict: 75.0%, Weighted: 80.0%). |
| **Task 5** | Multi-Modal Agent Evaluation | [`task5_multimodal_agent_evaluation.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task5_multimodal_agent_evaluation.md) | Structured evaluation report auditing Accuracy (93.3%), Task Completion Rate (84.0%), and Reasoning Traces. |

---

## Detailed Task Documentation & Execution

### Task 1: Simple Multi-Modal Agent
- **Goal**: Accept text prompt and image file, and confirm receipt of both modalities.
- **To Run**:
  ```bash
  python task1_multimodal_agent.py
  ```
- **Notebook**:
  You can also open and run [`task1.ipynb`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task1.ipynb) directly in VS Code.

---

### Task 2: Zapier Automation (Gmail -> Google Drive)
- **Goal**: Automatically extract attachments from incoming Gmail emails with subject `"Assignment"` and upload to Google Drive.
- **Documentation**: See [`task2_zapier_gmail_gdrive_workflow.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task2_zapier_gmail_gdrive_workflow.md).
- **Python Simulation**:
  To verify the workflow logic locally without third-party credentials:
  ```bash
  python task2_gmail_to_gdrive_simulation.py
  ```

---

### Task 3: Spotify Song Info Fetcher
- **Goal**: Query Spotify Web API search endpoint and print artist and album name for a given song.
- **To Run**:
  ```bash
  # Run built-in demo:
  python task3_spotify_fetch_song.py

  # Or query any specific song:
  python task3_spotify_fetch_song.py "Blinding Lights"
  ```

---

### Task 4: Task Completion Rate (TCR)
- **Given Data**: 20 total tasks, 15 successfully completed, 2 partially completed, 3 failed.
- **Formulas & Math**:
  - **Strict TCR**: $\frac{15}{20} \times 100 = \mathbf{75.0\%}$
  - **Weighted TCR**: $\frac{15 + (2 \times 0.5)}{20} \times 100 = \frac{16}{20} \times 100 = \mathbf{80.0\%}$
- **To Run**:
  ```bash
  python task4_calculate_tcr.py
  ```

---

### Task 5: Multi-Modal Agent Evaluation
- **Report Document**: [`task5_multimodal_agent_evaluation.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2013/task5_multimodal_agent_evaluation.md)
- **Metrics Covered**:
  1. **Accuracy**: 93.3% perceptual grounding across OCR, object detection, and visual alignment.
  2. **Task Completion Rate**: 84.0% strict / 88.0% weighted across 25 diverse test scenarios.
  3. **Reasoning Trace Analysis**: Audited step-by-step Chain-of-Thought (CoT) trajectory from file validation to cross-modal synthesis.
