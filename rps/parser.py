from .model import RPS

class JankenParser:
	def __init__(self, choice):
		choice = choice.lower()

		if choice == RPS.BATU:
			self.choice = RPS.BATU
		elif choice == RPS.KERTAS:
			self.choice = RPS.KERTAS
		elif choice == RPS.GUNTING:
			self.choice = RPS.GUNTING
		else:
			raise 