## 2025-02-17
## changed
- Remove application form manifest file.
- Add status field into the above xpath header.
- Remove barcode field from product_template.py file.
- Remove one product_template_barcode_view.xml file and
  add one xpath field to change label name for barcode and 
  add another xpath to move barcode field.

## 2025-03-06
## Constraints and Mail activity & Notification
## changed
- Remove comment from product_template from this function action_mark_borrowed
- Add docstring in product_template -> mark_as_returned.

## 2025-03-06
## mail template, mail compose wizard, attach report in mail template
- Add new function (models -> borrow_transaction_history -> send_overdue_book_reminder) 
- Add new schedule action (data -> ir_cron -> ir_cron_send_overdue_reminders)
- Add new function for renewal membership (models -> library_member -> action_send_renewal_email)
- Add new mail template (mail_template_data -> library_membership_renewal_reminder_email_template)

## 2025-03-17
## Schedule Actions, Automated Actions and Server Actions
## changed
- Optimise send book return reminders function from borrow transaction history python file which is schedule action.
- Optimise mark books as returned function from borrow transaction history python file which is server action.
- Optimise check overdue books action function from borrow transaction history python file which is automated action.

## 2025-03-18
## Borrow Books Requirement
## changed
- Add new function process borrow transaction.
- Optimise action confirm method from borrow transaction history to display Display warnings sequentially.
- Optimise action continue method from borrow books warning wizard to save transaction.

## [18.0.1.1.0] - 2025-03-20 | Schedule Actions, Automated Actions and Server Actions
## changed
- Optimise server action of automated action.
- Optimise send book return reminder function.
- Optimise check overdue books action function.

##  [18.0.1.2.0] - 2025-03-21 | Layout Design & custom report
## changed
- Optimise library location document from library location report file.