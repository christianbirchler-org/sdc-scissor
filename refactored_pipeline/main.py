import time

from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.sensors import Electrics


def main():
    print('* refactored pipeline')

    bng = BeamNGpy('localhost', 64256,
                   home=r'C:\Users\birc\Documents\BeamNG.tech.v0.24.0.2\BeamNG.drive-0.24.0.2.13392',
                   user=r'C:\Users\birc\Documents\BeamNG.drive')
    bng.open()
    scenario = Scenario('tig', 'example')

    road = Road(material='tig_road_rubber_sticky', rid='flat_road', interpolate=True)
    road_points = [(0, 0, -28, 10), (30, -30, -28, 10), (30, -100, -28, 10), (0, -200, -28, 10)]
    road.nodes.extend(road_points)
    # scenario.waypoints.extend(road_points[-1])

    scenario.add_road(road)

    vehicle = Vehicle(vid='ego_vehicle', model='etk800', licence='Scissor')
    electrics = Electrics()
    vehicle.attach_sensor('electrics', electrics)

    scenario.add_vehicle(vehicle, pos=(-2.5, 0, -28.0))

    scenario.make(bng)

    bng.load_scenario(scenario)
    bng.start_scenario()

    vehicle.ai_set_mode('span')
    vehicle.ai_drive_in_lane(lane=True)
    vehicle.ai_set_aggression(0.5)
    vehicle.set_color(rgba=(0, 0, 1, 0.5))
    vehicle.ai_set_speed(12)

    for _ in range(10):
        vehicle.update_vehicle()
        sensors = bng.poll_sensors(vehicle)

        pos = vehicle.state['pos']
        print('The vehicle position is: {}'.format(pos))

        direction = vehicle.state['dir']
        print('The vehicle direction is: {}'.format(direction))

        wheel_speed = sensors['electrics']['wheelspeed']
        print('The wheel speed is: {}'.format(wheel_speed))

        throttle = sensors['electrics']['throttle']
        print('The throttle intensity is: {}'.format(throttle))

        brake = sensors['electrics']['brake']
        print('The brake intensity is: {}'.format(brake))
        time.sleep(1)


if __name__ == '__main__':
    main()
    input('Hit enter...')
