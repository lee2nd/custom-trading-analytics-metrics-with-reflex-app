import os

import reflex as rx

# Reflex Cloud's own CORS check only accepts the backend's own origin unless
# `deploy_url` names the frontend's public origin (prod mode narrows
# cors_allowed_origins to it); without this the deployed WebSocket handshake
# is rejected with "<frontend origin> is not an accepted origin.".
# Override via the REFLEX_DEPLOY_URL env var if the assigned domain changes.
DEPLOY_URL = os.getenv(
    "REFLEX_DEPLOY_URL",
    "https://custom-trading-analytics-metrics-with-refle-lime-grass.reflex.run",
)

config = rx.Config(
    app_name="custom_trading_analytics_metrics_with_reflex_app",
    deploy_url=DEPLOY_URL,
)
