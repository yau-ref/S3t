#! /usr/bin/python3

block = False
blocks = []

with open('time.md', 'r') as file:
  for line in file:
    item = line 
    blocks.append(item)

for i in blocks:
  print(i)
