import math
from solar_system_cartography import envs, utils
class Star():
    def __init__(self, name:str, mass:str, parent:str=envs.ORIGIN, children:list=[]) -> None:
        self._name = name
        self._mass = mass
        self._type = "Star"
        self._parent = parent
        self._children = children

    def get_name(self) ->str:
        return self._name
    
    def get_parent(self) ->str:
        return self._parent
    
    def get_type(self) ->str:
        return self._type
    
    def get_mass(self) ->float:
        return self._mass
    
    def get_influences(self) ->list:
        influences = []
        for child in self._children:
            mass = child[3]
            influence = self.get_object_influence(mass)
            influences.append(influence)
        barycenter_influence = 1 - sum(influences)
        influences.insert(0, barycenter_influence)

        return influences
    
    def get_object_influence(self, object_mass) ->float:
        return float(object_mass) / float(self._mass) * 100
    
    def read(self) ->dict:
        return {
            envs.E_NAME : self.get_name(),
            envs.E_TYPE : self.get_type(),
            envs.E_PARENT : self.get_parent(),
            envs.E_MASS : self.get_mass()
        }

class ObjectInOrbit():
    def __init__(self, object_name:str, object_type:str, object_parent:str, object_mass:float, semi_major_axis:float,
                 inclination:float, eccentricity:float, rotation_period:float,
                 axis_inclination:float, ascending_node:float, arg_periapsis:float,
                 parent_mass:float, random_perihelion_day:list[int] = [2000,1,1]) -> None:
        
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
        self._type = object_type
        self._parent = object_parent
        self._mass = object_mass
        self._rotation_period = rotation_period
        self._axis_inclination = axis_inclination
        self._semi_major_axis = semi_major_axis
        self._inclination = inclination
        self._eccentricity = eccentricity
        self._parent_mass = parent_mass
        self._perihelion_day = random_perihelion_day
        self._arg_periapsis = arg_periapsis
        self._ascending_node = ascending_node
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
    
    def read(self) ->dict:
        return {
            envs.E_NAME : self.get_name(),
            envs.E_TYPE : self.get_type(),
            envs.E_PARENT : self.get_parent(),
            envs.E_MASS : self.get_mass(),
            envs.E_PERIOD : self.get_rotation_period(),
            envs.E_INCLINATION : self.get_axis_inclination(),
            envs.O_SEMI_MAJOR_AXIS : self.get_semi_major_axis(),
            envs.O_INCLINATION : self.get_inclination(),
            envs.O_ECCENTRICITY : self.get_eccentricity(),
            envs.O_ASCENDING_NODE : self.get_ascending_node(),
            envs.O_ARG_PERIAPSIS : self.get_arg_periapsis(),
            envs.O_PERIHELION_DAY : self.get_random_perihelion_day(),
            envs.O_SEMI_MINOR_AXIS : self.get_semi_minor_axis(),
            envs.O_PERIOD : self.get_orbital_period(),
            envs.O_CIRCUMFERENCE : self.get_orbital_circumference(),
            envs.O_PERIHELION_D : self.get_perihelion_distance(),
            envs.O_PERIHELION_V : self.get_perihelion_velocity(),
            envs.O_APHELION_D : self.get_aphelion_distance(),
            envs.O_APHELION_V : self.get_aphelion_velocity()
        }
    
    def get_name(self) ->str:
        return self._name
    
    def get_type(self) ->str:
        return self._type
    
    def get_parent(self) ->str:
        return self._parent

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
    
    def get_mass(self) ->float:
        return self._mass
    
    def get_orbital_period(self) ->float:
        return self._orbital_period
    
    def get_random_perihelion_day(self) ->list:
        return self._perihelion_day
    
    def get_arg_periapsis(self) ->float:
        return self._arg_periapsis
    
    def get_ascending_node(self) ->float:
        return self._ascending_node
    
    def set_orbital_period(self) ->float:
        """
        Calculates the time in days that it takes for an object to make a
        complete revolution around the Sun from its distance from the Sun.
        """
        # Using Kepler's law to calculate the orbital period (T)
        print("major axis", self._semi_major_axis)
        print("parent mass", self._parent_mass)
        orbital_period = 2 * math.pi * math.sqrt((utils.convert_au_to_meters(self._semi_major_axis)**3) / (envs.G * self._parent_mass))
        
        # Conversion to days
        return orbital_period / 86400

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
        return math.sqrt(envs.G * (self._parent_mass + self._mass) * (2 / utils.convert_au_to_meters(self._perihelion_distance) - 1 / utils.convert_au_to_meters(self._semi_major_axis)))

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
        return math.sqrt(envs.G * (self._parent_mass + self._mass) * (2 / utils.convert_au_to_meters(self._aphelion_distance) - 1 / utils.convert_au_to_meters(self._semi_major_axis)))

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
    
    def get_days(self) ->int:
        """Returns the number of days from J2000 to the specified perihelion date.
        """
        perihelion_day = self.get_random_perihelion_day()
        return utils.days_from_j2000(perihelion_day[0],
                                    perihelion_day[1],
                                    perihelion_day[2])
        
    def get_covered_distance_each_day(self) ->dict:
        def find_root(x, e, M):
            return x - e * math.sin(x) - M
        
        t,M,u,theta,R,X,Y = [],[],[],[],[],[],[]

        T_rev = self._orbital_period / 365 #orbital period (year)
        e = self._eccentricity
        a = self._semi_major_axis
        N = 80 # nb of keyposes

        # calculate the date at each N
        times_inc = []
        time_inc = T_rev / N
        for i in range(N-1):
            times_inc.append(time_inc*i)
        times_inc.append(T_rev)

        # Kepler
        # Find where is the object
        for i in range(N):
            t.append(i*time_inc)
            M.append(2*math.pi/T_rev *t[i])
            x = 0
            max_iterations = 1000  #l ambda number

            # Newton-Raphson method to find the root
            for _ in range(max_iterations):
                f_x = find_root(x, e, M[i])
                f_prime_x = 1 - e * math.cos(x)
                x = x - f_x / f_prime_x
            u.append(x)
        # polar coordinates
            theta.append(2*math.atan((math.sqrt((1+e)/ (1-e))*math.tan(u[i]/2))))
            R.append(a*(1-e**2)/(1+e*math.cos(theta[i]))) 
        # cartesian coordinates
            X.append(R[i]*math.cos(theta[i])) 
            Y.append(R[i]*math.sin(theta[i]))

        # t1,t2 = first area dates and t2, t3 = second aera dates
        t1,t2 = 0,2
        t3,t4 = 10,12
        # positions may change but space between dates must be the same

        AIRE1,AIRE2 = 0,0
        i1,i2 = 0,0 

        # calculation of swept area between t1 and t2
        Delta_t1 =t2-t1
        for i1 in range(Delta_t1):
            # calculate the length of triangle sides
            long1 = math.sqrt((X[t1+i1])**2+(Y[t1+i1])**2)
            long2 = math.sqrt((X[t2+i1])**2+(Y[t2+i1])**2)
            long3 = math.sqrt((X[t2+i1]-X[t1+i1])**2+(Y[t2+i1]-Y[t1+i1])**2) 
            # half perimeter
            S_1 = 1/2*(long1+long2+long3)
            # Heron formula
            AIRE1 = math.sqrt(S_1*(S_1-long1)*(S_1-long2)*(S_1-long3))+AIRE1
            
        # calculation of swept area between t3 and t4
        Delta_t2 =t4-t3

        for i2 in range(Delta_t2):
            # calculate the length of triangle sides
            long1b = math.sqrt((X[t3+i2])**2+(Y[t3+i2])**2)
            long2b = math.sqrt((X[t4+i2])**2+(Y[t4+i2])**2)
            long3b = math.sqrt((X[t4+i2]-X[t3+i2])**2+(Y[t4+i2]-Y[t3+i2])**2)
            #half perimeter
            S_1b = 1/2*(long1b+long2b+long3b)
            # Heron formula
            AIRE2 = math.sqrt(S_1b*(S_1b-long1b)*(S_1b-long2b)*(S_1b-long3b)) +AIRE2

        # Join points in tuple
        points = []
        for x,y in zip(X,Y):
            points.append((x,y))

        # distance between points
        def distance_between_points(point1, point2):
            x1, y1 = point1
            x2, y2 = point2
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        distances = []
        # distance between consecutive points
        for i in range(len(points) - 1):
            dist = distance_between_points(points[i], points[i + 1])
            distances.append(dist)

        # calculate percentage of distance done
        total = 0
        sum_distances = sum(distances)
        values = [0]
        for i, dist in enumerate(distances):
            cross_product = dist * 100 / sum_distances
            total += cross_product
            values.append(total)

        data = {}
        for time, value in zip(times_inc,values):
            data[time*365] = value
        
        return data
    
if __name__ == "__main__":
    pass