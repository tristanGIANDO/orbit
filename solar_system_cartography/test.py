import math

# Constantes
G = 6.67430e-11  # m^3/kg/s^2
M_soleil = 1.989e30  # kg
a = 1.496e11  # m (demi-grand axe de l'orbite terrestre)
e = 0.0167  # Excentricité de l'orbite terrestre
M_terre = 5.972e24  # Masse de la Terre en kilogrammes

# Calcul de la distance au Soleil au périhélie
r_min = a * (1 - e)

# Calcul de la vitesse maximale de la Terre (au périhélie)
v_max_terre = math.sqrt(G * (M_soleil + M_terre) * (2 / r_min - 1 / a))

print("La vitesse maximale de la Terre au périhélie est d'environ", v_max_terre, "m/s")
