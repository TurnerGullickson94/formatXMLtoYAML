#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 01 08:35:33 2022
@author: rivera

This is a text processor that allows to translate XML-based events to YAML-based events.
CAREFUL: You ARE NOT allowed using (i.e., import) modules/libraries/packages to parse XML or YAML
(e.g., yaml or xml modules). You will need to rely on Python collections to achieve the reading of XML files and the
generation of YAML files.
"""
from asyncio import events
from datetime import datetime
from datetime import date
from datetime import time
import datetime
import sys
import re
from time import time
from collections import OrderedDict
from operator import getitem

def print_hello_message(message):
    """Prints a welcome message.

    Parameters
    ----------
    message : str, required
        The file path of the file to read.

    Returns
    -------
    void
        This function is not expected to return anything
    """
    print(message)

def findEventFile(input):
    '''takes the argument on the line and outputs the filename'''
    name = re.split('=', input)
    return str(name[1])

def parseStart(input):
    '''takes the arguament on the line and outputs the startdate in y/m/d format'''
    list = re.split('=',input)
    startDate = datetime.datetime.strptime(list[1],"%Y/%m/%d")
    #print(startDate)
    return startDate

def parseEnd(input):
    '''takes the arguament on the line and outputs the end date in y/m/d format'''
    list = re.split('=',input)
    endDate = datetime.datetime.strptime(list[1],"%Y/%m/%d")
    #print(endDate)
    return endDate

def createLine(filename):
    '''takes file and outputs a list of lines'''
    file = open(filename)
    lines = file.readlines()
    return lines

def parseEvents(eventLines, eventDict):
    '''takes an events file and creates a dictionary'''
    dictKey = -1
    for line in eventLines:
        if("<event>" in line):
            dictKey+=1
            eventDict[dictKey] = {}
            eventDict[dictKey]["fullDate"] = datetime.datetime.min
        elif("<id>" in line):
            id = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["id"] = id
        elif("<description>" in line):
            description = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["description"] = description
        elif("<location>" in line):
            location = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["location"] = location
        elif("<day>" in line):
            dAY = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["day"] = dAY
            eventDict[dictKey]["fullDate"] = eventDict[dictKey]["fullDate"].replace(day =int(dAY[0]))
        elif("<month>" in line):
            mONTH = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["month"] = mONTH
            eventDict[dictKey]["fullDate"] = eventDict[dictKey]["fullDate"].replace(month = int(mONTH[0]))
        elif("<year>" in line):
            yEAR = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["year"] = yEAR
            eventDict[dictKey]["fullDate"] = eventDict[dictKey]["fullDate"].replace(year = int(yEAR[0]))
        elif("<start>" in line):
            start = re.findall(r'>(.*?)<', line)
            twentyfourStart = datetime.datetime.strptime(start[0], '%H:%M')
            twelveStart = twentyfourStart.strftime('%I:%M %p')
            eventDict[dictKey]["start"] = twelveStart
            splitStart = start[0].split(':')
            eventDict[dictKey]["fullDate"] = eventDict[dictKey]["fullDate"].replace(hour = int(splitStart[0]))
            eventDict[dictKey]["fullDate"] = eventDict[dictKey]["fullDate"].replace(minute = int(splitStart[1]))
        elif("<end>" in line):
            end = re.findall(r'>(.*?)<', line)
            twentyfourEnd = datetime.datetime.strptime(end[0], '%H:%M')
            twelveEnd = twentyfourEnd.strftime("%I:%M %p")
            eventDict[dictKey]["end"] = twelveEnd
        elif("<broadcaster>" in line):
            broadcaster = re.findall(r'>(.*?)<', line)
            eventDict[dictKey]["broadcaster"] = broadcaster

def parseCircuits(circuitLines, circuitDict):
    '''takes the circuits file and creates a dictionary'''
    dictKey = -1
    for line in circuitLines:
        if("<circuit>" in line):
            dictKey+=1
            circuitDict[dictKey] = {}
        elif("<id>" in line):
            id = re.findall(r'>(.*?)<', line)
            circuitDict[dictKey]["id"] = id
        elif("<name>" in line):
            name = re.findall(r'>(.*?)<', line)
            circuitDict[dictKey]["name"] = name
        elif("<location>" in line):
            location = re.findall(r'>(.*?)<', line)
            circuitDict[dictKey]["location"] = location
        elif("<timezone>" in line):
            timezone = re.findall(r'>(.*?)<', line)
            circuitDict[dictKey]["timezone"] = timezone
        elif("<direction>" in line):
            direction = re.findall(r'>(.*?)<', line)
            circuitDict[dictKey]["direction"] = direction

    return circuitDict

def parseBroadcasters(broadcastLines, broadcastDict):
    '''takes broadcasters file and creates a dictionary'''
    dictkey = -1
    for line in broadcastLines:
        if ("<broadcaster>" in line):
            dictkey += 1
            broadcastDict[dictkey] = {}
        elif("<id>" in line):
            id = re.findall(r'>(.*?)<', line)
            broadcastDict[dictkey]["id"] = id
        elif("<name>" in line):
            name = re.findall(r'>(.*?)<', line)
            broadcastDict[dictkey]["name"] = name
        elif("<cost>" in line):
            cost = re.findall(r'>(.*?)<', line)
            broadcastDict[dictkey]["cost"] = cost

    return broadcastDict

def findLocation(eventEntry, circuitsDict):
    '''uses location stored in events to find the actual location in circuits'''
    for key in circuitsDict:
        if (eventEntry == circuitsDict[key]['id'][0]):
            return circuitsDict[key]['location'][0]

def findCircuit(eventEntry, circuitsDict):
    '''uses location stored in events to find the circuit name'''
    for key in circuitsDict:
        if (eventEntry == circuitsDict[key]['id'][0]):
            return circuitsDict[key]['name'][0]

def findDirection(eventEntry, circuitsDict):
    '''uses the location stored in events to find the race direction'''
    for key in circuitsDict:
        if (eventEntry == circuitsDict[key]['id'][0]):
            return circuitsDict[key]['direction'][0]

def findTimeZone(eventEntry, circuitsDict):
    '''uses the location stored in events to find the timezone'''
    for key in circuitsDict:
        if (eventEntry == circuitsDict[key]['id'][0]):
            return circuitsDict[key]['timezone'][0]

def findBroadcasters(eventEntry, broadcastersDict):
    '''uses the broadcaster stored in events to find the broadcasters'''
    idList = eventEntry.split(',')
    namelist = []
    for key in broadcastersDict:
        for item in range(len(idList)):
            if (idList[item] == broadcastersDict[key]['id'][0]):
                namelist.append(broadcastersDict[key]['name'][0])
    return namelist

def broadcasterPrintLoop(broadcasterList,file):
    '''if there is more than one broadcaster, outputs both in yaml format'''
    for entry in broadcasterList:
        file.write(f'\n        - {entry}')

def createOutputFile(startDate, endDate, eventsDict, circuitsDict, broadcastersDict):
    '''takes all the information stored and outputs as a yaml file in the requested format'''
    outputfile = open("output.yaml", "w")
    outputfile.write("events:")
    curdate = startDate
    previousDate = None

    while(curdate<=endDate):
        res = OrderedDict(sorted(eventsDict.items(),key = lambda x: getitem(x[1], 'fullDate')))
        for entry in res:
            date = eventsDict[entry]["fullDate"]
            if (curdate.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d")):
                    newEvent = date.strftime("%d-%m-%Y")
                    if newEvent!=previousDate:
                        previousDate=newEvent
                        outputfile.write(f'\n  - {newEvent}:')
                    location = findLocation(eventsDict[entry]["location"][0], circuitsDict)
                    circuit = findCircuit(eventsDict[entry]["location"][0], circuitsDict)
                    direction = findDirection(eventsDict[entry]["location"][0], circuitsDict)
                    timezone = findTimeZone(eventsDict[entry]["location"][0], circuitsDict)
                    #print(eventsDict[entry]["broadcaster"][0])
                    when = date.strftime("%A, %B %d, %Y")
                    broadcasters = findBroadcasters(eventsDict[entry]["broadcaster"][0], broadcastersDict)
                    outputfile.write(f'\n    - id: {eventsDict[entry]["id"][0]}')
                    outputfile.write(f'\n      description: {eventsDict[entry]["description"][0]}')
                    outputfile.write(f'\n      circuit: {circuit} ({direction})')
                    outputfile.write(f'\n      location: {location}')
                    outputfile.write(f'\n      when: {eventsDict[entry]["start"]} - {eventsDict[entry]["end"]} {when} ({timezone})')
                    outputfile.write(f'\n      broadcasters:')
                    broadcasterPrintLoop(broadcasters,outputfile)

        curdate = curdate + datetime.timedelta(days=1)
    outputfile.close()
def main():
    """The main entry point for the program.
    """

    eventFilename = findEventFile(sys.argv[3])
    broadcastFileLines = createLine("broadcasters.xml")
    circuitFileLines = createLine("circuits.xml")
    eventFileLines = createLine(eventFilename)

    circuitsDict = {}
    broadcastersDict = {}
    eventsDict = {}

    startDate = parseStart(sys.argv[1])
    endDate = parseEnd(sys.argv[2])
    parseBroadcasters(broadcastFileLines, broadcastersDict)
    parseCircuits(circuitFileLines, circuitsDict)
    parseEvents(eventFileLines, eventsDict)

    createOutputFile(startDate, endDate, eventsDict, circuitsDict, broadcastersDict)



if __name__ == '__main__':
    main()