import json
import matplotlib.pyplot as plt

# Имя файла с данными
filename = "locations.json"

# Чтение данных построчно (каждая строка — отдельный JSON-объект)
data = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            data.append(json.loads(line))

# 📅 Сортируем по времени
data.sort(key=lambda x: x["timestamp"])

# Извлекаем координаты
latitudes = [point["latitude"] for point in data]
longitudes = [point["longitude"] for point in data]

# --- Построение траектории ---
plt.figure(figsize=(8, 8))
plt.plot(longitudes, latitudes, marker="o", markersize=2, linewidth=1)
plt.title("GPS траектория движения (в порядке времени)")
plt.xlabel("Долгота")
plt.ylabel("Широта")
plt.grid(True)
plt.axis("equal")  # одинаковый масштаб
plt.show()
