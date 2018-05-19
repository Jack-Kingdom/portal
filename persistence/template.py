shortURL_template = {
    'init': """
CREATE TABLE IF NOT EXISTS shortURL (
  id  INTEGER PRIMARY KEY AUTOINCREMENT,
  dst VARCHAR(255) NOT NULL
);
    """,
    'insert': """
INSERT INTO shortURL VALUES (NULL ,'https://baidu.com');
    """,
    'update': """
UPDATE shortURL SET dst='https://google.com' WHERE id=3;
    """,
    'query': """
SELECT dst FROM shortURL WHERE id=3;
    """,
    'delete': """
DELETE FROM shortURL WHERE id=2;
    """
}

alias_template = {
    'init': """
CREATE TABLE IF NOT EXISTS alias (
  src VARCHAR(255) PRIMARY KEY,
  dst VARCHAR(255) NOT NULL
);
    """,
    'insert': """
INSERT INTO shortURL VALUES (NULL ,'https://baidu.com');
    """,
    'update': """

    """,
    'query': """

    """,
    'delete': """

    """
}
