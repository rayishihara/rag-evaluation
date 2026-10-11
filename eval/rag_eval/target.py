import time

import httpx

from rag_eval.trace import Trace


def query(base_url: str, question: str) -> Trace:
    start = time.perf_counter()
    response = httpx.post(f"{base_url}/chat", json={"prompt": question}, timeout=60.0)
    latency = time.perf_counter() - start
    response.raise_for_status()
    body = response.json()
    return Trace(
        answer=body["answer"],
        chunk_ids=[f"{c['file_name']}#{c['chunk_index']}" for c in body["chunks"]],
        latency=latency,
    )
