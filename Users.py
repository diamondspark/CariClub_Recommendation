import json
import requests
import MySQLdb
import pandas as pd
from scoreframe import Scoreframe
class User:
     '''Common base class for all users.
        Each user object must be a singleton object. Since once created,
        it cannot be reinitaialized with new dataframe.
        Dataframe once created, can only be updated with new scores.
     '''
     def __init__(self, objectId, name,scoreframe):
          self.objectId = objectId
          self.name = name
          self.scoreframe = scoreframe

     def getLastClick(user):
          '''Returns the latest (just previous to the entity currently being viewed)
             entity (NPO or Member)
             the entered user object visited
          '''
          elasticQuery = 'https://search-cariclub-5svmfprpqyhwerkedgazkhrciq.us-east-1.es.amazonaws.com/warehouse-log-*/_search?q=member_name:'+user.name+'&size=1'+'&pretty=true&fields=url,object2.object,object2.name&sort=_timestamp:desc'
          r= requests.get(elasticQuery)
          body=json.loads(r.content)
          b_hits=body['hits']
          click_series= b_hits['hits']
          latest_click = click_series[0]
          latest_clicked_url= latest_click['fields']['url']
          latest_clicked_entity= latest_click['fields']['object2.name']
          #print "Latest Clicked Entity " +str(latest_clicked_entity[0])
          _object = latest_click['fields']['object2.object'][0]
          return _object

     def getUserInterest(user,cur):
          cur.execute("SELECT term FROM rel WHERE object = %s",(user.objectId,))
          return list(cur.fetchall())
          
     def getUserLocation(user,cur):
     	  cur.execute("SELECT location FROM member where object = %s",(user.objectId,))
	  return list(cur.fetchall())

     def getProfessionalNetwork(user,cur):
          cur.execute("SELECT member_type FROM member WHERE object = %s",(user.objectId,))
          member_type = list(cur.fetchall())[0][0]
          professional_network=[]
          if(member_type=='pro'):
               cur.execute("SELECT firm FROM member__pro WHERE member =%s",(user.objectId,))
               member_firms = list(cur.fetchall())
               for i in range(0,len(member_firms)):
                    cur.execute("SELECT member FROM member__pro WHERE firm=%s",member_firms[i])
                    professional_network.append(list(cur.fetchall()))
               return professional_network
          if(member_type=='nonprofit'):
               return professional_network

     def getTitleNetwork(user,cur):
          cur.execute("SELECT title FROM member__pro WHERE member =%s",(user.objectId,))
          title = list(cur.fetchall())[0]
          cur.execute("SELECT member FROM member__pro WHERE title = %s",title)
          return list( cur.fetchall())

     def getSimilarUsers(user,cur,user_count):
          '''Returns most similar users to 'user'
             Param user_count( optional) defines number of similar users
             to return. By default set to 10.
          '''
          ##Users in same firm as 'user'
          network = user.getProfessionalNetwork(cur)
          #To Do:make sf such that it forms correct score_matrix even when there are more than 1 firms for user
          sf = Scoreframe(pd.DataFrame.from_records(network[0]),10)

          ##Users with same title as 'user'
          sameTitle = user.getTitleNetwork(cur)
          sf1 = Scoreframe(pd.DataFrame.from_records(sameTitle),0)


          print sf1.score_matrix
          
