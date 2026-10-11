import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Sample:
    id: str
    question: str
    reference_answer: str
    relevant_chunks: list[str]


def load(path: Path) -> list[Sample]:
    with open(path) as f:
        return [Sample(**json.loads(line)) for line in f if line.strip()]
