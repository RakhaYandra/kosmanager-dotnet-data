# kosmanager-dotnet-data

[![ci](https://github.com/RakhaYandra/kosmanager-dotnet-data/actions/workflows/ci.yml/badge.svg)](https://github.com/RakhaYandra/kosmanager-dotnet-data/actions)

> Ekosistem: [api](https://github.com/RakhaYandra/kosmanager-dotnet) · [web](https://github.com/RakhaYandra/kosmanager-dotnet-web) · [docs](https://github.com/RakhaYandra/kosmanager-dotnet-docs/releases) · [qa](https://github.com/RakhaYandra/kosmanager-dotnet-qa) · [data](https://github.com/RakhaYandra/kosmanager-dotnet-data) · [ops](https://github.com/RakhaYandra/kosmanager-dotnet-ops)

Analytics pipeline KosManager: MySQL (read-only) → DuckDB marts + quality gates.
Data contoh fiktif.

## Purpose, Output & Expectations

**Purpose.** Jawab tanpa query operasional: berapa okupansi, siapa menunggak
berapa + sejak kapan — dari snapshot read-only, bukan DB produksi.

**Output.** 2 marts DuckDB (`mart_occupancy`, `mart_arrears`) + 3 quality gates
yang menggagalkan pipeline bila > 0.

**Expectations.** Setiap run mencetak jumlah baris + hasil gates; marts bisa
dibuka di analisis lanjutan tanpa menyentuh MySQL.

## Features

| Fitur | Deskripsi |
|---|---|
| Extract read-only | `mysql_scan` via ekstensi DuckDB MySQL; tanpa tulis ke operasional. |
| Quality gates | orphan bills · amount ≤ 0 · duplikat tenant+periode (assert 0). |
| Marts | okupansi (total vs terisi) · tunggakan per penghuni + max hari telat + open bills. |

## Insight (run seed fiktif)

Okupansi 5/6 · tunggakan terbesar contoh: Maya Citra Rp2.400.000 (2 open bills).
(DB demo dapat mengandung baris QA-run; gates tetap harus 0.)

## How It Works

```text
MySQL kosmanager --(mysql_scan, read-only)--> raw_* --> gates (assert) --> mart_*
```

Env: `KOS_MYSQL_HOST` (default 127.0.0.1), `KOS_MYSQL_PORT` (default 3308),
`KOS_DUCKDB` (default `./kosmanager.duckdb`).

## Cara run 5 menit

```bash
pip install duckdb pymysql
python3 pipeline.py  # butuh MySQL demo jalan (lihat kosmanager-dotnet)
```

## Struktur

```
pipeline.py       # extract + gates + marts
requirements.txt  # duckdb
kosmanager.duckdb # artefak lokal (tidak untuk produksi)
```

## Verifikasi

Gates mencetak `0` semua + `marts OK`; CI menjalankan pipeline vs MySQL
ephemeral + seed setiap push.
