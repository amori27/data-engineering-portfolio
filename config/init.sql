CREATE TABLE IF NOT EXISTS pageviews (
    id              BIGSERIAL PRIMARY KEY,
    event_id        UUID NOT NULL UNIQUE,
    user_id         VARCHAR(64) NOT NULL,
    page_url        TEXT NOT NULL,
    page_title      VARCHAR(255),
    referrer        TEXT,
    user_agent      TEXT,
    ip_address      VARCHAR(45),
    country         VARCHAR(2),
    device_type     VARCHAR(16),
    browser         VARCHAR(32),
    event_type      VARCHAR(32) NOT NULL DEFAULT 'pageview',
    session_id      VARCHAR(64) NOT NULL,
    ingested_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_timestamp TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS pageview_agg (
    id            BIGSERIAL PRIMARY KEY,
    window_start  TIMESTAMP NOT NULL,
    window_end    TIMESTAMP NOT NULL,
    page_url      TEXT NOT NULL,
    view_count    BIGINT NOT NULL DEFAULT 0,
    unique_users  BIGINT NOT NULL DEFAULT 0,
    UNIQUE (window_start, page_url)
);

CREATE INDEX idx_pageviews_timestamp ON pageviews (event_timestamp DESC);
CREATE INDEX idx_pageviews_country ON pageviews (country);
CREATE INDEX idx_agg_window ON pageview_agg (window_start, window_end);
