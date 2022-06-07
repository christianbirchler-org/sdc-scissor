from pymoo.model.duplicate import ElementwiseDuplicateElimination


class DuplicateElimination(ElementwiseDuplicateElimination):
    """
    Module to remove the same individuals
    """

    def is_equal(self, a, b):
        return a.X[0].states == b.X[0].states  # remove individuals that are the same
