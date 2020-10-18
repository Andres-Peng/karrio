import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import PickupDetails, ConfirmationDetails, ChargeDetails
from purpleserver.core.tests import APITestCase


class TesPickup(APITestCase):

    def test_schedule_pickup(self):
        url = reverse(
            'purpleserver.proxy:pickup-details',
            kwargs=dict(carrier_name="canadapost")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}?test", PICKUP_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, PICKUP_RESPONSE)

    def test_udpate_pickup(self):
        url = reverse(
            'purpleserver.proxy:pickup-details',
            kwargs=dict(carrier_name="canadapost")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = UPDATE_RETURNED_VALUE
            response = self.client.put(f"{url}?test", PICKUP_UPDATE_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_UPDATE_RESPONSE)

    def test_cancel_pickup(self):
        url = reverse(
            'purpleserver.proxy:pickup-cancel',
            kwargs=dict(carrier_name="canadapost")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = CANCEL_RETURNED_VALUE
            response = self.client.post(f"{url}?test", PICKUP_CANCEL_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertDictEqual(response_data, PICKUP_CANCEL_RESPONSE)


PICKUP_DATA = {
  "pickupDate": "2020-10-25",
  "address": {
    "addressLine1": "125 Church St",
    "personName": "John Doe",
    "companyName": "A corp.",
    "phoneNumber": "514-000-0000",
    "city": "Moncton",
    "countryCode": "CA",
    "postalCode": "E1C4Z8",
    "residential": False,
    "stateCode": "NB",
    "email": "john@a.com"
  },
  "parcels": [
    {
        "weight": 0.2,
        "width": 10,
        "height": 10,
        "length": 1,
        "packagingType": "envelope",
        "isDocument": True,
        "weightUnit": "KG",
        "dimensionUnit": "CM"
    }
  ],
  "readyTime": "13:00",
  "closingTime": "17:00",
  "instruction": "Should not be folded",
  "packageLocation": "At the main entrance hall"
}

PICKUP_UPDATE_DATA = {
    "pickupDate": "2020-10-23",
    "confirmationNumber": "27241",
    "address": {
        "addressLine1": "125 Church St",
        "personName": "John Doe",
        "companyName": "A corp.",
        "phoneNumber": "514-000-0000",
        "city": "Moncton",
        "countryCode": "CA",
        "postalCode": "E1C4Z8",
        "residential": False,
        "stateCode": "NB",
        "email": "john@a.com"
    },
    "parcels": [
        {
            "weight": 0.2,
            "width": 10,
            "height": 10,
            "length": 1,
            "packagingType": "envelope",
            "isDocument": True,
            "weightUnit": "KG",
            "dimensionUnit": "CM"
        }
    ],
    "readyTime": "14:30",
    "closingTime": "17:00",
    "instruction": "Should not be folded",
    "packageLocation": "At the main entrance hall"
}

PICKUP_CANCEL_DATA = {
  "confirmationNumber": "00110215"
}


SCHEDULE_RETURNED_VALUE = (
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-25",
        pickup_charge=ChargeDetails(
            name="Pickup fees",
            amount=0.0,
            currency="CAD"
        ),
        ready_time="13:00",
        closing_time="17:00"
    ),
    [],
)

UPDATE_RETURNED_VALUE = (
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-23",
        ready_time="14:30",
        closing_time="17:00"
    ),
    [],
)

CANCEL_RETURNED_VALUE = (
    ConfirmationDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        operation="Cancel Pickup",
        success=True
    ),
    []
)


PICKUP_RESPONSE = {
  "pickup": {
    "address": {
      "addressLine1": "125 Church St",
      "city": "Moncton",
      "companyName": "A corp.",
      "countryCode": "CA",
      "email": "john@a.com",
      "personName": "John Doe",
      "phoneNumber": "514-000-0000",
      "postalCode": "E1C4Z8",
      "residential": False,
      "stateCode": "NB"
    },
    "carrierId": "canadapost",
    "carrierName": "canadapost",
    "closingTime": "17:00",
    "confirmationNumber": "27241",
    "id": ANY,
    "instruction": "Should not be folded",
    "options": {},
    "packageLocation": "At the main entrance hall",
    "parcels": [
      {
        "dimensionUnit": "CM",
        "height": 10.0,
        "isDocument": True,
        "length": 1.0,
        "packagingType": "envelope",
        "weight": 0.2,
        "weightUnit": "KG",
        "width": 10.0
      }
    ],
    "pickupCharge": {
      "amount": 0.0,
      "currency": "CAD",
      "name": "Pickup fees"
    },
    "pickupDate": "2020-10-25",
    "readyTime": "13:00",
    "testMode": True
  }
}

PICKUP_UPDATE_RESPONSE = {
  "pickup": {
    "address": {
      "addressLine1": "125 Church St",
      "city": "Moncton",
      "companyName": "A corp.",
      "countryCode": "CA",
      "email": "john@a.com",
      "personName": "John Doe",
      "phoneNumber": "514-000-0000",
      "postalCode": "E1C4Z8",
      "residential": False,
      "stateCode": "NB"
    },
    "carrierId": "canadapost",
    "carrierName": "canadapost",
    "closingTime": "17:00",
    "confirmationNumber": "27241",
    "instruction": "Should not be folded",
    "options": {},
    "packageLocation": "At the main entrance hall",
    "parcels": [
      {
        "dimensionUnit": "CM",
        "height": 10.0,
        "isDocument": True,
        "length": 1.0,
        "packagingType": "envelope",
        "weight": 0.2,
        "weightUnit": "KG",
        "width": 10.0
      }
    ],
    "pickupDate": "2020-10-23",
    "readyTime": "14:30",
    "testMode": True
  }
}

PICKUP_CANCEL_RESPONSE = {
  "confirmation": {
    "carrierId": "canadapost",
    "carrierName": "canadapost",
    "operation": "Cancel Pickup",
    "success": True
  }
}
