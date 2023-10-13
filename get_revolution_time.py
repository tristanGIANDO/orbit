mercury = 57910000000  #  in meters
jupiter = 778340000000

def get_revolution_time(semi_major_axis):
    # Using Kepler's law to calculate the orbital period (T)
    gravitational_constant = 6.67430e-11  # Newton's gravitational constant
    solar_mass = 1.989e30  # Solar mass in kilograms
    
    orbital_period = 2 * math.pi * math.sqrt((semi_major_axis**3) / (gravitational_constant * solar_mass))
    
    # Conversion to days
    orbital_period_days = orbital_period / (60 * 60 * 24)
    
    return orbital_period_days
    
print(get_revolution_time(jupiter))