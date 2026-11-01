import subprocess
import sys


def run_script(script):
    print(f"\n[INFO] Running {script}...")
    
    result = subprocess.run([sys.executable, script])
    
    if result.returncode != 0:
        print(f"[ERROR] {script} failed.")
        sys.exit(1)
    
    print(f"[SUCCESS] {script} completed successfully.")


def main():
    print("=========================================")
    print("Starting Churn Prediction MLOps Pipeline")
    print("=========================================")

    scripts = [
        "pipelines/run_lab5_pipeline.py",
        "src/evaluate.py",
        "pipelines/07_quality_gate.py"
    ]

    for script in scripts:
        run_script(script)

    print("\n=========================================")
    print("MLOps Pipeline completed successfully!")
    print("=========================================")


if __name__ == "__main__":
    main()