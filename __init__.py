"""Interpret /me as ordinary conversation in Hermes messaging chats."""


ACTION_CONVENTION = (
    "A chat message that starts with /me or [Sender action] describes "
    "an action or state of the person who sent it. Attribute it to the "
    "indicated sender."
)


def translate_action(event):
    if event.internal or not event.allow_gateway_control or event.source is None:
        return None
    parts = (event.text or "").split(maxsplit=1)
    if not parts or parts[0].lower() != "/me":
        return None
    action = parts[1] if len(parts) == 2 else ""
    text = f"[Sender action] {action}" if action else "[The sender refers to themselves.]"
    return {"action": "rewrite", "text": text}


def register(ctx):
    ctx.register_hook("pre_gateway_dispatch", translate_action)
    # Busy steers can bypass ingress. A built prompt supplies the same meaning.
    ctx.register_system_prompt_section("me-action", ACTION_CONVENTION)
