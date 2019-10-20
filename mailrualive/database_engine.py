import os
import sqlite3
import traceback

SELECT_FROM_PROFILE_WHERE_NAME = "SELECT * FROM profiles WHERE name = :name"

INSERT_INTO_PROFILE = "INSERT INTO profiles (name) VALUES (?)"

SQL_CREATE_PROFILE_TABLE = """
    CREATE TABLE IF NOT EXISTS `profiles` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT NOT NULL);"""

SQL_CREATE_ACCOUNTS_PROGRESS_TABLE = """
    CREATE TABLE IF NOT EXISTS `accountsProgress` (
        `profile_id` INTEGER NOT NULL,
        `followers` INTEGER NOT NULL,
        `following` INTEGER NOT NULL,
        `total_posts` INTEGER NOT NULL,
        `created` DATETIME NOT NULL,
        `modified` DATETIME NOT NULL,
        CONSTRAINT `fk_accountsProgress_profiles1`
        FOREIGN KEY(`profile_id`) REFERENCES `profiles`(`id`));"""


def get_database(Settings, make=False):
    address = Settings.database_location
    logger = Settings.logger
    credentials = Settings.profile

    id, name = credentials["id"], credentials["name"]
    address = validate_database_address(Settings)

    if not os.path.isfile(address) or make:
        create_database(address, logger, name)

    id = get_profile(name, address, logger, Settings) if id is None or make else id

    return address, id


def create_database(address, logger, name):
    try:
        connection = sqlite3.connect(address)
        with connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            create_tables(cursor, ["profiles", "accountsProgress"])

            connection.commit()

    except Exception as exc:
        print("dnno0")
        logger.warning(
            "Wah! Error occurred while getting a DB for '{}':\n\t{}".format(
                name, str(exc).encode("utf-8")
            )
        )

    finally:
        if connection:
            # close the open connection
            connection.close()


def create_tables(cursor, tables):
    if "profiles" in tables:
        cursor.execute(SQL_CREATE_PROFILE_TABLE)

    if "accountsProgress" in tables:
        cursor.execute(SQL_CREATE_ACCOUNTS_PROGRESS_TABLE)


def verify_database_directories(address):
    db_dir = os.path.dirname(address)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)


def validate_database_address(Settings):
    address = Settings.database_location
    if not address.endswith(".db"):
        slash = "\\" if "\\" in address else "/"
        address = address if address.endswith(slash) else address + slash
        address += "mailrualive.db"
        Settings.database_location = address
    verify_database_directories(address)
    return address


def get_profile(name, address, logger, Settings):
    try:
        conn = sqlite3.connect(address)
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            profile = select_profile_by_username(cursor, name)

            if profile is None:
                add_profile(conn, cursor, name)
                # reselect the table after adding data to get the proper `id`
                profile = select_profile_by_username(cursor, name)
    except Exception as exc:
        traceback.print_exc()
        logger.error(
            "Heeh! Error occurred while getting a DB profile for '{}':\n\t{}".format(
                name, str(exc).encode("utf-8")
            )
        )
    finally:
        if conn:
            # close the open connection
            conn.close()

    profile = dict(profile)
    id = profile["id"]
    # assign the id to its child in `Settings` class
    Settings.profile["id"] = id

    return id


def add_profile(conn, cursor, name):
    cursor.execute(INSERT_INTO_PROFILE, (name,))
    # commit the latest changes
    conn.commit()


def select_profile_by_username(cursor, name):
    cursor.execute(SELECT_FROM_PROFILE_WHERE_NAME, {"name": name})
    profile = cursor.fetchone()

    return profile
