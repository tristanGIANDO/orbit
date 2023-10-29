from solar_system_cartography import envs
PRESETS = [
    (
        "Mercury",
        envs.T_PLANET,
        envs.ORIGIN,
        0.330e24,
        58.6458,
        0.03,
        0.38709808989279954,
        7.004,
        0.2056,
        48.33,
        29.12,
        [2000,11,24]
    )
]

OLD_PRESETS = {
    "Mercury" : {
        "semi_major_axis" : 0.38709808989279954,
        "inclination" : 7.004,
        "eccentricity" : 0.2056,
        "mass" : 0.330e24,
        "rotation_period" : 58.6458,
        "axis_inclination" : 0.03,
        "ascending_node" : 48.33,
        "arg_periapsis" : 29.12,
        "random_perihelion_day" : [2000,11,24]
    },
    "Venus" : {
        "semi_major_axis" : 0.723336,
        "inclination" : 3.39471,
        "eccentricity" : 0.00678,
        "mass" : 4.8675e24,
        "rotation_period" : -243.023,
        "axis_inclination" : 177.36,
        "ascending_node" :76.68,
        "arg_periapsis" : 54.9,
        "random_perihelion_day" : [2023,4,17]
    },
    "Earth" : {
        "semi_major_axis" : 1.0000001124,
        "inclination" : 0,
        "eccentricity" : 0.01671022,
        "mass" : 5.972e24,
        "rotation_period" : 0.99726949,
        "axis_inclination" : 23.4366907752,
        "ascending_node" :174.873,
        "arg_periapsis" : 288.064,
        "random_perihelion_day" :[2023,1,4]
    },
    "Mars" : {
        "semi_major_axis" : 1.52368055,
        "inclination" : 1.85,
        "eccentricity" : 0.09339,
        "mass" : 6.4185e23,
        "rotation_period" : 1.025957,
        "axis_inclination" : 25.19,
        "ascending_node" : 49.57854,
        "arg_periapsis" : 286.5,
        "random_perihelion_day" : [2022,6,21]
    },
    "Jupiter" : {
        "semi_major_axis" : 5.20289,
        "inclination" : 1.304,
        "eccentricity" : 0.04839,
        "mass" : 1.8986e27,
        "rotation_period" : 0.41351,
        "axis_inclination" : 3.12,
        "radius" : 69911000,
        "ascending_node" : 100.5,
        "arg_periapsis" : 274.255,
        "random_perihelion_day" : [2023,11,1]
    },
    "Saturn" : {
        "semi_major_axis" : 9.5367,
        "inclination" : 2.486,
        "eccentricity" : 0.0539,
        "mass" : 5.6846e26,
        "rotation_period" : 0.4,
        "axis_inclination" : 26.73,
        "ascending_node" : 113.7,
        "arg_periapsis" : 338.94,
        "random_perihelion_day" : [2003,6,20]
    },
    "Uranus" : {
        "semi_major_axis" : 19.19126393,
        "inclination" : 0.76986,
        "eccentricity" : 0.04716771,
        "mass" : 8.6811e25,
        "rotation_period" : -0.718,
        "axis_inclination" : 97.77,
        "ascending_node" : 74.22988,
        "arg_periapsis" : 96.9,
        "random_perihelion_day" : [2050,8,4]
    },
    "Neptune" : {
        "semi_major_axis" : 30.06896348,
        "inclination" : 1.76917,
        "eccentricity" : 0.00858587,
        "rotation_period" : 0.67125,
        "mass" : 102.409e24,
        "axis_inclination": 28.32,
        "ascending_node" : 131.72169,
        "arg_periapsis" : 273.2,
        "random_perihelion_day" : [1881,2,2]
    },
    "Pluto" : {
        "semi_major_axis" : 39.4450697,
        "inclination" : 17.0890009,
        "eccentricity" : 0.25024871,
        "rotation_period" :-6.387,
        "mass":1.314e22,
        "axis_inclination": 122.52,
        "ascending_node" : 110.376956,
        "arg_periapsis" : 112.5971417,
        "random_perihelion_day" : [1989,5,8]
    },
    "1P/Halley" : {
        "semi_major_axis" : 17.872265,
        "inclination" : 162.2239,
        "eccentricity" : 0.966321,
        "mass" : 2.2e14,
        "rotation_period" : 1,
        "axis_inclination" : 0,
        "random_perihelion_day" : [1986,2,9],
        "ascending_node" : 58.9763,
        "arg_periapsis" : 111.9047
    }
}