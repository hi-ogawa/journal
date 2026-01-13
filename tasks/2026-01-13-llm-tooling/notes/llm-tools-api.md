# LLM Tools/Function Calling API - How It Works

## Overview

Understanding how LLM "tools" (function calling) work at the API level, particularly how AI SDK maps to underlying LLM provider APIs.

## Tool Definition

Tools are defined as JSON schemas sent with each request:

```json
{
  "tools": [{
    "name": "get_weather",
    "description": "Get weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": { "type": "string" }
      }
    }
  }]
}
```

## Request-Response Flow

The flow is **sequential HTTP round-trips**, not bidirectional streaming:

```
Request 1: User message + tool definitions
    ↓
Response 1: LLM outputs tool_use block (streamed via SSE)
    ↓
[Client executes tool locally]
    ↓
Request 2: Original messages + tool_result
    ↓
Response 2: LLM continues with final answer (streamed)
```

Key point: You cannot send tool results mid-stream. Each response must complete before making a new request with results.

## AI SDK Abstraction

A single AI SDK call (e.g., `streamText()`) can involve **multiple HTTP requests** underneath:

```typescript
const result = await streamText({
  model: openai('gpt-4'),
  tools: { weather: weatherTool },
  maxSteps: 5,  // allows up to 5 round-trips
  prompt: "What's the weather in Tokyo?"
});
```

The SDK stitches multiple streaming responses into one unified interface. The UX feels smooth because each step streams visibly.

## Billing & Quota Implications

Each underlying HTTP request:
1. Is a **separate billable API call**
2. **Re-sends the full conversation context**

Token usage compounds with each step:

```
Step 1: Input 500 tokens, Output 50 tokens
Step 2: Input 650 tokens (previous context + tool_result), Output 200 tokens

Total: 1,150 input + 250 output tokens
```

Rate limits (RPM, TPM) are also hit per-request, so an agentic loop with 10 tool calls = 10 API requests.

## How LLMs "Know" About Tools

Two layers:

### 1. Model Training
Modern LLMs (GPT-4, Claude) are fine-tuned to:
- Recognize tool definition formats
- Know when to emit structured `tool_use` output vs. regular text
- Output valid JSON for tool arguments

### 2. Prompt Injection
Tool definitions are injected into the prompt by the provider API. Evidence: tools consume input tokens.

```
[Internal prompt]
You have access to these tools:
- get_weather: Get weather for a location
  Parameters: { location: string }
[User message]
```

## Where Prompt Manipulation Happens

```
Your Code (AI SDK format)
    ↓
AI SDK: Schema translation between providers
    ↓
Provider API (OpenAI/Anthropic): Injects tools into prompt internally
    ↓
Model: Sees tools as part of prompt context
```

AI SDK's role is **API normalization** (translating tool schemas and response formats between providers), not prompt manipulation.

Provider-specific formats:
- OpenAI: `tools[].function.parameters`
- Anthropic: `tools[].input_schema`

For models without native tool support, libraries must do prompt injection and output parsing manually.

## Why Not Bidirectional Streaming?

Current APIs use unidirectional SSE. A bidirectional approach (WebSocket/gRPC) could theoretically work but isn't implemented because:

1. **Model architecture** - The model genuinely stops generation at tool calls; it's not pausing mid-stream
2. **Stateless scaling** - HTTP request-response is easier to load-balance across GPU clusters
3. **Simpler infrastructure** - SSE works everywhere

## Source Code References

### Vercel AI SDK (Schema Translation Layer)

The AI SDK translates its unified tool format to provider-specific formats:

**Repository:** [vercel/ai](https://github.com/vercel/ai)

| Provider | Key File | Function |
|----------|----------|----------|
| OpenAI | [`packages/openai/src/chat/openai-chat-prepare-tools.ts`](https://github.com/vercel/ai/blob/main/packages/openai/src/chat/openai-chat-prepare-tools.ts) | `prepareChatTools()` - converts AI SDK tools to OpenAI format (`tools[].function`) |
| Anthropic | [`packages/anthropic/src/anthropic-prepare-tools.ts`](https://github.com/vercel/ai/blob/main/packages/anthropic/src/anthropic-prepare-tools.ts) | `prepareTools()` - converts AI SDK tools to Anthropic format (`tools[].input_schema`) |

The conversion is called from the language model implementations:
- OpenAI: [`packages/openai/src/chat/openai-chat-language-model.ts`](https://github.com/vercel/ai/blob/main/packages/openai/src/chat/openai-chat-language-model.ts)
- Anthropic: [`packages/anthropic/src/anthropic-messages-language-model.ts`](https://github.com/vercel/ai/blob/main/packages/anthropic/src/anthropic-messages-language-model.ts)

### Provider SDKs (API Layer)

These SDKs send the provider-formatted tools to the API. Prompt injection happens server-side (not visible in client SDKs):

| Provider | Repository |
|----------|------------|
| OpenAI | [openai/openai-node](https://github.com/openai/openai-node) |
| Anthropic | [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript) |

### Provider API Documentation

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
