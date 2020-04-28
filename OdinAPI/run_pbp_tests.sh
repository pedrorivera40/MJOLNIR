#!/bin/bash

echo "RUNNING ADJUST_SET TESTS"
python3 -m unittest tests/pbp_tests/adjust_set/test_adjust_set.py

echo "RUNNING GAME_ACTIONS TESTS"
python3 -m unittest tests/pbp_tests/game_actions/test_add_game_actions_valid.py
python3 -m unittest tests/pbp_tests/game_actions/test_add_game_actions_invalid.py
python3 -m unittest tests/pbp_tests/game_actions/test_edit_game_actions_valid.py
python3 -m unittest tests/pbp_tests/game_actions/test_edit_game_actions_invalid.py
python3 -m unittest tests/pbp_tests/game_actions/test_remove_game_actions_valid.py
python3 -m unittest tests/pbp_tests/game_actions/test_remove_game_actions_invalid.py

echo "RUNNING OPP_ROSTER TESTS"
python3 -m unittest tests/pbp_tests/opp_roster/test_opp_roster_add_invalid.py
python3 -m unittest tests/pbp_tests/opp_roster/test_opp_roster_add_valid.py
python3 -m unittest tests/pbp_tests/opp_roster/test_opp_roster_remove_invalid.py
python3 -m unittest tests/pbp_tests/opp_roster/test_opp_roster_remove_valid.py

echo "RUNNING UPRM_ROSTER TESTS"
python3 -m unittest tests/pbp_tests/uprm_roster/test_uprm_roster_add_invalid.py
python3 -m unittest tests/pbp_tests/uprm_roster/test_uprm_roster_add_valid.py
python3 -m unittest tests/pbp_tests/uprm_roster/test_uprm_roster_remove_invalid.py
python3 -m unittest tests/pbp_tests/uprm_roster/test_uprm_roster_remove_valid.py

echo "RUNNING CREATE_PBP TESTS"
python3 -m unittest tests/pbp_tests/test_create_pbp_existing_pbp.py
python3 -m unittest tests/pbp_tests/test_create_pbp_invalid_id.py
python3 -m unittest tests/pbp_tests/test_create_pbp_non_existing_event.py
python3 -m unittest tests/pbp_tests/test_create_pbp_other_sport.py
python3 -m unittest tests/pbp_tests/test_create_pbp_valid.py

echo "RUNNING END_PBP TESTS"
python3 -m unittest tests/pbp_tests/test_end_pbp_valid.py
python3 -m unittest tests/pbp_tests/test_end_pbp_invalid.py
python3 -m unittest tests/pbp_tests/test_end_pbp_non_existing.py
python3 -m unittest tests/pbp_tests/test_end_pbp_valid_already_over.py


echo "RUNNING REMOVE_PBP TESTS"
python3 -m unittest tests/pbp_tests/test_remove_pbp_invalid.py
python3 -m unittest tests/pbp_tests/test_remove_pbp_non_existing_pbp.py
python3 -m unittest tests/pbp_tests/test_remove_pbp_valid.py

echo "RUNNING SET_COLOR TESTS"
python3 -m unittest tests/pbp_tests/test_set_color.py