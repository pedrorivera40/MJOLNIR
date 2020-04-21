#!/bin/bash

# mv test_1_add_new_user_route.py  test_1_add_new_user_route.py                
# mv test_2_add_existent_user.py  test_2_add_existent_user.py
# mv test_3_get_users_route.py  test_3_get_users_route.py
# mv test_4_activateUser_account.py  test_4_activateUser_account.py
# mv test_4_login.py  test_5_login.py
# mv test_5_lockout.py  test_6_lockout.py
# mv test_6_reset_invalid_password.py  test_7_reset_invalid_password.py
# mv test_7_reset_password_route.py  test_8_reset_password_route.py
# mv test_8_toggle_active_state_route.py  test_9_toggle_active_state_route.py
# mv test_9_add_get_user_permissions.py  test_10_add_get_user_permissions.py
# mv test_10_user_set_permissions.py      test_11_user_set_permissions.py      
# mv test_11_remove_user_route.py    test_12_remove_user_route.py              
# mv test_12_actions_on_removed_user.py    test_13_actions_on_removed_user.py  

echo "**********************************" >> tests/test_results.out 
echo "Running test_1_add_new_user_route" > tests/test_results.out  
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_1_add_new_user_route.py 2>> tests/test_results.out        
echo "**********************************" >> tests/test_results.out 
echo "Running test_2_add_existent_user" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_2_add_existent_user.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_3_get_users_route" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_3_get_users_route.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_4_activateUser_account" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_4_activateUser_account.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_5_login." >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_5_login.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_6_lockout" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_6_lockout.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_7_reset_invalid_password" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_7_reset_invalid_password.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_8_reset_password_route" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_8_reset_password_route.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_9_toggle_active_state_route" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_9_toggle_active_state_route.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_10_add_get_user_permissions" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_10_add_get_user_permissions.py 2>> tests/test_results.out
echo "**********************************" >> tests/test_results.out 
echo "Running test_11_user_set_permissions" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_11_user_set_permissions.py  2>> tests/test_results.out    
echo "**********************************" >> tests/test_results.out 
echo "Running test_12_remove_user_route" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_12_remove_user_route.py  2>> tests/test_results.out       
echo "**********************************" >> tests/test_results.out 
echo "Running test_13_actions_on_removed_user" >> tests/test_results.out 
echo "**********************************" >> tests/test_results.out 
python3 -m unittest tests/test_13_actions_on_removed_user.py  2>> tests/test_results.out 