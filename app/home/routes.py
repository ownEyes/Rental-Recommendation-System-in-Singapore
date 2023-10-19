from flask import Flask, render_template, request, redirect, url_for, current_app
from app.home.forms import SurveyForm
from app.home import blueprint

@blueprint.route('/userin', methods=['GET', 'POST'])
def userin():
    form = SurveyForm()
    return render_template('userin.html', form=form)
    # return render_template('userin.html')

@blueprint.route('/recomm')
def recomm():
    # 这里返回 nav.html 的内容
    return render_template('recomm.html')

@blueprint.route('/submit_data', methods=['POST'])
def submit_data():
    form = SurveyForm()
    if form.validate_on_submit():
        minprice = form.minprice.data
        maxprice = form.maxprice.data
        location = form.location.data
        checkin = form.checkin.data
        checkout = form.checkout.data
        pr = form.p_rating.data
        lr = form.l_rating.data
        dr = form.d_rating.data
        r_type = form.roomtype.data
        #tr = form.t_rating.data
        day_diff = request.form["dayDifference"]
        public_facilities = form.public_facilities.data
        cooking_facilities = form.cooking_facilities.data
        interior_facilities = form.interior_facilities.data
        other_needs = form.other_needs.data
        #logger.debug("前端发送给后端的数据: minprice=%s,maxprice=%s,location=%s,checkin=%s,checkout=%s,p_rating=%s,l_rating=%s,d_rating=%s",minprice,maxprice,location,checkin,checkout,pr,lr,dr)
        print(minprice,maxprice,location,checkin,checkout,pr,lr,dr,r_type,day_diff,public_facilities,cooking_facilities,interior_facilities,other_needs)
        return redirect(url_for('home_blueprint.recomm')) 
        #return ("success") 
       
    else:
        current_app.logger.error("验证失败：%s", form.errors)
        return redirect(url_for('home_blueprint.userin'))
    # #if not form.validate_on_submit():
    #     #for field, errors in form.errors.items():
    #         #for error in errors:
    #             #print(f"Validation error in {field}: {error}")


