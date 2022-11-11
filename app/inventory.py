from flask import render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, IntegerField

from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('inventory', __name__)

class SearchForm(FlaskForm):
    types = ['fiction', 'nonfiction', 'drama', 'poetry']
    name = StringField('Name')
    description = StringField('Description')
    price = FloatField('Price')
    category = SelectField(label='Type', choices=[(state, state) for state in types])
    img_src = StringField('Image SRC')
    amount = IntegerField('Amount')
    add = SubmitField('Add')

class DeleteForm(FlaskForm):
    delete = SubmitField('Delist Item')

@bp.route('/inventory', methods=['GET', 'POST'])
def getKProducts():
    
    inventory = Inventory(1)
    form = SearchForm()
    delete_form = DeleteForm()
    
    if form.validate_on_submit() and form.add.data:
        
        product_info = {}
        product_info['name'] = form.name.data
        product_info['description'] = form.description.data
        product_info['price'] = form.price.data
        product_info['category'] = form.category.data
        product_info['img_src'] = form.img_src.data
        product_info['quantity'] = form.amount.data
        
        Inventory.add_product_to_catalog(product_info)
        inventory.add_product_to_inventory(product_info)
        updated_view = inventory.get_by_seller()
        return render_template('inventory.html', 
                               search_products=updated_view,
                               form=form,
                               delete_form=delete_form)
    
    # elif delete_form.validate_on_submit() and delete_form.delete.data:
        
    
    default_view = inventory.get_by_seller()
    return render_template('inventory.html', search_products=default_view, form=form)




