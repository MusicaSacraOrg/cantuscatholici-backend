def test_dummy(
    testclient,
):
    response = testclient.get("/tag")
    assert response.status_code == 200
