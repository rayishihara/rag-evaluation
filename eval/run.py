import argparse
from pathlib import Path

from rag_eval.dataset import load
from rag_eval.experiments import reliability

EXPERIMENTS = {"reliability": reliability.run}

parser = argparse.ArgumentParser(description="Run an evaluation experiment against the RAG system.")
parser.add_argument("--experiment", choices=EXPERIMENTS, default="reliability")
parser.add_argument("--base-url", required=True)
parser.add_argument("--dataset", type=Path, default=Path(__file__).parent / "datasets" / "golden.jsonl")
args = parser.parse_args()

EXPERIMENTS[args.experiment](load(args.dataset), args.base_url.rstrip("/"))
