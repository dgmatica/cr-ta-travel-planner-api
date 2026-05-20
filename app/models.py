from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True)
    description: Optional[str] = None
    start_date: Optional[date] = None

    is_completed: bool = Field(default=False)

    places: list["ProjectPlace"] = Relationship(back_populates="project")


class ProjectPlace(SQLModel, table=True):
    __tablename__ = "project_places"

    id: Optional[int] = Field(default=None, primary_key=True)

    project_id: int = Field(foreign_key="projects.id", index=True)

    external_id: int = Field(index=True)
    title: str

    notes: Optional[str] = None
    visited: bool = Field(default=False)

    project: Optional[Project] = Relationship(back_populates="places")
