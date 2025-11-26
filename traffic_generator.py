"""
ASID Traffic Generator
----------------------
Simulates mixed benign and SQLi attack traffic between hosts.
"""
import time, random, requests

BENIGN_PAYLOADS = [
    "GET /index.html HTTP/1.1",
    "SELECT id, name FROM customers;",
    "INSERT INTO logs VALUES('normal');"
]
ATTACK_PAYLOADS = [
    "SELECT * FROM users WHERE id='' OR '1'='1';",
    "DROP TABLE accounts; --",
    "' OR 1=1 --",
    "' UNION SELECT password FROM admin --"
]

def send_http_traffic(src="h1", dst="h2", attack_ratio=0.3, count=10):
    for i in range(count):
        is_attack = random.random() < attack_ratio
        payload = random.choice(ATTACK_PAYLOADS if is_attack else BENIGN_PAYLOADS)
        flow = {"flow_src": src, "flow_dst": dst, "payload": payload, "timestamp": time.time()}
        print(f"[Traffic] {flow}")
        try:
            # Emulate sending flow to detection module
            requests.post("http://127.0.0.1:5050/api/digest", json=[flow])
        except Exception:
            pass
        time.sleep(1)

if __name__ == "__main__":
    send_http_traffic()
