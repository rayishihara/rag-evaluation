from ragas.metrics.collections import AnswerCorrectness, AnswerRelevancy, Faithfulness

from rag_eval import judge
from rag_eval.dataset import Sample
from rag_eval.trace import Trace

_faithfulness = Faithfulness(judge.llm)
_answer_relevancy = AnswerRelevancy(judge.llm, judge.embeddings)
_answer_correctness = AnswerCorrectness(judge.llm, judge.embeddings)


def faithfulness(trace: Trace, sample: Sample) -> float:
    return _faithfulness.score(user_input=sample.question, response=trace.answer, retrieved_contexts=trace.chunks).value


def answer_relevance(trace: Trace, sample: Sample) -> float:
    return _answer_relevancy.score(user_input=sample.question, response=trace.answer).value


def answer_correctness(trace: Trace, sample: Sample) -> float:
    return _answer_correctness.score(user_input=sample.question, response=trace.answer, reference=sample.reference_answer).value
