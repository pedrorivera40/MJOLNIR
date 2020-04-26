data = {
    "valid_notification": {
        "event_id": 28,
        "data": {
            "action_type": "Notification",
            "message": "This is a test notification. Hopefully it works."
        }
    },
    "non_existing_event_notification": {
        "event_id": 99999,
        "data": {
            "action_type": "Notification",
            "message": "This is a test notification. Hopefully it works."
        }
    },
    "non_valid_id_notification": {
        "event_id": "INVALID_EVENT",
        "data": {
            "action_type": "Notification",
            "message": "This is a test notification. Hopefully it works."
        }
    },
    "more_params_notification": {
        "event_id": 28,
        "data": {
            "action_type": "Notification",
            "message": "This is a test notification. Hopefully it works.",
            "other": "UNNECESSARY_CONTENT"
        }
    },
    "message_limit_notification": {
        "event_id": 28,
        "data": {
            "action_type": "Notification",
            "message": '''This is a test notification. Hopefully it works. 
                            This is a test notification. Hopefully it works. 
                            This is a test notification. Hopefully it works. 
                            This is a test notification. Hopefully it works. 
                            This is a test notification. Hopefully it works.
                        '''
        }
    },
    "valid_scoring_uprm": {
        "event_id": 28,
        "data": {
            "action_type": "KillPoint",
            "team": "uprm",
            "athlete_id": 110
        }
    },
    "valid_scoring_opp": {
        "event_id": 28,
        "data": {
            "action_type": "KillPoint",
            "team": "opponent",
            "athlete_id": 1587365468141
        }
    },
    "valid_personal_uprm": {
        "event_id": 28,
        "data": {
            "action_type": "Assist",
            "team": "uprm",
            "athlete_id": 110
        }
    },
    "valid_personal_opp": {
        "event_id": 28,
        "data": {
            "action_type": "Assist",
            "team": "opponent",
            "athlete_id": 1587365468141
        }
    },
    "valid_error_uprm": {
        "event_id": 28,
        "data": {
            "action_type": "AttackError",
            "team": "uprm",
            "athlete_id": 110
        }
    },
    "valid_error_opp": {
        "event_id": 28,
        "data": {
            "action_type": "AttackError",
            "team": "opponent",
            "athlete_id": 1587365468141
        }
    },
    "more_params_play": {
        "event_id": 28,
        "data": {
            "action_type": "AttackError",
            "team": "opponent",
            "athlete_id": 1587365468141,
            "SOMETHING": "YEP SOMETHING...."
        }
    },
    "invalid_action_play": {
        "event_id": 28,
        "data": {
            "action_type": "SOMETHING",
            "team": "opponent",
            "athlete_id": 1587365468141,
        }
    },

    "valid_adjust": {
        "event_id": 28,
        "data": {
            "action_type": "ScoreAdjust",
            "team": "opponent",
            "difference": 5,
        }
    },
    "content_to_valid_edit": {
        "path": "v1/28/game-actions/25",
        "data": {
            "action_type": "Notification",
            "message": "This is a test notification. Hopefully it works."
        }
    },
    "valid_to_remove": {
        "event_id": 28,
        "action_id": 25
    },
    "invalid_pbp_to_remove1": {
        "event_id": 9999,
        "action_id": 25
    },
    "invalid_pbp_to_remove2": {
        "event_id": 28,
        "action_id": 9999
    },
    "edit_valid_notification": {
        "event_id": 28,
        "action_id": 25,
        "data": {
            "action_type": "Notification",
            "message": "I refuse to sleep..."
        }
    },
    "path_to_score_to_error": "v1/28/game-actions/26",
    "score_to_be_changed1": {
        "event_id": 28,
        "action_id": 26,
        "data": {
            "action_type": "KillPoint",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_score_to_error_uprm": {
        "event_id": 28,
        "action_id": 26,
        "data": {
            "action_type": "AttackError",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_score_to_error_opp": {
        "event_id": 28,
        "action_id": 26,
        "data": {
            "action_type": "AttackError",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "path_to_score_to_score": "v1/28/game-actions/27",
    "score_to_be_changed2": {
        "event_id": 28,
        "action_id": 27,
        "data": {
            "action_type": "KillPoint",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_score_to_score_uprm": {
        "event_id": 28,
        "action_id": 27,
        "data": {
            "action_type": "Ace",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_score_to_score_opp": {
        "event_id": 28,
        "action_id": 27,
        "data": {
            "action_type": "Ace",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "path_to_personal_to_personal": "v1/28/game-actions/28",
    "personal_to_be_changed2": {
        "event_id": 28,
        "action_id": 28,
        "data": {
            "action_type": "Assist",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_personal_to_personal_uprm": {
        "event_id": 28,
        "action_id": 28,
        "data": {
            "action_type": "Block",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_personal_to_personal_opp": {
        "event_id": 28,
        "action_id": 28,
        "data": {
            "action_type": "Block",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "path_to_error_to_error": "v1/28/game-actions/29",
    "error_to_be_changed2": {
        "event_id": 28,
        "action_id": 29,
        "data": {
            "action_type": "AttackError",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_error_to_error_uprm": {
        "event_id": 28,
        "action_id": 29,
        "data": {
            "action_type": "BlockingError",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_error_to_error_opp": {
        "event_id": 28,
        "action_id": 29,
        "data": {
            "action_type": "BlockingError",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "path_to_error_to_score": "v1/28/game-actions/30",
    "error_to_be_changed3": {
        "event_id": 28,
        "action_id": 30,
        "data": {
            "action_type": "AttackError",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_error_to_score_uprm": {
        "event_id": 28,
        "action_id": 30,
        "data": {
            "action_type": "Ace",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_error_to_score_opp": {
        "event_id": 28,
        "action_id": 30,
        "data": {
            "action_type": "Ace",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "path_to_error_to_personal": "v1/28/game-actions/31",
    "error_to_be_changed3": {
        "event_id": 28,
        "action_id": 31,
        "data": {
            "action_type": "AttackError",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_error_to_personal_uprm": {
        "event_id": 28,
        "action_id": 31,
        "data": {
            "action_type": "Assist",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_error_to_personal_opp": {
        "event_id": 28,
        "action_id": 31,
        "data": {
            "action_type": "Assist",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "path_to_personal_to_error": "v1/28/game-actions/32",
    "personal_to_be_changed3": {
        "event_id": 28,
        "action_id": 32,
        "data": {
            "action_type": "Assist",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_personal_to_error_uprm": {
        "event_id": 28,
        "action_id": 32,
        "data": {
            "action_type": "ReceptionError",
            "athlete_id": 111,
            "team": "uprm"
        }
    },
    "edit_valid_personal_to_error_opp": {
        "event_id": 28,
        "action_id": 32,
        "data": {
            "action_type": "ReceptionError",
            "athlete_id": 1587365468141,
            "team": "opponent"
        }
    },
    "edit_invalid_notification1": {
        "event_id": 9999999,
        "action_id": 32,
        "data": {
            "action_type": "Notification",
            "message": "Hopefully this one doesn't work.",
        }
    },
    "edit_invalid_notification2": {
        "event_id": 28,
        "action_id": 9999999,
        "data": {
            "action_type": "Notification",
            "message": "Hopefully this one doesn't work either.",
        }
    },
}
