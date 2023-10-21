import math

from solar_system_cartography import envs, utils

class ObjectInOrbit():
    def __init__(self, object_name:str, object_mass:float, semi_major_axis:float,
                 inclination:float, eccentricity:float, rotation_period:float,
                 axis_inclination:float, object_radius:float,
                 attraction_mass:float = envs.SOLAR_MASS) -> None:
        
        if not object_name:
            raise RuntimeError("What is the name of the object ? Specify 'object_name'")
        if not object_mass:
            raise RuntimeError("Need to specify the object mass. (KG)")
        if not semi_major_axis:
            raise RuntimeError("Need the semi major axis (AU) to build the orbit.")
        if not eccentricity:
            raise RuntimeError("Need the eccentricity to build the orbit.")
        if not rotation_period:
            raise RuntimeError("Need the rotation period (day)")
        
        self._name = object_name
        self._semi_major_axis = semi_major_axis
        self._inclination = inclination
        self._eccentricity = eccentricity
        self._attraction_mass = attraction_mass
        self._mass = object_mass
        self._radius = object_radius
        self._rotation_period = rotation_period
        self._axis_inclination = axis_inclination
        self._semi_minor_axis = self.set_semi_minor_axis()
        self._orbital_period = self.set_orbital_period()
        self._orbital_circumference = self.set_orbital_circumference()
        self._perihelion_distance = self.set_perihelion_distance()
        self._perihelion_velocity = self.set_perihelion_velocity()
        self._aphelion_distance = self.set_aphelion_distance()
        self._aphelion_velocity = self.set_aphelion_velocity()
        

    def __repr__(self) -> str:
        return f"""
        ################
        {__class__.__name__} : {self._name}
        ################

        # ORBITAL CHARACTERISTICS
        semi major axis : {self._semi_major_axis} AU
        semi minor axis : {self._semi_minor_axis} AU
        inclination : {self._inclination}°
        eccentricity : {self._eccentricity}
        period : {self._orbital_period} days
        circumference : {self._orbital_circumference} m
        distance at perihelion : {self._perihelion_distance} AU
        velocity at perihelion : {self._perihelion_velocity} m/s
        distance at aphelion : {self._aphelion_distance} AU
        velocity at aphelion : {self._aphelion_velocity} m/s

        # PHYSICAL CHARACTERISTICS
        mass : {self._mass} kg
        rotation period : {self._rotation_period} d
        axis inclination : {self._axis_inclination}°
        radius : {self._radius} m
            """
    
    def get_name(self) ->str:
        return self._name
    
    def get_semi_major_axis(self) ->float:
        return self._semi_major_axis
    
    def get_inclination(self) ->float:
        return self._inclination
    
    def get_eccentricity(self) ->float:
        return self._eccentricity
    
    def get_axis_inclination(self) ->float:
        return self._axis_inclination
    
    def get_rotation_period(self) ->float:
        return self._rotation_period

    def get_radius(self) ->float:
        return self._radius
    
    def get_orbital_period(self) ->float:
        return self._orbital_period
    
    def set_orbital_period(self) ->float:
        """
        Calculates the time in days that it takes for a star to make a
        complete revolution around the Sun from its distance from the Sun.
        """
        # Using Kepler's law to calculate the orbital period (T)
        orbital_period = 2 * math.pi * math.sqrt((utils.convert_au_to_meters(self._semi_major_axis)**3) / (envs.G * self._attraction_mass))
        
        # Conversion to days
        return orbital_period / (60 * 60 * 24)

    def get_semi_minor_axis(self) ->float:
        return self._semi_minor_axis
    
    def set_semi_minor_axis(self) ->float:
        """Calculates the semi minor axis of an ellipse.

        Returns:
            float: The semi minor axis of the ellipse
        """
        return self._semi_major_axis * math.sqrt(1 - self._eccentricity ** 2)

    def get_perihelion_distance(self) ->float:
        return self._perihelion_distance
    
    def set_perihelion_distance(self) ->float:
        return self._semi_major_axis * (1 - self._eccentricity)

    def get_perihelion_velocity(self) ->float:
        return self._perihelion_velocity
    
    def set_perihelion_velocity(self) ->float:
        """Calculate the speed of an object at perihelion around the Sun

        Returns:
            float: The velocity in meters
        """
        return math.sqrt(envs.G * (self._attraction_mass + self._mass) * (2 / utils.convert_au_to_meters(self._perihelion_distance) - 1 / utils.convert_au_to_meters(self._semi_major_axis)))

    def get_aphelion_distance(self) ->float:
        return self._aphelion_distance
    
    def set_aphelion_distance(self) ->float:
        return self._semi_major_axis * (1 + self._eccentricity)
    
    def get_aphelion_velocity(self) ->float:
        return self._aphelion_velocity
    
    def set_aphelion_velocity(self) ->float:
        """Calculate the speed of an object at aphelion around the Sun

        Returns:
            float: The velocity in meters
        """
        return math.sqrt(envs.G * (self._attraction_mass + self._mass) * (2 / utils.convert_au_to_meters(self._aphelion_distance) - 1 / utils.convert_au_to_meters(self._semi_major_axis)))

    def get_orbital_circumference(self) ->float:
        return self._orbital_circumference
    
    def set_orbital_circumference(self) ->float:
        return 2 * math.pi * (self._semi_major_axis * envs.AU) # in meters
    
    def get_circumference_percentage(self, radius:float, time:int) ->float:
        # time in days
        # radius = perihelion distance at first

        # Kepler's law
        orbital_speed = (2 * math.pi * radius) / self._orbital_period

        # percentage of covered distance
        return self._orbital_circumference / 100 * (orbital_speed * time)
    
    def get_covered_distance_each_day(self) ->dict:
        """Based on the speed at perihelion and aphelion,
        calculate the percentage of circumference covered each day by the object.

        Returns:
            dict: Dictionary with percentage covered per day
        """
        d = self._perihelion_velocity * (24*3600) #perihelion v*t
        p_max = 100 * d / self._orbital_circumference

        d = self._aphelion_velocity * (24*3600) #aphelion v*t
        p_min = 100 * d / self._orbital_circumference

        percentage_covered_dist = {} 
        max_to_min_speed_range = range(0, int(self._orbital_period / 2))
        for key in max_to_min_speed_range:
            transition_value = p_max + (p_min - p_max) * (key - max_to_min_speed_range.start) / (max_to_min_speed_range.stop - 1)
            
            percentage_covered_dist[key] = transition_value

        min_to_max_speed_range = range(int(self._orbital_period / 2), int(self._orbital_period)+2)
        for key in min_to_max_speed_range:
            transition_value = p_min + (p_max - p_min) * (key - min_to_max_speed_range.start) / (min_to_max_speed_range.stop - 1)
            
            percentage_covered_dist[key] = transition_value

        return percentage_covered_dist
    
if __name__ == "__main__":
    # print(get_semi_minor_axis(30.0699, 0.00859))
    # print(get_orbital_period(convert_au_to_meters(0.38709808989279954)))

    def get_perihelion():
        inclinaison_degrees = 162.238  # Inclinaison de l'orbite en degrés
        longitude_du_noeud_ascendant_degrees = 58  # Longitude du nœud ascendant en degrés

        # Conversion des angles en radians
        inclinaison_radians = math.radians(inclinaison_degrees)
        longitude_du_noeud_ascendant_radians = math.radians(longitude_du_noeud_ascendant_degrees)

        # Calcul de l'argument du périhélie (ω) en radians
        argument_du_perihelie_radians = math.atan2(-math.cos(inclinaison_radians) * math.sin(longitude_du_noeud_ascendant_radians), math.cos(longitude_du_noeud_ascendant_radians))

        # Conversion de l'angle résultant en degrés
        argument_du_perihelie_degrees = math.degrees(argument_du_perihelie_radians)

        return argument_du_perihelie_degrees
    
    object_name = "Mercury"