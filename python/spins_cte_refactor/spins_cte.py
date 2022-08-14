import sqlite3


def get_cte_query():
    """
        Which users are eligable for promotions based on 
        1. They listened to a certain artist more than X times. 
        2. The artist is part of an active promotion. 
        3. They've been paying customers for over a year. 
        4. They haven't already been promoted for the given promotional. 
    """

    return """
        WITH listener_artist_spins AS (
            SELECT sp.listener_id, a.artist_id as artist_id, SUM(spins) as artist_spins
                FROM daily_spins sp
                JOIN songs s ON sp.song_id = s.id 
                JOIN (SELECT DISTINCT artist_id FROM promotions) a ON a.artist_id = s.artist_id
            GROUP BY sp.listener_id, a.artist_id
            HAVING artist_spins > 100
        ),
        listeners_with_promotion AS (
            SELECT listener_id, p.id as promotion_id 
            FROM listener_artist_spins las
            JOIN promotions p ON p.artist_id = las.artist_id
        ),
        not_previously_promoted AS (
            SELECT p.listener_id, p.promotion_id FROM listeners_with_promotion p
            LEFT JOIN promoted_listeners prev 
                ON (p.promotion_id = prev.promotion_id 
                    AND p.listener_id = prev.listener_id)
            WHERE prev.promotion_id IS NULL
        ),
        listeners_eligable_for_promotion AS (
            SELECT l.id as listener_id, promotion_id FROM not_previously_promoted npp
            JOIN listeners l ON npp.listener_id = l.id
            JOIN accounts a ON l.account_id = a.id
            JOIN account_type t ON a.account_type_id = t.id
            WHERE t.type = 'paid' AND account_updated_at <= "2021-08-06"
        )
        SELECT listener_id, promotion_id FROM listeners_eligable_for_promotion
    """

def get_sloppy_version():
    return """
        SELECT l.id as listener_id, inner3.promotion_id FROM (
            SELECT inner2.listener_id, inner2.promotion_id FROM
                (SELECT listener_id, p.id as promotion_id FROM
                    (SELECT sp.listener_id, a.id as artist_id, SUM(spins) as artist_spins
                            FROM daily_spins sp
                            JOIN songs s ON sp.song_id = s.id 
                            JOIN artists a ON a.id = s.artist_id
                        GROUP BY sp.listener_id, a.id
                        HAVING artist_spins > 100) inner1
                JOIN promotions p ON p.artist_id = inner1.artist_id) inner2
            LEFT JOIN promoted_listeners prev 
                ON (inner2.promotion_id = prev.promotion_id AND inner2.listener_id = prev.listener_id)
            WHERE prev.promotion_id IS NULL) inner3
        JOIN listeners l ON inner3.listener_id = l.id
        JOIN accounts a ON l.account_id = a.id
        JOIN account_type t ON a.account_type_id = t.id
        WHERE t.type = 'paid' AND account_updated_at <= "2021-08-06"


CREATE TABLE daily_spins (listener_id BIGINT, song_id BIGINT, spins INT, 
                          FOREIGN KEY (listener_id) REFERENCES listeners(id), 
                          FOREIGN KEY(song_id) REFERENCES songs(id))

CREATE TABLE listeners (id BIGINT, account_id INT
                        FOREIGN KEY (account_id) REFERENCES accounts(id))

CREATE TABLE accounts (id INT, account_type_id INT, account_updated_at STRING
                       FOREIGN KEY (account_type_id) REFERENCES account_type(id))

CREATE TABLE account_type (id INT, type STRING)

CREATE TABLE songs (id INT, artist_id INT, name STRING
                    FOREIGN KEY (artist_id) REFERENCES artists(id))

CREATE TABLE artists (id INT, name STRING)

CREATE TABLE promotions (id INT, artist_id BIGINT, 
                         FOREIGN KEY (artist_id) REFERENCES artists(id))

CREATE TABLE promoted_listeners (id INT, promotion_id INT, listener_id BIGINT,
                                 FOREIGN KEY (listener_id) REFERENCES listeners(id),
                                 FOREIGN KEY (promotion_id) REFERENCES promotions(id))

    """

def get_spins_data():
    return [
        [1, 1, 20], # listener_id, song_id, spins
        [1, 1, 130], # spins for promoted artist song. passes. 
        [2, 1, 80],
        [2, 1, 30], # combined spins for promoted artist song. passes.
        [2, 3, 110], # song for artist not promoted. filtered. 
        [3, 1, 110],  # not promoted listener. filtered.
        [4, 1, 110], # listener not part of paid tier. filtered.
        [5, 1, 110], # listener not paid tier long enough. filtered.
        [6, 1, 90], # not enough spins for promoted artist song. filtered. 
    ]

def get_songs():
    return [
        [1, 1, "Whirlwind"], # song_id, name, artist_id
        [3, 3, "High"], # song_id, name, artist_id
    ]

def get_artists():
    return [
        [1, "Rockstar"], # artist_id, name
        [3, "Foo"], # artist_id, name
    ]

def get_listeners():
    return [
        [1, 1], # listener_id, account_id
        [2, 2], 
        [3, 3],
        [4, 4], 
        [5, 5],
        [6, 6],
    ]

def get_accounts():
    return [
        [1, 2, "2019-01-01"], # id, type, updated_at
        [2, 2, "2019-02-01"], 
        [3, 2, "2019-02-01"], # not part of promotion. filtered.
        [4, 1, "2019-02-01"], # free listener. filtered.
        [5, 2, "2022-02-01"], # too recent on paid tier. filtered.
        [6, 2, "2019-02-01"], # not enough combined spins. filtered.
    ]

def get_account_types():
    return [
        [1, "freemium"],
        [2, "paid"],
    ]

def get_promotions():
    return [
        [1, 1], # id, #artist_id
    ]

def get_promoted_listeners():
    return [
        [1, 1, 3], # id, promotion_id, #listener_id
    ]


con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.execute("CREATE TABLE daily_spins (listener_id bigint, song_id bigint, spins int, FOREIGN KEY (listener_id) REFERENCES listeners(id), FOREIGN KEY(song_id) REFERENCES songs(id))")
cur.execute("CREATE TABLE listeners (id bigint, account_id int, FOREIGN KEY (account_id) REFERENCES accounts(id))")
cur.execute("CREATE TABLE accounts (id int, account_type_id int, account_updated_at string, FOREIGN KEY (account_type_id) REFERENCES account_type(id))")
cur.execute("CREATE TABLE account_type (id int, type string)")
cur.execute("CREATE TABLE songs (id int, artist_id int, name string, FOREIGN KEY (artist_id) REFERENCES artists(id))")
cur.execute("CREATE TABLE artists (id int, name string)")
cur.execute("CREATE TABLE promotions (id int, artist_id bigint, FOREIGN KEY (artist_id) REFERENCES artists(id))")
cur.execute("CREATE TABLE promoted_listeners (id int, promotion_id int, listener_id bigint,  FOREIGN KEY (listener_id) REFERENCES listeners(id), FOREIGN KEY (promotion_id) REFERENCES promotions(id) )")

cur.executemany("INSERT INTO daily_spins values (?, ?, ?)", get_spins_data())
cur.executemany("INSERT INTO listeners values (?, ?)", get_listeners())
cur.executemany("INSERT INTO accounts values (?, ?, ?)", get_accounts())
cur.executemany("INSERT INTO account_type values (?, ?)", get_account_types())
cur.executemany("INSERT INTO promotions values (?, ?)", get_promotions())
cur.executemany("INSERT INTO promoted_listeners values (?, ?, ?)", get_promoted_listeners())
cur.executemany("INSERT INTO songs values (?, ?, ?)", get_songs())
cur.executemany("INSERT INTO artists values (?, ?)", get_artists())


cur.execute(get_cte_query())
results = cur.fetchall()
print("CTE version")
print("--------------------------")
for r in results:
    print(r)


cur.execute(get_sloppy_version())
results = cur.fetchall()
print("")
print("SLOPPY version")
print("--------------------------")
for r in results:
    print(r)
