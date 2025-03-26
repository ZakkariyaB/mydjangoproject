from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator

from .forms import CommonConfigurationForm,CommonResetForm
from .utilitties import CommonUtility
from .signals import reset_tables
# Create your views here.

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('rc_common.dashboard_permissions',raise_exception=True), name='dispatch')
class DashboardView(View):
    template_name = 'rc_common/dashboard.html'
    def get(self,request,*args,**kwargs):
        context = {}
        return render(request,self.template_name,context)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('rc_common.add_commonconfigurations',raise_exception=True), name='dispatch')
class CommonConfigurationsView(View):
    template_name = 'rc_common/configurations.html'

    def get_form_buttons(self):
        buttons = [
            {'type' : 'submit' , 'label' : 'Save Configurations', 'class' : 'btn btn-block btn-primary'},
        ]
        return buttons

    def get(self,request,*args,**kwargs):
        try:
            context = {}
            context['table_header'] = {'title' : 'Configurations','icon':'<i class="fa fa-cog"></i>'}
            initial = CommonUtility().get_configs(['record_sections','record_categories'])
            context['form'] = CommonConfigurationForm(initial=initial)
            context['form'].buttons = self.get_form_buttons()
            return render(request,self.template_name,context)
        except Exception:
            messages.error(request,"Some Error Occured. Please Try Again")
            return HttpResponseRedirect(reverse('dashboard'))

    def post(self,request,*args,**kwargs):
        try:
            if request.POST:
                form = CommonConfigurationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request,"Configurations Are Updated Successfully")
                else :
                    context = {}
                    context['table_header'] = {'title' : 'Configurations','icon':'<i class="fa fa-cog"></i>'}
                    context['form'] = form
                    context['form'].buttons = self.get_form_buttons()
                    return render(request,self.template_name,context)
            return HttpResponseRedirect(reverse('rc_configurations'))
        except Exception:
            messages.error(request,"Some Error Occured. Please Try Again")
            return HttpResponseRedirect(reverse('rc_configurations'))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('rc_common.system_reset_permissions',raise_exception=True), name='dispatch')
class CommonResetTables(View):
    template_name = 'rc_common/configurations.html'

    def get_form_buttons(self):
        buttons = [
            {'type' : 'submit' , 'label' : 'Reset', 'class' : 'btn btn-block btn-primary'},
        ]
        return buttons

    def get(self,request,*args,**kwargs):
        try:
            context = {}
            context['table_header'] = {'title' : 'Reset System','icon':'<i class="fa fa-cog"></i>'}
            context['form'] = CommonResetForm()
            context['form'].buttons = self.get_form_buttons()
            return render(request,self.template_name,context)
        except Exception:
            messages.error(request,"Some Error Occured. Please Try Again")
            return HttpResponseRedirect(reverse('dashboard'))

    def post(self,request,*args,**kwargs):
        try:
            if request.POST:
                form = CommonResetForm(request.POST)
                if form.is_valid():
                    reset_tables.send(sender=self.__class__,models=form.cleaned_data)
                    pass
                    messages.success(request,"Reset Completed")
                else :
                    context = {}
                    context['table_header'] = {'title' : 'Reset System','icon':'<i class="fa fa-cog"></i>'}
                    context['form'] = form
                    context['form'].buttons = self.get_form_buttons()
                    return render(request,self.template_name,context)
            return HttpResponseRedirect(reverse('rc_reset_tables'))
        except Exception:
            messages.error(request,"Some Error Occured. Please Try Again")
            return HttpResponseRedirect(reverse('rc_reset_tables'))


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class CeleryJobAsyncResult(View):  
    def get(self,request,*args,**kwargs):
        from celery.result import AsyncResult
        from rc_config.celery import app
        if request.is_ajax():
            if 'task_ids[]' in request.GET and request.GET['task_ids[]']:
                task_ids = request.GET.getlist('task_ids[]')
                return_data = {}
                for task_id in task_ids:
                    task = AsyncResult(task_id)
                    data = {
                        'result' : task.result,
                        'state' : task.state
                    }
                    return_data[task_id] = data
                return JsonResponse(return_data)
        if 'result_id' in kwargs:
            result = app.GroupResult.restore(kwargs['result_id'])
            task_ids = [task for parents in result.children for task in parents.as_list()[::-1]]
            return render(request,'rc_common/progress_bar.html',{'task_ids':task_ids})
        return render(request,'rc_common/progress_bar.html',{'task_ids':[]})

    def post(self,request,*args,**kwargs):
        print(request.POST)
