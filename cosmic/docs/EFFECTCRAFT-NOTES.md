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
