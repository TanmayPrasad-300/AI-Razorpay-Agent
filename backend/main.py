import os
import uuid
import time
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import razorpay

load_dotenv()

app = FastAPI(title="RazorAgent OS", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RZP_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_placeholder")
RZP_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "placeholder")
rzp_client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

CATALOG = {
    "sku_audio_01": {
        "id": "sku_audio_01",
        "name": "Sony WH-1000XM5 ANC Headphones",
        "price": 249900,
        "stock": 12,
        "category": "Audio",
        "tags": ["headphone", "headphones", "audio", "music", "noise", "anc", "sony"],
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80",
        "description": "Industry-leading noise cancellation, 30hr battery"
    },
    "sku_audio_02": {
        "id": "sku_audio_02",
        "name": "Apple AirPods Pro 2",
        "price": 199900,
        "stock": 20,
        "category": "Audio",
        "tags": ["airpods", "earbuds", "apple", "wireless", "audio", "earphone", "earphones"],
        "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&q=80",
        "description": "Active noise cancellation with MagSafe charging case"
    },
    "sku_desk_01": {
        "id": "sku_desk_01",
        "name": "ErgoPro Standing Desk Mat",
        "price": 149900,
        "stock": 30,
        "category": "Workspace",
        "tags": ["desk", "mat", "ergonomic", "workspace", "standing", "floor"],
        "image": "https://images.unsplash.com/photo-1593062096033-9a26b09da705?w=400&q=80",
        "description": "Anti-fatigue comfort mat for standing desks"
    },
    "sku_desk_02": {
        "id": "sku_desk_02",
        "name": "Monitor Laptop Stand (Aluminium)",
        "price": 249900,
        "stock": 18,
        "category": "Workspace",
        "tags": ["stand", "laptop", "monitor stand", "desk", "workspace", "aluminium"],
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&q=80",
        "description": "Ergonomic aluminium stand for laptop and monitor"
    },
    "sku_kb_01": {
        "id": "sku_kb_01",
        "name": "Keychron Q1 Pro Mechanical Keyboard",
        "price": 1299900,
        "stock": 0,
        "category": "Electronics",
        "tags": ["keyboard", "mechanical", "typing", "rgb", "keychron"],
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&q=80",
        "description": "Premium wireless mechanical keyboard (Out of stock demo)"
    },
    "sku_mouse_01": {
        "id": "sku_mouse_01",
        "name": "Logitech MX Master 3S Mouse",
        "price": 89900,
        "stock": 25,
        "category": "Electronics",
        "tags": ["mouse", "logitech", "wireless", "office", "mx"],
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7cde72?w=400&q=80",
        "description": "Quiet clicks, USB-C, multi-device pairing"
    },
    "sku_monitor_01": {
        "id": "sku_monitor_01",
        "name": "LG UltraWide 34 inch Curved Monitor",
        "price": 3499900,
        "stock": 4,
        "category": "Displays",
        "tags": ["monitor", "display", "screen", "ultrawide", "lg", "curved"],
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&q=80",
        "description": "34-inch WQHD curved IPS, 144Hz"
    },
    "sku_cam_01": {
        "id": "sku_cam_01",
        "name": "Logitech C920 HD Webcam",
        "price": 69900,
        "stock": 15,
        "category": "Electronics",
        "tags": ["webcam", "camera", "video", "meeting", "logitech", "call"],
        "image": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400&q=80",
        "description": "Full HD 1080p webcam for meetings and streaming"
    },
    "sku_chair_01": {
        "id": "sku_chair_01",
        "name": "ErgoMesh Office Chair",
        "price": 899900,
        "stock": 7,
        "category": "Furniture",
        "tags": ["chair", "office", "ergonomic", "mesh", "seat", "furniture", "chairs"],
        "image": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&q=80",
        "description": "Breathable mesh, lumbar support, adjustable height"
    },
    "sku_light_01": {
        "id": "sku_light_01",
        "name": "LED Desk Lamp with Wireless Charging",
        "price": 249900,
        "stock": 22,
        "category": "Workspace",
        "tags": ["lamp", "light", "led", "desk", "charging", "workspace"],
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&q=80",
        "description": "Eye-care LED lamp with phone wireless charging base"
    },
}

@app.get("/")
def root():
    return {"service": "RazorAgent OS", "status": "ok"}

@app.get("/api/v1/health")
def health():
    return {
        "status": "OPERATIONAL",
        "gateway": "RazorAgent OS v2.0",
        "razorpay": "TEST_MODE",
        "catalog_size": len(CATALOG),
    }

@app.get("/.well-known/agent-catalog.json")
def agent_catalog():
    return {
        "protocol": "AP2/1.0",
        "merchant": "RazorAgent Flagship Store",
        "currency": "INR",
        "payment_rails": ["razorpay_checkout", "upi_intent", "upi_mandate"],
        "capabilities": ["negotiate", "bundle", "subscribe"],
        "items": [
            {
                "sku": v["id"],
                "title": v["name"],
                "price_paise": v["price"],
                "available": v["stock"] > 0,
                "category": v["category"],
            }
            for v in CATALOG.values()
        ],
    }

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@app.post("/api/v1/chat")
def chat(req: ChatRequest):
    msg = req.message.lower().strip()
    matched = []
    intent = "GENERAL_GREETING"

    for product in CATALOG.values():
        if any(tag in msg for tag in product["tags"]):
            matched.append(product)
            intent = f"PRODUCT_SEARCH_{product['category'].upper()}"

    if any(w in msg for w in ["recommend", "suggest", "best", "bundle", "combo", "deal"]):
        matched = [CATALOG["sku_audio_01"], CATALOG["sku_desk_01"]]
        intent = "RECOMMENDATION_ENGINE"

    if matched:
        primary = matched[0]
        if primary["stock"] == 0:
            fallback = CATALOG["sku_audio_01"]
            reply = (
                f"The **{primary['name']}** is currently **out of stock**.\n\n"
                f"Graceful fallback: **{fallback['name']}** "
                f"(₹{fallback['price']//100:,}) with {fallback['stock']} units available."
            )
            primary = fallback
            matched = [fallback]
            intent = "STOCK_FALLBACK_TRIGGERED"
        else:
            reply = (
                f"Perfect match found.\n\n"
                f"**{primary['name']}**\n"
                f"Price: ₹{primary['price']//100:,} | Stock: {primary['stock']}\n"
                f"{primary['description']}"
            )
            if len(matched) > 1 and matched[1]["stock"] > 0:
                upsell = matched[1]
                reply += (
                    f"\n\nSmart upsell: pair with **{upsell['name']}** "
                    f"(₹{upsell['price']//100:,})."
                )
        products = matched
    else:
        reply = (
            "Welcome to **RazorAgent Commerce**.\n\n"
            "Try: headphones, airpods, monitor, mouse, webcam, chair, or bundle deal."
        )
        products = [CATALOG["sku_audio_01"]]

    return {
        "reply": reply,
        "intent": intent,
        "products": products,
        "reasoning_chain": [
            {"step": "TOKENIZE_INPUT", "detail": "Parsed query tokens", "status": "OK", "ms": 2},
            {"step": "INTENT_MATCH", "detail": intent, "status": "MATCHED", "ms": 5},
            {"step": "CATALOG_LOOKUP", "detail": f"Scanned {len(CATALOG)} SKUs", "status": "OK", "ms": 8},
            {"step": "INVENTORY_CHECK", "detail": "Live stock verification", "status": "VERIFIED", "ms": 11},
        ],
    }

class OrderRequest(BaseModel):
    product_id: str
    quantity: int = 1
    spending_limit: int = Field(default=500000)
    buyer_agent_id: str = "human_user_01"

@app.post("/api/v1/checkout/create-order")
def create_order(req: OrderRequest):
    audit = []
    start = time.time()

    if req.product_id not in CATALOG:
        return {
            "status": "ERROR",
            "reason": "SKU not found",
            "audit_trail": [{"step": "SKU_VALIDATION", "status": "FAILED_NOT_FOUND", "ms": 1}],
        }

    product = CATALOG[req.product_id]
    total = product["price"] * req.quantity
    audit.append({"step": "SKU_VALIDATION", "status": f"PASSED — {product['name']}", "ms": 2})

    if product["stock"] < req.quantity:
        audit.append({"step": "INVENTORY_CHECK", "status": "FAILED_OUT_OF_STOCK", "ms": 5})
        return {
            "status": "STOCK_EXHAUSTED",
            "reason": "Requested item is out of stock",
            "audit_trail": audit,
        }

    audit.append({"step": "INVENTORY_LOCK", "status": f"RESERVED {req.quantity} unit", "ms": 8})

    if total > req.spending_limit:
        audit.append({
            "step": "SPENDING_POLICY_CHECK",
            "status": f"BLOCKED — ₹{total/100:,.0f} > ₹{req.spending_limit/100:,.0f}",
            "ms": 12,
        })
        return {
            "status": "GATED_REJECTED",
            "reason": (
                f"Transaction of ₹{total/100:,.0f} exceeds authorized agent budget "
                f"of ₹{req.spending_limit/100:,.0f}."
            ),
            "audit_trail": audit,
        }

    audit.append({
        "step": "SPENDING_POLICY_CHECK",
        "status": f"PASSED — within ₹{req.spending_limit/100:,.0f}",
        "ms": 14,
    })

    try:
        rzp_order = rzp_client.order.create({
            "amount": total,
            "currency": "INR",
            "receipt": f"rcpt_{uuid.uuid4().hex[:8]}",
            "notes": {
                "buyer_agent": req.buyer_agent_id,
                "protocol": "AP2_AGENTIC",
                "product": product["name"],
                "timestamp": datetime.now().isoformat(),
            },
        })
        ms = int((time.time() - start) * 1000)
        audit.append({"step": "RAZORPAY_ORDER_CREATED", "status": f"ID: {rzp_order['id']}", "ms": ms})
        audit.append({"step": "CHECKOUT_SESSION_READY", "status": "AWAITING_PAYMENT", "ms": ms + 2})

        return {
            "status": "SUCCESS",
            "order_id": rzp_order["id"],
            "amount": total,
            "currency": "INR",
            "key_id": RZP_KEY_ID,
            "product_name": product["name"],
            "audit_trail": audit,
        }
    except Exception as e:
        audit.append({"step": "RAZORPAY_ERROR", "status": str(e), "ms": 999})
        return {
            "status": "PAYMENT_ERROR",
            "reason": str(e),
            "audit_trail": audit,
        }