# SIIB — Sistem Informasi Inventaris Barang

Dokumentasi teknis Sistem Informasi Inventaris Barang (tugas praktik: Menyusun Dokumentasi Teknis Sistem Informasi).

## Isi repositori

| Berkas / folder | Keterangan |
|:--|:--|
| `Dokumentasi-SIIB.pdf` | Dokumen final (PDF) |
| `Dokumentasi-SIIB.docx` | Versi yang dapat diedit |
| `sumber-editable/dokumentasi-sii.md` | Sumber Markdown dokumen |
| `sumber-editable/fix.py` | Skrip penata format DOCX |
| `diagram/` | Diagram use case, ERD, dan flowchart (`.dot` dan `.png`) |

## Membangun ulang dokumen

```bash
pandoc sumber-editable/dokumentasi-sii.md -o raw.docx --toc
python3 sumber-editable/fix.py        # menghasilkan Dokumentasi-SIIB.docx
soffice --headless --convert-to pdf Dokumentasi-SIIB.docx
```

Diagram dibuat dari berkas `.dot` dengan Graphviz: `dot -Tpng -o erd.png erd.dot`.

## Penyusun

[Nama Mahasiswa] — [NIM]
