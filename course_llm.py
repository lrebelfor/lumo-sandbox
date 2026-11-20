"""course_llm: one small helper so every lab works with the model you chose in Session 2.

    from course_llm import LLM
    llm = LLM("claude")          # or "openai", "gemini", "openrouter" (free open models), "ollama" (local)
    reply = llm.ask("Hello!")
    print(reply.text, reply.tokens_in, reply.tokens_out)

Routes
- claude      Anthropic API (reference route: every lab is tested on it weekly)
- openai      OpenAI API
- gemini      Google Gemini API; has a free tier (free-tier inputs may be used by Google to improve its products)
- openrouter  OpenRouter: many open models, some free (model ids ending in ':free'); quality and tool use vary
- ollama      Open models on your own computer (not in Colab); fully private, needs a decent laptop

Keys are read from Colab Secrets, then environment variables:
ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY. Ollama needs none.

Model ids change often. The defaults below were checked on 20 Nov 2026; the course's monthly freshness
check flags when one is retired. Pass model="..." to use another.
"""
import json
import os
from dataclasses import dataclass

ROUTES = {
    "claude": {"kind": "anthropic", "model": "claude-haiku-5-5", "large": "claude-sonnet-5-5",
               "key": "ANTHROPIC_API_KEY", "prices": {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00)}},
    "openai": {"kind": "openai", "model": "gpt-5.4-mini", "large": "gpt-5.5", "key": "OPENAI_API_KEY",
               "base_url": None, "max_param": "max_completion_tokens", "prices": {}},
    "gemini": {"kind": "openai", "model": "gemini-3.8-flash", "large": "gemini-3.1-pro-preview", "key": "GEMINI_API_KEY",
               "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/", "prices": {}},
    "openrouter": {"kind": "openai", "model": "openai/gpt-oss-120b:free", "large": "openai/gpt-oss-120b:free",
                   "key": "OPENROUTER_API_KEY", "base_url": "https://openrouter.ai/api/v1", "prices": {}},
    "ollama": {"kind": "openai", "model": "qwen3.5:4b", "large": "qwen3.5:9b", "key": None,
               "base_url": "http://localhost:11434/v1", "prices": {}},
}


def get_key(name):
    """Colab Secrets first, then environment variables."""
    if not name:
        return "ollama"
    try:
        from google.colab import userdata
        value = userdata.get(name)
        if value:
            return value
    except Exception:
        pass
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"No API key found. Add {name} to Colab Secrets (key icon, left sidebar) "
                           f"and switch on Notebook access, or set it as an environment variable.")
    return value


@dataclass
class Reply:
    text: str
    tokens_in: int
    tokens_out: int
    model: str
    cost: float | None = None   # in dollars, when the course knows the model's price

    def __str__(self):
        return self.text


def tool(name, description, parameters, fn):
    """Describe a Python function as a tool the model may ask for.
    parameters: {"arg": ("string", "what it is"), ...}; all are required."""
    props = {k: {"type": t, "description": d} for k, (t, d) in parameters.items()}
    return {"name": name, "description": description, "fn": fn,
            "schema": {"type": "object", "properties": props, "required": list(parameters)}}


class LLM:
    def __init__(self, route="claude", model=None, api_key=None):
        if route not in ROUTES:
            raise ValueError(f"Unknown route '{route}'. Choose one of: {', '.join(ROUTES)}")
        self.route = route
        self.cfg = ROUTES[route]
        self.model = model or self.cfg["model"]
        self.large_model = self.cfg["large"]
        key = api_key or get_key(self.cfg["key"])
        if self.cfg["kind"] == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=key)
        else:
            import openai
            self.client = openai.OpenAI(api_key=key, base_url=self.cfg["base_url"])

    def __repr__(self):
        return f"LLM(route={self.route!r}, model={self.model!r})"

    # ---------- one question, one answer ----------
    def ask(self, prompt, system="", model=None, max_tokens=1500):
        """Send one message. Returns a Reply with .text, .tokens_in, .tokens_out and .cost."""
        return self._call([{"role": "user", "content": prompt}], system, model or self.model, max_tokens)[0]

    def _call(self, messages, system, model, max_tokens, tools=None, schema=None):
        if self.cfg["kind"] == "anthropic":
            kw = {"model": model, "max_tokens": max_tokens, "messages": messages}
            if system:
                kw["system"] = system
            if tools:
                kw["tools"] = [{"name": t["name"], "description": t["description"], "input_schema": t["schema"]} for t in tools]
            if schema:
                kw["output_config"] = {"format": {"type": "json_schema", "schema": schema}}
            r = self.client.messages.create(**kw)
            text = "".join(b.text for b in r.content if b.type == "text")
            reply = self._reply(text, r.usage.input_tokens, r.usage.output_tokens, model)
            return reply, r
        msgs = ([{"role": "system", "content": system}] if system else []) + messages
        kw = {"model": model, "messages": msgs, self.cfg.get("max_param", "max_tokens"): max_tokens}
        if tools:
            kw["tools"] = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                             "parameters": t["schema"]}} for t in tools]
        if schema:
            kw["response_format"] = {"type": "json_schema", "json_schema": {"name": "result", "schema": schema, "strict": True}}
        r = self.client.chat.completions.create(**kw)
        msg = r.choices[0].message
        u = r.usage
        reply = self._reply(msg.content or "", getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0, model)
        return reply, r

    def _reply(self, text, t_in, t_out, model):
        price = self.cfg["prices"].get(model)
        cost = (t_in * price[0] + t_out * price[1]) / 1_000_000 if price else None
        return Reply(text, t_in, t_out, model, cost)

    # ---------- structured output ----------
    def json(self, prompt, schema, system="", model=None):
        """Ask for an answer that matches a JSON schema; returns a Python dict.
        Uses the provider's structured-output mode, and falls back to asking for JSON in the prompt."""
        try:
            reply, _ = self._call([{"role": "user", "content": prompt}], system, model or self.model, 1500, schema=schema)
            return json.loads(reply.text)
        except Exception as first_error:
            if self.route in ("claude", "openai"):
                raise
            # Some open models don't support schemas: ask for JSON in plain words instead.
            p = f"{prompt}\n\nReply with ONLY a JSON object matching this JSON schema, no other text:\n{json.dumps(schema)}"
            text = self.ask(p, system=system, model=model).text.strip()
            text = text[text.find("{"): text.rfind("}") + 1]
            try:
                return json.loads(text)
            except ValueError:
                raise RuntimeError(f"The model didn't return valid JSON ({first_error}). Try another model.")

    # ---------- the agent loop ----------
    def run_agent(self, question, tools, system="", max_steps=6, model=None, verbose=True):
        """The tool loop from Session 4: ask, run any tool the model requests, send the result back, repeat."""
        fns = {t["name"]: t["fn"] for t in tools}
        model = model or self.model
        messages = [{"role": "user", "content": question}]
        for step in range(1, max_steps + 1):
            reply, raw = self._call(messages, system, model, 2000, tools=tools)
            calls = self._tool_calls(raw)
            if not calls:
                return reply.text
            self._append_assistant(messages, raw)
            results = []
            for call_id, name, args in calls:
                try:
                    out = str(fns[name](**args))
                except Exception as e:
                    out = f"Error: {e}"
                if verbose:
                    print(f"  [step {step}] the agent decided to call {name}({args}) -> {out[:80]}")
                results.append((call_id, name, out))
            self._append_results(messages, results)
        return "Stopped: too many steps."

    def _tool_calls(self, raw):
        if self.cfg["kind"] == "anthropic":
            if raw.stop_reason != "tool_use":
                return []
            return [(b.id, b.name, b.input) for b in raw.content if b.type == "tool_use"]
        calls = raw.choices[0].message.tool_calls or []
        return [(c.id, c.function.name, json.loads(c.function.arguments or "{}")) for c in calls]

    def _append_assistant(self, messages, raw):
        if self.cfg["kind"] == "anthropic":
            messages.append({"role": "assistant", "content": raw.content})
        else:
            m = raw.choices[0].message
            messages.append({"role": "assistant", "content": m.content or "",
                             "tool_calls": [c.model_dump() for c in m.tool_calls]})

    def _append_results(self, messages, results):
        if self.cfg["kind"] == "anthropic":
            messages.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": cid, "content": out} for cid, _, out in results]})
        else:
            for cid, _, out in results:
                messages.append({"role": "tool", "tool_call_id": cid, "content": out})

    # ---------- LangChain (Session 10 and Levels 2-3) ----------
    def langchain_model(self, model=None, **kw):
        """The same model as a LangChain chat model, for LangChain and LangGraph."""
        model = model or self.model
        if self.cfg["kind"] == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model=model, api_key=self.client.api_key, max_tokens=kw.pop("max_tokens", 1500), **kw)
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, api_key=self.client.api_key, base_url=self.cfg["base_url"], **kw)
