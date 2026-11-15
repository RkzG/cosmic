# Roadmap

Kerjakan berurutan. Setiap fase punya kriteria selesai; jangan lanjut sebelum kriteria terpenuhi dan Franz menyetujui.

## Fase 0: Persiapan fork

- [ ] Fork `storytold/effectcraft` di GitHub, clone ke laptop Franz.
- [ ] Tambahkan remote upstream: `git remote add upstream https://github.com/storytold/effectcraft.git`.
- [ ] Pasang toolchain Rust sesuai versi minimum di README upstream (saat dokumen ini ditulis: Rust 1.95 atau lebih baru), lalu build dari source mengikuti README atau CONTRIBUTING.
- [ ] Pastikan editor hasil build bisa dibuka, membuka `D:\Editing\EffectCraft\efectCraft.ecproj`, dan me-render.
- [ ] Baca `docs/architecture.md` upstream; catat di mana kode panel UI, sistem perintah, dan control channel berada. Tulis ringkasannya di `cosmic/docs/CODEBASE-MAP.md`.
- [ ] Nama aplikasi: **Cosmic**. Susun rencana penggantian nama tampilan (judul jendela, ikon, about) yang menyentuh sesedikit mungkin file inti, dan minta persetujuan Franz sebelum dijalankan.
- [ ] Pastikan baris `@cosmic/CLAUDE.md` sudah ada di akhir `CLAUDE.md` root, dan `cosmic/docs/UPSTREAM-PATCHES.md` sudah mencatatnya.
- [ ] Kode baru Cosmic di luar editor (layanan Go, worker Python) ditaruh di bawah folder `cosmic/`, misalnya `cosmic/ai-service/` dan `cosmic/analysis/`.

**Selesai jika:** fork ter-build di Windows, bisa membuka dan me-render proyek, dan peta kode tersedia.

## Fase 1: Format resep dan penerjemah

- [ ] Sempurnakan draft format resep di `ARCHITECTURE.md`; tulis JSON Schema-nya.
- [ ] Bangun layanan Go minimal yang membaca resep tulisan tangan dan menerjemahkannya jadi perintah EffectCraft (lewat MCP, CLI, atau script).
- [ ] Kamus efek awal: hard cut, crossfade, zoom punch, shake, flash, whip blur, speed ramp, teks pop-up, color grade.
- [ ] Setiap perubahan dicek ulang dengan membaca properti atau `render-frame`.

**Selesai jika:** resep tulisan tangan bisa menghasilkan proyek `.ecproj` yang benar dan ter-render, tanpa AI.

## Fase 2: Detektif efek (Fase 1 di VISION)

- [ ] Analisis video referensi: cut, beat, gerakan kamera (worker Python) + makna efek (model AI).
- [ ] Output: draft resep + daftar kebutuhan dengan status *sudah ada / bisa dipasang / tidak didukung*.
- [ ] Inventaris perangkat: font sistem, efek bawaan EffectCraft (`effectcraft-cli commands`), preset buatan sendiri.
- [ ] Pemantauan realtime: deteksi font atau preset baru yang dipasang.
- [ ] Alur umpan balik "plugin tidak tersedia" → AI mencari pengganti sesuai urutan di VISION.

**Selesai jika:** untuk 3 video referensi pilihan Franz, daftar kebutuhan dan draft resep dinilai masuk akal oleh Franz.

## Fase 3: Panel tahap di editor

- [ ] Panel baru di editor: daftar tahap, preview per tahap, kolom prompt per tahap.
- [ ] Sinkron dua arah: editan manual di timeline tercermin di tahap, dan sebaliknya.
- [ ] Fitur kunci per tahap atau per layer.
- [ ] Riwayat perubahan dengan penanda asal (AI atau manual).

**Selesai jika:** Franz bisa mengedit satu video 15–30 detik sepenuhnya lewat prompt per tahap, lalu merapikan manual tanpa ditimpa AI.

## Fase 4: Footage dan cerita (Fase 2 di VISION)

- [ ] Indeks footage: orang yang muncul, jenis shot, aksi, ekspresi.
- [ ] Simulasi kecukupan footage terhadap resep.
- [ ] Penentuan pemeran utama dan pemilihan klip per tahap lewat prompt.

## Fase 5: Perpustakaan pengganti plugin

- [ ] Preset racikan efek untuk plugin populer (mulai dari Saber-like dan slow motion halus ala Twixtor).
- [ ] Modul efek berbasis AI bila efek bawaan tidak cukup (kandidat: RIFE untuk interpolasi frame, SAM 2 untuk masking, Depth Anything untuk parallax 2.5D).
- [ ] Penyimpanan preset hasil racikan yang disetujui pengguna.

## Fase 6: Program render terpisah (proyek kedua)

Dikerjakan setelah editor stabil. Membaca file proyek dan me-render tanpa editor.

## Keputusan

| Keputusan | Status |
| --- | --- |
| Engine | Fork EffectCraft, perubahan dipisah dari kode inti |
| Hubungan dengan Patcher Video | Proyek berdiri sendiri |
| Model analisis video | Terbuka: Gemini saja, atau Gemini + Claude sebagai perencana |
| Efek berat prioritas pertama | Terbuka |
| Nama aplikasi | Cosmic (repo `RkzG/cosmic`) |
