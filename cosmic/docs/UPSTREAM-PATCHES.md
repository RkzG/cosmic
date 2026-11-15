# Perubahan pada kode inti upstream

Setiap perubahan pada file milik EffectCraft upstream wajib dicatat di sini. Tujuannya: saat menggabungkan update dari upstream, kita tahu persis titik mana yang perlu dicek ulang.

Fitur baru sebaiknya berada di file atau modul baru, sehingga daftar ini tetap pendek.

## Format

| Tanggal | File | Alasan | Ringkasan perubahan | Commit |
| --- | --- | --- | --- | --- |
| 2026-11-15 | `CLAUDE.md` (root) | Supaya Claude Code memuat panduan Cosmic | Tambah satu baris `@cosmic/CLAUDE.md` di akhir file | |
| 2026-11-15 | `ATTRIBUTION.md` | Aturan aset upstream: setiap aset wajib tercatat di indeks (`cargo xtask assets`) | Tambah bagian baru "Cosmic fork assets" di **akhir** file. Saat sinkron upstream bentrok, pertahankan isi upstream lalu tempel ulang bagian ini di akhir | |

## Rebrand tampilan (Cosmic)

Semua perubahan teks, ikon, dan folder pengaturan pada file upstream (**27 file**) dilakukan oleh **`cosmic/tools/rebrand.py`**. Ditambah 2 file yang diubah manual (`CLAUDE.md`, `ATTRIBUTION.md`, tabel di atas), totalnya 29 file upstream. Pengujian 2026-11-15: ke-27 file dikembalikan ke versi `upstream/main`, skrip dijalankan, hasilnya identik. Daftar persis setiap penggantian ada di variabel `EDITS` di skrip itu.

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
| 2026-11-15 | `crates/ui-egui/src/i18n.rs`, `crates/ui-egui/src/i18n/ui.rs` | Terjemahan menu About dan judul dialog About | Baris `app.about` (13 bahasa) dan "About EffectCraft" (11 bahasa): EffectCraft → Cosmic. Di `ui.rs` juga dihapus 11 blok terjemahan deskripsi About lama ("A clean-room, open-source compositor…"), karena test i18n menolak baris katalog yang tidak dipakai |
| 2026-11-15 | `crates/ui-egui/src/lib.rs` | Mendaftarkan modul baru | Satu baris `pub(crate) mod cosmic_brand;` (isi modul di `crates/ui-egui/src/cosmic_brand.rs`, file milik Cosmic) |
| 2026-11-15 | `crates/ui-egui/src/header.rs` | Lisensi merek ArtCraft mewajibkan fork membuang logo ArtCraft | Logo di bilah Tools dan About memakai `cosmic_brand::LOGO_PNG`; tooltip "About Cosmic" |
| 2026-11-15 | `crates/ui-egui/src/panels/dialogs.rs` | Isi dialog About | Judul, nama, tagline, dan deskripsi dari `cosmic_brand` ("based on EffectCraft by the ArtCraft team") |
| 2026-11-15 | `crates/ui-egui/src/panels/unsaved.rs` | Judul jendela setelah proyek dibuka | `"Cosmic - <proyek>"` lewat `cosmic_brand::NAME` |
| 2026-11-15 | `crates/ui-egui/tests/it/ui_window_title.rs` | Test judul jendela mengikuti nama baru | Awalan yang dicek: `"Cosmic - "` |
| 2026-11-15 | `crates/engine/src/home/links.rs` | Link Help, About, Home ke repo Cosmic | `GITHUB` dan `ISSUES` ke `RkzG/cosmic`; konstanta baru `UPSTREAM` ke `storytold/effectcraft` |
| 2026-11-15 | `crates/engine/src/cmd/help.rs` | Label perintah Help | "Cosmic Help...", "Cosmic on GitHub", `help.appPage` menjadi "Based on EffectCraft" dan membuka `UPSTREAM`; `help.discord` dan `help.website` tidak lagi menyatakan menu Help (test menuntut menu yang dinyatakan ada di pohon menu), perintahnya tetap ada |
| 2026-11-15 | `crates/engine/src/tests/session.rs` | Test URL Help mengikuti link baru | `help.github` mengarah ke `https://github.com/RkzG/cosmic`; dokumentasi Help dicek dengan awalan `https://github.com/RkzG/cosmic/blob/main/` |
| 2026-11-15 | `crates/engine/src/tests/aep_import.rs` | Test urutan menu File ▸ Import | "Cosmic Project..." |
| 2026-11-15 | `crates/engine/src/menus.rs` (lanjutan) | Menu Help dan File | "Cosmic Help...", File ▸ Import ▸ "Cosmic Project..."; entri Discord dan ArtCraft Website dihapus; "Based on EffectCraft", "Cosmic on GitHub" |
| 2026-11-15 | `crates/engine/src/cmd/import_project.rs` | Label perintah impor | "Cosmic Project..." |
| 2026-11-15 | `crates/ui-egui/src/i18n.rs` (lanjutan) | Terjemahan menu | Baris `help.github`, `help.docs`, `file.importProject` diganti ke Cosmic (13 bahasa); baris `help.discord`, `help.website`, `help.appPage` dihapus |
| 2026-11-15 | `crates/ui-egui/src/i18n/ui.rs` (lanjutan) | Terjemahan panel | Welcome, "Cosmic project", "Cosmic on GitHub", Settings, Learn diganti ke Cosmic; baris Discord, ArtCraft website, "More ArtCraft apps", "EffectCraft home page", "Source code on GitHub" dihapus |
| 2026-11-15 | `crates/ui-egui/src/panels/home.rs` | Layar Welcome | "Welcome to Cosmic", jenis "Cosmic project" di Recent (termasuk test-nya); Community berisi "Cosmic on GitHub" dan "Based on EffectCraft"; daftar aplikasi ArtCraft dihapus; `home.help.discord` dihapus dari daftar kontrol di test |
| 2026-11-15 | `crates/ui-egui/src/header.rs` (lanjutan) | Toolbar | Tombol Discord dan website dihapus; tombol GitHub "Cosmic on GitHub" |
| 2026-11-15 | `crates/ui-egui/tests/it/ui_panels.rs` | Tombol Discord tidak ada lagi | Test `discord_pill_fits_its_label` dihapus |
| 2026-11-15 | `crates/ui-egui/src/panels/dialogs.rs` (lanjutan) | Link di About | Dua link: "Cosmic on GitHub" dan "Based on EffectCraft" |
| 2026-11-15 | `apps/effectcraft/src/file_dialogs.rs` | Dialog buka/simpan | Filter "Cosmic Project" (ekstensi tetap `.ecproj`) |
| 2026-11-15 | `apps/effectcraft/src/main.rs` (lanjutan) | Pesan GPU dan gagal buka jendela | Nama Cosmic; laporan ke `https://github.com/RkzG/cosmic/issues` |
| 2026-11-15 | `apps/effectcraft/build.rs` (lanjutan) | Info `.exe` sesuai nama terpasang | OriginalFilename `cosmic.exe`, InternalName `cosmic` |
| 2026-11-15 | `crates/ui-egui/src/panels/settings.rs` | Teks Settings (termasuk test-nya) | "Restart Cosmic to finish", "Needs a newer Cosmic", "Cosmic didn't quit normally last time.", "Cosmic keeps …", "Stored, but not used by Cosmic yet" |
| 2026-11-15 | `crates/ui-egui/src/panels/learn.rs` | Tab Learn | "Hands-on tutorials that run inside Cosmic." |
| 2026-11-15 | `crates/engine/src/settings/autosave.rs` | Folder di disk | `Cosmic Auto-Save` |
| 2026-11-15 | `crates/engine/src/system/logging.rs` | File log | `Cosmic Log.txt` |
| 2026-11-15 | `crates/ui-egui/src/panels/effects_presets.rs`, `crates/ui-egui/tests/it/ui_presets_folder.rs` | Folder preset | `Documents\Cosmic\Presets` |

## Catatan sinkron upstream

| Tanggal | Versi upstream | Konflik | Penyelesaian |
| --- | --- | --- | --- |
| | | | |
