from hdbcli import dbapi as hana_db
import traceback
import sys
import os
import time
from dotenv import load_dotenv
from custom_logger import log

load_dotenv()

HANA_CONFIG = {
    "address": os.getenv("SOURCE_ADDRESS"),
    "port": os.getenv("SOURCE_PORT"),
    "user": os.getenv("SOURCE_USER"),
    "password": os.getenv("SOURCE_PASSWORD"),
}

TARGET_CONFIG = {
    "address": os.getenv("TARGET_ADDRESS"),
    "port": os.getenv("TARGET_PORT"),
    "user": os.getenv("TARGET_USER"),
    "password": os.getenv("TARGET_PASSWORD"),
}

SOURCE_TABLE = os.getenv("SOURCE_TABLE")
TARGET_TABLE = os.getenv("TARGET_TABLE")
BATCH_SIZE = os.getenv("BATCH_SIZE")
ORDER_BY = os.getenv("ORDER_BY")
RETRY_LIMIT = 10
RETRY_DELAY = 2


def get_next_batch(cursor, offset):
    sql = f"SELECT * FROM {SOURCE_TABLE} ORDER BY {ORDER_BY} LIMIT ? OFFSET ?"
    cursor.execute(sql, [BATCH_SIZE, offset])
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    return cols, rows


def migrate_batch(target_conn, columns, rows):
    if not rows:
        return False

    placeholders = ', '.join(['?'] * len(columns))
    col_names = ', '.join(f'"{col}"' for col in columns)
    insert_sql = f"INSERT INTO {TARGET_TABLE} ({col_names}) VALUES ({placeholders})"

    try:
        with target_conn.cursor() as cur:
                cur.executemany(insert_sql, rows)
        target_conn.commit()
        print(f"Migrated batch of {len(rows)} rows.")
        return True
    except Exception as e:
        target_conn.rollback()
        print(f"Error migrating batch: {e}")
        traceback.print_exc()
        return False


def main():
    retries = 0
    batch_counter = 1
    offset = 0
    while retries < RETRY_LIMIT:
        try:
            hana_conn = hana_db.connect(**HANA_CONFIG)
            target_conn = hana_db.connect(**TARGET_CONFIG)

            hana_cursor = hana_conn.cursor()

            while True:
                columns, rows = get_next_batch(hana_cursor, offset)
                if not rows:
                    break
                log(f"Starting batch {batch_counter} of {len(rows)} and offset {offset}.")
                start = time.time()
                migration_result = migrate_batch(target_conn, columns, rows)
                end = time.time()
                if not migration_result:
                    log(f"Failed to migrate batch nr {batch_counter}. Trying again!", phrase='error')
                    continue
                log(f"Migrated batch number {batch_counter} of {len(rows)} rows. Total operation time: {end - start}", phrase='success')
                offset += len(rows)
                batch_counter += 1

            hana_cursor.close()
            hana_conn.close()
            target_conn.close()
            print("Migration completed.")
            break

        except Exception as e:
            error_code, error_msg = e.args
            if 'Socket closed by peer' in error_msg or 'Connection down' in error_msg:
                print(f"Connection lost: {error_msg}. Attempting to reconnect...")
                retries += 1
                time.sleep(RETRY_DELAY)
                continue
            else:
                print(f"Fatal error: {e}")
                traceback.print_exc()
                sys.exit(1)


if __name__ == "__main__":
    main()
