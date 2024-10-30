from abc import ABC, abstractmethod


# Parent class
class BaseDBHandler(ABC):
    """
    Abstract base class for CRUD operations in the database
    """

    @abstractmethod
    def create_pbi(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_pbis(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_pbi(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_projects(self, *args, **kwargs):
        pass
