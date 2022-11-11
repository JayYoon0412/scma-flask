from flask import current_app as app


class Product:
    def __init__(self, id, name, description, price, available, category, createdAt, imageSrc):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.available = available
        self.category = category
        self.createdAt = createdAt
        self.imageSrc = imageSrc

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE id = :id
        ''',
        id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        ''',
        available=available)
        return [Product(*row) for row in rows]
    
    # @staticmethod
    # def get_count(available=True):
    #     count = app.db.execute('''
    #     SELECT COUNT(*)
    #     FROM Products
    #     WHERE available = :available
    #     ''',
    #     available=available)
    #     return count

    
    @staticmethod
    def get_all_paginate(offset, available=True, rowNumber=60):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        OFFSET :offset ROWS
        FETCH NEXT :rowNumber ROWS ONLY
        ''',
        available=available, rowNumber=rowNumber, offset=offset)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_products(row_count, available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        LIMIT :row_count
        ''',
        available=available, row_count=row_count
        )
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_expensive(row_count):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        ORDER BY price DESC
        LIMIT :row_count
        ''',
        row_count=row_count
        )
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_categoryProducts(category):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE category = :category
        ''',
        category=category
        )
        return [Product(*row) for row in rows]
    
    # check multiconditions
    @staticmethod
    def get_priceProducts(lowerBound, upperBound, available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE price >= :lowerBound AND price <= :upperBound AND available = :available
        ''',
        lowerBound=lowerBound,
        upperBound=upperBound,
        available=available
        )
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_lowPriceProducts(available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        ORDER BY price ASC
        ''',
        available=available
        )
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_highPriceProducts(available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        ORDER BY price DESC
        ''',
        available=available
        )
        return [Product(*row) for row in rows]

    @staticmethod
    def get_priceAboveProducts(lowerBound, available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE price >= :lowerBound AND available = :available
        ''',
        lowerBound=lowerBound,
        available=available
        )
        return [Product(*row) for row in rows]

    @staticmethod
    def get_keywordProducts(keyword):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE name LIKE :keyword
        ''',
        keyword=keyword
        )
        return [Product(*row) for row in rows]

    @staticmethod
    def postProductReview(user, productId, rating, descp, time):
        """
        insert review into database
        """
        print("Review received")
        res = app.db.execute('''
        SELECT MAX(id) FROM productreviews;
        ''')
        newId = res[0][0] + 1
        print(newId)
        app.db.execute('''
        INSERT INTO productreviews(id, createdat, rating, description, productid, writerid)
        VALUES(:reviewid, :dateTime, :score, :description, :productid, :userid);
        ''',
        reviewid = newId, dateTime=time, score=rating, description=descp, productid=productId, userid=user)
        return 
