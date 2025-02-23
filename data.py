import csv
from datetime import datetime, timedelta
import random

# Technical skill categories and details
categories = [
    'Programming Languages',
    'Cloud Technologies',
    'DevOps Tools',
    'Data Engineering',
    'Cybersecurity',
    'AI/ML Frameworks',
    'Blockchain',
    'Quantum Computing',
    'Embedded Systems',
    'Distributed Systems'
]

skills = {
    'Rust Memory Management': 'Systems Programming',
    'Kubernetes Cluster Orchestration': 'Cloud Technologies',
    'Apache Kafka Stream Processing': 'Data Engineering',
    'Zero Trust Architecture': 'Cybersecurity',
    'FPGA Programming': 'Embedded Systems',
    'TensorFlow Distributed Training': 'AI/ML Frameworks',
    'ISTQB Advanced Level': 'QA Automation',
    'eBPF Kernel Programming': 'Linux Networking',
    'VHDL/Verilog Synthesis': 'Hardware Design',
    'Prometheus+Grafana Monitoring': 'DevOps Tools',
    'CRDT Algorithms': 'Distributed Systems',
    'Homomorphic Encryption': 'Cryptography',
    'SPARK Formal Verification': 'Safety-Critical Systems',
    'LLVM Compiler Development': 'Compiler Design',
    'OpenMPI Cluster Computing': 'HPC',
    'ROS2 Robotics Middleware': 'Robotics',
    'DPDK Packet Processing': 'Network Programming',
    'Apache Flink Stateful Streams': 'Real-time Analytics',
    'WebAssembly Runtime Optimization': 'Low-level Web',
    'Q# Quantum Algorithms': 'Quantum Computing',
    'Solidity Smart Contracts': 'Blockchain',
    'Apache Arrow Memory Format': 'In-Memory Computing',
    'Enzyme AD (Differentiation)': 'Scientific Computing',
    'Coreboot Firmware Development': 'System Firmware',
    'Mesa3D Graphics Drivers': 'GPU Programming',
    'Zig Comptime Metaprogramming': 'Systems Language',
    'Linux Kernel Module Development': 'OS Internals',
    'BPF Compiler Collection': 'Observability',
    'OpenTelemetry Instrumentation': 'Distributed Tracing',
    'Istio Service Mesh': 'Cloud Native',
    'SPIR-V Shader Optimization': 'GPU Compute',
    'MLIR Compiler Infrastructure': 'Compiler Intermediate',
    'Apache Iceberg Lakehouse': 'Big Data Formats',
    'Cilium Network Policies': 'Cloud Networking',
    'WebGPU API Development': 'Next-gen Graphics',
    'gRPC Protocol Buffers': 'Microservices Communication',
    'Apache Pulsar Functions': 'Event Streaming',
    'WebRTC Low-latency': 'Real-time Communication',
    'OpenCV CUDA Acceleration': 'Computer Vision',
    'ONNX Runtime Optimization': 'Model Deployment',
    'NixOS Configuration': 'Reproducible Builds',
    'Terraform Provider Development': 'Infrastructure as Code',
    'Envoy Filter Creation': 'API Gateways',
    'WasmEdge Runtime': 'Edge Computing',
    'OpenStack Bare Metal': 'Private Cloud',
    'Kubernetes Operators SDK': 'Cloud Automation',
    'Apache Druid OLAP': 'Analytics Databases',
    'Neo4j Cypher Queries': 'Graph Databases',
    'Redis Module Development': 'In-Memory DBs',
    'PostgreSQL Query Optimization': 'RDBMS Tuning'
}

descriptions = {
    'Rust Memory Management': 'Advanced ownership models and unsafe code practices',
    'Kubernetes Cluster Orchestration': 'Multi-cloud cluster federation and CRD development',
    'Apache Kafka Stream Processing': 'Exactly-once semantics in distributed event streaming',
    'Zero Trust Architecture': 'Implementation of continuous verification systems',
    'FPGA Programming': 'High-speed digital circuit design with VHDL',
    # Add descriptions for all 50 skills...
}

difficulty_levels = ['High', 'Very High', 'Extreme']

def generate_last_updated():
    return (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')

# Generate 50 records
records = []
for i, (skill, category) in enumerate(skills.items(), 1):
    description = descriptions.get(skill, f'Advanced implementation of {skill} in production systems')
    difficulty = random.choice(difficulty_levels)
    last_updated = generate_last_updated()
    docs_link = f'https://{skill.split()[0].lower()}-docs.org/{skill.replace(" ", "-")}'

    records.append([
        i,
        skill,
        category,
        description,
        difficulty,
        last_updated,
        docs_link
    ])

# Write to CSV
headers = ['Sr. No', 'Skill Name', 'Category', 'Description', 'Difficulty Level', 'Last Updated', 'Documentation Link']

with open('tech_skills.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(records)

print("tech_skills.csv created with 50 hardcore tech skills!")