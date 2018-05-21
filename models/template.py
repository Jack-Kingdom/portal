"""
sql template for CURD operation.
used prepare statement to avoid sql injection.
"""

shortURL_template = {
    'init': """
CREATE TABLE IF NOT EXISTS shortURL (
  id  INTEGER PRIMARY KEY AUTOINCREMENT,
  dst VARCHAR(255) NOT NULL
);
    """,
    'insert': """
INSERT INTO shortURL VALUES (NULL ,?);
    """,
    'update': """
UPDATE shortURL SET dst= ? WHERE id= ?;
    """,
    'query': """
SELECT dst FROM shortURL WHERE id=?;
    """,
    'delete': """
DELETE FROM shortURL WHERE id=?;
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
    INSERT INTO alias VALUES (NULL ,?);
        """,
    'update': """
    UPDATE alias SET dst= ? WHERE src= ?;
        """,
    'query': """
    SELECT dst FROM alias WHERE src=?;
        """,
    'delete': """
    DELETE FROM alias WHERE src=?;
        """
}
