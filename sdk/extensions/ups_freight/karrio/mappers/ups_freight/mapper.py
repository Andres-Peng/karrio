"""Karrio UPS Freight client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.ups_freight as provider
import karrio.mappers.ups_freight.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: models.PickupRequest) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)

    def create_pickup_update_request(
        self, payload: models.PickupUpdateRequest
    ) -> lib.Serializable:
        return provider.pickup_update_request(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: models.PickupCancelRequest
    ) -> lib.Serializable:
        return provider.pickup_cancel_request(payload, self.settings)

    def create_document_upload_request(
        self, payload: models.DocumentUploadRequest
    ) -> lib.Serializable[str]:
        return provider.document_upload_request(payload, self.settings)

    def parse_cancel_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_pickup_cancel_response(
            response.deserialize(), self.settings
        )

    def parse_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_response(response.deserialize(), self.settings)

    def parse_pickup_update_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_update_response(
            response.deserialize(), self.settings
        )

    def parse_rate_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return provider.parse_rate_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return provider.parse_tracking_response(response.deserialize(), self.settings)

    def parse_document_upload_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
        return provider.parse_document_upload_response(
            response.deserialize(), self.settings
        )
