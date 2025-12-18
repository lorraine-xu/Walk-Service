import json
import uuid
import os
from datetime import datetime
from typing import Optional

try:
    from google.cloud import pubsub_v1
except ImportError:
    pubsub_v1 = None  # Allows local dev without GCP installed


PROJECT_ID = os.getenv("GCP_PROJECT", "w4153-walk-service")
TOPIC_ID = os.getenv("PUBSUB_TOPIC", "walk-events")

_publisher: Optional["pubsub_v1.PublisherClient"] = None
_topic_path: Optional[str] = None


def encode(obj):
    """Convert UUIDs, datetimes, and other objects to JSON-safe formats."""
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    return obj


def _get_publisher():
    """
    Lazily initialize Pub/Sub publisher.
    Skips initialization in local/dev environments without credentials.
    """
    global _publisher, _topic_path

    # Local/dev mode: do nothing
    if not pubsub_v1 or not PROJECT_ID or not TOPIC_ID:
        return None, None

    if _publisher is None:
        _publisher = pubsub_v1.PublisherClient()
        _topic_path = _publisher.topic_path(PROJECT_ID, TOPIC_ID)

    return _publisher, _topic_path


def publish_event(event_type: str, data: dict):
    publisher, topic_path = _get_publisher()

    # Local/dev mode: log instead of publishing
    if publisher is None:
        print(f"[DEV] Event skipped: {event_type}")
        return None

    message = {
        "event_type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }

    message_json = json.dumps(message, default=encode)
    message_bytes = message_json.encode("utf-8")

    future = publisher.publish(topic_path, message_bytes)
    print(f"Published event: {message_json}")

    return future.result()