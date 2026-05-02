# db.py
# Database layer for TSIS 4 Snake.
# Uses psycopg2 to store players and game sessions in PostgreSQL.

import psycopg2
from psycopg2 import sql
from config import DB_CONFIG


class Database:
    def __init__(self):
        self.connection = None
        self.available = False
        self.connect()

    def connect(self):
        """Connects to PostgreSQL and creates tables if they do not exist."""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.connection.autocommit = True
            self.available = True
            self.create_tables()
            print("Database connected successfully.")
        except Exception as error:
            self.connection = None
            self.available = False
            print("Database connection failed:", error)

    def create_tables(self):
        """Creates required tables."""
        if not self.available:
            return

        query_players = """
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        """

        query_sessions = """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query_players)
            cursor.execute(query_sessions)

    def get_or_create_player(self, username):
        """
        Gets player id by username.
        If player does not exist, creates a new player.
        """
        if not self.available:
            return None

        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM players WHERE username = %s;",
                (username,)
            )

            result = cursor.fetchone()

            if result:
                return result[0]

            cursor.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id;",
                (username,)
            )

            return cursor.fetchone()[0]

    def save_game_session(self, username, score, level_reached):
        """Saves game result to database."""
        if not self.available:
            print("Database is not available. Result was not saved.")
            return

        player_id = self.get_or_create_player(username)

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s);
                """,
                (player_id, score, level_reached)
            )

    def get_top_scores(self, limit=10):
        """Returns top 10 all-time scores."""
        if not self.available:
            return []

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
                LIMIT %s;
                """,
                (limit,)
            )

            return cursor.fetchall()

    def get_personal_best(self, username):
        """Returns player's best score."""
        if not self.available:
            return 0

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                WHERE p.username = %s;
                """,
                (username,)
            )

            result = cursor.fetchone()
            return result[0] if result else 0

    def close(self):
        """Closes database connection."""
        if self.connection:
            self.connection.close()
