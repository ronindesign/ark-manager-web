import os
import csv
import uuid
from apps.file_manager import blueprint
from apps.file_manager.models import FileInfo
from flask import redirect, render_template, url_for, request
from apps.config import Config
from flask_login import current_user, login_required
from apps import db


def convert_csv_to_text(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    text = ''
    for row in rows:
        text += ','.join(row) + '\n'

    return text


def get_files_from_directory(directory_path):
  files = []
  for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
      try:
        print( ' > file_path ' + file_path)
        _, extension = os.path.splitext(filename)
        if extension.lower() == '.csv':
          csv_text = convert_csv_to_text(file_path)
        else:
          csv_text = ''

        files.append({
          'file': file_path.split(os.sep + 'media' + os.sep)[1],
          'filename': filename,
          'file_path': file_path,
          'csv_text': csv_text
        })
      except Exception as e:
        print( ' > ' +  str( e ) )    
  return files


@blueprint.route('/save-info/<file_path>', methods=['POST'])
def save_info(file_path):
  path = file_path.replace('%slash%', '/')
  if request.method == 'POST':
    file_info = FileInfo.find_by_path(path=path)
    if file_info:
        setattr(file_info, 'info', request.form.get('info'))
    else:
        file_info = FileInfo(path=path, info=request.form.get('info'))
        db.session.add(file_info)
    
    db.session.commit()
  
  return redirect(request.referrer)

def get_breadcrumbs(request):
  path_components = [component for component in request.path.split("/") if component]
  breadcrumbs = []
  url = ''

  for component in path_components:
    url += f'/{component}'
    if component == "file-manager":
      component = "media"
    breadcrumbs.append({'name': component, 'url': url})

  return breadcrumbs


@blueprint.route('/file-manager/<path:directory>')
@blueprint.route('/file-manager', defaults={'directory': ''})
@login_required
def file_manager(directory):
  user_id = str(current_user.id)
  media_path = os.path.join(Config.MEDIA_FOLDER, user_id)

  if not os.path.exists(media_path):
    os.makedirs(media_path)
    
  directories = generate_nested_directory(media_path, media_path, 1)
  selected_directory = directory

  files = []
  selected_directory_path = os.path.join(media_path, selected_directory)
  if os.path.isdir(selected_directory_path):
    files = get_files_from_directory(selected_directory_path)

  breadcrumbs = get_breadcrumbs(request)


  context = {
    'directories': directories, 
    'files': files, 
    'selected_directory': selected_directory,
    'segment': 'file_manager',
    'parent': 'apps',
    'breadcrumbs': breadcrumbs,
    'user_id': str(current_user.id),
  }
  return render_template('pages/pages/file-manager.html', **context)


def generate_nested_directory(root_path, current_path, base_depth=1):
    directories = []
    for name in os.listdir(current_path):
        if os.path.isdir(os.path.join(current_path, name)):
            depth = base_depth + 10
            unique_id = str(uuid.uuid4())
            nested_path = os.path.join(current_path, name)
            nested_directories = generate_nested_directory(root_path, nested_path, depth)
            directories.append({'id': unique_id, 'name': name, 'depth': str(depth), 'path': os.path.relpath(nested_path, root_path), 'directories': nested_directories})
    return directories


@blueprint.route('/delete-file/<file_path>')
def delete_file(file_path):
  path = file_path.replace('%slash%', '/')
  absolute_file_path = os.path.join(Config.MEDIA_FOLDER, path)
  os.remove(absolute_file_path)
  print("File deleted", absolute_file_path)
  return redirect(request.referrer)

from flask import send_file, abort

@blueprint.route('/download-file/<file_path>')
def download_file(file_path):
    path = file_path.replace('%slash%', '/')
    absolute_file_path = os.path.join(Config.MEDIA_FOLDER, path)
    if os.path.exists(absolute_file_path):
        return send_file(absolute_file_path, as_attachment=True)
    else:
        abort(404)

from werkzeug.utils import secure_filename
@blueprint.route('/upload-file', methods=['POST'])
def upload_file():
    media_path = os.path.join(Config.MEDIA_FOLDER)
    user_subdirectory = str(current_user.id)
    media_user_path = os.path.join(media_path, user_subdirectory)

    if not os.path.exists(media_user_path):
        os.makedirs(media_user_path)

    selected_directory = request.form.get('directory', '')
    selected_directory_path = os.path.join(media_user_path, selected_directory)

    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # Sanitize the file name
            filename = secure_filename(file.filename)
            file_path = os.path.join(selected_directory_path, filename)

            # Check if the file already exists
            if not os.path.exists(file_path):
                # Save the file
                with open(file_path, 'wb') as destination:
                    for chunk in file:
                        destination.write(chunk)

    return redirect(request.referrer)




@blueprint.app_template_filter('file_extension')
def file_extension(value):
  _, extension = os.path.splitext(value)
  return extension.lower()


@blueprint.app_template_filter('encoded_file_path')
def encoded_file_path(path):
  return path.replace('/', '%slash%')

@blueprint.app_template_filter('encoded_path')
def encoded_path(path):
  return path.replace('\\', '/')

@blueprint.app_template_filter('info_value')
def info_value(path):
    file_info = FileInfo.find_by_path(path=path)
    if file_info:
        return file_info.info
    else:
        return ""