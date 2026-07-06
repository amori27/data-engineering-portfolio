CREATE TABLE IF NOT EXISTS pageviews (
    event_id UUID PRIMARY KEY,
    user_id VARCHAR(64),
    page_url TEXT,
    page_title VARCHAR(255),
    referrer TEXT,
    user_agent TEXT,
    ip_address VARCHAR(45),
    country VARCHAR(2),
    device_type VARCHAR(16),
    browser VARCHAR(32),
    timestamp TIMESTAMP,
    event_type VARCHAR(32),
    session_id VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS pageview_agg (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    page_url TEXT,
    view_count BIGINT,
    unique_users BIGINT,
    PRIMARY KEY (window_start, page_url)
);
