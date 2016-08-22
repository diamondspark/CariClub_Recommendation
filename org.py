import pandas as pd
class Org:
     'Base class for all organisations, non-profit as well as firms'
     name=""
     _type=0
     objectId=0
     def __init__(self, name, _type, objectId):
          self.name=name
          self._type = _type
          self.objectId = objectId

     def similarNPOLoc(cur,u_interest,location, base_df, highScore):
          """Similar NPO's based on some given criteria (location)
             input: similarity criteria (eg. location), user interest id, overall score dataframe
                    highScore= score to be assigned if the similarity is true
             output: Similar NPO'S based on this given criteria and user's interest(s)
          """
          cur.execute("SELECT object FROM org WHERE location = %s AND org_type= 'nonprofit'",location)
          result_loc= list(cur.fetchall())
          # For each NPO with location similarity, find if it also matches users interest.
          for i in range(0,len(result_loc)):  
                  cur.execute("Select term FROM rel WHERE object = %s AND type = 'category'",result_loc[i])
                  res_sector= cur.fetchall()
                  # this loop checks if any of sector related to NPO a[i] is 660442( user's interest)
                  for j in range(0,len(res_sector)):
                       if res_sector[j]== (660442L,): #660442 is supposedly user's interest
                            temp = base_df[base_df[0]==a[i]]
                            base_df.iat[temp.index[0],1]+= highScore
                            break
          return base_df

     

##     def similarityInNetwork(cur, network, locSec):
##          """ Personalized similarity using network, sector and location
##              input: Similar NPO's based on sector and location (locSec)
##                     user's network id
##              output: Similar NPO's based on sector, location and network
##          """
##          #
##          cur.execute("SELECT member FROM member__pro WHERE firm = %s",network)
##          result_firm= list(cur.fetchall())
##          df = pd.DataFrame.from_records(result_firm)
##
##
##
##          
##          for i in range(0,len(locSec)): 
##               cur.execute locSec[i]
##          
      

                                 
     
