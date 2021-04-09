set APPX_COUNT_DISTINCT=true;
use dw;

DROP VIEW IF EXISTS raw_searches;
DROP VIEW IF EXISTS raw_pixels;
DROP VIEW IF EXISTS filtered_searches;
DROP VIEW IF EXISTS filtered_pixels;
DROP TABLE IF EXISTS s;
DROP VIEW IF EXISTS p;
DROP VIEW IF EXISTS users;
DROP VIEW IF EXISTS pk;
CREATE VIEW raw_searches AS SELECT user_cookie, keyword_category_id FROM searches 
   WHERE user_cookie is not null AND LENGTH(user_cookie) = 32 
       AND keyword_category_id is not null 
       AND (is_fraud is null or is_fraud = 0) 
       AND (is_blocked is null or is_blocked = 0) 
       AND y='2016' and m='02';

CREATE VIEW raw_pixels AS
    SELECT pixel_id, user_cookie FROM pixels
                       WHERE user_cookie is not null
                       AND user_cookie != ''
                       AND user_cookie != '-'
                       AND pixel_id is not null
		       AND y='2016' 
		       AND m='02';

CREATE VIEW filtered_searches AS
    SELECT user_cookie, keyword_category_id FROM raw_searches
       WHERE keyword_category_id is not NULL;


CREATE VIEW filtered_pixels AS
    SELECT user_cookie, pixel_id FROM raw_pixels
       WHERE pixel_id = '17214';

CREATE TABLE IF NOT EXISTS s AS SELECT keyword_category_id, COUNT(DISTINCT user_cookie) as cnt
                       FROM filtered_searches
                       GROUP BY keyword_category_id;

CREATE VIEW p AS SELECT pixel_id, COUNT(DISTINCT user_cookie) as cnt
                   FROM filtered_pixels GROUP BY pixel_id;

CREATE VIEW users AS SELECT DISTINCT user_cookie from raw_pixels
                                   UNION
                               SELECT DISTINCT user_cookie from raw_searches;


CREATE VIEW pk AS SELECT p_users.pixel_id as pixel_id,
                                   s_users.keyword_category_id as keyword_category_id,
                                   COUNT(DISTINCT s_users.user_cookie) as cnt
       FROM (SELECT p.pixel_id, user_cookie FROM p, filtered_pixels p_f
                       WHERE p.pixel_id = p_f.pixel_id) p_users,
            (SELECT s_f.keyword_category_id, s_f.user_cookie FROM s, filtered_searches s_f
                       WHERE s.keyword_category_id = s_f.keyword_category_id) s_users
       WHERE p_users.user_cookie = s_users.user_cookie
       GROUP BY pixel_id, keyword_category_id HAVING COUNT(DISTINCT s_users.user_cookie) >= 5;



SELECT labels.label, s.cnt FROM s, labels WHERE s.keyword_category_id = labels.keyword_category_id;

SELECT p.pixel_id as pixel_id, labels.label as label, p.cnt as p_users, pk.cnt as pk_users, t.total
FROM p, pk, labels, (SELECT COUNT(DISTINCT user_cookie) as total FROM users) t
WHERE p.pixel_id = pk.pixel_id and labels.keyword_category_id = pk.keyword_category_id;

DROP VIEW IF EXISTS raw_searches;
DROP VIEW IF EXISTS raw_pixels;
DROP VIEW IF EXISTS filtered_searches;
DROP VIEW IF EXISTS filtered_pixels;
DROP TABLE IF EXISTS s;
DROP VIEW IF EXISTS p;
DROP VIEW IF EXISTS users;
DROP VIEW IF EXISTS pk;
