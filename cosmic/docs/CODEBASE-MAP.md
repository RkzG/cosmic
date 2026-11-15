# Peta kode EffectCraft untuk Cosmic

Disusun 2026-11-15 dari EffectCraft 0.24.1 (`upstream/main` di commit `7cbefaf7`). Sumber utama: `docs/architecture.md`, `docs/agents.md`, `docs/control-protocol.md` milik upstream. Periksa ulang setelah sinkron upstream; nama file bisa berubah.

## Lapisan crate

Ketergantungan hanya boleh mengarah ke bawah. `cargo xtask layers` menolak build kalau crate di bawah L5 memakai egui, eframe, winit, rfd, cpal, atau muda.

| Lapisan | Crate | Isi singkat |
| --- | --- | --- |
| L0 | `time`, `geom`, `color`, `opusenc` | Waktu (`Tick`, 254 016 000 000 per detik), matematika, warna, encoder Opus |
| L1 | `raster`, `keyframe`, `segment`, `psd`, `path` | Gambar, keyframe, model AI roto/wajah, PSD, path Bezier |
| L2 | `project`, `text`, `effects`, `svg`, `pdf`, `model`, `track` | Dokumen proyek (`.ecproj`), teks, 306 efek, impor vektor, 3D, tracking |
| L3 | `render`, `media`, `expr`, `export`, `gpu`, `sam2`, `interchange`, `aep`, `lottie`, `plugin`, `helper-host` | Render, decoding footage, expression, encoding, GPU, impor/ekspor format lain, plug-in |
| L4 | `engine`, `script`, `host` | `Session`, undo, **registry perintah**, scripting JSX, sesi lengkap untuk frontend |
| L5 | `ui-egui`, `automation` | Antarmuka desktop, **server MCP** |
| L6 | `apps/effectcraft`, `apps/effectcraft-cli`, `apps/effectcraft-web` | Aplikasi desktop, CLI, versi browser |

## Tempat-tempat penting untuk Cosmic

### Sistem perintah (jalur utama AI → editor)

Setiap aksi adalah perintah dengan id, label, menu, shortcut, parameter, `enabled()`, dan `run()`. UI, CLI, control channel, dan MCP semuanya memanggil perintah lewat id.

- `crates/engine/src/cmd.rs`: registry perintah. Id mengikuti struktur menu After Effects.
- `crates/engine/src/cmd/`: implementasi per kelompok (`layer.rs`, `effect.rs`, `prop.rs`, `file.rs`, `markers.rs`, `query.rs`, dan lainnya).
- `crates/engine/src/menus.rs`: susunan menu sebagai pohon id perintah.
- `crates/engine/src/history.rs`: riwayat undo bercabang. AI bisa membacanya untuk membedakan editan manual dan editan AI.

### Control channel dan MCP

- `apps/effectcraft/src/control_server.rs`: server JSON-lines (`--control PORT`).
- `crates/ui-egui/src/control.rs`: penanganan permintaan control di sisi UI (state, input, screenshot).
- `crates/ui-egui/src/automation.rs`: id otomasi untuk setiap widget.
- `crates/automation/src/`: server MCP. `tools.rs` berisi daftar tool, `bridge.rs` untuk mode bridge ke aplikasi yang sedang terbuka, `confine.rs` untuk batas `--automation-read-root/--automation-write-root`, dan `autosave.rs`.
- `apps/effectcraft-cli/src/main.rs`: subperintah CLI (`render`, `render-frame`, `info`, `exec`, `get/set`, `script`, `mcp`).
- Referensi protokol: `docs/control-protocol.md` dan `docs/agents.md`.

### Panel UI (tempat panel tahap Cosmic nanti)

- `crates/ui-egui/src/dock.rs`: `enum PanelKind`, daftar semua jenis panel beserta judul dan id.
- `crates/ui-egui/src/panels.rs`: `panels::show` mengarahkan setiap `PanelKind` ke fungsi gambarnya.
- `crates/ui-egui/src/panels/`: isi tiap panel (`timeline/`, `effect_controls/`, `project.rs`, `script_console.rs`, dan lainnya). Contoh panel kecil yang bisa ditiru: `info.rs`.
- `crates/ui-egui/src/dock_ui.rs`: docking dan layout panel.
- `crates/ui-egui/src/header.rs`: bilah atas (tombol About, GitHub, web, logo).

**Titik sambung yang mungkin untuk panel Cosmic** (belum diubah): satu varian baru di `PanelKind` dan satu baris di `panels::show`, dengan isi panel di modul baru. Ini akan jadi patch upstream dan wajib dicatat di `UPSTREAM-PATCHES.md`.

### Scripting

- `crates/script/`: JavaScript (boa) dengan model objek ala After Effects. Setiap editan lewat script menjalankan perintah engine, jadi semuanya bisa di-undo.

### Format proyek

- `crates/project/`: `Project`, `Comp`, `Layer`, dan pohon `Property`. File `.ecproj` adalah JSON dengan `savedBy` dan `schema`.
- Properti diakses lewat path seperti `transform/position` atau `effects/#1/blurriness`, atau lewat `@uid`.

## Aturan teknis upstream yang ikut berlaku

- Kode non-test tidak boleh panik: tanpa `unwrap`, `expect`, `panic!`, dan sejenisnya. Juga tanpa `unsafe`.
- Crate baru wajib punya `[lints] workspace = true` dan atribut `#![deny(clippy::unwrap_used, ...)]`.
- Setiap aset punya file `.attribution` dan baris di `ATTRIBUTION.md`.
- Gerbang kualitas: `cargo xtask ci`.

## Build di Windows

- Toolchain: `stable-x86_64-pc-windows-msvc`, Rust 1.95 atau lebih baru (`rust-version` di `Cargo.toml`).
- Aplikasi: `cargo build --release -p effectcraft`, lalu jalankan `target/release/effectcraft.exe`.
- CLI: `cargo build --release -p effectcraft-cli`, lalu jalankan `target/release/effectcraft-cli.exe`.
- Untuk pengembangan cepat: `cargo run -p effectcraft -- --demo` (profil dev).
