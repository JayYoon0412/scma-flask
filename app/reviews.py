from flask import render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, Form, SelectField
from datetime import datetime

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__) # ? 

class SearchForm(FlaskForm):
    selectType = SelectField("Select Review Types", choices=["All", "Product", "Seller"])
    searchNumber = StringField('User ID')
    submit = SubmitField('Search')

class UpdateReviewForm(FlaskForm):
    selectType = SelectField("Select Review Types", choices=["Product", "Seller"])
    writerId = StringField('Your ID')
    rated = StringField('Rated ID')
    rating = StringField('New rating')
    descp = StringField('Details')
    submit = SubmitField('Commit Changes')

    

# need to change page route
# @bp.route('/products/search', methods=['GET', 'POST'])
@bp.route('/reviews/search', methods=['GET', 'POST'])
def main():
    form = SearchForm()
    updateForm = UpdateReviewForm()
    # mainForm = MainForm()
    if form.validate_on_submit() and form.searchNumber.data:
        rating = Review.get_top_review_by(int(form.searchNumber.data), form.selectType.data)
        return render_template('reviewSearch.html', search_review=rating, form=form, updateForm=updateForm, status = 1)

    if updateForm.validate_on_submit():
        dt = datetime.now().replace(second=0, microsecond=0)
        print(dt)
        Review.updateTable(userId = updateForm.writerId.data,
                           rating = updateForm.rating.data,
                           ratedId = updateForm.rated.data,
                           descp = updateForm.descp.data,
                           database = updateForm.selectType.data)

    return render_template('reviewSearch.html', form=form, updateForm=updateForm)
    

# @bp.route('/reviews/search/modal')
# def updateReviewInModal():
#     return render_template("reviewModal.html")