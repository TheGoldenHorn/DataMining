from pymongo import MongoClient


def main():
    client = MongoClient('mongodb://ip:port')
    CompanyED = client.Linkedin.CompanyED
    collection = CompanyED.find({'linkedinId' : {'$exists' : False}}, no_cursor_timeout = True)
    for doc in collection:
        CompanyED.update({'_id' : doc['_id']}, {'$set' : {'linkedinId' : doc['linkedinUrlId'].rsplit('/', 1)[1]}})
    collection.close()
    return

if __name__ == '__main__':
    main()
