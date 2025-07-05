def test_dummy(
    testclient,
):
    response = testclient.get("/user")
    assert response.status_code == 200
