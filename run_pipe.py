"""
One-shot runner for content_repurposer.pipe.

Reads examples/sample_blog_post.md, sends it through the four-platform
fan-out pipe via the local RocketRide engine, and writes each platform's
output to examples/sample_outputs/<platform>.md.

Connection details:
- The OpenAI key is loaded from .env via python-dotenv (the engine
  container also has it via --env-file).
- The local engine URI is overridden to ws://localhost:5565 since the
  default in ROCKETRIDE_URI points at the cloud service.
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from rocketride import RocketRideClient
from rocketride.schema import Question

ROOT = Path(__file__).parent
PIPE = ROOT / 'content_repurposer.pipe'
INPUT = ROOT / 'examples' / 'sample_blog_post.md'
OUT_DIR = ROOT / 'examples' / 'sample_outputs'

PLATFORMS = ['linkedin', 'x_thread', 'devto', 'instagram']

LOCAL_ENGINE_URI = 'ws://localhost:5565'


async def main() -> None:
    load_dotenv(ROOT / '.env')
    if not os.environ.get('ROCKETRIDE_OPENAI_KEY'):
        raise SystemExit('ROCKETRIDE_OPENAI_KEY missing from .env')

    blog_post = INPUT.read_text()
    print(f'input: {INPUT.name} ({len(blog_post)} chars)')

    async with RocketRideClient(uri=LOCAL_ENGINE_URI) as client:
        print(f'connected to {LOCAL_ENGINE_URI}')

        result = await client.use(filepath=str(PIPE), use_existing=True)
        token = result['token']
        print(f'pipe loaded, token={token[:8]}...')

        question = Question()
        question.addQuestion(blog_post)

        print('running pipe (4 parallel GPT-4o calls)...')
        response = await client.chat(token=token, question=question)

        result_types = response.get('result_types', {})
        answer_key = next(
            (key for key, lane in result_types.items() if lane == 'answers'),
            'answers',
        )
        answers = response.get(answer_key, [])

        if len(answers) != len(PLATFORMS):
            print(f'WARN: got {len(answers)} answers, expected {len(PLATFORMS)}')

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for platform, answer in zip(PLATFORMS, answers):
            out = OUT_DIR / f'{platform}.md'
            out.write_text(answer if isinstance(answer, str) else str(answer))
            print(f'wrote {out.relative_to(ROOT)} ({len(out.read_text())} chars)')


if __name__ == '__main__':
    asyncio.run(main())
