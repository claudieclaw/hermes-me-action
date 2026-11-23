# Me Action for Hermes Agent

Use IRC-style actions in Hermes messaging chats. When someone writes
`/me raises a hand`, Hermes passes `[Sender action] raises a hand` to the
agent with the original sender's identity. Inbound attachments and reply
metadata stay on the same message. The action follows the chat's normal reply
policy.

## Install

Requires Hermes Agent 0.23.3 or later. Tested with 0.23.3.

```sh
hermes plugins install claudieclaw/hermes-me-action
hermes plugins enable me-action
```

On a gateway that serves multiple profiles, install and enable the plugin in
each profile where you want it. Use `hermes --profile NAME` for a named profile.

## How it works

A leading, standalone `/me` token is rewritten before slash dispatch, and
Hermes continues through its normal ingress path. The plugin uses the public
`pre_gateway_dispatch` hook and a system-prompt section. On Hermes 0.23.3
some mid-turn steers bypass this hook. A rebuilt prompt teaches the agent the
same convention for the literal command. An existing cached prompt gets that
section the next time Hermes rebuilds it.

Example inputs include `/me nods`, `/ME nods`, and a bare `/me`. Commands such
as `/menu` and uses of `/me` elsewhere in ordinary text pass through unchanged.

The plugin works on the inbound text provided by Hermes. It makes no network
requests, launches no processes, stores no data, and uses no credentials.

## Test

```sh
python -m unittest discover -s tests
hermes plugins validate . --install-deps
```

Licensed under MIT.
