from flask import current_app as app


class Cart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, ownerId, productId, orderId, sellerId, quantity, isOrdered, isFulfilled, name, price, category):
        self.ownerId = ownerId
        self.productId = productId
        self.orderId = orderId
        self.sellerId = sellerId
        self.quantity = quantity
        self.isOrdered = isOrdered
        self.isFulfilled = isFulfilled
        self.name = name
        self.price = price
        self.category = category

    @staticmethod
    def get(ownerId):
        rows = app.db.execute('''
SELECT *
FROM CartItems
WHERE ownerId = :ownerId
''',
                              ownerId=ownerId)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_ownerid(ownerId, ordered = False):
        rows = app.db.execute('''
SELECT c.ownerId as ownerId, c.productId as productId, c.orderId as orderId, c.sellerId as sellerId, c.quantity as quantity, c.isOrdered as isOrdered, c.isFulfilled as isFulfilled, p.name as name, p.price as price, p.category as category
FROM CartItems c, Products p
WHERE c.ownerId = :ownerId
AND c.isOrdered = :ordered
AND c.productId = p.id
''',
                              ownerId=ownerId,
                              ordered=ordered)
        return [Cart(*row) for row in rows]