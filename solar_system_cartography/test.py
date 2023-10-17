import math
import numpy as np

# Paramètres orbitaux
longitude_noeud_ascendant_deg = 58.14536  # Longitude du nœud ascendant en degrés
inclinaison_deg = 162.238  # Inclinaison de l'orbite en degrés

# Convertir les angles en radians
longitude_noeud_ascendant_rad = math.radians(longitude_noeud_ascendant_deg)
inclinaison_rad = math.radians(inclinaison_deg)

# Calcul de la direction du demi-grand axe dans le repère XYZ
a = np.array([
    math.cos(longitude_noeud_ascendant_rad) * math.cos(inclinaison_rad),
    math.sin(longitude_noeud_ascendant_rad) * math.cos(inclinaison_rad),
    math.sin(inclinaison_rad)
])

print("Direction du demi-grand axe dans le repère XYZ :")
print(a)
