from django.urls import path
from django.views.generic import TemplateView

from . import views as rc_common

urlpatterns = [
    path('dashboard',rc_common.DashboardView.as_view(),name='dashboard'),
    path('configurations',rc_common.CommonConfigurationsView.as_view(),name='rc_configurations'),
    path('reset',rc_common.CommonResetTables.as_view(),name='rc_reset_tables'),
    path('progress-bar/',rc_common.CeleryJobAsyncResult.as_view(),name='celery_job_result_ajax'),
    path('progress-bar/<slug:result_id>',rc_common.CeleryJobAsyncResult.as_view(),name='celery_job_result'),
    path('test-code', TemplateView.as_view(template_name='rc_common/test_template.html'),name='test_code'),
]
