# 1) Egzistuoja bent kelios esybės
# 2) Yra bent dvi savybės su vienas-su-daug sąryšiu
# 3) Panaudojimo atvejuose bent vienai esybei reikalingos kelios užklausos pagal skirtingus parametrus

from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()
print("Connection successful")
# session.execute('''
#                 CREATE KEYSPACE spotify
#                     WITH REPLICATION = {
#                     'class' : 'SimpleStrategy',
#                     'replication_factor' : 1 };
#                 ''')
session.set_keyspace('spotify')
print("Keyspace set")
session.execute('DROP TABLE IF EXISTS artists')
session.execute('DROP TABLE IF EXISTS albums')
session.execute('DROP TABLE IF EXISTS albums_by_artist')
session.execute('DROP TABLE IF EXISTS songs_by_album')
session.execute('DROP TABLE IF EXISTS songs_by_artist')

session.execute('''
                CREATE TABLE IF NOT EXISTS artists (
                    artist_id int,
                    first_name text,
                    last_name text,
                    followers int,
                    PRIMARY KEY (artist_id));
                ''')
session.execute('''
                CREATE TABLE IF NOT EXISTS albums (
                    album_id int,
                    artist_id int,
                    album_genre text,
                    album_title text,
                    PRIMARY KEY (album_id, artist_id));
                ''')
session.execute('''
                CREATE TABLE IF NOT EXISTS albums_by_artist (
                    artist_id int,
                    album_id int,
                    album_genre text,
                    album_title text,
                    PRIMARY KEY (artist_id, album_id));
                ''')

session.execute('''
                CREATE TABLE IF NOT EXISTS songs_by_artist (
                    artist_id int,
                    song_id int,
                    title text,
                    album_id int,
                    duration int,
                    PRIMARY KEY (artist_id, song_id));
                ''')
session.execute('''
                CREATE TABLE IF NOT EXISTS songs_by_album (
                    artist_id int,
                    song_id int,
                    title text,
                    album_id int,
                    duration int,
                    PRIMARY KEY (album_id, song_id));
                ''')

def insertArtist(artist_id, first_name, last_name, followers):
    prep = session.prepare("INSERT INTO artists (artist_id, first_name, last_name, followers)"
                           "VALUES (?, ?, ?, ?)"
                           "IF NOT EXISTS")
    insert = session.execute(prep, [artist_id, first_name, last_name, followers]).one()
    if insert.applied == False:
        print(f"Artist {artist_id, first_name, last_name} already exists")

def insertAlbum(artist_id, album_id, genre, title):
    prep1 = session.prepare("INSERT INTO albums (artist_id, album_id, album_genre, album_title)"
                           "VALUES (?, ?, ?, ?)"
                           "IF NOT EXISTS")
    prep2 = session.prepare("INSERT INTO albums_by_artist (artist_id, album_id, album_genre, album_title)"
                            "VALUES (?, ?, ?, ?)"
                            "IF NOT EXISTS")
    insert1 = session.execute(prep1, [artist_id, album_id, genre, title]).one()
    insert2 = session.execute(prep2, [artist_id, album_id, genre, title]).one()
    if insert1.applied == False:
        print(f"Album {artist_id, album_id, genre, title} already exists in table albums.")
    if insert2.applied == False:
        print(f"Album {artist_id, album_id, genre, title} already exists in table albums_by_artist.")

def insertSong(artist_id, song_id, title, album_id, duration):
    prep1 = session.prepare("INSERT INTO songs_by_artist (artist_id, song_id, title, album_id, duration)"
                           "VALUES (?, ?, ?, ?, ?)"
                           "IF NOT EXISTS")
    prep2 = session.prepare("INSERT INTO songs_by_album (artist_id, song_id, title, album_id, duration)"
                            "VALUES (?, ?, ?, ?, ?)"
                            "IF NOT EXISTS")
    insert1 = session.execute(prep1, [artist_id, song_id, title, album_id, duration]).one()
    insert2 = session.execute(prep2, [artist_id, song_id, title, album_id, duration]).one()
    if insert1.applied == False:
        print(f"Song {artist_id, song_id, title, album_id, duration} already exists in table songs_by_artist.")
    if insert2.applied == False:
        print(f"Song {artist_id, song_id, title, album_id, duration} already exists in table songs_by_album.")

def artistAlbums(id):
    prep = session.prepare("SELECT first_name, last_name FROM artists WHERE artist_id = ?")
    name = session.execute(prep, [id]).one()
    prep1 = session.prepare("SELECT COUNT(album_id) AS album_count FROM albums_by_artist WHERE artist_id = ?")
    count = session.execute(prep1, [id]).one()
    rows_prep = session.prepare("SELECT album_title FROM albums_by_artist WHERE artist_id = ?")
    rows = session.execute(rows_prep, [id])
    print(f"Artist {name.first_name} {name.last_name} has {count.album_count} albums. Their titles are:")
    for album in rows:
        print(album.album_title)

def artistSongs(id):
    prep = session.prepare("SELECT first_name, last_name FROM artists WHERE artist_id = ?")
    name = session.execute(prep, [id]).one()
    prep1 = session.prepare("SELECT COUNT(song_id) AS song_count FROM songs_by_artist WHERE artist_id = ?")
    count = session.execute(prep1, [id]).one()
    rows_prep = session.prepare("SELECT title FROM songs_by_artist WHERE artist_id = ?")
    rows = session.execute(rows_prep, [id])
    print(f"Artist {name.first_name} {name.last_name} has {count.song_count} songs. Their titles are:")
    for song in rows:
        print(song.title)

def albumSongs(id):
    prep = session.prepare("SELECT album_title FROM albums WHERE album_id = ?")
    title = session.execute(prep, [id]).one()
    prep1 = session.prepare("SELECT COUNT(song_id) AS song_count FROM songs_by_album WHERE album_id = ?")
    count = session.execute(prep1, [id]).one()
    rows_prep = session.prepare("SELECT title FROM songs_by_album WHERE album_id = ?")
    rows = session.execute(rows_prep, [id])
    print(f"Album {title.album_title} has {count.song_count} songs. Their titles are:")
    for song in rows:
        print(song.title)

insertArtist(1, 'Kendrick', 'Lamar', 37676819)
insertArtist(2, 'Gus', 'Dapperton', 1773415)
insertArtist(3, 'Taylor', 'Swift', 73795017)
insertAlbum(1, 1, 'R&B', 'DAMN.')
insertAlbum(1, 2, 'Hip-Hop','good kid, m.A.A.d city')
insertAlbum(2, 3, 'Alternative', 'Where Polly People Go to Read')
insertAlbum(2, 4, 'Alternative', 'Orca')
insertAlbum(3, 5, 'Pop', 'Midnights')
insertAlbum(3, 6, 'Alternative', 'Lover')
insertSong(1, 1, 'BLOOD.', 1, 117)
insertSong(1, 2, 'PRIDE.', 1, 273)
insertSong(1, 3, 'LOVE. FEAT. ZACARI.', 1, 213)
insertSong(1, 4, 'Swimming Pools', 2, 313)
insertSong(1, 5, 'good kid', 2, 124)
insertSong(1, 6, 'Money Trees', 2, 386)
insertSong(2, 7, 'Roadhead', 3, 200)
insertSong(2, 8, 'Fill Me Up Anthem', 3, 276)
insertSong(2, 9, 'Palms', 4, 240)
insertSong(2, 10, 'Bluebird', 4, 227)
insertSong(3, 11, 'Maroon', 5, 218)
insertSong(3, 12, 'Lavender Haze', 5, 202)
insertSong(3, 13, 'Labyrinth', 5, 247)
insertSong(3, 14, 'Cruel Summer', 6, 178)
insertSong(3, 15, 'Paper Rings', 6, 222)
insertSong(3, 16, 'Cornelia Street', 6, 28)

print()
artistAlbums(1)
print()
artistSongs(1)
print()
albumSongs(1)

#insertArtist(1, 'Kendrick', 'Lamar', 37676819)
