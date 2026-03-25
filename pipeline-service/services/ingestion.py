import requests
import os
import dlt
from datetime import date, datetime
from decimal import Decimal

FLASK_URL = os.getenv("MOCK_SERVER_URL")
if not FLASK_URL:
    raise RuntimeError("MOCK_SERVER_URL environment variable is not set")

def fetch_all_customers():
    page = 1
    limit = 10

    while True:
        res = requests.get(FLASK_URL, params={"page": page, "limit": limit})
        res.raise_for_status()
        data = res.json()

        customers = data["data"]
        if not customers:
            break

        for c in customers:
            yield {
                "customer_id": c["customer_id"],
                "first_name": c["first_name"],
                "last_name": c["last_name"],
                "email": c["email"],
                "phone": c.get("phone"),
                "address": c.get("address"),
                "date_of_birth": date.fromisoformat(c["date_of_birth"]) if c.get("date_of_birth") else None,
                "account_balance": Decimal(str(c["account_balance"])) if c.get("account_balance") else None,
                "created_at": datetime.fromisoformat(c["created_at"].replace("Z", "")) if c.get("created_at") else None,
            }

        if len(customers) < limit:
            break

        page += 1


def run_dlt_pipeline():
    count = 0

    def source():
        nonlocal count
        for item in fetch_all_customers():
            count += 1
            yield item

    pipeline = dlt.pipeline(
        pipeline_name="customer_pipeline",
        destination="postgres",
        dataset_name="public"
    )

    pipeline.run(
        source(),
        table_name="customers",
        write_disposition="merge",
        primary_key="customer_id"
    )

    return count