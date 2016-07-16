#! /usr/bin/python3
from datetime import datetime

class Task(object):
  
  def __init__(self, name, timeMarks, issues = None):
    self.name = name
    self.timeMarks = timeMarks
    self.issues = issues if issues is not None else []
    self._totalTime = None
     
  def totalTime(self):
    if self._totalTime is None:
      def parseMark(mark):
        return datetime(1,1,1,*map(int, mark.split('.')))
      times = list(map(parseMark, self.timeMarks))
      pairs = zip(times[0::2], times[1::2])
      sums = map(lambda pair: (pair[1] - pair[0]).seconds / 60, pairs)
      self._totalTime = sum(sums) / 60
    return self._totalTime
    
  def fromLine(line):
    split = line.split('-')
    taskName = split.pop().strip()
    timeMarks = [timeMark.strip() for item in split for timeMark in item.split(',')]
    return Task(taskName, timeMarks)
      
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
    print(task.totalTime())
  print('===================')
