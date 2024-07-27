import time
import http.client
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PASTE_URL = 'direct-jania-dropcloud-aaabff56.koyeb.app'
PASTE_PATH = '/SphereKeyHubSystem.txt'
WEBHOOK_HOST = 'discord.com'
WEBHOOK_PATH = '/api/webhooks/1265525613842927636/iqll8fEX3SdhSpRzyXYyrFRMMKWiXF8md6YANS4jDXpzIr9HkH7xZ9CphygiPZDs8GH3'
ROLE_ID = "1265526450212311090"

def get_paste():
    try:
        conn = http.client.HTTPSConnection(PASTE_URL)
        conn.request("GET", PASTE_PATH)
        response = conn.getresponse()
        if response.status == 200:
            cleaned_text = response.read().decode('utf-8').replace('"', '')
            logging.info(f'Successfully fetched paste: {cleaned_text}')
            return cleaned_text
        else:
            logging.error(f'Failed to fetch paste. Error code: {response.status}')
            return None
    except Exception as e:
        logging.error(f'Exception occurred while fetching paste: {e}')
        return None
    finally:
        conn.close()

def send_webhook(key):
    content = f"<@&{ROLE_ID}>"
    data = {
        "content": content,
        "embeds": [
            {
                "title": "New Paste Key",
                "color": 242424,
                "fields": [
                    {"name": "Key:", "value": f"```{key}```", "inline": False},
                    {"name": "Info:", "value": "If there's a problem, contact <@711330346851106856> or <@1086803263464165376>"}
                ]
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        conn = http.client.HTTPSConnection(WEBHOOK_HOST)
        conn.request("POST", WEBHOOK_PATH, body=json.dumps(data), headers=headers)
        response = conn.getresponse()
        if response.status == 204:
            logging.info("Webhook sent successfully")
        else:
            logging.error(f'Failed to send webhook. Error code: {response.status}')
    except Exception as e:
        logging.error(f'Exception occurred while sending webhook: {e}')
    finally:
        conn.close()

def main():
    previous_key = get_paste()
    if previous_key:
        send_webhook(previous_key)

    while True:
        time.sleep(10)
        current_key = get_paste()
        if current_key and current_key != previous_key:
            send_webhook(current_key)
            previous_key = current_key

if __name__ == "__main__":
    main()
