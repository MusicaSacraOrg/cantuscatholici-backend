def test_dummy(
    testclient,
):
    response = testclient.get("/content")
    assert response.status_code == 200
