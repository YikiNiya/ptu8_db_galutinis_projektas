from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///wow_database/wow_o2m.db')
Base = declarative_base()


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    level = Column(Integer)
    race_id = Column(Integer, ForeignKey("race.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    profession_id = Column(Integer, ForeignKey("profession.id"))
    race = relationship("Race", back_populates="games")
    class_ = relationship("Class", back_populates="games")
    profession = relationship("Profession", back_populates="games")

    def __str__(self):
        return f"ID {self.id}: Username - {self.username}, level - {self.level}, race - {self.race.name}, class - {self.class_.name}, profession - {self.profession.name}"


class Race(Base):
    __tablename__ = "race"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    available = Column(String, ForeignKey("class.id"))
    faction = Column(String)
    games = relationship("Game", back_populates="race")
    class_ = relationship("Class", back_populates="races")

    def __str__(self):
        return f"ID {self.id}: Race name {self.name}, available {self.available}, faction {self.faction}"


class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    party_role = Column(String)
    resources = Column(String)
    armor_type = Column(String)
    weapon = Column(String)
    games = relationship("Game", back_populates="class_")
    races = relationship("Race", back_populates="class_")

    def __str__(self):
        return f"ID {self.id}: Class name {self.name}, party role {self.party_role}, resources {self.resources}, armor type {self.armor_type}, weapons {self.weapon}"


class Profession(Base):
    __tablename__ = "profession"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship("Game", back_populates="profession")

    def __str__(self):
        return f"ID {self.id}: Name {self.name}"


if __name__ == "__main__":
    Base.metadata.create_all(engine)