import { postVolleyballResults } from './index';

// Define payload to be sent to the API.
const payload = <JSON><unknown>{
    "event_id": 78,
    "team_statistics":
    {
        "volleyball_statistics":
        {
            "kill_points": 1,
            "attack_errors": 1,
            "assists": 1,
            "aces": 1,
            "service_errors": 1,
            "digs": 1,
            "blocks": 1,
            "blocking_points": 1,
            "blocking_errors": 1,
            "reception_errors": 1
        }
    },
    "athlete_statistics":
        [
            {
                "athlete_id": 70,
                "statistics":
                {
                    "volleyball_statistics":
                    {
                        "kill_points": 1,
                        "attack_errors": 1,
                        "assists": 1,
                        "aces": 1,
                        "service_errors": 1,
                        "digs": 1,
                        "blocks": 1,
                        "blocking_points": 1,
                        "blocking_errors": 1,
                        "reception_errors": 1
                    }
                }
            },
            {
                "athlete_id": 71,
                "statistics":
                {
                    "volleyball_statistics":
                    {
                        "kill_points": 3,
                        "attack_errors": 3,
                        "assists": 3,
                        "aces": 3,
                        "service_errors": 3,
                        "digs": 3,
                        "blocks": 3,
                        "blocking_points": 1,
                        "blocking_errors": 3,
                        "reception_errors": 3
                    }
                }
            }
        ],
    "uprm_score": 500,
    "opponent_score": 200
};

postVolleyballResults(payload);