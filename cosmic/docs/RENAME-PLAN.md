# Rencana penggantian nama tampilan: EffectCraft → Cosmic

Status: **disetujui Franz 2026-11-15, dikerjakan di branch `cosmic/rename-display`.** Penerapannya lewat `cosmic/tools/rebrand.py`; lihat `UPSTREAM-PATCHES.md`.

Belum ditangani (tugas lanjutan):
- **Pengecekan update** (`crates/ui-egui/src/lib.rs`, `UPDATE_APP` = `craft_update::suite::EFFECTCRAFT`): Cosmic masih memeriksa rilis EffectCraft dan bisa menawarkan update ke EffectCraft. Perlu dimatikan atau diarahkan ke rilis Cosmic.
- **Laporan bug** (`effectcraft_engine::links::ISSUES`) masih mengarah ke issue tracker upstream.
- Nama binary, installer, dan app id (pilihan 3 di bawah) ditunda sampai rilis.
- Label menu aplikasi macOS ("EffectCraft" di bilah menu Mac) belum diganti; Franz memakai Windows.

Keputusan Franz (2026-11-15):
- Folder pengaturan: **`%APPDATA%\Cosmic`** (beserta padanannya di macOS/Linux dan folder portable).
- Ikon aplikasi: **ikon sendiri**, bukan unicorn EffectCraft.
Disusun 2026-11-15 dari EffectCraft 0.24.1.

## Prinsip

- Hanya **tampilan** yang diganti: judul jendela, About, logo, dan teks yang dilihat pengguna.
- **Tidak** mengganti nama crate (`effectcraft-*`), nama binary, ekstensi `.ecproj`, atau id perintah. Mengganti semua itu akan bentrok dengan setiap sinkron upstream.
- Setiap file inti yang disentuh dicatat di `UPSTREAM-PATCHES.md`.
- Nama dan ikon Cosmic dikumpulkan di satu modul baru (misalnya `crates/ui-egui/src/cosmic_brand.rs`), sehingga patch di file upstream hanya berupa pemanggilan ke modul itu.

## Wajib (lisensi merek ArtCraft)

Menurut `docs/brand/LICENSE-brand.txt`, versi modifikasi yang **didistribusikan atau dipublikasikan** harus membuang logo ArtCraft (atau menggantinya dengan logo sendiri), dan tidak boleh tampil sebagai produk ArtCraft. Selama fork hanya dipakai pribadi dan belum dirilis, logo masih boleh ada, tapi sebaiknya langsung diganti.

| Lokasi | Isi sekarang | Usulan |
| --- | --- | --- |
| `crates/ui-egui/src/header.rs:906` | `ARTCRAFT_MARK` (logo ArtCraft dari `docs/brand/`), dipakai di bilah Tools (`header.rs:41`) dan dialog About (`panels/dialogs.rs:400`) | `paint_logo` membaca logo Cosmic dari modul baru |
| `README.md` | Logo ArtCraft di bagian atas | Ditangani terpisah: README Cosmic sendiri, atau README upstream dibiarkan dan Cosmic punya `cosmic/README.md` |

Logo Cosmic harus karya asli atau berlisensi terbuka, dengan file `.attribution` dan baris di `ATTRIBUTION.md`. **Franz perlu menyediakan atau memilih logo.**

## Teks yang terlihat pengguna

| Lokasi | Sekarang | Usulan |
| --- | --- | --- |
| `apps/effectcraft/src/main.rs:275` | Judul jendela `EffectCraft` | `Cosmic` |
| `apps/effectcraft/src/main.rs:299, 522` | Judul dialog pesan | `Cosmic` |
| `crates/engine/src/cmd/frontend.rs:20` | Label perintah `About EffectCraft...` | `About Cosmic...` |
| `crates/engine/src/menus.rs:536, 1326` | Menu `About EffectCraft...` | `About Cosmic...` (beserta terjemahannya di `crates/ui-egui/src/i18n`) |
| `crates/ui-egui/src/header.rs:43-45` | Tooltip `About EffectCraft` | `About Cosmic` |
| `crates/ui-egui/src/header.rs:316` | Tombol `EffectCraft on GitHub` / `getartcraft.com` | Arahkan ke `RkzG/cosmic`, atau sembunyikan |
| Dialog About (`panels/dialogs.rs`) | Nama, kredit | `Cosmic`, dengan teks polos "Based on EffectCraft by the ArtCraft team" (diizinkan lisensi merek) |
| `apps/effectcraft/src/file_dialogs.rs` | Filter `EffectCraft Project` | Biarkan dulu. Formatnya tetap `.ecproj` |

## Pilihan yang perlu diputuskan Franz

1. **Folder pengaturan.** ✅ Diputuskan: `%APPDATA%\Cosmic`. Sekarang `%APPDATA%\EffectCraft` (`crates/host/src/app_dirs.rs:85`, juga macOS `:82`, Linux `:87`, folder portable `EffectCraftData` `:21`, dan penanda portable `:19`). Patch kecil di satu file supaya pengaturan tidak bercampur dengan EffectCraft rilis di `F:\Program\effectCraft`.
2. **Ikon aplikasi.** ✅ Diputuskan: ikon sendiri. Ikon dipakai di `crates/ui-egui/src/lib.rs:16` dan `apps/effectcraft/src/main.rs:54,58` (`include_bytes!` dari `assets/app-icon/`). File ikon Cosmic ditaruh di folder baru (misalnya `cosmic/assets/app-icon/`) dengan file `.attribution`. Desain: galaksi spiral yang lengan luarnya membentuk huruf C. Master vector sudah ada di `cosmic/assets/app-icon/cosmic.svg` (dibuat oleh `make_icon.py`). **Masih perlu:** render PNG (128, 256, 512, 1024) dan `.ico` saat rencana ini dijalankan.
3. **Nama binary dan installer** (`effectcraft.exe`, `packaging/windows/effectcraft.wxs`, app id `ai.storyteller.effectcraft`). Usulan: ditunda sampai Cosmic siap dirilis. Untuk pemakaian lokal belum perlu.
4. **Tautan komunitas** (Discord, getartcraft.com) di menu Help. Usulan: tetap tampil di bawah "Tentang EffectCraft", tapi tidak dijadikan tautan dukungan Cosmic.

## Urutan pengerjaan setelah disetujui

1. Buat modul `cosmic_brand` (nama, logo, tautan) beserta test-nya.
2. Ganti logo, judul jendela, dan About lewat modul itu.
3. (Opsional) Ganti folder pengaturan.
4. Jalankan `cargo xtask ci`, buka aplikasi, dan periksa judul, About, dan bilah Tools.
5. Catat setiap file di `UPSTREAM-PATCHES.md`.
