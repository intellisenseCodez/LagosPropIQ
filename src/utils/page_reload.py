
import random
import time
from requests import RequestException


def with_retries(func, max_retries: int = 3, backoff_factor: float = 1.5, logger=None):
    "Allows automatic retry when a site fail"
    for attempt in range(max_retries):
        try:
            return func()
        except RequestException as e:
            wait_time = backoff_factor ** attempt + random.uniform(0, 0.5)
            if logger:
                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                    f"Retrying in {wait_time:.2f}s..."
                )
            time.sleep(wait_time)
    if logger:
        logger.error(f"All {max_retries} retry attempts failed for {func.__name__}.")
    return None
