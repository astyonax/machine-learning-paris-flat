
# coding: utf-8

# # Web scraping for flats
#
# Get some lists from ``leboncoin.fr``

# In[1]:

import hashlib
import urllib
import unidecode
import numpy as np
from string import atof,atoi
from pprint import pprint
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta

base_url='https://www.leboncoin.fr/locations/offres/ile_de_france/paris/'

urlget = urllib.urlopen


# ## Downlad page number
#
# The default search criteria are for flats with size > 30 sqm, in Paris.
# The function returns the `Beautifulsoup`-ped HTML of a given page.
# Each page contains a list of flats.

# In[3]:

def get_page_from_url(pgnr,base_url):
    CL_paris_apa_html="{0:s}?o={1:d}&sqs=2&ret=1&ret=2&ret=5".format(base_url,pgnr)
    print CL_paris_apa_html
    try:
        xpage = urlget(CL_paris_apa_html)
        CL_html = xpage.read()
        encoding = xpage.info()['content-type'].split('=')[-1]
    except IOError: # in case of network error
        print 'IOError'
        CL_html = ''
    try:
        return BS(CL_html.decode(encoding,'replace'),'lxml')
    except UnboundLocalError:
        return BS(CL_html.decode('latin-1','replace'),'lxml')
human_page=get_page_from_url(2,base_url)


# ## List flats urls from page
#
# From each page given by the previous function, we record the list of flats, their publication date, and pid.

# In[4]:

def get_listings_from_html(human_page,base_url):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime('%d/%m/%y')
    today = today.strftime('%d/%m/%y')

    apartments = human_page.findAll('a',attrs={'class':'list_item'})

    results=[]
    for item in apartments:
        try:
            title=unidecode.unidecode(''.join(item.select('h2.item_title')[0].contents).strip())
        except IndexError:
            continue
        insert_time = item.select('aside.item_absolute > p.item_supp')
        if not len(insert_time):
            continue
        insert_time = insert_time[0].contents[-1].strip().replace(u"Aujourd'hui",today)
        insert_time = insert_time.replace(u"Hier",yesterday)
        url = 'http:'+item.attrs['href']
        pid = url.split('/')[-1].split('.')[0]
        results.append({'insert_time':insert_time,'pid':pid,'url':url,'title':title})
        md5_input = title
        results[-1].update({'md5sum':hashlib.md5(md5_input).hexdigest()})

    return results
apas=get_listings_from_html(human_page,base_url)
# apas[1]


# In[5]:


# for jix in xrange(len(flats)):
#     keys=['insert_time','pid','url']
#     fl_ = {j:flats[jix] for j in keys}
#     flats[jix].update({'md5sum':hashlib.md5(str(fl)).hexdigest()})

# print flats[-1]


# ## From flat url to flat record
#
# We have the urls of all flats listed in CL.. well, we have the functions to get the urls, the actual work will be done at the end.
# Finally, we can get the informations out of each flat individual page. This is really boring, but needed. The results is a list of features for each flat. These features will need further refinement, that I will do in future notebooks

# In[6]:

def select2text(din):
    basic_string = [' '.join(list(j.stripped_strings)) for j in din]
#     basic_string =  [unidecode.unidecode(j) for j in basic_string]
    return basic_string

def make_col_name(nm):
    nm = unidecode.unidecode(nm)
    nm = nm.title()
    for sub in " ,./;'[]\<>?:{}|=+!@$%^&*()_-#":
        nm = nm.replace(sub,'')
    if nm[:2]=='Pi' and nm[-2:]=='es':
        nm='Pieces'
    if 'Meubl' in nm:
        nm = 'Meuble'
    return nm.strip()

# functions to process the raw features record
from collections import defaultdict as DDict
def default():
    return lambda out:out

def loyer(out):
    # process loyer
    lm = out['LoyerMensuel']
    lm = make_col_name(lm)
    eur = lm.split('Eur')[0].replace(' ','')
    out['LoyerMensuel']=atof(eur)
    # add a filed
    out['ChargesComprises'] = False
    if 'ChargesComprises' in lm:
        out['ChargesComprises'] = True
    return out

def surface(out):
    # process surface
    sr = out['Surface']
    sr = atof(sr.strip().split('m')[0])
    out['Surface'] = sr
    return out

def meublenonmeuble(out):
    #process MeubleNonMeuble
    mnm = out['Meuble']
    if 'Non' in mnm:
        out['Meuble'] = False
    else:
        out['Meuble'] = True
    return out

def ville(out):
    #process Ville
    vl = out['Ville']
    zipcode = atoi(vl.split()[-1])
    arrondissement = zipcode - 75000
    out['Arrondissement'] = arrondissement
    return out

unrawify_dict=DDict(default)
unrawify_dict['Ville']=ville
unrawify_dict['Meuble']=meublenonmeuble
unrawify_dict['Surface']=surface
unrawify_dict['LoyerMensuel']=loyer

def unrawify_apas(indict):
    outdict=indict.copy()
    for j in indict.keys():
        outdict.update(unrawify_dict[j](indict))
    return outdict

def apafeatures(apainfo):
    url = apainfo['url']
    apa=BS(urlget(url).read(),'lxml')
    col=select2text(apa.select('section.properties .property'))
    col = map(make_col_name,col)

    val=select2text(apa.select('section.properties .value'))

    lines = min(len(col),len(val))
    out = {}
    for i in xrange(lines):
        out[col[i]]=val[i]

    out = unrawify_apas(out)
    if len(val)!=len(col):
        out['Problematic']=True
    else:
        out['Problematic']=False


    out.update(apainfo)
    return out
# print apas[5]
# apafeatures(apas[5])


# ## A memoizing page getter
# As the docstring says: `sort of memoizing for apafeatures, specialized for the apas tuple`.
#
# This class saves its cache as pickle

# In[7]:

import cPickle as pkl
# from datetime import datetime as DT
import os
import time

class get_features_cache(object):
    """
        sort of memoizing for apafeatures, specialized for the flat record
    """
    def __init__(self,fname,maxdt=-1):
        self.fname=fname
        try:
            self.db=pkl.load(open(fname,'rb'))
        except IOError:
            self.db=[]
        self.clids=[j['md5sum'] for j in self.db]
        self.dirty = 0
        self.upd_time = time.strftime('%H:%M %d/%m/%y')

    def __call__(self,apainfo):
        url = apainfo['url']
        clid = apainfo['md5sum']
        ins_time = apainfo['insert_time']
        # check if app was already retrieved
        if clid in self.clids:
            #TODO check if retrieved version is too old/invalid
            return {'data':self.db[self.clids.index(clid)],'from_cache':True}
        else:
            #retrieve data, store, update self.clids, and finally return
            out = apafeatures(apainfo)

            self.clids.append(clid)
            self.db.append(out)
            self.dirty = 1
            self.upd_time = time.strftime('%H:%M %d/%m/%y')
            return {'data':out,'from_cache':False}

    def __len__(self):
        return len(self.db)

    def __del__(self):
        self._save()

    def _save(self):
        if self.dirty:
            print "saving apas db"
            print "db rows: {0:d}".format(len(self.db))
            pkl.dump(self.db,open(self.fname,'wb'))
            self.dirty = 0

    def upd_date(self):
        return self.upd_time


# ## Ask pages at random times
#
# This is class that behaves as a function (see the `__call__`) that waits a random time before retrieving the requested URL.
# The waiting time is sampled from a Poisson distribution.

# In[8]:

# ----------------------------------------------------------
#            Poissonian waiting time in the urlget function
class urlgetter(object):
    def __init__(self,waiting_time):
        self.mean=waiting_time

    def __call__(self,url):
        import time
        #waiting time [s]
        wt = self.poisson()
        time.sleep(wt)
        return urllib.urlopen(url)

    def poisson(self):
        from math import log
        from random import random
        return -log(1.0 - random()) / self.mean


# ## Put all togheter
#
# The culprit of all these efforts, the loop that rules them all, where the  work is  truly done.

# In[9]:

import random
pages=range(1,7)
# random.shuffle(pages)

apagetter = get_features_cache(fname='data/LBClocations.pkl',)
print 'The {2:s} the db {0:s} contains {1:d} locations'.format(apagetter.fname,len(apagetter),apagetter.upd_date())
urlget = urlgetter(1/.5)
failed=[]
flats = []
class Found(Exception): pass

try:
    for page in pages:
        human_page=get_page_from_url(page,base_url)
        apas=get_listings_from_html(human_page,base_url)
        print 'page', page
        if not len(apas): break
        for count,apa in enumerate(apas):
            try:
                last=apagetter(apa)
#                 print _['data']['title'],_['data']['insert_time']
            except Exception,msg:
                failed.append(apa)
                print 'failed #{1:d} {0:s}'.format(apa,count)
                print msg
#             if _['from_cache']: raise Found
except Found:
    pass
apagetter._save()
print 'last downloaded record:'
print 'title:',last['data']['title']
print 'insert time:',last['data']['insert_time']


# In[10]:

flats = apagetter.db
len(flats)


# ## to the pandas

# In[11]:

import pandas as pd
from datetime import datetime
df = pd.DataFrame(flats)
df.columns

months =  unidecode.unidecode(u"""
jan,fév,mar,avr,mai,jun,jul,aoû,sep,oct,nov,déc
jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec
""").split()
months = zip(*[j.split(',') for j in months])


def correct_instime_format(j):
    timefmt1 = '%d %b, %H:%M' # 25 oct, 11:59 # but this is locaized in english
    timefmt2 = '%d/%m/%y, %H:%M' # 26/10/16, 19:17
    fmts = [timefmt1,timefmt2]
    outfmt   = '%d/%m/%y %H:%M'

    j = unidecode.unidecode(j)
    for mon_fr,mon_en in months:
        j = j.replace(mon_fr,mon_en)

    for fmt in fmts:
        try:
            dt = datetime.strptime(j, fmt)
            dt = dt.replace(year=datetime.today().year)
            break
        except ValueError:pass

    return dt.strftime(outfmt)

df['insert_time']=df['insert_time'].apply(correct_instime_format)

def safe_conv_pos_int(x):
    try:
        return int(x)
    except ValueError:
        return -1
df['Pieces']=df['Pieces'].apply(safe_conv_pos_int)
df_all=df.copy() #backup
#######################################################################
df['aux'] = pd.to_datetime(df['insert_time'])
df['weekday']=df['aux'].apply(lambda x:x.weekday())
df['ins_hour']=df['aux'].apply(lambda x:x.hour)
#######################################################################
# we care only of 2 pieces
df=df[df['Pieces']==2]
#######################################################################
# remove if cheaper than 500 (it's crap) and bigger than 70
df=df[(df.LoyerMensuel>500) & (df.Surface<70)]


# ## work out some new columns
# - **Binning price by 250€**
# - **Binnig surface by 5 m<sup>2</sup>**

# In[15]:

# i = [10,15,20,25,30,35,40]
# o = np.digitize(i,bins=np.arange(0,130,5))
# print 'Surface binning legend'
# for p,q in zip(i,o):
#     print p,'sqm -> #',q


# In[16]:

#######################################################################
df['price_bin']=np.digitize(df.LoyerMensuel,bins=np.arange(0,21*250,250))
df['sqm_bin'] = np.digitize(df.Surface,bins=np.arange(0,130,5))
df['price_sqm'] = df.LoyerMensuel/df.Surface
df = df[(df['price_sqm'] < 200)]
#######################################################################
mapges2int={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'N':10,'V':11,'X':12}
def safe_ges(x):
    try:
        return x.strip()[0]
    except AttributeError:
        return 'X'

df['Ges_lit']=df['Ges'].apply(safe_ges)
df['Ges_int']=df['Ges_lit'].apply(lambda x:mapges2int[x])
########################################################################
df['ClasseEnergie_lit']=df['ClasseEnergie'].apply(safe_ges)
df['ClasseEnergie_int']=df['ClasseEnergie_lit'].apply(lambda x:mapges2int[x])
########################################################################
dfCC=df[df['ChargesComprises']==1]
dfNC=df[df['ChargesComprises']==0]
df=dfCC
########################################################################
def sistema_arrondissement(x):
    if x>100:
        return int(x-100)
    else:
        return int(x)
df['Arrondissement']=df['Arrondissement'].apply(sistema_arrondissement)
#######################################################################
df['Meuble_int']=df['Meuble'].apply(safe_conv_pos_int)
#######################################################################


# In[17]:

print "*"*100
print "{0:d} flats recorded with 2 pieces, of size < 70sqm, and price >500eu".format(df.shape[0])
print "*"*100


# ## Save the data for later

# In[18]:

print 'Saving'
df.to_pickle("data/lbc_pandas.pkl")
print 'bye'
