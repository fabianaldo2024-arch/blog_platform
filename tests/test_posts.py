def test_create_post_authenticated(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    payload = {
        "title": "Post de Prueba",
        "content": "Contenido detallado para la prueba de integración."
    }
    
    response = client.post("/api/v1/posts/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "id" in data
    assert "owner_id" in data


def test_create_post_unauthorized(client):
    payload = {
        "title": "Post no autorizado",
        "content": "Intento de creación sin JWT."
    }
    response = client.post("/api/v1/posts/", json=payload)
    assert response.status_code == 401


def test_read_posts_list(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    client.post(
        "/api/v1/posts/",
        json={"title": "Post 1", "content": "Contenido 1"},
        headers=headers
    )
    client.post(
        "/api/v1/posts/",
        json={"title": "Post 2", "content": "Contenido 2"},
        headers=headers
    )

    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_update_post_owner_success(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    create_res = client.post(
        "/api/v1/posts/",
        json={"title": "Título Original", "content": "Contenido Original"},
        headers=headers
    )
    post_id = create_res.json()["id"]

    update_payload = {
        "title": "Título Actualizado",
        "content": "Contenido Actualizado"
    }
    response = client.put(
        f"/api/v1/posts/{post_id}",
        json=update_payload,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_payload["title"]
    assert data["content"] == update_payload["content"]


def test_update_post_forbidden_other_user(client, user_token):
    # Crear post con primer usuario
    headers_owner = {"Authorization": f"Bearer {user_token}"}
    create_res = client.post(
        "/api/v1/posts/",
        json={"title": "Post Dueño", "content": "Contenido Dueño"},
        headers=headers_owner
    )
    post_id = create_res.json()["id"]

    # Registrar e iniciar sesión con segundo usuario
    second_user = {
        "username": "otheruser",
        "email": "other@example.com",
        "password": "password123"
    }
    client.post("/api/v1/auth/register", json=second_user)
    login_res = client.post(
        "/api/v1/auth/token",
        data={"username": second_user["username"], "password": second_user["password"]}
    )
    second_token = login_res.json()["access_token"]
    headers_other = {"Authorization": f"Bearer {second_token}"}

    # Intentar editar con el segundo usuario (debe retornar 403 Forbidden)
    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Hack Attempt", "content": "Hack Content"},
        headers=headers_other
    )
    assert response.status_code == 403


def test_delete_post_owner_success(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    create_res = client.post(
        "/api/v1/posts/",
        json={"title": "A borrar", "content": "Eliminar"},
        headers=headers
    )
    post_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/posts/{post_id}", headers=headers)
    assert delete_res.status_code == 204

    # Verificar que ya no existe en la BD
    get_res = client.get("/api/v1/posts/")
    posts = get_res.json()
    assert not any(p["id"] == post_id for p in posts)


def test_delete_post_not_found(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.delete("/api/v1/posts/99999", headers=headers)
    assert response.status_code == 404
