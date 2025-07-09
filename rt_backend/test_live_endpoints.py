import requests

BASE_URL = "http://localhost:8000"

def test_root():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print("Root Response:", response.json())

def test_api_test():
    response = requests.get(BASE_URL + "/api/test")
    assert response.status_code == 200
    print("API Test Response:", response.json())

def test_candidates():
    response = requests.get(BASE_URL + "/api/candidates")
    print("Candidates Response Status Code:", response.status_code)
    print("Candidates Response Body:", response.text)
    assert response.status_code == 200
    print("Candidates Response:", response.json())

def test_resume_ranking():
    resume_data = {
        "resume": "Experienced software developer with expertise in Python and FastAPI.",
        "job_description": "Looking for a Python developer with FastAPI experience."
    }
    response = requests.post(BASE_URL + "/api/rank", json=resume_data)
    assert response.status_code == 200
    print("Resume Ranking Response:", response.json())

if __name__ == "__main__":
    test_root()
    test_api_test()
    test_candidates()
    test_resume_ranking()
    print("All tests passed!") 