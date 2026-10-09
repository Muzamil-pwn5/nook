from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.agent import sessions
from app.database.connection import engine
from app.database.models import Order, Product

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def _day_key(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).date().isoformat()


@router.get("/summary")
def dashboard_summary():
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=6)
    with Session(engine) as db:
        product_count = db.scalar(select(func.count(Product.id))) or 0
        inventory_units = db.scalar(select(func.coalesce(func.sum(Product.stock_quantity), 0))) or 0
        order_count = db.scalar(select(func.count(Order.id))) or 0
        revenue = db.scalar(select(func.coalesce(func.sum(Order.total_amount), 0))) or 0
        status_rows = db.execute(select(Order.status, func.count(Order.id)).group_by(Order.status)).all()
        category_rows = db.execute(select(Product.category, func.count(Product.id)).group_by(Product.category).order_by(func.count(Product.id).desc())).all()
        recent_orders = db.execute(select(Order).order_by(Order.created_at.desc()).limit(8)).scalars().all()
        order_days = Counter()
        for created_at, in db.execute(select(Order.created_at).where(Order.created_at >= start)).all():
            order_days[_day_key(created_at)] += 1

    active_sessions = 0
    message_count = 0
    pending_approvals = 0
    events = []
    for session_id, session in sessions.items():
        last_activity = session.get("last_activity", session.get("created_at", now))
        if last_activity >= now - timedelta(minutes=30):
            active_sessions += 1
        message_count += session.get("message_count", 0)
        pending_approvals += len(session.get("pending_approvals", {}))
        for event in session.get("events", []):
            if event["timestamp"] >= start:
                events.append({**event, "session_id": session_id})

    timeline = []
    for offset in range(6, -1, -1):
        day = (now - timedelta(days=offset)).date().isoformat()
        timeline.append({"date": day, "orders": order_days.get(day, 0), "conversations": sum(1 for session in sessions.values() if _day_key(session.get("last_activity", now)) == day)})

    recent_activity = sorted(events, key=lambda item: item["timestamp"], reverse=True)[:10]
    for item in recent_activity:
        item["timestamp"] = item["timestamp"].isoformat()

    return {
        "generated_at": now.isoformat(),
        "overview": {
            "product_count": int(product_count),
            "inventory_units": int(inventory_units),
            "order_count": int(order_count),
            "revenue": float(revenue),
            "active_sessions": active_sessions,
            "message_count": message_count,
            "pending_approvals": pending_approvals,
        },
        "orders_by_status": [{"status": status, "count": int(count)} for status, count in status_rows],
        "catalog_by_category": [{"category": category or "Uncategorized", "count": int(count)} for category, count in category_rows],
        "timeline": timeline,
        "recent_activity": recent_activity,
        "recent_orders": [{"id": order.id, "status": order.status, "total": float(order.total_amount), "created_at": order.created_at.isoformat()} for order in recent_orders],
    }
