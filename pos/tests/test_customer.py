def test_customer_crud(client):
    payload = {
        "name": "Jane Doe",
        "phone": "+250788123456",
        "email": "jane@example.com",
        "address": "Kigali",
    }
    create_response = client.post("/customers/", json=payload)
    assert create_response.status_code == 201
    customer_id = create_response.json()["id"]

    assert client.get("/customers/").status_code == 200
    assert client.get(f"/customers/{customer_id}").status_code == 200

    update_response = client.put(
        f"/customers/{customer_id}", json={"phone": "+250788999999"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["phone"] == "+250788999999"

    assert client.delete(f"/customers/{customer_id}").status_code == 204
    assert client.get(f"/customers/{customer_id}").status_code == 404


def test_customer_validation_errors(client):
    assert client.post("/customers/", json={"phone": "123"}).status_code == 422
    assert (
        client.post(
            "/customers/",
            json={"name": "Jane", "phone": "123", "email": "not-an-email"},
        ).status_code
        == 422
    )


def test_missing_customer_operations_return_404(client):
    assert client.get("/customers/9999").status_code == 404
    assert client.put("/customers/9999", json={"name": "Missing"}).status_code == 404
    assert client.delete("/customers/9999").status_code == 404
