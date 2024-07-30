# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import os
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/dashboard/')
# @login_required
def index():
    server_host = os.environ.get('WEBHOOK_SERVER_HOST')
    server_port = os.environ.get('WEBHOOK_SERVER_PORT')
    return render_template('pages/index.html', segment='dashboard', parent='Dashboard', server_host=server_host, server_port=server_port)

def get_segment( request ):
  try:
    segment = request.path.split('/')[-1]
    if segment == '':
      segment = 'index'
    return segment
  except:
    return None

# Custom Filter
@blueprint.app_template_filter('replace_value')
def replace_value(value, arg):
  return value.replace(arg, ' ').title()

@blueprint.app_template_filter('get_result_field')
def get_result_field(result, field: str):
    result = json.loads(result.result)
    if result:
        return result.get(field)

@blueprint.app_template_filter('date_format')
def date_format(date):
    try:
        return date.strftime(r'%Y-%m-%d %H:%M:%S')
    except:
        return date


@blueprint.app_template_filter('name_from_path')
def name_from_path(path):
    try:
        name = path.split('/')[-1]
        return name
    except:
        return path

@blueprint.app_template_filter('getattribute')
def getattribute(value, arg):
    try:
        return getattr(value, arg)
    except:
        return ''