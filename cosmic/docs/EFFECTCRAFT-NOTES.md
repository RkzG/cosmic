# Catatan uji EffectCraft

Uji dilakukan 15 November 2026 dengan EffectCraft **0.24.1** (rilis Windows, 763 perintah, 308 efek), terpasang di `F:\Program\effectCraft`. Semua kriteria utama lulus.

## Hasil

| Aspek | Hasil |
| --- | --- |
| Render CLI | Lulus. Demo 300 frame 1080p selesai dalam 5,1 detik. Hasil proyek sendiri sama dengan render GUI. |
| MCP (headless) | Lulus. Claude membuat komposisi 1080×1920, zoom punch (100 → 115 → 100%), teks dengan Glow, mengecek frame di detik 3 dan 5, lalu render. |
| Mode bridge | Lulus. Perubahan dari Claude langsung tampil di editor yang terbuka. |
| Edit bersama | Lulus. Claude membaca posisi teks yang digeser manual, mengenali perubahan itu lewat riwayat undo, tidak menimpanya, dan tidak memasang shake dua kali. |

## Jebakan yang sudah ditemukan

- **Nama program Cosmic:** build lokal dipasang sebagai `D:\Coding\Cosmicin\cosmic.exe` dan `cosmic-cli.exe` (`cosmic/scripts/install-local.ps1`). Opsi CLI-nya sama dengan `effectcraft-cli`; contoh di bawah berlaku untuk keduanya.
- **CLI ikut terpasang di Windows** (`effectcraft-cli.exe` di folder instalasi) tapi tidak masuk PATH. Panggil dengan path lengkap atau `.\effectcraft-cli.exe` dari foldernya.
- **File proyek memakai opsi `--project`**, bukan argumen di akhir. Contoh:
  `effectcraft-cli render --project "D:\Editing\EffectCraft\efectCraft.ecproj" --comp "Comp 1" --out test.mp4`
- **`--comp` memakai nama komposisi**, bukan nama file. Cek dengan `effectcraft-cli info --project <file>`.
- **Path `--out` relatif** dihitung dari folder kerja saat ini.
- **PowerShell membuang `--` tanpa tanda kutip.** Pada `claude mcp add`, tulis `'--'`, kalau tidak opsi EffectCraft dibaca sebagai opsi Claude.
- **`claude mcp add` tanpa `--scope user`** hanya berlaku di folder tempat perintah dijalankan.
- **`--autosave` dan `--bridge` tidak bisa bersamaan**, jadi didaftarkan sebagai dua server MCP.
- **Perubahan lewat bridge bisa tidak tersimpan.** Warna teks yang diubah jadi biru sempat kembali putih sampai layer-nya dipilih dulu lalu diubah ulang. Setiap perubahan dari AI wajib diverifikasi.
- Footage landscape di komposisi portrait meninggalkan bar hitam; perlu skala (sekitar 177,8% untuk 16:9 ke 9:16).

## Kemampuan yang berguna untuk proyek ini

- `render-frame` untuk preview dan verifikasi per detik.
- `script FILE.jsx` menjalankan JavaScript dengan model objek ala After Effects (`app.project`, comps, layers, properties).
- `--automation-read-root` dan `--automation-write-root` untuk membatasi akses file AI.
- `bench --roto` untuk menguji Roto Brush (SAM2 / MobileSAM).
- `--gpu` untuk render dan benchmark dengan GPU.
- Riwayat undo bisa dibaca AI, berguna untuk membedakan perubahan manual dan perubahan AI.

## Build dan test di Windows (dicek 2026-11-15)

Perbandingan fork (`cosmic/fase-0`) dengan `upstream/main` (`7cbefaf7`) memakai worktree terpisah. Masalah di bawah ini terjadi juga di upstream tanpa perubahan Cosmic, jadi bukan bug Cosmic.

| Masalah | Fork | Upstream | Penyebab |
| --- | --- | --- | --- |
| Test `engine` `tests::blender::blender_export_defaults_and_script_escaping` gagal | gagal, lalu **lulus** setelah Python dipasang | gagal, pesan sama | Test memanggil `python3`. Di Windows, tanpa Python terpasang, `python3` hanyalah alias Microsoft Store (App execution alias) yang tidak menjalankan Python. **Solusi: pasang Python dari Microsoft Store** (dicek dengan Python 3.12.10: `python3 --version` berhasil dan test lulus). |
| Test `engine` `tests::lut_files::ocio_files_render_again_from_warm_caches` gagal | gagal | gagal, pesan sama | Test membandingkan path `luts/grade.cube` dengan path yang dicatat render, `luts\grade.cube`. Beda pemisah path di Windows, di kode test upstream. |
| `cargo xtask ci` gagal di tahap tests | gagal | (tidak dijalankan) | `xtask.exe` sedang berjalan saat tahap test membangun ulang workspace (termasuk `xtask`). Windows tidak bisa menimpa exe yang sedang dipakai ("failed to remove file … xtask.exe"). Pakai `cosmic/scripts/ci.ps1`. |
| Tahap `wasm` butuh target `wasm32-unknown-unknown`, contoh plug-in `posterize-bands` gagal tanpa target itu | - | - | Cosmic hanya desktop Windows; wasm dilewati (lihat `cosmic/CLAUDE.md`). Target sudah terpasang kalau perlu. |
| Test unit `ui-egui` sempat macet sekitar 18 menit (sekali, pukul 18:43) | tidak terulang | tidak terjadi | Tidak bisa direproduksi. Ulangan dengan `cargo test` biasa selesai dalam sekitar 6 detik di upstream (575 lulus) dan di fork setelah build bersih. Dengan `cargo nextest` di upstream: 575 lulus. Penyebab macet pertama tidak diketahui. |

Jebakan saat membandingkan:

- **Jangan berbagi folder `target` antara fork dan worktree upstream.** Strukturnya identik, jadi cargo menganggap hasil kompilasi satu tree masih berlaku untuk tree lain, dan test fork sempat tertaut ke `effectcraft-engine` milik upstream. Worktree upstream harus memakai `CARGO_TARGET_DIR` sendiri.
- `cargo clean -p <crate>` menghapus semua profil (debug dan release) untuk crate itu.
- Upstream menjalankan test lewat `cargo-nextest` 0.9.150 (`.config/nextest.toml` mewajibkan versi minimum ini), dengan test `ui-egui`, `gpu`, dan `sam2` berjalan satu per satu.
