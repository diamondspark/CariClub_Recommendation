import MySQLdb
class entity:
     ''' Each Member( pro or nonprofit), Org(firm or NPO) can be an
         entity object
     '''
     def __init__(self,objectId, objectType):
          self.objectId = objectId
          self.objectType = objectType

     
     def isUser(entity_obj,cur):
          _object=entity_obj.objectId
          cur.execute("SELECT name FROM member WHERE object = %s",(_object,))
          if len(cur.fetchall())==0:
               return False
          else:
               return True

     def __memberType(entity_obj,cur,_object):
          '''Private Method. Call only when isMember true
          '''
          cur.execute("SELECT member_type FROM member WHERE object = %s",(_object,))
          res = list(cur.fetchall())[0][0]
          return entity(_object,res)
          


     def isOrg(entity_obj,cur):
          _object=entity_obj.objectId
          cur.execute("SELECT name FROM org WHERE object = %s",(_object,))
          if len(cur.fetchall())==0:
               return False
          return True

          
     def __isNPO(entity_obj,cur,_object):
         '''Private Method. Call only when isOrg(cur,_object) is true
         '''
         cur.execute("SELECT org_type FROM org WHERE object = %s",(_object,))
         if(list(cur.fetchall())[0][0]=='nonprofit'):
             return True
         return False

     def __isFirm(entity_obj,cur,_object):
         '''Private Method. Call only when isOrg(cur,_object) is true
         '''
         cur.execute("SELECT org_type FROM org WHERE object = %s",(_object,))
         if(list(cur.fetchall())[0][0]=='firm'):
             return True
         return False

     def objectType(entity_obj,cur):
          
          '''
          Determine the input object is an organisation (NPO or firm)
          or is a member.
          Implement check for isNPO() or isFirm().
          Currently user can't click on Firms on Cariclub. 
          '''
          _object=entity_obj.objectId
          if(entity_obj.isUser(cur)):
               e= entity_obj.__memberType(cur,_object)
               return e
     
          elif(entity_obj.isOrg(cur)):             
               if(entity_obj.__isNPO(cur,_object)):
                  e = entity(_object,"NPO Org")
                  return e
               if(entity_obj.__isFirm(cur,_object)):
                  e = entity(_object,"Firm Org")
                  return e
          
          else:
                e= entity(_object,"Unknown")
                return e
