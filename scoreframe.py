import pandas as pd
import numpy as np
class Scoreframe:
     '''Common base class for all kinds of dataframes used.
     '''
     def __init__(self, score_matrix,base_score):
          '''Initialize the score matrix to keep track of similarity scores
             for NPO's. Every score matrix is initialized with 0 overall score
             for each NPO.
             score_matrix is pandas dataframe object.
             base_score is the value with which overall score is to be initiated
          '''
          zero = np.zeros(shape=(score_matrix[0].size,1))+base_score
          score_df = pd.DataFrame(zero,columns=['Overall Score'])
	  frames = [score_matrix,score_df]
          score_matrix = pd.concat(frames,axis=1)
          self.score_matrix = score_matrix
          
     def addSimilarityMeasure(sf,similarity_feature):
	 '''Takes in name of a similarity feature ('eg location')
	    and creates a column for it.
	    sf is scoreframe object
	 '''
	 zero = np.zeros(shape=(sf.score_matrix[0].size,1))
	 score_df = pd.DataFrame(zero,columns=[similarity_feature])
	 frames = [sf.score_matrix,score_df]
         sf.score_matrix = pd.concat(frames,axis=1)
		
     def updateScores(sf, similarity_feature,updatingRows,highScore):
          '''
           Takes in similarity feature name and python list of
           rows(NPO's) for which the score is to be updated.
           highScore is the numerical value by which score is
           to increased for given similarity feature.
          '''
          # Do to : Speed up the method by not using for loop.
          for i in range(0,len(updatingRows)):
               
               temp = sf.score_matrix[sf.score_matrix[0]==updatingRows[i][0]]
               sf.score_matrix.iat[temp.index[0],1]+=highScore
         
     def updateOverallScore(sf):
          # Dropping non-profit id column. Selects all columns starting at col2
          df_slice = sf.score_matrix.ix[:,1:]
          sf.score_matrix['Overall Score']= df_slice.sum(axis=1)
          sf.score_matrix = sf.score_matrix.sort('Overall Score', ascending=False)
          
	
	
	
