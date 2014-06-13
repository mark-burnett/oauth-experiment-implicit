from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy


Base = declarative_base()


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)

    access_token = Column(Text, unique=True)
    refresh_token = Column(Text, unique=True)
    expires = Column(DateTime)
    _scope = Column(Text)

    @property
    def scope(self):
        return self._scope.split(' ')

    @scope.setter
    def scope(self, value):
        self._scope = ' '.join(value)

    @property
    def as_dict(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': '%s' % (self.expires - datetime.now()),
            'scope': self.scope,
        }
