

class _mockEventDAO:

    def __init__(self):
        '''
        Initialize mock collection for the EventDAO mock class.
        '''
        self.records = {
            "randomEVENT1": (
                "femenino",  # col 0 -> event date
                "true",  # col 1 -> is local value
                "#e30b0b",  # col 2 -> opponent color
                "UPR-RP",  # col 3 -> opponent name
                "Voleibol",  # col 4 -> sport name
                "Coliseo Rafael Mangual",  # col 5 -> venue
                "28-may-2020"  # col 6 -> date
            )
        }

    def getEventById(self, id):
        return self.records[id]
