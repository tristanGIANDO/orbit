import numpy as np
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body

# Paramètres de l'orbite (exemple)
orbital_period = 10 * u.day  # Période orbitale de 10 jours
start_time = Time("2023-01-01T00:00:00", format="isot")

# Liste pour stocker les coordonnées
coordinates = []

# Calcul de la position à chaque intervalle de temps
current_time = start_time
while current_time < start_time + 365 * u.day:  # Exemple : calcul sur une année
    with solar_system_ephemeris.set('builtin'):
        body = get_body('earth', current_time)
        coord = body.heliocentrictrueecliptic
        coordinates.append(coord)

    current_time += orbital_period

# Calcul de la circonférence de l'orbite (ellipse)
a = coordinates[0].spherical.distance.mean()
b = a  # Pour une orbite circulaire, le demi-petit-axe est égal au demi-grand axe
circumference = 2 * np.pi * np.sqrt((a**2 + b**2) / 2)

# Calcul de la longueur parcourue en 10 jours
length_covered = 0 * u.m  # Initialisez la longueur parcourue avec des unités astropy
for i in range(1, len(coordinates)):
    delta_longitude = coordinates[i].lon - coordinates[i - 1].lon
    delta_latitude = coordinates[i].lat - coordinates[i - 1].lat
    delta_length = np.sqrt(delta_longitude**2 + delta_latitude**2)
    length_covered += delta_length

# Calcul du pourcentage
percentage_covered = (length_covered / circumference) * 100

print(f"Pourcentage de la circonférence parcouru en 10 jours : {percentage_covered:.2f}")
