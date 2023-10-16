from flask import Flask, render_template, request, redirect, url_for
from app.home.forms import SurveyForm
from app.home import blueprint

@blueprint.route('/userInput', methods=['GET', 'POST'])
def index():
    form = SurveyForm()

    if form.validate_on_submit()and request.method == 'POST':
        minprice = form.minprice.data
        maxprice = form.maxprice.data
        imp_p = form.imp_p.data
        imp_l = form.imp_l.data
        imp_d = form.imp_d.data
        location=form.location.data
        startdate=form.startdate.data
        enddate=form.enddate.data
        
        print(minprice)
        print(maxprice)
        print(location)
        print(startdate)
        print(enddate)
        return redirect(url_for('output_html'))

    return render_template('try.html', form=form)

    

@blueprint.route('/output')
def output_html():
    return render_template('output.html')