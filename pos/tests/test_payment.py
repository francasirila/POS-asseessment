from app.models.sales import Sale


def create_sale_record(db_session, registered_user):
    from app.repositories.users import user_repo

    user = user_repo.get_by_username(db_session, registered_user["username"])
    sale = Sale(user_id=user.user_id, total_amount=10.0, payment_method="cash")
    db_session.add(sale)
    db_session.commit()
    db_session.refresh(sale)
    return sale


def test_create_list_and_get_payment(client, db_session, registered_user):
    sale = create_sale_record(db_session, registered_user)
    create_response = client.post(
        "/payments/",
        json={"sale_id": sale.sale_id, "payment_method": "cash", "amount_paid": 10},
    )
    assert create_response.status_code == 201
    payment_id = create_response.json()["payment_id"]

    assert len(client.get("/payments/").json()) == 1
    assert client.get(f"/payments/{payment_id}").status_code == 200


def test_payment_validation_and_missing_resources(client):
    invalid = client.post(
        "/payments/",
        json={"sale_id": 1, "payment_method": "cash", "amount_paid": 0},
    )
    assert invalid.status_code == 422

    missing_sale = client.post(
        "/payments/",
        json={"sale_id": 9999, "payment_method": "cash", "amount_paid": 10},
    )
    assert missing_sale.status_code == 404
    assert client.get("/payments/9999").status_code == 404
