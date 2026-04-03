from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:123@127.0.0.1:5433/postgres"
)

with engine.connect() as conn:
    print("Conectou!")