from flask import current_app as app
import datetime

class InventoryItem:
    # productid | quantity 
    def __init__(self, id, seller_id, product_id, quantity):
        self.id = id
        self.seller_id = seller_id
        self.product_id = product_id
        self.quantity = quantity
        
        
class Inventory:
    """
    This is just a TEMPLATE for Inventory, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, seller_id):
        self.seller_id = seller_id

    def get_by_seller(self):
        rows = app.db.execute('''
        SELECT *
        FROM Inventories
        WHERE sellerId = :seller_id
        ''',
        seller_id=seller_id)
        return [InventoryItem(row[-2], row[-1]) for row in rows]

    @staticmethod
    def get_by_product(product_id):
        rows = app.db.execute('''
        SELECT *
        FROM Inventories
        WHERE productId = :product_id
        ''',
        product_id=product_id)
        return [InventoryItem(*row) for row in rows]
