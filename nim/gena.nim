#!/bin/nim/

# 1st we need to get all gena blocks and use cases

## Gena Block

# Generate few lines
# My name is %{John,Bob,Alice}%.
# My name is John.
# My name is Bob.
# My name is Alice.

# Gen code, but also name a variable (so it can be reused)
# My name is %{name:John,Bob,Alice}%.
# My name is John.
# My name is Bob.
# My name is Alice.




# GenaBlocks {name: string, blocks: list<string>}
# for genaBlock in genaBlocks:
#  for value in genaBlock:
#   gen with replace use case with value
#   gen with replace genaBlock.raw with value

# 0. получити список слів, та можна назва списка
# 1. получити підставлюючі слова

#type Range:
#  


import std/tables


# returns 
proc getRanges(gena: string) =
      var ranges: Table[system.string, system.string] = initTable[string, string]()
      values = gena.split(":")
      #if it has only 1 element than auto name with an index.
      if 2: values=values[2].split(",")
      elif 1: name="#0", values=values[0]
      else: return
      return name, values

getRanges()
