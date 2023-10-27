import random
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from collections import defaultdict
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise import Reader

from app.home.forms import FormData

class Recommender:
    def __init__(self, MF_model=None,recommend_default_topn=10,alpha=0.5): 
        # self.current_uid=uid
        self.matrix_factorization_model = MF_model
        self.recommend_num=recommend_default_topn
        self.popularity_recommend_result=None
        self.weighted_content_based_recommend_result=None
        self.content_based_recommend_result=None
        self.alpha=alpha
        self.data=None
        self.user_preference=None
        self.weight_vector=None
    
    def popularity_based_recommendation(self, df,rating_cols):
        df = df.assign(total_rating=df[rating_cols].sum(axis=1))
        sorted_df = df.sort_values(by='total_rating', ascending=False)
        max_total_rating = sorted_df['total_rating'].max()
        topn_candidates = sorted_df[sorted_df['total_rating'] == max_total_rating]
        
        if len(topn_candidates) <= self.recommend_num:
            self.popularity_recommend_result = topn_candidates
        else:
            sampled_rows = random.sample(topn_candidates.index.tolist(), self.recommend_num)
            self.popularity_recommend_result = df.loc[sampled_rows]
        pass

    def weighted_content_based_recommendation(self, data,user_preference,weight_vector):
        # data_vector=data.drop('HouseID',axis=1).values
        if 'HouseID' in data.columns:
            data_process = data.drop('HouseID', axis=1)

        if 'weighted_similarity' in data_process.columns:
            data_process = data_process.drop('weighted_similarity', axis=1)

        data_vector = data_process.values
        weighted_data_vector = data_vector * weight_vector
        user_preference = user_preference.reshape(1, -1)
        weighted_user_vector =  user_preference * weight_vector
        weighted_similarities = cosine_similarity(weighted_user_vector, weighted_data_vector)
        data['weighted_similarity'] = weighted_similarities.transpose()
        self.weighted_content_based_recommend_result = data.sort_values(by='weighted_similarity', ascending=False) 
        pass
    def content_based_recommendation(self, data,user_preference):
        similarities = cosine_similarity(user_preference, data)
        data['similarity'] = similarities.transpose()
        data['similarity']= similarities.transpose()
        self.content_based_recommend_result = data.nlargest(self.recommend_num, 'similarity')
        pass

    def content_based_recommendation_with_diversity(self, data,user_preference):
        self.weighted_content_based_recommendation(data,user_preference)
        
        pass
    
    def matrix_factorization_recommendation(self, user_id, df):
        if 'user_id' not in df.columns or 'item_id' not in df.columns:
            raise ValueError("DataFrame must contain 'user_id' and 'item_id' columns")
    
        item_ids = df['item_id'].unique()
        predictions = defaultdict(float)
        
        for item_id in item_ids:
            predictions[item_id] = self.matrix_factorization_model.predict(user_id, item_id, verbose=True).est
        
        recommended_items = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        self.matrix_factorization_recommendation=[item[0] for item in recommended_items]
        pass
    
    def hybrid_recommendation(self,user_id, matrix_factorization_model):
        """
        Hybrid recommendation function that combines matrix factorization and content-based recommendations.
        
        :param user_id: ID of the user
        :param item_id: ID of the item
        :param matrix_factorization_model: Trained matrix factorization model
        :param content_based_model: Trained content-based model
        :param alpha: Weight for matrix factorization recommendation score (0 <= alpha <= 1)
        :return: Hybrid recommendation score
        """
        # Get the matrix factorization recommendation score

        pass
    def set_param(self,weight_vector,user_vector_w,data_vector):
        print("Setting parameters:")
        print("Weight Vector:", weight_vector)
        print("User Vector W:", user_vector_w)
        print("Data Vector:", data_vector)
        self.data=data_vector
        self.user_preference=user_vector_w
        self.weight_vector=weight_vector          
    def test_recommend(self):
        print("Data:", self.data)
        print("User Preference:", self.user_preference)
        print("Weight Vector:", self.weight_vector)
        self.weighted_content_based_recommendation(self.data,self.user_preference,self.weight_vector)
    
    def get_result(self):
        result=self.weighted_content_based_recommend_result.head(self.recommend_num)
        return result['HouseID'].tolist()