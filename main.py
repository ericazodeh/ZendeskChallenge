from TicketViewer import TicketViewer

#get credentials
ticket = TicketViewer('eazodeh@tamu.edu','5qPXeeoJreTMN7SlBP2ap4svKkwPtEI6QAiMmcER')
#connect to API
ticket.connectToZenDeskAPI()
#load pages
ticket.getAllPages()
#open main menu
ticket.menu()





