"""
Policy Engine
-------------
Defines security policies for handling SQLi attack flows.
Can be extended to support fine-grained role or reputation-based logic.
"""

import json

class PolicyEngine:
    def __init__(self):
        self.policy_table = {
            "default": "MITIGATE",
            "trusted_hosts": ["10.0.0.1", "10.0.0.2"]
        }

    def evaluate(self, src, dst):
        if src in self.policy_table["trusted_hosts"]:
            return "ALLOW"
        return "MITIGATE"

    def add_trusted(self, host_ip):
        self.policy_table["trusted_hosts"].append(host_ip)
        print(f"[PolicyEngine] Added trusted host: {host_ip}")
