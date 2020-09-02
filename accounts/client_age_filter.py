from django.contrib import admin
from datetime import date
import datetime
from django.utils.translation import gettext_lazy as _


# '''custom function to filter min & max age range
#    Status: it currently isnt working will get back to it later
#    Installed Plugin: pip install python-dateutil
# '''
# def age_ranges(min_age, max_age):
#     from dateutil.relativedelta import relativedelta
#     today = datetime.date.today()
#     min_range = (today - relativedelta(years=min_age)).year
#     max_range = (today - relativedelta(years=max_age)).year
#     return [max_range, min_range]


class ClientAgeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('age ranges')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('children', _('children')),
            ('teenager', _('teenager')),
            ('youth', _('youth')),
            ('adult', _('adult')),
        )

    def queryset(self, request, queryset):

        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'children':
            return queryset.filter(birthday__gte=date(2010, 1, 1),
                                   birthday__lte=datetime.date.today())

        if self.value() == 'teenager':
            return queryset.filter(birthday__gte=date(2003, 1, 1),
                                   birthday__lte=datetime.date.today())

        if self.value() == 'youth':
            return queryset.filter(birthday__gte=date(1985, 1, 1),
                                   birthday__lte=datetime.date.today())
        if self.value() == 'adult':
            return queryset.filter(birthday__gte=date(1940, 1, 1),
                                   birthday__lte=datetime.date.today())