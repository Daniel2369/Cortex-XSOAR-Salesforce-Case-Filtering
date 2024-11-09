class Salesforcecase():
    def __init__(self, case_number: int = None, acv_created_date: str = None, case_created_date: str = None,
                 duplicate_count: int = None, acv: bool = False, case_status: str = None) -> None:
        self._case_number = case_number
        self._acv_created_date = acv_created_date
        self._case_created_date = case_created_date
        self._duplicate_count = duplicate_count
        self._acv = acv
        self._case_status = case_status

    def set_case_number(self, case_number: int):
        self._case_number = case_number

    def set_case_status(self, case_status: str):
        self._case_status = case_status

    def set_case_createdDate(self, case_created_date: str):
        self._case_created_date = case_created_date

    def get_owner_id(self, owner_email: str) -> str:  # SQL query to get the owner_id
        get_owner_id = f"SELECT Id FROM User WHERE Email = '{owner_email}'" 
        try:
            owner_id = demisto.executeCommand("salesforce-query", {"query": get_owner_id})
            if owner_id and isinstance(owner_id, list):
                contents: list = owner_id[0].get('Contents', [])
                return contents[0]["Id"] if contents else None
            else:
                return_error("No 'Id' found in the query results")
        except Exception as e:
            return str(e)

    def get_owner_case_list(self, owner_id: str):
        case_list_query = f"SELECT CaseNumber, Status, CreatedDate FROM Case WHERE Status != 'Closed' AND OwnerId = '{owner_id}'"
        try:
            case_list_response = demisto.executeCommand("salesforce-query", {"query": case_list_query})
            if case_list_response and isinstance(case_list_response, list):
                return case_list_response[0].get('Contents', [])
            else:
                return_error("No case list has been returned")
        except Exception as e:
            return str(e)

    def get_case_acv(self):
        acv_query = f"SELECT Case.CaseNumber, NewValue, CreatedDate FROM CaseHistory WHERE Case.CaseNumber = '{self._case_number}'"
        try:
            acv_query_response = demisto.executeCommand("salesforce-query", {"query": acv_query})

            if acv_query_response and isinstance(acv_query_response, list):
                contents: list = acv_query_response[0].get('Contents', [])

                if contents:  # Check if contents is not empty
                    table_data: list = []
                    # For duplicate check
                    awaiting_customer_verification_count = 0
                    acv_created_dates = []

                    for record in contents: # Looking for attributes key in the history to find the ACV records
                        self._acv = record.get('NewValue')
                        self._acv_created_date = record.get('CreatedDate')

                        if self._acv == 'Awaiting Customer Verification':
                            awaiting_customer_verification_count += 1 # If more then 1 record of acv it will be > 1
                            acv_created_dates.append(self._acv_created_date) # Saves the dates of the ACV record

                    self._acv = 'True' if awaiting_customer_verification_count > 0 else 'False'
                    self._acv_created_date = ', '.join(acv_created_dates) if acv_created_dates else 'None'
                    self._duplicate_count = awaiting_customer_verification_count if awaiting_customer_verification_count > 1 else 'None'
                    self._case_created_date = self._case_created_date if self._acv == 'False' else 'None'

                    # Append to table data only if _case_number is set
                    table_data.append({
                        'Case Number': self._case_number,
                        'ACV': self._acv,
                        'ACV Created Date/s': self._acv_created_date,
                        'Duplicate Count': self._duplicate_count,
                        'case Creation Date': self._case_created_date,
                        'Status': self._case_status
                    })
                return table_data
            else:
                return_error(f"No ACV status has been returned for case: {self._case_number}")
        except Exception as e:
            return str(e)

def main():
    email = demisto.args().get('email')

    # Get the get_owner_id method in salesforce Class to get the ownerId
    salesforce_case_instance = Salesforcecase()  # Define class instance

    owner_id = salesforce_case_instance.get_owner_id(email)

    # Get the case list by OwnerId
    case_list_content = salesforce_case_instance.get_owner_case_list(owner_id)

    # Get ACV status per case
    table_data = []  # Initialize table_data here
    for item in case_list_content:
        case_number = item.get("CaseNumber")
        case_creation_date = item.get("CreatedDate")
        case_status = item.get("Status")

        if case_number:
            salesforce_case_instance.set_case_number(case_number)
            salesforce_case_instance.set_case_status(case_status)
            salesforce_case_instance.set_case_createdDate(case_creation_date)
            acv_data = salesforce_case_instance.get_case_acv()  # get acv + duplicates and populate a list
            table_data.extend(acv_data)  # Append ACV data to the table_data

    # Return table_data list as a table in the XSOAR's war room
    demisto.results({
        'Type': entryTypes['note'],
        'ContentsFormat': formats['table'],
        'Contents': table_data
    })

    # Set email to Context
    demisto.setContext('Email', email)

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
