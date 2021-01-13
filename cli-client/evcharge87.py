from agithub.base import API, ConnectionProperties, Client

class EvCharge(API):
    def __init__(self, token=None, *args, **kwargs):
        props = ConnectionProperties(
            api_url="localhost:8765/evcharge/api",
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)



def get_token():
	return ""

class CommandLineInterface():
	"""docstring for CommandLineInterface"""
	def __init__(self):
		self.client = EvCharge(token=get_token())

	def healthcheck(self):
		return self.client.healthcheck.get()

	def resetsessions(self):
		return self.client.resetsessions.post()


		
import fire	
		
	


if __name__=="__main__":
	fire.Fire(CommandLineInterface)