import serial
import pygame
import math
import sys

# ================= SERIAL SETUP =================
SERIAL_PORT = 'COM3'  # Windows
# SERIAL_PORT = '/dev/ttyUSB0'  # Ubuntu/Linux

BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("ESP32 Connected")
except Exception as e:
    print("Could not connect to ESP32")
    print(e)
    sys.exit()

# ================= PYGAME SETUP =================
pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MirageMind AI")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT - 80

RADIUS = 300

# ================= COLORS =================
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# ================= VARIABLES =================
angle = 0
distance = 0

temperature = 0
humidity = 0

gas = 0
light = 0

life_score = 0
planet_status = "Unknown"

# ================= LIFE SCORE =================
def calculate_life_score(temp, hum, gas_val, light_val):

    score = 0

    # Temperature
    if 15 <= temp <= 35:
        score += 30

    # Humidity
    if 30 <= hum <= 70:
        score += 25

    # Gas
    if gas_val < 1500:
        score += 25

    # Light
    if light_val > 1000:
        score += 20

    return min(score, 100)

# ================= RADAR =================
def draw_radar():

    pygame.draw.circle(
        screen,
        GREEN,
        (CENTER_X, CENTER_Y),
        RADIUS,
        2
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (CENTER_X, CENTER_Y),
        225,
        1
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (CENTER_X, CENTER_Y),
        150,
        1
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (CENTER_X, CENTER_Y),
        75,
        1
    )

    pygame.draw.line(
        screen,
        GREEN,
        (CENTER_X - RADIUS, CENTER_Y),
        (CENTER_X + RADIUS, CENTER_Y),
        1
    )

    pygame.draw.line(
        screen,
        GREEN,
        (CENTER_X, CENTER_Y),
        (CENTER_X, CENTER_Y - RADIUS),
        1
    )

# ================= SCAN LINE =================
def draw_scan(a):

    rad = math.radians(a)

    x = CENTER_X + RADIUS * math.cos(rad)
    y = CENTER_Y - RADIUS * math.sin(rad)

    pygame.draw.line(
        screen,
        GREEN,
        (CENTER_X, CENTER_Y),
        (x, y),
        3
    )

# ================= OBJECT =================
def draw_object(a, d):

    if d <= 0 or d > 200:
        return

    mapped = (d / 200.0) * RADIUS

    rad = math.radians(a)

    x = CENTER_X + mapped * math.cos(rad)
    y = CENTER_Y - mapped * math.sin(rad)

    pygame.draw.circle(
        screen,
        RED,
        (int(x), int(y)),
        10
    )

# ================= MAIN LOOP =================
running = True

while running:

    screen.fill(BLACK)

    draw_radar()

    try:

        if ser.in_waiting:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            data = line.split(",")

            if len(data) == 6:

                angle = int(float(data[0]))
                distance = int(float(data[1]))

                temperature = float(data[2])
                humidity = float(data[3])

                gas = int(float(data[4]))
                light = int(float(data[5]))

                life_score = calculate_life_score(
                    temperature,
                    humidity,
                    gas,
                    light
                )

                if life_score >= 75:
                    planet_status = "Habitable"

                elif life_score >= 40:
                    planet_status = "Potentially Habitable"

                else:
                    planet_status = "Hostile"

    except Exception as e:
        print("Serial Error:", e)

    # Radar
    draw_scan(angle)
    draw_object(angle, distance)

    # ================= TEXT =================

    texts = [

        f"Angle : {angle}",
        f"Distance : {distance} cm",
        f"Temperature : {temperature:.1f} C",
        f"Humidity : {humidity:.1f} %",
        f"Gas Level : {gas}",
        f"Light Intensity : {light}",
        f"Life Possibility : {life_score} %",
        f"Planet Status : {planet_status}"

    ]

    y = 20

    for t in texts:

        txt = font.render(
            t,
            True,
            WHITE
        )

        screen.blit(txt, (20, y))

        y += 35

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

# ================= CLEANUP =================
ser.close()

pygame.quit()

sys.exit()