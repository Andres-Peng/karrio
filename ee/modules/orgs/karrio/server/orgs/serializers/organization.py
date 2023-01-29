from django.db import transaction

import karrio.server.orgs.serializers as serializers
import karrio.server.orgs.models as models


@serializers.owned_model_serializer
class OrganizationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("id", "name", "slug")

    @transaction.atomic
    def create(self, data: dict, **kwargs):
        created_by = data.pop("created_by")

        org = super().create(data, **kwargs)
        # Set as organization user
        org_user = org.add_user(created_by, is_admin=True)
        # Set as organization owner
        org.change_owner(org_user)
        org.save()

        return org

    def update(self, instance, data: dict, **kwargs) -> models.Organization:
        if "name" in data and "slug" not in data:
            data.update(
                slug=data["name"].lower().replace(" ", ""),
            )

        return super().update(instance, data)
