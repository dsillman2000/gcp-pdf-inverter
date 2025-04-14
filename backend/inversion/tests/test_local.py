from inversion.utils import get_temp_dir, get_temp_file


def test_local_download(client, test_uuid_pre):
    response = client.post(f"/download/{test_uuid_pre}")
    assert response.status_code == 200
    message = response.json().get("message", "")
    assert "Downloaded file to path: " in message
    assert test_uuid_pre in message


def test_local_invert(client, test_uuid_pre):
    response = client.post(f"/invert/{test_uuid_pre}")
    assert response.status_code == 200
    message = response.json().get("message", "")
    assert "Inverted file with UUID: " in message
    assert test_uuid_pre in message


def test_local_upload(client, test_uuid_inverted):
    response = client.post(f"/upload/{test_uuid_inverted}")
    assert response.status_code == 200
    message = response.json().get("message", "")
    assert "Uploaded PDF file with UUID: " in message
    assert test_uuid_inverted in message
