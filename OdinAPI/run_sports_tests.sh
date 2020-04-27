#!/bin/bash

echo "RUNNING GET_SPORTS TESTS"
python3 -m unittest tests/sport_tests/test_get_sports.py

echo "RUNNING GET_SPORT_DETAILS TESTS"
python3 -m unittest tests/sport_tests/test_get_sport_details.py
