# RAG evaluation

A lightweight evaluation pipeline for a simple, mock RAG application.

## RAG pipeline

A high-level picture of the system's architecture.

<img src="./assets/rag-system-architecture.png" alt="RAG system architecture diagram" width="600">

## Evaluation pipeline

What does a good RAG pipeline look like? So far, I think there's five criteria to evaluate on: 

- Time - we want the end-to-end latency, from query to response, to be as little as possible
- Cost - we want the cost per query to be as cheap as possible
- Scalability - we want performance to hold up as document and query volumes grow
- Consistency - we want similar queries to always produce similar answers
- Reliability - can we trust the response? (this one is deliberately left vague)

Let's break down how each of them can be quantified.

### Time & Cost

Time and cost are easily measured once a traceability/observability system is in place.

### Scalability

See how time, cost, and quality varies as we increase document or query volume. There's also architectural considerations but that is out of scope for RAG evaluation.

### Consistency

Can be further broken down into

- retrieval consistency
- answer consistency
- score variance

### Reliability

For retrieval metrics:

- context precision
- context recall
- mean reciprocal rank

For generation metrics:

- faithfulness
- answer relevance
- answer correctness