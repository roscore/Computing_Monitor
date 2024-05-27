import time
import datetime
import subprocess
import psutil
import csv
import os

def get_gpu_power():
    try:
        power_cmd = "nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits"
        power = subprocess.check_output(power_cmd, shell=True)
        return float(power)
    except subprocess.CalledProcessError as e:
        print(f"Error getting GPU power: {e}")
        return 0.0

def get_gpu_utilization():
    try:
        utilization_cmd = "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits"
        utilization = subprocess.check_output(utilization_cmd, shell=True).strip()
        return float(utilization)
    except subprocess.CalledProcessError as e:
        print(f"Error getting GPU utilization: {e}")
        return 0.0

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().used / (1024 ** 3)  # Convert bytes to GB

# 현재 날짜와 시간 기반으로 동적 파일 이름 생성
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'resource_usage_{current_datetime}.csv'

# CSV 파일 헤더 작성
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Time', 'CPU Usage (%)', 'RAM Usage (GB)', 'GPU Usage (%)', 'GPU Power (W)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

peak_gpu_power = 0
avg_gpu_power = 0
avg_cpu_usage = 0
count = 0

while True:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    gpu_utilization = get_gpu_utilization()
    gpu_power = get_gpu_power()
    count += 1

    if gpu_power > peak_gpu_power:
        peak_gpu_power = gpu_power

    avg_gpu_power = (avg_gpu_power * (count - 1) + gpu_power) / count
    avg_cpu_usage = (avg_cpu_usage * (count - 1) + cpu_usage) / count

    print(f"Time:    [{current_time}]")
    print(f"CPU:     {cpu_usage:<7.2f}%  Avg: {avg_cpu_usage:<7.2f}%")
    print(f"RAM:     {ram_usage:<7.2f} GB")
    print(f"GPU:     {gpu_utilization:<7.2f}%  Power: {gpu_power:<7.2f} W  Peak: {peak_gpu_power:<7.2f} W  Avg: {avg_gpu_power:<7.2f} W")
    print("-----------------------------")

    # 현재 데이터를 CSV 파일에 추가
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'Time': current_time,
            'CPU Usage (%)': cpu_usage,
            'RAM Usage (GB)': ram_usage,
            'GPU Usage (%)': gpu_utilization,
            'GPU Power (W)': gpu_power
        })

    time.sleep(1)
