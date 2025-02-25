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
