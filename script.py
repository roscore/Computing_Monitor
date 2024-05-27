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
    return psutil.cpu_percent(interval=0.1)

def get_ram_usage():
    return psutil.virtual_memory().used / (1024 ** 3)  # Convert bytes to GB

# 현재 날짜와 시간 기반으로 동적 파일 이름 생성
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'resource_usage_{current_datetime}.csv'

# CSV 파일 헤더 작성
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = [
        'Time', 'CPU Usage (%)', 'RAM Usage (GB)', 
        'GPU Usage (%)', 'GPU Power (W)',
        'Min CPU Usage (%)', 'Max CPU Usage (%)', 'Avg CPU Usage (%)',
        'Min RAM Usage (GB)', 'Max RAM Usage (GB)', 'Avg RAM Usage (GB)',
        'Min GPU Usage (%)', 'Max GPU Usage (%)', 'Avg GPU Usage (%)',
        'Min GPU Power (W)', 'Max GPU Power (W)', 'Avg GPU Power (W)'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# 초기화
min_cpu_usage = float('inf')
max_cpu_usage = float('-inf')
total_cpu_usage = 0

min_ram_usage = float('inf')
max_ram_usage = float('-inf')
total_ram_usage = 0

min_gpu_utilization = float('inf')
max_gpu_utilization = float('-inf')
total_gpu_utilization = 0

min_gpu_power = float('inf')
max_gpu_power = float('-inf')
total_gpu_power = 0

count = 0

while True:
    start_time = time.time()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    gpu_utilization = get_gpu_utilization()
    gpu_power = get_gpu_power()
    count += 1

    # CPU 사용량 업데이트
    min_cpu_usage = min(min_cpu_usage, cpu_usage)
    max_cpu_usage = max(max_cpu_usage, cpu_usage)
    total_cpu_usage += cpu_usage
    avg_cpu_usage = total_cpu_usage / count

    # RAM 사용량 업데이트
    min_ram_usage = min(min_ram_usage, ram_usage)
    max_ram_usage = max(max_ram_usage, ram_usage)
    total_ram_usage += ram_usage
    avg_ram_usage = total_ram_usage / count

    # GPU 사용량 업데이트
    min_gpu_utilization = min(min_gpu_utilization, gpu_utilization)
    max_gpu_utilization = max(max_gpu_utilization, gpu_utilization)
    total_gpu_utilization += gpu_utilization
    avg_gpu_utilization = total_gpu_utilization / count

    # GPU 전력 업데이트
    min_gpu_power = min(min_gpu_power, gpu_power)
    max_gpu_power = max(max_gpu_power, gpu_power)
    total_gpu_power += gpu_power
    avg_gpu_power = total_gpu_power / count

    print(f"Time:    [{current_time}]")
    print(f"CPU:     {cpu_usage:<7.2f}%  Min: {min_cpu_usage:<7.2f}%  Max: {max_cpu_usage:<7.2f}%  Avg: {avg_cpu_usage:<7.2f}%")
    print(f"RAM:     {ram_usage:<7.2f} GB  Min: {min_ram_usage:<7.2f} GB  Max: {max_ram_usage:<7.2f} GB  Avg: {avg_ram_usage:<7.2f} GB")
    print(f"GPU:     {gpu_utilization:<7.2f}%  Power: {gpu_power:<7.2f} W  Min: {min_gpu_power:<7.2f} W  Max: {max_gpu_power:<7.2f} W  Avg: {avg_gpu_power:<7.2f} W")
    print("-----------------------------")

    # 현재 데이터를 CSV 파일에 추가
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'Time': current_time,
            'CPU Usage (%)': cpu_usage,
            'RAM Usage (GB)': ram_usage,
            'GPU Usage (%)': gpu_utilization,
            'GPU Power (W)': gpu_power,
            'Min CPU Usage (%)': min_cpu_usage,
            'Max CPU Usage (%)': max_cpu_usage,
            'Avg CPU Usage (%)': avg_cpu_usage,
            'Min RAM Usage (GB)': min_ram_usage,
            'Max RAM Usage (GB)': max_ram_usage,
            'Avg RAM Usage (GB)': avg_ram_usage,
            'Min GPU Usage (%)': min_gpu_utilization,
            'Max GPU Usage (%)': max_gpu_utilization,
            'Avg GPU Usage (%)': avg_gpu_utilization,
            'Min GPU Power (W)': min_gpu_power,
            'Max GPU Power (W)': max_gpu_power,
            'Avg GPU Power (W)': avg_gpu_power
        })

    # 다음 측정을 0.1초 간격으로 실행
    elapsed_time = time.time() - start_time
    sleep_time = max(0, 0.1 - elapsed_time)
    time.sleep(sleep_time)
