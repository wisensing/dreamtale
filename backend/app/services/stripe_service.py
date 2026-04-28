import stripe
from app.config import get_settings

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

PRICE_MAP = {
    "10": settings.STRIPE_PRICE_10_CREDITS,
    "25": settings.STRIPE_PRICE_25_CREDITS,
    "50": settings.STRIPE_PRICE_50_CREDITS,
    "100": settings.STRIPE_PRICE_100_CREDITS,
}


def create_checkout_session(user_id: str, pack: str, success_url: str, cancel_url: str) -> dict:
    price_id = PRICE_MAP.get(pack)
    if not price_id:
        raise ValueError(f"Invalid credit pack: {pack}")

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": user_id, "pack": pack},
    )
    return {"checkout_url": session.url, "session_id": session.id}


def verify_webhook_signature(payload: bytes, sig_header: str) -> dict:
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return event
    except stripe.error.SignatureVerificationError:
        raise ValueError("Invalid webhook signature")
