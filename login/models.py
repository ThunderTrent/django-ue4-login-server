# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ActiveLogins(models.Model):
    
    #id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey('login.Users',db_column='user_id',primary_key=True)
    session_key = models.CharField(max_length=20)
    character_id = models.ForeignKey('login.Characters', db_column='character_id',blank=True, null=True)
    def __str__(self):
    	return self.session_key
    class Meta:
        managed = False
        verbose_name_plural = 'Active Logins'
        db_table = 'active_logins'



class Characters(models.Model):
    
    healAbility = "Ability'/Game/MMO/Abilities/Heal.Heal'"
    fileBlastAbility = "Ability'/Game/MMO/Abilities/FireBlast.FireBlast'"
    resAbility = "Ability'/Game/MMO/Abilities/resAbility.resAbility'"
    abilityBarChoices = (
        (healAbility, 'healAbility'),
        (fileBlastAbility, 'fileBlastAbility'),
        (resAbility,'resAbility'),
    )
    id = models.AutoField(primary_key=True, db_column='id')
    user_id = models.ForeignKey('login.Users',db_column='user_id')
    name = models.CharField(max_length=20)
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    gender = models.IntegerField(choices=((0,'Male'),(1,'Female')))
    health = models.IntegerField()
    mana = models.IntegerField()
    level = models.IntegerField()
    experience = models.IntegerField()
    clan = models.ForeignKey('login.Clans',db_column='clan')
    posx = models.IntegerField(blank=True, null=True)
    posy = models.IntegerField(blank=True, null=True)
    posz = models.IntegerField(blank=True, null=True)
    rotation_yaw = models.FloatField()
    equip_head = models.CharField(max_length=100, blank=True, null=True)
    equip_chest = models.CharField(max_length=100, blank=True, null=True)
    equip_hands = models.CharField(max_length=100, blank=True, null=True)
    equip_legs = models.CharField(max_length=100, blank=True, null=True)
    equip_feet = models.CharField(max_length=100, blank=True, null=True)
    hotbar0 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar1 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar2 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar3 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar4 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar5 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar6 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    hotbar7 = models.CharField(max_length=100, blank=True, null=True, choices=abilityBarChoices)
    
    
    
    
    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'characters'
        verbose_name_plural = 'Characters'
        


class Clans(models.Model):
    name = models.CharField(max_length=24)
    leader_id = models.ForeignKey('login.Characters', db_column='leader_id')
    
    def __str__(self):
    	return self.name

    class Meta:
        managed = False
        db_table = 'clans'
        verbose_name_plural = 'Guilds'



class Inventory(models.Model):
    
    RougeArmorChest = "Equipment'/Game/MMO/Blueprints/Inventory/RogueArmor.RogueArmor'"
    RougeArmorPants = "Equipment'/Game/MMO/Blueprints/Inventory/RogueBreeches.RogueBreeches'"
    RougeBoots = "Equipment'/Game/MMO/Blueprints/Inventory/RogueBoots.RogueBoots'"
    
    MagicTome = "ItemData'/Game/MMO/Blueprints/Inventory/MagicTome.MagicTome'"
    StrangePotion = "ItemData'/Game/MMO/Blueprints/Inventory/StrangePotion.StrangePotion'"
    
    itemChoices = (
        (RougeArmorPants, 'Rouge Armor Pants'),
        (RougeArmorChest, 'Rouge Armor Chest'),
        (RougeBoots, 'Rouge Boots'),
        
        (StrangePotion, 'Strange Potion'),
        (MagicTome, 'Magic Tome'),
        
    )
    
    id = models.AutoField(db_column='id',primary_key=True)
    character_id = models.ForeignKey('login.Characters',db_column='character_id')
    slot = models.IntegerField()
    item = models.CharField(max_length=100,choices=itemChoices)
    amount = models.IntegerField()
    
    def __str__(self):
    	return self.item

    class Meta:
        managed = False
        db_table = 'inventory'
        verbose_name_plural = 'Items'
        verbose_name = 'Item'


class Quests(models.Model):
    character_id = models.ForeignKey('login.Characters',db_column='character_id')
    quest = models.CharField(max_length=70)
    completed = models.BooleanField()
    task1 = models.IntegerField()
    task2 = models.IntegerField()
    task3 = models.IntegerField()
    task4 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'quests'
        verbose_name_plural = 'Quests'


class Users(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=32)
    role = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.username
    

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name_plural = 'Users'
