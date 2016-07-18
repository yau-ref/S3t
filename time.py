#! /usr/bin/python3
from datetime import datetime, timedelta
from functools import reduce
from itertools import takewhile, groupby
import sys
import argparse
    
class Task:
  
  def __init__(self, name, timeMarks, issues = None):
    self.name = name.capitalize()
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
    self.title = datetime.strptime(title, '%d.%m.%y').date()
    self.tasks = tasks if tasks is not None else []
  
  def totalTime(self):
    return reduce(lambda a, b: a + b.totalTime(), self.tasks, 0)       

def readFromFile(fileName):
  def startNewDay(day, days, title):
    if day is not None:
      days.append(day)
    return Day(title)
  days = []
  day = None
  with open(fileName, 'r') as file:
    for line in file:
      if line.startswith('#'):
        day = startNewDay(day, days, line.strip('# \n'))
      elif line.strip():
        if not line.startswith(' '):
          day.tasks.append(Task.fromLine(line)) 
        else:
          day.tasks[-1].issues.append(line.strip())
  days.append(day)
  days.reverse()
  return days


def printReport(days):
  totalTime = 0
  uniqueTasks = {}
  for day in days:
    for task in day.tasks:
      totalTime += task.totalTime()
      acc = uniqueTasks.get(task.name, [])
      acc.append(task)
      uniqueTasks[task.name] = acc

  print('Total time:', round(totalTime, 2))
  print()
   
  triplets = []
  for taskName, tasks in uniqueTasks.items():
    taskTime = 0
    issues = set()
    for task in tasks:
      taskTime += task.totalTime()
      for issue in task.issues:
        issues.add(issue)
    triplets.append((taskName, round(taskTime, 2), issues))
  triplets.sort(key = lambda t: -t[1])
  for t in triplets:
    i = '(' + ', '.join(t[2]) + ')' if t[2] else ''
    print("{:5.2f} | ".format(t[1]), t[0], i)

parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', default='time.md', dest='fileName', help='path to tasks file')
parser.add_argument('-a', '--all', action='store_true', dest='all', help='show all')
parser.add_argument('-w', '--week', action='store_true', dest='week', help='show week (from monday until today)')
parser.add_argument('-m', '--month', action='store_true', dest='month', help='show month')
parser.add_argument('-r', '--report', action='store_true', dest='report', help='shows report')
parser.add_argument('-p', '--previous', action='store_true', dest='previous', help='`previous` modifier')

args = parser.parse_args()

if [args.all, args.week, args.month].count(True) > 1:
  parser.print_help()
  sys.exit()
 
days = readFromFile(args.fileName)
today = datetime.now().date()

if not args.all:
  if args.week:
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    if args.previous:
      start -= timedelta(days=7)
      end -= timedelta(days=7)
  elif args.month:
    start = today - timedelta(days=today.day)
    end = today
  else:
    start = today if not args.previous else today - timedelta(days=1)
    end = start  
  days = [day for day in days if day.title >= start and day.title <= end]

if not days:
  print("No records")
  sys.exit()

if args.report:
  printReport(days)
else:   
  for day in days:
    print(day.title,': ', round(day.totalTime(), 2), 'h')
    for task in day.tasks:
      print()
      print(' -', task.name.capitalize(),': ',round(task.totalTime(), 2), 'h')
      for issue in task.issues:
        print('    ', issue)
    print()
    
 
## TODO:
# money
# month
# python style
