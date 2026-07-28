import requests
import json


class OllamaClient:
    def __init__(self, model_name, ollama_url):
        self.model_name = model_name
        self.ollama_url = ollama_url

    def generate_response(self, prompt):
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": True                },
                stream=True,
                timeout=120
            )

            response.raise_for_status()

            assistant_response = ""

            for line in response.iter_lines():
                if not line:
                    continue

                data = json.loads(line)

                # We intentionally only collect the final response.
                # If Ollama provides a separate thinking field,
                # we ignore it.
                content = data.get("response")

                if content:
                    assistant_response += content

            assistant_response = assistant_response.strip()

            if not assistant_response:
                print("\n[ERROR] Ollama returned an empty response.")
                return None

            return assistant_response

        except requests.exceptions.ConnectionError:
            print("\n[ERROR] Could not connect to Ollama. Is Ollama running?")
            return None

        except requests.exceptions.Timeout:
            print("\n[ERROR] Ollama took too long to respond.")
            return None

        except requests.exceptions.RequestException as error:
            print(f"\n[ERROR] Request failed: {error}")
            return None

        except json.JSONDecodeError:
            print("\n[ERROR] Received invalid JSON data from Ollama.")
            return None