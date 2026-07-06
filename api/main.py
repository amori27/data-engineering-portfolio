from fastapi import FastAPI, Query
import psycopg2

app = FastAPI(title="Clickstream Analytics API")

DB = "dbname=analytics user=user password=pass host=localhost port=5432"


def fetch(query, params=None):
    conn = psycopg2.connect(DB)
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(cols, r)) for r in rows]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/pageviews/recent")
def recent_pageviews(limit: int = Query(50, ge=1, le=500)):
    return fetch("SELECT * FROM pageviews ORDER BY timestamp DESC LIMIT %s", (limit,))


@app.get("/api/pageviews/top-pages")
def top_pages(min_views: int = Query(1, ge=1)):
    return fetch(
        """
        SELECT page_url, SUM(view_count) as total_views,
               SUM(unique_users) as total_users
        FROM pageview_agg
        GROUP BY page_url
        HAVING SUM(view_count) >= %s
        ORDER BY total_views DESC
        """,
        (min_views,),
    )


@app.get("/api/pageviews/country-breakdown")
def country_breakdown():
    return fetch(
        """
        SELECT country, COUNT(*) as cnt
        FROM pageviews
        GROUP BY country
        ORDER BY cnt DESC
        """
    )
