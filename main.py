import requests
import time
from columnar import columnar
from tabulate import tabulate
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
        print(self.response.json()['tickets'])
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

    def listTickets(self, pageNum):
        #Show user current page + other available pages
        print("Tickets (Page " + str(pageNum) + " of " + str(self.numOfPages-1) + ')')

        #set up display header and output box
        header = ["Ticket Number", "Subject","ID","Type", "Status"]
        ticketList = []
        for idx, x in enumerate(self.pages[pageNum]['tickets']):
            ticket = []
            ticket.extend((str(idx+1) + ".", x['subject'],x['id'] ,x['type'], x['status']))
            ticketList.append(ticket)

        table = columnar(ticketList, header, no_borders=False, max_column_width=None, justify='l')
        print(table)
        print("(Page " + str(pageNum) + " of " + str(self.numOfPages-1) + ')')

        #give user options to select
        keys = "N. View next page\nP. View previous page\nJ. Jump to a specific page\nR. Return to the main menu\nQ. Quit\n"
        #display in an output box
        table = [[keys]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        keyPressed = str(input("Type a character to select an option: ")).upper()

        #based on user input, perform an action
        if keyPressed == 'N':
            if pageNum + 1 < self.numOfPages:
                self.listTickets(pageNum + 1)
            else:
                print("Error: There are no more pages next. Please type a valid letter and try again")
                time.sleep(3)
                self.listTickets(pageNum)
        elif keyPressed == 'P':
            if pageNum - 1 > 0:
                self.listTickets(pageNum - 1)
            else:
                print("Error: This is the first page. Please try again")
                time.sleep(3)
                self.listTickets(pageNum)

        elif keyPressed == 'J':
            try:
                num = int(input("Which page would you like to jump to (1-" + str(self.numOfPages-1) + "): "))
            except:
                print("Error, please try again with a valid integer")
                time.sleep(3)
                self.listTickets(pageNum)

            if num > 0 and num < self.numOfPages: #validation
                self.listTickets(num)
            else:
                print("Error, cannot jump to page " + str(num) + ", either the input is invalid,"
                                                            " or the page does not exist")
                time.sleep(3)
                self.listTickets(pageNum)
        elif keyPressed == 'R':
            self.menu()
        elif keyPressed == 'Q':
            print("Goodbye!")
        else:
            print("Error: Unknown command. Please type a valid letter and try again")
            time.sleep(3)
            self.listTickets(pageNum)


    '''
    Helper Function to validate that there are any tickets to show 
    '''
    def viewTickets(self):
        #If there are tickets to display, display the first page
        if len(self.pages) < 1:
            print("Sorry, there are no tickets to view")
            return
        #start off on page 1
        self.listTickets(1)
    '''
        1. Access pages of dictionary
        2. Loop through each page, searching for the ticket ID
        3. Notify user if ID can't be found
    '''
    def viewSingleTicket(self,id):
       for index in self.pages:
           for ticket in self.pages[index]['tickets']:
               if ticket['id'] == id:
                   self.displaySingleTicket(ticket)
       print("Error: Could not find the given ID. Please try something else.")
       time.sleep(3)
       self.menu()

    '''Loads details of ticket into a table
       formats with Tabulate and columnar 
    '''
    def displaySingleTicket(self,ticket):
        headers = ["ID","Subject","Creation Date","Type", "Status"]
        ticketList = []
        ticketList.extend((ticket['id'],ticket['subject'],ticket['created_at'],ticket['type'],ticket['status']))
        ticketWrapper = [ticketList] #columnar only accepts lists of lists
        table = columnar(ticketWrapper, headers, no_borders=False, max_column_width=None, justify='l')
        desc = [[ticket['description']]]
        output = tabulate(desc, tablefmt='grid')

        #output single ticket
        print("*****TICKET HEADER***")
        print(table)
        print("*****DESCRIPTION*****")

        print(output)
        print("********END**********")

        #create option box for user
        keys = "A. View another single ticket\nR. Return to the main menu\nQ. Quit"
        table = [[keys]]
        output = tabulate(table, tablefmt='grid')
        print(output)

        keyPressed = str(input("Choose what to do next: ")).upper()

        if keyPressed == 'A':
            try:
                id = int(input("Type the Ticket ID of the ticket you'd like to view: "))
            except:
                print("Error, please try again with a valid integer")
                time.sleep(3)
                self.displaySingleTicket(ticket)

            self.viewSingleTicket(id)
        elif keyPressed == 'R':
            self.menu()
        elif keyPressed == 'Q':
            print("Goodbye!")
        else:
            print("Error: Unknown command. Please type a valid letter and try again")
            time.sleep(3)
            self.displaySingleTicket(ticket)
    '''
    Main menu - holds two main ticket functions, allows the user to also quit program
    '''
    def menu(self):

        # create options for users to choose from
        keys = "A. View all tickets \nB. View a single ticket \nQ. Quit"

        table = [[keys]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        keyPressed = str(input("Type a given letter above to select an option -  ")).upper()
        if keyPressed == 'A':
            self.viewTickets()
        elif keyPressed == 'B':
            try:
                id = int(input("Type the Ticket ID of the ticket you'd like to view: "))
            except:
                print("Error: Invalid command. Please type a valid integer and try again")
                time.sleep(3)
                self.menu()


            self.viewSingleTicket(id)
        elif keyPressed == 'Q':
            print("Goodbye!")
            return
        else:
            print("Error: Unknown command. Please type a valid letter and try again")
            time.sleep(1.5)
            self.menu()



#get credentials
ticket = TicketViewer('eazodeh@tamu.edu','5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
#connect to API
ticket.connectToZenDeskAPI()
#load pages
ticket.getAllPages()
#open main menu
ticket.menu()





