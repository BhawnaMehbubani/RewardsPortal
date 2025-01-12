import requests
import os
import datetime
import json
from flask import session, Flask, jsonify, render_template


class RewardsPortalDB:
    def __init__(self, db_file='rewards_portal_db.json'):
        self.base_url = 'http://localhost:3000'  # Replace with your server URL
        self.db_file = db_file

    def get_all_users(self):
        response = requests.get(f'{self.base_url}/users')
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            return data.get('users', [])

    def add_user(self, user_data):
        current_day = datetime.datetime.utcnow().date().isoformat()
        photo_dir = os.path.join('static', 'photos')
        user_details = {
            "first_name": user_data['user_details']['first_name'],
            "middle_name": user_data['user_details']['middle_name'],
            "last_name": user_data['user_details']['last_name'],
            "email_address": user_data['user_details']['email_address'],
            "phone_number": user_data['user_details']['phone_number'],
            "photo": user_data['user_details']['photo']
        }
        new_user = {
            "user_id": len(self.get_all_users()) + 1,
            "username": user_data['username'],
            "password": user_data['password'],
            "user_details": user_details,
            "reward_points": 0,
            "signup_details": {
                "signup_date": current_day,
                "active_session": True
            },
            "login_details": {
                "last_login_date": None,
                "current_login_date": current_day
            }
        }
        data = self.get_all_users()
        data.append(new_user)
        updated_data = {'users': data}
        requests.put(f'{self.base_url}/users', json=updated_data)
        return new_user

    def find_user(self, username, password):
        users = self.get_all_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return user
        return None

    def user_exists(self, username):
        users = self.get_all_users()
        for user in users:
            if user['username'] == username:
                return True
        return False

    def set_active_session(self, username, status=True):
        session['active_user'] = username
        session['active_session'] = status

    def check_active_session(self):
        return session.get('active_session', False)

    def get_user_details(self, username):
        # username = session.get('active_user')
        if username:
            users = self.get_all_users()
            for user in users:
                if user['username'] == username:
                    return user['user_details']
        return None

    # def update_personal_details(self, username, updated_details):
    #     users = self.get_all_users()
    #     for user in users:
    #         if user['username'] == username:
    #             user['user_details'].update(updated_details)
    #         if 'photo' in updated_details:
    #             user['user_details']['photo'] = updated_details['photo']
    #         break

    #     updated_data = {'users': users}
    def update_personal_details(self, username, updated_details):
        url = f'{self.base_url}/users'
        users = self.get_all_users()
        for user in users:
            if user['username'] == username:
                user_details = user['user_details']
                # Update the user details
                user_details.update(updated_details)
                # Update the data on the server
                updated_data = {'users': users}
                requests.put(url, json=updated_data)
                return True  # Indicate successful update
        return False  # Indicate failure (user not found)
