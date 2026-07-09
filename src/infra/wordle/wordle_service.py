import httpx
from datetime import date

_word_cache: str | None = None
_cache_date: date | None = None


def get_daily_word() -> str | None:
    global _word_cache, _cache_date
    today = date.today()
    if _cache_date == today and _word_cache is not None:
        return _word_cache
    try:
        resp = httpx.get(f"https://www.nytimes.com/svc/wordle/v2/{today}.json")
        resp.raise_for_status()
        _word_cache = resp.json()["solution"]
        _cache_date = today
        return _word_cache
    except Exception:
        return None
