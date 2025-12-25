# PrestaShop Selenium (Pytest) UI Test Automation

Bu repo, PrestaShop demo mağazası üzerinde **Selenium WebDriver + Pytest** kullanarak geliştirilmiş bir **UI test otomasyonu** örneğidir.  
Testler; temel akışlar (smoke), arama (pozitif/negatif), sepete ekleme ve sınır (boundary) senaryolarını kapsar.  
Ek olarak `pytest-html` ile **HTML test raporu** üretilebilir.

## ✅ Kapsam
- **Smoke Test**: Front office ana sayfanın açılması
- **Pozitif Test**: Ürün araması (ör. `mug`) ve sonuç doğrulama
- **Pozitif Test**: Arama sonucu ürüne gidip sepete ekleme
- **Negatif Test**: Sonuçsuz arama (no-result)
- **Boundary Tests**: 1 karakter, TR karakter, özel karakter, çok uzun input vb.

> Not: PrestaShop demo ortamı zaman zaman kararsız olabildiği için testlerde beklemeler (explicit wait) kullanılmıştır.

---
