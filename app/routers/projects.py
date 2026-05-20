from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app import crud
from app.artic_api import ArticApiError, fetch_artwork_by_id
from app.database import get_session
from app.schemas import ProjectCreate, ProjectRead, ProjectReadWithPlaces, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

MAX_PLACES_PER_PROJECT = 10


@router.post(
    "",
    response_model=ProjectReadWithPlaces,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    session: Session = Depends(get_session),
):
    places_data = project_data.places

    if places_data is not None:
        if len(places_data) < 1 or len(places_data) > MAX_PLACES_PER_PROJECT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project must contain from 1 to 10 places.",
            )

        external_ids = [place.external_id for place in places_data]

        if len(external_ids) != len(set(external_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project cannot contain the same external place more than once.",
            )

    fetched_places = []

    if places_data is not None:
        for place_data in places_data:
            try:
                artwork_data = fetch_artwork_by_id(place_data.external_id)
            except ArticApiError as error:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=str(error),
                ) from error

            if artwork_data is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"External place {place_data.external_id} does not exist.",
                )

            fetched_places.append(
                {
                    "external_id": artwork_data["external_id"],
                    "title": artwork_data["title"],
                    "notes": place_data.notes,
                }
            )

    project = crud.create_project(
        session=session,
        project_data=project_data,
    )

    for place_data in fetched_places:
        crud.create_project_place(
            session=session,
            project_id=project.id,
            external_id=place_data["external_id"],
            title=place_data["title"],
            notes=place_data["notes"],
        )

    session.refresh(project)

    return project


@router.get("", response_model=list[ProjectRead])
def read_projects(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return crud.get_projects(
        session=session,
        offset=offset,
        limit=limit,
    )


@router.get("/{project_id}", response_model=ProjectReadWithPlaces)
def read_project(
    project_id: int,
    session: Session = Depends(get_session),
):
    project = crud.get_project(
        session=session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: Session = Depends(get_session),
):
    project = crud.get_project(
        session=session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return crud.update_project(
        session=session,
        project=project,
        project_data=project_data,
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
):
    project = crud.get_project(
        session=session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    if crud.project_has_visited_places(
        session=session,
        project_id=project_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project cannot be deleted because it has visited places.",
        )

    crud.delete_project(
        session=session,
        project=project,
    )

    return None
