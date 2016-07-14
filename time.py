#! /usr/bin/python3
from collections import namedtuple
Task = namedtuple('Task', ['name', 'timeMarks', 'issues'])

def parseTask(task):
  split = task.split('-')
  taskName = split.pop().strip()
  timeMarks = [timeMark.strip() for item in split for timeMark in item.split(',')]
  return Task(taskName, timeMarks, [])

def startNewDay(day, days):
  if day is not None:
    days.append(day)  
  return []


days = []
day = None
with open('time.md', 'r') as file:
  for line in file:
    if line.startswith('#'):
      day = startNewDay(day, days)
    elif line.strip():
      if not line.startswith(' '):
        day.append(parseTask(line))        
      else:
        day[-1].issues.append(line.strip())
        

for day in days:
  for task in day:
    print(task.name)
    print(task.timeMarks)
    print(task.issues)
