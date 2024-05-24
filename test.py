import time
import datetime
import subprocess
import psutil
import csv
import os

def get_gpu_power():
    power_cmd = "nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits"
    power = subprocess.check_output(power_cmd, shell=True)
    return float(power)

def get_cpu_power():
    cpu_power_cmd = "sensors | awk '/Package id 0:/ {print $4}' | cut -c 2-5"
    cpu_power = subprocess.check_output(cpu_power_cmd, shell=True)
    return float(cpu_power)

def get_gpu_utilization():
    utilization_cmd = "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits"
    utilization = subprocess.check_output(utilization_cmd, shell=True)
    return float(utilization)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().used / (1024 ** 3)  # Convert bytes to GB

def get_cpu_instructions():
    instructions_cmd = "perf stat -e instructions -a sleep 1 2>&1 | grep instructions | awk '{print $1}'"
    instructions = subprocess.check_output(instructions_cmd, shell=True, universal_newlines=True)
    return int(instructions.replace(',', ''))

def get_gpu_flops():
    flops_cmd = "nvidia-smi dmon -s u | grep '^[0-9]' | awk '{print $5}'"
    flops = subprocess.check_output(flops_cmd, shell=True)
    return int(flops)

# Generate dynamic file name based on the current date and time
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'resource_usage_{current_datetime}.csv'

# Write the header of the CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Time', 'CPU Usage (%)', 'CPU Power (W)', 'RAM Usage (GB)', 'GPU Usage (%)', 'GPU Power (W)', 'CPU Instructions', 'GPU FLOPS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

peak_gpu_power = 0
peak_cpu_power = 0
avg_gpu_power = 0
avg_cpu_power = 0
count = 0

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    gpu_utilization = get_gpu_utilization()
    gpu_power = get_gpu_power()
    cpu_power = get_cpu_power()
    cpu_instructions = get_cpu_instructions()
    gpu_flops = get_gpu_flops()
    count += 1

    if gpu_power > peak_gpu_power:
        peak_gpu_power = gpu_power

    if cpu_power > peak_cpu_power:
        peak_cpu_power = cpu_power

    avg_gpu_power = (avg_gpu_power * (count - 1) + gpu_power) / count
    avg_cpu_power = (avg_cpu_power * (count - 1) + cpu_power) / count

    print(f"Time:    [{current_time}]")
    print(f"CPU:     {cpu_usage:<7.2f}%  Power: {cpu_power:<7.2f} W  Instructions: {cpu_instructions}  Peak: {peak_cpu_power:<7.2f} W  Avg: {avg_cpu_power:<7.2f} W")
    print(f"RAM:     {ram_usage:<7.2f} GB")
    print(f"GPU:     {gpu_utilization:<7.2f}%  Power: {gpu_power:<7.2f} W  FLOPS: {gpu_flops}  Peak: {peak_gpu_power:<7.2f} W  Avg: {avg_gpu_power:<7.2f} W")
    print("-----------------------------")

    # Append the current data to the CSV file
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'Time': current_time,
            'CPU Usage (%)': cpu_usage,
            'CPU Power (W)': cpu_power,
            'RAM Usage (GB)': ram_usage,
            'GPU Usage (%)': gpu_utilization,
            'GPU Power (W)': gpu_power,
            'CPU Instructions': cpu_instructions,
            'GPU FLOPS': gpu_flops
        })

    time.sleep(1
