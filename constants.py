"""
ASID Global Constants
---------------------
Centralized parameters and configuration defaults used across modules.
"""

# Controller endpoints
RYU_API = "http://127.0.0.1:5005/api/mitigation"
ONOS_API = "http://127.0.0.1:5006/api/mitigation"
ODL_API = "http://127.0.0.1:5007/api/mitigation"

# Model paths
ENSEMBLE_MODEL_PATH = "detection/models/ensemble.joblib"
DATASET_PATH = "detection/data/PASD.csv"

# Ports
DMCM_PORT = 5005
RYU_PORT = 6633
ONOS_PORT = 6653
ODL_PORT = 6635

# Metric constants
UPDATE_INTERVAL = 30  # seconds
CONFIDENCE_THRESHOLD = 0.75
