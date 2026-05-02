# TSIS 4: Snake Game — Database Integration & Advanced Gameplay

## Requirements

```bash
pip install pygame psycopg2
```

If `psycopg2` fails on Windows, use:

```bash
pip install psycopg2-binary
```

## PostgreSQL setup

Open pgAdmin or psql and create a database:

```sql
CREATE DATABASE snake_db;
```

Then check `config.py` and change username/password if needed:

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}
```

The game automatically creates these tables:

```sql
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE game_sessions (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT NOW()
);
```

## Run

```bash
python main.py
```

## Project structure

```text
TSIS4_Snake/
├── main.py
├── game.py
├── db.py
├── settings.json
├── config.py
└── assets/
```

## Implemented features

- Main Menu: Play, Leaderboard, Settings, Quit
- Username input in Pygame
- PostgreSQL leaderboard with psycopg2
- Top 10 scores
- Personal best during gameplay
- Weighted food
- Food disappearing after timer
- Poison food
- Speed Boost, Slow Motion, Shield
- Obstacles from Level 3
- Settings saved to JSON
- Game Over screen with Retry and Main Menu
