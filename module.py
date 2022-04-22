from sgu import Base, db

if __name__ == "__main__":
    Base.metadata.create_all(bind=db)
