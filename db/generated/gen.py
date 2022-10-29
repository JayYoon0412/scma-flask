from werkzeug.security import generate_password_hash
import csv
from faker import Faker

# number of sample entities to be generated
num_users = 10
num_products = 20
num_inventories = 10
num_orders = 10
num_cartItems = 10
num_productReviews = 10
num_sellerReviews = 10

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.sentence(nb_words=10)
            balance = fake.pyfloat(right_digits=2, min_value=0, max_value=10000)
            isSeller = fake.pybool()
            writer.writerow([uid, email, password, firstname, lastname, address, balance, isSeller])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            description = fake.sentence(nb_words=8)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            category = fake.random_element(elements=('fiction', 'nonfiction', 'drama', 'poetry'))
            createdAt = fake.date_time()
            imageSrc = fake.file_name(extension='jpeg')
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, description, price, available, category, createdAt, imageSrc])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_inventories(num_inventories, num_users, available_pids):
    with open('Inventories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventories...', end=' ', flush=True)
        for id in range(num_inventories):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            sellerId = fake.random_int(min=0, max=num_users-1)
            productId = fake.random_element(elements=available_pids)
            quantity = fake.pyint(min_value=0, max_value=9999)
            writer.writerow([id, sellerId, productId, quantity])
        print(f'{num_inventories} generated')
    return

def gen_orders(num_orders):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        for id in range(num_orders):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            isFulfilled = fake.pybool()
            createdAt = fake.date_time()
            writer.writerow([id, isFulfilled, createdAt])
        print(f'{num_orders} orders generated')
    return

def gen_cartItems(num_cartItems, num_users, num_orders, available_pids):
    with open('CartItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        for id in range(num_cartItems):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            ownerId = fake.random_int(min=0, max=num_users-1)
            productId = fake.random_element(elements=available_pids)
            orderId = fake.random_int(min=0, max=num_orders-1)
            sellerId = fake.random_int(min=0, max=num_users-1)
            quantity = fake.random_int(min=1, max=10)
            isOrdered = fake.pybool()
            isFulfilled = fake.pybool()
            writer.writerow([ownerId, productId, orderId, sellerId, quantity, isOrdered, isFulfilled])
        print(f'{num_cartItems} cart items created')
    return

def gen_productReviews(num_productReviews, available_pids, num_users):
    with open('ProductReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        for id in range(num_productReviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            createdAt = fake.date_time()
            rating = fake.random_int(min=1, max=5)
            description = fake.sentence(nb_words=15)
            productId = fake.random_element(elements=available_pids)
            writerId = fake.random_int(min=0, max=num_users-1)
            writer.writerow([id, createdAt, rating, description, productId, writerId])
        print(f'{num_productReviews} product reviews created')
    return

def gen_sellerReviews(num_sellerReviews, available_pids, num_users):
    with open('SellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        for id in range(num_sellerReviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            createdAt = fake.date_time()
            rating = fake.random_int(min=1, max=5)
            description = fake.sentence(nb_words=15)
            sellerId = fake.random_int(min=0, max=num_users-1)
            writerId = fake.random_int(min=0, max=num_users-1)
        print(f'{num_sellerReviews} seller reviews created')
    return


gen_users(num_users)
available_pids = gen_products(num_products)
gen_inventories(num_inventories, num_users, available_pids)
gen_orders(num_orders)
gen_cartItems(num_cartItems, num_users, num_orders, available_pids)
gen_productReviews(num_productReviews, available_pids, num_users)
gen_sellerReviews(num_sellerReviews, available_pids, num_users)