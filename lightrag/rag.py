"""
LightRAG instance factory for tolstoy.life

Creates and configures the LightRAG instance with Ollama backends.
"""

from functools import partial

from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc

from config import (
    LIGHTRAG_DIR,
    OLLAMA_HOST,
    OLLAMA_TIMEOUT,
    LLM_MODEL,
    LLM_CONTEXT_WINDOW,
    EMBED_MODEL,
    EMBED_DIM,
    EMBED_MAX_TOKENS,
)


def create_rag() -> LightRAG:
    """Create a configured LightRAG instance.

    Uses Ollama for both LLM and embedding, with all-local storage backends
    (JSON KV, NetworkX graph, NanoVectorDB vectors).

    Note: ollama_embed is decorated with @wrap_embedding_func_with_attrs which
    hardcodes embedding_dim=1024 (for bge-m3). To use nomic-embed-text (768d),
    we must access the unwrapped function via ollama_embed.func — otherwise the
    inner decorator's dimension check fires before ours and rejects 768d output.
    See EmbeddingFunc docstring in lightrag/utils.py for this pattern.
    """
    LIGHTRAG_DIR.mkdir(parents=True, exist_ok=True)

    rag = LightRAG(
        working_dir=str(LIGHTRAG_DIR),
        llm_model_func=ollama_model_complete,
        llm_model_name=LLM_MODEL,
        llm_model_kwargs={
            "host": OLLAMA_HOST,
            "options": {"num_ctx": LLM_CONTEXT_WINDOW},
            "timeout": OLLAMA_TIMEOUT,
        },
        embedding_func=EmbeddingFunc(
            embedding_dim=EMBED_DIM,
            max_token_size=EMBED_MAX_TOKENS,
            model_name=EMBED_MODEL,
            func=partial(
                ollama_embed.func,
                embed_model=EMBED_MODEL,
                host=OLLAMA_HOST,
            ),
        ),
    )

    return rag
