import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import gettext_lazy as _
from apps.api_exception import ParameterException
from .handler import KpiFactory


class DashboardResult(wtypes.Base):
    status_code = wsme.wsattr(int, default=200)
    content = _types.jsontype
    detail = wsme.wsattr(wtypes.text, default=str(_('success')))


class KpiBody(wtypes.Base):
    indicator = wsme.wsattr(wtypes.text, mandatory=True)

    def validate(self):
        if self.indicator not in KpiFactory.options:
            raise ParameterException(msg=str(_("params error")))
        return self
