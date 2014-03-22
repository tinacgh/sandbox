from __future__ import print_function
# Create your views here.

import os

from django.db.transaction import commit_on_success
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rhymes.rhymeapp.models import Word, Ending

def home(request):
    #return render(request, 'rhymeapp/index.html')
    count = Word.objects.count()
    #return HttpResponse(list(Word.objects.all())[0])
    return HttpResponse(count)

def match(request, input):
    endings = " ".join(input.split("-"))
    matches = list(Word.objects.filter(fuzzyending=endings))
    #return HttpResponse(matches[0])
    return render(request, "rhymeapp/listmatches.html", {"matches": matches})

def isascii(s):
    return all(ord(c) < 128 for c in s)
    
def search(request):
    matches = []

    if request.method == 'GET':
        q = request.GET.get('q', '')
        if isascii(q.replace(" ", "")):
            endings = extractendings("[ "+q+" ]", False)
            print(endings)
        else:
            try:
                entries = Word.objects.filter(entry__icontains=q)
                endings = ""
                for e in entries:
                    if q == e.entry.split()[1]:
                        endings = extractendings(e.entry, False)
                        break
                # return HttpResponse(endings)
            except Exception as e:
                return HttpResponse(e)
                # endings = "a"
        matches = list(Word.objects.filter(fuzzyending=endings))
    return render(request, 'rhymeapp/search.html', {"matches": matches, 'endings': endings})
    
def gettrad(entry):
    return entry.split()[0]

def prepareconvtable():
    msg = ""
    #os.chdir("/home/mandarinpandarin/rhymes/rhymes/rhymeapp")
    os.chdir("/home/heitor/sandbox/rhymes/rhymes/rhymeapp")
    table = open("convtable.txt")
    py2alt = {}
    for line in table:
        endings = line.strip().split(",")
        checkword = len(Ending.objects.filter(pinyin=endings[0]))
        if not checkword:
            msg += "Adding " + endings[0] + "<br>"
            ending = Ending(pinyin=endings[0], modified=endings[1])
            ending.save()
        else:
            msg += endings[0] + " already there.<br>"
    table.close()
    return msg

def convert(syl, savetone=True):
    if syl[-1].isdigit():
        base = syl[0:-1]
    else:
        base = syl
    if savetone:
        tone = syl[-1]
    else:
        tone = ""
    try:
        modifiedbase = Ending.objects.get(pinyin=base).modified
    except Ending.DoesNotExist:
        modifiedbase = base
    #return modifiedbase + tone
    #discard consonants
    vowels = set("aeiouwy")
    index = 0
    for char in modifiedbase:
        #print("char", char)
        if char in vowels:
            #print("found at index", index)
            return modifiedbase[index:] + tone
        index += 1
    return modifiedbase + tone

#convert("wan3")
#convert("quan2")

def extractendings(entry, savetone):
    py = entry[entry.find("[") + 1:entry.find("]")]
    return " ".join(map(lambda s: convert(s, savetone), py.split()))

def populatedb(request):
    convmsg = prepareconvtable()
    msg = convmsg
    cedict = open("cedictsubset.txt")
    cedict = open("cedictsnippet.txt")
    for line in cedict:
        trad = gettrad(line)
        checkword = len(Word.objects.filter(trad=trad))
        if not checkword:
            # msg += "adding " + trad + "<br>"
            print("adding " + trad)
            fullendings = extractendings(line, True)
            fuzzyendings = extractendings(line, False)
            newword = Word(trad=trad, entry=line, fullending=fullendings,
            fuzzyending=fuzzyendings)
            newword.save()

            # batch save
            # from django.db.transaction import commit_on_success
            #@commit_on_success
            #def lot_of_saves(queryset):
            #  for item in queryset:
            #  modify_item(item)
            #  item.save()
        else:
            pass
            # msg += trad + " already exists."

    #return HttpResponse(msg)
    return HttpResponse("Finished build.")
