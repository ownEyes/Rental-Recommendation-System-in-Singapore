from app.extension import db

class RentalHouse(db.Model):
    # __tablename__ = 'RentalHouse'
    HouseID = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    HouseName = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=False)
    neighbourhood_cleansed = db.Column(db.Text, nullable=False)
    neighbourhood_group_cleansed = db.Column(db.Text, nullable=False)
    picture_url = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.Text, nullable=False)
    accommodates= db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    minimum_months = db.Column(db.Integer, nullable=False)
    maximum_months = db.Column(db.Integer, nullable=False)
    distance_to_mrt = db.Column(db.Float, nullable=False)
    closest_mrt_name = db.Column(db.Text, nullable=False)
    closest_mrt_stop_id = db.Column(db.Text, nullable=False)
    closest_mall_distance = db.Column(db.Float, nullable=False)
    closest_mall_name = db.Column(db.Text, nullable=False)
    closest_mall_address = db.Column(db.Text, nullable=False)
    aircon = db.Column(db.Boolean, nullable=False)
    BBQ = db.Column(db.Boolean, nullable=False)
    gym = db.Column(db.Boolean, nullable=False)
    pool = db.Column(db.Boolean, nullable=False)
    dryer = db.Column(db.Boolean, nullable=False)
    Wifi = db.Column(db.Boolean, nullable=False)
    kitchen = db.Column(db.Boolean, nullable=False)
    Backyard = db.Column(db.Boolean, nullable=False)
    TV = db.Column(db.Boolean, nullable=False)
    refrigerator = db.Column(db.Boolean, nullable=False)
    Microwave = db.Column(db.Boolean, nullable=False)
    Oven = db.Column(db.Boolean, nullable=False)
    Pets = db.Column(db.Boolean, nullable=False)
    stove = db.Column(db.Boolean, nullable=False)
    fan = db.Column(db.Boolean, nullable=False)
    accommodates=db.Column(db.Integer, nullable=False)
    listing_url = db.Column(db.Text, nullable=False)
    review_scores_rating=db.Column(db.Float, nullable=False)
    review_scores_accuracy=db.Column(db.Float, nullable=False)
    review_scores_cleanliness=db.Column(db.Float, nullable=False)
    review_scores_checkin=db.Column(db.Float, nullable=False)
    review_scores_communication=db.Column(db.Float, nullable=False)
    review_scores_location=db.Column(db.Float, nullable=False)
    review_scores_value=db.Column(db.Float, nullable=False)


class Rating(db.Model):
    # __tablename__ = 'rating'
    ratingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer)
    listing_id = db.Column(db.Integer)
    rating = db.Column(db.Float)
    comments=db.Column(db.Text)

class Poi(db.Model):
    # __tablename__ = 'poi'
    POIid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name= db.Column(db.String)
    lat= db.Column(db.Float)
    lng= db.Column(db.Float)
    formatted_address= db.Column(db.String)
    store = db.Column(db.Boolean, nullable=False)
    food = db.Column(db.Boolean, nullable=False)
    health = db.Column(db.Boolean, nullable=False)
    restaurant = db.Column(db.Boolean, nullable=False)
    hospital = db.Column(db.Boolean, nullable=False)
    lodging = db.Column(db.Boolean, nullable=False)
    finance = db.Column(db.Boolean, nullable=False)
    cafe = db.Column(db.Boolean, nullable=False)
    convenience_store = db.Column(db.Boolean, nullable=False)
    clothing_store = db.Column(db.Boolean, nullable=False)
    atm = db.Column(db.Boolean, nullable=False)
    shopping_mall = db.Column(db.Boolean, nullable=False)
    grocery_or_supermarket = db.Column(db.Boolean, nullable=False)
    home_goods_store = db.Column(db.Boolean, nullable=False)
    school = db.Column(db.Boolean, nullable=False)
    bakery = db.Column(db.Boolean, nullable=False)
    beauty_salon = db.Column(db.Boolean, nullable=False)
    transit_station = db.Column(db.Boolean, nullable=False)
    place_of_worship = db.Column(db.Boolean, nullable=False)
    pharmacy = db.Column(db.Boolean, nullable=False)
    meal_takeaway = db.Column(db.Boolean, nullable=False)
    furniture_store = db.Column(db.Boolean, nullable=False)
    tourist_attraction = db.Column(db.Boolean, nullable=False)
    secondary_school = db.Column(db.Boolean, nullable=False)
    supermarket = db.Column(db.Boolean, nullable=False)
    doctor = db.Column(db.Boolean, nullable=False)
    shoe_store = db.Column(db.Boolean, nullable=False)
    dentist = db.Column(db.Boolean, nullable=False)
    jewelry_store = db.Column(db.Boolean, nullable=False)
    church = db.Column(db.Boolean, nullable=False)
    bank = db.Column(db.Boolean, nullable=False)
    primary_school = db.Column(db.Boolean, nullable=False)
    electronics_store = db.Column(db.Boolean, nullable=False)
    gym = db.Column(db.Boolean, nullable=False)
    spa = db.Column(db.Boolean, nullable=False)
    car_repair = db.Column(db.Boolean, nullable=False)
    pet_store = db.Column(db.Boolean, nullable=False)
    bus_station = db.Column(db.Boolean, nullable=False)
    university = db.Column(db.Boolean, nullable=False)
    park = db.Column(db.Boolean, nullable=False)
    general_contractor = db.Column(db.Boolean, nullable=False)
    subway_station = db.Column(db.Boolean, nullable=False)
    real_estate_agency = db.Column(db.Boolean, nullable=False)
    florist = db.Column(db.Boolean, nullable=False)
    hair_care = db.Column(db.Boolean, nullable=False)
    department_store = db.Column(db.Boolean, nullable=False)
    hardware_store = db.Column(db.Boolean, nullable=False)
    car_dealer = db.Column(db.Boolean, nullable=False)
    veterinary_care = db.Column(db.Boolean, nullable=False)
    travel_agency = db.Column(db.Boolean, nullable=False)
    bicycle_store = db.Column(db.Boolean, nullable=False)
    book_store = db.Column(db.Boolean, nullable=False)
    laundry = db.Column(db.Boolean, nullable=False)
    plumber = db.Column(db.Boolean, nullable=False)
    meal_delivery = db.Column(db.Boolean, nullable=False)
    lawyer = db.Column(db.Boolean, nullable=False)
    parking = db.Column(db.Boolean, nullable=False)
    mosque = db.Column(db.Boolean, nullable=False)
    physiotherapist = db.Column(db.Boolean, nullable=False)
    art_gallery = db.Column(db.Boolean, nullable=False)
    insurance_agency = db.Column(db.Boolean, nullable=False)
    bar = db.Column(db.Boolean, nullable=False)
    museum = db.Column(db.Boolean, nullable=False)
    storage = db.Column(db.Boolean, nullable=False)
    movie_theater = db.Column(db.Boolean, nullable=False)
    moving_company = db.Column(db.Boolean, nullable=False)
    liquor_store = db.Column(db.Boolean, nullable=False)
    gas_station = db.Column(db.Boolean, nullable=False)
    electrician = db.Column(db.Boolean, nullable=False)
    car_rental = db.Column(db.Boolean, nullable=False)
    locksmith = db.Column(db.Boolean, nullable=False)
    car_wash = db.Column(db.Boolean, nullable=False)
    post_office = db.Column(db.Boolean, nullable=False)
    embassy = db.Column(db.Boolean, nullable=False)
    night_club = db.Column(db.Boolean, nullable=False)
    fire_station = db.Column(db.Boolean, nullable=False)
    amusement_park = db.Column(db.Boolean, nullable=False)
    library = db.Column(db.Boolean, nullable=False)
    hindu_temple = db.Column(db.Boolean, nullable=False)
    local_government_office = db.Column(db.Boolean, nullable=False)
    funeral_home = db.Column(db.Boolean, nullable=False)
    bowling_alley = db.Column(db.Boolean, nullable=False)
    cemetery = db.Column(db.Boolean, nullable=False)
    aquarium = db.Column(db.Boolean, nullable=False)
    roofing_contractor = db.Column(db.Boolean, nullable=False)
    stadium = db.Column(db.Boolean, nullable=False)
    painter = db.Column(db.Boolean, nullable=False)
    courthouse = db.Column(db.Boolean, nullable=False)
    drugstore = db.Column(db.Boolean, nullable=False)
    campground = db.Column(db.Boolean, nullable=False)
    accounting = db.Column(db.Boolean, nullable=False)
    airport = db.Column(db.Boolean, nullable=False)
    zoo = db.Column(db.Boolean, nullable=False)
    casino = db.Column(db.Boolean, nullable=False)
    synagogue = db.Column(db.Boolean, nullable=False)
    premise = db.Column(db.Boolean, nullable=False)
    taxi_stand = db.Column(db.Boolean, nullable=False)
    police = db.Column(db.Boolean, nullable=False)
    light_rail_station = db.Column(db.Boolean, nullable=False)
    city_hall = db.Column(db.Boolean, nullable=False)
    train_station = db.Column(db.Boolean, nullable=False)
    natural_feature = db.Column(db.Boolean, nullable=False)
    subpremise = db.Column(db.Boolean, nullable=False)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    popularity_based = db.Column(db.String, nullable=True)
    content_based = db.Column(db.String, nullable=True)
    content_based_diversity = db.Column(db.String, nullable=True)
    matrix_factorization = db.Column(db.String, nullable=True)
    
    def __init__(self, user_id, popularity_based=None, content_based=None, content_based_diversity=None, matrix_factorization=None):
        self.user_id = user_id
        self.popularity_based = popularity_based
        self.content_based = content_based
        self.content_based_diversity = content_based_diversity
        self.matrix_factorization = matrix_factorization
    
    def save(self):
        db.session.add(self)
        db.session.commit()