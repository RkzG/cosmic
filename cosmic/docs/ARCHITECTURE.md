# Arsitektur

Dokumen ini adalah rancangan awal. Detail yang bergantung pada struktur kode EffectCraft harus dicek di repo (`docs/architecture.md` milik upstream) sebelum diimplementasikan.

## Komponen

```
┌─────────────────────────────────────────────────────────────┐
│ Editor (fork EffectCraft, Rust)                             │
│  ├─ kode inti upstream (sesedikit mungkin diubah)           │
│  └─ tambahan: panel AI, tampilan tahap, kunci layer         │
│        ▲ control channel (--control PORT) / bridge MCP      │
└────────┼────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────┐
│ Layanan AI (Go)                                             │
│  ├─ orkestrator: alur 4 fase, status kebutuhan, tahap       │
│  ├─ klien model AI (analisis video, perencana)              │
│  ├─ penerjemah resep → perintah EffectCraft                 │
│  ├─ inventaris: font sistem, efek bawaan, preset, plugin    │
│  └─ penyimpanan: riwayat, preferensi, preset (SQLite)       │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────┐
│ Worker analisis (Python, opsional)                          │
│  PySceneDetect (cut), librosa (beat), OpenCV (gerakan)      │
└─────────────────────────────────────────────────────────────┘
```

## Jalur komunikasi ke editor

Semua sudah tersedia di EffectCraft dan sudah diuji (lihat `EFFECTCRAFT-NOTES.md`):

| Jalur | Dipakai untuk |
| --- | --- |
| `effectcraft-cli mcp --autosave` | Kerja di belakang layar tanpa editor terbuka |
| `effectcraft --control PORT` + `effectcraft-cli mcp --bridge PORT` | Kerja langsung di editor yang terbuka; perubahan tampil realtime |
| `effectcraft-cli render` / `render-frame` | Render penuh, preview per tahap, cek frame |
| `effectcraft-cli script FILE.jsx` | JavaScript dengan model objek ala After Effects |
| `effectcraft-cli info` / `props` / `get` / `set` | Membaca dan mengubah properti secara langsung |

Opsi `--automation-read-root` dan `--automation-write-root` wajib dipakai untuk membatasi folder yang boleh diakses AI.

## Model AI

- **Analisis video**: model yang menerima video langsung (kandidat: Gemini). Output berupa JSON terstruktur dengan timestamp.
- **Perencana dan eksekutor**: Claude, karena sudah terbukti mengendalikan EffectCraft lewat MCP dengan benar.
- Keputusan final model masih terbuka (lihat ROADMAP).

## Format resep editan (draft)

Resep adalah rencana editan tingkat tinggi yang dihasilkan dari analisis video referensi. Resep **bukan** pengganti `.ecproj`; penerjemah mengubah resep menjadi perintah EffectCraft, dan `.ecproj` tetap menjadi sumber kebenaran.

```json
{
  "version": 1,
  "source": { "file": "referensi.mp4", "duration": 15.2 },
  "canvas": { "w": 1080, "h": 1920, "fps": 30 },
  "music": { "file": "lagu.mp3", "bpm": 128, "beats": [0.47, 0.94, 1.41] },
  "requirements": [
    { "kind": "font", "name": "Montserrat Black", "status": "missing" },
    { "kind": "effect", "name": "saber-like", "status": "substitute", "via": "preset:saber-like-v1" }
  ],
  "stages": [
    {
      "id": "stage-1",
      "start": 0.0,
      "end": 1.88,
      "intent": "hook: close-up pemeran utama, zoom punch di beat 1",
      "footage": { "clip": "klip03.mp4", "in": 2.1, "role": "pemeran-utama" },
      "effects": [{ "type": "zoom_punch", "at": 0.47, "scale": 1.15 }],
      "text": [{ "content": "WAIT FOR IT", "style": "pop_bold", "at": 0.47 }],
      "transition_out": { "type": "flash_white", "dur": 0.1 },
      "locked": false
    }
  ]
}
```

Prinsip:

- `stages` adalah unit yang dilihat dan di-prompt pengguna (Fase 3). Batas tahap mengikuti beat atau struktur video referensi.
- `locked: true` berarti AI tidak boleh mengubah tahap itu.
- Setiap tahap menyimpan pemetaan ke layer atau keyframe di `.ecproj`, supaya editan manual di timeline bisa dipetakan balik ke tahapnya.
- Format ini masih draft dan akan disempurnakan di ROADMAP Fase 1.

## Render

- Sementara: `effectcraft-cli render` dipanggil oleh layanan Go.
- Proyek kedua: program render terpisah yang membaca file proyek tanpa editor. Syarat dari sekarang: file proyek harus bisa di-render tanpa aplikasi editor.
