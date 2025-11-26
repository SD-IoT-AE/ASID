# 🧠 ASID Framework  
### Confidence-Aware Multi-Controller Framework for Detecting and Mitigating Advanced SQL Injection Attacks in SDN

## 🚀 Overview

**ASID** (Adaptive Security and Intelligence-Driven framework) is a programmable, multi-controller architecture that integrates:
- **P4-based in-switch traffic feature extraction**
- **Machine-learning–based detection (CAAWE)**
- **Distributed multi-controller mitigation (DMCM)** across **RYU**, **ONOS**, and **OpenDaylight**

The framework enables real-time detection and mitigation of *advanced SQL Injection (SQLi) attacks* in Software-Defined Networking (SDN) environments.

## 🧩 Architecture Overview

ASID is composed of three major modules:

1. **P4 Data Plane (Traffic Engineering Module)**  
   - Runs on BMv2 (Behavioral Model v2)  
   - Extracts 20 statistical and temporal features from SQLi traffic  
   - Exports digest messages to the controller via gRPC

2. **CAAWE Detection Module**  
   - Confidence-Aware Adaptive Weighted Ensemble of 4 models:  
     KNN, Decision Tree, Random Forest, and SVM  
   - Dynamically adjusts model weights based on accuracy and confidence

3. **DMCM Mitigation Module**  
   - Distributes mitigation actions to multiple controllers  
   - Coordinates via RESTful APIs with RYU, ONOS, and OpenDaylight adapters  
   - Logs and visualizes all mitigation events

## 🏗️ Directory Structure

```
ASID/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── controllers/
│   ├── onos/
│   │   ├── onos_app.py
│   │   ├── mitigation_service.py
│   │   └── config/
│   │       ├── onos_conf.json
│   │       └── topology.json
│   ├── ryu/
│   │   ├── ryu_controller.py
│   │   ├── mitigation_agent.py
│   │   └── config/
│   │       ├── ryu_conf.yaml
│   │       └── topology.json
│   └── opendaylight/
│       ├── odl_app.py
│       ├── odl_mitigation_module.py
│       └── config/
│           ├── odl_conf.json
│           └── topology.json
│
├── dataplane/
│   ├── p4src/
│   │   ├── asid_traffic_engineering.p4
│   │   └── asid_feature_export.p4
│   ├── runtime/
│   │   ├── p4runtime_shell_config.json
│   │   ├── asid_pipeline.bmv2.json
│   │   └── switch_cli_commands.txt
│   └── test/
│       ├── p4_test_flows.py
│       └── p4_digest_collector.py
│
├── detection/
│   ├── caawe_ensemble.py
│   ├── base_models/
│   │   ├── knn_model.py
│   │   ├── decision_tree_model.py
│   │   ├── random_forest_model.py
│   │   └── svm_model.py
│   ├── retraining/
│   │   ├── feedback_loop.py
│   │   └── incremental_update.py
│   └── data/
│       ├── PASD.csv
│       └── feature_extractor.py
│
├── mitigation/
│   ├── dmcm_core.py
│   ├── coordination_bus.py
│   ├── policy_engine.py
│   └── logs/
│       └── mitigation_log.json
│
├── experiments/
│   ├── mininet_topology.py
│   ├── traffic_generator.py
│   ├── performance_evaluator.py
│   └── grafana_prometheus_config/
│       ├── prometheus.yml
│       └── grafana_dashboard.json
│
└── utils/
    ├── helpers.py
    ├── logger.py
    ├── constants.py
    └── metrics.py
```

## ⚙️ Installation & Environment Setup

### 🔧 Prerequisites
- **Python ≥ 3.9**
- **Mininet 2.3+**
- **BMv2 (Behavioral Model v2)** with `simple_switch_grpc`
- **P4C Compiler**
- **ONOS 2.7+**
- **OpenDaylight Aluminium+**
- **Prometheus** & **Grafana**
- **RYU Controller**

### 🧰 Install Dependencies
```bash
pip install -r requirements.txt
```

## 🧠 Deployment Workflow

1. **Compile and deploy P4 program**
   ```bash
   p4c --target bmv2 --arch v1model -o dataplane/runtime dataplane/p4src/asid_traffic_engineering.p4
   simple_switch_grpc --device-id 1 --no-p4      --p4info dataplane/runtime/p4runtime_shell_config.json      --config dataplane/runtime/asid_pipeline.bmv2.json
   ```

2. **Start SDN Controllers**
   ```bash
   onos-service start
   ./distribution-karaf/bin/karaf  # OpenDaylight
   python3 controllers/onos/onos_app.py &
   python3 controllers/opendaylight/odl_app.py &
   ryu-manager controllers/ryu/ryu_controller.py &
   ```

3. **Run Detection and Mitigation Services**
   ```bash
   python3 detection/caawe_ensemble.py &
   python3 mitigation/dmcm_core.py &
   ```

4. **Start Mininet Topology**
   ```bash
   sudo python3 experiments/mininet_topology.py
   ```

5. **Generate Traffic**
   ```bash
   python3 experiments/traffic_generator.py
   ```

6. **Monitor Performance**
   ```bash
   python3 experiments/performance_evaluator.py
   docker-compose -f experiments/grafana_prometheus_config/docker-compose.yml up
   ```

## 📊 Metrics & Visualization

Prometheus scrapes metrics from DMCM and detection modules. Grafana visualizes:  
- Mitigation rates  
- Detection accuracy  
- Controller delay  
- Feature extraction latency  

## 📁 Logs & Output
| File | Description |
|------|--------------|
| `mitigation/logs/mitigation_log.json` | Real-time mitigation actions |
| `experiments/performance_summary.json` | Experiment statistics |
| `experiments/performance_metrics.json` | Accuracy and F1 metrics |

## 🧩 Key Features
- ✅ Multi-controller orchestration (RYU, ONOS, ODL)
- ✅ Adaptive ML detection (CAAWE)
- ✅ In-switch P4 feature extraction
- ✅ Real-time distributed mitigation
- ✅ Prometheus-Grafana visualization

## 🤝 Contributing
1. Fork this repo  
2. Create a feature branch (`feature/my-feature`)  
3. Commit your changes  
4. Push to your branch and open a PR

## 📜 License
MIT License © 2025 ASID Research Team


