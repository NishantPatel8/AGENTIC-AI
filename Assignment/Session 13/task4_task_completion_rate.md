# Session 13 – Task 4: Task Completion Rate (TCR) Calculation

## 1. Problem Statement
> **Agent Log Data**:
> - Total Assigned Tasks ($N$): **20**
> - Successfully Completed Tasks ($C_{\text{full}}$): **15**
> - Partially Completed Tasks ($C_{\text{partial}}$): **2**
> - Failed / Incomplete Tasks ($F$): **3** ($20 - 15 - 2 = 3$)

---

## 2. Calculation Methodologies

In AI Agentic Systems and benchmark frameworks (such as AgentBench, GAIA, and SWE-bench), there are two recognized ways to compute the **Task Completion Rate (TCR)**:

### Method A: Strict (Binary) Task Completion Rate
Under the standard binary pass/fail criterion, a task is only credited if it was completely and accurately fulfilled from end to end:

$$\text{TCR}_{\text{strict}} = \left( \frac{\text{Successfully Completed Tasks}}{\text{Total Assigned Tasks}} \right) \times 100$$

$$\text{TCR}_{\text{strict}} = \left( \frac{15}{20} \right) \times 100 = 0.75 \times 100 = \mathbf{75.0\%}$$

---

### Method B: Weighted Task Completion Rate (Partial Credit)
In complex multi-step agent environments, partial completions (where intermediate tools and sub-goals succeeded) receive partial credit ($0.5$ or $50\%$ credit):

$$\text{Effective Score} = C_{\text{full}} + (C_{\text{partial}} \times 0.5)$$
$$\text{Effective Score} = 15 + (2 \times 0.5) = 15 + 1 = 16.0$$

$$\text{TCR}_{\text{weighted}} = \left( \frac{\text{Effective Score}}{\text{Total Assigned Tasks}} \right) \times 100$$

$$\text{TCR}_{\text{weighted}} = \left( \frac{16.0}{20} \right) \times 100 = 0.80 \times 100 = \mathbf{80.0\%}$$

---

## 3. Summary of Results

| Metric | Calculation | Final Percentage |
| :--- | :--- | :--- |
| **Strict Task Completion Rate** | $\frac{15}{20} \times 100$ | **75.0%** |
| **Weighted Task Completion Rate** | $\frac{15 + (2 \times 0.5)}{20} \times 100$ | **80.0%** |

### Interpretation:
- If your system requires **all-or-nothing completion**, the agent achieved **75%**.
- If your evaluation grants **pro-rated credit for partial progress**, the agent achieved **80%**.
