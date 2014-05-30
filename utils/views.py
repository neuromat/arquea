# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.conf import settings
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
import os
import datetime
import logging
import magic
import urllib
from membro.models import Membro

# Get an instance of a logger
logger = logging.getLogger(__name__)


def verifica(request):
    return HttpResponse('Ok')

@login_required
def uso_admin(request):
    if 'inicial' not in request.GET:
        return TemplateResponse(request, 'admin/logs_escolha.html', {'anos':range(2008, datetime.datetime.now().year+1)})

    inicial = request.GET.get('inicial')
    final = request.GET.get('final')
    try:
        inicial = int(inicial)
        final = int(final)
    except:
        raise Http404
        
    user_ids = LogEntry.objects.filter(action_time__range=(datetime.date(inicial,1,1), datetime.date(final+1,1,1))).values_list('user', flat=True).order_by('user').distinct()
    emails = Membro.objects.values_list('email', flat=True).order_by('email').distinct()
    emails = list(emails)
    if '' in emails: emails.remove('')
    user_ids = list(user_ids)
    users = []
    for u in user_ids:
        user = User.objects.get(id=u)
        if user.email in emails: users.append(user)
        
    users.sort(key=lambda x: x.first_name)
        
    returned = []

    sem_abuse = LogEntry.objects.exclude(content_type_id=166)
    for user in users:
        log_user = sem_abuse.filter(user=user)
        user_return = {'nome': '%s %s' % (user.first_name, user.last_name)}
        dados = []
        for ano in range(inicial, final+1):
            log_ano = log_user.filter(action_time__year=ano)
            dados.append((ano, log_ano.filter(action_flag=1).count(), log_ano.filter(action_flag=2).count(), log_ano.filter(action_flag=3).count()))
        user_return['dados'] = dados
        returned.append(user_return)
        
    return TemplateResponse(request, 'admin/logs.html', {'users':returned})

@login_required
def serve_files(request, filename):
 
    # evita que o usuario tente acessar qualquer arquivo do sistema
    filename = filename.replace('..','')

    path = '%s/%s' % (settings.MEDIA_ROOT, filename)

    # descobre o mime type
    try:
        mime = magic.from_file(path, mime=True)
    except:
        raise Http404

    # monta a resposta sem conteúdo, apenas com o header do x-sendfile
    response = HttpResponse(mimetype=mime)
    response['X-Sendfile-encoding'] = 'url'
    response['X-Sendfile'] = urllib.quote(path.encode('utf-8'))
    response['Content-length'] = os.path.getsize(path)

    return response
