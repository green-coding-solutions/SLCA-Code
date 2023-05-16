import matplotlib.pyplot as plt
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

APP_NAME = "gcb_power_logger"
app_support_path = Path.home() / 'Library' / 'Application Support' / APP_NAME
app_support_path.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = app_support_path / 'logger.txt'

# Initialize lists to hold time and energy data
times = []
energies = []

# Open the file and process each line
with open(OUTPUT_FILE, 'r') as f:
    for line in f:
        data = json.loads(line)
        time = datetime.fromtimestamp(data['time'] // 1000000000)  # Convert ns to s
        energy = data['cpu_energy'] + data['gpu_energy'] + data['ane_energy']
        times.append(time)
        energies.append(energy)

# Convert to pandas DataFrame for easier plotting
df = pd.DataFrame({
    'time': times,
    'energy': energies
})

print(sum(energies))

# Plot
plt.figure(figsize=(10, 5))
plt.scatter(df['time'], df['energy'])
plt.xlabel('Time')
plt.ylabel('mJ')
plt.title('Energy over Time')
plt.grid(True)
plt.show()
