# Channel stats — History Group Chat

Source: vidIQ `vidiq_get_videos_by_ids` (public counts); from 2026-10-27 Kervly `get_youtube_stats` (same public counts, 0 credits) while the Kervly token works. Updated every run. Dates = publish date (Dubai).

## Summary (snapshot 2026-11-04 ~08:50 Dubai, Kervly get_youtube_stats — token OK)

| Group | n | avg views | median views | avg likes | comments | 48h-matured n | median (48h-matured) |
|---|---|---|---|---|---|---|---|
| v1 (44–59 s) | 23 | 76 | 81 | 0.5 | 1 | 23 | 81 |
| v2 (all, published) | 22 | 254 | 146 | 1.7 | 1 | 16 | 168 |
| v2-A (hook) | 7 | 160 | 113 | 0.1 | 0 | 7 | 113 |
| v2-B (cold open) | 15 | 298 | 164 | 2.4 | 1 | 9 | 343 |

Decision rule: once ≥ 6 v2 videos have 48 h of data, compare A vs B; if one reaches 2× the other's median views, use it for both slots. If the v2 median does not beat the v1 median (79), cut to 12–18 s and 4–6 messages.

Decisions:
- 2026-11-04: token OK (0 error posts). lincoln-wrestling finally published (99 @8 h). Kokoro-only pair from 3 Nov: napoleon-elba-escape 88 @16 h, caesar-calendar 48 @12 h vs ElevenLabs pair 2 Nov at the same age (newton 161 @16 h, roman 88 @12 h) → Kokoro looks ~45% weaker early, but n=2 and topic-confounded. Matured numbers unchanged (B/A 343 / 113 = 3.0×, v2 168 vs v1 81) → cold open in both slots + 18–28 s stay. Warning: the 6 newest B (not yet matured) have median 99 views — the short test (washington-whiskey, 6 Nov 01:00) is the next lever. ElevenLabs CDN still blocked → Kokoro again. Today: alexander-gordian-knot (B, 17:00) and marie-antoinette-warship-hair (B, 21:00), both "famous name + surprising true fact" titles.
- 2026-11-03: Kervly YouTube token works again (connection OK, stats readable; 0 error posts). The 2 Nov batch published: newton-south-sea 161 @16 h, roman-pee-laundry 88 @12 h, napoleon-vs-pug 321 @8 h (fastest start since washington-teeth → Napoleon is the strongest recurring character: 710 / 343 / 321). Matured numbers unchanged (B/A 343 / 113 = 3.0×, v2 168 vs v1 81) → cold open in both slots + 18–28 s stay. Today: napoleon-elba-escape (B, 17:00, 19.9 s) and caesar-calendar (B, 21:00, 21.2 s). ElevenLabs generation worked but its CDN (elevenlabsusercontent.com) is blocked by this session's proxy → both built with Kokoro (first Kokoro-only day since 15 Oct; compare voice quality impact).
- 2026-11-02: all 16 published v2 matured (7 A / 9 B). **B/A median = 343 / 113 = 3.0× → cold open in both slots stays.** v2 median 168 vs v1 81 (2.1×) → 18–28 s stays. Nothing new published since 30 Oct: Kervly YouTube token expired again (invalid_grant), so 1 Nov (henry-groom-of-stool, washington-whiskey) and 2 Nov 01:00 (lincoln-wrestling) failed → moved to 01:00 slots 4–6 Nov. Short-format test (washington-whiskey) still unmeasured. Today: newton-south-sea (B, 17:00, 26.3 s) and roman-pee-laundry (B, 21:00, 23.1 s), both "famous name + surprising true fact" titles.
- 2026-11-01: 14 v2 matured (7 A / 7 B). **B/A matured median = 466 / 113 = 4.1× → cold open in both slots stays.** v2 matured median 230 vs v1 81 (2.8×) → 18–28 s stays as default. BUT the trigger from 31 Oct fired: the last 4 published v2 (29–30 Oct) have median 94 views (franklin 466, cleopatra-iphone 128, leonardo 52, poe 60) < 150. **Test today: 21:00 slot gets a SHORT cold open (12–18 s, 4–6 messages): washington-whiskey (17.6 s, 5 msgs, `"variant"` field in JSON).** 17:00 keeps the standard B: henry-groom-of-stool (23.7 s). Compare short vs standard once both have 48 h. Note: Oct 31 videos (lincoln-wrestling, napoleon-vs-pug) never published — Kervly YouTube token expired again (invalid_grant); rescheduled to 01:00 slots.
- 2026-10-31: 12 v2 matured (6 A / 6 B). **B/A matured median = 445.5 / 140.5 = 3.17× → cold-open-in-both-slots decision CONFIRMED, kept.** v2 matured median 229.5 vs v1 81 (2.8×) → 18–28 s stays. Warning: the last 5 videos are weak (revere 78, viking 46, leonardo 50, cleopatra-iphone 111 @16 h, poe 42 @12 h); only franklin-vs-eagle (464) hit. Hits share one pattern: top-tier name + a surprising true fact in the title (washington 1107, napoleon-short 709, henry 549, franklin 464). Today both picks follow it: lincoln-wrestling (B, 17:00) and napoleon-vs-pug (B, 21:00, Napoleon = best-performing character). If the next 2 days stay < 150 median, try 12–18 s / 4–6 messages on one slot.
- 2026-10-30: 10 v2 matured. **B/A matured median = 549 / 168 = 3.27× → 2× rule MET. DECISION: cold open (v2-B, `"hook": {"mode": "none"}`) in BOTH daily slots from today.** Confirmation from the latest pair: franklin-vs-eagle (B) 456 views in 12 h vs leonardo-mona-lisa (A) 44 in 16 h. v2 matured median 316.5 vs v1 81 (3.9×) → 18–28 s stays. Slots stay 17:00 / 21:00 Dubai. Today: cleopatra-iphone (B, 17:00), poe-vs-raven (B, 21:00, Halloween tie-in). Myth-bust / surprising-fact angle with a top-tier name keeps leading.
- 2026-10-29: 8 v2 matured. **B/A matured median = 446 / 229 = 1.95× → 2× rule still NOT met.** v2 matured median 317 vs v1 81 (3.9×) → 18–28 s stays. Slot-swap test (28 Oct) inconclusive and both weak: revere-vs-dawes (B, 17:00) 57 views at 16 h, viking-horns (A, 21:00) 40 at 12 h — roughly the same views/hour, so the slot alone does not explain B's lead. Back to default today: A (leonardo-mona-lisa) 17:00, B (franklin-vs-eagle) 21:00. Content signal holds: "famous name + surprising myth-bust" (washington 1106, napoleon-short 698, henry 549) beats everything; 28 Oct topics (Revere, Vikings) were weaker. If B/A ≥ 2× on the next snapshot, switch both slots to cold open.
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
| alexander-vs-diogenes | v1 | 58 | 2026-10-15 | 82 | 3 | 0 |
| antony-vs-cleopatra | v1 | 49 | 2026-10-15 | 153 | 3 | 0 |
| newton-vs-leibniz | v1 | 59 | 2026-10-15 | 2 | 0 | 0 |
| darwin-vs-fitzroy | v1 | 54 | 2026-10-16 | 16 | 0 | 0 |
| archimedes-vs-hiero | v1 | 59 | 2026-10-15 | 125 | 1 | 0 |
| franklin-vs-adams | v1 | 59 | 2026-10-15 | 7 | 0 | 0 |
| dickens-vs-andersen | v1 | 59 | 2026-10-16 | 4 | 1 | 0 |
| group-halloween-party | v1 | 44 | 2026-10-15 | 5 | 1 | 0 |
| socrates-vs-xanthippe | v1 | 59 | 2026-10-16 | 98 | 0 | 0 |
| leonardo-vs-michelangelo | v1 | 59 | 2026-10-16 | 55 | 0 | 0 |
| beethoven-vs-goethe | v1 | 59 | 2026-10-17 | 81 | 0 | 0 |
| caesar-vs-cleopatra | v1 | 59 | 2026-10-17 | 159 | 0 | 1 |
| kepler-vs-galileo | v1 | 59 | 2026-10-17 | 5 | 1 | 0 |
| lovelace-vs-babbage | v1 | 59 | 2026-10-18 | 72 | 0 | 0 |
| hannibal-vs-scipio | v1 | 59 | 2026-10-19 | 54 | 0 | 0 |
| shakespeare-vs-anne | v1 | 52 | 2026-10-19 | 98 | 0 | 0 |
| cope-vs-marsh | v1 | 57 | 2026-10-20 | 96 | 0 | 0 |
| plato-vs-diogenes | v1 | 59 | 2026-10-20 | 103 | 0 | 0 |
| rousseau-vs-marie-antoinette | v1 | 59 | 2026-10-20 | 119 | 0 | 0 |
| byron-vs-mary-shelley | v1 | 59 | 2026-10-21 | 68 | 0 | 0 |
| philip-vs-sparta | v1 | 59 | 2026-10-21 | 220 | 1 | 0 |
| halley-vs-newton | v1 | 59 | 2026-10-21 | 83 | 0 | 0 |
| darwin-vs-emma | v1 | 59 | 2026-10-22 | 37 | 0 | 0 |
| caesar-vs-pirates | v2-A | 28.7 | 2026-10-24 17:00 | 168 (232 h) | 0 | 0 |
| henry-viii-catfish-v2 | v2-B | 24.3 | 2026-10-24 21:00 | 550 (228 h) | 1 | 0 |
| xerxes-vs-leonidas | v2-A | 27.4 | 2026-10-25 01:00 | 292 (224 h) | 1 | 0 |
| spartan-mom | v2-A | 25.6 | 2026-10-25 17:00 | 383 (208 h) | 0 | 0 |
| washington-teeth | v2-B | 20.3 | 2026-10-25 21:00 | 1108 (204 h) | 9 | 0 |
| napoleon-vs-rabbits | v2-B | 22.7 | 2026-10-26 01:00 | 343 (200 h) | 2 | 0 |
| vangogh-sunflowers | v2-A | 28.3 | 2026-10-26 17:00 | 113 (184 h) | 0 | 0 |
| alexander-city-names | v2-B | 24.7 | 2026-10-26 21:00 | 168 (180 h) | 3 | 0 |
| diogenes-lamp | v2-A | 29.6 | 2026-10-27 17:00 | 63 (160 h) | 0 | 0 |
| napoleon-short | v2-B | 26.2 | 2026-10-27 21:00 | 709 (156 h) | 10 | 1 |
| revere-vs-dawes | v2-B | 26.1 | 2026-10-28 17:00 | 81 (136 h) | 0 | 0 |
| viking-horns | v2-A | 28.3 | 2026-10-28 21:00 | 46 (132 h) | 0 | 0 |
| leonardo-mona-lisa | v2-A | 29.2 | 2026-10-29 17:00 | 52 (112 h) | 0 | 0 |
| franklin-vs-eagle | v2-B | 26.9 | 2026-10-29 21:00 | 466 (108 h) | 1 | 0 |
| cleopatra-iphone | v2-B | 25.3 | 2026-10-30 17:00 | 128 (88 h) | 2 | 0 |
| poe-vs-raven | v2-B | 24.3 | 2026-10-30 21:00 | 64 (84 h) | 0 | 0 |
| lincoln-wrestling | v2-B | 26.2 | 2026-11-04 01:00 | 99 (8 h) | 1 | 0 |
| napoleon-vs-pug | v2-B | 23.7 | 2026-11-03 01:00 | 356 (32 h) | 3 | 0 |
| henry-groom-of-stool | v2-B | 23.7 | not published (token) → 2026-11-05 01:00 | – | – | – |
| washington-whiskey | v2-B short | 17.6 | not published (token) → 2026-11-06 01:00 | – | – | – |
| newton-south-sea | v2-B | 26.3 | 2026-11-02 17:00 | 164 (40 h) | 2 | 0 |
| roman-pee-laundry | v2-B | 23.1 | 2026-11-02 21:00 | 98 (36 h) | 0 | 0 |
| napoleon-elba-escape | v2-B (kokoro) | 19.9 | 2026-11-03 17:00 | 88 (16 h) | 1 | 0 |
| caesar-calendar | v2-B (kokoro) | 21.2 | 2026-11-03 21:00 | 48 (12 h) | 1 | 0 |
| alexander-gordian-knot | v2-B (kokoro) | – | 2026-11-04 17:00 (sched.) | – | – | – |
| marie-antoinette-warship-hair | v2-B (kokoro) | – | 2026-11-04 21:00 (sched.) | – | – | – |
