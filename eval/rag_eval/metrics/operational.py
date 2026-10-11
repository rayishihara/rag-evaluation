from rag_eval.trace import Trace


def latency(trace: Trace) -> float:
    return trace.latency
