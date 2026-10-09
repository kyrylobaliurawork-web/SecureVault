
def test_upload_empty_file_is_rejected(client, create_user):
    user = create_user()

    response = client.post(
        "/files",
        headers=user["headers"],
        files={
            "file": (
                "empty.txt",
                b"",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400


def test_fake_pdf_is_rejected(client, create_user):
    user = create_user()

    response = client.post(
        "/files",
        headers=user["headers"],
        files={
            "file": (
                "fake.pdf",
                b"This is plain text, not a PDF file.",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400


def test_disallowed_file_type_is_rejected(
    client,
    create_user,
):
    user = create_user()

    response = client.post(
        "/files",
        headers=user["headers"],
        files={
            "file": (
                "program.exe",
                b"MZ fake executable content",
                "application/x-msdownload",
            )
        },
    )

    assert response.status_code == 400


def test_file_over_10_mb_is_rejected(client, create_user):
    user = create_user()

    content = b"A" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/files",
        headers=user["headers"],
        files={
            "file": (
                "large.pdf",
                content,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 413