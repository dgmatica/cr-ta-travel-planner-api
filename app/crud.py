from sqlmodel import Session, select

from app.models import Project, ProjectPlace
from app.schemas import ProjectCreate, ProjectPlaceUpdate, ProjectUpdate


def get_projects(session: Session, offset: int = 0, limit: int = 100) -> list[Project]:
    statement = select(Project).offset(offset).limit(limit)
    return list(session.exec(statement).all())


def get_project(session: Session, project_id: int) -> Project | None:
    return session.get(Project, project_id)


def create_project(session: Session, project_data: ProjectCreate) -> Project:
    project = Project(
        name=project_data.name,
        description=project_data.description,
        start_date=project_data.start_date,
        is_completed=False,
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


def update_project(
    session: Session,
    project: Project,
    project_data: ProjectUpdate,
) -> Project:
    update_data = project_data.model_dump(exclude_unset=True)

    for field_name, value in update_data.items():
        setattr(project, field_name, value)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()


def get_project_places(session: Session, project_id: int) -> list[ProjectPlace]:
    statement = select(ProjectPlace).where(ProjectPlace.project_id == project_id)
    return list(session.exec(statement).all())


def get_project_place(
    session: Session,
    project_id: int,
    place_id: int,
) -> ProjectPlace | None:
    statement = (
        select(ProjectPlace)
        .where(ProjectPlace.project_id == project_id)
        .where(ProjectPlace.id == place_id)
    )

    return session.exec(statement).first()


def get_project_place_by_external_id(
    session: Session,
    project_id: int,
    external_id: int,
) -> ProjectPlace | None:
    statement = (
        select(ProjectPlace)
        .where(ProjectPlace.project_id == project_id)
        .where(ProjectPlace.external_id == external_id)
    )

    return session.exec(statement).first()


def count_project_places(session: Session, project_id: int) -> int:
    places = get_project_places(session=session, project_id=project_id)
    return len(places)


def create_project_place(
    session: Session,
    project_id: int,
    external_id: int,
    title: str,
    notes: str | None = None,
) -> ProjectPlace:
    place = ProjectPlace(
        project_id=project_id,
        external_id=external_id,
        title=title,
        notes=notes,
        visited=False,
    )

    session.add(place)
    session.commit()
    session.refresh(place)

    refresh_project_completion(session=session, project_id=project_id)

    return place


def update_project_place(
    session: Session,
    place: ProjectPlace,
    place_data: ProjectPlaceUpdate,
) -> ProjectPlace:
    update_data = place_data.model_dump(exclude_unset=True)

    for field_name, value in update_data.items():
        setattr(place, field_name, value)

    session.add(place)
    session.commit()
    session.refresh(place)

    refresh_project_completion(session=session, project_id=place.project_id)

    return place


def delete_project_place(session: Session, place: ProjectPlace) -> None:
    project_id = place.project_id

    session.delete(place)
    session.commit()

    refresh_project_completion(session=session, project_id=project_id)


def project_has_visited_places(session: Session, project_id: int) -> bool:
    places = get_project_places(session=session, project_id=project_id)

    for place in places:
        if place.visited:
            return True

    return False


def refresh_project_completion(session: Session, project_id: int) -> Project | None:
    project = get_project(session=session, project_id=project_id)

    if project is None:
        return None

    places = get_project_places(session=session, project_id=project_id)

    if not places:
        project.is_completed = False
    else:
        project.is_completed = all(place.visited for place in places)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project
