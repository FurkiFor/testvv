# Channel stats — History Group Chat

Source: vidIQ `vidiq_get_videos_by_ids` (public counts); from 2026-10-27 Kervly `get_youtube_stats` (same public counts, 0 credits) while the Kervly token works. Updated every run. Dates = publish date (Dubai).

## Summary (snapshot 2026-11-21 ~08:50 Dubai, Kervly get_youtube_stats)

| Group | n | avg views | median views | avg likes | comments | 48h-matured n | median (48h-matured) |
|---|---|---|---|---|---|---|---|
| v1 (44–59 s) | 23 | 76 | 82 | 0.5 | 1 | 23 | 82 |
| v2 (all, published) | 42 | 253 | 140.5 | 1.3 | 5 | 42 | 140.5 |
| v2-A (hook) | 7 | 161 | 114 | 0.1 | 0 | 7 | 114 |
| v2-B (cold open) | 35 | 271 | 144 | 1.5 | 5 | 35 | 144 |
| v2-B Kokoro | 20 | 232 | 124.5 | 1.1 | 4 | 20 | 124.5 |
| v2-B ElevenLabs | 15 | 323 | 200 | 2.2 | 1 | 15 | 200 |
| v3-R (relatable) | 8 | 286 | 135.5 | 2.8 | 0 | 5 | 178 |
| v3-D (dark) | 7 | 107 | 59 | 0.7 | 0 | 4 | 53.5 |

(v1 counts unchanged from the last snapshot; vidIQ's recent-uploads list stops at 20 Oct.)

v3 rule (12 Nov): once v3-R and v3-D each have ≥ 6 videos past 48 h, the style whose matured median is ≥ 1.5× the other's takes both slots. Benchmark to beat: v2-B matured median (167 on 12 Nov; 140 today with more matured videos).

Decision rule: once ≥ 6 v2 videos have 48 h of data, compare A vs B; if one reaches 2× the other's median views, use it for both slots. If the v2 median does not beat the v1 median (79), cut to 12–18 s and 4–6 messages.

Decisions:
- 2026-11-21: token OK (0 error posts). Matured: v3-R 178 (n=5), v3-D 53.5 (n=4), v2-B 144 (n=35) → rule needs ≥ 6 matured each → no style decision, keep 1 R + 1 D. **Dark is turning: the "gross/shocking daily life" angle works** — mummy-medicine (D) 268 @11 h (best D ever, beats every R since 13 Nov at that age), henry-anne-little-neck (D) 171 @7 h, socrates-rooster recovered to 162 @59 h; the "death scene" Ds stay weak (green-wallpaper 10, guillotin-name 34, caesar-23-stabs 59). v3-R matured 178 still beats the v2-B benchmark (144); newton-lockdown-bread (R) only 95 @15 h. Today's D follows the winning angle (food + shocking death: king-14-desserts), R goes back to Napoleon (channel #1 character): napoleon-left-on-read. ElevenLabs: test line failed again ("subscription has a failed or incomplete payment", 27 credits shown on the failed take) → Kokoro; storage.googleapis.com 200, elevenlabsusercontent.com 403 at root (reachable), upload.wikimedia.org 000 (blocked). vidIQ: 10 credits (2× keyword research), balance 1835 → 1825.
- 2026-11-20: token OK (0 error posts). Matured: v3-R 234.5 (n=4), v3-D 29 (n=2), v2-B 144 (n=35) → rule needs ≥ 6 matured each → no style decision, keep 1 R + 1 D. **v3-D still failing: all 5 published dark videos < 100 views** (best socrates-rooster 87 @35 h; guillotin-name 15 @11 h), while v3-R matured median (234.5) beats the v2-B benchmark (144). Yesterday: lincoln-hat-late-reply (R) 122 @15 h, guillotin-name (D) 15 @11 h. Today's D switches from "death scene" to "gross daily life" (topic-bank angle that hits 1M+ in the niche): mummy medicine. ElevenLabs: test line failed again ("subscription has a failed or incomplete payment", 33 credits shown on the failed take) → Kokoro. storage.googleapis.com 200, elevenlabsusercontent.com 403 at root (reachable), upload.wikimedia.org 000 (blocked). Built: newton-lockdown-bread (v3-R, 17.8 s, plague lockdown 1665: Newton = calculus + gravity, classmate = bread) at 17:00 and mummy-medicine (v3-D, 22.5 s, dark bank #14) at 21:00. vidIQ: 10 credits (2× keyword research), balance 1855 → 1845.
- 2026-11-19: token OK (0 error posts). Matured: v3-R 795 (n=2), v3-D 48 (n=1), v2-B 144 (n=35) → rule needs ≥ 6 matured each → no style decision, keep 1 R + 1 D. **Dark keeps failing: all 4 published v3-D are < 50 views** (washington-bloodletting 48 @107 h, caesar-23-stabs 41 @8 h, socrates-rooster 24 @12 h, napoleon-green-wallpaper 10 @36 h) vs v3-R henry-armor-shrank 173 @16 h, caesar-three-word-update 109 @40 h. If henry-anne-little-neck (21 Nov) and marie-antoinette-pardon-me (23 Nov) also stay < 100 at 48 h, replace D with a second R before the 6-video rule completes. Today's D tests a different dark angle (a name everyone knows — the guillotine — instead of a death scene). ElevenLabs: test line failed again ("subscription has a failed or incomplete payment", 36 credits shown on the failed take) → Kokoro; storage.googleapis.com 200, elevenlabsusercontent.com 403 at root (reachable), upload.wikimedia.org 000 (blocked). Built: lincoln-hat-late-reply (v3-R, 15.6 s, "sorry for the late reply" — real 1850 letter: he lost it in his old hat) at 17:00 and guillotin-name (v3-D, 21.4 s, dark bank #20) at 21:00. vidIQ: 10 credits (2× keyword research), balance 1875 → 1865.
- 2026-11-18: token OK (0 error posts). Matured: v3-R 795 (n=2), v3-D 48 (n=1), v2-B 144 (n=35) → rule needs ≥ 6 matured each → no style decision, keep 1 R + 1 D. Early v3 (not matured): caesar-three-word-update (R) 77 @15 h, napoleon-green-wallpaper (D) 7 @11 h, napoleon-kicked-from-europe (R) 47 @7 h. **Dark is weak: all v3-D so far < 50 views (48 / 7)**; if caesar-23-stabs, henry-anne-little-neck and marie-antoinette-pardon-me also stay < 100 at 48 h, propose replacing D with a second R. ElevenLabs: test line failed again ("subscription has a failed or incomplete payment", 16 credits shown, not charged) → Kokoro. upload.wikimedia.org 000 (blocked), elevenlabsusercontent.com 403 at root (reachable). Built: henry-armor-shrank (v3-R, 17.7 s, "my armor shrank" excuse, 32 → 52 inch waist) at 17:00 and socrates-rooster (v3-D, 24.5 s, dark bank #18, last words about a rooster) at 21:00. vidIQ: 10 credits (2× keyword research), balance 1905 → 1895.
- 2026-11-17: **Kervly connector is back (YouTube token OK, 0 error posts) → backlog of 6 videos scheduled at 01:00 Dubai, 18–23 Nov** (napoleon-kicked-from-europe, caesar-23-stabs, napoleon-dutch-rabbit, henry-anne-little-neck, mozart-borrows-money, marie-antoinette-pardon-me) + today's 2 at 17:00 / 21:00 → 3 posts/day max. Matured: v3-R 789.5 (n=2), v3-D 47 (n=1), v2-B 143 (n=35). Rule needs ≥ 6 matured each → no style decision yet, keep 1 R + 1 D (v3-R looks 5× v2-B but n=2, both Napoleon). ElevenLabs: subscription payment failed again → Kokoro. Nothing new on YouTube since 13 Nov (no posts 14–16 Nov).
- 2026-11-16: **Kervly still needs reconnecting → nothing published since 13 Nov; backlog now 6 unscheduled videos** (the 4 from 14–15 Nov + today's 2). First matured v3 numbers: v3-R median 769.5 (n=2: napoleon-mom-texts 1199, napoleon-grouchy-omw 340), v3-D 46 (n=1: washington-bloodletting), v2-B matured ~140 (n=35; 129 for the 31 in the table). Rule needs ≥ 6 matured each → no style decision; keep 1 R + 1 D, but dark is 0 for 1 so far — if the next dark videos also stay < 100, propose dropping D. ElevenLabs: test generation failed again ("subscription has a failed or incomplete payment", no charge shown) → Kokoro. elevenlabsusercontent.com 403 at root (reachable), upload.wikimedia.org 000 (blocked). Built: mozart-borrows-money (v3-R, 16.9 s, new character) and marie-antoinette-pardon-me (v3-D, 22.2 s, dark bank #3). vidIQ: 5 credits (channel_videos), balance 1945 → 1940.
- 2026-11-15: **Kervly still disconnected (needs reconnect) → nothing published since 13 Nov 21:00; backlog now 4 unscheduled videos** (napoleon-kicked-from-europe, caesar-23-stabs, napoleon-dutch-rabbit, henry-anne-little-neck). v3 still has 0 matured videos (oldest 40 h) → no style decision, keep 1 R + 1 D. Early numbers: napoleon-mom-texts 1170 @40 h (growth slowed: +60 in 24 h), napoleon-grouchy-omw 317 @39 h, washington-bloodletting 30 @36 h → v3-R early median 743.5, v3-D 30, v2-B matured 140. Dark start is weak (n=1). **ElevenLabs generations all failed: "subscription has a failed or incomplete payment"** (15 lines, no audio) → both built with Kokoro. elevenlabsusercontent.com 403 at root (reachable), upload.wikimedia.org 000 (blocked). Metricool is connected but only has the kuranikerim_tr brand, so it cannot post to this channel. Built: napoleon-dutch-rabbit (v3-R, 16.7 s) and henry-anne-little-neck (v3-D, 20.3 s). vidIQ: 5 credits (no keyword research), balance 1970 → 1965.
- 2026-11-14: **Kervly connector disconnected in this session (needs reconnect in claude.ai) → today's 2 videos built and pushed but NOT scheduled**; stats via vidIQ channel_videos (5 credits). First v3 data (none matured yet): **napoleon-mom-texts (v3-R) 1110 views / 12 likes @16 h** (best start ever, most likes ever), napoleon-grouchy-omw (v3-R) 297 @15 h, washington-bloodletting (v3-D) 21 @12 h (weak). v3-R early median 703.5 vs v2-B matured 140 → promising, but rule needs ≥ 6 matured each → keep 1 R + 1 D. ElevenLabs CDN reachable (HTTP 403 at root, downloads OK) → both voiced with ElevenLabs; upload.wikimedia.org still blocked (000). Built: napoleon-kicked-from-europe (v3-R, 17.9 s) and caesar-23-stabs (v3-D, 25.4 s). vidIQ: 5 credits (no keyword research), balance 427 → 422. ElevenLabs ≈ 467 credits (13 lines, 1 take).
- 2026-11-13: token OK (0 error posts). v3 has no data yet (0 published; pilot napoleon-mom-texts goes live today 17:00) → no style decision possible, keep 1 R + 1 D. v2-B matured median 140 (n=31). Yesterday: **napoleon-renamed-josephine 790 @16 h** (2nd-fastest start ever, Napoleon again), caesar-laurel-bald 103 @12 h. **ElevenLabs CDN (elevenlabsusercontent.com) is reachable again** → both new episodes voiced with ElevenLabs (first since 2 Nov; matured EL v2-B median 200 vs Kokoro 124.5). upload.wikimedia.org still blocked (403). Today: napoleon-grouchy-omw (v3-R, 18:00 — 17:00 taken by the pilot) and washington-bloodletting (v3-D, 21:00). vidIQ: 10 credits (2× keyword research), balance 502 → 492. ElevenLabs ≈ 490 credits (15 lines, 1 take each).
- 2026-11-12 (evening, owner session): owner said the channel is not progressing and handed over full control. **Style v3 from 13 Nov: one v3-R (relatable everyday situation, 12–18 s) + one v3-D (dark humor bank, 16–26 s) per day**, themed music (`theme.music`), every fact web-verified. Pilot napoleon-mom-texts scheduled 13 Nov 17:00. Compare v3-R / v3-D / v2-B; ≥ 6 matured each → 1.5× rule. Blocked: realistic voices and real paintings need the owner to allow elevenlabsusercontent.com, assets.vidiq.com, upload.wikimedia.org, commons.wikimedia.org. vidIQ this session: 48 credits (4 outlier searches + 1 voiceover test).
- 2026-11-12: token OK (connection fine, 0 error posts). Matured B/A = 167 / 114 = 1.5× (same-period 3.0× still stands) → cold open in both slots stays. v2 matured median 153 vs v1 82 → no cut to 12–18 s. New split: matured ElevenLabs B median 199 (n=15) vs Kokoro B 132.5 (n=14) — voice quality may matter, but ElevenLabs CDN still blocked (elevenlabsusercontent.com 403) → Kokoro again. Yesterday: napoleon-hand-coat 119 @16 h + 1 comment (good), franklin-air-bath 24 @12 h (weak; Franklin's 2nd video flops). Today: napoleon-renamed-josephine (B, 17:00, Napoleon renamed Rose → Josephine, and himself from Buonaparte) and caesar-laurel-bald (B, 21:00, Suetonius: Caesar's always-on laurel wreath hid his baldness). vidIQ: 10 credits (2× keyword research), balance 570 → 560.
- 2026-11-11: token OK (connection fine, 0 error posts). Matured B/A = 168 / 114 = 1.5× (same-period 3.0× still stands) → cold open in both slots stays. v2 matured median 153.5 vs v1 82 → no cut to 12–18 s. New split: matured B ≤ 20 s median 138 (n=7) vs B > 20 s 168.5 (n=20) → the ≤ 20 s builds are not beating 20–26 s (confounded: most > 20 s were ElevenLabs), so aim back at 20–26 s. Yesterday: napoleon-canned-food 108 @15 h (ok), lincoln-sword-duel 36 @11 h (weak). Beethoven 60 @35 h (weak, confirmed). ElevenLabs CDN still blocked (403) → Kokoro. Today: napoleon-hand-coat (B, 17:00, 22.2 s, hand-in-coat was just a portrait pose + short callback) and franklin-air-bath (B, 21:00, 25.5 s, Franklin's 1768 naked "air baths"; Franklin = 467 views last time). vidIQ: 10 credits (2× keyword research), balance 595 → 585.
- 2026-11-10: token OK (connection fine, 0 error posts). Matured B/A = 167 / 114 = 1.5× (same-period 3.0× still stands) → cold open in both slots stays. v2 matured median 153 vs v1 82 → 18–28 s stays (≤ 20 s builds). Yesterday: napoleon-rosetta-stone 145 @15 h (ok), beethoven-60-beans 27 @11 h (weak → Beethoven not a repeat character). napoleon-chess-turk 530 @39 h (3rd best ever). Napoleon top-5: 1201 / 715 / 530 / 388 / 344. ElevenLabs CDN still blocked (403) → Kokoro. Today: napoleon-canned-food (B, 17:00, Napoleon funded canning → "what's the worst that could happen" Russia irony) and lincoln-sword-duel (B, 21:00, Lincoln picks broadswords vs Shields 1842). vidIQ: 10 credits (2× keyword research), balance 625 → 615.
- 2026-11-09: token OK (connection fine, 0 error posts). Matured B/A = 167 / 114 = 1.5× (same-period 3.0× still stands) → cold open in both slots stays. v2 matured median 153 vs v1 82 → 18–28 s stays; ≤ 20 s keeps working. Yesterday: **napoleon-chess-turk 419 @16 h** (2nd-fastest start ever, 1 comment) → Napoleon confirmed again (1199 / 711 / 419 / 385 / 344); egypt-cat-shields 122 @12 h (ok). washington-cherry-tree 252 @40 h, erik-greenland-scam 249 @60 h. ElevenLabs CDN still blocked → Kokoro. Today: napoleon-rosetta-stone (B, 17:00, 19.0 s, "French found it, British kept it") and beethoven-60-beans (B, 21:00, 19.9 s, new character test: Beethoven's 60-bean coffee). vidIQ: 10 credits (2× keyword research), balance 650 → 640.
- 2026-11-08: token OK (connection fine, 0 error posts). Matured B/A = 166 / 114 = 1.5× (same-period 24–30 Oct comparison 3.0× still stands, A has no new data) → cold open in both slots stays. v2 matured median 148 vs v1 82 → 18–28 s stays; short (≤ 20 s) keeps looking good: washington-whiskey (17.6 s) 212 @55 h, napoleon-sphinx-nose (19.5 s) 1168. Yesterday: washington-cherry-tree 136 @15 h (OK), olympics-naked 60 @11 h (weak). erik-greenland-scam 194 @35 h. ElevenLabs CDN still blocked → Kokoro. Today: napoleon-chess-turk (B, 17:00, 18.7 s, Napoleon = #1 character, "robot was a guy in a box") and egypt-cat-shields (B, 21:00, 19.1 s, ancient Egypt + cats, universal hook). vidIQ: 10 credits, balance 660 → 650.
- 2026-11-07: token OK (connection fine, 0 error posts). Matured B/A = 148 / 114 = 1.3× (A has had no new data since 29 Oct; same-period 24–30 Oct comparison B 344 vs A 114 = 3.0× still stands) → cold open in both slots stays. v2 matured median 129 vs v1 82 → 18–28 s stays, but the v2 median keeps sliding (the 2–6 Nov batch is mostly ~100–190, only napoleon-sphinx-nose 1105 broke out). Short test washington-whiskey (17.6 s) = 194 @32 h, best of the 4–5 Nov batch after the Sphinx → shorter keeps looking good; today's olympics-naked is 18.0 s. Yesterday: erik-greenland-scam 136 @12 h, napoleon-louisiana-sale 103 @16 h. ElevenLabs CDN still blocked → Kokoro. Today: washington-cherry-tree (B, 17:00, 20.5 s, Washington = 2 of top 3 videos, myth-bust) and olympics-naked (B, 21:00, 18.0 s, ancient Greece, new "everyday surprising fact" angle). vidIQ: 10 credits, balance 690 → 680.
- 2026-11-06: token OK (connection fine, 0 error posts). **napoleon-sphinx-nose = 1061 views in 15 h** (fastest video ever, 7 likes) → Napoleon confirmed as the #1 character (1061 / 711 / 382 / 344 / 112). Short test washington-whiskey (17.6 s, 5 msgs) 159 @7 h = 2nd-best start of the week; cleopatra-pearl-bet weak (49 @11 h); marie-antoinette-warship-hair stalled (8 @35 h). Matured B/A = 169 / 114 = 1.5× (fell under 2× as the weaker 2–3 Nov B batch matured), but same-period comparison (24–30 Oct) is B 344 vs A 114 = 3.0× → cold open in both slots stays. v2 167 vs v1 82 → 18–28 s stays (short test still unmatured). ElevenLabs CDN still blocked → Kokoro. Today: napoleon-louisiana-sale (B, 17:00, 23.7 s, Napoleon again + US-history hook) and erik-greenland-scam (B, 21:00, 20.2 s, "famous myth/fact" Viking angle). vidIQ: 10 credits (2× keyword research), balance 715.
- 2026-11-05: token OK (0 error posts, connection fine). henry-groom-of-stool published 01:00 (72 @8 h). Matured: B/A 256 / 113 = 2.3× → cold open in both slots stays; v2 168 vs v1 81 → 18–28 s stays. Recent trend is weak: the 9 v2 published since 2 Nov have median 102 (only napoleon-vs-pug 371 broke out). marie-antoinette-warship-hair has only 3 views @12 h (looks suppressed/stalled, watch it); alexander-gordian-knot 92 @16 h. Kokoro-only videos (4) median 91 vs same-age ElevenLabs ~100–165 — weak signal. ElevenLabs CDN still blocked → Kokoro again. Today: Napoleon returns (strongest character) with a myth-bust: napoleon-sphinx-nose (B, 17:00, 19.5 s); cleopatra-pearl-bet (B, 21:00, 20.9 s). Short test washington-whiskey publishes 6 Nov 01:00.
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
| group-halloween-party | v1 | 44 | 2026-10-15 | 6 | 1 | 0 |
| socrates-vs-xanthippe | v1 | 59 | 2026-10-16 | 98 | 0 | 0 |
| leonardo-vs-michelangelo | v1 | 59 | 2026-10-16 | 55 | 0 | 0 |
| beethoven-vs-goethe | v1 | 59 | 2026-10-17 | 85 | 0 | 0 |
| caesar-vs-cleopatra | v1 | 59 | 2026-10-17 | 159 | 0 | 1 |
| kepler-vs-galileo | v1 | 59 | 2026-10-17 | 5 | 1 | 0 |
| lovelace-vs-babbage | v1 | 59 | 2026-10-18 | 74 | 0 | 0 |
| hannibal-vs-scipio | v1 | 59 | 2026-10-19 | 54 | 0 | 0 |
| shakespeare-vs-anne | v1 | 52 | 2026-10-19 | 98 | 0 | 0 |
| cope-vs-marsh | v1 | 57 | 2026-10-20 | 96 | 0 | 0 |
| plato-vs-diogenes | v1 | 59 | 2026-10-20 | 103 | 0 | 0 |
| rousseau-vs-marie-antoinette | v1 | 59 | 2026-10-20 | 119 | 0 | 0 |
| byron-vs-mary-shelley | v1 | 59 | 2026-10-21 | 68 | 0 | 0 |
| philip-vs-sparta | v1 | 59 | 2026-10-21 | 220 | 1 | 0 |
| halley-vs-newton | v1 | 59 | 2026-10-21 | 83 | 0 | 0 |
| darwin-vs-emma | v1 | 59 | 2026-10-22 | 37 | 0 | 0 |
| caesar-vs-pirates | v2-A | 28.7 | 2026-10-24 17:00 | 168 (591 h) | 0 | 0 |
| henry-viii-catfish-v2 | v2-B | 24.3 | 2026-10-24 21:00 | 570 (587 h) | 1 | 0 |
| xerxes-vs-leonidas | v2-A | 27.4 | 2026-10-25 01:00 | 294 (583 h) | 1 | 0 |
| spartan-mom | v2-A | 25.6 | 2026-10-25 17:00 | 387 (567 h) | 0 | 0 |
| washington-teeth | v2-B | 20.3 | 2026-10-25 21:00 | 1114 (611 h) | 9 | 0 |
| napoleon-vs-rabbits | v2-B | 22.7 | 2026-10-26 01:00 | 344 (559 h) | 2 | 0 |
| vangogh-sunflowers | v2-A | 28.3 | 2026-10-26 17:00 | 114 (591 h) | 0 | 0 |
| alexander-city-names | v2-B | 24.7 | 2026-10-26 21:00 | 170 (611 h) | 3 | 0 |
| diogenes-lamp | v2-A | 29.6 | 2026-10-27 17:00 | 65 (591 h) | 0 | 0 |
| napoleon-short | v2-B | 26.2 | 2026-10-27 21:00 | 718 (587 h) | 9 | 1 |
| revere-vs-dawes | v2-B | 26.1 | 2026-10-28 17:00 | 86 (567 h) | 0 | 0 |
| viking-horns | v2-A | 28.3 | 2026-10-28 21:00 | 47 (563 h) | 0 | 0 |
| leonardo-mona-lisa | v2-A | 29.2 | 2026-10-29 17:00 | 53 (543 h) | 0 | 0 |
| franklin-vs-eagle | v2-B | 26.9 | 2026-10-29 21:00 | 469 (539 h) | 1 | 0 |
| cleopatra-iphone | v2-B | 25.3 | 2026-10-30 17:00 | 129 (519 h) | 2 | 0 |
| poe-vs-raven | v2-B | 24.3 | 2026-10-30 21:00 | 64 (515 h) | 0 | 0 |
| napoleon-vs-pug | v2-B | 23.7 | 2026-11-03 01:00 | 389 (367 h) | 3 | 0 |
| newton-south-sea | v2-B | 26.3 | 2026-11-02 17:00 | 168 (447 h) | 2 | 0 |
| roman-pee-laundry | v2-B | 23.1 | 2026-11-02 21:00 | 104 (443 h) | 0 | 0 |
| lincoln-wrestling | v2-B | 26.2 | 2026-11-04 01:00 | 200 (343 h) | 1 | 0 |
| napoleon-elba-escape | v2-B (kokoro) | 19.9 | 2026-11-03 17:00 | 118 (423 h) | 1 | 0 |
| caesar-calendar | v2-B (kokoro) | 21.2 | 2026-11-03 21:00 | 116 (419 h) | 1 | 0 |
| alexander-gordian-knot | v2-B (kokoro) | 19.4 | 2026-11-04 17:00 | 109 (399 h) | 0 | 0 |
| marie-antoinette-warship-hair | v2-B (kokoro) | 22.2 | 2026-11-04 21:00 | 15 (395 h) | 0 | 0 |
| henry-groom-of-stool | v2-B | 23.7 | 2026-11-05 01:00 | 112 (319 h) | 0 | 0 |
| washington-whiskey | v2-B short | 17.6 | 2026-11-06 01:00 | 213 (295 h) | 0 | 0 |
| napoleon-sphinx-nose | v2-B (kokoro) | 19.5 | 2026-11-05 17:00 | 1206 (375 h) | 8 | 0 |
| cleopatra-pearl-bet | v2-B (kokoro) | 20.9 | 2026-11-05 21:00 | 127 (371 h) | 1 | 0 |
| napoleon-louisiana-sale | v2-B (kokoro) | 23.7 | 2026-11-06 17:00 | 144 (351 h) | 2 | 0 |
| erik-greenland-scam | v2-B (kokoro) | 20.2 | 2026-11-06 21:00 | 251 (347 h) | 1 | 0 |
| washington-cherry-tree | v2-B (kokoro) | 20.5 | 2026-11-07 17:00 | 265 (327 h) | 1 | 0 |
| olympics-naked | v2-B (kokoro) | 18.0 | 2026-11-07 21:00 | 72 (323 h) | 0 | 0 |
| napoleon-chess-turk | v2-B (kokoro) | 18.7 | 2026-11-08 17:00 | 574 (303 h) | 3 | 1 |
| egypt-cat-shields | v2-B (kokoro) | 19.1 | 2026-11-08 21:00 | 137 (299 h) | 1 | 0 |
| napoleon-rosetta-stone | v2-B (kokoro) | 19.0 | 2026-11-09 17:00 | 169 (279 h) | 0 | 0 |
| beethoven-60-beans | v2-B (kokoro) | 19.9 | 2026-11-09 21:00 | 74 (275 h) | 0 | 0 |
| napoleon-canned-food | v2-B (kokoro) | 18.9 | 2026-11-10 17:00 | 122 (255 h) | 0 | 0 |
| lincoln-sword-duel | v2-B (kokoro) | 18.4 | 2026-11-10 21:00 | 51 (251 h) | 0 | 0 |
| napoleon-hand-coat | v2-B (kokoro) | 22.2 | 2026-11-11 17:00 | 144 (231 h) | 0 | 3 |
| franklin-air-bath | v2-B (kokoro) | 25.5 | 2026-11-11 21:00 | 26 (227 h) | 0 | 0 |
| napoleon-renamed-josephine | v2-B (kokoro) | 24.0 | 2026-11-12 17:00 | 815 (207 h) | 1 | 0 |
| caesar-laurel-bald | v2-B (kokoro) | 24.6 | 2026-11-12 21:00 | 115 (203 h) | 1 | 0 |
| napoleon-mom-texts | v3-R (kokoro) | 16.7 | 2026-11-13 17:00 | 1246 (183 h) | 12 | 0 |
| napoleon-grouchy-omw | v3-R (elevenlabs) | 18.0 | 2026-11-13 18:00 | 348 (182 h) | 1 | 0 |
| washington-bloodletting | v3-D (elevenlabs) | 24.3 | 2026-11-13 21:00 | 48 (179 h) | 0 | 0 |
| napoleon-kicked-from-europe | v3-R (elevenlabs) | 17.9 | 2026-11-18 01:00 | 69 (79 h) | 0 | 0 |
| caesar-23-stabs | v3-D (elevenlabs) | 25.4 | 2026-11-19 01:00 | 59 (55 h) | 0 | 0 |
| napoleon-dutch-rabbit | v3-R (kokoro) | 16.7 | 2026-11-20 01:00 | 77 (31 h) | 1 | 0 |
| henry-anne-little-neck | v3-D (kokoro) | 20.3 | 2026-11-21 01:00 | 171 (7 h) | 1 | 0 |
| mozart-borrows-money | v3-R (kokoro) | 16.9 | 2026-11-22 01:00 (scheduled) | – | – | – |
| marie-antoinette-pardon-me | v3-D (kokoro) | 22.2 | 2026-11-23 01:00 (scheduled) | – | – | – |
| caesar-three-word-update | v3-R (kokoro) | 17.6 | 2026-11-17 17:00 | 127 (87 h) | 3 | 0 |
| napoleon-green-wallpaper | v3-D (kokoro) | 25.0 | 2026-11-17 21:00 | 10 (83 h) | 0 | 0 |
| henry-armor-shrank | v3-R (kokoro) | 17.7 | 2026-11-18 17:00 | 178 (63 h) | 0 | 0 |
| socrates-rooster | v3-D (kokoro) | 24.5 | 2026-11-18 21:00 | 162 (59 h) | 1 | 0 |
| lincoln-hat-late-reply | v3-R (kokoro) | 15.6 | 2026-11-19 17:00 | 144 (39 h) | 2 | 0 |
| guillotin-name | v3-D (kokoro) | 21.4 | 2026-11-19 21:00 | 34 (35 h) | 2 | 0 |
| newton-lockdown-bread | v3-R (kokoro) | 17.8 | 2026-11-20 17:00 | 95 (15 h) | 3 | 0 |
| mummy-medicine | v3-D (kokoro) | 22.5 | 2026-11-20 21:00 | 268 (11 h) | 1 | 0 |
| napoleon-left-on-read | v3-R (kokoro) | 16.0 | 2026-11-21 17:00 (scheduled) | – | – | – |
| king-14-desserts | v3-D (kokoro) | 23.9 | 2026-11-21 21:00 (scheduled) | – | – | – |
