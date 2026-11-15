# Setup di Windows

Langkah ini untuk Fase 0. Perintah build yang persis harus diambil dari README atau CONTRIBUTING upstream, karena bisa berubah antarversi.

## 1. Fork dan clone

1. Buka https://github.com/storytold/effectcraft, klik **Fork**.
2. Clone fork ke laptop:

```powershell
git clone https://github.com/<akun-github-franz>/effectcraft.git
cd effectcraft
git remote add upstream https://github.com/storytold/effectcraft.git
git fetch upstream
```

3. Salin folder `cosmic/` dari paket dokumen ini ke root repo. Jangan menimpa `CLAUDE.md`, `ROADMAP.md`, atau `docs/architecture.md` milik upstream (di Windows, `docs/ARCHITECTURE.md` dan `docs/architecture.md` dianggap file yang sama).
4. Tambahkan satu baris di **akhir** `CLAUDE.md` root milik upstream, supaya Claude Code ikut memuat panduan Cosmic:

```
@cosmic/CLAUDE.md
```

Ini satu-satunya perubahan pada file upstream di tahap ini, dan sudah tercatat di `cosmic/docs/UPSTREAM-PATCHES.md`. Kalau saat sinkron upstream baris ini bentrok, cukup pertahankan isi upstream lalu tambahkan baris ini lagi di akhir.

## 2. Toolchain

- Rust: pasang lewat https://rustup.rs, lalu pastikan versinya memenuhi minimum di README (saat dokumen ini ditulis: 1.95 atau lebih baru). Cek dengan `rustc --version`.
- Visual Studio Build Tools dengan komponen C++ (biasanya dibutuhkan Rust di Windows).
- Go versi terbaru untuk layanan AI.
- Python 3.10+ bila worker analisis dipakai.

## 3. Build

Ikuti instruksi build di README atau CONTRIBUTING upstream. Setelah berhasil, jalankan editor hasil build, buka proyek uji, dan render untuk memastikan semuanya jalan.

## 4. MCP untuk Claude Code

Untuk pengembangan, versi rilis di `F:\Program\effectCraft` tetap bisa dipakai sebagai pembanding. Setelah fork ter-build, arahkan pendaftaran MCP ke binary hasil build.

Daftarkan dengan scope user supaya berlaku di semua folder. Di PowerShell, `--` wajib diberi tanda kutip:

```powershell
claude mcp add --scope user effectcraft '--' "<path>\effectcraft-cli.exe" mcp --autosave --automation-read-root "D:\Editing\EffectCraft" --automation-write-root "D:\Editing\EffectCraft\mcp-test"

claude mcp add --scope user effectcraft-live '--' "<path>\effectcraft-cli.exe" mcp --bridge 9877 --automation-read-root "D:\Editing\EffectCraft" --automation-write-root "D:\Editing\EffectCraft\mcp-test"
```

Pendaftaran lama (scope lokal di `F:\Program\effectCraft`) dihapus dulu dari folder itu dengan `claude mcp remove effectcraft` dan `claude mcp remove effectcraft-live`.

Mode bridge butuh editor dibuka dengan `--control 9877`.

## 5. Rutinitas sinkron upstream

Setiap minggu, atau sebelum fitur besar:

```powershell
git fetch upstream
git checkout -b sync-upstream-<tanggal>
git merge upstream/main
# build, uji, lalu gabungkan ke branch utama
```

Gunakan `cosmic/docs/UPSTREAM-PATCHES.md` untuk memeriksa ulang setiap titik yang kita ubah di kode inti.
