def test_dummy(
    testclient,
):
    response = testclient.get("/calendar")
    assert response.status_code == 200
