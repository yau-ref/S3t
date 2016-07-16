#! /usr/bin/python3

class Task(object):
  
  def __init__(self, name, timeMarks, issues = None):
    self.name = name
    self.timeMarks = timeMarks
    self.issues = issues if issues is not None else []
  
  def fromLine(line):
    split = line.split('-')
    taskName = split.pop().strip()
    timeMarks = [timeMark.strip() for item in split for timeMark in item.split(',')]
    return Task(taskName, timeMarks)
    
  def totalTime

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
        day.append(Task.fromLine(line)) 
      else:
        day[-1].issues.append(line.strip())
days.append(day)

for day in days:
  for task in day:
    print(task.name)
    print(task.timeMarks)
    print(task.issues)
  print('===================')
