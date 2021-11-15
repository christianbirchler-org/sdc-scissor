import json
import os
from pathlib import Path
from typing import List, Callable

from deeper.Deeper_test_generator.folders import folders


class FolderStorage:

    def __init__(self, path: Path, mask: str):
        self.mask = mask  # 'road{:03}_nodes.json'
        self.folder = path
        path.mkdir(parents=True, exist_ok=True)

    def all_files(self) -> List[str]:
        expanded = [os.path.join(self.folder, filename) for filename in os.listdir(self.folder)]
        return [path for path in expanded if os.path.isfile(path)]

    def get_path_by_index(self, index) -> Path:
        assert index > 0
        return self.folder.joinpath(self.mask.format(index))

    def load_json_by_index(self, index):
        path = self.get_path_by_index(index)
        nodes = self.load_json_by_path(path)
        return nodes

    def save_json_by_index(self, index, object_instance):
        path = self.get_path_by_index(index)
        dumps = self.save_json_by_path(path, object_instance)
        return dumps

    @staticmethod
    def load_json_by_path(path):
        assert os.path.exists(path), path
        with open(path, 'r') as f:
            nodes = json.loads(f.read())
        return nodes

    @staticmethod
    def save_json_by_path(path, object_instance):
        with open(path, 'w') as f:
            dumps = json.dumps(object_instance)
            f.write(dumps)
        return dumps

    def cache(self, road_name: str, get_points: Callable):
        path = os.path.join(self.folder, road_name + '.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                nodes = json.loads(f.read())
        else:
            nodes = get_points()
            with open(path, 'w') as f:
                f.write(json.dumps(nodes))
        return nodes

    def save(self, road_name: str, contents: str):
        path = os.path.join(self.folder, road_name + '.json')
        with open(path, 'w') as f:
            f.write(contents)

    @staticmethod
    def read(path):
        assert os.path.exists(path), path
        with open(path, 'r') as f:
            beamng_member = json.loads(f.read())
        return beamng_member


class SeedStorage(FolderStorage):
    def __init__(self, subfolder: str):
        super().__init__(folders.member_seeds.joinpath(subfolder), 'member_seeds{:04}.json')
