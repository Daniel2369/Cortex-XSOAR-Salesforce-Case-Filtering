def main():
    # Define the Salesforce query
    case_number = demisto.args().get('caseNumber')
    query = f"SELECT Case.CaseNumber, NewValue, CreatedDate FROM CaseHistory WHERE Case.CaseNumber = '{case_number}'"

    # Execute the Salesforce query
    response = demisto.executeCommand("salesforce-query", {"query": query})

    # Check if the response was successful
    if not response or response[0]['Type'] == entryTypes['error']:
        return_error(f"Error querying Salesforce: {response[0]['Contents'] if response else 'No response received'}")

    # Check if 'Contents' is a list
    records = response[0].get('Contents', [])

    # Ensure 'records' is a list
    if isinstance(records, list):
        # Prepare to store results
        awaiting_customer_verification_count = 0
        created_dates = []

    # Loop through the records to find 'Awaiting Customer Verification'
    for record in records:
		new_value = record.get('NewValue')
        created_date = record.get('CreatedDate')

        if new_value == 'Awaiting Customer Verification':
            awaiting_customer_verification_count += 1
            created_dates.append(created_date)  # Save the CreatedDate
          
    # Prepare context data
    result = {
        'caseNumber': case_number,
        'AwaitingCustomerVerification': awaiting_customer_verification_count > 0,
        'CreatedDates': created_dates,  # List of all CreatedDates
        'DuplicateCount': awaiting_customer_verification_count if awaiting_customer_verification_count > 1 else None
    }

    # Save to context
    demisto.setContext("SalesforceCaseVerification", result)

    # Return a readable output to the War Room
    readable_output = f"Case {case_number} - Awaiting Customer Verification count: {awaiting_customer_verification_count}, CreatedDates: {created_dates}"

    if result['DuplicateCount']:
        readable_output += f", Duplicate status count: {result['DuplicateCount']}"

    return_results(readable_output)

# Entry point for the automation script
if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
