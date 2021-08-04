import unittest
from TicketViewer import TicketViewer
from unittest.mock import patch



class TestTicketViewer(unittest.TestCase):

    def test_rejection_if_credentials_are_invalid(self):
        #Assume
        badEmail = "invalidEmail@invalidEmail.com"
        badToken = "badToken"

        #Action
        ticket = TicketViewer(badEmail,badToken)
        ticket.connectToZenDeskAPI()

        #Assert
        self.assertFalse(ticket.response.status_code == 200)

    def test_error_id_not_found(self):


        #Assume
        user_input = 88888888888 #assuming no such id is ever given

        #Action

        # get credentials
        ticket = TicketViewer('eazodeh@tamu.edu', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
        # connect to API
        ticket.connectToZenDeskAPI()

        # load pages
        ticket.getAllPages()
        #request a bad ticket id based off user input
        ticket.viewSingleTicket(user_input)

        #Assert
        self.assertTrue(ticket.invalidCommandFlag == True and ticket.lastErrorMessage == "Error: Could not find the given ID. Please try something else.")

    def test_previous_page_when_on_first_page(self):
        #Assume
        action = 'P' #would tell program to go to previous page
        currentPage = 1

        #Action
        ticket = TicketViewer('eazodeh@tamu.edu', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
        # connect to API
        ticket.connectToZenDeskAPI()

        # load pages
        ticket.getAllPages()
        ticket.actionListTickets('P',currentPage)

        #Assert
        self.assertTrue(ticket.invalidCommandFlag == True and ticket.lastErrorMessage == "Error: This is the first page. There is no previous page")


    def test_next_when_on_final_page(self):


        #Action
        ticket = TicketViewer('eazodeh@tamu.edu', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
        ticket.connectToZenDeskAPI()
        ticket.getAllPages()

        # Assume
        action = 'N'  # would tell program to go to next page
        currentPage = ticket.numOfPages-1 #last page

        #Action
        ticket.actionListTickets(action, currentPage)

        #Assert
        self.assertTrue(ticket.invalidCommandFlag == True and ticket.lastErrorMessage == "Error: There are no more pages next. Please type a valid letter and try again")

    def test_listTickets_with_unknown_command(self):

        #Assume
        badCommand = "B"
        firstPage = 1

        # Action
        ticket = TicketViewer('eazodeh@tamu.edu', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
        ticket.connectToZenDeskAPI()
        ticket.getAllPages()
        ticket.actionListTickets(badCommand, firstPage)

        # Assert
        self.assertTrue(ticket.invalidCommandFlag == True and ticket.lastErrorMessage == "Error: Unknown command. Please type a valid letter and try again")


    def test_displaySingleTicket_unknown_command(self):
        # Assume
        badCommand = "fgrefgr3543"

        # Action
        ticket = TicketViewer('eazodeh@tamu.edu', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
        ticket.connectToZenDeskAPI()
        ticket.getAllPages()
        ticket.actionDisplaySingleTicket(badCommand)

        # Assert
        self.assertTrue(ticket.invalidCommandFlag == True and ticket.lastErrorMessage == "Error: Unknown command. Please type a valid letter and try again")


    def test_menu_unkown_command(self):
        # Assume
        badCommand = ""

        # Action
        ticket = TicketViewer('eazodeh@tamu.edu', '5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
        ticket.connectToZenDeskAPI()
        ticket.getAllPages()
        ticket.actionMenu(badCommand)

        # Assert
        self.assertTrue(ticket.invalidCommandFlag == True and ticket.lastErrorMessage == "Error: Unknown command. Please type a valid letter and try again")



