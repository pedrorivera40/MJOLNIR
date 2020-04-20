#WHAT ARE WE GOING TO USE FOR TESTING? Team 1 is Basketball. Make a new event for it? 
# Team 25[1,8,4], event 32, 33 are valid. event 34 is invalid. Basketball(1), 2025.


class EventDAO:
    def getEventByID(self,eID):
        #   id  date            is_local|venue      team_id
        #   3	"2020-03-30"	true	"Mangual"	1
        #   4	"2020-03-14"	true	"Espada"	1
        valid_events = [3,4,5,6,7,8,9,10,11,12,13,14,15,21,22,23,24,25,26,27,32,33,35]

        if eID in valid_events:
            return 1
        return None

    def getEventTeamByID(self,eID):
        team1events =[3,4,5,6,21,22,23,25,26]
        team4events =[7,8]
        team5events =[]
        team7events =[10,11,12,15]
        team8events =[12,13,14]
        team14events = [24]
        team15events = [27,35]
        team25events =[32,33]
        if eID in team1events:
            return 1
        if eID in team4events:
            return 4
        if eID in team5events:
            return 5
        if eID in team7events:
            return 7
        if eID in team8events:
            return 8
        if eID in team14events:
            return 14
        if eID in team15events:
            return 15
        if eID in team25events:
            return 25

        else:
            return None

class TeamDAO:
    def getTeamSportByID(self,tID) :
        # Sport ID distribution
        # Team 1 is Basketball M (1)
        # Team 2 is Volleyball M (2)
        # Team 3 is Basketball F (10)
        # Teams 4 and 5 is Volleyball F (12)
        # Team 14 is Baseball M (4)
        # Team 25 is Basketball M (1)
        if tID == 1:
            return 1
        if tID == 2:
            return 2
        if tID == 3:
            return 10
        if tID == 4 or tID == 5:
            return 12
        if tID == 7 or tID == 15:
            return 11
        if tID == 8:
            return 16
        if tID == 14:
            return 4
        if tID == 25:
            return 1
        else:
            return None
        return
    def getTeamMemberByIDs(self,aID,tID):
        # Team 1 has Athletes 1,3,4,8
        # Team 25 has Athletes 1,8,4
        #returnable = dict(athlete_id = 8,team_id = 1)
        if tID == 1:
            if aID == 1 or aID == 3 or aID == 4 or aID == 8:
                return (aID,tID)
        if tID == 4 or tID == 5:
            if aID == 70 or aID == 71:
                return (aID,tID)
        if tID == 7:
            if aID == 73 or aID == 74:
                return (aID,tID)
        if tID == 8:
            if aID == 75 or aID == 76:
                return (aID,tID)
        if tID == 14:
            if aID == 104 or aID == 105:
                return (aID, tID)
        if tID == 15:
            if aID == 106 or aID == 107 or aID ==108:
                return (aID, tID)
        if tID == 25:
            if aID == 1 or aID == 8 or aID == 4:
                return (aID, tID)
        return None
            

class AthleteDAO:
    def getAthleteByID(self,aID):
        # Many Athletes in system, gonna only demo a few.
        valid_list = [1,3,4,5,7,8,9,10,11,12,13,15,16,70,71,72,73,74,75,76,104,105,106,107,108]
        if aID in valid_list:
            # We dont care about value here, just that it returns 
            # something to prove it exists
            return True
        return False
    def getAthleteSportByID(self,aID):
        basketball_athletes_m = [1,3,4,5,7,8,15,16]
        basketball_athletes_f = []
        volleyball_athletes_m = [68,69,72]
        volleyball_athletes_f = [70,71]
        baseball_athletes_m = [104,105]
        softball_athletes_f = []
        soccer_athletes_f = [73,74,106,107,108]
        if aID in basketball_athletes_m:
            return 1
        if aID in basketball_athletes_f:
            return 10
        if aID in volleyball_athletes_m:
            return 2
        if aID in volleyball_athletes_f:
            return 12
        if aID in baseball_athletes_m:
            return 4
        if aID in softball_athletes_f:
            return 16
        if aID in soccer_athletes_f:
            return 11

class SportDAO:
    def getSportById(self,sID):
        # Many Athletes in system, gonna only demo a few.
        valid_list = [18,16,17,13,14,15,7,1,2,12,10,5,3,11,4,9,8,6]
        if sID in valid_list:
            # We dont care about value here, just that it returns 
            # something to prove it exists
            return True
        return False
   
        
        
            