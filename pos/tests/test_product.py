def test_product_crud(client, category_record):
    payload = {
        "name": "Tea",
        "price": 2.50,
        "quantity": 30,
        "category_id": category_record["id"],
        "sku": "TEA-001",
    }
    create_response = client.post("/products", json=payload)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    assert len(client.get("/products").json()) == 1
    assert client.get(f"/products/{product_id}").status_code == 200

    update_response = client.put(
        f"/products/{product_id}", json={"price": 3.0, "quantity": 25}
    )
    assert update_response.status_code == 200
    assert update_response.json()["price"] == 3.0
    assert update_response.json()["quantity"] == 25

    assert client.delete(f"/products/{product_id}").status_code == 204
    assert client.get(f"/products/{product_id}").status_code == 404


def test_product_validation_errors(client, category_record):
    base = {
        "name": "Invalid",
        "price": 2.0,
        "quantity": 1,
        "category_id": category_record["id"],
        "sku": "INVALID-1",
    }
    assert client.post("/products", json={**base, "price": 0}).status_code == 422
    assert client.post("/products", json={**base, "quantity": -1}).status_code == 422
    assert client.post("/products", json={**base, "sku": ""}).status_code == 422


def test_product_requires_existing_category(client):
    response = client.post(
        "/products",
        json={
            "name": "Coffee",
            "price": 3.5,
            "quantity": 10,
            "category_id": 9999,
            "sku": "COFFEE-MISSING-CATEGORY",
        },
    )

    assert response.status_code == 404


def test_duplicate_sku_is_rejected(client, product_record, category_record):
    response = client.post(
        "/products",
        json={
            "name": "Another Coffee",
            "price": 4.0,
            "quantity": 5,
            "category_id": category_record["id"],
            "sku": product_record["sku"],
        },
    )

    assert response.status_code == 400


def test_missing_product_operations_return_404(client):
    assert client.get("/products/9999").status_code == 404
    assert client.put("/products/9999", json={"price": 5.0}).status_code == 404
    assert client.delete("/products/9999").status_code == 404
