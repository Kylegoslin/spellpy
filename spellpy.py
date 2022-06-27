import requests
import json
from nltk import ngrams
from bs4 import BeautifulSoup
import urllib.request
import urllib
import distance, re 


class SearchResult:
    baseTerm = ''
    associated = dict()
    
   
words_counts = {}
data_list = []   
def generateWildcardCorpus(term1, term2):
    global words_counts, data_list
    
    generations = list()
    word = sentence
    
    

    
    print("--- one astrix")    
    
    #
    # One astrix matches
    wildlocation = 0
    new_character = '*'

    print("-------")
    word = term1
    for x in range(0,len(word)):
        
        str1 = word
        str1 = str1[:wildlocation] + new_character + str1[wildlocation+1:]
        

        outputTemp = ("~" + str1)
        print(outputTemp)
        generations.append('"'+outputTemp + '' + term2+'"') # two double quotes added
        wildlocation = wildlocation + 1 
    
    
    
    
    print()
    
    
    
    print("--- two astrix")
    #
    #    two astrix matches
    #
    #
   
    wildlocation = 0
    new_character = '**'

    print("-------")
    word = term1
    for x in range(0,len(word)):
        
        str1 = word
        str1 = str1[:wildlocation] + new_character + str1[wildlocation+2:]
        

        outputTemp = ("~" + str1)
        print(outputTemp)
        generations.append('"'+outputTemp + '' + term2+'"') # two double quotes added
        wildlocation = wildlocation + 1 
    


        
    
    
    

    print("--- remove char")    
    
    #Remove one character at increasing position
    
    wildlocation = 0

    print("-------")
    word = term1
    for x in range(0,len(word)):
        
        str1 = word
        str1 = str1[:wildlocation+1] + str1[wildlocation+2:]
        

        outputTemp = ("~" + str1)
        print(outputTemp)
        generations.append('"'+outputTemp + '' + term2+'"') # two double quotes added
        wildlocation = wildlocation + 1 



    print("--- one astrix insert additional character")    
    
    #
    # One astrix matches
    wildlocation = 0
    new_character = '*'

    print("-------")
    word = term1
    for x in range(0,len(word)):
        
        str1 = word
        str1 = str1[:wildlocation] + new_character + str1[wildlocation:]
        

        outputTemp = ("~" + str1)
        print(outputTemp)
        generations.append('"'+outputTemp + '' + term2+'"') # two double quotes added
        wildlocation = wildlocation + 1 
    
    

  










    print("all generations.........")
    for x in generations:
        print(x)

        input = "https://en.wikipedia.org/w/index.php?search="+x+"&title=Special:Search&limit=100&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1"
        print(input)

        f = urllib.request.urlopen(input)
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser') 
        f.close()
        
        
        
        resultDiv = soup.find_all("div", {"class": "searchresult"})
        for x in resultDiv:
            #print(x.get_text())
            text = x.get_text()
            text = text.lower().replace(',','').replace('"','').replace('.','')
            stripped_string = re.sub(r'[^a-zA-Z ]+', '', text)
            data_list.append(stripped_string)
            

         
        for text in data_list:
           for word in text.split():
              if word in words_counts:
                words_counts[word] += 1
              else:
                words_counts[word] = 1  






   



words_counts = {}
data_list = []
# wildcard string generator
def generateCorpus(sentence):
    global words_counts, data_list
    sentence = sentence.replace(' ','+')
   

   
    input = "https://en.wikipedia.org/w/index.php?search="+sentence+"&title=Special:Search&limit=100&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1"
    print(input)

    f = urllib.request.urlopen(input)
    content = f.read()
    soup = BeautifulSoup(content, 'html.parser') 
    f.close()
    
    
    
    resultDiv = soup.find_all("div", {"class": "searchresult"})
    for x in resultDiv:
        #print(x.get_text())
        text = x.get_text()
        text = text.lower().replace(',','').replace('"','').replace('.','')
        stripped_string = re.sub(r'[^a-zA-Z ]+', '', text)
        data_list.append(stripped_string)
        

     
    for text in data_list:
       for word in text.split():
          if word in words_counts:
            words_counts[word] += 1
          else:
            words_counts[word] = 1    
    
    
    #for x in words_counts:
    #    print(x + ' ' + str(words_counts[x]))
 

        
        
        
results = list()
 
''''
Find out the number of times both words
showed up together in context
''' 
def getCount(term):
    url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srwhat=text&srnamespace=0&srsearch="'+term+'"&srinfo=totalhits&srlimit=1&srprop=&format=json'
    r = requests.get(url)
    
    li = r.json()

    part1 = str(li['query']).split(',')
    trimbit = "{'searchinfo': {'totalhits':"
    final = str(part1[0])[len(trimbit):-1]
    return final
  




def findReplacement(term):
    print("finding replacement")

    

    
    simValues = {}
    
    for x in words_counts:
        #print(x + ' ' + str(words_counts[x]))
        
        res = distance.levenshtein(term, x)
        
        simValues[x] = res
        #print(x + " distance to "+ term + ' is '+ str(res))

    simValues = dict(sorted(simValues.items(), key=lambda item: item[1]))
    smallSet = dict()
    lowestTerm = ''
    lowestVal = 100.0
    
    counter = 0
    #
    # add top 5 candiates
    #
    #
    for x in simValues:
       
   
        
        #score = getCount(x)
        print(x + ' ' + str(simValues[x]))
        
        
        smallSet[x] = simValues[x]
        counter = counter + 1
       
         
        if counter > 10:
            break;
            
            
            
            
    
    #
    # Check count and apply filter remove non words
    #
    secondSet = dict()
    print("checking count")
    ## Validation step based on number of records
    for item in smallSet:
        countTotal = getCount(item)
        # arbitrary number to make cutoff of real words
        if int(countTotal) > 500:
            print("is greater adding..")
            secondSet[item] = int(countTotal)

    
    vals = dict(sorted(secondSet.items(), key=lambda item: item[1], reverse=True))
    print(".............. sorted ...........")
    
    print("adding result to vector")
    tempSet = SearchResult()
    tempSet.baseTerm = term
    tempSet.associated = vals
    results.append(tempSet)
    
    
    for x in vals:
        print(x + ' ' + str(vals[x]))
        
  
        
        
    return ''
    
'''
--------------------------
 MAIN
--------------------------
'''
data = dict()

import sys

#query = 'obbamma+fanily'
#number = 1
query = sys.argv[1]
number = sys.argv[2]
print(query + " " +str(number))


sentence = query
final = ''
 
#
# Generate the wildcard corpus
#
for term in sentence.split('+'): 
    generateWildcardCorpus(term,'') 




for term in sentence.split('+'): 
    replacement = findReplacement(term)
    print("replacement: " + replacement)
    final = final + replacement + ' ' 






totalLength = len(sentence.split('+'))
final = dict()  



if totalLength == 1:
    baseTerm1 = results[0].baseTerm
    terms1 = results[0].associated

    for term1 in terms1:
        complete = term1
        print(complete)
        co = getCount(complete)
        final[complete] = int(co)
        

if totalLength == 2:
    baseTerm1 = results[0].baseTerm
    terms1 = results[0].associated
    
    baseTerm2 = results[1].baseTerm
    terms2 = results[1].associated

    for term1 in terms1:
        
        for term2 in terms2:
            complete = term1 + ' ' + term2
            print(complete)
            co = getCount(complete)
            final[complete] = int(co)
            
            
            
if totalLength == 3:
    print("total length is 3")
    baseTerm1 = results[0].baseTerm
    terms1 = results[0].associated
    
    baseTerm2 = results[1].baseTerm
    terms2 = results[1].associated

    baseTerm3 = results[2].baseTerm
    terms3 = results[2].associated

    for term1 in terms1:
        #print("term 1" + term1)
        
        for term2 in terms2:
            print("term 2" + term2)
            
            for term3 in terms3:
                complete = term1 + ' ' + term2 + ' ' + term3
                print(complete)
                co = getCount(complete)
                final[complete] = int(co)




if totalLength == 4:
    baseTerm1 = results[0].baseTerm
    terms1 = results[0].associated
    
    baseTerm2 = results[1].baseTerm
    terms2 = results[1].associated

    baseTerm3 = results[2].baseTerm
    terms3 = results[2].associated
    
    baseTerm4 = results[3].baseTerm
    terms4 = results[3].associated
    
    for term1 in terms1:
        
        for term2 in terms2:
        
            for term3 in terms3:
                for term4 in terms4:
            
                    complete = term1 + ' ' + term2 + ' ' + term3 + ' ' + term4
                    print(complete)
                    co = getCount(complete)
                    final[complete] = int(co)

if totalLength == 5:
    baseTerm1 = results[0].baseTerm
    terms1 = results[0].associated
    
    baseTerm2 = results[1].baseTerm
    terms2 = results[1].associated

    baseTerm3 = results[2].baseTerm
    terms3 = results[2].associated
    
    baseTerm4 = results[3].baseTerm
    terms4 = results[3].associated

    baseTerm5 = results[4].baseTerm
    terms5 = results[4].associated

    for term1 in terms1:
        
        for term2 in terms2:
        
            for term3 in terms3:
            
                for term4 in terms4:
                
                    for term5 in terms5:
                        complete = term1 + ' ' + term2 + ' ' + term3 + ' ' + term4 + ' ' + term5
                        print(complete)
                        co = getCount(complete)
                        final[complete] = int(co)







  
vals = dict(sorted(final.items(), key=lambda item: item[1], reverse=True))

print("after process.......")


if totalLength == 1:
    topTerm = ''
    lowestVal = 500
    for x in vals:
        res = distance.levenshtein(sentence, x)
        print(x + str(res))
        if int(res) < lowestVal:
            topTerm = x
            lowestVal = int(res)
            
            
    print("Final term: " + topTerm)
    output = open('output/sim10/' + str(number) + '.txt','w')
    output.write(topTerm)
    output.close()
else:    
    print("longer than 1 term")
    for x in vals:
        print(x + ' ' + str(vals[x]))
        
        output = open('output/sim10/' + str(number) + '.txt','w')
        output.write(x)
        output.close()
        break







