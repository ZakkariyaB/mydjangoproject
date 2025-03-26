from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def rc_validate_class(form,field):
    field_classes = field.field.widget.attrs.get('class','')
    field_classes = ' '.join([field_classes,'form-control'])
    if form.is_bound:
        if field.errors :
            field_classes = ' '.join([field_classes,'is-invalid'])
        else:
            field_classes = ' '.join([field_classes,'is-valid'])
    return field_classes

@register.simple_tag
def rc_validate_error(field):
    if field.errors:
        error_message = ''
        for error in field.errors:
            error_message += f'<div class="invalid-feedback">{error}</div>'
        return mark_safe(error_message)    
    return ''

@register.simple_tag
def rc_field_help_text(field):
    if field.help_text:
        return mark_safe(f'<p class="form-text text-muted">{field.help_text}</p>')    
    return mark_safe('<p class="form-text text-muted"></p>')