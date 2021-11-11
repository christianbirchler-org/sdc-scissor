# this classes are here in the belief that it is needed to have on a drive folder files a representation of the
# individual this representation is different from saving/loading a member. This folder structure is aimed to
# give the highest information to the human inspecting the individual
# ------------ o --------------- o ----------------
# it is advisable that the folder structure is hidden externally to this file source code
# this is in the aim to access the individuals information through save (and load)
# so, if the folder structure changes, the only source code affected should be in this file source code

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from deeper.Deeper_test_generator.archive import IndividualSet
from deeper.Deeper_test_generator.folders import folders
from deeper.Deeper_test_generator.beamng_individual import BeamNGIndividual
from deeper.Deeper_test_generator.beamng_member import BeamNGMember
from self_driving.beamng_road_imagery import BeamNGRoadImagery
from self_driving.road_points import RoadPoints


class BeamNGIndividualSetStore:
    def __init__(self, folder: Path):
        self.folder = folder

    def save(self, individuals: IndividualSet):
        for ind in individuals:
            _BeamNGIndividualCompositeMembersStore(self.folder).save(ind)
            # _BeamNGIndividualSimpleStore(self.folder).save(ind)


class _BeamNGIndividualStore:
    def save(self, ind: BeamNGIndividual, prefix: str = None):
        raise NotImplementedError()

    def load(self, prefix: str) -> BeamNGIndividual:
        raise NotImplementedError()


class _BeamNGIndividualCompositeMembersStore:
    def __init__(self, folder: Path):
        self.folder = folder

    def save(self, ind: BeamNGIndividual, prefix: str = None):
        if not prefix:
            prefix = ind.name

        self.folder.mkdir(parents=True, exist_ok=True)
        ind_path = self.folder.joinpath(prefix + '.json')
        ind_path.write_text(json.dumps(ind.to_dict()))

        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10)
        ml = ind.members_by_distance_to_boundary()

        def plot(member: BeamNGMember, ax):
            ax.set_title(f'dist to bound', fontsize=12)
            road_points = RoadPoints.from_nodes(member.sample_nodes)
            road_points.plot_on_ax(ax)

        plot(ml, ax)
        #plot(mr, right)
        #fig.suptitle(f'members distance = {ind.members_distance} ; oob_ff = {ind.oob_ff}')
        fig.savefig(self.folder.joinpath(prefix + '_both_roads.svg'))
        plt.close(fig)

    def load(self, prefix: str) -> BeamNGIndividual:
        ind_path = self.folder.joinpath(prefix + '.json')
        ind = BeamNGIndividual.from_dict(json.loads(ind_path.read_text()))
        return ind


if __name__ == '__main__':
    store = _BeamNGIndividualCompositeMembersStore(folders.experiments.joinpath('exp1/gen0/population'))
    ind = store.load('ind1')
    store.save(ind, 'ind_xx')


class _BeamNGIndividualSimpleStore:
    def __init__(self, folder: Path):
        self.folder = folder

    def save(self, ind: BeamNGIndividual, prefix=None):
        if not prefix:
            prefix = ind.name

        self.folder.mkdir(parents=True, exist_ok=True)

        def save_road_img(member: BeamNGMember, name):
            filepath = self.folder.joinpath(name)
            # BeamNGRoadImagery.from_sample_nodes(member.sample_nodes).save(filepath.with_suffix('.jpg'))
            BeamNGRoadImagery.from_sample_nodes(member.sample_nodes).save(filepath.with_suffix('.svg'))

        ind_path = self.folder.joinpath(prefix + '.json')
        ind_path.write_text(json.dumps(ind.to_dict()))
        save_road_img(ind.m1, ind.name + '_m1_road')
        save_road_img(ind.m2, ind.name + '_m2_road')
