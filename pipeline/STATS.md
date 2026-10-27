# Channel stats — History Group Chat

Source: vidIQ `vidiq_get_videos_by_ids` (public counts); from 2026-10-27 Kervly `get_youtube_stats` (same public counts, 0 credits) while the Kervly token works. Updated every run. Dates = publish date (Dubai).

## Summary (snapshot 2026-10-27 ~08:50 Dubai)

| Group | n | avg views | median views | avg likes | comments | 48h-matured n | median (48h-matured) |
|---|---|---|---|---|---|---|---|
| v1 (44–59 s) | 23 | 75 | 80 | 0.4 | 0 | 23 | 80 |
| v2 (all, published) | 8 | 357 | 313 | 1.6 | 0 | 3 | 290 |
| v2-A (hook) | 4 | 225 | 229 | 0.2 | 0 | 2 | 229 |
| v2-B (cold open) | 4 | 489 | 443 | 3.0 | 0 | 1 | 550 |

Decision rule: once ≥ 6 v2 videos have 48 h of data, compare A vs B; if one reaches 2× the other's median views, use it for both slots. If the v2 median does not beat the v1 median (79), cut to 12–18 s and 4–6 messages.

Decisions: none yet (3 of 8 v2 videos matured to 48 h as of 2026-10-27; 6 by the 2026-10-28 run).
- 2026-10-24: first two v2 videos never published (Kervly token expired); rescheduled to 01:00 slots.
- 2026-10-25: token OK again. Early v2 read: every v2 video beats every v1 lifetime except philip-vs-sparta. Keep 18–28 s.
- 2026-10-26: v2 median 342 vs v1 80 (4.3×) — short format confirmed. B (cold open) leads A: median 531 vs 288 (1.84×, not yet 2×, none matured). washington-teeth (B, 20 s) = channel record 917 views in ~16 h (VPH 83). Watch: if B ≥ 2× A once 6 videos mature, switch both slots to cold open.
- 2026-10-27: v2 median 313 vs v1 80 (3.9×). B leads A: median 443 vs 229 (1.93×, still < 2×; only 3 videos matured to 48 h, decision rule needs 6). Day-3 batch was weaker (vangogh A 73 in 16 h, alexander B 143 in 12 h) — fame filter matters more than format. Keep A/B split one more day; decision at the 2026-10-28 run (spartan-mom, washington-teeth, napoleon-vs-rabbits pass 48 h today → 6 matured).

Note: 48h-view counts are not tracked per video (snapshot only); v1 numbers are lifetime views at snapshot time. Ages for v2 rows are hours since publish at snapshot.

## Per video

| slug | format | sec | published | views | likes | comments |
|---|---|---|---|---|---|---|
| alexander-vs-diogenes | v1 | 58 | 2026-10-15 | 80 | 3 | 0 |
| antony-vs-cleopatra | v1 | 49 | 2026-10-15 | 150 | 3 | 0 |
| newton-vs-leibniz | v1 | 59 | 2026-10-15 | 2 | 0 | 0 |
| darwin-vs-fitzroy | v1 | 54 | 2026-10-16 | 16 | 0 | 0 |
| archimedes-vs-hiero | v1 | 59 | 2026-10-15 | 125 | 1 | 0 |
| franklin-vs-adams | v1 | 59 | 2026-10-15 | 5 | 0 | 0 |
| dickens-vs-andersen | v1 | 59 | 2026-10-16 | 2 | 1 | 0 |
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
| philip-vs-sparta | v1 | 59 | 2026-10-21 | 216 | 0 | 0 |
| halley-vs-newton | v1 | 59 | 2026-10-21 | 83 | 0 | 0 |
| darwin-vs-emma | v1 | 59 | 2026-10-22 | 37 | 0 | 0 |
| caesar-vs-pirates | v2-A | 28.7 | 2026-10-24 17:00 | 168 (64 h) | 0 | 0 |
| henry-viii-catfish-v2 | v2-B | 24.3 | 2026-10-24 21:00 | 550 (60 h) | 1 | 0 |
| xerxes-vs-leonidas | v2-A | 27.4 | 2026-10-25 01:00 | 290 (56 h) | 1 | 0 |
| spartan-mom | v2-A | 25.6 | 2026-10-25 17:00 | 370 (40 h) | 0 | 0 |
| washington-teeth | v2-B | 20.3 | 2026-10-25 21:00 | 928 (36 h) | 6 | 0 |
| napoleon-vs-rabbits | v2-B | 22.7 | 2026-10-26 01:00 | 336 (32 h) | 2 | 0 |
| vangogh-sunflowers | v2-A | 28.3 | 2026-10-26 17:00 | 73 (16 h) | 0 | 0 |
| alexander-city-names | v2-B | 24.7 | 2026-10-26 21:00 | 143 (12 h) | 3 | 0 |
| diogenes-lamp | v2-A | 29.6 | 2026-10-27 17:00 (sched.) | – | – | – |
| napoleon-short | v2-B | 26.2 | 2026-10-27 21:00 (sched.) | – | – | – |
