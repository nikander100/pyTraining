from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total", 
    "Total number of HTTP requests", 
    ["method", "endpoint", "endpoint_error"]
)

REQUEST_TIME = Histogram(
    "http_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"]
)