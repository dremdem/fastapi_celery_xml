"""
SQLAlchemy models, session and all that DB stuff
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://postgres:postgres@db:5432/test_db')
Session = sessionmaker(bind=engine)

session = Session()


def build_schema() -> None:
    """
    Let's create our tables in postgres
    """
    Base.metadata.create_all(engine)


class Url(Base):
    """
    Urls object is storing all info about XML-file that received by an url
    """
    __tablename__ = 'url'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    processed = Column(Boolean, default=False)
    error = Column(String, nullable=True)

    keys = relationship("Key", backref="url", order_by="Key.id")

    @property
    def as_dict(self):
        return {'id': self.id,
                'url': self.url,
                'processed': self.processed,
                'error': self.error}

    @property
    def as_dict_with_keys(self):
        return {'id': self.id,
                'url': self.url,
                'keys': [key.value for key in self.keys]}


class Key(Base):
    """
    Key represent keys in the Url(XML-file)
    """
    __tablename__ = 'key'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)

    url_id = Column(ForeignKey('url.id'))
