from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user_favorites")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_favorites: Mapped["User"] = relationship(back_populates="favorites")

   
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    fav_character: Mapped["Characters"] = relationship(back_populates="favorites")

    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    fav_planet: Mapped["Planets"] = relationship(back_populates="favorites")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets": self.planet_id,
            "characters": self.character_id,
            
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    terrain: Mapped[str] = mapped_column(String(60), nullable=True)
    population: Mapped[int] = mapped_column( nullable=True)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="fav_planet")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
        }

class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    gender: Mapped[str] = mapped_column(String(60), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(60), nullable=True)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="fav_character")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
        }

