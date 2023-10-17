def convert_inclination(inclination):
    if inclination > 90:
        inclination = -(180 - inclination)
    
    return inclination

print(convert_inclination(91))