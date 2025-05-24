import os
import json
import logging
from data_collector import DataCollector
from ppo_agent import PPOAgent
import pandas as pd
import numpy as np

def main():
    # 设置日志格式
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 收集进程数据
    collector = DataCollector()
    process_data = collector.collect()
    
    # 打印进程数据摘要
    print("\n=== 进程数据摘要 ===")
    print(f"总进程数: {len(process_data)}")
    cpu_usages = [proc["cpu_usage"] for proc in process_data]
    memory_usages = [proc["memory_usage_mb"] for proc in process_data]
    wait_times = [proc["wait_time"] for proc in process_data]
    print(f"平均CPU使用率: {np.mean(cpu_usages):.2f}% (最小: {np.min(cpu_usages):.2f}%, 最大: {np.max(cpu_usages):.2f}%)")
    print(f"平均内存使用量: {np.mean(memory_usages):.2f}MB (最小: {np.min(memory_usages):.2f}MB, 最大: {np.max(memory_usages):.2f}MB)")
    print(f"平均等待时间: {np.mean(wait_times):.2f}μs (最小: {np.min(wait_times):.2f}μs, 最大: {np.max(wait_times):.2f}μs)")
    task_types = [proc["task_type"] for proc in process_data]
    task_type_counts = {tt: task_types.count(tt) for tt in set(task_types)}
    print("任务类型分布:")
    for tt, count in task_type_counts.items():
        print(f"  {tt}: {count} 个 ({count/len(process_data)*100:.1f}%)")
    
    # 生成调度策略
    agent = PPOAgent()
    policies = agent.generate_policy(process_data)
    
    # 打印调度策略摘要
    print("\n=== 调度策略摘要 ===")
    print(f"总策略数: {len(policies)}")
    time_slices = [policy["time_slice"] for policy in policies]
    priorities = [policy["priority"] for policy in policies]
    predicted_latencies = [policy["predicted_latency_ms"] for policy in policies]
    print(f"平均时间片: {np.mean(time_slices):.0f}μs (最小: {np.min(time_slices):.0f}μs, 最大: {np.max(time_slices):.0f}μs)")
    print(f"平均优先级: {np.mean(priorities):.1f} (最小: {np.min(priorities):.0f}, 最大: {np.max(priorities):.0f})")
    print(f"平均预测延迟: {np.mean(predicted_latencies):.2f}ms (最小: {np.min(predicted_latencies):.2f}ms, 最大: {np.max(predicted_latencies):.2f}ms)")
    
    # 状态分布
    exec_states = [policy["exec_state"] for policy in policies]
    state_counts = {state: exec_states.count(state) for state in set(exec_states)}
    print("执行状态分布:")
    for state, count in state_counts.items():
        print(f"  {state}: {count} 个 ({count/len(policies)*100:.1f}%)")
    
    # 风险分析
    thermal_risks = sum(1 for policy in policies if policy["thermal_risk"])
    power_surges = sum(1 for policy in policies if policy["power_surge"])
    deadline_misses = sum(1 for policy in policies if not policy["deadline_compliance"])
    print("\n=== 风险分析 ===")
    print(f"热风险进程数: {thermal_risks} ({thermal_risks/len(policies)*100:.1f}%)")
    print(f"功耗激增进程数: {power_surges} ({power_surges/len(policies)*100:.1f}%)")
    print(f"未满足截止时间进程数: {deadline_misses} ({deadline_misses/len(policies)*100:.1f}%)")
    
    # 打印前5个进程的详细策略
    print("\n=== 前5个进程的详细调度策略 ===")
    for policy in policies[:5]:
        print(f"\nPID: {policy['pid']}")
        print(f"  时间片: {policy['time_slice']}μs")
        print(f"  优先级: {policy['priority']}")
        print(f"  执行状态: {policy['exec_state']}")
        print(f"  预测延迟: {policy['predicted_latency_ms']}ms")
        print(f"  资源分配: {policy['resource_allocation']}%")
        print(f"  网络带宽: {policy['network_bandwidth_mb']}MB")
        print(f"  热风险: {'是' if policy['thermal_risk'] else '否'}")
        print(f"  功耗激增: {'是' if policy['power_surge'] else '否'}")
        print(f"  截止时间合规: {'是' if policy['deadline_compliance'] else '否'}")
    
    # 生成详细报告
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
    
    # 生成CSV指标
    csv_file = os.path.join("src", "shared", "metrics.csv")
    df = pd.DataFrame(policies)
    df.to_csv(csv_file, index=False)
    logging.info(f"Metrics saved to {csv_file}")

if __name__ == "__main__":
    main()