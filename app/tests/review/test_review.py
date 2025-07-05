def test_dummy(
    testclient,
):
    response = testclient.get("/review")
    assert response.status_code == 200
