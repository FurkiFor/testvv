# Yok Artık! — Türkçe Shorts üretim hattı

"Yok Artık!" YouTube kanalı (Kervly brand `yokartik`) için kodla animasyonlu, ElevenLabs seslendirmeli
"yok artık" dedirten bilgi Shorts'ları. Tema: **pop** (sarı çizgi roman). Videolar `videos/yokartik/` altına
gider, Kervly oradan yayınlar.

## Dosyalar
- `engine.py` — render motoru (1080x1920, 30 fps, Pillow + ffmpeg). Sahne tipleri: `hook`, `statement`,
  `number`, `timeline`, `outro`.
- `setup.sh` — Twemoji ikonlarını (npm) ve Python paketlerini kurar.
- `YAZIM-KURALLARI.md` — hook, uzunluk, Türkçe dil ve doğruluk kuralları. **Her senaryodan önce oku.**
- `scripts/NNN-slug.json` — her videonun senaryosu (seslendirme + altyazı + sahneler + YouTube metinleri).
- `LOG.md` — yayınlanan her video (konu, kategori, hook tipi, post id). Konu tekrarını buradan kontrol et.
- `FIKIRLER.md` — kullanılabilir konu havuzu.

## Senaryo JSON
```json
{"id": "004-slug", "theme": "pop", "topic": "uzay|tarih|vücut|hayvan",
 "hook_mechanism": "...", "sources": ["..."],
 "youtube": {"title": "... #shorts", "caption": "...", "tags": ["..."]},
 "scenes": [
  {"type": "hook", "say": "[surprised] ...", "cap": "öbek / öbek / öbek", "icons": ["1f988","274c","1f333"],
   "text": "Ekrandaki hook", "hl": {"kelime!": "red"}},
  {"type": "number", "say": "...", "cap": "...", "icon": "1f988", "value": 450, "prefix": "MÖ ", "suffix": " GÜN",
   "year": true, "size": 170, "color": "green", "label": "etiket"},
  {"type": "statement", "say": "...", "icon": "venus", "text": "Venüs", "hl": {"Venüs": "red"}},
  {"type": "timeline", "say": "...", "cap": "...",
   "points": [{"at": -450, "icon": "1f988", "label": "Köpekbalığı", "year": "450 milyon", "delay": 0}],
   "spans": [{"from": -450, "to": -385, "text": "60+ MİLYON YIL", "color": "red|green", "side": "below|above", "delay": 4.0}]},
  {"type": "outro", "say": "[excited] ... Yok artık!", "icon": "1f92f", "text": "Bilmeyen arkadaşına gönder", "hl": {"gönder": "red"}}
 ]}
```
- `say`: ElevenLabs'e gidecek metin; sayılar yazıyla, ses etiketleri `[surprised]`, `[curious]`, `[excited]`.
  Tüm sahnelerin `say` metinleri boşlukla birleştirilip TEK seslendirme olarak üretilir.
- `cap`: ekrandaki altyazı; rakamla, öbekler ` / ` ile (2–3 kelime, ≤ 20 karakter).
- İkonlar: Twemoji kod noktası (`assets/tw/package/<kod>.svg` var olmalı) veya özel: `pyramid`, `venus`, `mars`, `planet`.
- `delay`: sahne başından saniye. Görsel olayı ilgili kelimeye denk getir (kelime zamanları `--words` dosyasında).
  Gizli kalacak nokta için `"delay": 99`.

## Bir videonun üretimi
1. `bash yokartik/setup.sh` (bir kez).
2. Senaryoyu yaz → `python3 yokartik/engine.py --preview yokartik/scripts/<id>.json /tmp/<id>.png` → Read ile bak.
3. Seslendirme: `creative_generate_speech` (model `eleven_v4`, voice `RDNgFQdRVzvDdSV3I6nb` "Fatih",
   **generations_count 1**, prompt = birleşik `say`). Asla aynı üretimi tekrar başlatma.
4. `creative_add_flow_asset_node` (generation_id) → dönen node ile `creative_transcribe_audio`
   (`eleven_scribe_v1`, connect_from). `creative_get_flow_run_status` ile ses `media[0].url` ve
   `transcripts[0].words_download_url` al, curl ile indir (`work/vo-<id>.mp3`, `work/vo-<id>.words.json`).
5. `python3 yokartik/engine.py yokartik/scripts/<id>.json work/vo-<id>.mp3 videos/yokartik/<id>.mp4 --words work/vo-<id>.words.json`
   Konsolda "uyarı: kelime sayısı tutmadı" görürsen sessizlik hizalamasına düşmüştür; video yine geçerli.
6. Kontrol: ffprobe (süre 18–35 sn, < 50 MB), 5 kareyi yan yana Read ile incele (hook ilk karede, taşma yok, Türkçe doğru).
7. Commit + push → raw URL 200 → Kervly `schedule_post`.

## Kervly
- brand `yokartik`, platform `["youtube"]`, saat dilimi Europe/Istanbul, günde en fazla 3 gönderi.
- options: `{"youtube":{"privacy":"public","category":"EDUCATION","madeForKids":false,"notifySubscribers":true,"language":"tr","audioLanguage":"tr","aiGenerated":false}}`
- `create_upload_link` PUT'u bu ortamda proxy'ye takılıyor (403); videoyu git ile push edip raw URL kullan.
