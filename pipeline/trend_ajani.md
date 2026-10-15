# Trend Ajanı — talimat

Her üretim çalıştırmasının başında bir alt ajan (Agent tool, `general-purpose`) bu talimatla başlatılır. Ajan güncel olayları araştırır ve bölüm fikirleri önerir. Çıktısı `pipeline/fikirler/YYYY-MM-DD.md` dosyasına kaydedilir. Ana oturum bölümleri bu listeden seçer (ya da `karakter.md` §7 fikir bankasından).

## Ajana verilecek görev

1. **Araştır** (WebSearch, aramaları paralel gönder): son ~2 haftada sıradan insanların grup sohbetlerinde konuştuğu 10–15 konuyu bul. Kaynakları ve tarihlerini not et.
   - **Konu kaynakları:** teknoloji ve gadget lansmanları, uygulama güncellemeleri, yapay zeka ürünleri, viral TikTok/Reddit trendleri ve meme'ler, büyük film/dizi/oyun/albüm çıkışları, hafif spor anları, mevsimsel konular (saat değişikliği, bayramlar, Cadılar Bayramı, indirim günleri), fiyat artışları ve abonelikler.
   - vidIQ varsa `vidiq_keyword_research` mode `rising` ile de kontrol et.
   - **Hariç:** savaş, terör, felaket, ölümler, suç, seçimler, parti siyaseti, din, sağlık trajedileri.
2. **Kadro:** Yalnızca `karakter.md`'deki karakterler ve sabit şakaları. Yaşayan kişiler asla karakter olmaz. Hitler ve Stalin önerilerde yalnızca §0'daki şartlarla yer alır (haftada en fazla 1).
3. **Çıktı:** 8–10 fikir, en iyisi en üstte. Her fikir için:
   - Başlık (İngilizce)
   - Güncel kanca + kaynak ve tarih (1 satır)
   - Günlük problem (1 satır)
   - İkili (tam 2 karakter) ve sabit şakalarının neden çarpıştığı
   - 5–7 satırlık mini senaryo: İngilizce, iki konuşmacı, küçük harfle mesajlaşma tarzında, argo sadece doğal olduğu yerde, en fazla bir 💀, PG-13, punchline şakalardan doğmalı
   - Shorts'ta neden tutar (1 satır)
4. `episodes/LOG.md`'de daha önce kullanılmış ikili+espri kombinasyonlarını tekrar önerme.
5. Doğrulanamayan söylentileri (ör. henüz duyurulmamış ürünler) "rumor" diye işaretle.
