# cr-ta-travel-planner-api

A FastAPI CRUD application for managing travel projects and project places.

The application allows users to create travel projects, add places from the Art Institute of Chicago API, attach notes to places, mark places as visited, and automatically mark a project as completed when all its places are visited.

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
- httpx
- Poetry
- Docker

## Features

- Create, read, update and delete travel projects
- Create a project with places in a single request
- Add places to existing projects
- Validate external places through the Art Institute of Chicago API before saving
- Update notes for project places
- Mark project places as visited
- Automatically mark a project as completed when all its places are visited
- Prevent deleting a project if any place is already visited
- Prevent adding more than 10 places to a project
- Prevent adding the same external place twice to the same project
- Swagger/OpenAPI documentation
- Docker setup for local running

## External API

This project uses the Art Institute of Chicago API.

External places are validated through the artwork detail endpoint:

```text
GET https://api.artic.edu/api/v1/artworks/{id}
```

Example valid external artwork IDs for testing:

```text
129884
27992
24645
28560
```

## Running With Docker

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON is available at:

```text
http://127.0.0.1:8000/openapi.json
```

To stop the application:

```bash
docker compose down
```

## Database

The project uses SQLite by default.

A local database file is created automatically after application startup:

```text
travel_planner.db
```

When the application is run inside Docker, the SQLite database is created inside the container filesystem.

## Project Structure

```text
app/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── artic_api.py
└── routers/
    ├── __init__.py
    ├── projects.py
    └── places.py
```

## Main Endpoints

### Projects

```text
POST   /projects
GET    /projects
GET    /projects/{project_id}
PATCH  /projects/{project_id}
DELETE /projects/{project_id}
```

### Project Places

```text
POST   /projects/{project_id}/places
GET    /projects/{project_id}/places
GET    /projects/{project_id}/places/{place_id}
PATCH  /projects/{project_id}/places/{place_id}
DELETE /projects/{project_id}/places/{place_id}
```

## Manual Testing

You can test all endpoints through Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Important: IDs in examples are sample values. After creating a project or place, use the actual `id` returned by the API.

---

## Health Check

Endpoint:

```text
GET /
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

---

## Create Project Without Places

Endpoint:

```text
POST /projects
```

Body:

```json
{
  "name": "Test project without places",
  "description": "Project created first, places will be added later",
  "start_date": "2026-06-01"
}
```

Expected result:

```text
201 Created
```

---

## Create Project With Places

Endpoint:

```text
POST /projects
```

Body:

```json
{
  "name": "Chicago art trip",
  "description": "Artworks from Art Institute API",
  "start_date": "2026-06-01",
  "places": [
    {
      "external_id": 129884,
      "notes": "Interesting artwork from Art Institute"
    },
    {
      "external_id": 27992,
      "notes": "Another artwork to visit"
    }
  ]
}
```

Expected result:

```text
201 Created
```

---

## List Projects

Endpoint:

```text
GET /projects
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

Example with pagination:

```text
GET /projects?offset=0&limit=10
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

---

## Get Single Project

Endpoint:

```text
GET /projects/{project_id}
```

Example:

```text
GET /projects/1
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

---

## Update Project

Endpoint:

```text
PATCH /projects/{project_id}
```

Example:

```text
PATCH /projects/1
```

Body:

```json
{
  "name": "Updated Chicago art trip",
  "description": "Updated project description",
  "start_date": "2026-07-01"
}
```

Expected result:

```text
200 OK
```

Partial update example:

```json
{
  "name": "Only name was updated"
}
```

---

## Delete Project

Endpoint:

```text
DELETE /projects/{project_id}
```

Example:

```text
DELETE /projects/1
```

Body:

```text
No body
```

Expected result:

```text
204 No Content
```

Note: a project cannot be deleted if any of its places are marked as visited.

---

## Add Place To Existing Project

Endpoint:

```text
POST /projects/{project_id}/places
```

Example:

```text
POST /projects/1/places
```

Body:

```json
{
  "external_id": 129884,
  "notes": "Added later through places endpoint"
}
```

Expected result:

```text
201 Created
```

Another example:

```json
{
  "external_id": 27992,
  "notes": "Second place added to the project"
}
```

---

## List Places For Project

Endpoint:

```text
GET /projects/{project_id}/places
```

Example:

```text
GET /projects/1/places
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

---

## Get Single Place In Project

Endpoint:

```text
GET /projects/{project_id}/places/{place_id}
```

Example:

```text
GET /projects/1/places/1
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

---

## Update Place Notes

Endpoint:

```text
PATCH /projects/{project_id}/places/{place_id}
```

Example:

```text
PATCH /projects/1/places/1
```

Body:

```json
{
  "notes": "Updated notes for this place"
}
```

Expected result:

```text
200 OK
```

---

## Mark Place As Visited

Endpoint:

```text
PATCH /projects/{project_id}/places/{place_id}
```

Example:

```text
PATCH /projects/1/places/1
```

Body:

```json
{
  "visited": true
}
```

Expected result:

```text
200 OK
```

Note: when all places in a project are marked as visited, the project is automatically marked as completed.

---

## Update Place Notes And Visited Status

Endpoint:

```text
PATCH /projects/{project_id}/places/{place_id}
```

Example:

```text
PATCH /projects/1/places/1
```

Body:

```json
{
  "notes": "Visited and updated notes",
  "visited": true
}
```

Expected result:

```text
200 OK
```

---

## Delete Place From Project

Endpoint:

```text
DELETE /projects/{project_id}/places/{place_id}
```

Example:

```text
DELETE /projects/1/places/1
```

Body:

```text
No body
```

Expected result:

```text
204 No Content
```

---

# Business Rules To Check

## Project Place Limit

A project cannot contain more than 10 places.

Endpoint:

```text
POST /projects/{project_id}/places
```

Body:

```json
{
  "external_id": 129884,
  "notes": "This should fail if the project already has 10 places"
}
```

Expected result:

```text
400 Bad Request
```

---

## Duplicate External Place

The same external artwork cannot be added twice to the same project.

Endpoint:

```text
POST /projects/{project_id}/places
```

Body:

```json
{
  "external_id": 129884,
  "notes": "This should fail if this external_id already exists in the project"
}
```

Expected result:

```text
400 Bad Request
```

---

## Invalid External Place

The API validates that an external artwork exists before saving it.

Endpoint:

```text
POST /projects/{project_id}/places
```

Body:

```json
{
  "external_id": 999999999,
  "notes": "This should fail because this external artwork probably does not exist"
}
```

Expected result:

```text
400 Bad Request
```

---

## Delete Project With Visited Place

A project cannot be deleted if any place is marked as visited.

Step 1 endpoint:

```text
PATCH /projects/{project_id}/places/{place_id}
```

Step 1 body:

```json
{
  "visited": true
}
```

Step 2 endpoint:

```text
DELETE /projects/{project_id}
```

Step 2 body:

```text
No body
```

Expected result:

```text
400 Bad Request
```

---

# Suggested Full Test Flow

This flow can be used to check the main business logic.

## Step 1: Create Project Without Places

Endpoint:

```text
POST /projects
```

Body:

```json
{
  "name": "Full test project",
  "description": "Project for testing all main actions",
  "start_date": "2026-06-01"
}
```

Expected result:

```text
201 Created
```

Save returned project `id`.

---

## Step 2: Add Place To Project

Endpoint:

```text
POST /projects/{project_id}/places
```

Example:

```text
POST /projects/1/places
```

Body:

```json
{
  "external_id": 129884,
  "notes": "First place added to the project"
}
```

Expected result:

```text
201 Created
```

Save returned place `id`.

---

## Step 3: Get Project With Places

Endpoint:

```text
GET /projects/{project_id}
```

Example:

```text
GET /projects/1
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

The response should include the added place.

---

## Step 4: Mark Place As Visited

Endpoint:

```text
PATCH /projects/{project_id}/places/{place_id}
```

Example:

```text
PATCH /projects/1/places/1
```

Body:

```json
{
  "visited": true
}
```

Expected result:

```text
200 OK
```

---

## Step 5: Check Project Completion

Endpoint:

```text
GET /projects/{project_id}
```

Example:

```text
GET /projects/1
```

Body:

```text
No body
```

Expected result:

```text
200 OK
```

If all places are visited, `is_completed` should be `true`.

---

## Step 6: Try To Delete Completed Project

Endpoint:

```text
DELETE /projects/{project_id}
```

Example:

```text
DELETE /projects/1
```

Body:

```text
No body
```

Expected result:

```text
400 Bad Request
```

The project should not be deleted because it has a visited place.

## Notes

- The application creates database tables automatically on startup.
- SQLite is used for simplicity.
- Swagger UI can be used instead of a Postman collection.
- Project places are validated through the Art Institute of Chicago API before being saved.
- The application can be started locally with Docker using `docker compose up --build`.
