from typing import Dict

from deeper.Deeper_test_generator.problem import Problem
from deeper.Deeper_test_generator.member import Member
from deeper.Deeper_test_generator.folder_storage import SeedStorage
from deeper.Deeper_test_generator.folders import folders
from deeper.Deeper_test_generator.seed_pool import SeedPool


class SeedPoolFolder(SeedPool):
    def __init__(self, problem: Problem, folder_name):
        super().__init__(problem)
        self.storage = SeedStorage(folder_name)
        self.file_path_list = self.storage.all_files()
        assert (len(self.file_path_list)) > 0
        self.cache: Dict[str, Member] = {}

    def __len__(self):
        return len(self.file_path_list)

    def __getitem__(self, item) -> Member:
        path = self.file_path_list[item]
        result: Member = self.cache.get(path, None)
        if not result:
            x = (self.storage.read(path)).get("m1")
            result = self.problem.member_class().from_dict(x)
            #result = self.problem.member_class().from_dict(self.storage.read(path))
            self.cache[path] = result
        result.problem = self.problem
        return result


class SeedPoolRandom(SeedPool):
    def __init__(self, problem, n):
        super().__init__(problem)
        self.n = n
        self.seeds = [problem.generate_random_member() for _ in range(self.n)]

    def __len__(self):
        return self.n

    def __getitem__(self, item):
        return self.seeds[item]


class SeedPoolMnist(SeedPool):
    def __init__(self, problem: Problem, filename):
        super().__init__(problem)
        content = folders.member_seeds.joinpath(filename).read_text()
        self.seeds_index = content.split(',')
        self.cache: Dict[str, Member] = {}

    def __len__(self):
        return len(self.seeds_index)

    def __getitem__(self, item) -> Member:
        mnist_index = self.seeds_index[item]
        result: Member = self.cache.get(mnist_index, None)
        if not result:
            # result = self.problem.member_class().from_dict(self.storage.read(path))
            raise NotImplementedError()
            self.cache[mnist_index] = result
        return result
