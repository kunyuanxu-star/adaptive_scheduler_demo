import os
import json
import logging
from data_collector import DataCollector
from ppo_agent import PPOAgent
import pandas as pd

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Collect process data
    collector = DataCollector()
    process_data = collector.collect()
    
    # Generate scheduling policies
    agent = PPOAgent()
    policies = agent.generate_policy(process_data)
    
    # Generate detailed report
    report_file = os.path.join("src", "shared", "report.txt")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, "w") as f:
        f.write("=== Adaptive Scheduler Report ===\n")
        f.write(f"Generated on: {pd.Timestamp.now()}\n\n")
        for policy in policies:
            f.write(f"PID: {policy['pid']}\n")
            for key, value in policy.items():
                f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
    logging.info(f"Detailed report saved to {report_file}")
    
    # Generate CSV metrics
    csv_file = os.path.join("src", "shared", "metrics.csv")
    df = pd.DataFrame(policies)
    df.to_csv(csv_file, index=False)
    logging.info(f"Metrics saved to {csv_file}")

if __name__ == "__main__":
    main()