from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class BasketballEventDAO:

# getAllStatisticsByEventID(eID)//Return all statistics of a Basketball Event event.
# getAllAthleteStatisticsByEventId(eID,aID)//Returns all of an Athlete statistics of a Basketball Event for a given id.
# addStatistics(eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPe rcentage,threePointPercentage,freeThrowPercentage)//Adds a Basketball Event record in the database and returns the id of the inserted record.
# editStatistics(eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPe rcentage,threePointPercentage,freeThrowPercentage)//Edits a Basketball record in the database for a specific Athlete during an Event by the ids given and returns the updated record.
# removesStatistics(eID, aID)//Invalidates a Basketball Event record on a database and it returns the invalidated record.
# commitChanges()//Commits changes on the database after an insertion or update query.

#TODO: need to add not-invalid check to all the queries

    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)


    def getAllStatisticsByEventID(self,eID):
        cursor = self.conn.cursor()
        #TODO: Confirm that's the info we want from athlete...
        #TODO: verify if need to check the joined column's is_invalid (And all the foreign keys)
        query = """
                SELECT
                athlete.id as athlete_id, athlete.first_name, athlete.middle_name, athlete.last_names, 
                athlete.number, athlete.profile_image_link,
                points,rebounds,assists,steals,blocks,turnovers,field_goal_attempt,successful_field_goal,
                three_point_attempt,successful_three_point,free_throw_attempt,successful_free_throw,
                get_percentage(successful_field_goal,field_goal_attempt) as field_goal_percentage,
                get_percentage(successful_free_throw,free_throw_attempt) as free_throw_percentage,
                get_percentage(successful_three_point,three_point_attempt) as three_point_percentage
                FROM basketball_event
                INNER JOIN athlete ON athlete.id = basketball_event.athlete_id
                WHERE event_id = %s and 
                (basketball_event.is_invalid = false or basketball_event.is_invalid is null);
                """
        #TODO: need to avoid sql injections. the use of  %s and just a non-validated string is dangerous. 
        cursor.execute(query,(int(eID),))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result       
    
    def getAllAthleteStatisticsByEventID(self,eID,aID):
        cursor = self.conn.cursor()
        query = """
                SELECT
                points,rebounds,assists,steals,blocks,turnovers,field_goal_attempt,successful_field_goal,
                three_point_attempt,successful_three_point,free_throw_attempt,successful_free_throw,
                get_percentage(successful_field_goal,field_goal_attempt) as field_goal_percentage,
                get_percentage(successful_free_throw,free_throw_attempt) as free_throw_percentage,
                get_percentage(successful_three_point,three_point_attempt) as three_point_percentage
                FROM basketball_event
                WHERE event_id = %s and athlete_id = %s and 
                (basketball_event.is_invalid = false or basketball_event.is_invalid is null);
                """
        cursor.execute(query,(int(eID),int(aID),))
        result = cursor.fetchone()
        return result

    #NEW: given an event, get aggregate of team statistics
    def getAllTeamStatisticsByEventID(self,eID):
        cursor = self.conn.cursor()
        query = """
                SELECT
                points,rebounds,assists,steals,blocks,turnovers,field_goal_attempt,successful_field_goal,
                three_point_attempt,successful_three_point,free_throw_attempt,successful_free_throw,
                get_percentage(successful_field_goal,field_goal_attempt) as field_goal_percentage,
                get_percentage(successful_free_throw,free_throw_attempt) as free_throw_percentage,
                get_percentage(successful_three_point,three_point_attempt) as three_point_percentage
                FROM basketball_event_team_stats
                WHERE event_id = %s  and 
                (basketball_event_team_stats.is_invalid = false or basketball_event_team_stats.is_invalid is null);
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        return result

    #NEW : given team and athlete, return all statistics
    def getAllAthleteStatisticsPerSeason(self,aID,season_year):
        cursor = self.conn.cursor()
        query = """
                SELECT
                event.id as event_id, event.event_date,
                points,rebounds,assists,steals,blocks,turnovers,field_goal_attempt,successful_field_goal,
                three_point_attempt,successful_three_point,free_throw_attempt,successful_free_throw,
                get_percentage(successful_field_goal,field_goal_attempt) as field_goal_percentage,
                get_percentage(successful_free_throw,free_throw_attempt) as free_throw_percentage,
                get_percentage(successful_three_point,three_point_attempt) as three_point_percentage
                FROM basketball_event
                INNER JOIN event ON event.id = basketball_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE athlete_id = 8 and team.season_year = 2020 and
                (basketball_event.is_invalid = false or basketball_event.is_invalid is null);
                """
        cursor.execute(query,(int(aID),int(season_year),))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result  
    

    # Need to validate: event exists. athlete belongs to team  that is tied to the event. 
    # needless to say, a bunch changes since these are more complex statistics...
    # TODO: need to update documentation, substitute percentages for success/attempt.
    def addStatistics(self,eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalAttempt, 
    successfulFieldGoal,threePointAttempt,successfulThreePoint, freeThrowAttempt,successfulFreeThrow):
        cursor = self.conn.cursor()
        query = """
                INSERT INTO basketball_event(points,rebounds,assists,steals,blocks,turnovers,
                field_goal_attempt,successful_field_goal,three_point_attempt,successful_three_point,
                free_throw_attempt,successful_free_throw,event_id,athlete_id)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id;
                """
        cursor.execute(query,(int(points),int(rebounds),int(assists),int(steals),int(blocks),
        int(turnovers),int(fieldGoalAttempt),int(successfulFieldGoal),int(threePointAttempt),
        int(successfulThreePoint),int(freeThrowAttempt),int(successfulFreeThrow),int(eID),int(aID)))
        sID = cursor.fetchone()[0]
        if not sID:
            return sID
        self.commitChanges()
        return sID

    #NEW: add team statistics aggregate passed by parameter
    def addTeamStatistics(self,eID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalAttempt, 
    successfulFieldGoal,threePointAttempt,successfulThreePoint, freeThrowAttempt,successfulFreeThrow):
        cursor = self.conn.cursor()
        query = """
                INSERT INTO basketball_event_team_stats(points,rebounds,assists,steals,blocks,turnovers,
                field_goal_attempt,successful_field_goal,three_point_attempt,successful_three_point,
                free_throw_attempt,successful_free_throw,event_id)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id;
                """
        cursor.execute(query,(int(points),int(rebounds),int(assists),int(steals),int(blocks),
        int(turnovers),int(fieldGoalAttempt),int(successfulFieldGoal),int(threePointAttempt),
        int(successfulThreePoint),int(freeThrowAttempt),int(successfulFreeThrow),int(eID)))
        tsID = cursor.fetchone()[0]
        if not tsID:
            return tsID
        self.commitChanges()
        return tsID

    #NEW : aggregate statistics automatically and update
    def addTeamStatisticsAuto(self,eid):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,))
        aID = cursor.fetchone()[0]
        if not aID:
            return aID
        self.commitChanges()
        return aID

    def editStatistics(self,eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPercentage,threePointPercentage,freeThrowPercentage):
        #NEW: will also have to update the team statistics
        cursor = self.conn.cursor()
        query = """
                update basketball_event
                set first_name = %s,
                    middle_name = %s,
                    last_names = %s,
                    short_bio = %s,
                    height_inches = %s,
                    study_program = %s,
                    date_of_birth = %s,
                    school_of_precedence = %s,
                    number = %s,
                    profile_image_link = %s,
                    sport_id = %s
                where event = %s 
                returning first_name,
                    middle_name,
                    last_names,
                    short_bio,
                    height_inches,
                    study_program,
                    date_of_birth,
                    school_of_precedence,
                    number,
                    profile_image_link,
                    sport_id
                """
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aID,))
        result = cursor.fetchone()
        if not result:
            return result
        self.commitChanges()
        return result

    #NEW: edit team statistics. automatically update based on aggregate. 
    def updateTeamStatistics(self,eID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aID,))
        result = cursor.fetchone()
        if not result:
            return result
        self.commitChanges()
        return result
                
    
    def removeStatistics(self,eID,aID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
        self.commitChanges()
        return result

    #NEW : remove team statistics
    def removeTeamStatistics(self,eID,aID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
        self.commitChanges()
        return result

    def commitChanges(self):
        self.conn.commit()


