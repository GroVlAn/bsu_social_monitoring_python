from celery.result import AsyncResult
from celery.states import state, STARTED
from django.contrib.auth.models import User

from apps.celery_app.celery import app
from apps.monitoring.models_db.team import Team
from apps.vk_api_app.services.vk_api_service import thread_worker


def task_exits(task_id):
    result = AsyncResult(task_id, app=app)
    return result.state in ('PENDING', 'STARTED', 'RETRY')


@app.task
def start_get_data(body):
    task_id = str(body['user_id']) + body['user_name']
    result = AsyncResult(task_id)
    if not result.state < state(STARTED):
        return {'status': 'error', 'message': f'task by user {body["user_id"]} already exist'}

    user = User.objects.get(pk=body['user_id'])
    team = Team.objects.get(users=user)
    thread_worker(team)()
    result = AsyncResult(task_id)
    result.forget()

    return {'status': 'success', 'message': 'Data updated successfully'}
