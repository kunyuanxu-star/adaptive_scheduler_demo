import torch
import torch.nn as nn
import numpy as np
import json
import os
import logging

class PPOAgent(nn.Module):
    """Simplified PPO Agent for scheduling decisions."""
    def __init__(self, state_dim=30, action_dim=2):
        super(PPOAgent, self).__init__()
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )
        self.output_file = os.path.join("src", "shared", "sched_policy.json")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def decide_policy(self, state):
        """Generate scheduling policy based on state."""
        state = torch.FloatTensor(state)
        policy = self.actor(state)
        action = torch.argmax(policy, dim=-1).item()
        return action

    def generate_policy(self, process_data):
        """Generate scheduling policies for all processes with rich metrics."""
        policies = []
        for proc in process_data:
            state = np.array([
                proc["cpu_usage"] / 100.0,
                proc["wait_time"] / 100.0,
                proc["context_switches"] / 12.0,
                proc["memory_usage_mb"] / 768.0,
                proc["io_operations"] / 500.0,
                {"compute": 0.0, "io_bound": 0.5, "mixed": 1.0}[proc["task_type"]] / 1.0,
                proc["runtime_ms"] / 4000.0,
                proc["priority_level"] / 5.0,
                proc["thread_count"] / 5.0,
                proc["disk_read_mb"] / 200.0,
                proc["disk_write_mb"] / 150.0,
                proc["network_tx_mb"] / 100.0,
                proc["network_rx_mb"] / 80.0,
                proc["cache_hits"] / 1000.0,
                proc["cache_misses"] / 200.0,
                proc["page_faults"] / 50.0,
                proc["cpu_cycles"] / 1000000.0,
                proc["instruction_count"] / 500000.0,
                proc["load_avg"] / 2.0,
                proc["temperature_c"] / 80.0,
                proc["power_usage_w"] / 50.0,
                proc["deadline_ms"] / 5000.0,
                proc["dependency_count"] / 5.0,
                proc["error_rate"] / 0.05,
                proc["retry_count"] / 10.0,
                proc["queue_length"] / 20.0,
                proc["preempt_count"] / 5.0,
                proc["affinity_mask"] / 15.0,
                proc["start_time_ms"] / 10000.0,
                proc["completion_time_ms"] / 20000.0
            ])
            action = self.decide_policy(state)
            time_slice = int(800 + action * 1400)  # Range 800-2200 μs
            priority = int(action * 12)  # Range 0-12
            sched_weight = round(0.5 + (proc["cpu_usage"] / 100.0), 2)
            exec_state = "ready" if proc["wait_time"] < 50 else "pending" if proc["io_operations"] < 200 else "running"
            predicted_latency_ms = round(0.3 + (proc["cpu_usage"] / 200.0), 2)

            policy = {
                "pid": proc["pid"],
                "time_slice": time_slice,
                "priority": priority,
                "sched_weight": sched_weight,
                "exec_state": exec_state,
                "predicted_latency_ms": predicted_latency_ms,
                "resource_allocation": round(proc["memory_usage_mb"] / 768.0 * 100, 2),
                "io_priority": int(proc["io_operations"] / 50),
                "network_bandwidth_mb": round(proc["network_tx_mb"] + proc["network_rx_mb"], 1),
                "cache_efficiency": round(proc["cache_hits"] / (proc["cache_hits"] + proc["cache_misses"]) * 100, 2),
                "thermal_threshold": round(proc["temperature_c"] / 80.0 * 100, 2),
                "power_efficiency": round(proc["cpu_cycles"] / proc["power_usage_w"], 2),
                "deadline_compliance": proc["runtime_ms"] < proc["deadline_ms"],
                "dependency_status": proc["dependency_count"] == 0,
                "error_impact": round(proc["error_rate"] * 100, 2),
                "retry_success": proc["retry_count"] < 5,
                "queue_delay_ms": round(proc["queue_length"] * 10, 2),
                "preempt_frequency": proc["preempt_count"] / (proc["runtime_ms"] / 1000),
                "affinity_score": proc["affinity_mask"] / 15.0,
                "execution_window_ms": proc["completion_time_ms"] - proc["start_time_ms"],
                "load_factor": round(proc["load_avg"] * proc["cpu_usage"] / 100.0, 2),
                "instruction_per_cycle": round(proc["instruction_count"] / proc["cpu_cycles"], 4),
                "memory_pressure": round(proc["memory_usage_mb"] / proc["thread_count"], 1),
                "io_throughput_mb": round(proc["io_operations"] * (proc["disk_read_mb"] + proc["disk_write_mb"]) / proc["runtime_ms"], 2),
                "network_latency_ms": round(proc["network_tx_mb"] / (proc["network_rx_mb"] + 1) * 0.5, 2),
                "thermal_risk": proc["temperature_c"] > 70,
                "power_surge": proc["power_usage_w"] > 40,
                "critical_path": proc["priority_level"] > 3,
                "dynamic_adjustment": action == 1
            }
            policies.append(policy)
            logging.info(f"Generated policy for PID {proc['pid']}: Time Slice={time_slice}μs, Priority={priority}")

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w") as f:
            json.dump(policies, f, indent=4)
        logging.info(f"Scheduling policies saved to {self.output_file}")
        return policies

if __name__ == "__main__":
    process_data = [
        {"pid": 1001, "cpu_usage": 80.0, "wait_time": 50.0, "context_switches": 5, "memory_usage_mb": 128.5, "io_operations": 150, "task_type": "compute", "runtime_ms": 2300, "priority_level": 3, "thread_count": 2, "disk_read_mb": 50.0, "disk_write_mb": 30.0, "network_tx_mb": 20.0, "network_rx_mb": 15.0, "cache_hits": 500, "cache_misses": 50, "page_faults": 10, "cpu_cycles": 500000, "instruction_count": 250000, "load_avg": 1.0, "temperature_c": 60.0, "power_usage_w": 25.0, "deadline_ms": 3000, "dependency_count": 2, "error_rate": 0.02, "retry_count": 3, "queue_length": 5, "preempt_count": 1, "affinity_mask": 7, "start_time_ms": 1000, "completion_time_ms": 15000}
    ]
    agent = PPOAgent()
    agent.generate_policy(process_data)