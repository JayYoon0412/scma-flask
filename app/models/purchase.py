from flask import current_app as app


class Purchase:
    def __init__(self, ownerId, productId, productName, quantity):
        self.ownerId = ownerId
        self.productId = productId
        self.productName = productName
        self.quantity = quantity

    @staticmethod
    def getByUserId(uid):
        rows = app.db.execute('''
SELECT ownerId, productId, name, quantity        
FROM
(SELECT ownerId, productId, quantity
FROM CartItems
WHERE ownerId = :uid AND isOrdered = true) purchases JOIN Products ON purchases.productId = Products.id
''', uid=uid)
        return [Purchase(*row) for row in rows]
