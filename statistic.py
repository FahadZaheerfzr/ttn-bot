from components.database import DB

statistic = DB['statistic'].find_one({"_id":1})

total_subscriptions = DB['memberships'].count_documents({})
total_groups_installed = DB['groups'].count_documents({})
total_telegram_members = DB['users'].count_documents({})

business = DB['groups'].count_documents({"category": "Business"})
crypto = DB['groups'].count_documents({"category": "Crypto"})
finance = DB['groups'].count_documents({"category": "Finance"})
sports = DB['groups'].count_documents({"category": "Sports"})
media = DB['groups'].count_documents({"category": "Media"})
influencer = DB['groups'].count_documents({"category": "Influencer"})
actor = DB['groups'].count_documents({"category": "Actor"})
baking = DB['groups'].count_documents({"category": "Baking"})
cooking = DB['groups'].count_documents({"category": "Cooking"})
nature = DB['groups'].count_documents({"category": "Nature"})
diy = DB['groups'].count_documents({"category": "DIY"})
celebrity = DB['groups'].count_documents({"category": "Celebrity"})

x= DB['statistic'].update_one({"_id": 1}, {"$set": {
    "total_subscriptions": total_subscriptions, 
    "total_groups_installed": total_groups_installed, 
    "total_telegram_members": total_telegram_members, 
    "business": business, 
    "crypto": crypto, 
    "finance": finance, 
    "sports": sports, 
    "media": media, 
    "influencer": influencer, 
    "actor": actor, 
    "baking": baking, 
    "cooking": cooking, 
    "nature": nature, 
    "diy": diy, 
    "celebrity": celebrity
    }})

print(x.raw_result)