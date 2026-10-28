# Channel stats — History Group Chat

Source: vidIQ `vidiq_get_videos_by_ids` (public counts); from 2026-10-27 Kervly `get_youtube_stats` (same public counts, 0 credits) while the Kervly token works. Updated every run. Dates = publish date (Dubai).

## Summary (snapshot 2026-10-28 ~08:50 Dubai)

| Group | n | avg views | median views | avg likes | comments | 48h-matured n | median (48h-matured) |
|---|---|---|---|---|---|---|---|
| v1 (44–59 s) | 23 | 75 | 81 | 0.4 | 0 | 23 | 81 |
| v2 (all, published) | 10 | 382 | 316 | 2.6 | 1 | 6 | 360 |
| v2-A (hook, 17:00 slot) | 5 | 199 | 168 | 0.2 | 0 | 3 | 291 |
| v2-B (cold open, 21:00 slot) | 5 | 565 | 554 | 5.0 | 1 | 3 | 554 |

Decision rule: once ≥ 6 v2 videos have 48 h of data, compare A vs B; if one reaches 2× the other's median views, use it for both slots. If the v2 median does not beat the v1 median (79), cut to 12–18 s and 4–6 messages.

Decisions:
- 2026-10-28: **6 v2 videos matured. B/A matured median = 554 / 291 = 1.90× → 2× rule NOT met (just under).** v2 median 360 vs v1 81 (4.4×) → 18–28 s format stays. B won all 4 same-day pairs (554 vs 168, 1101 vs 380, 158 vs 99, 671 vs 57 at ~12 h), but format is confounded with slot (A always 17:00 Dubai = 9 AM ET, B always 21:00 = 1 PM ET). **Test today: slots swapped — B (revere-vs-dawes) at 17:00, A (viking-horns) at 21:00.** If B beats A again from the 17:00 slot (or B/A matured median ≥ 2×), switch both slots to cold open. If A wins at 21:00, the slot was the driver: keep A/B and move both posts later (19:00 / 22:00).
- Content signal: myth-busting titles with a famous name are the top 3 (washington-teeth 1101 "weren't wood", napoleon-short 671 "wasn't short", henry-viii-catfish-v2 554). Diogenes (57, 101) and Van Gogh (99) underperform. Today's picks follow the myth-bust angle (Vikings never wore horns; Revere never yelled "the British are coming").
- First comment on the channel: napoleon-short (B, Team-X-or-Team-Y CTA).
- Pipeline fix 2026-10-28: `ending: "cut"` skipped the hook scene in the template (hook audio played over an empty chat). Fixed in template.html; diogenes-lamp (A + none) was not affected, earlier A episodes used none/block.

History:
- 2026-10-24: first two v2 videos never published (Kervly token expired); rescheduled to 01:00 slots.
- 2026-10-25: token OK again. Early v2 read: every v2 video beats every v1 lifetime except philip-vs-sparta. Keep 18–28 s.
- 2026-10-26: v2 median 342 vs v1 80 (4.3×). B leads A: median 531 vs 288 (1.84×, none matured). washington-teeth = channel record.
- 2026-10-27: v2 median 313 vs v1 80 (3.9×). B leads A: median 443 vs 229 (1.93×, 3 matured). Day-3 batch weaker — fame filter matters more than format.

Note: 48h-view counts are not tracked per video (snapshot only); v1 numbers are lifetime views at snapshot time. Ages for v2 rows are hours since publish at snapshot.

## Per video

| slug | format | sec | published | views | likes | comments |
|---|---|---|---|---|---|---|
| alexander-vs-diogenes | v1 | 58 | 2026-10-15 | 81 | 3 | 0 |
| antony-vs-cleopatra | v1 | 49 | 2026-10-15 | 151 | 3 | 0 |
| newton-vs-leibniz | v1 | 59 | 2026-10-15 | 2 | 0 | 0 |
| darwin-vs-fitzroy | v1 | 54 | 2026-10-16 | 16 | 0 | 0 |
| archimedes-vs-hiero | v1 | 59 | 2026-10-15 | 125 | 1 | 0 |
| franklin-vs-adams | v1 | 59 | 2026-10-15 | 5 | 0 | 0 |
| dickens-vs-andersen | v1 | 59 | 2026-10-16 | 4 | 1 | 0 |
| group-halloween-party | v1 | 44 | 2026-10-15 | 4 | 1 | 0 |
| socrates-vs-xanthippe | v1 | 59 | 2026-10-16 | 98 | 0 | 0 |
| leonardo-vs-michelangelo | v1 | 59 | 2026-10-16 | 55 | 0 | 0 |
| beethoven-vs-goethe | v1 | 59 | 2026-10-17 | 81 | 0 | 0 |
| caesar-vs-cleopatra | v1 | 59 | 2026-10-17 | 156 | 0 | 0 |
| kepler-vs-galileo | v1 | 59 | 2026-10-17 | 5 | 1 | 0 |
| lovelace-vs-babbage | v1 | 59 | 2026-10-18 | 72 | 0 | 0 |
| hannibal-vs-scipio | v1 | 59 | 2026-10-19 | 53 | 0 | 0 |
| shakespeare-vs-anne | v1 | 52 | 2026-10-19 | 97 | 0 | 0 |
| cope-vs-marsh | v1 | 57 | 2026-10-20 | 96 | 0 | 0 |
| plato-vs-diogenes | v1 | 59 | 2026-10-20 | 101 | 0 | 0 |
| rousseau-vs-marie-antoinette | v1 | 59 | 2026-10-20 | 119 | 0 | 0 |
| byron-vs-mary-shelley | v1 | 59 | 2026-10-21 | 67 | 0 | 0 |
| philip-vs-sparta | v1 | 59 | 2026-10-21 | 217 | 0 | 0 |
| halley-vs-newton | v1 | 59 | 2026-10-21 | 83 | 0 | 0 |
| darwin-vs-emma | v1 | 59 | 2026-10-22 | 37 | 0 | 0 |
| caesar-vs-pirates | v2-A | 28.7 | 2026-10-24 17:00 | 168 (88 h) | 0 | 0 |
| henry-viii-catfish-v2 | v2-B | 24.3 | 2026-10-24 21:00 | 554 (84 h) | 1 | 0 |
| xerxes-vs-leonidas | v2-A | 27.4 | 2026-10-25 01:00 | 291 (80 h) | 1 | 0 |
| spartan-mom | v2-A | 25.6 | 2026-10-25 17:00 | 380 (64 h) | 0 | 0 |
| washington-teeth | v2-B | 20.3 | 2026-10-25 21:00 | 1101 (60 h) | 9 | 0 |
| napoleon-vs-rabbits | v2-B | 22.7 | 2026-10-26 01:00 | 340 (56 h) | 2 | 0 |
| vangogh-sunflowers | v2-A | 28.3 | 2026-10-26 17:00 | 99 (40 h) | 0 | 0 |
| alexander-city-names | v2-B | 24.7 | 2026-10-26 21:00 | 158 (36 h) | 3 | 0 |
| diogenes-lamp | v2-A | 29.6 | 2026-10-27 17:00 | 57 (16 h) | 0 | 0 |
| napoleon-short | v2-B | 26.2 | 2026-10-27 21:00 | 671 (12 h) | 10 | 1 |
| revere-vs-dawes | v2-B | 26.1 | 2026-10-28 17:00 (sched.) | – | – | – |
| viking-horns | v2-A | 28.3 | 2026-10-28 21:00 (sched.) | – | – | – |
