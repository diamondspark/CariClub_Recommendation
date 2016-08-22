from org import Org
from Users import User
import numpy as np
import MySQLdb
import pandas as pd
from Entity import entity
from OnClick import clickDetails
from scoreframe import Scoreframe


def showNonProfits(user,number_of_res_to_display):
     for i in range(0,number_of_res_to_display):
          cur.execute("SELECT name FROM org WHERE object = %s", (user.scoreframe.score_matrix.iloc[i,0],))
          print cur.fetchall()
     


conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123', db='cariclub_dev_mohit2')
#conn = MySQLdb.connect(host='cariclubprod1.cq6h9g2nwhxw.us-east-1.rds.amazonaws.com', port=3306, user='CariClubDB', passwd='CariClub682281kusai', db='cariclub_staging')

cur = conn.cursor()
##Creating a base dataframe with NPO id's and score
     #npo_df is dataframe of all NPO's on platform
cur.execute("SELECT org FROM org__nonprofit")
npo_df= pd.DataFrame.from_records(list(cur.fetchall()))



###Defining criterias on which similarity is to be considered####
sf1 = Scoreframe(npo_df,0)
sf1.addSimilarityMeasure('Interest_Score')
sf1.addSimilarityMeasure('Location_Score')
sf1.addSimilarityMeasure('Network_Score')



##o1= Org("ABC",0,001)
##print o1.objectId

# User ID will be provided by Web Service
# User ID for the user for whom we are making recommendation
uid = 709793 #Alexis Harmon
cur.execute("SELECT name FROM member WHERE object = %s",(uid,))
name= list(cur.fetchall())[0][0]

#Create User Object
u1 = User(uid,name,sf1)
## Make a .py to run these following methods in order.
## This new .py file should be executed on each user click
     #Suppose we are making recommendation for user u1 when
     #he's visiting Landon School (700020) page.
     #The information i.e. for which user the recommendation is to be made
     #and which NPO page is the user visiting (like Landon school in this example)
     #will be provided by backend.
a= clickDetails('700020',u1,cur)
showNonProfits(u1,10)
onPageLoad(u1,cur)






