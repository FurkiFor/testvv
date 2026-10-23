# History Group Chat — Shorts pipeline

Builds one vertical YouTube Short (1080×1920, under 60 s) per episode: historical figures text each other on a WhatsApp-style chat, fully voiced, with sound effects, a music bed, and a meme ending card. Channel: **History Group Chat** (Kervly brand `groupchat`). All content is in English, slangy and funny.

## Format v2 (23 Oct)
Decided from the 15–22 Oct data (v1: 23 videos, 44–59 s, avg 72 / median 79 views, 0 comments). These rules override anything above.
1. **Length 18–28 s. Never publish a video over 32 s.** Chat 6–8 messages (date chip excluded). Total spoken words (hook say + chat say + meme say) ≤ 60.
2. **The first message IS the conflict**: a threat, insult or absurd demand. No greetings, no setup. The last message is the punchline and must land on one read.
3. **Fame filter:** an average US high-schooler has heard of them and the joke needs no prior knowledge (Sparta/Leonidas, Diogenes, Cleopatra, Caesar, Napoleon, Alexander, Henry VIII, Marie Antoinette, Archimedes, Newton, Shakespeare, Mozart, Beethoven, Van Gogh, Leonardo, Washington, Lincoln, Socrates, Vikings, Roman legionaries). Niche science/literature gossip (Kepler anagram, Royal Society reports, Cope–Marsh) is banned.
4. **Series logic:** winning characters may return with new anecdotes. A pair+joke in LOG.md is never repeated, but the same character may come back with a different event.
5. **Hook & ending:** each day 1 video **A = hook scene** (`hook.say` ≤ 10 words, 3 lines ≤ 22 chars) and 1 video **B = cold open** (`"hook": {"mode": "none"}`). Ending `none` (meme card) or `cut` (ends on the last message). `block` adds ~5 s: at most once every 3 days. `meme.say` ≤ 8 words.
6. **Comment CTA makes viewers pick a side:** "Sparta or Macedon? Pick one 👇", "Comment the reply YOU would've sent 👇". "Who won?" is banned.
7. **Title** starts with the famous name + the conflict, ≤ 70 chars (ending ` #shorts`), one emoji. E.g. "Xerxes told Sparta to surrender. Leonidas replied in 3 words 💀 #shorts".
8. All other rules still apply: only people who died before 1900; no Hitler/Nazis/dictators/genocide perpetrators/prophets/religious figures; no living or modern politicians; PG-13; the joke rests on a real, well-known event.
Episode JSON carries `"format": "v2-A"` or `"format": "v2-B"`. Performance is tracked in `pipeline/STATS.md`.

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
- `chat`: first a `{"k":"chip","text":"<date>"}`, then 6–8 messages (Format v2). `k` = `out` (you) or `in` (them). `text` = what is shown (slang, lowercase, emoji ok), `say` = what the voice reads (spell slang out: "ur" → "your", "ngl" → "not gonna lie", no emoji, numbers as words if odd). `time` = clock label. Optional: `typing` (seconds of typing dots before an `in` message, 0.6–1.2 for dramatic pauses), `quote` (an `in` reply quoting an earlier `out` line), `sfx` (`boom` vine boom, `scratch` record scratch), `big: true` (a lone emoji reaction, no `say`).
- `ending`: `block` (them's profile opens → video call → Declined → "<them> blocked you" → meme) or `none` (meme card right after the chat). Alternate between them.
- `meme`: `top` (white) / `bottom` (yellow) ALL-CAPS lines, ≤ 24 chars each; 2 `chips` (scoreboard jokes, ≤ 26 chars each); `say` (narrator, ≤ 12 words).
- `narrator`: keep `am_onyx` / 1.2.

Voices (Kokoro): American male `am_puck` (cocky, energetic), `am_fenrir`, `am_michael`, `am_adam`, `am_eric`, `am_liam`, `am_onyx` (deep narrator), `am_echo`; British male `bm_george` (old, deadpan), `bm_lewis`, `bm_daniel`, `bm_fable`; female `af_heart`, `af_bella`, `af_nicole`, `af_sarah`, `bf_emma`, `bf_isabella`. Speeds 1.05–1.25. Give the two characters clearly different voices.

### ElevenLabs voices (preferred)
Every character and the narrator also get an `el_voice` (ElevenLabs voice id); optional `el_speed` (default 1.06, tempo applied to the ElevenLabs take). Keep the Kokoro `voice`/`speed` too: it is the fallback.
Any chat line, hook or meme may add `el_say` — the `say` text with eleven_v4 audio tags such as `[laughs]`, `[sighs]`, `[whispers]`, `[shouting]` (max one or two per line). Captions still use `text`.

Tested voice ids (all English):
- Narrator (hook + meme): `7lJ2JuXZKHyck5zlS7XQ` Romulus — deep, cinematic history narrator.
- Young, cocky / energetic male: `SOYHLrjzK2X1ezoPC6cr` Harry, `unWb9iRIK7Xxf4A5Hfis` VALF, `2UyW0L6yjNuo3ZH3XnoV` Boom Mike (Jersey guy).
- Smug / sly male: `N2lVS1w4EtoT3dr4eOWO` Callum, `qvI9Sgo8A9eFU874jTGo` Sniffleworth.
- Nerdy male (scientists, inventors): `2t3wubVNRseKNVjtlWx1` Quinn.
- Old British male (philosophers, kings): `fGIZlgPQ75MMlvQ6WxgY` Gerald; rough British: `U4Y0Z2HmYcQYMkJB8hrg` Tom (pirates, sailors).
- Deep / grim male (generals, emperors): `dqoktGAat2XIYpd4sTb7` Malakor, `mB6ZkFrKfGXPm8AMkuVl` Shawn.
- Female: `FGY2WhTYpPnrIDTdsKH5` Laura (sassy, young), `uOKjDs6WxcKhmWoVHGF8` Lexi (expressive), `NPC1Rk3VsPo28KCMJFLI` Gee Louise (British), `QnYI2oCbco37NvlkNHTK` Ms Diva (mature, regal).
Use `creative_list_voices` for anything else; never invent an id.

How the ElevenLabs path works (the build script cannot call ElevenLabs itself):
1. `python3 make_episode.py episodes/<slug>.json --lines` writes `build/<slug>/lines.json`: one row per line with `name`, `text`, `voice_id` and the target `file` (`build/<slug>/vo_src/<name>.mp3`).
2. For each row: `creative_generate_speech` with `model_id` `eleven_v4`, that `voice_id`, `prompt` = `text`, **`generations_count: 1`** (never 4 — it multiplies cost), one shared `flow_id` per episode (`creative_create_flow` first). Then `creative_get_flow_run_status` until done and download `media[0].url` to `file` with curl. Never re-run a generation to retry; if one line fails, the whole episode falls back to Kokoro.
3. Run `make_episode.py` normally. It prints `voice engine: elevenlabs` when every line has a file in `vo_src/`, otherwise `voice engine: kokoro`.
Before spending credits, check the download path once: `curl -sS -o /dev/null -w '%{http_code}' https://storage.googleapis.com/eleven-public-prod/premade/voices/N2lVS1w4EtoT3dr4eOWO/ac833bd8-ffda-4938-9ebc-b0f99ca25481.mp3` must print 200. If it does not (the session's network blocks storage.googleapis.com), skip ElevenLabs entirely and use Kokoro.

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

## SEO (vidIQ)
For each episode, before writing the final `youtube` block (≈10 vidIQ credits per episode):
1. `vidiq_keyword_research` mode `research`, keyword = the two characters (e.g. "alexander the great diogenes"). Pick 1–2 high-volume, lower-competition keywords (prefer `overall` ≥ 55) that truly match the episode.
2. `vidiq_generate_titles` with `type: "short"`, `numTitles: 5`, `language: "en"`, `regionCode: "US"`, your working title and a 2-sentence description of the joke. Take the best-scoring title as a base, but keep the channel voice: curiosity hook, one emoji, ends with ` #shorts`, ≤ 90 chars, and it must name at least one character.
3. Caption: first line uses the main keyword naturally; keep the comment-bait question, the "Parody · fictional chat." line, one line of real history; 5–8 hashtags drawn from the vidIQ keywords.
4. Tags: 8–12, the vidIQ keywords that fit first, then `history group chat`, `history memes`, `funny history`, `shorts`.
Skip vidIQ (write SEO yourself) if `vidiq_balance` is below 40 credits or the tools are missing.

## Publishing (Kervly)
1. Copy the mp4 to `videos/groupchat/<slug>.mp4` at the repo root, commit and push to `main`.
2. Wait until `https://raw.githubusercontent.com/FurkiFor/testvv/main/videos/groupchat/<slug>.mp4` returns 200 (can take a few minutes).
3. `schedule_post` brand `groupchat`, platform `youtube`, that URL as `media_url`, the episode's title/caption/tags, options `{"youtube":{"privacy":"public","category":"ENTERTAINMENT","madeForKids":false,"notifySubscribers":true,"language":"en","audioLanguage":"en"}}`.
4. Add a line to `episodes/LOG.md`.
