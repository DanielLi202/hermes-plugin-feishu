#!/usr/bin/env python3
"""Emit a Slack manifest with /tag plus a ready slack_tag config block."""
from __future__ import annotations

import json
import sys
from pathlib import Path

TAG_COMMAND = {
    "command": "/tag",
    "description": "Hermes Tag commands",
    "usage_hint": "help | status | admin count | standing ...",
    "url": "https://hermes-agent.local/slack/commands",
    "should_escape": False,
}


BASE_MANIFEST = {
    "display_information": {"name": "Hermes Tag"},
    "features": {"bot_user": {"display_name": "Hermes Tag", "always_online": True}, "slash_commands": []},
    "oauth_config": {
        "scopes": {
            "bot": [
                "app_mentions:read",
                "channels:history",
                "channels:read",
                "chat:write",
                "commands",
                "files:read",
                "groups:history",
                "groups:read",
                "im:history",
                "im:read",
                "mpim:history",
                "reactions:read",
                "reactions:write",
                "users:read",
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "bot_events": [
                "app_mention",
                "message.channels",
                "message.groups",
                "message.im",
                "message.mpim",
                "file_shared",
                "reaction_added",
                "reaction_removed",
            ]
        },
        "socket_mode_enabled": True,
        "org_deploy_enabled": False,
        "token_rotation_enabled": False,
    },
}

CONFIG_BLOCK = """\

--- slack_tag config ---
platforms:
  slack:
    enabled: true
    require_mention: false
    extra:
      slack_tag:
        enabled: true
        enabled_chats:
          - C_TEST_CHANNEL_ID
        admins:
          - U_YOUR_USER_ID
        encryption_posture: plaintext-db-on-local-disk
        db_path: ~/.hermes/profiles/shiling-pm/slack-tag.sqlite3
        media_cache_dir: ~/.hermes/profiles/shiling-pm/slack-tag-media
"""


def main() -> int:
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else None
    manifest = json.loads(path.read_text()) if path and path.exists() else json.loads(json.dumps(BASE_MANIFEST))
    scopes = manifest.setdefault("oauth_config", {}).setdefault("scopes", {}).setdefault("bot", [])
    if "commands" not in scopes:
        scopes.append("commands")
    commands = manifest.setdefault("features", {}).setdefault("slash_commands", [])
    if not any(cmd.get("command") == "/tag" for cmd in commands):
        # ponytail: Slack caps apps at 50 slash commands; trade one low-value core command for /tag.
        for drop in ("/version", "/usage", "/insights"):
            if any(cmd.get("command") == drop for cmd in commands):
                commands[:] = [cmd for cmd in commands if cmd.get("command") != drop]
                break
        commands.append(TAG_COMMAND)
    if len(commands) > 50:
        raise SystemExit(f"too many Slack slash commands: {len(commands)}")
    output = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if path:
        path.write_text(output)
        print(f"ok: wrote {path}; /tag present, {len(commands)} slash commands, commands scope present")
    else:
        print(output, end="")
    print(CONFIG_BLOCK, end="", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
