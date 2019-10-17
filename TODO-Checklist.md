# Progress Tracking

### Functionality so far
- [x] User registration
- [x] User login
- [x] admin login
- [x] form fields
- [x] model forms saved to db
- [x] admin filtering users by staff or student
- [x] admin's ability to modify forms and delete users
- [x] admin can search users by any field {name, last name, username} 
- [x] sidebar and navbar {`all links are working, some just need styling`} 
- [x] page for terms
- [ ] submit page
- [ ] current degree applied page
- [ ] previous degree page
- [x] Welcome Page
- [x] Super Admin Reset Password
- [x] auto fill in form values from other models  
---
### Minimum requirements
- [x] creating and associating an application with a user
- [x] account management (password reset, email change)
- [x] user document upload (.pdf)
- [x] {assume user already has username generated from the central system, therefore they can login with that username}
- [x] generate & export csv(filtered) and download pdf files
- [x] admin view and download uploaded documents 
- [ ] pagination `next button at every page`
- [ ] cancel application, review(overview tab) application
- [ ] add and modify records as user pleases
- [X] mark application status
- [x] add a reason for applicant.
- [x] list applicants per degree {fields to be shown: `Surname`,`Name`,`Title`,`Student Number`,`Email`,`Status`} [filter by and order degree]
---
### Minimum requirements with Dependencies
- [x] `citizenship` { if SA=>Choose Race, if INT=> Choose country }
- [x] `degree applied` { if MIT... }
- [x] `Previous degree` { did it have a project? }
---
### Possibly Automated Tasks
- [x] send notification emails
- [x] application reason sent via email {reason: `denied`, `accepted`, `withdrawn`} with explanation
- [ ] qualification check `IMPORTANT TO CLIENT` It would be nice to add a field indicating the South African equivalent of the degree. `<<will definitely get us more marks>>`
- [ ] application status {`new`,`active`, `withdrawn`, `complete`, `incomplete`}
---
### strict fixes that need to be added
- [x] button to redirect to login after registration
- [x] make login form using crispy forms
- [x] link user to their application form
- [ ] address form should have current address, and permanent postal address formsets
---
### extended functionality and additionals we'd love to have
- [ ] send notifications : https://github.com/pinax/pinax-notifications
- [ ] reduce size of banner on homepage
- [ ] countdown timer using django fluent content
