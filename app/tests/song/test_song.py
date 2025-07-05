def test_dummy(
    testclient,
):
    response = testclient.get("/song")
    assert response.status_code == 200
