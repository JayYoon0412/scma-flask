from flask import current_app as app

Queries = {
    "All": '''
        SELECT * FROM
        ((SELECT *
        FROM ProductReviews
        WHERE writerId = :writerId
        ORDER BY createdat DESC
        LIMIT 5)

        UNION ALL

        (SELECT * 
        FROM SellerReviews
        WHERE writerId = :writerId
        ORDER BY createdat DESC
        LIMIT 5)) AS t
        ORDER BY t.createdat DESC
        LIMIT 5;
        ''',
    "Product": '''
        SELECT *
        FROM ProductReviews
        WHERE writerId = :writerId
        ORDER BY createdat DESC
        LIMIT 5;
        ''',
    "Seller": '''
        SELECT * 
        FROM SellerReviews
        WHERE writerId = :writerId
        ORDER BY createdat DESC
        LIMIT 5;
        '''
}
updateQueries = {
    "Product":'''
        UPDATE productreviews
        SET rating = :score,
            description = :description
        WHERE writerid = :user AND productId = :id;
        ''',
    "Seller":'''
        UPDATE sellerreviews
        SET rating = :score,
            description = :description
        WHERE writerid = :user AND sellerId = :id;
        '''
}

class Review:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, id, createdAt, rating, descp, ratedId, writerId):
        self.id = id
        self.createdAt = createdAt
        self.rating = rating
        self.description = descp
        self.ratedId = ratedId # can be product Id or seller ID? 
        self.writerId = writerId

    @staticmethod
    def get_top_review_by(id, type):
        rows = app.db.execute(Queries[type], writerId=id)
        print(rows)
        # return Review(*(rows[0])) if rows else None
        return [Review(*row) for row in rows]

    @staticmethod
    def updateTable(userId, rating, ratedId, descp, database):
        app.db.execute(updateQueries[database], 
                                    user=userId, 
                                    score=rating, 
                                    description=descp, 
                                    id = ratedId)
        return
        

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT id, uid, pid, review_time, review_content
        FROM Review
        WHERE uid = :uid
        AND review_time >= :since
        ORDER BY review_time DESC
        ''',
        uid=uid,
        since=since)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_reviews_by_product(productId):
        rows = app.db.execute('''
        SELECT *
        FROM ProductReviews
        WHERE productId = :productId
        ORDER BY createdAt DESC
        ''',
        productId=productId
        )
        return [Review(*row) for row in rows]
