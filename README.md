# 🛠️ GBSS Agency - Game Dev Asset Scraper

An automated, anti-bot resistant scraper designed to harvest, structure, and categorize 4,000+ game development assets across major game engines and distribution platforms into searchable CSV databases.

---

## 🚀 Features

* **Anti-Bot Resistance:** Utilizes `curl_cffi` to mimic real browser TLS/JA3 fingerprints and bypass Cloudflare protection without headless browsers.
* **Multi-Engine Target Coverage:** Scrapes assets for:
  * **Godot Engine** (GDScript, Shaders, 2D/3D Assets)
  * **Unity** (Packages, Tools, VFX)
  * **Unreal Engine** (Low-poly Megakits, Blueprints, Characters)
  * **Itch.io** (Indie Audio, Pixel Art Tilesets, Retro Assets)
* **Automated Pagination:** Handles multi-page queries (pages 1–8+) for full dataset extraction.
* **CI/CD Integration:** Runs automatically via GitHub Actions with write permissions to update asset CSVs on a schedule.

---

## 📁 Repository Structure

```text
├── .github/
│   └── workflows/
│       └── scrape.yml         # Automated GitHub Actions runner
├── data/
│   ├── godot_assets.csv       # Godot asset directory
│   ├── unity_assets.csv       # Unity asset directory
│   ├── unreal_assets.csv      # Unreal Engine asset directory
│   └── itchio_assets.csv      # Itch.io indie resource directory
├── scraper_master.py          # Main Python engine
├── requirements.txt           # Python dependencies
└── README.md
