ga = {"population": 100, "n_gen": 75, "mut_rate": 0.4, "cross_rate": 1}

model = {
    "speed": 9,  # parameter for the simplified car model
    "map_size": 200,
    "steer_ang": 12,  # a parameter for the simplified car model
    "min_len": 5,  # minimal possible distance in meters
    "max_len": 30,  # maximal possible disance to go straight in meters
    "min_angle": 10,  # minimal angle of rotation in degrees
    "max_angle": 85,  # maximal angle of rotation in degrees
}

files = {"ga_archive": ".\\GA_archive\\", "tc_img": ".\\TC_img\\", "tc_file": ".\\TC_file\\"}
