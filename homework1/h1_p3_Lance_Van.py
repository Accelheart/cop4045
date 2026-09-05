import numpy as np
def find_dup_str(s,n):
  # using two loops I had it splice a piece and then I compare the pieces together and if they are equal it returns a piece
  for i in range(0, len(s)-n+1):
    piece1 = s[i:i+n]
    for j in range(i+n, len(s)-n+1):
      piece2 = s[j:j+n]
      if piece1 == piece2:
        return piece1
  return ""

  find_dup_str("abcdefbcdgh")