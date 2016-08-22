'''Update Scores for just previously clicked entity
'''
from Users import User
from Entity import entity

def onPageLoad(u1,cur):

     '''On each user(u1) click on the platform; fetches details of the click.
        Updates user's score dataframe accordingly. This method runs after the
        page has been loaded.
     '''
     # Finding Latest landing page for u1
     landing_objectId= User.getLastClick(u1)
     #Find type details of latest page object
     e = entity(landing_objectId,"")
     latest_entity = entity.objectType(e,cur)
     #return latest_entity
     click_score_weight = 70
     updateScores(u1,latest_entity,click_score_weight)
     
     


def updateScores(u1,latest_entity,score_weight):
     'Update scores of clicked entities'
##     '//This method should be part of DataFrame Class'
     if latest_entity.objectType == 'NPO Org':

           #Update the Score for currently clicked NPO
           updateNPOScore(u1,latest_entity,score_weight)

     if latest_entity.objectType == 'Firm Org':
          return updateFirmScore(u1,latest_entity)

     if latest_entity.objectType == 'nonprofit':
          return updateNonProfitMemberScore(u1,latest_entity)

     if latest_entity.objectType == 'pro':
          return updateProMemberScore(u1,latest_entity)


def updateNPOScore(u1,latest_entity,scoreWeight):
     '''Logic to update non-profit's overall score for user u1 goes here.
        The method updates the score in u1's dataframe for latest_entity
        by adding value of scoreWeight to current score
     '''
     df= u1.dataframe
     #a= "("+latest_entity.objectId+",)"
     temp = df[df[0]==int(latest_entity.objectId)]
     df.iat[temp.index[0],1]+= scoreWeight
     print df
     return

def updateFirmScore(u1,latest_entity):
     return

def updateNonProfitMemberScore(u1,latest_entity):
     return

def updateProMemberScore(u1,latest_entity):
     return
