from datetime import datetime

class Business:
    def __init__(self, name, service, city, state):
        self.name = name
        self.service = service
        self.city = city
        self.state = state
        self.dateAdded = str(datetime.now())