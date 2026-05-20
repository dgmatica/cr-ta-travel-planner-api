from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud
from app.artic_api import ArticApiError, fetch_artwork_by_id
from app.database import get_session
from app.schemas import ProjectPlaceCreate, ProjectPlaceRead, ProjectPlaceUpdate

router = APIRouter(
    prefix="/projects/{project_id}/places",
    tags=["places"],
)

MAX_PLACES_PER_PROJECT = 10


@router.post(
    "",
    response_model=ProjectPlaceRead,
    status_code=status.HTTP_201_CREATED,
)
def add_place_to_project(
    project_id: int,
    place_data: ProjectPlaceCreate,
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

    places_count = crud.count_project_places(
        session=session,
        project_id=project_id,
    )

    if places_count >= MAX_PLACES_PER_PROJECT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project cannot contain more than 10 places.",
        )

    existing_place = crud.get_project_place_by_external_id(
        session=session,
        project_id=project_id,
        external_id=place_data.external_id,
    )

    if existing_place is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This external place already exists in the project.",
        )

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

    return crud.create_project_place(
        session=session,
        project_id=project_id,
        external_id=artwork_data["external_id"],
        title=artwork_data["title"],
        notes=place_data.notes,
    )


@router.get("", response_model=list[ProjectPlaceRead])
def read_project_places(
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

    return crud.get_project_places(
        session=session,
        project_id=project_id,
    )


@router.get("/{place_id}", response_model=ProjectPlaceRead)
def read_project_place(
    project_id: int,
    place_id: int,
    session: Session = Depends(get_session),
):
    place = crud.get_project_place(
        session=session,
        project_id=project_id,
        place_id=place_id,
    )

    if place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found.",
        )

    return place


@router.patch("/{place_id}", response_model=ProjectPlaceRead)
def update_project_place(
    project_id: int,
    place_id: int,
    place_data: ProjectPlaceUpdate,
    session: Session = Depends(get_session),
):
    place = crud.get_project_place(
        session=session,
        project_id=project_id,
        place_id=place_id,
    )

    if place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found.",
        )

    return crud.update_project_place(
        session=session,
        place=place,
        place_data=place_data,
    )


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_place(
    project_id: int,
    place_id: int,
    session: Session = Depends(get_session),
):
    place = crud.get_project_place(
        session=session,
        project_id=project_id,
        place_id=place_id,
    )

    if place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found.",
        )

    crud.delete_project_place(
        session=session,
        place=place,
    )

    return None
