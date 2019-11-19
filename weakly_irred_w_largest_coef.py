import numpy as np
import sympy 
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_irreducible_p
from sympy import prime
import math
import xlsxwriter
  
# Workbook is created 
wb = xlsxwriter.Workbook("wi-polynomial-w-firstcoef-results.xlsx")

# Worksheets   
prop = wb.add_worksheet('Proportions') 
total = wb.add_worksheet('Totals') 
examples = wb.add_worksheet('Examples') 

# Determines if irreducible
def is_irreducible(f, p): return gf_irreducible_p(f,p, ZZ)

# Test
print(is_irreducible([3, 2, 4], 5))
print(is_irreducible([1, 4, 2, 2, 3, 2, 4, 1, 4, 0, 4], 5))

# Convert integer to array of digits 
def num_to_arr(n):
   x = []
   n_str = str(n) 
   for i in n_str:
      try: elt = int(i)
      except: elt = ord(i) - 55
      x += [elt]
   return x

# Add the polynomial jx^m to polyn represented as arr
def add_jx_tothe_m(arr,j,m): 
   cpy = arr.copy()
   k = len(arr) - m  - 1
   cpy[k] = cpy[k] + j
   return cpy

# Only consider monics - but still include changing largest coeff

# Determine if polynomial x is weakly irreducible of F_p
def is_wi_poly(x, p):
   # must be irreducible
   if not is_irreducible(x,p): return False
   # for each cofficient (other then the highest degree)
   for m in range(0, len(x)):
      for j in range(1,p):
         z = x.copy()
         y = add_jx_tothe_m(z, j, m)
         print("\t", y)
         # each  x +jx^m must be reducible 
         if is_irreducible(y,p): return False
   return True

# If a is exact power b return True else return False
def is_power(a,b): return b ** int(round(math.log(a, b))) == a
power = 12
# row, column 
for e in range(3, power + 1):
   total.write(e, 0, "p^" + str(e)) 
   prop.write(e, 0, "p^" + str(e)) 

examples.set_column(1,13,30.0)

# Iterate through the primes
for k in range(1,10):
   
   p = prime(k)
   if p > 4: power = 7
   if p > 10: power = 4
   if p > 20: power = 3

   # Write p to each rows 
   total.write(0, k, p) 
   prop.write(0, k, p) 
   examples.write(0, k, p) 

   # Initialize counts 
   ired_count = 0
   wi_count = 0

   n = p**power
   for i in range(n + 1):
      # Make polynomial x 
      x = num_to_arr(np.base_repr(i, p))
      x = [1] + x
      try:
         print(i,x)
         # Check if irreducible and if weakly irreducible
         irred = is_irreducible(x,p)
         wi = is_wi_poly(x,p)
         if irred: ired_count += 1 
         if wi: 
            wi_count += 1 
            examples.write(wi_count, k, str(x)) 
      except:
         irred = "exception"
         wi = "exception"

      # Write to proportions adn totals
      if i > 0 and is_power(i,p) and int(round(math.log(i, p))) > 2:
         e = int(round(math.log(i, p))) 
         total.write(e, k, wi_count) 
         prop.write(e, k, 1.0 * wi_count/ired_count)

wb.close()

