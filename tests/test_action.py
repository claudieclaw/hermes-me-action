import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


spec = importlib.util.spec_from_file_location(
    "me_action", Path(__file__).resolve().parents[1] / "__init__.py"
)
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)


def message(text, **overrides):
    fields = {"text": text, "internal": False, "allow_gateway_control": True, "source": object()}
    return SimpleNamespace(**{**fields, **overrides})


class MeActionTest(unittest.TestCase):
    def test_rewrites_only_text(self):
        event = message("  /ME raises a hand\nthen waves", message_id="message", media_urls=["attachment"])
        before = vars(event).copy()
        self.assertEqual(
            plugin.translate_action(event),
            {"action": "rewrite", "text": "[Sender action] raises a hand\nthen waves"},
        )
        self.assertEqual(vars(event), before)

    def test_bare_action(self):
        self.assertEqual(
            plugin.translate_action(message("/me"))["text"], "[The sender refers to themselves.]"
        )

    def test_action_text_does_not_become_a_command(self):
        self.assertEqual(plugin.translate_action(message("/me /approve"))["text"], "[Sender action] /approve")

    def test_passes_other_text_and_commands_through(self):
        for text in (None, "", "Try /me", "/menu", "/media", "/me.md", "/approve", "/me@other_bot waves"):
            with self.subTest(text=text):
                self.assertIsNone(plugin.translate_action(message(text)))

    def test_passes_internal_or_non_control_events_through(self):
        self.assertIsNone(plugin.translate_action(message("/me waves", internal=True)))
        self.assertIsNone(plugin.translate_action(message("/me waves", allow_gateway_control=False)))
        self.assertIsNone(plugin.translate_action(message("/me waves", source=None)))

    def test_registers_public_extension_points(self):
        context = Mock()
        plugin.register(context)
        context.register_hook.assert_called_once_with("pre_gateway_dispatch", plugin.translate_action)
        context.register_system_prompt_section.assert_called_once_with("me-action", plugin.ACTION_CONVENTION)


if __name__ == "__main__":
    unittest.main()
