import django.dispatch

reset_tables = django.dispatch.Signal(providing_args=['reset_models'])