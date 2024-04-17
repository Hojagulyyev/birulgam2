import strawberry
 
 
@strawberry.type
class Product:
    id: int
    name: str
