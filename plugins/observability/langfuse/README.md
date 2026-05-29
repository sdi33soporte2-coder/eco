# Langfuse Observability Plugin

This plugin ships bundled with ECO but is **opt-in** — it only loads when
you explicitly enable it.

## Enable

```bash
pip install langfuse
eco plugins enable observability/langfuse
```

Or check the box in the interactive `eco plugins` UI.

## Required credentials

Set these in `~/.eco/.env`:

```bash
HERMES_LANGFUSE_PUBLIC_KEY=pk-lf-...
HERMES_LANGFUSE_SECRET_KEY=sk-lf-...
HERMES_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```

Without the SDK or credentials the hooks no-op silently — the plugin fails
open.

## Verify

```bash
eco plugins list                 # observability/langfuse should show "enabled"
eco chat -q "hello"              # then check Langfuse for a "ECO turn" trace
```

## Optional tuning

```bash
HERMES_LANGFUSE_ENV=production       # environment tag
HERMES_LANGFUSE_RELEASE=v1.0.0       # release tag
HERMES_LANGFUSE_SAMPLE_RATE=0.5      # sample 50% of traces
HERMES_LANGFUSE_MAX_CHARS=12000      # max chars per field (default: 12000)
HERMES_LANGFUSE_DEBUG=true           # verbose plugin logging
```

## Disable

```bash
eco plugins disable observability/langfuse
```
