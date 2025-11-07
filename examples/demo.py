"""
Simple demonstration of the `retry` helper utilities.

Run this script directly to see both the decorator-based retry and the
`retry_call` helper in action.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict

from retry import retry, retry_call


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger("retry-demo")


class TransientError(RuntimeError):
    """Custom error to simulate a flaky dependency."""


@dataclass
class UnreliableService:
    """Pretend service that fails a configurable number of times."""

    failures_before_success: int
    metadata: Dict[str, Any] | None = None

    def request(self) -> Dict[str, Any]:
        if self.failures_before_success > 0:
            self.failures_before_success -= 1
            raise TransientError("simulated intermittent failure")

        return {"status": "ok", "metadata": self.metadata or {}}


# --- Using the decorator-based API -------------------------------------------------

service_for_decorator = UnreliableService(failures_before_success=2)


@retry(
    exceptions=TransientError,
    tries=4,
    delay=0.2,
    backoff=2,
    jitter=(0, 0.1),
    logger=LOGGER,
)
def fetch_with_decorator() -> Dict[str, Any]:
    """
    Wraps `service_for_decorator.request` with retry logic.

    The first two attempts will raise `TransientError`, but the third attempt
    succeeds and the function returns.
    """

    response = service_for_decorator.request()
    LOGGER.info("Decorated call succeeded: %s", response)
    return response


# --- Using the functional helper ---------------------------------------------------

def fetch_with_retry_call() -> Dict[str, Any]:
    """
    Shows the direct helper API by resetting the failure counter and calling
    `retry_call` manually.
    """

    service = UnreliableService(failures_before_success=2, metadata={"source": "retry_call"})
    return retry_call(
        f=service.request,
        exceptions=TransientError,
        tries=4,
        delay=0.2,
        backoff=2,
        jitter=(0, 0.1),
        logger=LOGGER,
    )


def main() -> None:
    try:
        result = fetch_with_decorator()
        print("Decorated call result:", result)
    except TransientError as exc:
        print("Decorated call failed:", exc)

    try:
        result = fetch_with_retry_call()
        print("retry_call result:", result)
    except TransientError as exc:
        print("retry_call failed:", exc)


if __name__ == "__main__":
    main()
