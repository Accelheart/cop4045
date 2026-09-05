def find_pythagorean(n):
  tuples = []
  # created multiple loops to loop through all the possible tuples for a,b,c within n+1 range
  # appeds the possible tuples if they fall within the equation
  for a in range(1, n+1):
    for b in range(a, n+1):
      for c in range(b, n+1):
        if a**2 + b**2 == c**2:
          tuples.append((a, b, c))
  return tuples

  find_pythagorean(50)