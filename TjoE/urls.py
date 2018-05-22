from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from login.models import ActiveLogins, Characters, Users, Inventory, Quests
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json


    
@csrf_exempt 
def MMOCheckClient(request):
    
    data = json.loads(request.body)
    userid = data['userid']
    charid = data['charid']
    sessionkey = data['sessionkey']
  
    if ActiveLogins.objects.filter(user_id=userid) > 0:
        try:
            session = ActiveLogins.objects.get(session_key=sessionkey)
            return HttpResponse('{"status":"OK"}')
        except:
            return HttpResponse('{"status":"Character not found"}')
    else:
        return HttpResponse('{"status":"You are not logged in."}')
        
@csrf_exempt 
def newRegistration(request):
    from bcrypt import hashpw, gensalt
    
    
    data = json.loads(request.body)
    username = data['accountname']
    accountpassword = data['accountpassword']
    accountemail = data['accountemail']
    plaintext_password = accountpassword
    hashed = hashpw(plaintext_password, gensalt())
    
    if Users.objects.filter(username=username) > 0:
        return HttpResponse('{"status":"This account name is unavailable"}')
    else:
        newUser = Users(
            username=username,
            password=hashed,
            email=accountemail
            )
        newUser.save()
        return HttpResponse('{"status":"OK"}')
        
@csrf_exempt 
def mmoLogin(request):
    from bcrypt import hashpw, gensalt
    import random
    import string
    import hashlib
    
    def random_md5(string_length=25, slug=False, number=1):
        hashes = []
        for n in range(number):
            r = ''.join(random.choice(string.letters + string.digits) for i in xrange(string_length))
            m = hashlib.md5()
            m.update(r)
            if slug == True:
                hashes.append(m.hexdigest()[:7])
            else:
                hashes.append(m.hexdigest())
        return hashes
    
    data = json.loads(request.body)
    login = data['login']
    password = data['password']
    
    #Get User profile
    if Users.objects.filter(username=login) > 0:
        user = Users.objects.get(username=login)
        attemptPass = str(user.password).encode('utf-8')
        enteredPass = str(password).encode('utf-8')
        if hashpw(enteredPass, attemptPass) == attemptPass:
            #Need To delete active Login Session
            ActiveLogins.objects.filter(user_id_id=user.pk).delete()
            #Create New Session
            newKey = str(random_md5(7,True,1)).replace("['","").replace("']","")
            
            newSession = ActiveLogins(
                user_id_id=user.pk,
                session_key=newKey,
                )
            newSession.save()
            return HttpResponse('{"status":"OK","sessionkey":"' + str(newKey) + '","userid":' + str(user.pk) + '}')
        else:
            HttpResponse('{"status":"Login Information is not correct. Check your username and password."}')
        
    else:
        return HttpResponse('{"status":"Login Information is not correct. Check your username and password."}')
        


    
    
    plaintext_password = accountpassword
    hashed = hashpw(plaintext_password, gensalt())
    
    if Users.objects.filter(username=username) > 0:
        return HttpResponse('{"status":"This account name is unavailable"}')
    else:
        newUser = Users(
            username=username,
            password=hashed,
            email=accountemail
            )
        newUser.save()
        return HttpResponse('{"status":"OK"}')
        
        
@csrf_exempt       
def createCharacter(request):
    data = json.loads(request.body)
    userid = data['user_id']
    sessionkey = data['sessionkey']
    name = data['name']
    classid = data['classid']
    

    #Check if username is available
    if not Characters.objects.filter(name=name).count() > 0:
        #Create Character
        newToon = Characters(
            health = 300,
            gender = 0,
            mana = 150,
            level = 1,
            name = name,
            user_id_id = userid,
            class_field = classid,
            experience = 0,
            clan_id = 1,
            posx = 0,
            posy = 0,
            posz = 0,
            rotation_yaw = 0,
            equip_head='',
            equip_chest = '',
            equip_hands = '',
            equip_legs = '',
            equip_feet = '',
            hotbar0 = '',
            hotbar1 = '',
            hotbar2 = '',
            hotbar3 = '',
            hotbar4 = '',
            hotbar5 = '',
            hotbar6 = '',
            hotbar7 = ''
            )
        newToon.save()
        return HttpResponse('{"status":"OK"}')
    else:
        return HttpResponse('{"status":"This name is unavailable"}')

@csrf_exempt 
def getCharacters(request):

    #Check if Logged In
    characters = Characters.objects.all()
        
    return render(request, 'character.json', {
            'characters': characters,
        })
        
@csrf_exempt 
def getCharacter(request):
    data = json.loads(request.body)
    charid = data['charid']
    userid = data['userid']
    
    #Check if Logged In
    
    #Check if username is available
    character = Characters.objects.get(pk=charid)
    items = Inventory.objects.filter(character_id_id=charid)
    return render(request, 'single_character.json', {
            'character': character,
            'items': items,
        })
        
@csrf_exempt 
def getServer(request):
    return HttpResponse('{"status":"OK","address":"192.168.86.160"}')

@csrf_exempt 
def saveCharacter(request):
    
    data = json.loads(request.body)
    charid = data['charid']
    inventory = data['inventory']
    quests = data['quests']
    
    experience = data['experience']
    level = data['level']
    
    posx = data['posx']
    posy = data['posy']
    posz = data['posz']
    
    yaw = data['yaw']
    
    equipHead = data['equip_head']
    equipChest = data['equip_chest']
    equipHands = data['equip_hands']
    equipLegs = data['equip_legs']
    equipFeet = data['equip_feet']
    
    hotbar0 = data['hotbar0']
    hotbar1 = data['hotbar1']
    hotbar2 = data['hotbar2']
    hotbar3 = data['hotbar3']
    hotbar4 = data['hotbar4']
    hotbar5 = data['hotbar5']
    hotbar6 = data['hotbar6']
    hotbar7 = data['hotbar7']
    
    
    
    charSave = Characters.objects.get(id=charid)
    charSave.experience = experience
    charSave.level = level
    
    charSave.posx = posx
    charSave.posy = posy
    charSave.posz = posz
    
    charSave.yaw = yaw
    
    charSave.equipHead = equipHead
    charSave.equipChest = equipChest
    charSave.equipHands = equipHands
    charSave.equipLegs = equipLegs
    charSave.equipFeet = equipFeet
    
    charSave.hotbar0 = hotbar0
    charSave.hotbar1 = hotbar1
    charSave.hotbar2 = hotbar2
    charSave.hotbar3 = hotbar3
    charSave.hotbar4 = hotbar4
    charSave.hotbar5 = hotbar5
    charSave.hotbar6 = hotbar6
    charSave.hotbar7 = hotbar7
    
    try:
        charSave.save()
        charSaveSuccess = True
    except:
        charSaveSuccess = False
        
    if charSaveSuccess == True:
        #Delete Quests
        Quests.objects.filter(character_id_id=charid).delete()
        #Delete Inventory
        Inventory.objects.filter(character_id_id=charid).delete()
        
        for entry in inventory:
            newItem = Inventory(
                character_id_id=charid,
                slot=entry['slot'],
                item=entry['item'],
                amount=entry['amount']
                )
            newItem.save()
        
        for entry in quests:
            if entry.completed:
                newQuest = Quests(
                    character_id=charid,
                    quest = entry['quest'],
                    completed = entry['completed'],
                    )
            else:
                newQuest = Quests(
                    character_id=charid,
                    quest = entry['quest'],
                    completed = entry['completed'],
                    task1 = entry['task1'],
                    task2 = entry['task2'],
                    task3 = entry['task3'],
                    task4 = entry['task4']
                    )
                newQuest.save()
    return HttpResponse('{"status":"OK"}')
    
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mmo/mmocheckclient.php', MMOCheckClient, name='MMOCheckClient'),
    url(r'^mmo/mmocreatecharacter.php', createCharacter, name='Create Character'),
    url(r'^mmo/mmogetcharacters.php', getCharacters, name='Get Characters'),
    url(r'^mmo/mmogetcharacter.php', getCharacter, name='Get Characters'),
    url(r'^mmo/mmogetserver.php', getServer, name='MMO Get Server'),
    url(r'^mmo/mmologin.php', mmoLogin, name='MMO Login'),
    url(r'^mmo/mmosavecharacter.php', saveCharacter, name='MMO Login'),
    url(r'^mmo/mmogetserver.php', saveCharacter, name='MMO Login'),
    
]
