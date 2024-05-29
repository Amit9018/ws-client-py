import websocket
import time
import json
import subprocess

def parse_json(json_data):
    try:
        parsed_data = json.loads(json_data)
        # Handle duplicate keys here if needed
        return parsed_data
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None


def websocket_func():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    
    ws.run_forever()

def on_message(ws, message):
    print(message)
    temp = parse_json(message)
    print(temp["cmd"])
    cmd_output = subprocess.run(temp["cmd"], shell=True, capture_output=True, text=True)
    

def on_error(ws, error):
    print(error)
    reconnect()

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    reconnect()

def on_open(ws):
    print("Opened connection")
    obj = {
        "type": "login",
        "userid": "abcd",
    }
    ws.send(json.dumps(obj))

def reconnect():
    print("Reconnecting...")
    time.sleep(5)  # Wait for 5 seconds before attempting to reconnect
    websocket_func()  # Call the WebSocket function again to establish a new connection

if __name__ == "__main__":
    websocket_func()
