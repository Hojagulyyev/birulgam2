import strawberry

from .otp.resolvers import (
    send_otp_resolver,
    send_otp_response,
)
from .user.resolvers import (
    signup_user_resolver,
    signup_user_response,
    signin_user_resolver,
    signin_user_response,
)
from .company.resolvers import (
    create_company_resolver,
    create_company_response,
)
from .contact.resolvers import (
    create_contact_resolver,
    create_contact_response,
)
from .deal.resolvers import (
    create_deal_resolver,
    create_deal_response,
)
from .payment.resolvers import (
    create_payment_resolver,
    create_payment_response,
)


@strawberry.type
class Mutation:
    send_otp: send_otp_response = strawberry.mutation(
        resolver=send_otp_resolver)
    signup_user: signup_user_response = strawberry.mutation(
        resolver=signup_user_resolver)
    signin_user: signin_user_response = strawberry.mutation(
        resolver=signin_user_resolver)
    create_company: create_company_response = strawberry.mutation(
        resolver=create_company_resolver)
    create_contact: create_contact_response = strawberry.mutation(
        resolver=create_contact_resolver)
    create_deal: create_deal_response = strawberry.mutation(
        resolver=create_deal_resolver)
    create_payment: create_payment_response = strawberry.mutation(
        resolver=create_payment_resolver)
