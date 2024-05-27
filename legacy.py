import time
import datetime
import subprocess
import psutil
import os

def get_gpu_power():
    power_cmd = "nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits"
    power = subprocess.check_output(power_cmd, shell=True)
    return float(power)

def get_cpu_power():
    cpu_power_cmd = "sensors | awk '/Package id 0:/ {print $4}' | cut -c 2-5"
    cpu_power = subprocess.check_output(cpu_power_cmd, shell=True)
    return float(cpu_power)

peak_gpu_power = 0
peak_cpu_power = 0
avg_gpu_power = 0
avg_cpu_power = 0
count = 0

while True:
    os.system('cls' if os.name=='nt' else 'clear')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    gpu_power = get_gpu_power()
    cpu_power = get_cpu_power()
    count += 1
    
    if gpu_power > peak_gpu_power:
        peak_gpu_power = gpu_power

    if cpu_power > peak_cpu_power:
        peak_cpu_power = cpu_power

    avg_gpu_power = (avg_gpu_power * (count - 1) + gpu_power) / count
    avg_cpu_power = (avg_cpu_power * (count - 1) + cpu_power) / count

    print(f"Time:    [{current_time}]")
    print(f"GPU:     {gpu_power:<7.2f} W  Peak: {peak_gpu_power:<7.2f} W  Avg: {avg_gpu_power:<7.2f} W")
    print(f"CPU:     {cpu_power:<7.2f} W  Peak: {peak_cpu_power:<7.2f} W  Avg: {avg_cpu_power:<7.2f} W")
    print("-----------------------------")
    time.sleep(0.1)
