# Perubahan pada kode inti upstream

Setiap perubahan pada file milik EffectCraft upstream wajib dicatat di sini. Tujuannya: saat menggabungkan update dari upstream, kita tahu persis titik mana yang perlu dicek ulang.

Fitur baru sebaiknya berada di file atau modul baru, sehingga daftar ini tetap pendek.

## Format

| Tanggal | File | Alasan | Ringkasan perubahan | Commit |
| --- | --- | --- | --- | --- |
| 2026-11-15 | `CLAUDE.md` (root) | Supaya Claude Code memuat panduan Cosmic | Tambah satu baris `@cosmic/CLAUDE.md` di akhir file | |
| 2026-11-15 | `ATTRIBUTION.md` | Aturan aset upstream: setiap aset wajib tercatat di indeks (`cargo xtask assets`) | Tambah bagian baru "Cosmic fork assets" di **akhir** file. Saat sinkron upstream bentrok, pertahankan isi upstream lalu tempel ulang bagian ini di akhir | |

## Rebrand tampilan (Cosmic)

Semua perubahan teks, ikon, dan folder pengaturan pada file upstream dilakukan oleh **`cosmic/tools/rebrand.py`**. Daftar persis setiap penggantian ada di variabel `EDITS` di skrip itu.

Saat sinkron upstream:
1. Kalau salah satu file di bawah bentrok, ambil versi upstream (`git checkout --theirs <file>`), lalu jalankan `python -I cosmic/tools/rebrand.py`.
2. Kalau skrip melaporkan `FAIL`, berarti upstream mengubah baris itu. Perbarui anchor di `EDITS`, lalu jalankan lagi.
3. `python -I cosmic/tools/rebrand.py --check` memastikan semua perubahan masih terpasang.

| Tanggal | File | Alasan | Ringkasan perubahan |
| --- | --- | --- | --- |
| 2026-11-15 | `crates/host/src/app_dirs.rs` | Pengaturan tidak bercampur dengan EffectCraft | Folder `%APPDATA%\Cosmic`, `~/Library/Application Support/Cosmic`, `~/.config/cosmic`, portable `CosmicData`; test ikut disesuaikan |
| 2026-11-15 | `apps/effectcraft/src/main.rs` | Nama dan ikon jendela | Judul jendela, nama app eframe, judul kotak pesan; ikon dari `cosmic/assets/app-icon/` |
| 2026-11-15 | `apps/effectcraft/src/crash_report.rs` | Nama di pesan crash | "Cosmic stopped unexpectedly." |
| 2026-11-15 | `apps/effectcraft/build.rs` | Ikon dan info versi `.exe` Windows | `cosmic.ico`, ProductName, FileDescription, LegalCopyright |
| 2026-11-15 | `crates/engine/src/cmd/frontend.rs`, `crates/engine/src/menus.rs` | Menu About | "About Cosmic..." |
| 2026-11-15 | `crates/ui-egui/src/i18n.rs`, `crates/ui-egui/src/i18n/ui.rs` | Terjemahan menu About dan judul dialog About | Baris `app.about` (13 bahasa) dan "About EffectCraft" (11 bahasa): EffectCraft → Cosmic |
| 2026-11-15 | `crates/ui-egui/src/lib.rs` | Mendaftarkan modul baru | Satu baris `pub(crate) mod cosmic_brand;` (isi modul di `crates/ui-egui/src/cosmic_brand.rs`, file milik Cosmic) |
| 2026-11-15 | `crates/ui-egui/src/header.rs` | Lisensi merek ArtCraft mewajibkan fork membuang logo ArtCraft | Logo di bilah Tools dan About memakai `cosmic_brand::LOGO_PNG`; tooltip "About Cosmic" |
| 2026-11-15 | `crates/ui-egui/src/panels/dialogs.rs` | Isi dialog About | Judul, nama, tagline, dan deskripsi dari `cosmic_brand` ("based on EffectCraft by the ArtCraft team") |

## Catatan sinkron upstream

| Tanggal | Versi upstream | Konflik | Penyelesaian |
| --- | --- | --- | --- |
| | | | |
