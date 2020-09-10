"""views for BOINC monitor app ."""
import xml.etree.ElementTree as ET
from django.http import JsonResponse
from django.conf import settings
from boincrpc import BoincRpc, BoincRpcError


def task_status(request):
    """Get tasks status in JSON format."""
    try:
        boinc_rpc = BoincRpc(settings.BOINC_HOST,
                             settings.BOINC_PORT,
                             settings.BOINC_PASSWORD)
        xml = boinc_rpc.simple_request('get_state')
    except BoincRpcError as exception:
        print('Error:' + str(exception))
    root = ET.fromstring(xml)
    data = {}
    for project in root.iter('project'):
        url = project.find('master_url').text
        name = project.find('project_name').text
        data[url] = {'name': name, 'url': url, 'tasks': []}
    for task in root.iter('result'):
        url = task.find('project_url').text
        name = task.find('name').text
        state = task.find('state').text
        if state == '5': # Uploaded
            state = 'Uploaded'
            progress = '1'
        elif state == '2': # Downloaded
            state = 'Wait'
            progress = '0'
            active_task = task.find('active_task')
            if active_task is not None:
                state = 'Run'
                progress = active_task.find('fraction_done').text
        else:
            progress = 'Unknown'
            progress = '0'
        data[url]['tasks'].append({'name': name,
                                   'url': url,
                                   'state': state,
                                   'progress': progress})
    return JsonResponse(data)
