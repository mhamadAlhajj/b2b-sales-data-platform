"""
Protection tests for the dev and prod PostgreSQL servers.
Reads all settings from the .env file in the project root.

Run:  python test_protection.py
Needs: pip install psycopg2-binary python-dotenv
"""
import os
import sys

import psycopg2
from dotenv import load_dotenv

load_dotenv()

HOST = "localhost"
TEST_TABLE = "t_protection_test"


def cfg(env):
    """Connection settings for 'DEV' or 'PROD' (admin/owner account)."""
    return dict(
        host=HOST,
        port=int(os.environ[f"POSTGRES_PORT_{env}"]),
        user=os.environ[f"POSTGRES_USER_{env}"],
        password=os.environ[f"POSTGRES_PASSWORD_{env}"],
        dbname=os.environ[f"POSTGRES_DB_{env}"],
    )


def reader_cfg():
    c = cfg("PROD")
    c["user"] = os.environ["READER_USER_PROD"]
    c["password"] = os.environ["READER_PASSWORD_PROD"]
    return c


def connect(c):
    conn = psycopg2.connect(**c)
    conn.autocommit = True
    return conn


results = []


def report(name, passed, detail=""):
    results.append(passed)
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    if detail:
        print(f"       {detail}")


def expect_success(name, c, sql):
    try:
        with connect(c) as conn, conn.cursor() as cur:
            cur.execute(sql)
        report(name, True)
    except psycopg2.Error as e:
        report(name, False, f"unexpected error: {str(e).strip()}")


def expect_failure(name, c, sql):
    try:
        with connect(c) as conn, conn.cursor() as cur:
            cur.execute(sql)
        report(name, False, "write succeeded, but it should have been refused")
    except psycopg2.Error as e:
        report(name, True, f"refused: {str(e).strip().splitlines()[0]}")


def scalar(c, sql):
    with connect(c) as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchone()[0]


def main():
    dev, prod, reader = cfg("DEV"), cfg("PROD"), reader_cfg()

    # Who am I talking to? Prevents mixing up the two servers.
    print("Connections")
    for label, c in [("dev", dev), ("prod admin", prod), ("prod reader", reader)]:
        info = scalar(c, "SELECT current_user || ' @ ' || current_database() "
                         "|| ' port ' || inet_server_port()")
        print(f"  {label:12} -> {info}")
    print()

    # 1. Dev must accept writes
    expect_success(
        "1. dev: write succeeds",
        dev,
        f"DROP TABLE IF EXISTS {TEST_TABLE}; "
        f"CREATE TABLE {TEST_TABLE} (id int); INSERT INTO {TEST_TABLE} VALUES (1);",
    )

    # 2. Reader on prod must be refused
    expect_failure("2. prod reader: CREATE TABLE refused",
                   reader, f"CREATE TABLE {TEST_TABLE} (id int);")

    # 3. Admin on prod must be refused by default
    expect_failure("3. prod admin: CREATE TABLE refused by default",
                   prod, f"CREATE TABLE {TEST_TABLE} (id int);")

    # 4. Protection state
    state = scalar(prod, "SHOW default_transaction_read_only")
    report("4. prod: default_transaction_read_only is on", state == "on",
           f"current value: {state}")

    # 5. Dev change is invisible in prod
    exists_in_prod = scalar(
        prod,
        "SELECT count(*) FROM information_schema.tables "
        f"WHERE table_name = '{TEST_TABLE}'",
    )
    report("5. prod: dev test table does not exist", exists_in_prod == 0,
           f"tables named {TEST_TABLE} in prod: {exists_in_prod}")

    # 6. Reader cannot lift the protection itself (privileges are the real wall)
    expect_failure("6. prod reader: cannot bypass with SET ... = off",
                   reader,
                   "SET default_transaction_read_only = off; "
                   f"CREATE TABLE {TEST_TABLE} (id int);")

    # 7. Admin can lift it for one session only (release procedure)
    expect_success("7. prod admin: session-level lift allows a write",
                   prod,
                   "SET default_transaction_read_only = off; "
                   f"CREATE TABLE {TEST_TABLE} (id int); DROP TABLE {TEST_TABLE};")

    # 8. Protection is still on for new sessions afterwards
    state = scalar(prod, "SHOW default_transaction_read_only")
    report("8. prod: protection still on after the lift", state == "on",
           f"current value: {state}")

    # Cleanup in dev
    expect_success("cleanup: drop dev test table", dev,
                   f"DROP TABLE IF EXISTS {TEST_TABLE};")

    print()
    print(f"{sum(results)}/{len(results)} checks passed")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()