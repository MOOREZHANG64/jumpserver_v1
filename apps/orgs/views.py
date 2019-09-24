from django.shortcuts import redirect, reverse
from django.http import HttpResponseForbidden

from django.views.generic import DetailView, View

from .models import Organization
from common.utils import UUID_PATTERN


class SwitchOrgView(DetailView):
    model = Organization
    object = None

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.object = Organization.get_instance(pk)
        oid = str(self.object.id)
        request.session['oid'] = oid
        host = request.get_host()
        referer = request.META.get('HTTP_REFERER')
        if referer.find(host) == -1:
            return redirect(reverse('index'))
        if UUID_PATTERN.search(referer):
            return redirect(reverse('index'))
        return redirect(referer)


class SwitchToAOrgView(View):
    def get(self, request, *args, **kwargs):
        admin_orgs = Organization.get_user_admin_orgs(request.user)
        if not admin_orgs:
            return HttpResponseForbidden()
        default_org = Organization.default()
        if default_org in admin_orgs:
            redirect_org = default_org
        else:
            redirect_org = admin_orgs[0]
        return redirect(reverse('orgs:org-switch', kwargs={'pk': redirect_org.id}))