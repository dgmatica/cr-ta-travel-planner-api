from datetime import date

from sqlmodel import SQLModel


class ProjectPlaceBase(SQLModel):
    external_id: int
    notes: str | None = None


class ProjectPlaceCreate(ProjectPlaceBase):
    pass


class ProjectPlaceUpdate(SQLModel):
    notes: str | None = None
    visited: bool | None = None


class ProjectPlaceRead(SQLModel):
    id: int
    project_id: int
    external_id: int
    title: str
    notes: str | None
    visited: bool


class ProjectBase(SQLModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class ProjectCreate(ProjectBase):
    places: list[ProjectPlaceCreate] | None = None


class ProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectRead(SQLModel):
    id: int
    name: str
    description: str | None
    start_date: date | None
    is_completed: bool


class ProjectReadWithPlaces(ProjectRead):
    places: list[ProjectPlaceRead]
