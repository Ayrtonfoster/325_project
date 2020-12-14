# Results and Question Responses for XSS Testing

## XSS Results
### Logged out
|          | Route/URL                      | Parameter | XSS Succ |
|----------|--------------------------------|-----------|----------|
| Register | http://127.0.0.1:8081/register | password  | No       |
| Login    | http://127.0.0.1:8081/login    | password  | No       |
| Register | http://127.0.0.1:8081/register | password2 | No       |

XSS Test could not find the following fields: 
- /login error finding email field
- /register error finding fields email, name
### Logged in
|                          | Route/URL                    | Parameter                                                   | XSS Succ |
|--------------------------|------------------------------|-------------------------------------------------------------|----------|
| Sell - 5000/200          | http://127.0.0.1:8081/sell   | sell_num_ticket, sell_ticket_price, sell_ticket_date        | Yes      |
| Update - 5000/200        | http://127.0.0.1:8081/update | update_num_tickets, update_ticket_price, update_ticket_date | Yes      |
| Sell - document.cookie   | http://127.0.0.1:8081/sell   | sell_num_ticket, sell_ticket_price, sell_ticket_date        | Yes      |
| Update - document.cookie | http://127.0.0.1:8081/update | update_num_tickets, update_ticket_price, update_ticket_date | Yes      |
| Sell - document.cookie   | http://127.0.0.1:8081/sell   | sell_num_ticket, sell_ticket_price, sell_ticket_date        | Yes      |
| Update - document.cookie | http://127.0.0.1:8081/update | update_num_tickets, update_ticket_price, update_ticket_date | Yes      |

## Question Responses for XSS

1.We did two rounds of scanning. Why the results are different? What is the purpose of adding in the session id?

The results are different because in the second run we give PwnXSS the session_id of a logged in user. The session
 id allows the xss script to be verified as the logged in user, hence the script is capable of accessing pages that
 are off limit to the script without the session id.

2.Are all the possible XSS (script injection) links/routes covered in the table above? (think about any links that
 will render user inputs, such as URL paramer, cookies, flask flash calls). If not, are those link/pages vulnerable to XSS?

Technically no. We can see from the output of PwnXSS that it is failing to execute some of the inputs that should be 
usable for XSS. For example the email input field returned a type error from PwnXSS on /login. The table won't cover all possibilities. This  script appears to be searching only for POST forms and finding their input keys to test. So the other links that will render user inputs, such as URL parameters, cookies, flask flash calls should still be susceptible to XSS.