from datetime import datetime

def test_create_feedback(client, logged_in_user):
    data = {
        "user_id": logged_in_user["user_id"],
        "application_id": logged_in_user["application_id"],
        "fee_rating": 5,
        "fee_comment": "Excelente app",
        "fee_date": datetime.utcnow().isoformat()
    }

    response = client.post("/feedback/", json=data)
    assert response.status_code == 201
    body = response.json()

    assert body["fee_rating"] == 5
    assert body["application_id"] == logged_in_user["application_id"]

def test_create_feedback_duplicate(client, logged_in_user):
    data = {
        "user_id": logged_in_user["user_id"],
        "application_id": logged_in_user["application_id"],
        "fee_rating": 4,
        "fee_comment": "Muy buena",
        "fee_date": datetime.utcnow().isoformat()
    }

    client.post("/feedback/", json=data)  # primero OK
    response = client.post("/feedback/", json=data)  # duplicado

    assert response.status_code == 409
    assert "ya existe" in response.json()["detail"]

def test_read_feedback(client, logged_in_user_with_apps):
    data = {
        "user_id": logged_in_user_with_apps["user_id"],
        "application_id": logged_in_user_with_apps["application_id"],
        "fee_rating": 3,
        "fee_comment": "Está bien",
        "fee_date": datetime.utcnow().isoformat()
    }

    created = client.post("/feedback/", json=data).json()
    print("✅Created feedback ID:", created)
    feedback_id = created["id"]
    

    response = client.get(f"/feedback/{feedback_id}")
    assert response.status_code == 200
    assert response.json()["fee_rating"] == 3

def test_update_feedback(client, logged_in_user_with_apps):
    data = {
        "user_id": logged_in_user_with_apps["user_id"],
        "application_id": logged_in_user_with_apps["application_id"],
        "fee_rating": 2,
        "fee_comment": "Regular",
        "fee_date": datetime.utcnow().isoformat()
    }

    created = client.post("/feedback/", json=data).json()
    print("✅Created feedback ID for deletion:", created)
    
    feedback_id = created["id"]

    update = {
        "fee_rating": 5,
        "fee_comment": "Regular",
    }

    response = client.put(f"/feedback/{feedback_id}", json=update)
    assert response.status_code == 200
    assert response.json()["fee_rating"] == 5

def test_delete_feedback(client, logged_in_user_with_apps):
    data = {
        "user_id": logged_in_user_with_apps["user_id"],
        "application_id": logged_in_user_with_apps["application_id"],
        "fee_rating": 4,
        "fee_comment": "Bien",
        "fee_date": datetime.utcnow().isoformat()
    }

    created = client.post("/feedback/", json=data).json()
    print("✅Created feedback ID for deletion:", created)
    feedback_id = created["id"]

    response = client.delete(f"/feedback/{feedback_id}")
    assert response.status_code == 200

    # Verificar que no existe
    response2 = client.get(f"/feedback/{feedback_id}")
    assert response2.status_code == 404

def test_app_rating(client, logged_in_user_with_apps):
    data = {
        "user_id": logged_in_user_with_apps["user_id"],
        "application_id": logged_in_user_with_apps["application_id"],
        "fee_rating": 5,
        "fee_comment": "Muy buena",
        "fee_date": datetime.utcnow().isoformat()
    }

    client.post("/feedback/", json=data)

    response = client.get(f"/feedback/app/{logged_in_user_with_apps['application_id']}/rating")
    assert response.status_code == 200
    body = response.json()

    assert body["average"] == 5.0
    assert body["count"] == 1
