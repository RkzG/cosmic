# Visi dan kebutuhan

## Visi

Editor video lengkap ala After Effects dengan AI sebagai rekan kerja di dalamnya. Video referensi dipakai sebagai template; AI memahami efek, pacing, dan alur ceritanya, lalu membuat ulang editan itu dengan footage pengguna. Pendekatan utamanya **prompting per tahap**, bukan mengatur keyframe manual, tapi kontrol manual tetap utuh.

Masalah yang diselesaikan: Franz sering melihat editan keren di TikTok atau YouTube. Kadang ia tahu efek atau plugin apa yang dipakai, kadang tidak. Program ini harus bisa memberi tahu kebutuhannya, lalu membantu membuat ulang editan itu.

## Alur kerja (9 kebutuhan dalam 4 fase)

### Fase 1: Persiapan

1. **Analisis video sumber.** Setelah video referensi diunggah, AI menganalisisnya dan mengeluarkan daftar kebutuhan yang belum ada di perangkat: font, efek, plugin, library, dll.
2. **Umpan balik kebutuhan.** Kalau ada plugin atau efek yang tidak tersedia atau tidak bisa diunduh, pengguna memberi tahu AI. AI lalu mencari solusi lain, termasuk mengedit tanpa plugin tersebut.
3. **Deteksi otomatis realtime.** Saat pengguna memasang kebutuhan, program terus mengecek apakah efek, font, dll. sudah terpasang.

Status setiap kebutuhan dibagi tiga: *sudah ada*, *bisa dipasang*, *tidak didukung (pakai alternatif)*.

### Fase 2: Footage dan cerita

4. **Simulasi footage.** Setelah footage diunggah, AI mengecek apakah footage cukup untuk template itu atau perlu footage tambahan (bisa lebih dari satu klip).
5. **Pemilihan footage dan cerita.** AI harus bisa memilih potongan footage yang tepat untuk tiap segmen dan menentukan pemeran utama, sesuai video referensi dan prompt pengguna. Ini membutuhkan indeks footage: siapa yang muncul, jenis shot, aksi, ekspresi.

### Fase 3: Editing per tahap (inti pengalaman pengguna)

6. **Prototype per tahap.** Pengguna bisa melihat editan dari detik berapa ke berapa, mengecek efek, sinkronisasi beat lagu, dan durasi, lalu memperbaikinya.
7. **Tahapan dinamis.** AI membagi video jadi beberapa tahap per beberapa detik atau beberapa beat, jumlahnya tergantung video. Tiap tahap bisa diputar ulang dan diperbaiki lewat prompt, tanpa mengatur keyframe manual.

### Fase 4: Fitur dan render

8. **Fitur editor lengkap.** Cut, efek audio, masking, tracking, 3D, partikel, dll. Dasarnya fork EffectCraft (308 efek di v0.24.1).
9. **Render.** Sementara di program sendiri. Proyek kedua nanti adalah program khusus render yang membaca file proyek tanpa membuka editor. Media Encoder tidak bisa membaca format proyek ini.

## Strategi plugin yang tidak didukung

AI mengenali **ciri visual** efek, bukan nama plugin, sehingga berlaku untuk plugin apa pun. Contoh: Saber = garis cahaya mengikuti bentuk objek + inti putih dengan pendaran berwarna + distorsi bergerak + animasi muncul sepanjang garis.

Urutan jalur pengganti:

1. Plugin pengganti yang terpasang dan mirip (plugin OFX seperti Twixtor bisa dipakai kalau engine mendukung OFX).
2. Racikan efek bawaan, misalnya Saber = Roto Brush + stroke + glow bertumpuk + noise displacement.
3. Efek custom tulisan AI (shader kecil).
4. Disederhanakan, dengan persetujuan pengguna.

Racikan yang memuaskan disimpan sebagai preset ("Saber-like v1") supaya bisa dipakai ulang.

## Di luar cakupan awal

- Mengunduh video langsung dari TikTok atau YouTube (masalah ToS). Mulai dengan upload file lokal.
- Membuka file `.aep` After Effects atau memuat plugin After Effects.
- Versi mobile.
