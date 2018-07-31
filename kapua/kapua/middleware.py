from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import remove_www, get_tenant_model, get_public_schema_name


class CustomTenantMiddleware(MiddlewareMixin):
    def get_tenant(self, model, hostname, request):
        return model.objects.get(domain_url=hostname)

    def hostname_from_request(self, request):
        """ Extracts hostname from request. Used for custom requests filtering.
           By default removes the request's port and common prefixes.
       """
        return remove_www(request.get_host().split(':')[0]).lower()

    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()

        hostname = self.hostname_from_request(request)
        TenantModel = get_tenant_model()

        try:
            # get_tenant must be implemented by extending this class.
            tenant = self.get_tenant(TenantModel, hostname, request)
            assert isinstance(tenant, TenantModel)
            request.tenant = tenant
            connection.set_tenant(request.tenant)

        except (TenantModel.DoesNotExist, AssertionError):
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
            request.public_tenant = True
            return

        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
