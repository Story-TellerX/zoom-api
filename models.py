import sqlalchemy

metadata = sqlalchemy.MetaData()


zoom_events_table = sqlalchemy.Table(
    "zoom_events",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("event_ts", sqlalchemy.BigInteger),
    sqlalchemy.Column("event", sqlalchemy.String(100)),
    sqlalchemy.Column("payload", sqlalchemy.JSON),
)
