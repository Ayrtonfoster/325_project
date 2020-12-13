# A5 Failure Report
## Contributors
- Matthew Kruzich

## Integration-Posting | Failure Report
No problems were discovered during posting integration testing

## Integration-Purchase | Failure Report

| Test Name | Test Function | Error in Output | Cause of Error | Solution |
|---|---|---|---|---|
| test_purchase | Test that one user can post a ticket for sale, then another user can purchase that ticket, using full system from login through logout | Tickets with identical names from other tests were purchased | Ticket name is not unique | Added check in backend to prevent listing tickets with duplicate ticket_name |
