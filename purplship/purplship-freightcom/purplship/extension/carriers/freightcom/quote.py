from typing import List, Tuple
from pyfreightcom.quote_request import (
    Freightcom, QuoteRequestType, FromType, ToType, PackagesType, PackageType
)
from pyfreightcom.quote_reply import QuoteType
from purplship.core.errors import RequiredFieldError
from purplship.core.utils import Element, Serializable, concat_str
from purplship.core.models import RateRequest, RateDetails, Error, ChargeDetails
from purplship.core.units import Package, Options
from purplship.extension.carriers.freightcom.utils import Settings, standard_request_serializer
from purplship.extension.carriers.freightcom.units import Service, FreightPackagingType, FreightClass, Option
from purplship.extension.carriers.freightcom.error import parse_error_response


def parse_quote_reply(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    estimates = response.xpath(".//*[local-name() = $name]", name="Quote")
    return (
        [_extract_rate(node, settings) for node in estimates],
        parse_error_response(response, settings)
    )


def _extract_rate(node: Element, settings: Settings) -> RateDetails:
    quote = QuoteType()
    quote.build(node)
    service = Service(str(quote.serviceId)).name if quote.serviceId is not None else None

    extra_charges = [ChargeDetails(
        name="Fuel surcharge",
        amount=float(quote.fuelSurcharge),
        currency=quote.currency
    )] if quote.fuelSurcharge is not None else []

    return RateDetails(
        carrier=settings.carrier_name,
        currency=quote.currency,
        service=service,
        base_charge=float(quote.baseCharge),
        total_charge=float(quote.totalCharge),
        estimated_delivery=str(quote.transitDays),
        extra_charges=extra_charges
    )


def quote_request(payload: RateRequest, settings: Settings) -> Serializable[Freightcom]:
    package = Package(payload.parcel)
    dimensions = [("weight", package.weight.value), ("height", package.height.value), ("width", package.width.value), ("length", package.length.value)]

    for key, dim in dimensions:
        if dim is None:
            raise RequiredFieldError(key)

    packaging_type = FreightPackagingType[package.packaging_type or "small_box"].value
    options = Options(payload.parcel.options)
    service = next(
        (Service[s].value for s in payload.parcel.services if s in Service.__members__),
        Service.freightcom_central_transport.value
    )
    freight_class = next(
        (FreightClass[c].value for c in payload.parcel.options.keys() if c in FreightClass.__members__),
        None
    )
    special_services = {
        Option[s]: True for s in payload.parcel.options.keys() if s in Option.__members__
    }

    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        QuoteRequest=QuoteRequestType(
            saturdayPickupRequired=special_services.get(Option.freightcom_saturday_pickup_required),
            homelandSecurity=special_services.get(Option.freightcom_homeland_security),
            pierCharge=None,
            exhibitionConventionSite=special_services.get(Option.freightcom_exhibition_convention_site),
            militaryBaseDelivery=special_services.get(Option.freightcom_military_base_delivery),
            customsIn_bondFreight=special_services.get(Option.freightcom_customs_in_bond_freight),
            limitedAccess=special_services.get(Option.freightcom_limited_access),
            excessLength=special_services.get(Option.freightcom_excess_length),
            tailgatePickup=special_services.get(Option.freightcom_tailgate_pickup),
            residentialPickup=special_services.get(Option.freightcom_residential_pickup),
            crossBorderFee=None,
            notifyRecipient=special_services.get(Option.freightcom_notify_recipient),
            singleShipment=special_services.get(Option.freightcom_single_shipment),
            tailgateDelivery=special_services.get(Option.freightcom_tailgate_delivery),
            residentialDelivery=special_services.get(Option.freightcom_residential_delivery),
            insuranceType=options.insurance is not None,
            scheduledShipDate=None,
            insideDelivery=special_services.get(Option.freightcom_inside_delivery),
            isSaturdayService=special_services.get(Option.freightcom_is_saturday_service),
            dangerousGoodsType=special_services.get(Option.freightcom_dangerous_goods_type),
            serviceId=service,
            stackable=special_services.get(Option.freightcom_stackable),
            From=FromType(
                id=payload.shipper.type,
                company=payload.shipper.company_name,
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=concat_str(payload.shipper.address_line_1, join=True),
                address2=concat_str(payload.shipper.address_line_2, join=True),
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code
            ),
            To=ToType(
                id=payload.recipient.type,
                company=payload.recipient.company_name,
                notifyRecipient=None,
                instructions=None,
                email=payload.recipient.email,
                attention=payload.recipient.person_name,
                phone=payload.recipient.phone_number,
                tailgateRequired=None,
                residential=payload.recipient.residential,
                address1=concat_str(payload.recipient.address_line_1, join=True),
                address2=concat_str(payload.recipient.address_line_2, join=True),
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code
            ),
            COD=None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=package.length.value,
                        width=package.width.value,
                        height=package.height.value,
                        weight=package.weight.value,
                        type_=packaging_type,
                        freightClass=freight_class,
                        nmfcCode=None,
                        insuranceAmount=None,
                        codAmount=None,
                        description=payload.parcel.description,
                    )
                ]
            ),
        )
    )

    return Serializable(request, standard_request_serializer)
