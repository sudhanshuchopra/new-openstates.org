from django.contrib.contenttypes.models import ContentType
from opencivicdata.legislative.models import Bill
from .common import create_issues
from ..issues import IssueType
from ..models import DataQualityIssue


def bills_report(jur):
    contenttype_obj = ContentType.objects.get_for_model(Bill)
    DataQualityIssue.objects.filter(jurisdiction=jur, status='active',
                                    content_type=contenttype_obj).delete()
    bills = Bill.objects.filter(legislative_session__jurisdiction=jur)
    count = 0
    for issue in IssueType.get_issues_for('bill'):
        if issue == 'no-actions':
            queryset = bills.filter(actions__isnull=True)
            count += create_issues(queryset, issue, jur)
        elif issue == 'no-sponsors':
            queryset = bills.filter(sponsorships__isnull=True)
            count += create_issues(queryset, issue, jur)
        elif issue == 'unmatched-person-sponsor':
            queryset = bills.filter(sponsorships__entity_type='person',
                                    sponsorships__person__isnull=True).distinct()
            count += create_issues(queryset, issue, jur)
        elif issue == 'unmatched-org-sponsor':
            queryset = bills.filter(sponsorships__entity_type='organization',
                                    sponsorships__organization__isnull=True).distinct()
            count += create_issues(queryset, issue, jur)
        elif issue == 'no-versions':
            queryset = bills.filter(versions__isnull=True)
            count += create_issues(queryset, issue, jur)
        else:
            raise ValueError("Bill Importer needs update for new issue.")
    print("Imported Bills Related {} Issues for {}".format(count, jur.name))
