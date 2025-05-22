import httpx

async def fetch_raw_content(url: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP error while fetching {url}: {str(e)}")
