class EventDAO:
    def getEventByID(self,eID):
        #   id  date            is_local|venue      team_id
        #   3	"2020-03-30"	true	"Mangual"	1
        #   4	"2020-03-14"	true	"Espada"	1
        valid_events = [3,4,5,6,7,8,9,10,11,12,13,14,15]
        if eID in valid_events:
            return 1
        return None

    def getEventTeamByID(self,eID):
        team1events =[3,4,5,6]
        team4events =[7,8]
        team5events =[]
        team7events =[10,11,12,15]
        team8events =[12,13,14]
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

        else:
            return None

class TeamDAO:
    def getTeamSportByID(self,tID) :
        # Sport ID distribution
        # Team 1 is Basketball M (1)
        # Team 2 is Volleyball M (2)
        # Team 3 is Basketball F (10)
        # Teams 4 and 5 is Volleyball F (12)
        if tID == 1:
            return 1
        if tID == 2:
            return 2
        if tID == 3:
            return 10
        if tID == 4 or tID == 5:
            return 12
        if tID == 7:
            return 11
        if tID == 8:
            return 16
        else:
            return None
        return
    def getTeamMemberByIDs(self,aID,tID):
        # Team 1 has Athletes 1,3,4,8
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
        return None
            

class AthleteDAO:
    def getAthleteByID(self,aID):
        # Many Athletes in system, gonna only demo a few.
        valid_list = [1,3,4,5,7,8,9,10,11,12,13,15,16,70,71,72,73,74,75,76]
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
        if aID in basketball_athletes_m:
            return 1
        if aID in basketball_athletes_f:
            return 10
        if aID in volleyball_athletes_m:
            return 2
        if aID in volleyball_athletes_f:
            return 12
        
            