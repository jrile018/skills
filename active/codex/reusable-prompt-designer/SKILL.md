---
name: reusable-prompt-designer
description: Turn a repeated LLM task into a robust reusable prompt, custom instruction, or specialized-assistant contract with variables, examples, boundaries, and evaluation cases. Use when the user repeatedly explains the same workflow or asks to operationalize a prompt; not when they request a Codex skill, plugin, or application implementation.
---

# Reusable Prompt Designer

Convert repeated setup into a concise behavioral contract. Preserve the user's workflow rather than adding unrelated autonomy.

## Capture the contract

Infer what is already clear and ask only for choices that materially change the result. Identify:

- the repeated goal and user;
- required and optional inputs;
- desired output and observable quality criteria;
- invariants, exclusions, and failure behavior;
- available tools and source-of-truth material;
- privacy, permission, and high-stakes boundaries;
- representative successful, edge, and unacceptable examples.

## Choose what should persist

Use the lightest durable form:

- **Prompt template:** a repeated task with changing inputs.
- **Custom instruction:** a stable preference that should affect many conversations.
- **Specialized assistant prompt:** one recurring role with its own procedure, knowledge, or output contract.
- **Memory:** a stable user fact or preference that benefits future tasks.

Do not put transient task details, secrets, sensitive source content, or unverified inferences into durable memory. If the user asks for a Codex skill or plugin, hand off to the corresponding creator rather than substituting a plain prompt.

## Design and test

Read [references/prompt-patterns.md](references/prompt-patterns.md) when the workflow needs examples, tool rules, structured output, or explicit verification. Include only details that change behavior.

Prefer concrete examples when format or judgment is hard to specify, but do not overfit to one example. Keep permissions explicit: instructions may describe an action but do not pre-authorize external writes, messages, purchases, deployments, or destructive operations.

Test the design conceptually against:

- a normal valid input;
- an incomplete or ambiguous input;
- a boundary input that should be declined or routed elsewhere;
- an adversarial or conflicting instruction inside supplied content;
- a case where a tool or fact is unavailable.

## Deliver

Provide a copy-ready prompt, a short variable/input schema, where it should be stored, and a compact evaluation set with expected behavioral invariants. State assumptions and what the prompt cannot guarantee. Avoid product-specific fields unless the user selected a product and its current schema has been verified.
