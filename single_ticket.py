class salesforce_ticket(): # Define Salesforce ticket class with the attributes we want to get

    def __init__(self,ticket_number: int = None, acv_created_date: str = None, ticket_created_date: str = None
                 , duplicate_count: int = None, acv: bool = False, ticket_status: str = None) -> None:
        
        self._ticket_number = ticket_number
        self._acv_created_date = acv_created_date
        self._ticket_created_date = ticket_created_date
        self._duplicate_count = duplicate_count
        self._acv = acv
        self._ticket_status = ticket_status

    def get_owner_id(self, owner_full_name: str) -> str: # SQL query to get the owner_id
        get_owner_id = f"SELECT Id FROM User WHERE Name = '{owner_full_name}'"
        owner_id = demisto.executeCommand("salesforce-query", {"query": get_owner_id, "using": "SalesforcePy_XSOAR"})

        if isinstance(owner_id, list) and owner_id:
            if owner_id and owner_id[0]['Type'] != entryTypes['error']:
                contents: list = owner_id[0].get('Contents', [])
                owner_id = contents[0]["Id"]
                return(owner_id)
            else:
                return_error("No 'Id' found in the query results")

    def get_owner_ticket_list(self, owner_id: str):
        ticket_list_query = f"SELECT CaseNumber, Status, CreatedDate FROM Case WHERE Status != 'Closed' AND OwnerId = '{owner_id}'"
        ticket_list_response = demisto.executeCommand("salesforce-query", {"query": ticket_list_query, "using": "SalesforcePy_XSOAR"})

        if isinstance(ticket_list_response, list) and ticket_list_response:
            if ticket_list_response and ticket_list_response[0]['Type'] != entryTypes['error']:
                contents: list = ticket_list_response[0].get('Contents', [])
                
                return_results(contents)
            else:
                return_error("No ticket list has been returned")


def main():
    # Step 1: Get the full name from the arguments
    full_name = demisto.args().get('full_name')

    # Get the get_owner_id method in salesforce Class to get the ownerId
    salesforce_ticket_instance = salesforce_ticket() # Define class instance

    owner_id = salesforce_ticket_instance.get_owner_id(full_name)

    # Get the ticket list by OwnerId
    salesforce_ticket_instance.get_owner_ticket_list(owner_id)


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()

