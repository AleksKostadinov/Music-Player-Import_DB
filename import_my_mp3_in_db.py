import pathlib
import psycopg2
from decouple import config

files = pathlib.Path(config('MUSIC_PATH'))

filtered_data = list(files.rglob('*.mp3'))

con = psycopg2.connect(
    host=config("PG_HOST"),
    database=config("PG_DB"),
    user=config("PG_USER"),
    password=config("PG_PASSWORD")
)

cur = con.cursor()

query_create_table = """
    CREATE TABLE IF NOT EXISTS music(
        id SERIAL PRIMARY KEY,
        singer VARCHAR(50),
        song VARCHAR(50),
        CONSTRAINT unique_singer_song UNIQUE (singer, song)
    );
"""

cur.execute(query_create_table)

try:
    for file in filtered_data:
        file_str = str(file)
        # Extract singer from the filename
        clean_file = pathlib.Path(file).stem.split('.')[-1]
        singer, song = clean_file.split(' - ')

        query_insert_song = """
            INSERT INTO music(singer, song)
            VALUES (TRIM(%s), TRIM(%s))
            ON CONFLICT (singer, song) DO NOTHING;
        """

        cur.execute(query_insert_song, (singer, song))

    con.commit()
except psycopg2.Error as e:
    print("Error:", e)
finally:
    con.close()
