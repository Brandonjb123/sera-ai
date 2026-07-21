# ============================================================
# SERA AI — LLM Adapter (Multi-Provider)
# ============================================================
from openai import OpenAI

def call_llm(
    provider: str,
    api_key: str,
    model: str,
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 300
) -> str:
    """
    Panggil LLM dari berbagai provider dengan interface yang seragam.

    Args:
        provider: "groq" atau "openai" (mudah ditambah provider lain)
        api_key: API key client (plain text, akan dikirim langsung ke provider)
        model: nama model (contoh: "llama-3.3-70b-versatile", "gpt-4o-mini")
        messages: list of dict dengan format [{"role": "...", "content": "..."}]
        temperature: suhu kreativitas (0.0 - 1.0)
        max_tokens: batas token respons

    Returns:
        str: teks respons dari LLM
    """
    # Pilih base URL sesuai provider
    if provider == "groq":
        base_url = "https://api.groq.com/openai/v1"
        default_model = "llama-3.3-70b-versatile"
    elif provider == "openai":
        base_url = None  # OpenAI pakai default
        default_model = "gpt-4o-mini"
    else:
        raise ValueError(f"Provider tidak didukung: {provider}")

    # Inisialisasi client
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = OpenAI(**client_kwargs)

    # Panggil API
    response = client.chat.completions.create(
        model=model or default_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content