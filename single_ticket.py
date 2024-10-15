class salesforce_ticket(): # Define Salesforce ticket class with the attributes we want to get

    def __init__(self,ticket_number: int = None, acv_created_date: str = None, ticket_created_date: str = None
                 , duplicate_count: int = None, acv: bool = False, ticket_status: str = None) -> None:
        
        self._ticket_number = ticket_number
        self._acv_created_date = acv_created_date
        self._ticket_created_date = ticket_created_date
        self._duplicate_count = duplicate_count
        self._ = acv
        self._ticket_status = ticket_status

    def sql_query(self, owner_full_name: str) -> str: # SQL query to get the owner_id
        get_owner_id = f"SELECT Id FROM User WHERE Name = '{owner_full_name}'"
        owner_id = demisto.executeCommand("salesforce-query", {"query": get_owner_id, "using": "SalesforcePy_XSOAR"})

        if owner_id and owner_id[0]['Type'] != entryTypes['error']:
            contents: list = owner_id[0].get('Contents', [])
            if isinstance(contents, list) and contents:
                owner_id = contents[0]["Id"]
                return_results(owner_id)
            else:
                return_error("No 'Id' found in the query results")


def main():
    # Step 1: Get the full name from the arguments
    full_name = demisto.args().get('full_name')

    # Run the sql_query method in salesforce Class to get the ownerId
    salesforce_ticket_instance = salesforce_ticket() # Define class instance
    owner_id = salesforce_ticket_instance.sql_query(full_name)

    


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()