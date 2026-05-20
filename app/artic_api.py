import httpx

ARTIC_BASE_URL = "https://api.artic.edu/api/v1"


class ArticApiError(Exception):
    pass


def fetch_artwork_by_id(external_id: int) -> dict | None:
    url = f"{ARTIC_BASE_URL}/artworks/{external_id}"

    try:
        response = httpx.get(url, timeout=10)
    except httpx.RequestError as error:
        raise ArticApiError(
            f"[{url}] [API UNAVAILABLE] Art Institute API is unavailable"
        ) from error

    if response.status_code == 404:
        return None

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise ArticApiError(
            f"[{url}] [API ERROR] Art Institute API returned an error"
        ) from error

    response_data = response.json()
    artwork_data = response_data.get("data")

    if artwork_data is None:
        return None

    artwork_id = artwork_data.get("id")
    title = artwork_data.get("title") or "Untitled"

    if artwork_id is None:
        return None

    return {
        "external_id": artwork_id,
        "title": title,
    }
