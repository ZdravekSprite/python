import socket
import time
import math
import random

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

BASE_WALKING_SPEED = 1.4  # m/s
INTERVAL = 3               # seconds between updates
PAUSE_PROBABILITY = 0.2    # chance to pause at a waypoint
PAUSE_DURATION_RANGE = (3, 8)  # seconds
ACC_DEC_DISTANCE = 3       # meters for acceleration/deceleration
CURVE_VARIATION = 0.00005  # lat/lon deviation for natural curves

# Example path
path = [
    (45.8150, 15.9819),
    (45.8155, 15.9790),
    (45.8160, 15.9760),
    (45.8170, 15.9730),
    (45.8180, 15.9700),
]

def distance_m(lat1, lon1, lat2, lon2):
    R = 6378137
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def move_towards(lat1, lon1, lat2, lon2, distance):
    total_dist = distance_m(lat1, lon1, lat2, lon2)
    if distance >= total_dist:
        return lat2, lon2
    ratio = distance / total_dist
    # Interpolate with a slight curve
    curve_lat = lat1 + (lat2 - lat1) * ratio + random.uniform(-CURVE_VARIATION, CURVE_VARIATION)
    curve_lon = lon1 + (lon2 - lon1) * ratio + random.uniform(-CURVE_VARIATION, CURVE_VARIATION)
    return curve_lat, curve_lon

def add_random_offset(lat, lon, max_offset_m=1.5):
    angle = random.uniform(0, 2 * math.pi)
    offset = random.uniform(0, max_offset_m)
    delta_lat = (offset * math.cos(angle)) / 6378137 * (180 / math.pi)
    delta_lon = (offset * math.sin(angle)) / (6378137 * math.cos(math.radians(lat))) * (180 / math.pi)
    return lat + delta_lat, lon + delta_lon

def get_speed(distance_to_waypoint):
    """Acceleration/deceleration with random speed variation"""
    if distance_to_waypoint < ACC_DEC_DISTANCE:
        speed = BASE_WALKING_SPEED * (distance_to_waypoint / ACC_DEC_DISTANCE)
    elif distance_to_waypoint > ACC_DEC_DISTANCE * 2:
        speed = BASE_WALKING_SPEED
    else:
        speed = BASE_WALKING_SPEED * ((ACC_DEC_DISTANCE * 2 - distance_to_waypoint) / ACC_DEC_DISTANCE)
    speed *= random.uniform(0.85, 1.15)
    return max(0.1, speed)

def simulate_realistic_walking():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server {SERVER_IP}:{SERVER_PORT}")

            current_index = 0
            lat, lon = path[current_index]

            while True:
                next_index = (current_index + 1) % len(path)
                lat_next, lon_next = path[next_index]
                distance_to_next = distance_m(lat, lon, lat_next, lon_next)

                # Random pause at waypoint
                if distance_to_next < 0.5 and random.random() < PAUSE_PROBABILITY:
                    pause_time = random.uniform(*PAUSE_DURATION_RANGE)
                    print(f"Pausing for {pause_time:.1f}s at waypoint {current_index}")
                    time.sleep(pause_time)

                # Calculate speed with acceleration/deceleration
                speed = get_speed(distance_to_next)

                # Move towards next waypoint along a curved path
                lat, lon = move_towards(lat, lon, lat_next, lon_next, speed * INTERVAL)

                # Add small GPS jitter
                lat, lon = add_random_offset(lat, lon)

                msg = f"{lat:.6f},{lon:.6f}"
                try:
                    s.sendall(msg.encode())
                    print(f"Sent: {msg} | Speed: {speed:.2f} m/s")
                except (BrokenPipeError, ConnectionResetError):
                    print("Connection lost. Exiting simulation.")
                    break

                # Advance to next waypoint if close enough
                if distance_m(lat, lon, lat_next, lon_next) < 0.5:
                    current_index = next_index

                time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except ConnectionRefusedError:
        print(f"Cannot connect to server {SERVER_IP}:{SERVER_PORT}")

if __name__ == "__main__":
    simulate_realistic_walking()
