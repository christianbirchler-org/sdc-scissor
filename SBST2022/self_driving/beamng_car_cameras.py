from beamngpy.sensors import Camera


class BeamNGCarCameras:
    def __init__(self, training=False):
        direction = (0, 1, 0)
        fov = 120
        resolution = (320, 160)
        y, z = 1.7, 1.0

        cam_center = 'cam_center', Camera((-0.3, y, z), direction, fov, resolution, colour=True)
        if training:
            cam_left = 'cam_left', Camera((-1.3, y, z), direction, fov, resolution, colour=True)
            cam_right = 'cam_right', Camera((0.4, y, z), direction, fov, resolution, colour=True)
            self.cameras_array = [cam_center, cam_left, cam_right]
        else:
            self.cameras_array = [cam_center]
