from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()

@register.filter
def getattribute(obj,key):
    try:
        if str(key) in obj:
            return obj[str(key)]
    except:
        if hasattr(obj,str(key)):
            return getattr(obj,str(key)) if getattr(obj,str(key)) else '-'
    return '-'

@register.filter
def get_as_list(values_as_list):
    if values_as_list != '-':
        html = '<ul style="padding:0;">'
        for item in values_as_list:
            html += f'<li>{item}</li>'
    else :
        html = '<ul style="padding:0;list-style:none;"><li>-</li>'
    html += '</ul>'
    return mark_safe(html)

@register.filter
def value_as_issue_status(obj,status):
    if getattr(obj,str(status)):
        html = f'<span class="badge bg-red">Issued</span>'
    else :
        html = f'<span class="badge bg-green">Available</span>'
    return mark_safe(html)

@register.filter
def value_as_issue_history_status(obj,status):
    if getattr(obj,str(status)):
        html = f'<span class="badge bg-red">Issued</span>'
    else :
        html = f'<span class="badge bg-green">Returned</span>'
    return mark_safe(html)

@register.simple_tag
def render_table_action(links_map):
    links = links_map.get('links',[])
    modal_links = links_map.get('modal',[])
    html = ''
    for m_link in modal_links:
        html += f'<td><a '
        for attr_key,attr_value in m_link.items() :
            if attr_key != 'label' :
                html += f'{attr_key}="{attr_value}"'
        html += f'>{m_link["label"]}</a></td>'
    for link in links:
        html += f'<td><a href="{reverse(link["url_name"],kwargs=link["kwargs"])}">{link["label"]}</a></td>'
    return mark_safe(html)

@register.simple_tag
def render_record_to_issue(record):
    html = ''
    for key,value in record.items():
        if key not in ['_state','id','created','modified','is_issued']:
            html += f'<tr><th>{key}</th><td>{value}</td></tr>'
    return mark_safe(html)

@register.simple_tag
def load_join_col_head(join_cols_headers):
    if not join_cols_headers:
        return ''
    html= '<th>'
    for col_head in join_cols_headers.values():
        html += f' {col_head}'
    html += '</th>'
    return mark_safe(html)

@register.simple_tag
def load_join_col_data(data, join_cols_headers):
    if not join_cols_headers:
        return ''
    html= '<td>'
    for key in join_cols_headers.keys():
        try:
            if str(key) in data:
                html += data[str(key)]
        except:
            if hasattr(data,str(key)):
                html += getattr(data,str(key)) if getattr(data,str(key)) else '-'
    html += '</td>'
    return mark_safe(html)

@register.inclusion_tag('elements/tables/inner_filter.html', takes_context=True)
def table_inner_filter(context):
    return {'table_inner_filter' : context['table_inner_filter'] if 'table_inner_filter' in context else {} ,'request':context['request']}
