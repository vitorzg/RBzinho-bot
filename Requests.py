import requests
from Parameters import Parameters

class api:
    
    @staticmethod
    def GET(base_url: str, endpoint: str, params: Parameters):
        url = f"{base_url}{endpoint}"

        headers = {
            "User-Agent": "PostmanRuntime/7.32.0",
            "Accept": "application/json",
        }

        response = requests.get(url,headers=headers,params=params.to_query())

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
