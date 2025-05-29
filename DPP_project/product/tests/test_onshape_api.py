"""

Test file for Onshape API integration

Declaration of Assistance
This test file was developed with the assistance of GitHub Copilot, which provided suggestions during the coding
process. The author adapted and integrated these suggestions to align with the project's structure and
objectives. All code has been critically reviewed and approved by the author.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""


import time
from product.onshape_codes import onshape_api

DID_chair = "ddd738631676985828abef74"  # Document ID
WID_chair = "76466b78737892550146d811"  # Workspace ID
EID_chair = "789de4812fe20a46c3f3962b"  # Element ID

DID = DID_chair # Document ID
WID = WID_chair # Workspace ID
EID = EID_chair # Element ID

# def test_pytest_works():
#     assert 2 + 2 == 4

# def test_get_api_data_returns_dict(monkeypatch):
#     # Mock requests.get for å unngå ekte API-kall
#     class MockResponse:
#         def __init__(self):
#             self.ok = True
#         def json(self):
#             return {"key": "value"}
#     monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

#     result = onshape_api.get_api_data("http://fakeurl")
#     assert isinstance(result, dict)
#     assert result["key"] == "value"

def test_real_onshape_api_response_time_average():
    url = f"https://cad.onshape.com/api/partstudios/d/{DID}/w/{WID}/e/{EID}/features"
    N = 20
    times = []
    times_dict = {}

    for i in range(N):
        start_time = time.time()
        result = onshape_api.get_api_data(url)
        elapsed = time.time() - start_time
        times.append(elapsed)
        times_dict[i+1] = round(elapsed, 2)
        assert isinstance(result, dict)
        assert "features" in result

    avg = sum(times) / N
    print(f"\nAverage response time over {N} runs: {avg:.2f} seconds")
    print(f"Min: {min(times):.2f}, Max: {max(times):.2f}")
    print(f"Test run with time:", times_dict)

    assert avg < 5, f"Average API call took too long: {avg} seconds"