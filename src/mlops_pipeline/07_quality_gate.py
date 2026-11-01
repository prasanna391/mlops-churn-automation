import json
import os
import sys

def run_quality_gate():
    print("[INFO] Starting Model Quality Gate...")

    # Static settings mapping to your custom layout values directly
    base_dir = r"C:\Users\vamsi\Videos\churn-prediction(1)\churn-prediction"
    report_path = os.path.join(base_dir, "reports", "evaluation_report.json")
    quality_gate_report_path = os.path.join(base_dir, "reports", "quality_gate_report.json")
    
    metric_name = "f1_score"
    minimum_value = 0.50

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except FileNotFoundError:
        # Check alternative common fallback path
        fallback_path = os.path.join(base_dir, "artifacts", "evaluation_report.json")
        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                report = json.load(f)
                report_path = fallback_path
        except FileNotFoundError:
            print(f"[ERROR] Evaluation report not found at target locations.")
            return False

    # Extract performance metrics
    metrics_data = report.get("metrics", report)
    actual_value = float(metrics_data.get(metric_name, 0.0))
    
    # If not found directly, check standard variants
    if actual_value == 0.0 and "f1" in metrics_data:
        actual_value = float(metrics_data.get("f1", 0.0))

    passed = actual_value >= minimum_value

    print(
        f"[INFO] Quality Gate: {metric_name}={actual_value:.4f} | "
        f"required>={minimum_value:.4f}"
    )

    os.makedirs(os.path.dirname(quality_gate_report_path), exist_ok=True)

    gate_report = {
        "stage": "Lab 7 - Model Quality Gate",
        "metric": metric_name,
        "minimum_value": minimum_value,
        "actual_value": actual_value,
        "status": "PASSED" if passed else "FAILED",
    }

    with open(quality_gate_report_path, "w", encoding="utf-8") as f:
        json.dump(gate_report, f, indent=4)

    if passed:
        print("[SUCCESS] Model Quality Gate PASSED.")
    else:
        print("[ERROR] Model Quality Gate FAILED. Pipeline will stop before promotion.")

    return passed

if __name__ == "__main__":
    passed = run_quality_gate()
    sys.exit(0 if passed else 1)
