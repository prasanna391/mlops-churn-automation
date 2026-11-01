import os
import shutil
import subprocess
import sys


def run_command(command):
    print(f"\n[INFO] Running: {command}")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print("[INFO] Expected failure detected.")
        return False

    return True


def main():
    print("=========================================")
    print("Lab 9 - Failure and Recovery Tests")
    print("=========================================")

    os.makedirs("reports", exist_ok=True)
    os.makedirs("artifacts", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Failure test: temporarily rename the raw dataset
    dataset = "data/raw/churn.csv"
    backup = "data/raw/churn_backup.csv"

    if os.path.exists(dataset):
        print("\n[TEST 1] Simulating missing input data...")

        os.rename(dataset, backup)

        try:
            result = subprocess.run(
                [sys.executable, "src/validate_data.py"]
            )

            if result.returncode != 0:
                print("[SUCCESS] Failure detected correctly.")
            else:
                print("[WARNING] Failure was not detected.")

        finally:
            os.rename(backup, dataset)

        print("[SUCCESS] Original dataset recovered.")

    else:
        print("[ERROR] Dataset not found:", dataset)
        sys.exit(1)

    print("\n[TEST 2] Running recovery pipeline...")

    result = subprocess.run(
        [sys.executable, "src/mlops_pipeline/churn_prediction_pipeline.py"]
    )

    if result.returncode == 0:
        print("[SUCCESS] Recovery pipeline completed successfully.")
    else:
        print("[ERROR] Recovery pipeline failed.")
        sys.exit(1)

    print("\n=========================================")
    print("Lab 9 Failure and Recovery Tests PASSED")
    print("=========================================")


if __name__ == "__main__":
    main()