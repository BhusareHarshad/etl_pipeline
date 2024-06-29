from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    model: str
    
    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...