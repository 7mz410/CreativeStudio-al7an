# Attribution

Every asset bundled with or committed to SoundCraft is listed here with its author, source and
license. `cargo xtask assets` fails CI when a tracked asset file has no row.

**Rule:** no Avid, Pro Tools, Adobe or other proprietary icons, images, sounds or presets — ever.
Assets must be original, public domain (CC0) or permissively licensed. See `AGENTS.md`.

## Icons

All UI icons (tools, transport, track buttons) are drawn procedurally in
`crates/ui-egui/src/icons.rs` by the SoundCraft contributors (MIT OR Apache-2.0). No UI icon image
files are used. The app icon (`assets/app-icon/`, a singing nightingale drawn as original SVG by
the SoundCraft contributors) is listed under Files below.

## Audio

The demo session's audio (drums, bass, pad) and its MIDI parts are synthesised in code in
`crates/engine/src/demo.rs` by the SoundCraft contributors (MIT OR Apache-2.0). No sample files
are bundled.

## Fonts

SoundCraft bundles one font file, for the Arabic interface: Noto Sans Arabic (OFL-1.1, see `assets/fonts/noto-sans-arabic/`). It uses the default fonts shipped inside the `egui` crate
(Ubuntu-Light: Ubuntu Font Licence 1.0; Hack: MIT; Noto Emoji: OFL-1.1; emoji-icon-font: OFL-1.1/MIT)
and, at runtime, the operating system's own UI fonts when available (never redistributed).

## Files

| Path | Author | Source | License |
|---|---|---|---|
| `assets/app-icon/al7an-document.svg` | Hamza Abu Ayyash (Creative Studio) | the mzika icon (`file icons/mzika.svg`, the former name of this app) used as the document icon | MIT OR Apache-2.0 | Document icon of `.al7an` sessions |
| `assets/app-icon/al7an-document.icns` | Hamza Abu Ayyash (Creative Studio) | `assets/app-icon/al7an-document.svg` rendered with rsvg-convert, packed with iconutil | MIT OR Apache-2.0 | Document icon of `.al7an` sessions |
| `assets/app-icon/icon.svg` | Hamza Abu Ayyash (Creative Studio) | the al7an star (`docs/studio/al7an.svg`) on a navy tile, rendered by `packaging/icons.sh` | MIT OR Apache-2.0 | App icon (see `assets/app-icon/README.md`) |
| `packaging/macos/dmg/` (all files) | @XusBadia | original (macOS DMG window background and layout, from the app icon; see `packaging/macos/dmg/README.md`) | MIT OR Apache-2.0 |
| `assets/app-icon/soundcraft-1024.png` | Hamza Abu Ayyash (Creative Studio) | the al7an star (`docs/studio/al7an.svg`) on a navy tile, rendered by `packaging/icons.sh` | MIT OR Apache-2.0 | App icon (see `assets/app-icon/README.md`) |
| `assets/app-icon/soundcraft-macos-512.png` | Hamza Abu Ayyash (Creative Studio) | the al7an star (`docs/studio/al7an.svg`) on a navy tile, rendered by `packaging/icons.sh` | MIT OR Apache-2.0 | App icon (see `assets/app-icon/README.md`) |
| `assets/app-icon/soundcraft.icns` | Hamza Abu Ayyash (Creative Studio) | the al7an star (`docs/studio/al7an.svg`) on a navy tile, rendered by `packaging/icons.sh` | MIT OR Apache-2.0 | App icon (see `assets/app-icon/README.md`) |
| `assets/app-icon/soundcraft.ico` | Hamza Abu Ayyash (Creative Studio) | the al7an star (`docs/studio/al7an.svg`) on a navy tile, rendered by `packaging/icons.sh` | MIT OR Apache-2.0 | App icon (see `assets/app-icon/README.md`) |
| `assets/app-icon/hicolor/` | Hamza Abu Ayyash (Creative Studio) | the al7an star (`docs/studio/al7an.svg`) on a navy tile, rendered by `packaging/icons.sh` | MIT OR Apache-2.0 | App icon (see `assets/app-icon/README.md`) |
| `assets/fonts/noto-sans-arabic/NotoSansArabic.ttf`, `OFL.txt` | The Noto Project Authors (Google Fonts) | [google/fonts@7085eb8](https://github.com/google/fonts/tree/7085eb89a950e85db5b166b7a58d414544b4140c/ofl/notosansarabic), byte-identical to `craft-fonts` | OFL-1.1 (`assets/fonts/noto-sans-arabic/OFL.txt`) |
| `docs/images/` | SoundCraft contributors | screenshots of SoundCraft rendered from the synthesised demo session | MIT OR Apache-2.0 |
