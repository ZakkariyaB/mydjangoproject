import traceback

from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required


from .forms import AddUserForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.add_user',raise_exception=True), name='dispatch')
class AddNewUserView(View):
    template_name = 'rc_core/add_user.html'
    def get(self,request,*args,**kwargs):
        context = {}
        context.update(self.get_add_context())
        context['form'] = AddUserForm()
        context['form'].buttons = self.get_form_buttons()
        return render(request,self.template_name,context)
    
    def post(self,request,*args,**kwargs):
        if request.POST:
            try:
                form = AddUserForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    messages.success(request,"User Added Successfully")
                else:
                    context = {}
                    context.update(self.get_add_context())
                    context['form'] = form
                    context['form'].buttons = self.get_form_buttons()
                    return render(request,self.template_name,context)
            except Exception as e:
                traceback.print_exc()
                messages.error(request,"Some Error Occured. Please Try Again")
        return HttpResponseRedirect(reverse('adduser'))

    def get_add_context(self):
        context = {}        
        context['table_header'] = {'title' : 'Add User','icon':'<i class="fa fa-user"></i>'}
        return context

    def get_form_buttons(self):
        buttons = [
            {'type' : 'submit', 'label' : "Add User" , 'class' : 'btn btn-block btn-success' }
        ]
        return buttons

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.view_user',raise_exception=True), name='dispatch')
class ManageUserView(ListView):
    model = User
    paginate_by = 20
    template_name = 'common_table_page.html'
    
    def get_queryset(self,**kwargs):
        qs = User.objects.filter(is_superuser=False,is_staff=False,is_active=True).annotate(fullname=Concat('first_name',V(' '),'last_name')).prefetch_related('groups').order_by('id')
        for q in qs:
            q.group = [g.name for g in q.groups.all()]
        #     q['actions'] = {}
        #     q['actions']['links'] = [{'url_name' : 'edit_a_record', 'kwargs':{'record':q["id"]}, 'label':mark_safe('<i class="fa fa-pencil" aria-hidden="true"></i>')}]
        #     q['actions']['links'].append({'url_name' : 'delete_a_record', 'kwargs':{'record':q["id"]}, 'label':mark_safe('<i class="fa fa-trash text-danger" aria-hidden="true"></i>')})
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_header'] = {'title' : 'All Users','icon':'<i class="fa fa-users"></i>'}
        context['table_values'] = context['page_obj']
        # context['value_as_actions'] = ['actions']
        context['value_as_list'] = ['group']

        table_headers = {
            'fullname' : 'Name',
            'username' : 'Username',
            'email' : 'E-mail',
            'group' : 'Role',
            # 'actions' : 'Actions',
        }
        context['table_headers'] = table_headers
        return context
