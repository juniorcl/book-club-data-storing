"""
This script main to create a sqlite database.
"""

#%%
from sqlalchemy import create_engine

engine = create_engine('sqlite:///../db/bookclub_db.sqlite', echo=False)
conn = engine.connect()

scheam_customer = '''
CREATE TABLE book(
    scraping_time       TEXT,
    category            TEXT,
    title               INTEGER,
    price               REAL,
    star_rating         INTEGER,
    description         TEXT,
    upc                 TEXT,
    type                TEXT,
    price_excl_tax      REAL,
    price_incl_tax      REAL,
    tax                 REAL,
    number_reviews      INTEGER,
    availability_stock  TEXT,
    availability_number REAL
)
'''

#create schema
conn.execute(scheam_customer)

# %%
