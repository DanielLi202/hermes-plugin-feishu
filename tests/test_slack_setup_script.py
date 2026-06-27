import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "docs" / "slack-manifest-add-tag.py"


class SlackSetupScriptTest(unittest.TestCase):
    def test_stdout_manifest_and_stderr_config_block(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], text=True, capture_output=True, check=True)
        manifest = json.loads(result.stdout)
        commands = manifest["features"]["slash_commands"]
        self.assertTrue(any(cmd["command"] == "/tag" for cmd in commands))
        self.assertIn("commands", manifest["oauth_config"]["scopes"]["bot"])
        self.assertIn("slack_tag:", result.stderr)
        self.assertIn("C_TEST_CHANNEL_ID", result.stderr)

    def test_patches_existing_manifest_in_place(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            json.dump({"features": {"slash_commands": []}, "oauth_config": {"scopes": {"bot": []}}}, f)
            path = f.name
        result = subprocess.run([sys.executable, str(SCRIPT), path], text=True, capture_output=True, check=True)
        manifest = json.loads(Path(path).read_text())
        self.assertIn("/tag", [cmd["command"] for cmd in manifest["features"]["slash_commands"]])
        self.assertIn("commands", manifest["oauth_config"]["scopes"]["bot"])
        self.assertIn("wrote", result.stdout)
        self.assertIn("slack_tag:", result.stderr)


if __name__ == "__main__":
    unittest.main()
