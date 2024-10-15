class salesforce_ticket(): # Define Salesforce ticket class with the attributes we want to get

    def __init__(self,ticket_number: int, acv_created_date: str, ticket_created_date: str
                 , duplicate_count: int, acv: bool, ticket_status: str) -> None:
        
        self._ticket_number = ticket_number
        self._acv_created_date = acv_created_date
        self._ticket_created_date = ticket_created_date
        self._duplicate_count = duplicate_count
        self._ = acv
        self._ticket_status = ticket_status

    def sql_query(self, owner_full_name: str) -> str: # SQL query to get the owner_id
        get_owner_id = f"SELECT Id FROM User WHERE Name = '{owner_full_name}'"
        if get_owner_id:
            demisto.executeCommand("salesforce-query", {"query": user_query})