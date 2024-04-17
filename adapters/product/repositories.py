from domain.product.interfaces import IProductRepository
from domain.product.entities import Product

from sqlite3 import Connection


class ProductListRepository(IProductRepository):
    _products: list[Product] = []
    
    def list(self) -> list[Product]:
        return self._products
    
    def save(self, product) -> Product:
        self._products.append(product)
        return product


class ProductSqliteRepository(IProductRepository):

    def __init__(self, conn: Connection):
        self._conn = conn
    
    def list(self) -> list[Product]:
        stmt = "SELECT id, name FROM products"
        cursor = self._conn.cursor()
        cursor.execute(stmt)

        products = []
        for row in cursor.fetchall():
            product = Product(
                id=row[0],
                name=row[1],
            )
            products.append(product)

        return products
        
    def save(self, product: Product) -> Product:
        if not product.id:
            stmt = "INSERT INTO products (name) VALUES (:name)"
            data = {'name': product.name}
        else:
            stmt = "UPDATE products SET name = :name WHERE id = :id"
            data = {"name": product.name, "id": product.id}
        
        cursor = self._conn.cursor()
        cursor.execute(stmt, data)

        if not product.id:
            product.id = cursor.lastrowid

        return product
