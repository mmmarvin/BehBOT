########################
# This file is part of BehBOT.
#
# BehBOT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BehBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BehBOT. If not, see <https://www.gnu.org/licenses/>.
########################
def tokenizeKeyValue(string, delimiter):
	if len(string) > 0:
		i = 0
		while i < len(string) and string[i] == ' ':
			i += 1
			
		j = i
		
		while j < len(string) and string[j] != delimiter:
			j += 1
			
		if i != j:
			command = string[i:j]
			value = string[j:len(string)]
			if len(value) > 0 and value[0] == delimiter:
				value = value[1:len(value)]
			
			return (command, value)
			
	return ("", "")

def tokenize(string, delimiter):
	ret = []
	
	i = 0
	while i < len(string):
		while i < len(string) and string[i] == delimiter:
			i += 1
			
		j = i
		
		while j < len(string) and string[j] != delimiter:
			j += 1
			
		if i != j:
			ret.append(string[i:j])
			i = j
			
	return ret
	
def combineTokens(tokens, separator = ' '):
	ret = ""
	
	if len(tokens) > 0:
		ret += tokens[0]
		for i in range(1, len(tokens)):
			ret += separator
			ret += tokens[i]
			
	return ret
