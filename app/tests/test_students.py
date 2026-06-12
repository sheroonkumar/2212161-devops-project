def test_create_and_get_student(client):
    # Test POST /students
    payload = {"name": "Sheroon Kumar", "reg_no": "2212161", "email": "sheroon@example.com"}
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    assert response.json()["reg_no"] == "2212161"

    # Test GET /students (List all)
    response_list = client.get("/students")
    assert response_list.status_code == 200
    assert len(response_list.json()) == 1

    # Test GET /students/{reg_no} (Fetch specific)
    response_single = client.get("/students/2212161")
    assert response_single.status_code == 200
    assert response_single.json()["name"] == "Sheroon Kumar"