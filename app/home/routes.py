from flask import Flask, render_template, request, redirect, url_for, current_app,jsonify
from app.home.forms import SurveyForm, FormData
from app.home import blueprint
from app.home.utils import *
from app.services.DataProcessing import *
from app.services.Recommender import Recommender
from app.services.DataManger import DataManager
from app.services.MapDrawer import MapDrawer

@blueprint.route('/userin', methods=['GET', 'POST'])
def userin():
    form = SurveyForm()
    return render_template('userin.html', form=form)

# def get_data_from_database():
#     # 在这里获取数据库中的数据，这里假设 data 是一个列表
#     data =[ [["BBQ","Pool","Backyard"],["Kitchen", "Refrigerator","Microwave"],["Aircon","Dryer","Wifi"],["Pets"]],[["BBQ","Gym","Pool","Backyard"],["Kitchen", "Oven", "Stoven","Refrigerator","Microwave"],["Aircon","Dryer","Wifi","TV","Fan"],["Pets"]],[["BBQ","Pool","Backyard"],["Kitchen", "Refrigerator","Microwave"],["Aircon","Dryer","Wifi"],["Pets"]] ]  # 从数据库中获取的数据
#     return data
@blueprint.route('/get_data', methods=['GET'])
def get_data():
    lists=current_app.recommender.get_result()
    recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
    data = recomm_list.apply(df_to_amenities, axis=1).tolist()

    return jsonify(data=data)



@blueprint.route('/recomm')
def recomm():
    current_app.recommender.test_recommend()
    lists=current_app.recommender.get_result()
    recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
    rents=[]
    for row_num, row in enumerate(recomm_list.itertuples(index=False), start=1):
        dic=df_to_display(row_num, row)
        rents.append(dic)
    
    return render_template('recomm.html', rents=rents)

@blueprint.route('/submit_data', methods=['POST',"GET"])
def submit_data():
    form = SurveyForm()
    if form.validate_on_submit():
        form_data=FormData(
            minprice = int(form.minprice.data),
            maxprice = int(form.maxprice.data),
            location = get_geocoding(form.location.data),
            checkin = form.checkin.data,
            checkout = form.checkout.data,
            p_rating = float(form.p_rating.data),
            l_rating = float(form.l_rating.data),
            t_rating = float(form.t_rating.data),
            a_rating = float(form.a_rating.data),
            roomtype = form.roomtype.data,
            #tr = form.t_rating.data
            vector=[],
            desired_month = int(request.form["dayDifference"])//30,
            public_facilities = form.public_facilities.data,
            cooking_facilities = form.cooking_facilities.data,
            interior_facilities = form.interior_facilities.data,
            other_needs = form.other_needs.data
        )
        current_app.map_drawer.draw_target(form_data.location[0],form_data.location[1],2,form.location.data)
        weight_vector,user_vector_w,data_vector=form_to_vecs(form_data)
        current_app.recommender.set_param(weight_vector,user_vector_w,data_vector)
        #logger.debug("前端发送给后端的数据: minprice=%s,maxprice=%s,location=%s,checkin=%s,checkout=%s,p_rating=%s,l_rating=%s,t_rating=%s",minprice,maxprice,location,checkin,checkout,pr,lr,dr)
        # print(minprice,maxprice,location,checkin,checkout,pr,lr,tr,ar,r_type,day_diff,public_facilities,cooking_facilities,interior_facilities,other_needs)
        return redirect(url_for('home_blueprint.recomm')) 
        #return ("success") 
       
    else:
        current_app.logger.error("验证失败：%s", form.errors)
        return redirect(url_for('home_blueprint.userin'))

@blueprint.route('/map/<int:recomm_idx>', methods=['GET'])
def draw_map(recomm_idx):
    
    lists=current_app.recommender.get_result()
    recommendations=current_app.data_manager.get_recommends(lists,"HouseID")
    if recomm_idx < 1 or recomm_idx > len(recommendations):
        return "Place not found", 404
    place = recommendations.iloc[recomm_idx - 1]
    m=current_app.map_drawer.add_to_map(place["latitude"],place["longitude"],2,place["HouseName"],place["listing_url"],place["picture_url"])

    return m.get_root().render()