from config import CONFIG

if CONFIG['ODBC_DSN']:
    from .mysql import *
else:
    from .sqlite import *
