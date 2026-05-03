# Sample outputs

These are **illustrative** outputs — what the four platform-specific prompts in `content_repurposer.pipe` would produce when the source post `examples/sample_blog_post.md` is sent through GPT-4o.

To regenerate them with the real model, install the RocketRide engine, set `ROCKETRIDE_OPENAI_KEY` in your `.env`, and run the pipe (see the main [README](../../README.md) for instructions).

| File | Platform |
|---|---|
| [`linkedin.md`](linkedin.md) | LinkedIn post (~1,300 chars max, professional, hook + insight + soft question) |
| [`x_thread.md`](x_thread.md) | X (Twitter) thread (5–8 numbered tweets, ≤280 chars each) |
| [`devto.md`](devto.md) | dev.to article in markdown (TL;DR + 3 takeaways + CTA) |
| [`instagram.md`](instagram.md) | Instagram caption (800–1,500 chars, conversational, with hashtags) |
