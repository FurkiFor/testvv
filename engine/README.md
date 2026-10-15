# asmrvideo engine

Generates seamless, endlessly "shrinking" 3D ASMR loop Shorts (1080×1920, no on-screen
text, synthesized sound) for the Kervly brand `asmrvideo`, and stores them in
`videos/asmrvideo/` of this repo, which is the brand's media storage.

## How a loop stays seamless

Each scene is an infinite chain of copies, copy n+1 = M(copy n), where M is a uniform
scale `r` plus a rotation `phi` about the vertical axis through a fixed point on the
floor. Copy n is drawn with M^(n−T) and local time τ = T − n, so the frame at T+1 is
identical to the frame at T. A video is a whole number of cycles, and per-copy colours
repeat with a period that divides that number. The soundtrack is built on a circular
buffer of the exact video length (events wrap around, beds and reverb are circular).

## Scene families (`page/scenes/`)

| family | what happens |
|---|---|
| `cubecut` | knife cuts a cube (kinetic sand, soap, clay, chocolate, marble) into 8; the back corner piece is the next cube in a new colour |
| `nestshell` | hollow sphere cracks, halves roll into rocking bowls, smaller sphere inside |
| `dominospiral` | dominoes topple along a log spiral, each smaller than the last |
| `funnelmarbles` | marbles roll down a spiral track into a funnel, shrinking forever |

Each run picks materials, palettes, timing and camera variation from a seed, so every
video is different. To add a family, add a module that returns the same shape
(`M`, `makeCopy`, `cycles`, `cycleSec`, `events`, `meta`, camera) and append it to
`FAMILIES` in `daily.mjs`.

## Commands

```bash
bash engine/run-daily.sh --date 2026-10-16 --count 3   # renders 3 videos, ~5 min each
node engine/render.mjs --family cubecut --seed 7 --preview /tmp/prev --at 0,0.5,1
node engine/render.mjs --family nestshell --seed 3 --out /tmp/test.mp4
```

`daily.mjs` rotates families by date, avoids titles used in the last 14 days, and
writes `engine/runs/<date>.json` with each video's file, public URL, title, caption
and tags. Re-running skips videos that already exist.

## Daily publishing procedure (what the scheduled task does)

1. Attach `FurkiFor/testvv` with push access, then clone without old videos:
   `git clone --depth 1 --filter=blob:none --sparse https://github.com/FurkiFor/testvv /home/claude/testvv`
   and `git -C /home/claude/testvv sparse-checkout set engine`.
2. Run `run-daily.sh` in the background for today's Dubai date with `--count 3`
   and poll the log until it prints `DONE`.
3. `git add --sparse videos/asmrvideo/<date>-* engine/runs/<date>.json`, commit, push to `main`.
4. Wait until each `url` in the manifest answers HTTP 200 with a Content-Length.
5. Kervly: `get_calendar` for `asmrvideo`, then `schedule_post` each video to
   `youtube` at 12:00, 17:00 and 21:00 Asia/Dubai (skip taken or past slots, max 3 a day),
   with the manifest title, caption and tags and options
   `{youtube:{privacy:"public", category:"ENTERTAINMENT", madeForKids:false, notifySubscribers:true, language:"en", audioLanguage:"en", aiGenerated:false}}`.

Uploading through Kervly's own upload link is blocked from the cloud sandbox, so
videos reach storage by git push; the raw.githubusercontent.com URL is the brand's
allowlisted media prefix.
