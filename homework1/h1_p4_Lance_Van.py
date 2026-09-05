import math
import numpy as np
import matplotlib.pyplot as plt
def plot_function(fun_str, domain, ns):
  xs = np.linspace(domain[0], domain[1], ns)
  ys = []
  # using eval, it takes the string and evaluate it and I looped it to append to the empty list
  for x in xs:
    y = eval(fun_str)
    ys.append(y)
    # using .format I left aligned x and y
  print("{:>10}{:>10}".format("x", "y"))
  for i in range(len(ys)):
    print("{:10.2f}{:10.2f}".format(xs[i], ys[i]))
  plt.plot(xs, ys)
  plt.xlabel("x")
  plt.ylabel("y")
  plt.title(fun_str)
  plt.grid()
  plt.show()


funstr = input("Enter function with variable x: ")
xmin = float(input("Enter minimum x: "))
xmax = float(input("Enter maximum x: "))
domain = (xmin, xmax)
ns = int(input("Enter number of samples: "))
plot_function(funstr, domain, ns)