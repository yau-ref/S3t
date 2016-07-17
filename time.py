#! /usr/bin/python3
from datetime import datetime
from functools import reduce
    
class Task:
  
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
  

class Day:

  def __init__(self, title, tasks = None):
    self.title = title
    self.tasks = tasks if tasks is not None else []
  
  def totalTime(self):
    return reduce(lambda a, b: a + b.totalTime(), self.tasks, 0)      
  
      
def startNewDay(day, days, title):
  if day is not None:
    days.append(day)
  return Day(title)

days = []
day = None
with open('time.md', 'r') as file:
  for line in file:
    if line.startswith('#'):
      day = startNewDay(day, days, line.strip('# \n'))
    elif line.strip():
      if not line.startswith(' '):
        day.tasks.append(Task.fromLine(line)) 
      else:
        day.tasks[-1].issues.append(line.strip())
days.append(day)

for day in days:
  print(day.title,': ', round(day.totalTime(), 2))
  for task in day.tasks:
    print(' -', task.name.capitalize(),' [', round(task.totalTime(), 2), ']')
    for issue in task.issues:
      print('    ', issue)
    print()
  print()
