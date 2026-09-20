def test_supplier_crud(client):
    payload = {
        "company_name": "Rwanda Coffee Supply",
        "contact_name": "Alice",
        "phone_number": "+250788111222",
        "email": "alice@supplier.example",
    }
    create_response = client.post("/suppliers/", json=payload)
    assert create_response.status_code == 201
    supplier_id = create_response.json()["supplier_id"]

    assert client.get("/suppliers/").status_code == 200
    assert client.get(f"/suppliers/{supplier_id}").status_code == 200

    updated_payload = {**payload, "contact_name": "Beatrice"}
    update_response = client.put(
        f"/suppliers/{supplier_id}", json=updated_payload
    )
    assert update_response.status_code == 200
    assert update_response.json()["contact_name"] == "Beatrice"

    assert client.delete(f"/suppliers/{supplier_id}").status_code == 204
    assert client.get(f"/suppliers/{supplier_id}").status_code == 404


def test_supplier_validation_errors(client):
    assert client.post("/suppliers/", json={"company_name": ""}).status_code == 422
    assert (
        client.post(
            "/suppliers/",
            json={"company_name": "Supplier", "email": "invalid-email"},
        ).status_code
        == 422
    )


def test_missing_supplier_operations_return_404(client):
    assert client.get("/suppliers/9999").status_code == 404
    assert (
        client.put("/suppliers/9999", json={"company_name": "Missing"}).status_code
        == 404
    )
    assert client.delete("/suppliers/9999").status_code == 404
