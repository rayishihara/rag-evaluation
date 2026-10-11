from pathlib import Path
from statistics import mean

from rag_eval import target, tracking
from rag_eval.dataset import Sample
from rag_eval.metrics.retrieval import context_precision, context_recall


def run(samples: list[Sample], base_url: str, dataset: Path, run_name: str | None) -> None:
    params = {"base_url": base_url, "dataset": dataset.name, "n_samples": len(samples)}
    with tracking.start_run("reliability", run_name, params):
        rows = []
        for sample in samples:
            trace = target.query(base_url, sample.question)
            rows.append({
                "id": sample.id,
                "question": sample.question,
                "retrieved": ", ".join(trace.chunk_ids),
                "relevant": ", ".join(sample.relevant_chunks),
                "precision": context_precision(trace, sample),
                "recall": context_recall(trace, sample),
            })
            print(f"{sample.id}\tprecision={rows[-1]['precision']:.2f}\trecall={rows[-1]['recall']:.2f}")
        metrics = {
            "context_precision": mean(r["precision"] for r in rows),
            "context_recall": mean(r["recall"] for r in rows),
        }
        print(f"mean\tprecision={metrics['context_precision']:.2f}\trecall={metrics['context_recall']:.2f}")
        tracking.log_results(metrics, rows)
