from statistics import mean

from rag_eval import target
from rag_eval.dataset import Sample
from rag_eval.metrics.retrieval import context_precision, context_recall


def run(samples: list[Sample], base_url: str) -> None:
    precisions, recalls = [], []
    for sample in samples:
        trace = target.query(base_url, sample.question)
        precisions.append(context_precision(trace, sample))
        recalls.append(context_recall(trace, sample))
        print(f"{sample.id}\tprecision={precisions[-1]:.2f}\trecall={recalls[-1]:.2f}")
    print(f"mean\tprecision={mean(precisions):.2f}\trecall={mean(recalls):.2f}")
