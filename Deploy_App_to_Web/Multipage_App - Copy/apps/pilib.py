import requests
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




DEBUGMODE = 0
TEST = 0



serverIP = "40.117.156.48" #API server
headers = {'authorization': "Basic YmVwdmlzaW9uXGxhbmRhdW46U21pdGhFbmczNDdXMzY=", # User:Password in 64bit encryption
                'x-requested-with': "true",
        'content-type': "application/json",
        'cache-control': "no-cache",
        }


#in> url = url of the piwebapi page
#Task: return whole page
#out> Object Response
def getResponse(url):
        response = requests.request("GET", url, headers=headers, auth=('smith1','SmithEng347W36'),verify = False) #POST request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Ignore the ssl verify = False warning
        DEBUG(response)
        return (response)

#in> webid of the attribute
#Task: POST Value,Time to Attribute
#out> Object Response
def sendtoPI(AttributeWebid,value,Time):
        url = "https://"+ serverIP +"/piwebapi/streams/"+ AttributeWebid + "/value" #URL to POST
        response = requests.request("POST", url, json = {"Good":True , "Questionable": False, "Value": value, "Timestamp": Time}, headers=headers, auth=('smith1','SmithEng347W36'), verify = False) #POST request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Ignore the ssl verify = False warning
        DEBUG(response)
        return (response)


#in> webid of the attribute
#Task: POST Value,Time to Attribute
#out> Object Response
def listoPI(row):
        url = "https://"+ serverIP +"/piwebapi/streams/"+ row[0] + "/value" #URL to POST
        response = requests.request("POST", url, json = {"Good":True , "Questionable": False, "Value": row[1], "Timestamp": row[2]}, headers=headers,verify = False) #POST request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Ignore the ssl verify = False warning
        DEBUG(response)
        return (response)



#in> Webid of the Element
#Task: Returns atributes page from Element webid
#out> Object Response
def getatrfromPI(ElementWebid):
        url = "https://"+ serverIP +"/piwebapi/elements/"+ ElementWebid + "/attributes" #URL to POST
        response = getResponse(url)
        DEBUG(response)
        return response

#in> webid of the AssetDatabase
#Task: Returns Elements page from AssetServer
#out> Object Response
def getEleFromAdb(AssetDatabaseWebid):
        url = "https://"+ serverIP + "/piwebapi/assetdatabases/" + AssetDatabaseWebid + "/elements"
        response = getResponse(url)
        DEBUG(response)
        return (response)

#Duplicate of getatrfromPI
#in> Webid of the Element
#Task: Returns atributes page from Element webid
#out> Object Response
def getAttrFromEle(ElementWebid):
        url = "https://"+ serverIP +"/piwebapi/elements/"+ ElementWebid + "/attributes" #URL to POST
        response = getResponse(url)
        DEBUG(response)
        return (response)

#Task: Returns Current Value of Attribute
#out> Object Response
def getCV(AttributeWebid):
        url = "https://"+ serverIP +"/piwebapi/streams/"+ AttributeWebid + "/value" #URL to POST
        response = requests.request("GET", url, headers=headers,verify = False) #GET request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Ignore the ssl verify = False warning
        DEBUG(response)
        return (response)

#in> url = /piwevapi/?type1?/?webid?/?type2?
#Taks: Returns Response
#out> Object Response
def getanyfromPI(type1,webid,type2):
        url = "https://"+ serverIP +"/piwebapi/" + type1+ "/"+ webid + "/" + type2 #URL to POST
        response = getResponse(url)
        DEBUG(response)
        return (response)



#in> webid of the Assetdatabase
#Task: Returns self Assetdatabase page
#out> Object Response
def getSelfAssetdb(AssetdatabaseWebid):
    url = "https://" + serverIP + "/piwebapi/assetdatabases/"+ AssetdatabaseWebid
    response = getResponse(url)
    return response

#in> webid of the Element
#Task: Returns self Elements page
#out> Object Response
def getSelfElement(ElementWebid):
        url = "https://" + serverIP + "/piwebapi/elements/"+ ElementWebid
        response = getResponse(url)
        print(response)
        return response

#in> webid of the Attribute
#Task: Returns self Attribute page
#out> Object Response
def getSelfAttribute(AttributeWebid):
    url = "https://" + serverIP + "/piwebapi/attributes/"+ AttributeWebid
    response = getResponse(url)
    return response

#in> webid of the Element
#task: returns name of the element
#out> string Name of the Element
def getElementName(ElementWebid):
        response = getSelfElement(ElementWebid)
        res = response.json()
        print(res)
        return res['Name']

#in> webid of the Attribute
#Task: returns Name of the attribute
#out> string Name of the Atrribute
def getAttributeName(AttributeWebid):
    url = "https://" + serverIP + "/piwebapi/attributes/"+ AttributeWebid
    response = getResponse(url).json()
    return response['Name']

#in> webid of the parent Element
#Task: Extract webid,name of attributes from the Element
#out> List of [WebId, Name]
def getAttributes(ElementWebid):
        list = []
        res = getatrfromPI(ElementWebid)
        list = parseNameId(res.json())
        return list

#in> webid of the parent a AssetDatabase
#Taks: Extract webid,names of elements from the AssetDatabase
#out> List of [Webid, Name]
def getElements(AssetdatabaseWebid):
        list = []
        res = getEleFromAdb(AssetdatabaseWebid)
        list = parseNameId(res.json())
        return list


##Under Developement
#in> Element webid
#Task: Multiple posts at time
#out> Object Response
def sendAlltoPI(webid,value,Time,type1,type2):
        url = "https://"+ serverIP +"/piwebapi/" + type1 + "/" + webid + "/" + type2 #URL to POST
        response = requests.request("POST", url, json = {"Good":True , "Questionable": False, "Value": value, "Timestamp": Time}, headers=headers,verify = False) #POST request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Ignore the ssl verify = False warning
        DEBUG(response)
        return (response) #Returning response back

#in> JSON response
#taks: Parse response to extract WebId and Name
#out> list of [Webid,Name]
def parseNameId(res):
        DataList = [ ]
        for names in res['Items']:
                data = [str(names['WebId']) , str(names['Name'])]
                DataList.append(data)
        return DataList


#in> WebID to check
#task> Checks if webid is Element or not
#out> Returns Boolean
def isAttribute(uknwebid):
        response = getSelfAttribute(uknwebid)
        res = isSuccess(response)
        return res

#in> WebID to check
#task> Checks if webid is Element or not
#out> returns Boolean
def isElement(uknwebid):
        response = getSelfElement(uknwebid)
        res = isSuccess(response)
        return res

#in> WebID to check
#task> Returns type of WebID
#out> returns bool
def isAssetdb(uknwebid):
        response = getSelfAssetdb(uknwebid)
        res = isSuccess(response)
        return res

#in> WebID to check
#task> Returns type of WebID
#out> String Assetdatabase, Element, Attribute
def typeofWebid(webid):
        if isAttribute(webid):
                type =  "Attribute"
        elif isElement(webid):
                type =  "Element"
        elif isAssetdb(webid):
                type = "Assetdatabase"
        else:
                type =  "Invalid Webid"
        return type
#in> Object Response
#task: if response is 200 return True , else return False
#out> Bool
def isSuccess(response):
        if response.status_code == 200|202:
                return True
        else:
                return False

#DEBUG Area
def DEBUG(response):
        if DEBUGMODE:
                print(response)
        else:
                return
        return


if TEST :
        TestElementWebid = "E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q"
        TestAttributeWebid = "A0EQ0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwM21Hw25ag0-zpud7jmneNQQkVQUElBRlxURVNUQVBJXFRFU1R8VEVTVFZBUjE"
        TestAssetdatabaseWebid = "D0Q0Ru7rdIvUSmr-scUjIw_gaZgSu92wukCWlJPkdhfzDQQkVQUElBRlxURVNUQVBJ"
        getResponse ("https://"+ serverIP +"/piwebapi/")
        sendtoPI(TestAttributeWebid,999,str(datetime.datetime.now()))
        getatrfromPI(TestElementWebid)
        getanyfromPI("elements",TestElementWebid,"attributes")
        getElementName(TestElementWebid)
        getAttributeName(TestAttributeWebid)
        sendAlltoPI(TestAttributeWebid,999,str(datetime.datetime.now()),"streams","value")
        pprint (getAttributes(TestElementWebid))
        getEleFromAdb(TestAssetdatabaseWebid)
        pprint (getElements(TestAssetdatabaseWebid))
        print(isAttribute(TestAttributeWebid))

        #examples leftover
        (getSelfElement("E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q").json())
        (getSelfAttribute("A0EQ0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwM21Hw25ag0-zpud7jmneNQQkVQUElBRlxURVNUQVBJXFRFU1R8VEVTVFZBUjE").json())
        (getAttrFromEle("E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q").json())
        (getEleFromAdb("D0Q0Ru7rdIvUSmr-scUjIw_gaZgSu92wukCWlJPkdhfzDQQkVQUElBRlxURVNUQVBJ").json())
        (getSelfAssetdb("D0Q0Ru7rdIvUSmr-scUjIw_gaZgSu92wukCWlJPkdhfzDQQkVQUElBRlxURVNUQVBJ").json())
        print(isAttribute("A0EQ0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwM21Hw25ag0-zpud7jmneNQQkVQUElBRlxURVNUQVBJXFRFU1R8VEVTVFZBUjE"))
        print(isAttribute("E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q"))
        print(isElement("A0EQ0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwM21Hw25ag0-zpud7jmneNQQkVQUElBRlxURVNUQVBJXFRFU1R8VEVTVFZBUjE"))
        print(isElement("E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q"))
        print(isAssetdb("D0Q0Ru7rdIvUSmr-scUjIw_gaZgSu92wukCWlJPkdhfzDQQkVQUElBRlxURVNUQVBJ"))
        print(isAssetdb("E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q"))

        print(typeofWebid("A0EQ0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwM21Hw25ag0-zpud7jmneNQQkVQUElBRlxURVNUQVBJXFRFU1R8VEVTVFZBUjE"))
        print(typeofWebid("E0Q0Ru7rdIvUSmr-scUjIw_gH67nD0tY5xGA2wANOhm-bwQkVQUElBRlxURVNUQVBJXFRFU1Q"))
        print(typeofWebid("D0Q0Ru7rdIvUSmr-scUjIw_gaZgSu92wukCWlJPkdhfzDQQkVQUElBRlxURVNUQVBJ"))
        print(typeofWebid("dIvUSmr-scUjIw_gaZgSu92wukCWlJPkdhfzDQQkVQUElBRlxURVNUQJ"))
