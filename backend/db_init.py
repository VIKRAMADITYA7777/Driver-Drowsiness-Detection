from app.database import engine, Base
from app.logger import configure_logging

if __name__ == '__main__':
    configure_logging()
    Base.metadata.create_all(bind=engine)
    print('Database schema created successfully.')
