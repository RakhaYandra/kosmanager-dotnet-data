# kosmanager-dotnet-data

Analytics pipeline KosManager: MySQL (read-only) → DuckDB marts + quality gates.
Data contoh fiktif (DB demo mengandung baris hasil QA-run — by design untuk
menunjukkan gates menangkap anomali volume, bukan data produksi).

## Marts

- `mart_occupancy` — total vs terisi
- `mart_arrears` — tunggakan per penghuni + max hari telat + open bills

## Gates (harus 0)

orphan bills · amount ≤ 0 · duplikat tenant+periode.

## Run

```bash
pip install duckdb
python3 pipeline.py  # butuh MySQL demo jalan (lihat kosmanager-dotnet)
```
