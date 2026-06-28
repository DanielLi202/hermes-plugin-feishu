# README hero GIF script

## Goal

Record a **real Hermes + hermes-tag + Lark/Feishu** demo for the README hero.

The GIF should prove the headline, not document setup:

> **Post first, @ last — it already has everything that matters.**

Show that Hermes Tag stays quiet while useful context accumulates, then answers after a late @ using the original images, the user's note, and relevant replies. It should not look like last-message-only chat, and it should not imply whole-history retrieval.

## Constraints

- Use only a test group and synthetic data.
- Do not show private chats, names, sidebars, secrets, hostnames, tokens, or real business screenshots.
- Record the chat pane only; crop away sidebars and account UI.
- Keep the bot answer real. If the bot fails to answer correctly, do not fake it in post.
- Target: 14-18s, 960x540 source, README display width 720px, 12-15 fps.

## Storyboard

| Time | Real action | Viewer sees | Why it matters |
| --- | --- | --- | --- |
| 0.0-1.0s | Start on clean test group | Title overlay: `Post first, @ last.` | Immediate hook. |
| 1.0-4.0s | Upload three generated chart images | Three thumbnails appear | Context exists before the bot is mentioned. |
| 4.0-5.5s | Send a short note | `Note: mobile conversion dipped after Friday's deploy.` | User explanation is retained. |
| 5.5-7.8s | Send two relevant replies and one unrelated line | Related replies stay bright; unrelated line gets a subtle post-production dim/highlight | Shows selective context, not whole-history retrieval. |
| 7.8-9.0s | Pause | Overlay: `silent until mentioned` | Quiet behavior is the feature. |
| 9.0-10.5s | Mention the bot | `@Hermes Tag summarize what matters from the images above.` | Late @ triggers retrieval. |
| 10.5-15.5s | Wait for real bot reply | Bot answer mentions the original images, note, and relevant replies | This is the proof shot. |
| 15.5-17.0s | Freeze on answer | Overlay chips: `original images` `your note` `related replies` `not whole history` | Landing frame for README skimmers. |

## Exact demo script

Use the Chinese version for the real Feishu/Lark recording.

1. Upload three generated chart images:
   - `demo-chart-revenue.png`
   - `demo-chart-funnel.png`
   - `demo-chart-ios-spike.png`
2. Send: `说明：周五发布后，移动端转化掉了一段。`
3. Send: `第二张图已经换了新漏斗口径。`
4. Send: `第三张里的 spike 只出现在 iOS。`
5. Send: `中午 12 点吃饭？`
6. Pause 1s. Bot should stay silent.
7. Send: `@时令 PM 看上面几张图和讨论，帮我总结关键结论。`
8. Expected bot answer must include, in substance:
   - it used the images above / charts;
   - Friday deploy or Friday release note;
   - new funnel definition;
   - iOS-only spike;
   - it should not anchor on the lunch message.

Do not use the exact expected answer as an overlay unless it is what the bot actually returns.

## Local execution notes

Local runtime details live in `docs/local-runtime.md` and must stay out of git. Use it for:

- remote Hermes host/profile/path;
- safe Feishu test group;
- configured bot display name;
- gateway log command;
- acceptance smoke commands.

Current local exploration showed this path is viable:

- remote Hermes is reachable over SSH from this Mac;
- `hermes-tag` is enabled in the active profile;
- the gateway service is loaded and running;
- gateway logs show Slack and Feishu connected, with two platforms running;
- local Lark/Feishu desktop is running;
- local `screencapture`, `osascript`, and `ffmpeg` are available;
- local `hermes` is not on PATH, so runtime checks should use the remote commands from `docs/local-runtime.md`.

## Capture pipeline

### 1. Preflight

```bash
# local, from repo root
git status --short --ignored=matching docs/local-runtime.md

# remote, commands copied from docs/local-runtime.md
ssh <runtime-alias> '<hermes> --profile <profile> plugins list --plain --no-bundled'
ssh <runtime-alias> '<hermes> --profile <profile> gateway status'
ssh <runtime-alias> 'tail -n 80 <gateway-log>'
```

Need to see:

- `hermes-tag` enabled;
- gateway service loaded/running;
- Feishu connected;
- `Gateway running with 2 platform(s)` or equivalent.

### 2. Prepare safe chart assets

Generate three synthetic chart PNGs locally. No real dashboard screenshots.

### 3. Stage Feishu/Lark

1. Open the safe test group from `docs/local-runtime.md`.
2. Send `/tag admin clear @BOT` if a clean session is needed.
3. Crop the recording region to only the chat pane.
4. Start screen recording.
5. Execute the exact demo script above.
6. Stop recording after the answer is visible.

### 4. Export GIF

```bash
ffmpeg -y -i raw-recording.mov \
  -vf "crop=<w>:<h>:<x>:<y>,fps=12,scale=960:-1:flags=lanczos,palettegen" \
  /tmp/hermes-tag-palette.png

ffmpeg -y -i raw-recording.mov -i /tmp/hermes-tag-palette.png \
  -lavfi "crop=<w>:<h>:<x>:<y>,fps=12,scale=960:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer" \
  docs/demo.zh.gif
```

For the English README, either reuse the real Chinese UI with an English caption below it, or record a second English Slack/Lark pass. Do not subtitle over the bot answer in a way that implies a translated response was live.

## README embed

Chinese README:

```html
<p align="center"><img src="docs/demo.zh.gif" alt="在飞书群里先发三张图、补一段说明，同事插几句，然后 @ 时令 PM——它基于真实 Hermes Tag 回复总结原图、说明和相关讨论，并忽略无关闲聊" width="720"></p>
```

English README:

```html
<p align="center"><img src="docs/demo.zh.gif" alt="Real Lark demo: post charts and notes first, @ Hermes Tag last, then it answers from the original images, your note, and relevant replies instead of the last line or whole history" width="720"></p>
```
