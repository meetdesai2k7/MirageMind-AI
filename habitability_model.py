def habitability_score(temp, humidity, air_quality, pressure, light):

    score = 0

    if 15 <= temp <= 35:
        score += 30

    if 30 <= humidity <= 70:
        score += 20

    if air_quality > 70:
        score += 20

    if 900 <= pressure <= 1100:
        score += 15

    if light > 40:
        score += 15

    return score


planet_a = habitability_score(
    temp=90,
    humidity=0,
    air_quality=10,
    pressure=500,
    light=5
)

planet_b = habitability_score(
    temp=24,
    humidity=55,
    air_quality=90,
    pressure=1013,
    light=75
)

print("Planet A Habitability:", planet_a, "%")
print("Planet B Habitability:", planet_b, "%")