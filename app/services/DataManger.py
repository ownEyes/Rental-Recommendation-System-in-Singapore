import pandas as pd
from flask import current_app
from typing import List, Optional, Type
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from flask_sqlalchemy import Model
# from app import db
from app.authentication.models import User
from app.home.models import Rating, RentalHouse, Poi, Recommendation



class DataManager:
    def __init__(self):
        self.db = current_app.extensions['sqlalchemy'].db
        # self.Model = self.db.Model

    def get_by_id(self, model: Type[Model], id: int) -> Optional[Model]:
        """Get a single object by its ID."""
        try:
            return self.db.session.query(model).filter_by(id=id).first()
        except Exception as e:
            print(f"Error getting {model.__name__} by ID: {e}")
            return None

    def add(self, obj: Model) -> bool:
        """Add an object to the database."""
        try:
            self.db.session.add(obj)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error adding object: {e}")
            self.db.session.rollback()
            return False

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.get_by_id(User, user_id)

    def get_rating(self, user_id: int) -> List[Rating]:
        """Get a poi by ID."""
        return self.get_by_id(Rating, user_id)

    def get_poi(self, poi_id: int) -> Optional[Poi]:
        """Get a poi by ID."""
        return self.get_by_id(Poi, poi_id)

    def get_df_by_ids(self, model: Type[DeclarativeMeta], ids: List[int], id_column_name: str) -> pd.DataFrame:
        """Get records by a list of IDs."""
        query = self.db.session.query(model).filter(getattr(model, id_column_name).in_(ids))
        df = pd.read_sql(query.statement, self.db.engine)
        return df

    def get_recommends(self, house_ids: List[int], id_column_name: str = 'id') -> pd.DataFrame:
        """Get rentalhouses by a list of IDs."""
        return self.get_df_by_ids(RentalHouse, house_ids, id_column_name)
    
    # def get_columns_by_ids(self, model: db.Model, ids: List[int], columns: List[str]) -> pd.DataFrame:
    #     """Get specific columns of records by a list of IDs."""
    #     query = self.db.session.query(*[getattr(model, column) for column in columns]).filter(model.id.in_(ids))
    #     df = pd.read_sql(query.statement, self.db.engine)
    #     return df

    # def get_rentalhouse_columns(self, house_ids: List[int], columns: List[str]) -> pd.DataFrame:
    #     """Get specific columns of rentalhouses by a list of IDs."""
    #     return self.get_columns_by_ids(RentalHouse, house_ids, columns)
    
    def get_df_from_columns(self, model: Type[DeclarativeMeta], columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        query = self.db.session.query(*[getattr(model, column) for column in columns])
        df = pd.read_sql(query.statement, self.db.engine)
        return df
    
    def get_houses_df(self, columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        return self.get_df_from_columns(RentalHouse, columns)
    
    def get_ratings_df(self, columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        return self.get_df_from_columns(Rating, columns)
    
    def get_pois_df(self, columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        return self.get_df_from_columns(Poi, columns)
    
    def update_object_by_id(self, model: Model, primary_key_name: str, object_id: int, **kwargs) -> bool:
        """Update an object in the database by ID."""
        try:

            obj = self.db.session.query(model).filter(getattr(model, primary_key_name) == object_id).one()
            
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    print(f"Warning: {model.__name__} does not have attribute {key}")
            
            self.db.session.commit()
            return True
        except NoResultFound:
            print(f"{model.__name__} with {primary_key_name} {object_id} not found.")
            return False
        except Exception as e:
            print(f"Error updating {model.__name__}: {e}")
            self.db.session.rollback()
            return False

    def update_recommends_by_uid(self, user_id: int, updates: Dict[str, str]) -> bool:
        """Update a user's recommendation results in the database by user ID."""
        return self.update_object_by_id(Recommendation, 'userID', user_id, **updates)

    def update_rating_by_uid(self, user_id: int, updates: Dict[str, str]) -> bool:
        """Update a user's rating results in the database by user ID."""
        return self.update_object_by_id(Rating, 'userID', user_id, **updates)
