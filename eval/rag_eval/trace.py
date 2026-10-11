from dataclasses import dataclass


@dataclass
class Trace:
    answer: str
    chunk_ids: list[str]
    latency: float
