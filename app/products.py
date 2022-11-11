from flask import render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from datetime import datetime

from .models.product import Product
from .models.inventory import Inventory
from .models.review import Review

from flask import Blueprint
bp = Blueprint('products', __name__)

class SearchForm(FlaskForm):
    searchWord = StringField('')
    submit = SubmitField('search')


class AddReviewForm(FlaskForm):
    # selectType = SelectField("Select Review Types", choices=["Product", "Seller"])
    writerId = StringField('Your ID')
    # rated = StringField('Rated ID')
    rating = StringField('New rating')
    descp = StringField('Details')
    submit = SubmitField('Commit Changes')

@bp.route('/products/search', methods=['GET', 'POST'])
def getKProducts():
    form = SearchForm()
    if form.validate_on_submit():
        products = Product.get_k_expensive(int(form.searchNumber.data))
        return render_template('productSearch.html', search_products=products, form=form)
    return render_template('productSearch.html', form=form)

@bp.route('/products', methods=['GET', 'POST'])
def getProducts():
    form = SearchForm()
    totalNum = int(len(Product.get_all())/60)
    if form.validate_on_submit():
        keyword = '%'+form.searchWord.data+'%'
        products = Product.get_keywordProducts(keyword)
        return render_template('productsList.html', products=products, form=form, totalNum=totalNum)
    products = Product.get_all_paginate(offset=0)
    return render_template('productsList.html', products=products, form=form, totalNum=totalNum)

@bp.route('/products/page/<pageNumber>', methods=['GET', 'POST'])
def getProductsPage(pageNumber):
    form = SearchForm()
    totalNum = int(len(Product.get_all())/60)
    offset = (int(pageNumber)-1)*60
    if form.validate_on_submit():
        keyword = '%'+form.searchWord.data+'%'
        products = Product.get_keywordProducts(keyword)
        return render_template('productsList.html', products=products, form=form, totalNum=totalNum)
    products = Product.get_all_paginate(offset=offset)
    return render_template('productsList.html', products=products, form=form, totalNum=totalNum)

@bp.route('/products/filter/category/<category>')
def getByCategory(category):
    form = SearchForm()
    totalNum = int(len(Product.get_all())/60)
    products = Product.get_categoryProducts(category)
    return render_template('productsList.html', products=products, form=form, totalNum=totalNum)

@bp.route('/products/filter/price/<lowerBound>/<upperBound>')
def getByPriceRange(lowerBound, upperBound):
    form = SearchForm()
    totalNum = int(len(Product.get_all())/60)
    products = Product.get_priceProducts(lowerBound, upperBound)
    return render_template('productsList.html', products=products, form=form, totalNum=totalNum)

@bp.route('/products/filter/price/above/<lowerBound>')
def getAbovePriceProducts(lowerBound):
    form = SearchForm()
    totalNum = int(len(Product.get_all())/60)
    products = Product.get_priceAboveProducts(lowerBound)
    return render_template('productsList.html', products=products, form=form, totalNum=totalNum)

@bp.route('/products/sort/price/<order>')
def getSortedPriceProducts(order):
    form = SearchForm()
    totalNum = int(len(Product.get_all())/60)
    if order == 'asc':
        products = Product.get_lowPriceProducts()
    if order == 'desc':
        products = Product.get_highPriceProducts()
    return render_template('productsList.html', products=products, form=form, totalNum=totalNum)

@bp.route('/products/<productId>', methods=["GET", "POST"])
def getProductById(productId):
    product = Product.get(productId)
    inventories = Inventory.get_by_product(productId)
    reviews = Review.get_reviews_by_product(productId)
    newPost = AddReviewForm()

    if newPost.validate_on_submit():
        print("Hello")
        submitTime = datetime.now().replace(second=0, microsecond=0)
        Product.postProductReview(user=newPost.writerId.data, 
                                productId=productId, 
                                rating=newPost.rating.data, 
                                descp=newPost.descp.data, 
                                time=submitTime)
    return render_template('productDetail.html', product=product, inventories=inventories, reviews=reviews, updateForm=newPost)