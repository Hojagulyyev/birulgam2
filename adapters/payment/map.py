from domain.payment.entities import Payment

# from api.gql.payment.schemas import PaymentSchema


class PaymentMap:
    
    @classmethod
    def to_gql_schema(cls, payment: Payment):
        ...