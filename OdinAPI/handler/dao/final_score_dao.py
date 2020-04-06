from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class FinalScoreDAO:

    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)

    #NEW get the final score table detal
    def getFinalScore(self,eID):
        """
        Gets the final score for a given event. 

        This function uses an ID to perform a query to the database
        that gets the final score in the system that match the given ID.

        Args:
            eID: The ID of the event of final score need to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing athe final score in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT local_score, opponent_score, opponent_name, opponent_color, 
                event_id, id as final_score_id
                FROM final_score
                WHERE event_id = %s and 
                (is_invalid = false or is_invalid is Null)
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        return result

    def getFinalScoreInvalid(self,eID):
        """
        Gets the invalid final score for a given event. 

        This function uses an ID to perform a query to the database
        that gets the invalid final score in the system that match the given ID.

        Args:
            eID: The ID of the event of final score need to be fetched.
            
        Returns:
           The id of the invalid event, if it exists. 
        """
        cursor = self.conn.cursor()
        query = """
                SELECT local_score, opponent_score, opponent_name, opponent_color, 
                event_id, id as final_score_id
                FROM final_score
                WHERE event_id = %s and 
                (is_invalid = true)
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        return result

    #NEW: add final score
    def addFinalScore(self,eID, local_score, opponent_score, opponent_name, opponent_color):
        """
        Adds a new sports-specific event final score with the provided information.

        This function accepts an ID and score information 
        to perform a query to the database that adds a final score record 
        to the system with the provided information.

        Args:
            eID: the ID of the event for which the final score record will be added.
            local_score: the final score of the local team for the event
            opponent_score: the final score of the opponent team for the event
            opponent_name: name of the opponent team
            opponent_color: color to be used for opponent team
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new final record entry. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO final_score(local_score,opponent_score,event_id,is_invalid,
                opponent_name, opponent_color)
                VALUES(%s,%s,%s,false,%s,%s) returning id;
                """
        cursor.execute(query,(int(local_score),int(opponent_score),int(eID),str(opponent_name),str(opponent_color),))
        fsID = cursor.fetchone()[0]
        if not fsID:
            return fsID
        #self.commitChanges()
        return fsID

    #NEW: edit final score for an event 
    def editFinalScore(self,eID, local_score, opponent_score,opponent_name, opponent_color):
        """
        Updates the final score for the sports-specific event with the given IDs.

        This function accepts an ID and the updated scores and uses them to update
        the final score entry of an event in the system

        Args:
            eID: the ID of the event for which the final score record will be updated
            local_score: the local score to be updated
            opponent_score: the opponent score to be updated
            opponent_name: name of the opponent team
            opponent_color: color to be used for opponent team
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified sports-specific
            event final score.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE final_score
                SET local_score = %s,
                    opponent_score = %s,
                    opponent_name = %s,
                    opponent_color = %s,
                    is_invalid = false
                WHERE event_id = %s 
                RETURNING
                    local_score,
                    opponent_score,
                    opponent_name,
                    opponent_color, 
                    event_id, 
                    id as final_score_id;
                """
        cursor.execute(query,(int(local_score),int(opponent_score),str(opponent_name),str(opponent_color),int(eID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW : remove final score
    def removeFinalScore(self,eID):
        """
        Invalidates a sports-specific event final score entry in the database.

        This function accepts an ID and uses it to set the valid field
        within the database as invalid, this acts as a deletion of the 
        final score entry from the system.

        Args:
            eID: The ID of the event for which the final score will be invalidated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified 
            final score entry.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE final_score
                SET is_invalid = true
                WHERE event_id = %s
                RETURNING id;
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    def commitChanges(self):
        self.conn.commit()