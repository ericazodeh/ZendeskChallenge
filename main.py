import requests

'''
Class: TicketViewer
Use: Heavy-duty class that runs entire project
'''

class TicketViewer():
    def __init__(self, email, authToken):
        #store authentication credentials within variables
        self.email = email
        self.authToken = authToken

        self.pages = {} # dictionary that stores up to 25 tickets in each entry
        self.numOfPages = 0

    def connectToZenDeskAPI(self):
        #connect to the Zendesk API
        self.response = requests.get('https://zccstudents8735.zendesk.com/api/v2/tickets.json?page[size]=25', auth=(self.email + '/token', self.authToken))


    def getAllPages(self):
        #check if there are any tickets to show at all
        if self.response.json():
            #add first page of tickets to dictionary
            self.numOfPages += 1
            self.pages[1] = self.response.json()

        currentPage = self.response.json()
        #begin adding the rest of the tickets (if any) to the dictionary
        while currentPage['links']['next']:
            self.numOfPages += 1
            nextPageResponse = requests.get(currentPage['links']['next'],
                                    auth=('eazodeh@tamu.edu/token', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER'))
            currentPage = nextPageResponse.json()
            self.pages[self.numOfPages] = currentPage

    def queryPages(self):
        while True:
            num = int(input("Ask for a page number - "))
            self.listTickets(num)

    def listTickets(self, pageNum):
        print("Tickets By Subject")
        print("-----------------------")
        for idx, x in enumerate(self.pages[pageNum]['tickets']):
            print(str(idx+1) + '. ' + x['subject'])





#get credentials
ticket = TicketViewer('eazodeh@tamu.edu','5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
#connect to API
ticket.connectToZenDeskAPI()
#load pages
ticket.getAllPages()
#choose a page by user choice
ticket.queryPages()





