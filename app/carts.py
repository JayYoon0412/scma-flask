from flask import render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('carts', __name__)

class SearchForm(FlaskForm):
    searchNumber = StringField('User ID')
    submit = SubmitField('Search')

@bp.route('/carts/search', methods=['GET', 'POST'])
def getCartItems():
    form = SearchForm()
    if form.validate_on_submit():
        cartItems = Cart.get_all_by_ownerid(int(form.searchNumber.data))
        return  render_template('cartSearch.html', search_cart=cartItems, form=form)
    return render_template('cartSearch.html', form=form)
