from flask import render_template, request, redirect, url_for, current_app,jsonify
import flask_wtf as wtf
from flask_login import current_user,login_required
from folium.plugins import MarkerCluster
import folium
from app.home.models import Rating
from app.home.forms import SurveyForm,CommentForm,QueryForm
from app.services.DataManger import FormData
from app.home import blueprint
# from app.home.utils import *
# from app.services.DataProcessing import *
from app.services.Convert import *
from app.extension import db
from app.home.mywordcloud import *

# @blueprint.route('/userin', methods=['GET', 'POST'])
# @login_required
# def userin():
#     form = SurveyForm()
#     return render_template('userin.html', form=form)

# @blueprint.route('/get_data', methods=['GET'])
# @login_required
# def get_data():
#     lists=current_app.recommender.get_result()
#     recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
#     data = recomm_list.apply(df_to_amenities, axis=1).tolist()

#     return jsonify(data=data)



# @blueprint.route('/recomm')
# @login_required
# def recomm():
#     user_id = current_user.get_id()
#     current_app.recommender.currUID=user_id
#     checker=Rating.query.filter_by(userID=user_id).first()
#     if checker:
#         print("rating exists")
#         current_app.recommender.mode="hybrid"
#         ratingInfo=get_ratings()
#         current_app.recommender.rating=ratingInfo
#     else:
#         print("rating not exists")
#         current_app.recommender.mode="content_based"
#     current_app.recommender.recommend()
#     lists=current_app.recommender.get_result()
#     recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
#     rents=[]
#     form = CommentForm()
#     for row_num, row in enumerate(recomm_list.itertuples(index=False), start=1):
#         dic=df_to_display(row_num, row)
#         form = CommentForm()  
#         dic['form'] = form  
#         dic['recomm_idx'] = row_num  
#         rents.append(dic)
    
#     return render_template('recomm.html', rents=rents,form=form)

# @blueprint.route('/submit_data', methods=['POST',"GET"])
# @login_required
# def submit_data():
#     form = SurveyForm()
#     if form.validate_on_submit():
#         day_difference = int(request.form.get("dayDifference", 0)) // 30
#         form_data = FormData.from_form(form, day_difference)
#         current_app.map_drawer.draw_target(form_data.location[0],form_data.location[1],2,form.location.data)
#         weight_vector,user_vector_w,data_vector=form_to_vecs(form_data)
#         current_app.recommender.set_param(weight_vector,user_vector_w,data_vector)
#         return redirect(url_for('home_blueprint.recomm')) 
       
#     else:
#         current_app.logger.error("验证失败：%s", form.errors)
#         return redirect(url_for('home_blueprint.userin'))

# @blueprint.route('/map/<int:recomm_idx>', methods=['GET'])
# @login_required
# def draw_map(recomm_idx):
    
#     lists=current_app.recommender.get_result()
#     recommendations=current_app.data_manager.get_recommends(lists,"HouseID")
#     if recomm_idx < 1 or recomm_idx > len(recommendations):
#         return "Place not found", 404
#     place = recommendations.iloc[recomm_idx - 1]
#     m=current_app.map_drawer.add_to_map(place["latitude"],place["longitude"],2,place["HouseName"],place["listing_url"],place["picture_url"])

#     return m.get_root().render()

# @blueprint.route('/comment/<int:recomm_idx>', methods=['GET','POST'])
# @login_required
# def get_comment(recomm_idx):
#     lists=current_app.recommender.get_result()
#     if recomm_idx < 1 or recomm_idx > len(lists):
#         return "Place not found", 404
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = form.comment.data
#         rating=current_app.rating_estimator.comments_to_rating(comment)
#         user_id = current_user.get_id()
#         record=Rating(userID=user_id,listing_id=lists[recomm_idx - 1],rating=rating,comments=comment)
#         db.session.add(record)
#         db.session.commit()
#         rating_df=get_ratings()
#         current_app.recommender.model_update(rating_df)
#         return redirect(url_for('home_blueprint.recomm')) 
#     return render_template('rent_block.html', form=form,wtf=wtf,recomm_idx=recomm_idx)


user_input_data={}

@blueprint.route('/userin', methods=['GET', 'POST'])
@login_required
def userin():
    form = QueryForm()
    return render_template('userin.html', form=form)


@blueprint.route('/submit_data', methods=['POST',"GET"])
@login_required
def submit_data():
    form = QueryForm()
    if form.validate_on_submit():
        user_input_data['minmonth'] = form.minmonth.data
        user_input_data['maxmonth'] = form.maxmonth.data
        user_input_data['region'] = form.region.data
        user_input_data['postcode'] = form.postcode.data
        user_input_data['numbedrooms'] = form.numbedrooms.data
        user_input_data['numbeds'] = form.numbeds.data
        user_input_data['numbathrooms'] = form.numbathrooms.data
        user_input_data['bathroomtype'] = form.bathroomtype.data
        user_input_data['roomtype'] = form.roomtype.data
        user_input_data['accommodates'] = form.accommodates.data
        user_input_data['public_facilities'] = ', '.join(form.public_facilities.data)
        user_input_data['cooking_facilities'] = ', '.join(form.cooking_facilities.data)
        user_input_data['interior_facilities'] = ', '.join(form.interior_facilities.data)
        user_input_data['other_needs'] = ', '.join(form.other_needs.data)
        #logger.debug("前端发送给后端的数据: minprice=%s,maxprice=%s,location=%s,checkin=%s,checkout=%s,p_rating=%s,l_rating=%s,t_rating=%s",minprice,maxprice,location,checkin,checkout,pr,lr,dr)
        # print(user_input_data)
        amv=amenities_to_vector([form.public_facilities.data,form.cooking_facilities.data,form.interior_facilities.data,form.other_needs.data])
        geocoding=get_geocoding(user_input_data['region'],user_input_data['postcode'])
        mrt_dis,mrt=cal_mrt_dis(geocoding)
        mall_dis,mall=cal_mall_dis(geocoding)
        user_input_data['latitude']=geocoding[0]
        user_input_data['longitude']=geocoding[1]
        user_input_data['mrt_dis']=mrt_dis
        user_input_data['mrt_name']=mrt['name']
        user_input_data['stop_id']=mrt['stop_id']
        user_input_data['mall_dis']=mall_dis
        user_input_data['mall_name']=mall['name']
        user_input_data['mall_adress']=mall['formatted_address']
        input = { 'neighbourhood_group_cleansed':user_input_data['region'], 'latitude':geocoding[0], 'longitude':geocoding[1], 'room_type':user_input_data['roomtype'],
                 'minimum_months':int(user_input_data['minmonth']), 'maximum_months':int(user_input_data['maxmonth']),
                'distance_to_mrt':mrt_dis, 'closest_mall_distance':mall_dis, 'conditioning':amv[0], 'BBQ':amv[1], 'gym':amv[2], 'pool':amv[3], 'dryer':amv[4],
                'Wifi':amv[5], 'kitchen':amv[6], 'Backyard':amv[7], 'TV':amv[8], 'refrigerator':amv[9], 'Microwave':amv[10], 'Oven':amv[11], 'Pets':amv[12], 'stove':amv[13], 'fan':amv[14], 'accommodates':int(user_input_data['accommodates']),
                'total_bedrooms':int(user_input_data['numbedrooms']), 'total_beds':int(user_input_data['numbeds']),
                'total_baths':float(user_input_data['numbathrooms']), 'bath_type':user_input_data['bathroomtype'], }
        current_app.forcaster.load_input(input)
        data,input_vec=get_house_data(input)
        current_app.recommender.content_based_recommendation(data,input_vec)
        user_input_data['price']=current_app.forcaster.predict()
        return redirect(url_for('home_blueprint.mapgenerate')) 
        #return ("success") 
       
    # else:
    #     logger.error("验证失败：%s", form.errors)
    #     return redirect(url_for('userin'))
    # #if not form.validate_on_submit():
    #     #for field, errors in form.errors.items():
    #         #for error in errors:
    #             #print(f"Validation error in {field}: {error}")
@blueprint.route('/priadv')
@login_required
def priadv():
    result=user_input_data['price']
    feature_imp=current_app.forcaster.get_feature_importance()
    file_path=current_app.config['WORDCLOUD_PATH']
    generate_wordcloud(process_feature_imp(feature_imp),file_path)
    
    predadv={
        'price':'S$ '+str(int(result))+' /month',
        'cloud_img':'./static/img/wordcloud.png'
        }

    return render_template('predic&advan.html',predadv=predadv)



@blueprint.route('/mapgenerate')
@login_required
def mapgenerate():
    
    columns = ['name','details', 'region', 'accommodation_info', 'room_type', 'public_facilities', 'cooking_facilities',
               'interior_facilities', 'other_needs', 'price', 'distance_to_mrt', 'mall_info', 'latitude', 'longitude']


    userin = ['The information of your own residents',str(user_input_data.get('numbedrooms', '')+' bedroom · '+user_input_data.get('numbeds', '')+' bed · ' +user_input_data.get('numbathrooms', '') +' '+user_input_data.get('bathroomtype', '')+  ' bath'), user_input_data.get('region', ''),str(user_input_data.get('accommodates', '')+ ' accommodate'), user_input_data.get('roomtype', ''),
              user_input_data.get('public_facilities', ''), user_input_data.get('cooking_facilities', ''), user_input_data.get('interior_facilities', ''), user_input_data.get('other_needs', ''), 'S$ '+str(int(user_input_data.get('price', '')))+' /month', 
              str(int(user_input_data.get('mrt_dis', '')*1000))+'m to '+str(user_input_data.get('stop_id', ''))+' '+str(user_input_data.get('mrt_name', '')),
              str(int(user_input_data.get('mall_dis', '')*1000))+'m to '+str(user_input_data.get('mall_name', ''))+'('+str(user_input_data.get('mall_adress', ''))+')', user_input_data.get('latitude', 1.352083),
              user_input_data.get('longitude', 103.819836)]
    
    user_df = pd.DataFrame([userin], columns=columns)
    
    lists= current_app.recommender.get_similar()
    recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
    s=[]
    for row_num, row in enumerate(recomm_list.itertuples(index=False), start=1):
        s1=house_to_draw(row_num, row)
        s.append(s1)
    
    df = pd.DataFrame(s, columns=columns)

    mapdf1 = folium.Map(location=[1.34, 103.96], zoom_start=10)
    mapdf1_rooms_map = MarkerCluster().add_to(mapdf1)

    labels = zip(df.name, df.details, df.region, df.accommodation_info, df.room_type, df.public_facilities,
                 df.cooking_facilities, df.interior_facilities, df.other_needs, df.price, df.distance_to_mrt, df.mall_info)
    for lat, lon, label in zip(df.latitude, df.longitude, labels):
        simi_labels=f'''
        <div class="custom-popup">
            <h3>{label[0]}</h3>
            <p>{label[1]}</p>
            <p>{label[2]}</p>
            <p>{label[3]}</p>
            <p>{label[4]}</p>
            <p>{next(iter(label[5]), " ")}</p>
            <p>{next(iter(label[6]), " ")}</p>
            <p>{next(iter(label[7]), " ")}</p>
            <p>{next(iter(label[8]), " ")}</p>
            <p>{label[9]}</p>
            <p>{label[10]}</p>
            <p>{label[11]}</p>
        </div>
    '''
        iframe0 = folium.IFrame(html=simi_labels, width=300, height=150)
        popup0 = folium.Popup(iframe0, max_width=2650)
        folium.Marker(
            location=[lat, lon], 
            icon=folium.Icon(icon='home'), 
            popup=popup0
            ).add_to(mapdf1_rooms_map)

    user_lat, user_lon = user_df.latitude.iloc[0], user_df.longitude.iloc[0]
    user_public=user_df.public_facilities.iloc[0]
    user_cooking=user_df.cooking_facilities.iloc[0]
    user_interior=user_df.interior_facilities.iloc[0]
    user_other=user_df.other_needs.iloc[0]
    
    user_label = f'''
        <div class="custom-popup">
            <h3>{user_df.name.iloc[0]}</h3>
            <p>{user_df.details.iloc[0]}</p>
            <p>{user_df.region.iloc[0]}</p>
            <p>{user_df.accommodation_info.iloc[0]}</p>
            <p>{user_df.room_type.iloc[0]}</p>
            <p>{user_public}</p>
            <p>{user_cooking}</p>
            <p>{user_interior}</p>
            <p>{user_other}</p>
            <p>{user_df.price.iloc[0]}</p>
            <p>{user_df.distance_to_mrt.iloc[0]}</p>
            <p>{user_df.mall_info.iloc[0]}</p>
            <!-- Add other user label information here -->
        </div>
    '''
    iframe1 = folium.IFrame(html=user_label, width=300, height=150)
    popup1 = folium.Popup(iframe1, max_width=2650)
    folium.Marker(
        location=[user_lat, user_lon],
        icon=folium.Icon(color='red', icon='home'),
        popup=popup1
    ).add_to(mapdf1_rooms_map)

    

    mapdf1.add_child(mapdf1_rooms_map)
    # map_html = mapdf1.get_root().render()
    # mapdf1.save("templates/map.html")

    # return render_template('map.html',map_html=map_html)
    return mapdf1.get_root().render()
