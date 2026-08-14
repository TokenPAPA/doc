#!/usr/bin/env python3
"""Trim blog descriptions to 120-155 chars, fill missing keywords/category/date."""

import json

def trim_desc(text, max_chars=155, min_chars=120):
    """Trim description to length, prefer ending at sentence/word boundary."""
    text = text.strip()
    if len(text) <= max_chars and len(text) >= min_chars:
        return text

    # If too short, just return as-is
    if len(text) < min_chars:
        return text

    # Try to cut at sentence end first (within window)
    target = min(max_chars, len(text))
    for sep in ['. ', '? ', '! ', '.\n', '——']:
        idx = text.rfind(sep, min_chars, target)
        if idx > 0:
            result = text[:idx + len(sep)]
            # Remove trailing punctuation clutter
            result = result.rstrip(' .,;:')
            if len(result) >= min_chars:
                return result + '.'

    # Cut at last word boundary
    idx = text.rfind(' ', min_chars, target)
    if idx > 0:
        result = text[:idx].rstrip('.,;:')
        if len(result) >= min_chars:
            return result + '.'

    # Fallback: hard cut
    return text[:target].rstrip('.,;: ') + '.'

# ---- EN blog posts ----

# category lookup by slug pattern
cat_map = {
    'access-deepseek-from-us': 'Overseas Access',
    'ai-api-for-content-creation': 'Content Creation',
    'ai-api-key-management-security': 'Best Practices',
    'ai-api-without-phone-verification': 'Overseas Access',
    'cheapest-ai-apis-side-projects-2025': 'Developer Guides',
    'cheapest-llm-api-2026': 'Pricing',
    'chinese-llm-apis-complete-guide': 'Provider Guides',
    'claude-4-model-comparison': 'Model Comparison',
    'claude-api-guide-overseas': 'Provider Guides',
    'deepseek-api-for-us-developers': 'Developer Guides',
    'deepseek-api-key-overseas': 'Provider Guides',
    'deepseek-cache-hit-optimization': 'Technical Guides',
    'deepseek-coder-overseas-guide': 'Provider Guides',
    'deepseek-r1-advanced-use-cases': 'Technical Guides',
    'deepseek-r1-vs-v3-comparison': 'Model Comparison',
    'deepseek-v4-flash-vs-pro-guide': 'Model Comparison',
    'deepseek-vs-openai-pricing': 'Pricing',
    'deepseek-without-chinese-phone': 'Overseas Access',
    'fine-tune-llm-api-guide': 'Technical Guides',
    'flagship-llm-comparison-2026': 'Model Comparison',
    'gemini-api-guide-overseas': 'Provider Guides',
    'glm-4-api-guide-overseas': 'Provider Guides',
    'gpt-5-api-guide': 'Provider Guides',
    'llm-api-benchmarks-2026': 'Comparisons',
    'llm-api-error-handling-debugging': 'Technical Guides',
    'llm-api-latency-comparison-2026': 'Performance',
    'llm-api-pricing-comparison-2026': 'Pricing',
    'llm-api-rate-limiting-retry-strategies': 'Technical Guides',
    'llm-apis-for-indie-hackers': 'Developer Guides',
    'minimax-api-guide-overseas': 'Provider Guides',
    'mistral-api-guide': 'Provider Guides',
    'moonshot-kimi-api-guide-overseas': 'Provider Guides',
    'multi-provider-llm-api-aggregator': 'Comparisons',
    'multi-provider-llm-strategy': 'Technical Guides',
    'openai-to-deepseek-migration-guide': 'Migration Guide',
    'qwen-api-guide-overseas': 'Provider Guides',
    'streaming-websocket-llm-guide': 'Technical Guides',
    'tokenpapa-referral-free-api-credits': 'Promotions',
}

# Detailed fixes per slug: (new_desc or None, keywords or None, category or None, date or None)
fixes_en = {
    'access-deepseek-from-us': (
        "Sign up for DeepSeek API from the US without a Chinese phone. Step-by-step guide, pricing comparison, Python integration, and 3 working methods including TokenPAPA relay.",
        "[access DeepSeek US, no Chinese phone DeepSeek, DeepSeek API overseas, DeepSeek without phone verification, DeepSeek US registration, overseas DeepSeek access]",
        "Overseas Access",
        "2026-06-26"
    ),
    'ai-api-for-content-creation': (
        "Compare the best LLM APIs for content creation, marketing copy, and SEO content generation in 2026. DeepSeek V4, GPT-5, Claude Sonnet 4, and Gemini 2.5 use cases and cost analysis.",
        None, None, None
    ),
    'ai-api-without-phone-verification': (
        "Need AI API access without phone verification? Complete 2026 guide to accessing DeepSeek, GPT-5, Claude, Gemini, and more without a Chinese or US phone number. Use TokenPAPA for instant access.",
        None, None, None
    ),
    'best-llm-api-2026-comparison': (
        "2026's best LLM APIs compared: DeepSeek V4 Flash/Pro, GPT-4o, Claude Sonnet 4, Gemini 2.5, MiniMax, and more. Pricing, performance, and which API is best for your project.",
        None, None, None
    ),
    'cheapest-ai-apis-side-projects-2025': (
        "Find the cheapest AI APIs for side projects in 2025-2026. Compare DeepSeek, GPT-5 Mini, Claude Haiku, Gemini Flash pricing. Build on a budget without sacrificing quality.",
        None, None, None
    ),
    'cheapest-llm-api-2026': (
        "Find the cheapest LLM API in 2026. Compare DeepSeek V4 Flash pricing vs GPT-5 Mini, Claude Haiku, Gemini 2.5 Flash. Cache hit pricing, free tiers, and tokens per dollar analysis.",
        None, None, None
    ),
    'chinese-llm-apis-complete-guide': (
        "Complete guide to Chinese LLM APIs for overseas developers in 2026. Compare DeepSeek, Qwen, GLM-4, MiniMax, Moonshot Kimi. Pricing, capabilities, and access methods.",
        None, None, None
    ),
    'claude-4-model-comparison': (
        "Claude 4 Opus vs Sonnet vs Haiku: in-depth model comparison for 2026. Benchmark performance, pricing, use cases, and when to choose each Claude 4 variant for your project.",
        None, None, None
    ),
    'claude-api-guide-overseas': (
        "Claude API access guide for overseas developers in 2026. Compare Claude Sonnet 4 vs Opus vs Haiku pricing, features, and how to integrate Claude 4 API in your projects.",
        None, None, None
    ),
    'deepseek-cache-hit-optimization': (
        "Optimize DeepSeek API costs with cache hit strategies in 2026. Learn prompt engineering for cache hits, multi-turn conversation caching, and reduce costs by up to 90%.",
        None, None, None
    ),
    'deepseek-coder-overseas-guide': (
        "Access DeepSeek Coder V2 API from overseas. Comprehensive guide for coding tasks, code generation pricing, features, and how to integrate with external API providers like TokenPAPA.",
        None, None, None
    ),
    'deepseek-r1-advanced-use-cases': (
        "Explore advanced DeepSeek R1 use cases in 2026. Agentic reasoning, multi-step planning, code generation, Chain-of-Thought, and production deployment strategies for R1 models.",
        None, None, None
    ),
    'deepseek-r1-vs-v3-comparison': (
        "DeepSeek R1 vs V3 detailed comparison for 2026. Compare reasoning capability, speed, pricing, coding benchmarks, and choose the right DeepSeek model for your specific use case.",
        None, None, None
    ),
    'deepseek-vs-openai-pricing': (
        "Compare DeepSeek vs OpenAI pricing in 2026. DeepSeek V4, V3, R1 vs GPT-5, GPT-4o cost per token. See how much you save switching from OpenAI to DeepSeek with TokenPAPA.",
        None, None, None
    ),
    'fine-tune-llm-api-guide': (
        "Complete guide to fine-tuning LLMs via API in 2026. Covers DeepSeek V4 fine-tuning, OpenAI GPT-5, Claude 4 custom models, Qwen fine-tuning, dataset preparation, and cost comparison.",
        None, None, None
    ),
    'flagship-llm-comparison-2026': (
        "Flagship LLM model comparison 2026: DeepSeek V4 Pro vs GPT-5.5 vs Claude 4 Opus vs Gemini 2.5 Pro. Benchmark performance, pricing, speed, and which flagship is right for you.",
        None, None, None
    ),
    'gemini-api-guide-overseas': (
        "Gemini API access guide for overseas developers in 2026. Gemini 2.5 Pro vs Flash pricing, features, and how to integrate Google's latest multimodal models with TokenPAPA relay.",
        None, None, None
    ),
    'glm-4-api-guide-overseas': (
        "Access GLM-4 API from overseas in 2026. Comprehensive guide to Zhipu AI's GLM-4 model capabilities, pricing, and integration with TokenPAPA for developers outside China.",
        None, None, None
    ),
    'gpt-5-api-guide': (
        "GPT-5 API complete guide for 2026. GPT-5.5 vs 5.4 vs 5 Mini pricing, features, streaming, vision, and code generation. How to access and integrate OpenAI's latest models.",
        None, None, None
    ),
    'llm-api-benchmarks-2026': (
        "Real-world benchmark results for DeepSeek V4 Flash/Pro, GPT-5.5/5.4, Claude 4 Opus/Sonnet/Haiku, and Gemini 2.5 Pro/Flash. MMLU, coding, reasoning, latency and cost-per-task comparisons.",
        None, None, None
    ),
    'llm-api-error-handling-debugging': (
        "Complete guide to LLM API error handling in 2026. Covers 401, 403, 429, 500, 503, 529 errors for OpenAI GPT-5, DeepSeek V4, Claude 4, Gemini 2.5 with debugging tips and fixes.",
        None, None, None
    ),
    'llm-api-latency-comparison-2026': (
        "Real-world LLM API latency comparison: DeepSeek vs GPT-5 vs Claude vs Gemini. Time-to-first-token, tokens per second, and geographic latency benchmarks for production applications.",
        None, None, None
    ),
    'llm-api-pricing-comparison-2026': (
        "Complete LLM API pricing comparison for 2026. DeepSeek V4, GPT-5, Claude 4, Gemini 2.5, MiniMax, Qwen — input/output costs per million tokens plus cache hit and batch pricing.",
        None, None, None
    ),
    'llm-api-rate-limiting-retry-strategies': (
        "Master LLM API rate limiting, exponential backoff retry, and concurrent request management for OpenAI, DeepSeek V4, Claude 4, Gemini. Code examples in Python, Node.js, and curl.",
        None, None, None
    ),
    'llm-apis-for-indie-hackers': (
        "Best LLM APIs for indie hackers and solo developers in 2026. Compare DeepSeek, GPT-5 Mini, Claude Haiku, Gemini Flash. Cost-effective options with free tiers for bootstrapped projects.",
        None, None, None
    ),
    'mistral-api-guide': (
        "Complete Mistral AI API guide for 2026. Mistral Large 2 vs Small vs Codestral pricing, features, benchmarks, and how to access Mistral models from overseas via TokenPAPA relay.",
        None, None, None
    ),
    'moonshot-kimi-api-guide-overseas': (
        "Access Moonshot Kimi API from overseas in 2026. Complete guide to Kimi k1.5 model capabilities, long context window features, pricing, and integration with TokenPAPA for global developers.",
        None, None, None
    ),
    'multi-provider-llm-api-aggregator': (
        "Why use a multi-provider LLM API aggregator in 2026. Compare TokenPAPA vs direct providers: unified billing, fallback chains, cost optimization, and single API key for all models.",
        None, None, None
    ),
    'multi-provider-llm-strategy': (
        "Build a multi-provider LLM strategy in 2026. Covers fallback chains between OpenAI, DeepSeek, Claude, Gemini, cost optimization, load balancing, and high-availability LLM architecture.",
        None, None, None
    ),
    'openai-to-deepseek-migration-guide': (
        "Complete guide to migrating from OpenAI to DeepSeek API. Code examples, endpoint mapping, model equivalents, cost savings analysis, and overseas access via TokenPAPA relay.",
        None, None, None
    ),
    'streaming-websocket-llm-guide': (
        "Compare SSE streaming, WebSocket, and WebRTC for real-time LLM APIs in 2026. Covers DeepSeek V4 cache-hit streaming, GPT-5 streaming, Claude 4 extended thinking, and Gemini Live API.",
        None, None, None
    ),
    'tokenpapa-referral-free-api-credits': (
        "TokenPAPA referral program: earn free API credits by inviting friends. Get $5 for each referral, unlimited rewards, and access 200+ AI models at cost. How the TokenPAPA referral system works.",
        None, None, None
    ),
    'deepseek-v4-flash-vs-pro-guide': (
        "DeepSeek V4 Flash vs Pro detailed comparison in 2026. Speed benchmarks, pricing breakdown, use cases for each variant, and how to choose between Flash and Pro for your workload.",
        None, None, None
    ),
    'deepseek-vs-openai-pricing': (
        "Compare DeepSeek vs OpenAI pricing in 2026. DeepSeek V4, V3, R1 vs GPT-5, GPT-4o cost per token. See how much you save switching from OpenAI to DeepSeek with TokenPAPA.",
        None, None, None
    ),
}

def parse_frontmatter(content):
    """Split content into frontmatter dict and body."""
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    fm_lines = parts[1].strip().split('\n')
    fm = {}
    body = parts[2]
    for line in fm_lines:
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip()
            fm[key] = val
    return fm, body

def rebuild_frontmatter(fm, body):
    """Rebuild the full file content from frontmatter dict + body."""
    lines = []
    for key, val in fm.items():
        lines.append(f'{key}: {val}')
    return '---\n' + '\n'.join(lines) + '\n---\n' + body

def process_file(path, name, lang):
    with open(path) as f:
        content = f.read()
    
    fm, body = parse_frontmatter(content)
    changed = False
    
    # Fix description (EN only for trim)
    if lang == 'en' and name in fixes_en:
        new_desc = fixes_en[name][0]
        if new_desc:
            old_desc = fm.get('description', '').strip('"').strip("'")
            if old_desc != new_desc:
                fm['description'] = f'"{new_desc}"'
                changed = True
                print(f"  {lang}/{name}: description trimmed {len(old_desc)} -> {len(new_desc)} chars")
    
    # Fix keywords
    if name in fixes_en:
        new_kw = fixes_en[name][1]
        if new_kw:
            fm['keywords'] = new_kw
            changed = True
            print(f"  {lang}/{name}: added keywords")
    
    # Fix category
    if name in cat_map:
        if 'category' not in fm or not fm['category'].strip():
            fm['category'] = cat_map[name]
            changed = True
            print(f"  {lang}/{name}: added category '{cat_map[name]}'")
    
    # Fix date
    if name in fixes_en:
        new_date = fixes_en[name][3]
        if new_date and ('date' not in fm or not fm['date'].strip()):
            fm['date'] = new_date
            changed = True
            print(f"  {lang}/{name}: added date '{new_date}'")
    
    if changed:
        new_content = rebuild_frontmatter(fm, body)
        with open(path, 'w') as f:
            f.write(new_content)
        return True
    return False

# Process all files
base = '/home/newApi/tokenpapa-doc/content/docs'
total = 0
for lang in ['en', 'ja', 'zh']:
    import glob
    for path in sorted(glob.glob(f'{base}/{lang}/blog/*.mdx')):
        name = path.split('/')[-1].replace('.mdx', '')
        if name == 'index':
            continue
        if process_file(path, name, lang):
            total += 1

print(f'\nDone! {total} files modified.')
