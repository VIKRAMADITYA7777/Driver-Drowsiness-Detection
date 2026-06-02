import asyncio
import json
from typing import Any, Dict, List
from app.config import settings

import httpx
import aiosmtplib
from email.message import EmailMessage


async def _send_webhooks(payload: Dict[str, Any]):
    urls: List[str] = settings.WEBHOOK_URLS or []
    if not urls:
        return
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for u in urls:
            tasks.append(client.post(str(u), json=payload))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


async def _send_email(subject: str, body: str, to: List[str]):
    if not settings.SMTP_SERVER or not to:
        return None
    message = EmailMessage()
    message["From"] = settings.SMTP_USER or "noreply@example.com"
    message["To"] = ", ".join(to)
    message["Subject"] = subject
    message.set_content(body)

    return await aiosmtplib.send(
        message,
        hostname=settings.SMTP_SERVER,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )


def _send_sms_placeholder(message: str, to_provider: str | None = None):
    # Integrate with Twilio or other SMS providers. Placeholder logs the message.
    # Example: use `twilio` library and settings.SMS_API_KEY.
    print("[SMS PLACEHOLDER]", message)


def send_alert(session_id: int, level: str, message: str, metadata: Dict[str, Any] | None = None):
    payload = {
        "session_id": session_id,
        "level": level,
        "message": message,
        "metadata": metadata or {},
    }

    async def _dispatch():
        tasks = []
        tasks.append(_send_webhooks(payload))
        if settings.ALERT_EMAIL_TO:
            subject = f"Alert: {level}"
            body = f"{message}\n\nMetadata:\n{json.dumps(metadata or {}, indent=2)}"
            tasks.append(_send_email(subject, body, settings.ALERT_EMAIL_TO))
        await asyncio.gather(*tasks, return_exceptions=True)

    try:
        asyncio.run(_dispatch())
    except RuntimeError:
        # If there's already a running loop, schedule the task
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(_dispatch())
        else:
            asyncio.run(_dispatch())
