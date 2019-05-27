import sentry_sdk
import os
import logging


def init_monitoring():
    dsn = os.getenv("DILA2SQL_SENTRY_DSN")
    if dsn:
        logging.debug("initing SENTRY ...")
        sentry_sdk.init(os.getenv("DILA2SQL_SENTRY_DSN"))
    else:
        logging.debug("missing DILA2SQL_SENTRY_DSN env var, skipping init")
