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

def get_cpu_power():
    try:
        cpu_power_cmd = "sudo turbostat --Summary --quiet --show PkgWatt --interval 1"
        result = subprocess.check_output(cpu_power_cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT).strip()
        lines = result.splitlines()
        if len(lines) > 2:
            cpu_power = float(lines[2].split()[-1])  # Extracting the PkgWatt value from the output
            return cpu_power
        else:
            print("Unexpected output format from turbostat.")
            return 0.0
    except subprocess.CalledProcessError as e:
        print(f"Error getting CPU power: {e}")
        return 0.0
    except ValueError:
        print("Failed to convert CPU power to float. Setting it to 0.0")
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

# Generate dynamic file name based on the current date and time
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'resource_usage_{current_datetime}.csv'

# Write the header of the CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Time', 'CPU Usage (%)', 'CPU Power (W)', 'RAM Usage (GB)', 'GPU Usage (%)', 'GPU Power (W)']
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
    count += 1

    if gpu_power > peak_gpu_power:
        peak_gpu_power = gpu_power

    if cpu_power > peak_cpu_power:
        peak_cpu_power = cpu_power

    avg_gpu_power = (avg_gpu_power * (count - 1) + gpu_power) / count
    avg_cpu_power = (avg_cpu_power * (count - 1) + cpu_power) / count

    print(f"Time:    [{current_time}]")
    print(f"CPU:     {cpu_usage:<7.2f}%  Power: {cpu_power:<7.2f} W  Peak: {peak_cpu_power:<7.2f} W  Avg: {avg_cpu_power:<7.2f} W")
    print(f"RAM:     {ram_usage:<7.2f} GB")
    print(f"GPU:     {gpu_utilization:<7.2f}%  Power: {gpu_power:<7.2f} W  Peak: {peak_gpu_power:<7.2f} W  Avg: {avg_gpu_power:<7.2f} W")
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
            'GPU Power (W)': gpu_power
        })

    time.sleep(1)
