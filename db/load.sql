\COPY Users FROM '../generated/Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM '../generated/Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Inventories FROM '../generated/Inventories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.inventories_id_seq',
                         (SELECT MAX(id)+1 FROM Inventories),
                         false);

\COPY Orders FROM '../generated/Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_id_seq',
                         (SELECT MAX(id)+1 FROM Orders),
                         false);

\COPY CartItems FROM '../generated/CartItems.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.cartItems_id_seq',
                         (SELECT MAX(id)+1 FROM CartItems),
                         false);

\COPY ProductReviews FROM '../generated/ProductReviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.productReviews_id_seq',
                         (SELECT MAX(id)+1 FROM ProductReviews),
                         false);

\COPY SellerReviews FROM '../generated/SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellerReviews_id_seq',
                         (SELECT MAX(id)+1 FROM SellerReviews),
                         false);