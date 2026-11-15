# CLAUDE.md — Cosmic

## Bahasa

Selalu balas Franz dalam Bahasa Indonesia, termasuk ringkasan progres, rencana, dan pertanyaan. Kode, komentar kode, nama variabel, dan pesan commit tetap dalam bahasa Inggris sesuai aturan upstream.

Panduan Cosmic untuk Claude Code. File ini berada di `cosmic/CLAUDE.md` dan dimuat lewat baris `@cosmic/CLAUDE.md` di `CLAUDE.md` root milik upstream. Baca file ini dulu, lalu dokumen di `cosmic/docs/` sesuai kebutuhan tugas.

**Penting soal nama file:** `CLAUDE.md`, `ROADMAP.md`, dan `docs/architecture.md` di root repo adalah milik EffectCraft upstream. Jangan ditimpa atau diedit (kecuali satu baris import di `CLAUDE.md` root, lihat `cosmic/docs/UPSTREAM-PATCHES.md`). `ROADMAP.md` upstream berisi rencana EffectCraft; rencana Cosmic ada di `cosmic/docs/ROADMAP.md`. Semua dokumen dan catatan Cosmic ditaruh di folder `cosmic/`.

## Tentang proyek

Repo ini adalah **fork dari [EffectCraft](https://github.com/storytold/effectcraft)** (editor motion graphics dan compositing open source ala After Effects, ditulis dengan Rust, lisensi MIT/Apache-2.0).

Tujuannya: membangun **editor video lengkap dengan AI sebagai rekan kerja di dalamnya**. Pengguna mengunggah video referensi (TikTok, YouTube, dll.) sebagai _template_. AI menganalisis efek, pacing, dan alur ceritanya, lalu membuat ulang editan itu memakai footage milik pengguna. Pengguna mengarahkan lewat **prompt per tahap**, tapi tetap bisa mengedit manual di timeline, keyframe, dan panel efek seperti editor biasa.

Pemilik proyek: Franz, backend developer Go dengan pengalaman editing di Premiere Pro, After Effects, dan Alight Motion. Komunikasi dengan Franz dalam **Bahasa Indonesia**, singkat dan jelas.

Dokumen detail:

| File                               | Isi                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------- |
| `cosmic/docs/VISION.md`            | Visi dan 9 kebutuhan fitur, dikelompokkan jadi 4 fase alur kerja                |
| `cosmic/docs/ARCHITECTURE.md`      | Komponen sistem, cara AI berkomunikasi dengan editor, draft format resep editan |
| `cosmic/docs/ROADMAP.md`           | Urutan pengerjaan per fase beserta kriteria selesai                             |
| `cosmic/docs/SETUP.md`             | Langkah menyiapkan fork, build, dan alat pendukung di Windows                   |
| `cosmic/docs/EFFECTCRAFT-NOTES.md` | Hasil uji EffectCraft dan jebakan yang sudah ditemukan                          |
| `cosmic/docs/UPSTREAM-PATCHES.md`  | Daftar setiap perubahan pada kode inti EffectCraft (wajib diperbarui)           |

## Sebelum mengubah kode

1. Baca dokumentasi asli EffectCraft yang ada di repo ini: `CLAUDE.md` root, `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `docs/architecture.md`, `docs/agents.md`, `docs/control-protocol.md`, dan `docs/gaps.md`. Ikuti aturan di `AGENTS.md` milik upstream kecuali bertentangan dengan file ini.
2. Jangan menebak nama crate, modul, perintah build, atau struktur folder. Cek langsung di repo.
3. Untuk tugas besar, susun rencana singkat dulu dan minta persetujuan Franz sebelum menulis kode.

## Aturan utama fork

Proyek upstream bergerak sangat cepat (commit pertama 1 Oktober 2026, sudah v0.24 pertengahan November 2026). Supaya update dari upstream tetap mudah digabung:

- **Fitur baru ditaruh di file atau modul baru.** Hindari mengubah file inti EffectCraft.
- Kalau file inti terpaksa diubah, buat perubahannya sekecil mungkin (misalnya satu titik pemanggilan ke modul baru), lalu **catat di `cosmic/docs/UPSTREAM-PATCHES.md`**: file, alasan, dan ringkasan perubahan.
- Jangan merapikan, memformat ulang, atau me-refactor kode upstream yang tidak terkait tugas.
- Pertahankan `LICENSE*`, `NOTICE`, dan `ATTRIBUTION.md`. Nama dan merek "EffectCraft" punya aturan tersendiri, jadi aplikasi ini bernama **Cosmic** (repo `RkzG/cosmic`).
- Penggabungan upstream dilakukan rutin: `git fetch upstream` lalu `git merge upstream/main` di branch terpisah, uji, baru gabung ke branch utama.
- Kerja selalu di branch `cosmic/<nama-fase-atau-tugas>`, commit per langkah kecil, lalu push branch itu ke `origin`. **Berhenti di situ: jangan membuat PR dan jangan merge.** Setelah push, berikan Franz link compare `https://github.com/RkzG/cosmic/compare/main...<nama-branch>` dan draft deskripsi PR, supaya Franz yang membuat PR ke `main`. Jangan pernah membuat PR ke `storytold/effectcraft`.

## Build dan pemeriksaan

Aturan ini **menggantikan** aturan CI di `AGENTS.md` upstream ("`cargo xtask ci` sebelum setiap commit").

- Cosmic hanya menargetkan **desktop Windows**, jadi pemeriksaan wasm (`cargo xtask wasm`) dilewati.
- Saat kerja harian, cukup build dan jalankan test pada crate yang diubah (`cargo test -p <crate>`), ditambah `cargo fmt --check`.
- Pemeriksaan lengkap tanpa wasm, `powershell -ExecutionPolicy Bypass -File cosmic/scripts/ci.ps1`, hanya dijalankan **sekali sebelum Franz merge PR sebuah fase**. Skrip ini menjalankan tahap-tahap `cargo xtask ci` satu per satu (fmt, clippy, test lewat cargo-nextest, test GPU, doctest, pdf-deps, lock-patches, layers, assets) ditambah `rebrand.py --check`. Jangan memakai `cargo xtask ci` langsung di Windows: tahap test-nya gagal karena membangun ulang `xtask.exe` yang sedang berjalan.
- Test `ui-egui` dijalankan lewat `cargo nextest`, bukan `cargo test` biasa, karena test yang memakai GPU harus berjalan satu per satu (`.config/nextest.toml`).

## Pembagian bahasa dan komponen

- **Rust**: hanya untuk bagian di dalam editor (panel AI, tampilan tahap, fitur kunci layer, modul efek baru).
- **Go**: layanan AI (orkestrasi, pemanggilan model, penyusunan resep, riwayat dan preferensi). Ini bahasa utama Franz, jadi logika sebanyak mungkin ditaruh di sini.
- **Python**: worker analisis video (deteksi cut, beat, gerakan) bila library-nya tidak ada padanan di Go.
- Komunikasi layanan Go ke editor memakai jalur yang sudah ada: MCP (`effectcraft-cli mcp`), control channel (`--control PORT`), CLI, atau `script FILE.jsx`. Jangan membuat protokol baru selama yang lama cukup.

## Prinsip AI sebagai rekan kerja

- AI dan pengguna mengedit **satu file proyek yang sama**. Tampilan tahap dan timeline hanyalah dua cara melihat data yang sama.
- Sebelum bertindak, AI **selalu membaca kondisi proyek terbaru**. Jangan pernah menimpa editan manual dengan versi lama.
- Setiap perubahan dari AI **wajib dicek ulang** (baca kembali propertinya atau render frame). Saat uji, satu perubahan warna lewat bridge sempat tidak tersimpan sampai layer dipilih.
- Bagian yang dikunci pengguna tidak boleh diubah AI kecuali diminta eksplisit.
- Semua perubahan tercatat dan bisa di-undo.

## Lingkungan Franz

- Windows, laptop dengan RTX 4070 (laptop) dan RAM 32 GB.
- EffectCraft rilis terpasang di `F:\Program\effectCraft` (CLI: `effectcraft-cli.exe`, belum masuk PATH).
- Proyek uji ada di `D:\Editing\EffectCraft\` dan `D:\Editing\EffectCraft\mcp-test\`.
- Shell utama PowerShell. Lihat jebakan PowerShell di `cosmic/docs/EFFECTCRAFT-NOTES.md`.

## Gaya kerja

- Jelaskan ke Franz dengan paragraf singkat, sedikit jargon.
- Setelah selesai satu tugas: apa yang berubah, cara mengujinya, dan apa langkah berikutnya.
- Kalau ada keputusan desain yang bisa ke dua arah, tanyakan dulu.
