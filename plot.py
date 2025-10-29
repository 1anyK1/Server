import json
import matplotlib.pyplot as plt

filename = "locations.json"

data = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            data.append(json.loads(line))

data.sort(key=lambda x: x["timestamp"])

latitudes = [point["latitude"] for point in data]
longitudes = [point["longitude"] for point in data]

plt.figure(figsize=(8, 8))
plt.plot(longitudes, latitudes, marker="o", markersize=2, linewidth=1)
plt.title("GPS траектория движения (в порядке времени)")
plt.xlabel("Долгота")
plt.ylabel("Широта")
plt.grid(True)
plt.axis("equal")
plt.show()
