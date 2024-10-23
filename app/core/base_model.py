from abc import abstractmethod
from app.core.base_request import UserRequest

class Model:

	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	@abstractmethod
	def generate(self, data: UserRequest) -> str:
		pass


class TestModel(Model):

	def generate(self, data: UserRequest) -> str:
		return f"select 'This is a test for `{data.question}`' as answer"

