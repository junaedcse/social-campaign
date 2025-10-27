# Fonts Directory

This directory contains bundled fonts for multi-language text rendering in generated campaign images.

## Fonts Included

### Latin Languages (English, French, Spanish, German, Portuguese)
- **Noto Sans Bold** (`latin/NotoSans-Bold.ttf`)
  - Designer: Google
  - License: SIL Open Font License 1.1
  - Unicode coverage: Latin, Latin Extended, Cyrillic
  - Size: ~500 KB

### Japanese
- **Noto Sans Japanese Bold** (`japanese/NotoSansJP-Bold.ttf`)
  - Designer: Google
  - License: SIL Open Font License 1.1
  - Unicode coverage: Hiragana, Katakana, Kanji
  - Size: ~6 MB

### Fallback
- **DejaVu Sans Bold** (`fallback/DejaVuSans-Bold.ttf`)
  - Designer: DejaVu Fonts Team
  - License: DejaVu Fonts License
  - Unicode coverage: Extensive Latin, Cyrillic, Greek
  - Size: ~700 KB

## Total Size

Approximately 7-8 MB

## Why Bundle Fonts?

Bundled fonts ensure consistent text rendering across all platforms:
- ✅ Developers' machines
- ✅ Client machines
- ✅ CI/CD servers
- ✅ Docker containers
- ✅ Cloud deployments

Without bundled fonts, users would see missing characters (□ "tofu") for languages their system doesn't support.

## Font Licenses

All fonts are open source and free for commercial use.

### Noto Sans Family
- License: SIL Open Font License 1.1
- Copyright: Google Inc.
- Source: https://fonts.google.com/noto
- License text: https://scripts.sil.org/OFL

### DejaVu Sans
- License: DejaVu Fonts License (based on Bitstream Vera & Arev licenses)
- Copyright: DejaVu Fonts Team
- Source: https://dejavu-fonts.github.io/
- License text: https://dejavu-fonts.github.io/License.html

Both licenses allow:
- ✅ Commercial use
- ✅ Distribution
- ✅ Modification
- ✅ Bundling in applications

## Updating Fonts

To update or re-download fonts, run:

```bash
python scripts/maintenance/download_fonts.py
```

## Manual Download

If the script fails, download fonts manually:

1. **Noto Sans**: https://fonts.google.com/noto/specimen/Noto+Sans
2. **Noto Sans JP**: https://fonts.google.com/noto/specimen/Noto+Sans+JP
3. **DejaVu Sans**: https://dejavu-fonts.github.io/

Place downloaded `.ttf` files in the appropriate subdirectories.

## Adding More Languages

To add support for additional languages:

1. Download appropriate Noto font (e.g., `NotoSansArabic-Bold.ttf`)
2. Place in relevant subdirectory
3. Update `FONT_MAP` in `src/services/image_processor.py`
4. Test with `python scripts/dev/test_fonts.py`

### Available Noto Fonts

- Arabic: NotoSansArabic
- Chinese (Simplified): NotoSansSC
- Chinese (Traditional): NotoSansTC
- Korean: NotoSansKR
- Thai: NotoSansThai
- Hebrew: NotoSansHebrew
- And many more: https://fonts.google.com/noto

## Troubleshooting

### Font not rendering
- Verify font file exists
- Check file size (should not be 0 bytes)
- Ensure language code is in `FONT_MAP`
- Run test: `python scripts/dev/test_fonts.py`

### Download failed
- Check internet connection
- Try manual download (links above)
- Check GitHub/source website is accessible

### File too large
- Fonts are compressed (7-8 MB total is normal)
- Consider using Git LFS for very large repositories
- Alternatively, download on first run (not recommended)

## Support

For issues or questions:
1. Check this README
2. See main project README.md
3. Review `FONT_BUNDLING_GUIDE.md`

---

*Last updated: 2025-10-27*
