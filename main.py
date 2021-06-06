

#User input (in)
total_length = 240
total_height = 24

#Material Properties (lb/in^3,psi)
density = 0.2834
youngs_modulus = 2.9e7
yield_strength = 60200

#Loading (lbs)
force_in = -250


#Calculate Reactionary Forces r1x, r1y, r2x
r1x = force_in * (total_length / total_height)
r1y = -1 * force_in
r2x = -1 * force_in * (total_length / total_height)

print(r1x, r1y, r2x)