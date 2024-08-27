import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

# Define column names for the houses table
house_columns = [
    "url_key",
    "area",
    "city",
    "price_exc",
    "price_inc",
    "available_from",
    "max_register",
    "contract_type",
    "rooms",
]

# Non-mass assignables: 'created_at', 'occupied_at'

# Configure logging
logging.basicConfig(
    filename="house_sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_connection() -> Optional[sqlite3.Connection]:
    """
    Create a connection to the SQLite database.

    Returns:
        Optional[sqlite3.Connection]: SQLite connection object if successful, None otherwise.
    """
    try:
        conn = sqlite3.connect("houses.db")
        logging.info("Database connection created")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error creating database connection: {e}")
        return None


def create_table() -> None:
    """
    Create the 'houses' table and necessary indexes if they don't exist.
    """
    conn = create_connection()
    if conn is None:
        return

    try:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS houses
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      url_key TEXT,
                      area TEXT,
                      city TEXT,
                      price_exc TEXT,
                      price_inc TEXT,
                      available_from TEXT,
                      max_register TEXT,
                      contract_type TEXT,
                      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                      occupied_at TEXT DEFAULT NULL,
                      rooms TEXT)"""
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_url_key ON houses (url_key)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_occupied_at ON houses (occupied_at)")
        conn.commit()
        logging.info("Table 'houses' created if not exists")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")
    finally:
        conn.close()


def sync_houses(city_id: str, houses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sync houses data with the database. Updates `occupied_at` for houses not present in the new data
    and inserts new houses into the database.

    Args:
        city_id (str): The city identifier to filter houses by.
        houses (List[Dict[str, Any]]): A list of house data dictionaries to sync.

    Returns:
        List[Dict[str, Any]]: A list of new houses inserted into the database.
    """
    conn = create_connection()
    if conn is None:
        return []

    new_houses = []
    try:
        c = conn.cursor()

        # Get the existing houses in the database for the given city_id
        c.execute(
            "SELECT url_key FROM houses WHERE city = ? AND occupied_at IS NULL",
            (city_id,),
        )
        existing_houses = {row[0] for row in c.fetchall()}

        # Extract the url_keys from the new houses
        new_houses_url_keys = {house["url_key"] for house in houses}

        # Houses to be updated (those in the database but not in the new houses)
        to_be_updated = existing_houses - new_houses_url_keys
        if to_be_updated:
            update_query = f"""
            UPDATE houses
            SET occupied_at = ?
            WHERE occupied_at IS NULL AND url_key IN ({','.join(['?'] * len(to_be_updated))})
            """
            c.execute(
                update_query, (datetime.now().isoformat(),) + tuple(to_be_updated)
            )

        # Insert new houses into the database
        to_be_inserted = [
            tuple(house[column] for column in house_columns)
            for house in houses
            if house["url_key"] not in existing_houses
        ]

        if to_be_inserted:
            insert_query = f"""
            INSERT INTO houses ({','.join(house_columns)})
            VALUES ({','.join(['?'] * len(house_columns))})
            """
            c.executemany(insert_query, to_be_inserted)
            conn.commit()

            new_houses = [
                house for house in houses if house["url_key"] not in existing_houses
            ]
            logging.info(f"{len(new_houses)} new houses inserted into the database")

    except sqlite3.Error as e:
        logging.error(f"Error syncing houses: {e}")
    finally:
        conn.close()

    return new_houses
