import os

import httpx
from openai import AsyncOpenAI
from ragas.embeddings.base import embedding_factory
from ragas.llms import llm_factory

# Point the OpenAI client at Gemini's compatible endpoint; no retries, like the rest of the eval
client = AsyncOpenAI(
    api_key=os.environ["JUDGE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
    max_retries=0,
    # Skip keep-alive so no pooled connection outlives the event loop each .score() call creates
    http_client=httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=0)),
)
llm = llm_factory(os.environ["JUDGE_MODEL"], client=client)
embeddings = embedding_factory("openai", model=os.environ["EMBEDDING_MODEL"], client=client)
