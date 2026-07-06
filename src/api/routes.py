from fastapi import APIRouter, HTTPException, Query

from src.api.database import fetch_all

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok", "service": "clickstream-analytics"}


@router.get("/pageviews/recent")
def recent_pageviews(limit: int = Query(50, ge=1, le=1000)):
    rows = fetch_all(
        "SELECT * FROM pageviews ORDER BY event_timestamp DESC LIMIT %s",
        (limit,),
    )
    return {"count": len(rows), "results": rows}


@router.get("/pageviews/top-pages")
def top_pages(min_views: int = Query(1, ge=1)):
    rows = fetch_all(
        """
        SELECT page_url,
               SUM(view_count) AS total_views,
               SUM(unique_users) AS total_users
        FROM pageview_agg
        GROUP BY page_url
        HAVING SUM(view_count) >= %s
        ORDER BY total_views DESC
        LIMIT 100
        """,
        (min_views,),
    )
    return {"count": len(rows), "results": rows}


@router.get("/pageviews/country-breakdown")
def country_breakdown():
    rows = fetch_all(
        """
        SELECT country, COUNT(*) AS cnt
        FROM pageviews
        GROUP BY country
        ORDER BY cnt DESC
        """
    )
    return {"count": len(rows), "results": rows}


@router.get("/pageviews/country/{country_code}")
def country_detail(country_code: str, limit: int = Query(50, ge=1, le=500)):
    rows = fetch_all(
        """
        SELECT * FROM pageviews
        WHERE country = %s
        ORDER BY event_timestamp DESC
        LIMIT %s
        """,
        (country_code.upper(), limit),
    )
    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No pageviews found for country '{country_code}'",
        )
    return {"country": country_code.upper(), "count": len(rows), "results": rows}
