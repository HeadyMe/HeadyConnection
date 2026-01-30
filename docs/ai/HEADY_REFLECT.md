# HeadyReflect (Socratic Validation Cycle)

HeadyReflect requires structured reflection before sensitive tool execution.

## Reflection Object
```
{
  "question": "What is the action and why is it necessary?",
  "answer": "Short justification.",
  "risk": "Low/Medium/High"
}
```

## MCP Gateway Enforcement
Set `HEADY_REFLECT_ENFORCE=1` in the MCP gateway environment to require reflection objects for tool calls.
