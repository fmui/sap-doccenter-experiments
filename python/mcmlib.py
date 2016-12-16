# -*- coding: utf-8 -*-

##########################################################################
# Copyright 2016, Florian Müller
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

from datetime import datetime
import requests

# constants
NAME = "cmis:name"
OBJECT_ID = "cmis:objectId"
OBJECT_TYPE_ID = "cmis:objectTypeId"
BASE_TYPE_ID = "cmis:baseTypeId"
CREATED_BY = "cmis:createdBy"
CREATION_DATE = "cmis:creationDate"
LAST_MODIFIED_BY = "cmis:lastModifiedBy"
LAST_MODIFICATION_DATE = "cmis:lastModificationDate"
CHANGE_TOKEN = "cmis:changeToken"
DESCRIPTION = "cmis:description"
SECONDARY_OBJECT_TYPE_IDS = "cmis:secondaryObjectTypeIds"
IS_IMMUTABLE = "cmis:isImmutable"
IS_LATEST_VERSION = "cmis:isLatestVersion"
IS_MAJOR_VERSION = "cmis:isMajorVersion"
IS_LATEST_MAJOR_VERSION = "cmis:isLatestMajorVersion"
VERSION_LABEL = "cmis:versionLabel"
VERSION_SERIES_ID = "cmis:versionSeriesId"
IS_VERSION_SERIES_CHECKED_OUT = "cmis:isVersionSeriesCheckedOut"
VERSION_SERIES_CHECKED_OUT_ID = "cmis:versionSeriesCheckedOutId"
CHECKIN_COMMENT = "cmis:checkinComment"
CONTENT_STREAM_LENGTH = "cmis:contentStreamLength"
CONTENT_STREAM_MIME_TYPE = "cmis:contentStreamMimeType"
CONTENT_STREAM_FILE_NAME = "cmis:contentStreamFileName"
CONTENT_STREAM_ID = "cmis:contentStreamId"
IS_PRIVATE_WORKING_COPY = "cmis:isPrivateWorkingCopy"
PARENT_ID = "cmis:parentId"
ALLOWED_CHILD_OBJECT_TYPE_IDS = "cmis:allowedChildObjectTypeIds"
PATH = "cmis:path"
SOURCE_ID = "cmis:sourceId"
TARGET_ID = "cmis:targetId"
POLICY_TEXT = "cmis:policyText"
EXPIRATION_DATE = "cmis:rm_expirationDate"
START_OF_RETENTION = "cmis:rm_startOfRetention"
DESTRUCTION_DATE = "cmis:rm_destructionDate"
HOLD_IDS = "cmis:rm_holdIds"
CONTENT_STREAM_HASH = "cmis:contentStreamHash"
LATEST_ACCESSIBLE_STATE_ID = "cmis:latestAccessibleStateId"

# CMIS Exceptions

class CmisBaseError(Exception):
    """CMIS Base Exception"""
    def __init__(self, message, errorContent): 
        self.message = message
        self.errorContent = errorContent
       
class CmisRuntimeError(CmisBaseError):
    EXCEPTION = "runtime"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
    
    
class CmisConstraintError(CmisBaseError):
    EXCEPTION = "constraint"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
        
class CmisContentAlreadyExistsError(CmisBaseError):
    EXCEPTION = "contentAlreadyExists"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
           
class CmisFilterNotValidError(CmisBaseError):
    EXCEPTION = "filterNotValid"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisInvalidArgumentError(CmisBaseError):
    EXCEPTION = "invalidArgument"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisNameConstraintViolationError(CmisBaseError):
    EXCEPTION = "nameConstraintViolation"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisNotSupportedError(CmisBaseError):
    EXCEPTION = "notSupported"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisObjectNotFoundError(CmisBaseError):
    EXCEPTION = "objectNotFound"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisPermissionDeniedError(CmisBaseError):
    EXCEPTION = "permissionDenied"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisStorageError(CmisBaseError):
    EXCEPTION = "storage"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisStreamNotSupportedError(CmisBaseError):
    EXCEPTION = "streamNotSupported"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisUpdateConflictError(CmisBaseError):
    EXCEPTION = "updateConflict"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
            
class CmisVersioningError(CmisBaseError):
    EXCEPTION = "versioning"
    
    def __init__(self, message, errorContent): 
        CmisBaseError.__init__(self, message, errorContent)
        
           
class CmisServiceUnavailableError(CmisRuntimeError):
    def __init__(self, message, errorContent): 
        CmisRuntimeError.__init__(self, message, errorContent)

        
class CmisUnauthorizedError(CmisRuntimeError):
    def __init__(self, message, errorContent): 
        CmisRuntimeError.__init__(self, message, errorContent)


class CmisProxyAuthenticationError(CmisRuntimeError):
    def __init__(self, message, errorContent): 
        CmisRuntimeError.__init__(self, message, errorContent)

    
# CMIS objects

class CmisObject:
    def __init__(self, repository, json):
        self._repository = repository
        self._json = json
        self._properties = {}
        
        if 'succinctProperties' in json:
            for propId in json['succinctProperties']:
                self._properties[propId] = json['succinctProperties'][propId]
        elif 'properties' in json:
            for propId in json['properties']:
                if 'value' in json['properties'][propId]:
                    self._properties[propId] = json['properties'][propId]['value']
    
        self.id = self.get_property(OBJECT_ID)
        self.name = self.get_property(NAME)
        self.base_type_id = self.get_property(BASE_TYPE_ID)
        self.object_type_id = self.get_property(OBJECT_TYPE_ID)
        self.creation_date = self.get_datetime_property(CREATION_DATE)
        
    def get_properties(self):
        return self._properties
    
    def get_property(self, popertyId):
        return self._properties.get(popertyId)
        
    def get_datetime_property(self, popertyId):
        if popertyId in self._properties:
            millis = self._properties[popertyId]
            return datetime.utcfromtimestamp(millis // 1000).replace(microsecond=millis % 1000 * 1000)
        return None    
        
    @staticmethod
    def convert_object(repository, json):
        baseType = None
        
        if 'succinctProperties' in json:
            if OBJECT_TYPE_ID in json['succinctProperties']:
                baseType = json['succinctProperties'][BASE_TYPE_ID]
                
        if 'properties' in json:
            if OBJECT_TYPE_ID in json['properties']:
                if 'value'  in json['properties'][BASE_TYPE_ID]:
                    baseType = json['properties'][BASE_TYPE_ID]['value']
            
        if baseType == 'cmis:document':
            return Document(repository, json)
        elif baseType == 'cmis:folder':
            return Folder(repository, json)
        else:
            return CmisObject(repository, json)
        

class Document(CmisObject):
        def __init__(self, repository, json):
            CmisObject.__init__(self, repository, json)
        
        def get_content(self):
            pass
     
     
class Folder(CmisObject):
        def __init__(self, repository, json):
            CmisObject.__init__(self, repository, json)

        def get_children(self, propertyFilter=None, orderBy=None,
             includeAllowableActions=False, includeRelationships='none',
             renditionFilter='cmis:none', includePathSegment=False,
             maxItems=None, skipCount=None, succinct=True):
            return self._repository.get_children(self.id, propertyFilter,
             orderBy, includeAllowableActions, includeRelationships,
             renditionFilter, includePathSegment, maxItems, skipCount,
             succinct)

# Repositories

class Repository:
    def __init__(self, session, repositoryInfo):
        self._session = session
        self._repositoyInfo = repositoryInfo
        self._rootFolderURL = repositoryInfo['rootFolderUrl']
        self._repositoryURL = repositoryInfo['repositoryUrl']

    def get_root_folder(self):
        return self.get_object(self._repositoyInfo['rootFolderId'], "*")
    
    def get_object(self, objectId, propertyFilter=None, includeAllowableActions=False,
                   includeRelationships='none', renditionFilter='cmis:none',
                   includePolicyIds=False, includeAcl=False, succinct=True):
        params = {'objectId' : objectId,
                  'cmisselector' : 'object',
                  'filter' : propertyFilter,
                  'includeAllowableActions' : includeAllowableActions,
                  'includeRelationships': includeRelationships,
                  'renditionFilter' : renditionFilter,
                  'includePolicyIds' : includePolicyIds,
                  'includeAcl' : includeAcl,
                  'succinct' : succinct}
        
        response = self._session._get(self._rootFolderURL, params)
        
        return CmisObject.convert_object(self, response.json())
    
    def get_object_by_path(self, path):
        pass
    
    def get_children(self, folderId, propertyFilter=None, orderBy=None,
                     includeAllowableActions=False, includeRelationships='none',
                     renditionFilter='cmis:none', includePathSegment=False,
                     maxItems=None, skipCount=None, succinct=True):
        params = {'objectId' : folderId,
                  'cmisselector' : 'children',
                  'filter' : propertyFilter,
                  'orderBy' : orderBy,
                  'includeAllowableActions' : includeAllowableActions,
                  'includeRelationships': includeRelationships,
                  'renditionFilter' : renditionFilter,
                  'includePathSegment' : includePathSegment,
                  'maxItems' : maxItems,
                  'skipCount' : skipCount,
                  'succinct' : succinct}
        
        response = self._session._get(self._rootFolderURL, params)
        json = response.json()
        
        
        children = []
        if 'objects' in json:
            for obj in json['objects']:
                if 'object' in obj:
                    children.append(CmisObject.convert_object(self, obj['object']))
        
        hasMoreItems = False
        if 'hasMoreItems' in json:
            hasMoreItems = json['hasMoreItems']
           
        numItems = None
        if 'numItems' in json:
            numItems = json['numItems']      
        
        return ChildrenIterator(children, hasMoreItems, numItems)
    
    
class MyDocumentsRepository(Repository):
    def __init__(self, session, repositoryInfo):
        Repository.__init__(self, session, repositoryInfo);
        self._homeFolderId = repositoryInfo['myDocuments']
        
    def get_home_folder(self):
        return self.get_object(self._homeFolderId, "*")
    
        
class SharingRepository(Repository):
    def __init__(self, session, repositoryInfo):
        Repository.__init__(self, session, repositoryInfo);
        self._homeFolderId = repositoryInfo['sharing']

    def get_home_folder(self):
        return self.get_object(self._homeFolderId, "*") 
    

class CorporateRepository(Repository):
    def __init__(self, session, repositoryInfo):
        Repository.__init__(self, session, repositoryInfo);

# Session

class MCMSession:
    def __init__(self, user, password, url="https://mdocs.sap.com/mcm/b/json"):
        self._user = user
        self._url = url
        self._csrfToken = "fetch"

        self._myDocumentsRep = None
        self._sharingRep = None
        self._corparteReps = {}
        
        self._httpSession = requests.Session()
        self._httpSession.auth = (user, password)
        self._httpSession.headers.update({"X-CSRF-Token": "fetch"})
        # self._httpSession.proxies = {'https', 'https://proxy:8080'}
        
        self.__loadRepositories()
    
    def __loadRepositories(self):
        response = self._get(self._url)
        self._repositories = response.json()
        
        for repId in self._repositories:
            repsitory = self._repositories[repId]
            if repsitory:
                if 'myDocuments' in repsitory:
                    self._myDocumentsRep = MyDocumentsRepository(self, repsitory)
                if 'sharing' in repsitory:
                    self._sharingRepId = SharingRepository(self, repsitory)
                if 'corporate' in repsitory:
                    self._corparteReps[repId] = CorporateRepository(self, repsitory)
    
    
    def _get(self, url, params={}):
        """HTTP GET call"""
        response = self._httpSession.get(url, params=params)
        
        if "X-CSRF-Token" in response.headers:
            self._httpSession.headers.update({"X-CSRF-Token": response.headers["X-CSRF-Token"]})
        
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204 and response.status_code != 206:
            raise self.__convertStatusCode(response)
        
        return response
     
     
    def __convertStatusCode(self, response):
        """ Converts a HTTP status code into and Error"""
        jsonError = {}
        try:
            jsonError = response.json()
        except ValueError:
            pass

        errorContent = response.text
        message = response.reason
        
        if jsonError and jsonError['exception']:
            exception = jsonError['exception']
            
            if jsonError['message']:
                message = jsonError['message']
            
            if CmisConstraintError.EXCEPTION.lower() == exception.lower():
                return CmisConstraintError(message, errorContent)
            elif CmisContentAlreadyExistsError.EXCEPTION.lower() == exception.lower():
                return CmisContentAlreadyExistsError(message, errorContent)
            elif CmisFilterNotValidError.EXCEPTION.lower() == exception.lower():
                return CmisFilterNotValidError(message, errorContent)
            elif CmisInvalidArgumentError.EXCEPTION.lower() == exception.lower():
                return  CmisInvalidArgumentError(message, errorContent)
            elif CmisNameConstraintViolationError.EXCEPTION.lower() == exception.lower():
                return  CmisNameConstraintViolationError(message, errorContent)
            elif CmisNotSupportedError.EXCEPTION.lower() == exception.lower():
                return  CmisNotSupportedError(message, errorContent)
            elif CmisObjectNotFoundError.EXCEPTION.lower() == exception.lower():
                return CmisObjectNotFoundError(message, errorContent)
            elif CmisPermissionDeniedError.EXCEPTION.lower() == exception.lower():
                return  CmisPermissionDeniedError(message, errorContent)
            elif CmisStorageError.EXCEPTION.lower() == exception.lower():
                return  CmisStorageError(message, errorContent)
            elif CmisStreamNotSupportedError.EXCEPTION.lower() == exception.lower():
                return  CmisStreamNotSupportedError(message, errorContent)
            elif CmisUpdateConflictError.EXCEPTION.lower() == exception.lower():
                return  CmisUpdateConflictError(message, errorContent)
            elif CmisVersioningError.EXCEPTION.lower() == exception.lower():
                return  CmisVersioningError(message, errorContent)
            elif response.status_code == 503:
                return  CmisServiceUnavailableError(message, errorContent)

        # fall back to status code
        if response.status_code == 400:
            return  CmisInvalidArgumentError(message, errorContent)
        elif response.status_code == 401:
            return  CmisUnauthorizedError(message, errorContent)
        elif response.status_code == 403:
            return  CmisPermissionDeniedError(message, errorContent)
        elif response.status_code == 404:
            return  CmisObjectNotFoundError(message, errorContent)
        elif response.status_code == 405:
            return  CmisNotSupportedError(message, errorContent)
        elif response.status_code == 407:
            return  CmisProxyAuthenticationError(message, errorContent)
        elif response.status_code == 409:
            return  CmisConstraintError(message, errorContent)
        elif response.status_code == 503:
            return  CmisServiceUnavailableError(message, errorContent)
        else:
            return  CmisRuntimeError(message, errorContent)


    def get_my_documents_repository(self):
        return self._myDocumentsRep
    
    
    def get_sharing_repository(self):
        return self._sharingRep


    def get_all_corporate_repositories(self):
        return self._corparteReps

    
    def get_corporate_repository(self, repositoryId):
        return self._corparteReps.get(repositoryId)
    
        
    def close(self):
        self._httpSession.close()


# helpers

class ChildrenIterator:
    def __init__(self, children, hasMoreItems, numItems):
        self.children = children
        self.hasMoreItems = hasMoreItems
        self.numItems = numItems
        self._counter = 0
    
    def __iter__(self):
        return self
        
    def next(self):
        self._counter += 1
        if self._counter > len(self.children):
            raise StopIteration

        return self.children[self._counter - 1]
    
