import bs4 as bs
import urllib.request
from urllib.error import HTTPError
import os
import sys
import ssl

baseURL = 'https://en.wikipedia.org/wiki/'
context = ssl._create_unverified_context()

#recursive call to print parent's title
def printPath(obj):
    if obj['parent']:
        printPath(obj['parent'])
        print(' -> ', end='')
    print(obj['title'], end='')

#play game
def playGame(Q, history, targetPageTitle):
    targetAcquired = False
    while targetAcquired == False:

        #if Q is empty print "pages unlinkable"
        if not Q[0]:
            print('unable to link the pages')
            targetAcquired = True
            break

        current = Q[0]
        Q = Q[1:]
        #print("\t" + current['title'])

        #try to follow link path
        try: 
            source = urllib.request.urlopen(baseURL + current['title'], context=context)
            soup = bs.BeautifulSoup(source, 'lxml')

            #Breadth First search of links starting with root page's links
            for url in soup.find_all('a'):
                #create object and add to history/Q
                link = url.get('href')

                if link is not None: 
                    if(link.startswith('/wiki/')):
                        title = link.strip('/wiki/').split(':')[0]                  #remove sections in title
                        if(title not in history):
                            history[title] = {
                                'title': title,
                                'parent': current,
                            }

                            #check targetAcquired
                            if(title.lower() == targetPageTitle.lower()):
                                targetAcquired = True
                                print('Path Found!')
                                printPath(history[title])
                                print()
                            Q.append(history[title])
        #exit on ctrl+c
        except KeyboardInterrupt:
            print('Exiting')
            sys.exit()
        
        #continue on if 404 error occurs
        except urllib.error.HTTPError as error:
            if(error.code == 404):
                print('could not get page: ' + current['title'])
                pass
            else:
                raise


#init variables and game
def initGame():
    print('Root: ' + sys.argv[1] + ' => Target: ' + sys.argv[2])
    rootPageTitle = sys.argv[1].replace(" ", "_")
    targetPageTitle = sys.argv[2].replace(" ", "_")

    #Track history to disregard duplicates and so the program can end eventually
    history = {}
    history[rootPageTitle] = {
        'title': rootPageTitle,
        'parent': None
    }

    #add rootPage to Q
    Q = [history[rootPageTitle]]

    playGame(Q, history, targetPageTitle)

initGame()