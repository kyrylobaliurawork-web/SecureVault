
PDF_CONTENT = (
    b"%PDF-1.4\n"
    b"1 0 obj\n"
    b"<< /Type /Catalog >>\n"
    b"endobj\n"
    b"%%EOF\n"
)


def upload_pdf(client, headers, filename="test.pdf"):
    return client.post(
        "/files",
        headers=headers,
        files={
            "file": (
                filename,
                PDF_CONTENT,
                "application/pdf",
            )
        },
    )


def test_upload_file(client, create_user):
    user = create_user()

    response = upload_pdf(client, user["headers"])

    assert response.status_code == 200

    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["size"] == len(PDF_CONTENT)
    assert data["checksum"]
    assert "storage_key" not in data


def test_list_files(client, create_user):
    user = create_user()

    upload_response = upload_pdf(client, user["headers"])
    assert upload_response.status_code == 200

    response = client.get(
        "/files",
        headers=user["headers"],
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["filename"] == "test.pdf"


def test_download_file(client, create_user):
    user = create_user()

    upload_response = upload_pdf(client, user["headers"])
    file_id = upload_response.json()["id"]

    response = client.get(
        f"/files/{file_id}",
        headers=user["headers"],
    )

    assert response.status_code == 200
    assert response.content == PDF_CONTENT


def test_delete_file(client, create_user):
    user = create_user()

    upload_response = upload_pdf(client, user["headers"])
    file_id = upload_response.json()["id"]

    delete_response = client.delete(
        f"/files/{file_id}",
        headers=user["headers"],
    )

    assert delete_response.status_code == 200

    list_response = client.get(
        "/files",
        headers=user["headers"],
    )

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_user_cannot_download_another_users_file(
    client,
    create_user,
):
    user_a = create_user()
    user_b = create_user()

    upload_response = upload_pdf(
        client,
        user_a["headers"],
    )
    file_id = upload_response.json()["id"]

    response = client.get(
        f"/files/{file_id}",
        headers=user_b["headers"],
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_file(
    client,
    create_user,
):
    user_a = create_user()
    user_b = create_user()

    upload_response = upload_pdf(
        client,
        user_a["headers"],
    )
    file_id = upload_response.json()["id"]

    response = client.delete(
        f"/files/{file_id}",
        headers=user_b["headers"],
    )

    assert response.status_code == 404

    owner_files = client.get(
        "/files",
        headers=user_a["headers"],
    )

    assert owner_files.status_code == 200
    assert len(owner_files.json()) == 1


def test_files_require_authentication(client):
    response = client.get("/files")

    assert response.status_code == 401