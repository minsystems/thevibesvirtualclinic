from django.utils.decorators import method_decorator

from thevibesvirtualclinic.decorators import ajax_required


class AjaxRequiredMixin(object):
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxRequiredMixin, self).dispatch(request, *args, **kwargs)
