import json
import requests
from pprint import pprint
hanyang_lat = 37.55837671
hanyang_lng = 127.050856 

def hosp_list(lat=hanyang_lat, lng= hanyang_lng):    
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "Fcn7YL6ijC+gZBXN7lCbi+ZeWwShKENY8LDYSfZ9WmCU7AHlov3csFG5DqDdsOuEWQ9OqmYGiOx161pte9Vz1g=="
    i = 0
    #while(r != None):
    params = {
    'ServiceKey': default_key,
    'numOfRows' : 10000000,
    'yPos': lat,
    'xPos': lng,
    'radius' : 2000,      
    '_type': 'json'
  }

    r = requests.get(url, params=params) 
    return r.json()

def hosp_list_kwa(lat=hanyang_lat, lng= hanyang_lng):    
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key ="Fcn7YL6ijC+gZBXN7lCbi+ZeWwShKENY8LDYSfZ9WmCU7AHlov3csFG5DqDdsOuEWQ9OqmYGiOx161pte9Vz1g=="
 
    #while(r != None):
    params = {
    'ServiceKey': default_key,
    'numOfRows' : 10000000,
    'dgsbjtCd' : "13",
    'yPos': lat,
    'xPos': lng,
    'radius' : 2000,      
    '_type': 'json'
  }
    r = requests.get(url, params=params) 
    return r.json()

def subject_search(code,lat,lng):
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "Fcn7YL6ijC+gZBXN7lCbi+ZeWwShKENY8LDYSfZ9WmCU7AHlov3csFG5DqDdsOuEWQ9OqmYGiOx161pte9Vz1g=="
    params = {
    'ServiceKey': default_key,
    'numOfRows' : 10000000,
    'dgsbjtCd' : code,
    'yPos': lat,
    'xPos': lng,
    'radius' : 2000,
    '_type': 'json'
  }
    r = requests.get(url, params=params)
    if not r:
      return "fail"
    else:
      return r.json()


def pharm_list(lat, lng):    
    url = "http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'numOfRows': 1000000,
      'ServiceKey': default_key,      
      'yPos': lat,  
      'xPos': lng,
      'radius' : 2000,
      '_type': 'json'
    }
    r = requests.get(url, params=params)
    return r.json()


def test_run():
    clinics = pharm_list(hanyang_lat,hanyang_lng)
    pprint(clinics)




if __name__ == ("__main__"):
    test_run()