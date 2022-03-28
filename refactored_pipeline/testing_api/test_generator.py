from pathlib import Path

from refactored_pipeline.testing_api.frenetic.src.generators.random_frenet_generator import CustomFrenetGenerator


class TestGenerator:
    def __init__(self, count: int, destination: Path):
        self.count: int = count
        self.destination: Path = destination
        self.generated_tests: list[list] = []
        kwargs: dict = {
            'map_size': 200,
            'time_budget': 100,
            'count': count
        }
        self.random_frenet_generator = CustomFrenetGenerator(**kwargs)

    def generate(self):
        print('* generate')
        road_points = self.random_frenet_generator.start()
        self.generated_tests.extend(road_points)
        print('** {} tests generated'.format(len(road_points)))
        print('** test generator has {} tests'.format(len(self.generated_tests)))

    def save_tests(self):
        print('* save_tests')


if __name__ == '__main__':
    print('* test_generator.py')
