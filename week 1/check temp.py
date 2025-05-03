import numpy as np
temperatures = np.array([18.5, 19, 20, 25.0, 2, 30, 13.9])

avg_temp = np.mean(temperatures)
print(f"average temperature:{avg_temp: .2f}degree celsius")

max_temp = np.max(temperatures)
min_temp = np.min(temperatures)
print(f"maximum temperature:{max_temp}degree celsius")
print(f"minimum temperature:{min_temp}degree celsius")

temp_farenheit = (temperatures*9/5)+32
print(f"temperature in Farenheit:",temp_farenheit)

above_20_indices = np.where(temperatures>20)[0]
print(f"Days with temperature above 20 degree celcius(by indices):",above_20_indices)



