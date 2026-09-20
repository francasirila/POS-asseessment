def test_category_crud(client):
    create_response = client.post(
        "/categories/",
        json={"name": "Food", "description": "Prepared food"},
    )
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    list_response = client.get("/categories/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Food"

    update_response = client.put(
        f"/categories/{category_id}",
        json={"name": "Meals", "description": "Prepared meals"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Meals"

    delete_response = client.delete(f"/categories/{category_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/categories/{category_id}").status_code == 404


def test_category_validation_error(client):
    response = client.post("/categories/", json={"name": ""})

    assert response.status_code == 422


def test_missing_category_operations_return_404(client):
    assert client.get("/categories/9999").status_code == 404
    assert client.put("/categories/9999", json={"name": "Missing"}).status_code == 404
    assert client.delete("/categories/9999").status_code == 404
