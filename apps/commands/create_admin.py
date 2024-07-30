# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.config import Config
from apps import db
from apps.authentication.models import Users, Role
import getpass
import re



regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def validate_email(email):
    """ validate email  """
    if re.fullmatch(regex, email):
        return True
    else:
        return False


class CreateAdmin:
    """ create admin command  """

    def create_admin(test):
        """ create admin """
        if not test:
            while True:
                username = input("Username: ")
                if username.strip() == "":
                    print("\033[91mUsername cannot be empty\033[0m")
                elif Users.find_by_username(username):
                    print("\033[91mUsername already exists\033[0m")
                else:
                    break
            
            email = ""
            while True:
                email = input("Email: ")
                if email.strip() == "":
                    break
                elif not validate_email(email):
                    print("\033[91mInvalid email address\033[0m")
                elif Users.find_by_email(email):
                    print("\033[91mEmail address already exists\033[0m")
                else:
                    break
            
            while True:
                password = getpass.getpass("Password: ")
                if password.strip() == "":
                    print("\033[91mPassword cannot be empty\033[0m")
                else:
                    confirm_password = getpass.getpass("Re-type Password: ")
                    if confirm_password.strip() == "":
                        print("\033[91mConfirmation password cannot be empty\033[0m")
                    elif password != confirm_password:
                        print("\033[91mPasswords do not match\033[0m")
                    else:
                        break


            role = Role.ADMIN
            new_user = Users(username=username, email=email, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()

            print("Admin user created successfully")

        else:
            username = "admin"
            email = "admin@admin.com"
            password = "admin"

            if Users.find_by_username(username):
                print("\033[91mUsername already exists\033[0m")
                return
            if Users.find_by_email(email):
                print("\033[91mEmail address already exists\033[0m")
                return

            role = Role.ADMIN
            new_user = Users(username=username, email=email, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()

            print("Admin user created successfully")