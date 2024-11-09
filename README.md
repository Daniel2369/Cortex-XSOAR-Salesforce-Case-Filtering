# Cortex-XSOAR-Salesforce-Case-Filtering
## Description

This project integrates Salesforce with Cortex XSOAR using Demisto SDK to streamline case management. It extracts and processes open cases from Salesforce, identifies important case statuses, and displays the relevant data in a formatted table within the Cortex XSOAR environment. Additionally, it includes a Slack alerting feature to notify users of important case status updates.

## Motivation

This project was born from my experience as a Senior Technical Support Engineer within the Cortex XSOAR team. Each day, I faced the time-consuming task of manually reviewing all of my Salesforce cases to understand the CaseHistory statuses, which could take anywhere from 15 to 30 minutes daily. This manual effort was inefficient and repetitive, so I set out to automate the process.

Leveraging my knowledge of Python and the DemistoSDK, I built this tool to automate the extraction and parsing of Salesforce cases, streamlining my workflow. By integrating Palo Alto Networks' Cortex XSOAR as the automation platform, I was able to significantly reduce the time spent on these tasks, while also demonstrating my technical expertise.

In addition, I added Slack alerting to ensure that critical case events are communicated to the team immediately. This solution not only saves me time, but it also benefits my team by providing better visibility into case status changes and improving our collective response times. Ultimately, this project has helped us deliver more efficient and responsive support to our customers, while also improving internal workflows and statistics for the entire team.

Feel free to explore my [LinkedIn profile](https://www.linkedin.com/in/daniel-berliant-6725241a9/) to learn more about my professional background and experience.

## Features

1. Integration with **Demisto SDK**: The project works with Demisto SDK to interact with the **Cortex XSOAR platform**, allowing seamless automation of tasks.
2. **Salesforce Beyond Integration**: It integrates with Salesforce Beyond to pull relevant case data.
      * Uses **SQL** queries to retrieve data directly from Salesforce.
3. Open Cases Extraction: Extracts the list of open cases assigned to the user (owner) from Salesforce.
4. **Data Parsing**:
    * "Awaiting Customer Verification" Status: Identifies when a solution has been provided and extracts the date for follow-up.
    * Duplicate Detection: Looks for duplicate cases and extracts their dates if any duplicates are found.
    * Case Creation Date: If no cases are marked as "Awaiting Customer Verification", the case creation date is displayed.
5. Formatted Table Display: All data is displayed in the Cortex XSOAR Playground or War Room in a user-friendly, formatted table, depending 
   on where the script is executed.
6. Slack Alerting: Sends real-time alerts to a specified Slack channel for important case updates, such as new cases, status changes, or 
   duplicate detection. This ensures that the team stays informed on critical case events without having to manually check the platform.
---------------------------
## Prerequisites

Before you begin, ensure that you have the following:
1. Basic knowledge of Cortex XSOAR:
   * Familiarity with how to install content packs.
   * Understanding of how to configure new integrations within Cortex XSOAR.
2. Configure the following integrations:
   * Salesforce Integration: Set up and configure the Salesforce Beyond integration to extract data using SQL queries.
   * Slack Integration: Set up a Slack app and configure the necessary permissions to send messages to your Slack workspace. You'll need to 
     obtain your Slack webhook URL for real-time alerts.
---------------------------
## How to use

1. Create a New Automation in XSOAR’s UI
   * Make sure you are running with Admin role.
   * For quick navigation, use CTL+K (Windows/Linux) or CMD+K (Mac).
2. Set Up the Automation
   * Delete any existing content inside the automation and paste the new automation script.
3. Add Arguments in the Settings
   * `email`:
     * Type: String
     * Description: Pass this argument if you want to receive Slack notifications.
4. Add Output
   * `Email`:
     * Type: String
5. Upload getSFOwnerTicketsStatus.yml into the Playbooks tab in Cortex XSOAR.
   * Edit playbooks first task insert your email.
6. Create an Incident Type
   * Select the playbook you just created.
   * Check the box to enable Run Automatically.
7. Create a Job to Run Daily
   * Set up a job that will run the incident type daily.
