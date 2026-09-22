"""KosManager analytics: MySQL (read-only) -> DuckDB marts + quality gates."""
import duckdb

con = duckdb.connect("/home/rakha/Work/kos/data/repo/kosmanager.duckdb")
con.execute("INSTALL mysql; LOAD mysql;")
con.execute("ATTACH 'host=127.0.0.1 port=3308 user=kos password=kospass database=kosmanager' AS kos (TYPE mysql)")

for tbl in ["Rooms", "Tenants", "Bills", "Payments", "NotificationLogs"]:
    con.execute(f"CREATE OR REPLACE TABLE raw_{tbl.lower()} AS SELECT * FROM kos.{tbl}")
    n = con.execute(f"SELECT COUNT(*) FROM raw_{tbl.lower()}").fetchone()[0]
    print(f"raw_{tbl.lower()}: {n} rows")

gates = {
    "orphan bills": "SELECT COUNT(*) FROM raw_bills b LEFT JOIN raw_tenants t ON t.Id=b.TenantId WHERE t.Id IS NULL",
    "amount <= 0": "SELECT COUNT(*) FROM raw_bills WHERE Amount <= 0",
    "duplikat tenant+periode": "SELECT COUNT(*) FROM (SELECT TenantId, Period, COUNT(*) c FROM raw_bills GROUP BY TenantId, Period HAVING c>1)",
}
for name, q in gates.items():
    n = con.execute(q).fetchone()[0]
    print(f"gate {name}: {n}")
    assert n == 0, name

con.execute("""
CREATE OR REPLACE TABLE mart_occupancy AS
SELECT (SELECT COUNT(*) FROM raw_rooms) AS total,
       (SELECT COUNT(*) FROM raw_rooms WHERE Status='isi') AS filled
""")
con.execute("""
CREATE OR REPLACE TABLE mart_arrears AS
SELECT t.Name AS tenant, SUM(b.Amount) AS total,
       MAX(DATE_DIFF('day', b.DueDate, CURRENT_DATE)) AS max_days_late,
       COUNT(*) AS open_bills
FROM raw_bills b JOIN raw_tenants t ON t.Id = b.TenantId
WHERE b.Status != 'paid'
GROUP BY t.Name ORDER BY total DESC
""")
print(con.execute("SELECT * FROM mart_occupancy").fetchall())
for r in con.execute("SELECT * FROM mart_arrears").fetchall():
    print(r)
con.close()
print("marts OK")
