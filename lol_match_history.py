#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 11:57:27 2017

@author: matthewgonzalez
"""
# -*- coding: UTF-8 -*-
import pandas as pd
import requests
import csv
#use beautiful soup to pull list of all north american tournaments
#use median/mean length of game to show margin of victory


def historical_tournament_data(file):
    #opens file and creates tournament list
    a = open(file)
    ls = list(csv.reader(a))[0]
    tournaments = [i.split(' ') for i in ls]  

    all_region_tournaments = []
    
    #loop through each tournament and pull data from html
    for i in tournaments:
        print("Generating data for: " + "-".join(i))
        tourney = "-".join(i)
        placeholder = '%s'*len(i)
        count = 0
        while count <= len(i) - 2:
            i[count] = i[count] + '%%20'
            count += 1
        elements = tuple(i)
        #read url
        url_1 = 'https://lol.gamepedia.com/Special:RunQuery/MatchHistoryTournament?MHT%%5Btournament%%5D=Concept:' + placeholder +'&MHT%%5Btext%%5D=Yes&wpRunQuery=true'
        url_2 = url_1 % elements
        new_url = url_2.replace('%%','%')
        print(new_url)
        header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
        r = requests.get(new_url, headers=header)
        print("Reading html as table...")
        #generate table
        team_table = pd.read_html(r.text, flavor='bs4')[0].astype('str')
        
### Everything that deals with columnn modification is a bit messy. Works, but messy ###
        
        #modify columns
        team_table.drop([0,len(team_table)-1], inplace=True)
        team_table.columns = team_table.iloc[0]
        team_table = team_table.reset_index(drop=True)
        team_table = team_table.drop(0)
        team_table = team_table.drop(['SB','MH','VOD'], axis=1)
        team_table['Tournament'] = tourney
        all_region_tournaments.append(team_table)
        
    #combine all tables
    result = pd.concat(all_region_tournaments)
    result.columns = ['Date','Patch','Blue', 'Red', 'Winner','Blue_Bans','Red_Bans', 
'Blue_Picks', 'Red_Picks', 'Blue_Roster', 'Red_Roster', 'Length',
'Blue_Gold', 'Blue_Kills', 'Blue_Towers', 'Blue_Dragons', 'Blue_Barons',
'Blue_RiftHerald', 'Red_Gold', 'Red_Kills', 'Red_Towers', 'Red_Dragons',
'Red_Barons', 'Red_RiftHerald', 'Diff_Gold', 'Diff_Kills', 'Diff_Towers',
'Diff_Dragons', 'Diff_Barons', 'Diff_RiftHerald', 'Tournament']
    result['Loser'] = ''
    result = result[['Date','Patch','Blue', 'Red', 'Winner','Loser','Blue_Bans','Red_Bans', 
'Blue_Picks', 'Red_Picks', 'Blue_Roster', 'Red_Roster', 'Length',
'Blue_Gold', 'Blue_Kills', 'Blue_Towers', 'Blue_Dragons', 'Blue_Barons',
'Blue_RiftHerald', 'Red_Gold', 'Red_Kills', 'Red_Towers', 'Red_Dragons',
'Red_Barons', 'Red_RiftHerald', 'Diff_Gold', 'Diff_Kills', 'Diff_Towers',
'Diff_Dragons', 'Diff_Barons', 'Diff_RiftHerald', 'Tournament']]
    #modify format of columns to ascii characters
    result['Blue_Roster'] = [i.replace(' • ',',') for i in result['Blue_Roster']]
    result['Red_Roster'] = [i.replace(' • ',',') for i in result['Red_Roster']]
    result.reset_index(drop=True, inplace=True)
    #Changer winner column to team name
    for i,k in result.iterrows():
        if k['Winner'] == 'blue':
            k['Winner'] = k['Blue']
            k['Loser'] = k['Red']
        elif k['Winner'] == 'red':
            k['Winner'] = k['Red']
            k['Loser'] = k['Blue']
            
            
    
    return result
#Export as csv to modify in Tableau
#Use Tournaments file that has list of tournaments from lol.gamepedia.com        
test_na = historical_tournament_data('Tournaments.csv')
test_na.to_excel('Test.xlsx', index=False)



































        
"""     
TO DO:
- Clean up missing data
- export to postgres/sql file
- make this applicable for all regions.        
        
"""       

    
    
    
