# Developed by Matthew Mifsud

from Parser import parse
from SemanticCodeGen import expressionBuilder

parseStatus = parse() # Parser calls Scanner and parses collected tokens
expression = expressionBuilder(parseStatus) # If parsing was a success, expression is built using Semantic

print(expression) # Outputting result