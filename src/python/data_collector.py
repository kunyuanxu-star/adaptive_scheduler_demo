import numpy as np
import json
import os
import logging

class DataCollector:
    """Simulates eBPF process state collection."""
    def __init__(self):
        self.processes = list(range(1001, 1031))  # 30 simulated PIDs (1001-1030)
        self.output_file = os.path.join("src", "shared", "process_data.json")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def collect(self):
        """Simulate collecting process data with rich metrics."""
        data = []
        for pid in self.processes:
            cpu_usage = np.random.uniform(10, 95)
            wait_time = np.random.uniform(10, 100)
            context_switches = np.random.randint(1, 12)
            memory_usage_mb = np.random.uniform(32, 768)
            io_operations = np.random.randint(20, 500)
            task_type = np.random.choice(["compute", "io_bound", "mixed"])
            runtime_ms = np.random.randint(500, 4000)
            priority_level = np.random.randint(1, 6)
            thread_count = np.random.randint(1, 6)
            disk_read_mb = np.random.uniform(10, 200)
            disk_write_mb = np.random.uniform(5, 150)
            network_tx_mb = np.random.uniform(1, 100)
            network_rx_mb = np.random.uniform(1, 80)
            cache_hits = np.random.randint(100, 1000)
            cache_misses = np.random.randint(10, 200)
            page_faults = np.random.randint(0, 50)
            cpu_cycles = np.random.randint(100000, 1000000)
            instruction_count = np.random.randint(50000, 500000)
            load_avg = np.random.uniform(0.1, 2.0)
            temperature_c = np.random.uniform(40, 80)
            power_usage_w = np.random.uniform(10, 50)
            deadline_ms = np.random.randint(1000, 5000)
            dependency_count = np.random.randint(0, 5)
            error_rate = np.random.uniform(0, 0.05)
            retry_count = np.random.randint(0, 10)
            queue_length = np.random.randint(0, 20)
            preempt_count = np.random.randint(0, 5)
            affinity_mask = np.random.randint(0, 15)
            start_time_ms = np.random.randint(0, 10000)
            completion_time_ms = np.random.randint(10000, 20000)

            process_data = {
                "pid": pid,
                "cpu_usage": round(cpu_usage, 2),
                "wait_time": round(wait_time, 2),
                "context_switches": context_switches,
                "memory_usage_mb": round(memory_usage_mb, 1),
                "io_operations": io_operations,
                "task_type": task_type,
                "runtime_ms": runtime_ms,
                "priority_level": priority_level,
                "thread_count": thread_count,
                "disk_read_mb": round(disk_read_mb, 1),
                "disk_write_mb": round(disk_write_mb, 1),
                "network_tx_mb": round(network_tx_mb, 1),
                "network_rx_mb": round(network_rx_mb, 1),
                "cache_hits": cache_hits,
                "cache_misses": cache_misses,
                "page_faults": page_faults,
                "cpu_cycles": cpu_cycles,
                "instruction_count": instruction_count,
                "load_avg": round(load_avg, 2),
                "temperature_c": round(temperature_c, 1),
                "power_usage_w": round(power_usage_w, 1),
                "deadline_ms": deadline_ms,
                "dependency_count": dependency_count,
                "error_rate": round(error_rate, 4),
                "retry_count": retry_count,
                "queue_length": queue_length,
                "preempt_count": preempt_count,
                "affinity_mask": affinity_mask,
                "start_time_ms": start_time_ms,
                "completion_time_ms": completion_time_ms
            }
            data.append(process_data)
            logging.info(f"Collected data for PID {pid}: CPU Usage={cpu_usage:.2f}%, Memory={memory_usage_mb:.1f}MB")

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Collected data saved to {self.output_file}")
        return data