import math
import matplotlib.pyplot as plt
import numpy as np

while True:
  print("Enter value for a")
  a = input()
  if a == "":
    print("Stopped")
    break
  coefA = float(a)
  print("Enter value for b")
  coefB = float(input())
  print("Enter value for c")
  coefC = float(input())
  if coefA == 0:
    print("not a quadratic equation")
    break
  # figured I would make part of the quadratic equation as a var and then test if its less than, greater, or equal to 0 to see how many solutions 
  quadraticPart = coefB**2 - 4 * coefA * coefC
  if quadraticPart < 0:
    print("no real solutions")
    xopt = -coefB / (2 * coefA)
    x = np.linspace(xopt - 2, xopt + 2, 150)
  elif quadraticPart == 0:
    x1 = (-coefB + math.sqrt(quadraticPart)) / (2 * coefA)
    print(f"one solution x1 = {x1}")
    x = np.linspace(x1 - 2, x1 + 2, 150)
  elif quadraticPart > 0:
    x1 = (-coefB + math.sqrt(quadraticPart)) / (2 * coefA)
    x2 = (-coefB - math.sqrt(quadraticPart)) / (2 * coefA)
    print(f"two solutions: x1 = {x1}, x2 = {x2}")
    x = np.linspace(min(x1,x2)-2,max(x1,x2)+2, 150)

  y = coefA * x**2 + coefB * x + coefC
  plt.plot(x, y)
  plt.xlabel("x")
  plt.ylabel("y")
  plt.grid()
  plt.show()