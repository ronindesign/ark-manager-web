# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ChangePasswordForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass
from apps.authentication.util import hash_pass

@blueprint.route('/')
def route_default():
    # return redirect(url_for('authentication_blueprint.login'))
    return redirect(url_for('home_blueprint.index'))

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/auth-signin.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/auth-signin.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/auth-signup.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/auth-signup.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/auth-signup.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/auth-signup.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('pages/403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('pages/403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('pages/404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('pages/500.html'), 500


@blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm(request.form)
    if 'change_password' in request.form:

        # read form data
        current_password = request.form['current_password']
        new_password1 = request.form['new_password1']
        new_password2 = request.form['new_password2']

        # Locate user
        user = Users.query.filter_by(username=current_user.username).first()

        # Check the password
        if user and verify_pass(current_password, user.password):

            if(new_password1 == new_password2):
                current_user.password = hash_pass(new_password1)
                db.session.commit()
                return redirect(url_for('authentication_blueprint.route_default'))
            else:
                return render_template('accounts/auth-change-password.html',
                                msg='Two password field does not match',
                                form=change_password_form)

        else:
            # Something (user or pass) is not ok
            return render_template('accounts/auth-change-password.html',
                                msg='Current password is not correct',
                                form=change_password_form)
    else:
        return render_template('accounts/auth-change-password.html', form=change_password_form)