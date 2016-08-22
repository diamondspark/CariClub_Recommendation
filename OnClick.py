#(Say the object_ currently being navigated to is 700020)

from Users import User
from Entity import entity


def clickDetails(object_,u1,cur):
     '''On each user(u1) click on the platform; uses details of the click.
       ( Which is recieved from backend).
       From details of the click we know, which for which item do we
       need to show similarity for.
       This method runs before the page is loaded
       and updates user's score dataframe accordingly
     '''
     ## Method to check if object is NPO or firm or member etc.
     ## To do this Create entity object for object_.
     ## There are suitable methods to perform this task in entity class.
     e = entity(object_,"")
     latest_entity = entity.objectType(e,cur)
     updateClickScores(u1,latest_entity,cur)
     
     


def updateClickScores(u1,latest_entity,cur):
     'Update scores of clicked entities'
     if latest_entity.objectType == 'NPO Org':
           
           #Determine similar NPO's to the one user is currently
           #navigating to. The current object user is navigating to
           #Comes from the backend to this webservice before the page
           #is loaded. (Say the object currently being navigated to is 700020)

           
           #Update the Score for currently clicked NPO
           updateNPOClickScore(u1,latest_entity,cur)
           
           
           
     
     if latest_entity.objectType == 'Firm Org':
          return updateFirmScore(u1,latest_entity)

     if latest_entity.objectType == 'nonprofit':
          return updateNonProfitMemberScore(u1,latest_entity)

     if latest_entity.objectType == 'pro':
          return updateProMemberScore(u1,latest_entity)


def updateNPOClickScore(u1,latest_entity,cur):
     '''Logic to update non-profit's overall score for user u1 goes here.
        The method updates the score in u1's dataframe for latest_entity
        by adding value of scoreWeight to current score
     '''
     #Interest based similarity
     if("Interest_Score" in u1.scoreframe.score_matrix.columns):
          u_interests = u1.getUserInterest(cur)
          highScoreInterest = 50
          similarNPOInterest(cur,u_interests,u1.scoreframe,latest_entity,highScoreInterest)

     #Location Based Similarity
     if("Location_Score" in u1.scoreframe.score_matrix.columns):
          u_location = u1.getUserLocation(cur)
          highScoreLocation = 30
          similarNPOLoc(cur,u_location,u1.scoreframe,latest_entity,highScoreLocation)

     #Network Based Similarity
          if("Network_Score" in u1.scoreframe.score_matrix.columns):
               similarNPONetwork(u1,cur)
     


##     df= u1.dataframe
##     temp = df[df[0]==int(latest_entity.objectId)]
##     df.iat[temp.index[0],1]+= scoreWeight
##     print df
##     return


def similarNPOInterest(cur,u_interests,sf,latest_entity,highScore):
     '''
          Updates u1's scoreframe for NPOs having same sector as each of u1's interests
     '''
     #Caution! SQL query "SELECT object FROM rel WHERE term=%s" returns a list of all ids in database which
     # have the same interest/sector as the queried u1's interest.
     # This resulting list contains both users and npo's. Since we are only
     # interested in NPO's we'll use join to get only the Npo's.
     
     for i in range(0,len(u_interests)):
          cur.execute("SELECT rel.object from rel inner join org__nonprofit on rel.object=org__nonprofit.org WHERE term = %s AND type = 'category'", u_interests[i])
          result_interest = list(cur.fetchall())
          sf.updateScores('Interest_Score',result_interest,highScore)
     sf.updateOverallScore()

def similarNPOLoc(cur,u_location,sf,latest_entity,highScoreLocation):
     '''
          Updates u1's scoreframe for NPOs having same location as  u1's location
     '''
     cur.execute("SELECT object FROM org WHERE location = %s AND org_type= 'nonprofit'",(u_location,))
     result_loc= list(cur.fetchall())
     sf.updateScores('Location_Score',result_loc,highScoreLocation)
     sf.updateOverallScore()
    


def similarNPONetwork(user,cur):
     '''
          Update's u1's scoreframe for NPO's to which people similar to u1
          (i.e. people in the network of u1) have shown their interest in.
          By shown their interest, we mean people who are on associate board or
          are being onboarded or have joined fanclub
     '''
     similar_user = user.getSimilarUsers(cur,10)
     

def updateFirmScore(u1,latest_entity):
     return

def updateNonProfitMemberScore(u1,latest_entity):
     return

def updateProMemberScore(u1,latest_entity):
     return
