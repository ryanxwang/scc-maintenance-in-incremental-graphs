import scc_maintainer
from abc import abstractmethod, ABCMeta

class SCC_Maintainer(metaclass=ABCMeta):
    @property
    @abstractmethod
    def time(self):
        pass

    @time.setter
    @abstractmethod
    def time(self, t: int): 
        pass

    @abstractmethod
    def get_scc_count(self) -> int:
        pass

    @abstractmethod
    def add_vertex(self, id: int, birthday: int) -> None:
        pass

    @abstractmethod
    def add_edge(self, u: int, v: int, birthday: int) -> None:
        pass

    @abstractmethod
    def __init__(self):
        pass