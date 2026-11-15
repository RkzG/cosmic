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

## 4. Pasang build lokal dan MCP untuk Claude Code

Setelah build release, jalankan:

```powershell
cargo build --release -p effectcraft -p effectcraft-cli
powershell -ExecutionPolicy Bypass -File cosmic/scripts/install-local.ps1
```

Skrip ini:

- menyalin `targetelease\effectcraft.exe` dan `effectcraft-cli.exe` ke `D:\Coding\Cosmicin` sebagai **`cosmic.exe`** dan **`cosmic-cli.exe`** (di `targetelease` namanya tetap nama Cargo upstream, supaya sinkron upstream tetap mudah);
- mendaftarkan ulang server MCP scope user **`cosmic`** (headless, `--autosave`) dan **`cosmic-live`** (bridge ke port **9878**) ke `cosmic-cli.exe`.

Mode `cosmic-live` butuh Cosmic dibuka dengan `D:\Coding\Cosmicin\cosmic.exe --control 9878`.

Windows tidak bisa menimpa exe yang sedang berjalan. Kalau skrip menolak karena `cosmic.exe` atau `cosmic-cli.exe` masih jalan, tutup aplikasinya dan sesi Claude Code yang memakai server MCP-nya, lalu ulangi.

Pendaftaran **`effectcraft`** dan **`effectcraft-live`** (scope lokal di `F:\Program\effectCraft`, versi rilis) tetap mengarah ke EffectCraft rilis sebagai pembanding; skrip tidak menyentuhnya. Di PowerShell, `--` pada `claude mcp add` wajib diberi tanda kutip (`'--'`).

## 5. Rutinitas sinkron upstream

Setiap minggu, atau sebelum fitur besar:

```powershell
git fetch upstream
git checkout -b sync-upstream-<tanggal>
git merge upstream/main
# build, uji, lalu gabungkan ke branch utama
```

Gunakan `cosmic/docs/UPSTREAM-PATCHES.md` untuk memeriksa ulang setiap titik yang kita ubah di kode inti.
