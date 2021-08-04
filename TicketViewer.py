import sys
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
        self.invalidCommandFlag = False #used for testing purposes when unknown user commands are found (i.e. true == invalid command)
        self.lastErrorMessage = "" #used during testing to make sure the correct error was output

    def connectToZenDeskAPI(self):
        #connect to the Zendesk API
        print("Loading tickets... this may take a while...")
        try:
            self.response = requests.get('https://zccstudents8735.zendesk.com/api/v2/tickets.json?page[size]=25', auth=(self.email + '/token', self.authToken))

        except Exception as e:
            print("Error(" + e + "): it seems like there was an issue connecting to the Zendesk API. Please try again later.")
            sys.exit()




    '''
    This function loads all tickets into it's pages first to avoid any further API calls 
    User can now run program offline
    '''
    def getAllPages(self):
        '''If connection was not successful to the API previously,
         then end the program to avoid any other logic'''
        if self.response.status_code != 200:
            print("Error: it seems like there was an issue connecting to the Zendesk API. Please try again later.")
            sys.exit()

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
        self.outputTable(keys)
        try:
            keyPressed = str(input("Type a character to select an option: ")).upper()
        except:
            self.invalidCommandFlag = True
            self.lastErrorMessage = "Error: input must be a single character"
            print(self.lastErrorMessage)
            self.menu()


        #based on user input, perform an action
        listTicketsResult = self.actionListTickets(keyPressed,pageNum)
        if not listTicketsResult and self.invalidCommandFlag:
            print(self.lastErrorMessage)
            time.sleep(1.5)
            self.invalidCommandFlag = False
            self.listTickets(pageNum)



    def actionListTickets(self,keyPressed,pageNum):
        if keyPressed == 'N':
            if pageNum + 1 < self.numOfPages:
                self.invalidCommandFlag = False
                self.listTickets(pageNum + 1)

            else:
                self.invalidCommandFlag = True
                self.lastErrorMessage = "Error: There are no more pages next. Please type a valid letter and try again"
                return False

        elif keyPressed == 'P':
            if pageNum - 1 > 0:
                self.invalidCommandFlag = False
                self.listTickets(pageNum - 1)
            else:
                self.invalidCommandFlag = True
                self.lastErrorMessage = "Error: This is the first page. There is no previous page"
                return False

        elif keyPressed == 'J':
            try:
                num = int(input("Which page would you like to jump to (1-" + str(self.numOfPages-1) + "): "))
                self.invalidCommandFlag = False
            except:
                self.invalidCommandFlag = True
                self.lastErrorMessage = "Error, please try again with a valid integer"
                return False

            if self.canJumptoPage(num): #validation
                self.invalidCommandFlag = False
                self.listTickets(num)
            else:
                self.invalidCommandFlag = True
                self.lastErrorMessage = "Error, cannot jump to page " + str(num) + ", either the input is invalid, or the page does not exist"
                return False
        elif keyPressed == 'R':
            self.invalidCommandFlag = False
            self.menu()
        elif keyPressed == 'Q':
            print("Goodbye!")
            sys.exit()
        else:
            self.invalidCommandFlag = True
            self.lastErrorMessage = "Error: Unknown command. Please type a valid letter and try again"
            return False

        return True

    def canJumptoPage(self,num):
        if num > 0 and num < self.numOfPages:
            return True
        else:
            return False



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
                   return True
       self.invalidCommandFlag = True
       self.lastErrorMessage = "Error: Could not find the given ID. Please try something else."

       return False

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
        self.outputTable(keys)

        keyPressed = str(input("Choose what to do next: ")).upper()

        #choose option based on user input
        displaySingleTicketResult = self.actionDisplaySingleTicket(ticket,keyPressed)
        if not displaySingleTicketResult:
            print(self.lastErrorMessage)
            time.sleep(1.5)
            self.displaySingleTicket(ticket)




    def actionDisplaySingleTicket(self,keyPressed):
        if keyPressed == 'A':
            try:
                id = int(input("Type the Ticket ID of the ticket you'd like to view: "))
                self.invalidCommandFlag = False
            except:
                self.invalidCommandFlag = True
                self.lastErrorMessage = "Error, please try again with a valid integer"
                return False


            displayResult = self.viewSingleTicket(id)
            if not displayResult:
                print(self.lastErrorMessage)
                time.sleep(1.5)
                self.menu()

        elif keyPressed == 'R':
            self.menu()
        elif keyPressed == 'Q':
            print("Goodbye!")
            sys.exit()
        else:
            self.invalidCommandFlag = True
            self.lastErrorMessage = "Error: Unknown command. Please type a valid letter and try again"
            return False

        return True


    #displays and formats strings into a border padded text box
    def outputTable(self,text):
        table = [[text]]
        output = tabulate(table, tablefmt='grid')
        print(output)

    '''
    Main menu - holds two main ticket functions, allows the user to also quit program
    '''
    def menu(self):

        # create options for users to choose from
        keys = "A. View all tickets \nB. View a single ticket \nQ. Quit"

        self.outputTable(keys)
        keyPressed = str(input("Type a given letter above to select an option -  ")).upper()
        resultActionMenu = self.actionMenu(keyPressed)
        if not resultActionMenu:
            print(self.lastErrorMessage)
            time.sleep(1.5)
            self.menu()


    def actionMenu(self,keyPressed):
        if keyPressed == 'A':
            self.invalidCommandFlag = False
            self.viewTickets()
        elif keyPressed == 'B':
            try:
                id = int(input("Type the Ticket ID of the ticket you'd like to view: "))
                self.invalidCommandFlag = False
            except:
                self.invalidCommandFlag = True
                self.lastErrorMessage = "Error: Invalid command. Please type a valid integer and try again"
                return False

            self.viewSingleTicket(id)
        elif keyPressed == 'Q':
            print("Goodbye!")
            sys.exit()
        else:
            self.invalidCommandFlag = True
            self.lastErrorMessage = "Error: Unknown command. Please type a valid letter and try again"
            return False

    # used for Unit Testing where user input is necessary
    def get_input(text):
        return input(text)

