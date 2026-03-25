from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.customer import Customer, Base
from services.ingestion import run_dlt_pipeline

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/ingest")
def ingest():
    records_processed = run_dlt_pipeline()

    return {
        "status": "success",
        "records_processed": records_processed
    }


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Customer)

    total = query.count()
    customers = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "data": [
            {k: v for k, v in c.__dict__.items() if k != "_sa_instance_state"}
            for c in customers
        ],
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter_by(customer_id=customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        k: v for k, v in customer.__dict__.items()
        if k != "_sa_instance_state"
    }