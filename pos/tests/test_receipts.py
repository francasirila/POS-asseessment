from app.models.receipts import Receipt
from app.models.sales import Sale
from app.repositories.users import user_repo


def test_list_get_and_missing_receipt(client, db_session, registered_user):
    user = user_repo.get_by_username(db_session, registered_user["username"])
    sale = Sale(user_id=user.user_id, total_amount=12.0, payment_method="cash")
    db_session.add(sale)
    db_session.flush()
    receipt = Receipt(sale_id=sale.sale_id, receipt_number="RCPT-001")
    db_session.add(receipt)
    db_session.commit()
    db_session.refresh(receipt)

    list_response = client.get("/receipts/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/receipts/{receipt.receipt_id}")
    assert get_response.status_code == 200
    assert get_response.json()["receipt_number"] == "RCPT-001"

    assert client.get("/receipts/9999").status_code == 404
