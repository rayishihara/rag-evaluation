import subprocess
from pathlib import Path

import mlflow

# Anchor the store to eval/ so runs land in one place regardless of the working directory
EVAL_DIR = Path(__file__).resolve().parents[1]


def start_run(experiment: str, run_name: str | None, params: dict) -> mlflow.ActiveRun:
    mlflow.set_tracking_uri(f"sqlite:///{EVAL_DIR / 'mlflow.db'}")
    mlflow.set_experiment(experiment)
    run = mlflow.start_run(run_name=run_name)
    git_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=EVAL_DIR).stdout.strip()
    mlflow.log_params({**params, "git_sha": git_sha})
    return run


def log_results(metrics: dict[str, float], rows: list[dict]) -> None:
    mlflow.log_metrics(metrics)
    mlflow.log_table({key: [row[key] for row in rows] for key in rows[0]}, "per_query.json")
