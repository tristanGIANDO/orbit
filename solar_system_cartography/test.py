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

def get_object_position():
    pos_at_perihelion = [0,-1]
def get_circumference_percentage(self, radius:float, time:int) ->float:
    # time in days
    # radius = perihelion distance at first

    # Kepler's law
    orbital_speed = (2 * math.pi * Rayon_orbite) / self._orbital_period

    # percentage of covered distance
    percentage = self._orbital_circumference / 100 * (orbital_speed * time)

get_circumference_percentage()