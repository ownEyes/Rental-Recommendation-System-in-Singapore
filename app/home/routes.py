from flask import Flask, render_template, request, redirect, url_for, current_app,jsonify
from app.home.forms import SurveyForm
from app.services.DataManger import FormData
from app.home import blueprint
# from app.home.utils import *
from app.services.DataProcessing import *
from app.services.Recommender import Recommender
from app.services.DataManger import DataManager
from app.services.MapDrawer import MapDrawer

@blueprint.route('/userin', methods=['GET', 'POST'])
def userin():
    form = SurveyForm()
    return render_template('userin.html', form=form)

@blueprint.route('/get_data', methods=['GET'])
def get_data():
    lists=current_app.recommender.get_result()
    recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
    data = recomm_list.apply(df_to_amenities, axis=1).tolist()

    return jsonify(data=data)



@blueprint.route('/recomm')
def recomm():
    current_app.recommender.recommend()
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
        day_difference = int(request.form.get("dayDifference", 0)) // 30
        form_data = FormData.from_form(form, day_difference)
        current_app.map_drawer.draw_target(form_data.location[0],form_data.location[1],2,form.location.data)
        weight_vector,user_vector_w,data_vector=form_to_vecs(form_data)
        current_app.recommender.set_param(weight_vector,user_vector_w,data_vector)
        return redirect(url_for('home_blueprint.recomm')) 
       
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