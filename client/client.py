import requests
import json

def main():
    # Example data for prediction (Iris setosa)
    data = [[5.1, 3.5, 1.4, 0.2]]
    
    try:
        response = requests.post("http://api:8000/predict/", json={"data": data})
        response.raise_for_status() # Raise an exception for bad status codes
        
        result = response.json()
        print(f"Prediction from API: {result.get('prediction')}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from response: {response.text}")

if __name__ == "__main__":
    main()