# rocketride-content-repurposer

A [RocketRide](https://rocketride.org) pipeline that takes one long-form blog post and produces four platform-native variants in parallel: a **LinkedIn** post, an **X (Twitter)** thread, a **dev.to** article summary, and an **Instagram** caption.

Built as a single `.pipe` file. No glue code, no orchestration scripts — RocketRide runs the fan-out itself.

---

## Why this exists

If you write long-form, you've probably retyped the same idea four times for four platforms. Each one wants a different shape: LinkedIn rewards opinion + hook, X rewards punchy + numbered, dev.to rewards markdown + structure, Instagram rewards warmth + visual line breaks.

This pipe does the rewriting once, in one pass, with prompts tuned per platform. The output is a list of four strings — paste each into the right surface.

---

## Architecture

```
                    ┌─→ prompt(LinkedIn)  → GPT-4o ──┐
                    │                                │
                    ├─→ prompt(X thread)  → GPT-4o ──┤
chat (paste post) ──┤                                ├─→ response (4 outputs)
                    ├─→ prompt(dev.to)    → GPT-4o ──┤
                    │                                │
                    └─→ prompt(Instagram) → GPT-4o ──┘
```

Ten components in one `.pipe` file:

| # | Component | Role |
|---|---|---|
| 1 | `chat_1` | Source — paste your blog post here |
| 2–5 | `prompt_{linkedin,twitter,devto,instagram}_1` | Platform-specific instruction templates |
| 6–9 | `llm_openai_{linkedin,twitter,devto,instagram}_1` | Four GPT-4o calls in parallel |
| 10 | `response_answers_1` | Single response node, four inputs (per RocketRide's fan-out pattern) |

The four LLM calls run in parallel — total latency is roughly one GPT-4o call, not four.

---

## Quick start

### Prerequisites

- [RocketRide engine](https://github.com/rocketride-org/rocketride-server) — install via the VS Code extension (recommended) or run the Docker image
- An OpenAI API key

### Run it

1. Clone this repo.
2. Copy `.env.example` to `.env` and add your OpenAI key:

   ```bash
   cp .env.example .env
   # edit .env, set ROCKETRIDE_OPENAI_KEY=sk-...
   ```

3. Open `content_repurposer.pipe` in VS Code with the RocketRide extension installed. The pipeline renders on the visual canvas.
4. Click ▶ on the `chat_1` source node (or open the chat panel) and paste a long-form blog post.
5. The four outputs come back as `response.answers` — one per platform.

### Run it programmatically (Python SDK)

```python
import asyncio
from rocketride import RocketRideClient
from rocketride.schema import Question

async def repurpose(blog_post: str):
    async with RocketRideClient() as client:
        result = await client.use(filepath='content_repurposer.pipe', use_existing=True)
        token = result['token']

        question = Question()
        question.addQuestion(blog_post)

        response = await client.chat(token=token, question=question)
        return response['answers']  # [LinkedIn, X thread, dev.to, Instagram]

with open('examples/sample_blog_post.md') as f:
    outputs = asyncio.run(repurpose(f.read()))

print('LINKEDIN:\n', outputs[0])
print('\nX THREAD:\n', outputs[1])
print('\nDEV.TO:\n', outputs[2])
print('\nINSTAGRAM:\n', outputs[3])
```

---

## Output order

```python
response['answers'][0]  # LinkedIn post
response['answers'][1]  # X (Twitter) thread
response['answers'][2]  # dev.to markdown
response['answers'][3]  # Instagram caption
```

Order matches the input order in `response_answers_1` in the pipe file.

---

## Customizing

### Change the platforms

Each platform is a `prompt` + `llm_openai` pair. Want to drop Reddit and add a TikTok script? Duplicate one of the prompt blocks, swap the instructions, point a new LLM node at it, and add an input to `response_answers_1`. That's the entire change.

### Swap GPT-4o for another model

The `openai-4o` profile is configurable in `pyproject.toml` of your RocketRide install. To swap to Claude:

```diff
- "provider": "llm_openai",
+ "provider": "llm_anthropic",
  "config": {
-   "profile": "openai-4o",
-   "openai-4o": { "apikey": "${ROCKETRIDE_OPENAI_KEY}" },
+   "profile": "claude",
+   "claude": { "apikey": "${ROCKETRIDE_ANTHROPIC_KEY}" },
    "parameters": {}
  }
```

### Production: webhook instead of chat

For a CMS integration ("when a new blog post is published, generate platform variants and queue them for review"), swap `chat` for `webhook`. The webhook accepts arbitrary text via HTTP POST, so you can wire it to a publish hook. You'll need to insert a `parse` and a `question` node between webhook and the four prompts to convert the incoming `tags` → `text` → `questions`.

---

## Built with

- [RocketRide](https://github.com/rocketride-org/rocketride-server) — open-source, developer-native AI pipeline tool
- OpenAI GPT-4o

---

## License

MIT
