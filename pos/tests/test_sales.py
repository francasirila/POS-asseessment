def test_sale_deducts_inventory_and_uses_catalog_price(
    client, auth_headers, product_record
):
    response = client.post(
        "/sales",
        headers=auth_headers,
        json={
            "payment_method": "cash",
            "items": [{"product_id": product_record["id"], "quantity": 2}],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert float(data["total_amount"]) == 7.0
    assert data["payment_method"] == "cash"
    assert data["sale_items"][0]["quantity"] == 2

    product_response = client.get(f"/products/{product_record['id']}")
    assert product_response.json()["quantity"] == 18

    sale_id = data["sale_id"]
    assert client.get(f"/sales/{sale_id}").status_code == 200
    assert len(client.get("/sales").json()) == 1


def test_sale_with_insufficient_stock_rolls_back(client, auth_headers, product_record):
    response = client.post(
        "/sales",
        headers=auth_headers,
        json={
            "items": [{"product_id": product_record["id"], "quantity": 1000}]
        },
    )

    assert response.status_code == 400
    assert client.get(f"/products/{product_record['id']}").json()["quantity"] == 20
    assert client.get("/sales").json() == []


def test_sale_with_missing_product_is_rejected(client, auth_headers):
    response = client.post(
        "/sales",
        headers=auth_headers,
        json={"items": [{"product_id": 9999, "quantity": 1}]},
    )

    assert response.status_code == 404
    assert client.get("/sales").json() == []


def test_sale_requires_authentication(client, product_record):
    response = client.post(
        "/sales",
        json={"items": [{"product_id": product_record["id"], "quantity": 1}]},
    )

    assert response.status_code == 401


def test_sale_requires_at_least_one_valid_item(client, auth_headers):
    assert client.post("/sales", headers=auth_headers, json={"items": []}).status_code == 422
    assert (
        client.post(
            "/sales",
            headers=auth_headers,
            json={"items": [{"product_id": 1, "quantity": 0}]},
        ).status_code
        == 422
    )


def test_missing_sale_returns_404(client):
    assert client.get("/sales/9999").status_code == 404
