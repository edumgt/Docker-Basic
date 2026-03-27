import os
import time
from contextlib import asynccontextmanager
from enum import Enum

import psycopg
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field


DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "app")
DB_USER = os.getenv("DB_USER", "app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app1234")


def get_conninfo() -> str:
    return (
        f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} "
        f"user={DB_USER} password={DB_PASSWORD}"
    )


class OrderStatus(str, Enum):
    created = "CREATED"
    completed = "COMPLETED"


class DeliveryStatus(str, Enum):
    requested = "REQUESTED"
    preparing = "PREPARING"
    in_transit = "IN_TRANSIT"
    delivered = "DELIVERED"


class OrderCreate(BaseModel):
    customer_name: str = Field(..., examples=["Alice"])
    product_name: str = Field(..., examples=["Docker Handbook"])
    quantity: int = Field(..., ge=1, examples=[2])


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    product_name: str
    quantity: int
    status: OrderStatus
    created_at: str


class DeliveryCreate(BaseModel):
    address: str = Field(..., examples=["Seoul, Gangnam-gu"])


class DeliveryResponse(BaseModel):
    id: int
    order_id: int
    address: str
    status: DeliveryStatus
    requested_at: str
    delivered_at: str | None


def init_db() -> None:
    last_error = None
    for _ in range(20):
        try:
            with psycopg.connect(get_conninfo()) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS orders (
                            id SERIAL PRIMARY KEY,
                            customer_name TEXT NOT NULL,
                            product_name TEXT NOT NULL,
                            quantity INTEGER NOT NULL CHECK (quantity > 0),
                            status TEXT NOT NULL DEFAULT 'CREATED',
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        )
                        """
                    )
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS deliveries (
                            id SERIAL PRIMARY KEY,
                            order_id INTEGER NOT NULL UNIQUE REFERENCES orders(id) ON DELETE CASCADE,
                            address TEXT NOT NULL,
                            status TEXT NOT NULL DEFAULT 'REQUESTED',
                            requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            delivered_at TIMESTAMPTZ
                        )
                        """
                    )
                conn.commit()
            return
        except psycopg.OperationalError as exc:
            last_error = exc
            time.sleep(2)
    raise last_error


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Order Delivery API",
    description=(
        "주문 생성, 배송 요청, 배송 완료 프로세스를 실습하는 FastAPI 예제입니다. "
        "Swagger UI는 /docs, OpenAPI 스키마는 /openapi.json 에서 확인할 수 있습니다."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"], summary="서비스 상태 확인")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/orders",
    tags=["orders"],
    summary="주문 생성",
    response_model=OrderResponse,
    status_code=201,
)
def create_order(payload: OrderCreate) -> OrderResponse:
    with psycopg.connect(get_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO orders (customer_name, product_name, quantity)
                VALUES (%s, %s, %s)
                RETURNING id, customer_name, product_name, quantity, status, created_at
                """,
                (payload.customer_name, payload.product_name, payload.quantity),
            )
            row = cur.fetchone()
        conn.commit()

    return OrderResponse(
        id=row[0],
        customer_name=row[1],
        product_name=row[2],
        quantity=row[3],
        status=row[4],
        created_at=row[5].isoformat(),
    )


@app.post(
    "/orders/{order_id}/delivery-request",
    tags=["deliveries"],
    summary="배송 요청 생성",
    response_model=DeliveryResponse,
    status_code=201,
)
def request_delivery(
    payload: DeliveryCreate,
    order_id: int = Path(..., ge=1, description="배송 요청을 생성할 주문 ID"),
) -> DeliveryResponse:
    with psycopg.connect(get_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM orders WHERE id = %s",
                (order_id,),
            )
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Order not found")

            cur.execute(
                "SELECT id FROM deliveries WHERE order_id = %s",
                (order_id,),
            )
            if cur.fetchone() is not None:
                raise HTTPException(status_code=409, detail="Delivery already exists")

            cur.execute(
                """
                INSERT INTO deliveries (order_id, address)
                VALUES (%s, %s)
                RETURNING id, order_id, address, status, requested_at, delivered_at
                """,
                (order_id, payload.address),
            )
            row = cur.fetchone()
        conn.commit()

    return DeliveryResponse(
        id=row[0],
        order_id=row[1],
        address=row[2],
        status=row[3],
        requested_at=row[4].isoformat(),
        delivered_at=row[5].isoformat() if row[5] else None,
    )


@app.patch(
    "/deliveries/{delivery_id}/complete",
    tags=["deliveries"],
    summary="배송 완료 처리",
    response_model=DeliveryResponse,
)
def complete_delivery(
    delivery_id: int = Path(..., ge=1, description="완료 처리할 배송 ID"),
) -> DeliveryResponse:
    with psycopg.connect(get_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE deliveries
                SET status = 'DELIVERED', delivered_at = NOW()
                WHERE id = %s
                RETURNING id, order_id, address, status, requested_at, delivered_at
                """,
                (delivery_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Delivery not found")

            cur.execute(
                """
                UPDATE orders
                SET status = 'COMPLETED'
                WHERE id = %s
                """,
                (row[1],),
            )
        conn.commit()

    return DeliveryResponse(
        id=row[0],
        order_id=row[1],
        address=row[2],
        status=row[3],
        requested_at=row[4].isoformat(),
        delivered_at=row[5].isoformat() if row[5] else None,
    )


@app.get(
    "/orders/{order_id}",
    tags=["orders"],
    summary="주문 상세 조회",
    response_model=OrderResponse,
)
def get_order(order_id: int = Path(..., ge=1, description="조회할 주문 ID")) -> OrderResponse:
    with psycopg.connect(get_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, customer_name, product_name, quantity, status, created_at
                FROM orders
                WHERE id = %s
                """,
                (order_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Order not found")

    return OrderResponse(
        id=row[0],
        customer_name=row[1],
        product_name=row[2],
        quantity=row[3],
        status=row[4],
        created_at=row[5].isoformat(),
    )
