import asyncio
import functools
import logging
import random
from typing import Callable


logger = logging.getLogger(__name__)

class OptimisticLockException(Exception):

    def __init__(
            self,
            entity_type: str,
            entity_id: int,
            message: str = None
    ):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.message = message or f"{entity_type} with id=[{entity_id}] was modified by another transaction"
        super().__init__(self.message)



class RetryConfig:

    def __init__(
            self,
            max_retries: int = 5,
            base_delay: float = 0.1, # 100ms
            max_delay: float = 2.0,
            exponential_base: int = 2,
            jitter: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for a given retry attempt"""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            delay *= 0.75 + random.random() * 0.5

        return delay



def optimistic_retry_async(
        conf: RetryConfig = None,
        on_conflict: Callable[[Exception, int], None] = None
):
    """Async retry decorator"""
    if conf is None:
        conf = RetryConfig()

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, conf.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except OptimisticLockException as e:
                    last_error = e

                    if attempt < conf.max_retries:
                        delay = conf.get_delay(attempt)

                        logger.info(
                            f"Optimistic lock retry. Attempt={attempt}, "
                            f"retrying in {delay:.2f}s"
                        )

                        if on_conflict:
                            on_conflict(e, attempt)

                        await asyncio.sleep(delay)

            raise last_error

        return wrapper
    return decorator
