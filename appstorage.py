import sqlite3
import os
from datetime import datetime
from android.storage import app_storage_path
import environment as env 


class AppStorage:
    storage_instance = None

    def __init__(self):
        self.db_name = os.path.join(app_storage_path(), 'appstorage.db')
        self.create_table()  # Ensure the table is created upon initialization
    
    @classmethod
    def get_appstorage(cls):
        if not AppStorage.storage_instance:
            AppStorage.storage_instance = AppStorage()
        return AppStorage.storage_instance
    
    def create_connection(self):
        """Create a new database connection."""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Create the lookup table if it doesn't exist."""
        with self.create_connection() as connection:
            with connection:
                connection.execute('''
                    CREATE TABLE IF NOT EXISTS lookup (
                        lookup_time TEXT NOT NULL,
                        lookup TEXT PRIMARY KEY,
                        lookup_response TEXT,
                        success_reinforces INTEGER,
                        last_reinforce_time TEXT
                    )
                ''')
                # Create the index in a separate statement
                connection.execute('''
                    CREATE INDEX IF NOT EXISTS idx_success_reinforces_last_reinforce_time
                    ON lookup (success_reinforces, last_reinforce_time)
                ''')
                connection.execute('''
                    CREATE TABLE IF NOT EXISTS settings (
                        openai_api_key TEXT NOT NULL,
                        openai_org_id TEXT NOT NULL,
                        learning_curve_min_interval REAL,
                        learning_curve_max_interval REAL
                    )
                ''')
                connection.execute('''
                    INSERT INTO settings (openai_api_key, openai_org_id, learning_curve_min_interval, learning_curve_max_interval)
                    SELECT 
                        '', '',
#                        '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', 
#                        'org-68N6LbPiQuUQ7ZbKmpyuxjOg', 
                        0.005,
                        0.02
                    WHERE (SELECT COUNT(*) FROM settings) = 0
                ''')

    def add_lookup(self, lookup, lookup_response):
        """Add a new lookup to the database."""
        print(f"Adding lookup: {lookup} with response: {lookup_response}")
        with self.create_connection() as connection:
            cursor = connection.cursor()
            # Check if the lookup already exists
            cursor.execute('SELECT * FROM lookup WHERE lookup = ?', (lookup,))
            existing_record = cursor.fetchone()

            if existing_record:
                # If the lookup exists, return False
                return False

            # If the lookup does not exist, add a new record
            with connection:
                cursor.execute('''
                    INSERT INTO lookup (lookup_time, lookup, lookup_response, success_reinforces, last_reinforce_time)
                    VALUES (DATETIME('now'), ?, ?, 0, DATETIME('now'))
                ''', (lookup, lookup_response))

            return True  # Return True if the lookup was added successfully

    def get_all_lookups(self):
        """Retrieve all lookups from the database."""
        learning_curve_basetime = env.get_learning_curve_basetime()
        learning_curve_maxtime = env.get_learning_curve_maxtime()
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                           SELECT lookup, lookup_response, lookup_time, success_reinforces, last_reinforce_time, DATETIME(JULIANDAY(last_reinforce_time) + MIN(?, (1 << success_reinforces) * ?)) as review_due_time FROM lookup ORDER BY success_reinforces, review_due_time
                           ''', (learning_curve_maxtime, learning_curve_basetime, ))
            all_lookups = [row for row in cursor.fetchall()]  # Fetch all records
            print(f"All lookups: {all_lookups}")
            return all_lookups  # Return the list of all lookups

    def get_review_lookups(self):
        """Retrieve lookups due for review."""
        learning_curve_basetime = env.get_learning_curve_basetime()
        learning_curve_maxtime = env.get_learning_curve_maxtime()
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                           SELECT lookup, lookup_response, lookup_time, success_reinforces, last_reinforce_time FROM lookup WHERE julianday(DATETIME('now')) - julianday(last_reinforce_time) > MIN(?, (1 << success_reinforces) * ?)
                           ''', (learning_curve_maxtime, learning_curve_basetime, ))
            all_lookups = [row for row in cursor.fetchall()]  # Fetch all records
            print(f"Lookups due review: {all_lookups}")
            return all_lookups  # Return the list of lookups due review

    def get_statistics(self):
        """Retrieve statistics from the database."""
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT success_reinforces, count(*) AS count FROM lookup GROUP BY success_reinforces ORDER BY count(*) DESC')
            statistics = [row for row in cursor.fetchall()]  # Fetch all records
            print(f"statistics: {statistics}")
            return statistics  # Return the statistics
        
    def reinforce_result(self, lookup, success):
        """Reinforce the result of a lookup."""
        with self.create_connection() as connection:
            cursor = connection.cursor()
            # Check if the lookup exists
            cursor.execute('SELECT success_reinforces FROM lookup WHERE lookup = ?', (lookup,))
            record = cursor.fetchone()

            if record:
                if success:
                    # If the lookup exists, increment the success_reinforces
                    success_reinforces = record[0] + 1
                else:
                    # If the lookup exists, reset to 0
                    success_reinforces = 0
                with connection:
                    cursor.execute('''
                        UPDATE lookup
                        SET success_reinforces = ?, last_reinforce_time = DATETIME('now')
                        WHERE lookup = ?
                    ''', (success_reinforces, lookup))
                return True  # Return True if the reinforcement was successful
            return False  # Return False if the lookup does not exist

    def delete_lookup(self, lookup):
        """Remove a specific lookup from the lookup table by its lookup value."""
        with self.create_connection() as connection:
            cursor = connection.cursor()
            # Execute the delete statement
            cursor.execute('DELETE FROM lookup WHERE lookup = ?', (lookup,))
            if cursor.rowcount > 0:
                print(f"Removed lookup: {lookup}")
                return True  # Return True if a record was deleted
            else:
                print(f"Lookup: {lookup} not found.")
                return False  # Return False if no record was deleted

    def cleanup(self):
        """Remove all records from the lookup table."""
        with self.create_connection() as connection:
            with connection:
                connection.execute('DELETE FROM lookup')  # Delete all records

    def read_settings(self):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                           SELECT openai_api_key, openai_org_id, learning_curve_min_interval, learning_curve_max_interval FROM settings
                           ''')
            settings = [row for row in cursor.fetchall()]
            print(f"Settings: {settings}")
            return settings[0]

    def update_settings(self, openai_api_key, openai_org_id, learning_curve_min_interval, learning_curve_max_interval):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE settings
                SET openai_api_key = ?, openai_org_id = ?, learning_curve_min_interval = ?, learning_curve_max_interval = ?
            ''', (openai_api_key, openai_org_id, learning_curve_min_interval, learning_curve_max_interval))
