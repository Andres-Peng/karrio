from typing import Any
from karrio.core.utils import XP, request as http, Serializable, Deserializable
from karrio.api.proxy import Proxy as BaseProxy
from dhl_express_lib.dct_req_global_2_0 import DCTRequest
from dhl_express_lib.tracking_request_known_1_0 import KnownTrackingRequest
from dhl_express_lib.ship_val_global_req_10_0 import ShipmentRequest
from dhl_express_lib.book_pickup_global_req_3_0 import BookPURequest
from dhl_express_lib.modify_pickup_global_req_3_0 import ModifyPURequest
from dhl_express_lib.cancel_pickup_global_req_3_0 import CancelPURequest
from dhl_express_lib.routing_global_req_2_0 import RouteRequest
from karrio.mappers.dhl_express.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, request: Serializable) -> str:
        return http(
            url=self.settings.server_url,
            data=request.serialize(),
            headers={"Content-Type": "application/xml"},
            trace=self.trace_as("xml"),
            method="POST",
        )

    def validate_address(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def get_tracking(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def modify_pickup(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def cancel_pickup(self, request: Serializable) -> Deserializable:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)
