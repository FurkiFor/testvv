# History Group Chat — Shorts pipeline

Builds one vertical YouTube Short (1080×1920, under 60 s) per episode: historical figures text each other on a WhatsApp-style chat, fully voiced, with sound effects, a music bed, and a meme ending card. Channel: **History Group Chat** (Kervly brand `groupchat`). All content is in English, slangy and funny.

## Run

```bash
bash pipeline/setup.sh                                  # once per fresh session (~1 min)
python3 pipeline/make_episode.py pipeline/episodes/<slug>.json   # ~4–5 min per episode
```

Output: `pipeline/out/<slug>.mp4` and `pipeline/out/<slug>_sheet.png` (6 check frames — always look at it).
If an episode is too long the script speeds the voices up automatically; if it still fails, cut chat lines.

## Writing an episode

Copy `episodes/alexander-vs-diogenes.json` and change everything. Fields:

- `slug`: kebab-case, unique (check `episodes/LOG.md`).
- `youtube`: `title` (≤ 90 chars, ends with ` #shorts`, curiosity hook + one emoji), `caption` (3–6 short lines, a question to drive comments, the line "Parody · fictional chat." plus one line of the real history behind it, 5–8 hashtags), `tags` (8–10).
- `theme`: `hookBg` (dark color), `glow` and `footerColor` (accent), `footer` (`"<emoji> <YEAR> · <PLACE>"`), `stamp` (one word slammed over the photos: REJECTED, DENIED, EXPOSED, COOKED, BLOCKED…).
- `hook`: 3 short ALL-CAPS `lines` (each ≤ 22 chars so it fits one line), `punch` (yellow label, ≤ 18 chars + emoji), `say` (narrator reads the hook, ≤ 20 words).
- `you`: the character who types (green bubbles, keyboard). `them`: the contact (white bubbles, typing dots, profile, call). Each: `name`, `label` (ALL CAPS name under the photo), `portrait` (file in `portraits/`), `face` (viewBox crop of the head for round avatars, e.g. `"44 50 112 112"`), `voice`, `speed`. `them` also: `status` (funny "last seen…" line), `subtitle`, `about`, `aboutDate`.
- `notifications`: exactly 2 short lines from `them` (shown in the hook).
- `chat`: first a `{"k":"chip","text":"<date>"}`, then 12–16 messages. `k` = `out` (you) or `in` (them). `text` = what is shown (slang, lowercase, emoji ok), `say` = what the voice reads (spell slang out: "ur" → "your", "ngl" → "not gonna lie", no emoji, numbers as words if odd). `time` = clock label. Optional: `typing` (seconds of typing dots before an `in` message, 0.6–1.2 for dramatic pauses), `quote` (an `in` reply quoting an earlier `out` line), `sfx` (`boom` vine boom, `scratch` record scratch), `big: true` (a lone emoji reaction, no `say`).
- `ending`: `block` (them's profile opens → video call → Declined → "<them> blocked you" → meme) or `none` (meme card right after the chat). Alternate between them.
- `meme`: `top` (white) / `bottom` (yellow) ALL-CAPS lines, ≤ 24 chars each; 2 `chips` (scoreboard jokes, ≤ 26 chars each); `say` (narrator, ≤ 12 words).
- `narrator`: keep `am_onyx` / 1.2.

Voices (Kokoro): American male `am_puck` (cocky, energetic), `am_fenrir`, `am_michael`, `am_adam`, `am_eric`, `am_liam`, `am_onyx` (deep narrator), `am_echo`; British male `bm_george` (old, deadpan), `bm_lewis`, `bm_daniel`, `bm_fable`; female `af_heart`, `af_bella`, `af_nicole`, `af_sarah`, `bf_emma`, `bf_isabella`. Speeds 1.05–1.25. Give the two characters clearly different voices.

### Comedy rules
- Every episode is built on a real, well-known historical fact or anecdote, and the joke twists it (the "history" must be recognizable).
- Gen-Z group-chat voice: "bro", "fr", "ngl", "lowkey", "it's giving", "mid", "cooked", "ratio", "no cap", "bet", "💀". One escalation, a reversal, and a last-line punchline. The 3rd–5th second must already be funny.
- PG-13: no f-word, no slurs, nothing sexual, no graphic violence or gore, no suicide/self-harm jokes.

### Who can be in it (hard rules)
- Only people who died before 1900 (the further back the better). No living people, no 20th-century figures, no politicians of any era after 1900.
- Never: Hitler, Nazis, fascists, Stalin, Mao, or any genocide/atrocity perpetrator as a joke protagonist; no religious prophets, saints, or deities (Muhammad, Jesus, Moses, Buddha, etc.); no slavery, colonial massacre or ethnic stereotypes as the joke.
- Keep it light: rivalries, failed inventions, famous quotes, bad decisions, petty beef.
- Never reuse a pair or core joke that is in `episodes/LOG.md`.

### Portraits
Each character needs an SVG in `portraits/<name>.svg` (reuse an existing one if the character already has one):
- `viewBox="0 0 200 250"`, no width/height, flat cartoon style like `alexander.svg` and `diogenes.svg`: colored background, shoulders/clothes at the bottom, head around x 100, y 110.
- One iconic, instantly recognizable attribute (bicorne hat, laurel wreath, lightbulb, apple, toga, crown, quill, ruff collar…) plus a funny expression.
- No text, no photos, no external images. Prefix any gradient/def ids with the character name (e.g. `id="newton-bg"`).
- Set `face` so the round crop shows the whole head.

## Publishing (Kervly)
1. Copy the mp4 to `videos/groupchat/<slug>.mp4` at the repo root, commit and push to `main`.
2. Wait until `https://raw.githubusercontent.com/FurkiFor/testvv/main/videos/groupchat/<slug>.mp4` returns 200 (can take a few minutes).
3. `schedule_post` brand `groupchat`, platform `youtube`, that URL as `media_url`, the episode's title/caption/tags, options `{"youtube":{"privacy":"public","category":"ENTERTAINMENT","madeForKids":false,"notifySubscribers":true,"language":"en","audioLanguage":"en"}}`.
4. Add a line to `episodes/LOG.md`.
