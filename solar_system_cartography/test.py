import math
"""
# Constantes
G = 6.67430e-11  # Constante gravitationnelle en m^3/kg/s^2
M_soleil = 1.989e30  # Masse du Soleil en kg
Rayon_orbite = 1.496e11  # Rayon moyen de l'orbite terrestre en mètres
Periode_orbite = 365.25 * 24 * 3600  # Période orbitale de la Terre en secondes
circumference = 939951248818.1 #meters
# Calcul de la vitesse orbitale (loi de Kepler)
Vitesse_orbitale = (2 * math.pi * Rayon_orbite) / Periode_orbite

# Durée pendant laquelle vous souhaitez calculer la distance parcourue (en secondes)
Temps = 60 * 60 * 24 * 30  # Par exemple, 30 jours

# Calcul de la distance parcourue
Distance = circumference / 100 * (Vitesse_orbitale * Temps)

print(f"Distance parcourue en {Temps} secondes : {Distance} mètres")
"""

orbital_period = 87.95601264719063
t = ((0.30751072261083995 * 149597870700) / 58983.30058671956)/3600

c = 363853292112.728 #circonference en metres

d = 58983.30058671956 * (24*3600) #perihelion v*t
print(f"en un jour au plus proche du soleil, mercure parcourt : {d} metres")
p_max = 100 * d / c
print(f"soit {p_max} % de sa revolution")

d = 38865.572317592916 * (24*3600) #aphelion v*t
print(f"en un jour au plus loin du soleil, mercure parcourt : {d} metres")
p_min = 100 * d / c
print(f"soit {p_min} % de sa revolution")

# essaie de calculer la variation de pourcentage entre ces deux distances.
# exemple :
# {0 : 1.85,
#  1 : 1.8,
#  2 : 1.7,
#  3 : 1.8,
#  4 : 1.85
# }
# et on additionne le pourcentage de chaque jour pour avoir le pourcentage à appliquer dans le pointOnCurveInfo

def get_covered_distance_each_day() ->dict:
    orbital_period = 87.95601264719063
    t = ((0.30751072261083995 * 149597870700) / 58983.30058671956)/3600

    c = 363853292112.728 #circonference en metres

    d = 58983.30058671956 * (24*3600) #perihelion v*t
    print(f"en un jour au plus proche du soleil, mercure parcourt : {d} metres")
    p_max = 100 * d / c
    print(f"soit {p_max} % de sa revolution")

    d = 38865.572317592916 * (24*3600) #aphelion v*t
    print(f"en un jour au plus loin du soleil, mercure parcourt : {d} metres")
    p_min = 100 * d / c
    print(f"soit {p_min} % de sa revolution")

    transition_dict = {} 
    max_to_min_speed_range = range(0, int(orbital_period / 2))
    for key in max_to_min_speed_range:
        transition_value = p_max + (p_min - p_max) * (key - max_to_min_speed_range.start) / (max_to_min_speed_range.stop - 1)
        
        transition_dict[key] = transition_value

    min_to_max_speed_range = range(int(orbital_period / 2), int(orbital_period)+2)
    for key in min_to_max_speed_range:
        transition_value = p_min + (p_max - p_min) * (key - min_to_max_speed_range.start) / (min_to_max_speed_range.stop - 1)
        
        transition_dict[key] = transition_value

    return transition_dict

import json
print(json.dumps(transition_dict, indent=4))

