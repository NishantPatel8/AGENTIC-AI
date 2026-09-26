"""
Session 13 - Task 4: Task Completion Rate (TCR) Calculator
==========================================================
Given:
- Total Assigned Tasks: 20
- Successfully Completed: 15
- Partially Completed: 2
- Failed / Incomplete: 3

This script calculates and prints both Strict (Binary) and Weighted
Task Completion Rates with detailed step-by-step math.
"""

import sys

# Ensure safe UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def calculate_tcr(total_tasks: int, completed: int, partial: int):
    failed = total_tasks - completed - partial

    # 1. Strict (Binary) Calculation
    strict_rate = (completed / total_tasks) * 100

    # 2. Weighted (Partial Credit = 0.5) Calculation
    effective_score = completed + (partial * 0.5)
    weighted_rate = (effective_score / total_tasks) * 100

    print("=" * 70)
    print("      SESSION 13 - TASK 4: TASK COMPLETION RATE CALCULATION")
    print("=" * 70)

    print("\n[+] LOG DATA SUMMARY:")
    print(f"  • Total Assigned Tasks (N):        {total_tasks}")
    print(f"  • Successfully Completed (C_full): {completed}")
    print(f"  • Partially Completed (C_part):    {partial}")
    print(f"  • Failed / Incomplete (F):         {failed}")

    print("\n" + "-" * 70)
    print("[+] METHOD 1: STRICT (BINARY) TASK COMPLETION RATE")
    print("-" * 70)
    print("  Formula:     (Completed / Total) * 100")
    print(f"  Calculation: ({completed} / {total_tasks}) * 100 = {completed/total_tasks:.4f} * 100")
    print(f"  >>> Final Strict TCR: {strict_rate:.1f}%")

    print("\n" + "-" * 70)
    print("[+] METHOD 2: WEIGHTED TASK COMPLETION RATE (50% PARTIAL CREDIT)")
    print("-" * 70)
    print("  Formula:     ((Completed + (Partial * 0.5)) / Total) * 100")
    print(f"  Score:       {completed} + ({partial} * 0.5) = {effective_score}")
    print(f"  Calculation: ({effective_score} / {total_tasks}) * 100 = {effective_score/total_tasks:.4f} * 100")
    print(f"  >>> Final Weighted TCR: {weighted_rate:.1f}%")

    print("\n" + "=" * 70)
    print("[CONCLUSION]")
    print(f"The agent's Task Completion Rate is 75.0% (strict) or 80.0% (weighted).")
    print("=" * 70)

if __name__ == "__main__":
    calculate_tcr(total_tasks=20, completed=15, partial=2)
