from msedge.selenium_tools import Edge, EdgeOptions

#this is for data cleaning
import re

#create a login.py with your login information
from login import username, password
from time import sleep

class TwitterBot():
    def __init__(self):
        self.driver = Edge()
        self.driver.maximize_window()
        self.driver.get('https://twitter.com')
        self.driver.implicitly_wait(3)

    def goToTwitter(self):
        self.driver.get('https://twitter.com')

    def login(self):
        self.driver.find_element_by_xpath("//a[@href='/login']").click()

        #I used sleep because before this time there is another instance of an element named like below. 
        #It is crucial to get the right element in order to interact with it.
        sleep(1) 
        self.driver.find_element_by_xpath("//input[@name='session[username_or_email]']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='session[password]']").send_keys(password)
        
        self.driver.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()

    def basicSearch(self, topic):
        self.driver.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']").send_keys(topic)
        self.driver.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']").submit()
    
    def advancedSearch(self, exact, any, none, hashtags, dateFrom, dateTo):
        finalSearch = ''
        #This is to accommodate for different search types that a user might want.
        if exact != None:
            finalSearch+='"' + exact + '" '
        if any != None:
            finalSearch+='(' + any + ') '
        if none != None:
            finalSearch+= '-' + none + ' '
        if hashtags != None:
            finalSearch+= '(#' + hashtags + ') '
        if dateTo != None:
            finalSearch+= 'until:' + dateTo + ' '
        if dateFrom != None:
            finalSearch+= 'since:' + dateFrom + ' '

        self.driver.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']").send_keys(finalSearch)
        self.driver.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']").submit()

    def scrapeTweets(self, desiredNum):
        allLines = ''
        oldDataLines = []
        dataLines = ['init']
        tweetsFile = open('tweets.csv', 'w')

        #I included this array to help clean data later
        dirtyArray = ['Quote Tweet', 'Promoted', 'Show this thread', '', '\n', ' ']
        numDataLines = 0
        while numDataLines < desiredNum and oldDataLines != dataLines:

            oldDataLines = dataLines
            sleep(1)
            #all these are different types of data that I do not want to pick up.
            dirtyData = self.driver.find_elements_by_xpath("//div[@class='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2']")
            dirtyData2 = self.driver.find_elements_by_xpath("//div[@class = 'css-1dbjc4n r-18u37iz r-1wtj0ep r-156q2ks r-1mdbhws']")
            dirtyData3 = self.driver.find_elements_by_xpath("//div[contains(text(),'Replying to')]")
            dirtyData4 = self.driver.find_elements_by_xpath("//div[@role = 'blockquote']")

            #adding all the dirty data into one array
            for dirt in dirtyData2:
                dirtyData.append(dirt)

            for dirt in dirtyData3:
                dirtyData.append(dirt)

            for dirt in dirtyData4:
                dirtyData.append(dirt)

            #the data is stored with strings with many lines so I split the strings up by line and have an array where each index is one lin
            dirtyLines = []
            for dirt in dirtyData:
                dirt = dirt.text
                chunks = dirt.split('\n')
                for chunk in chunks:
                    dirtyLines.append(chunk)

            #this includes dirty data that will be weeded out later
            data = self.driver.find_elements_by_xpath("//div[@data-testid='tweet']")
            
            #same thing I did with dirtyLines
            dataLines = []
            for datapoint in data:
                datapoint = datapoint.text
                chunks = datapoint.split('\n')
                for chunk in chunks:
                    dataLines.append(chunk)

            #I check oldDataLines as well to avoid redundancy 
            for line in dataLines:
                if line not in dirtyLines and line not in oldDataLines and line not in dirtyArray:
                    if numDataLines >= desiredNum:
                        break
                    try:
                        noPunctuationLine = re.sub(r'[^\w\s]','', line)
                        tweetsFile.write(noPunctuationLine)
                        tweetsFile.write("\n")
                        allLines+=line
                        numDataLines+=1
                    except Exception:
                        print('This data point not encodable.')

            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")

        tweetsFile.close()
        return allLines