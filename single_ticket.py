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
            if owner_id[0]['Type'] != entryTypes['error']:
                contents: list = owner_id[0].get('Contents', [])
                owner_id = contents[0]["Id"]
                return(owner_id)
            else:
                return_error("No 'Id' found in the query results")

    def get_owner_ticket_list(self, owner_id: str):
        ticket_list_query = f"SELECT CaseNumber, Status, CreatedDate FROM Case WHERE Status != 'Closed' AND OwnerId = '{owner_id}'"
        ticket_list_response = demisto.executeCommand("salesforce-query", {"query": ticket_list_query, "using": "SalesforcePy_XSOAR"})

        if isinstance(ticket_list_response, list) and ticket_list_response:
            if ticket_list_response[0]['Type'] != entryTypes['error']:
                contents: list = ticket_list_response[0].get('Contents', [])
                return_results(contents)
            else:
                return_error("No ticket list has been returned")

    def set_ticket_number(self, ticket_number: int):
        return self._ticket_number == ticket_number

    def set_ticket_status(self, ticket_status: int):
        return self._ticket_status == ticket_status

    def get_ticket_acv(self,ticket_creation_date,ticket_status):
        acv_query = f"SELECT Case.CaseNumber, NewValue, CreatedDate FROM CaseHistory WHERE Case.CaseNumber = '{self._ticket_number}'"
        acv_query_response = demisto.executeCommand("salesforce-query", {"query": acv_query, "using": "SalesforcePy_XSOAR"})

        if isinstance(acv_query_response, list) and acv_query_response:
            if acv_query_response[0]['Type'] != entryTypes['error']:
                contents: list = acv_query_response[0].get('Contents', [])

                awaiting_customer_verification_count = 0
                created_dates = []

                if isinstance(contents, list):
                     table_data: list = []
                     for record in contents:
                          self._acv = record.get('NewValue')
                          self._acv_created_date = record.get('CreatedDate')

                          if self._acv == 'Awaiting Customer Verification':
                               awaiting_customer_verification_count += 1
                               created_dates.append(self._acv_created_date)
                
                self._acv = 'True' if awaiting_customer_verification_count > 0 else 'False'
                self._acv_created_date = ', '.join(created_dates) if created_dates else 'None'
                self._duplicate_count = awaiting_customer_verification_count if awaiting_customer_verification_count > 1 else 'None'
                self._ticket_created_date = ticket_creation_date if self._acv == 'False' else 'None'

                table_data.append({
                    'Case Number': self._ticket_number,
                    'ACV': self._acv,
                    'ACV Created Date/s': self._acv_created_date,
                    'Duplicate Count': self._duplicate_count,
                    'Ticket Creation Date': self._ticket_created_date,
                    'Status': self._ticket_status
                })

                return table_data
            else:
                return_error(f"No acv status has been returned for ticket: {self._ticket_number}")
     

def main():
    # Step 1: Get the full name from the arguments
    full_name = demisto.args().get('full_name')

    # Get the get_owner_id method in salesforce Class to get the ownerId
    salesforce_ticket_instance = salesforce_ticket() # Define class instance

    owner_id = salesforce_ticket_instance.get_owner_id(full_name)

    # Get the ticket list by OwnerId
    ticket_list_content = salesforce_ticket_instance.get_owner_ticket_list(owner_id)

    # Get ACV status per ticket
    for item in ticket_list_content:
        ticket_number = item.get("CaseNumber")
        ticket_creation_date = item.get("CreatedDate")
        ticket_status = item.get("Status")
        if ticket_number:
            salesforce_ticket_instance.set_ticket_number(ticket_number) # Change self ticket_number
            salesforce_ticket_instance.set_ticket_status(ticket_status) # Change self ticket_status
            table_data = salesforce_ticket_instance.get_ticket_acv(ticket_creation_date) # get acv + duplicates and populate a a list

    # Return table_data list as a table in the XSOAR's warroom
    demisto.results({
        'Type': entryTypes['note'],
        'ContentsFormat': formats['table'],
        'Contents': table_data
    })


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()

