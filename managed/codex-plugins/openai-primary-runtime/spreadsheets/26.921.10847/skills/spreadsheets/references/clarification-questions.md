# Clarification questions

Ask the user one clarifying question about the unresolved detail that would most affect the result, such as audience, purpose, scope, style, or data sources.
Check the chat history and attachments and reuse answers already given. Ask only once. If everything is already specified, ask whether there is anything else to prioritize before proceeding.

Use `request_user_input_async` if available, otherwise send a message. For choices, offer two great options. Make the first recommended. Have `Use your judgment` as the third option. Continue independent work like finding a template if none was provided while allowing 40 seconds for a reply. If none arrives, make a reasonable assumption or use a visible placeholder, and disclose it. Do not stop the turn.
