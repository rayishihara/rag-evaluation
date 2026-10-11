from rag_eval.dataset import Sample
from rag_eval.trace import Trace


def context_precision(trace: Trace, sample: Sample) -> float:
    if not trace.chunk_ids:
        return 0.0
    hits = set(trace.chunk_ids) & set(sample.relevant_chunks)
    return len(hits) / len(trace.chunk_ids)


def context_recall(trace: Trace, sample: Sample) -> float:
    hits = set(trace.chunk_ids) & set(sample.relevant_chunks)
    return len(hits) / len(sample.relevant_chunks)
