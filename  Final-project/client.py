import urllib.request
import urllib.parse
import json

URL_BASE = "http://localhost:8080/listSpecies"


def test_client():
    params = urllib.parse.urlencode({"limit": 5, "json": "1"})
    url_completa = f"{URL_BASE}?{params}"

    print(f"Connecting to server via: {url_completa}\n")

    try:
        with urllib.request.urlopen(url_completa) as response:
            raw_data = response.read().decode("utf-8")
            json_object = json.loads(raw_data)

            print("--- JSON RECEIVED SUCCESSFULLY ---")
            for idx, species in enumerate(json_object, 1):
                display_name = species.get("display_name", "Unknown")
                scientific_name = species.get("name", "Unknown")
                print(f"{idx}. {display_name} ({scientific_name})")

    except Exception as e:
        print(f"Error connecting to server: {e}")


if __name__ == "__main__":
    test_client()