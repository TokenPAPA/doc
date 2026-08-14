#!/usr/bin/env python3
import json

posts_zh = [
    ('access-deepseek-from-us', {'title': '如何从美国访问 DeepSeek API（无需中国手机号）', 'date': '2026-06-26'}),
    ('fine-tune-llm-api-guide', {'title': '2026年LLM API微调完全指南：DeepSeek、GPT-5、Claude 4及更多', 'date': '2026-06-29'}),
    ('llm-api-error-handling-debugging', {'title': 'LLM API 错误处理与调试完全指南（2026）：常见错误与修复', 'date': '2026-06-30'}),
    ('llm-api-latency-comparison-2026', {'title': 'LLM API延迟与响应速度对比2026 — 哪个供应商最快？', 'date': '2026-07-01'}),
    ('llm-api-rate-limiting-retry-strategies', {'title': 'LLM API 限流与重试策略完全指南（2026）', 'date': '2026-06-29'}),
    ('multi-provider-llm-strategy', {'title': '2026年多提供商LLM策略：回退链、成本优化与冗余架构', 'date': '2026-06-30'}),
    ('openai-to-deepseek-migration-guide', {'title': '从OpenAI迁移到DeepSeek API完全指南 — 10分钟无缝切换', 'date': '2026-07-01'}),
    ('streaming-websocket-llm-guide', {'title': '实时 LLM API 完全指南：SSE 流式 vs WebSocket vs WebRTC（2026）', 'date': '2026-06-28'}),
]

posts_ja = [
    ('access-deepseek-from-us', {'title': '米国から DeepSeek API にアクセスする方法（中国の電話番号は不要）', 'date': '2026-06-26'}),
]

for lang, posts in [('zh', posts_zh), ('ja', posts_ja)]:
    for slug, info in posts:
        path = f'content/docs/{lang}/blog/{slug}.mdx'
        with open(path) as f:
            content = f.read()
        parts = content.split('---')
        if len(parts) < 3:
            print(f'SKIP {lang}/{slug}')
            continue
        jd = json.dumps({
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': info['title'],
            'description': info['title'],
            'datePublished': info['date'],
            'author': {'@type': 'Organization', 'name': 'TokenPAPA'},
            'publisher': {'@type': 'Organization', 'name': 'TokenPAPA'}
        }, ensure_ascii=False)
        block = f'---\n{parts[1]}---\n\nimport {{ JsonLd }} from "@/components/json-ld";\n\n<JsonLd json="{jd}" />\n'
        new_content = block + '---'.join(parts[2:])
        with open(path, 'w') as f:
            f.write(new_content)
        print(f'DONE {lang}/{slug}')

print('All ZH+JA done!')
