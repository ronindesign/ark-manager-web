import os
from apps.tasks import blueprint
from flask import render_template, request, redirect, url_for
from apps.home.models import TaskResult
from apps.config import Config

@blueprint.route('/run_script', methods=['POST'])
def run_script_route():
    from apps.tasks.tasks import run_script
    script_name = request.form['script']
    file_path = os.path.join(Config.CELERY_SCRIPTS_DIR, script_name)
    if os.path.isfile(file_path):
        run_script.delay(file_path)

    return redirect(url_for('tasks_blueprint.tasks'))


@blueprint.route('/tasks', methods=['GET', 'POST'])
def tasks():
    from apps.tasks.tasks import get_scripts
    scripts, ErrInfo = get_scripts()
    context = {
        'cfgError' : ErrInfo,
        'scripts'  : scripts,
        'tasks'	   : TaskResult.query.order_by(TaskResult.id.desc()).first(),
        'segment'  : 'tasks',
        'parent'   : 'apps',
    }
    task_results = TaskResult.query.all()
    context["task_results"] = task_results
    return render_template("pages/pages/tasks.html", **context)