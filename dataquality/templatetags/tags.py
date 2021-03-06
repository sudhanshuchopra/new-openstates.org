from django import template
from opencivicdata.legislative.models import LegislativeSession
from opencivicdata.core.models import Person, Jurisdiction

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def legislative_session_list(jur_id):
    legislative_sessions = LegislativeSession.objects.filter(
        jurisdiction_id=jur_id).values('name', 'identifier') \
        .order_by('-identifier')
    return legislative_sessions


@register.simple_tag
def person_from_id(person_id):
    return Person.objects.get(id=person_id).name


@register.simple_tag
def jurisdiction_name_from_id(jurisdiction_id):
    return Jurisdiction.objects.get(id=jurisdiction_id).name
