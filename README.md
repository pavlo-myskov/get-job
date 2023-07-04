# Get Job

[![Tests](https://img.shields.io/github/actions/workflow/status/FlashDrag/get-job/production.yml?branch=master&label=Django%20CI&logo=github)](https://github.com/FlashDrag/get-job/actions)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=flat&logo=heroku&logoColor=white&labelColor=575757&label=Live%20Demo)](https://get-job.herokuapp.com)

[![Django](https://img.shields.io/badge/v.3.2-575757?style=flat&logo=django&logoColor=white&labelColor=092E20&label=Django)](https://docs.djangoproject.com/en/3.2/)
[![Bootstrap](https://img.shields.io/badge/v.5-575757?style=flat&logo=bootstrap&logoColor=white&labelColor=7952B3&label=Bootstrap)](https://getbootstrap.com/docs/5.0)
[![jQuery](https://img.shields.io/badge/v.3.7-575757?style=flat&logo=jquery&logoColor=white&labelColor=0769AD&label=jQuery)](https://jquery.com/)
[![PostgreSQL](https://img.shields.io/badge/ElephantSQL-575757?style=flat&logo=postgresql&logoColor=white&labelColor=4169E1&label=PostgreSQL)](https://www.elephantsql.com/)


<!-- TODO Add coverage -->
<!-- [![Codecov](https://img.shields.io/codecov/c/github/FlashDrag/get-job?label=Coverage&logo=codecov)](https://codecov.io/gh/FlashDrag/get-job)

https://github.com/aiogram/aiogram/blob/dev-3.x/.github/workflows/tests.yml
https://about.codecov.io/blog/python-code-coverage-using-github-actions-and-codecov/
-->

## Overview
The relevance of job search in our time constantly increases. [Get Job](https://get-job.live) is an online Job Platform that helps Jobseekers to get desirable jobs and Employers to find the right candidates. The app includes two modes: _Jobseeker Mode_ and _Employer Mode_. _Jobseeker Mode_ allows users to search for jobs and apply for jobs as well as create their resumes and manage their applications. And _Employer Mode_ allows users to post jobs, search for candidates and hire them. The *Get Job* portal is designed to be simple and intuitive so that users can easily navigate the app and perform the desired actions.

Live Demo: https://get-job.live

Heroku: https://get-job.herokuapp.com



![mockup]()

## Table of Contents
...

## Agile UX
The main goal of the app is to deliver a solution that creates real value for the users and _UX design_ and _Agile Methodology_ are the best way to achieve this goal.

#### Project Goals
- To help jobseekers get a job.
- To help employers connect with the right candidates.
- To provide a website with a clear purpose.
- To provide a simple and intuitive UI that allows users to easily navigate the app.
- To make the website available and functional on every device, especially on mobile devices, as they are the most popular devices for job search.
- To set up an authentication mechanism that allows users to create their profile, save and manage their data.


### User Stories
#### Jobseeker Goals
- ##### First Time Visitor:
    - As a Jobseeker I want to be able to see the purpose of the app so that I can decide if it is useful for me.
    - As a Jobseeker I want to be able to see the navigation bar so that I can easily navigate the app.
    - As a Jobseeker I want to be able to create a resume so that I can apply for jobs.
    - As a Jobseeker I want to be able to search for jobs so that I can find an appropriate job.
    - As a Jobseeker I want to be able to see the latest jobs so that I be informed about new jobs.
    - As a Jobseeker I want to be able to register an account so that I can build my profile.

- ##### Frequent Visitor:
    - As a Jobseeker I want to be able to see the navigation bar when I scroll the page up so that I can access the navigation bar at any time.
    - As a Jobseeker I want see the dropdown menu so that I can access the most important features of the app.
    - As a Jobseeker I want to be able to log in to my account so that I can manage my data and apply for jobs.
    - As a Jobseeker I want to be able to update my profile so that I can keep my data up to date.
    - As a Jobseeker I want to be able to get notifications so that I can be informed about my applications.
    - As a Jobseeker I want to be able to open the appropriate job so that I can see the full job description.
    - As a Jobseeker I want to be able to see a full detailed view of the job so that I can decide if the job is appropriate for me.
    - As a Jobseeker I want to be able to apply for a job so that I can get a job.
    - As a Jobseeker I want to be able to see my applications so that I can manage them.
    - As a Jobseeker I want to be able to log out so that I can protect my data.
    - As a Jobseeker I want to be able to see the number of applicants for a job so that I can see my chances to get a job.
    - As a Jobseeker I want to be able to open the list of all jobs.
    - As a Jobseeker I want to be able to select sort order for the list of jobs so that I can see the most relevant jobs first.
    - As a Jobseeker I want to be able to reset my password so that I can restore access to my account.
    - As a Jobseeker I want to be able to select the searching area in the list of jobs so that I can find jobs in the desired area.
    - As a Jobseeker I want to be able to use the search bar on the page of the full list of jobs.
    - As a Jobseeker I want to be able to reset search parameters so that I can see the full list of jobs.
    - As a Jobseeker I want to be able to see the search panel all the time when I scroll the page so that I can easily search for jobs.
    - As a Jobseeker I want to be able to save a job so that I can apply for it later.
    - As a Jobseeker I want to be able to see my favorite jobs so that I can apply for them later.
    - As a Jobseeker I want to be able to see the list of my resumes so that I can manage them.
    - As a Jobseeker I want to be able to see the Apply and Save buttons on the detailed job page on the mobile screens all the time when I scroll the page so that I can easily apply for a job or save it for later.
    - As a Jobseeker I want to be able to go back to the list of jobs from the detailed job page so that I can continue searching for jobs.
    - As a Jobseeker I want to be able to have access to the search bar on the navigation panel so that I can easily search for jobs at any time.
    - As a Jobseeker I want to be able to delete my account so that I can remove my data from the app.
    - As a Jobseeker I want to be able to see the date when the job was posted so that I can see how old the job post is.
    - As a Jobseeker I want to be able to see all jobs of the particular company so that I can find a job in the company I like.
    - As a Jobseeker I want to be able to see buttons for pagination so that I can navigate through the list of jobs.
    - As a Jobseeker I want to be able to return to the home page from the list of jobs so that I can access the home page at any time.
    - As a Jobseeker I want to be able to see the number of jobs found in the list of jobs so that I can see how many jobs are available based on my search criteria.
    - As a Jobseeker I want to be able to see the footer with the navigation links so that I can easily navigate the app.
    - As a Jobseeker I want to be able to change the password so that I can protect my account.

#### Employer Goals
- ##### First Time Visitor:
    - As an Employer I want to be able to see the navigation bar so that I can easily navigate the app.
    - As an Employer I want to be able to toggle the site to employer mode so that I can see the relevant content.
    - As an Employer I want to be able to see the purpose of the app so that I can decide if it is useful for me.
    - As an Employer I want to be able to post a job so that I can find the right candidate.
    - As an Employer I want to be able to register an account so that I can add jobs.
    - As an Employer I want to be able to search for resumes so that I can find the right candidate.
    - As an Employer I want to be able to see the latest resumes so that I be informed about new candidates.

- ##### Frequent Visitor:
    - As an Employer I want to be able to see the navigation bar when I scroll the page up so that I can access the navigation bar at any time.
    - As an Employer I want to be able to login to my account so that I can manage my jobs.
    - As an Employer I want to be able to update my profile so that I can keep my data up to date.
    - As an Employer I want to be able to see my all posted jobs so that I can manage them.
    <!-- - As an Employer I want to be able to see applicants for my jobs so that I can select the right candidate. -->
    - As an Employer I want to be able to open a resume card from the search results so that I can see the full resume.
    - As an Employer I want to be able to see a full detailed view of the jobseeker's resume so that I can decide if the candidate is the perfect match for my job.
    - As an Employer I want to be able can to get notifications so that I can be informed about new applicants.
    - As an Employer I want to be able to logout so that I can protect my data.
    - As an Employer I want to be able to open the list of all resumes.
    - As an Employer I want to be able to select the sort order for the list of resumes so that I can see the most relevant resumes first.
    - As an Employer I want to be able to reset my password so that I can restore access to my account.
    - As an Employer I want to be able to use search filters on the list of resumes so that I can find the right candidate.
    - As an Employer I want to be able to use the search bar on the page of the full list of resumes.
    - As an Employer I want to be able to reset search parameters so that I can see the full list of resumes.
    - As an Employer I want to be able to see the search panel all the time when I scroll the page so that I can easily search for resumes.
    - As an Employer I want to be able to hire a jobseeker so that I can get the right candidate.
    - As an Employer I want to be able to save a resume so that I can hire the candidate later.
    - As an Employer I want to be able to see the bookmarked resumes so that I can hire the candidate later.
    - As an Employer I want to be able to see the Hire and Save buttons on the detailed resume page on the mobile screen all the time when I scroll the page so that I can easily hire a candidate or save the resume for later.
    - As an Employer I want to be able to return to the list of resumes from the detailed resume page so that I can continue searching for candidates.
    As an Employer I want to be able to have access to the search bar on the navigation panel so that I can easily search for resumes at any time.
    - As an Employer I want to be able to close/deactivate the job so that I can stop receiving new applications and remove the job from the search results.
    - As an Employer I want to be able to reopen/activate the job so that I can start receiving new applications and the job will be shown in the search results.
    - As an Employer I want to be able to delete the job so that I can remove it from the list of my jobs.
    - As an Employer I want to be able to update the job details so that I can keep the job information up to date.
    - As an Employer I want to be able to delete my account so that I can remove my data from the app.
    - As an Employer I want to be able to style the job description so that I can make it more readable and attractive.
    - As an Employer I want to be able to see the button for pagination so that I can navigate through the list of resumes.
    - As an Employer I want to be able to return to the home page from the list of resumes so that I can access the home page at any time.
    - As an Employer I want to be able to see the number of resumes found in the list of resumes so that I can see how many resumes are available based on my search criteria.
    - As an Employer I want to be able to see the footer with the navigation links so that I can easily navigate the app.
    - As an Employer I want to be able to change the password so that I can protect my account.

#### Moderator Goals
- As a Moderator I want to be able to review and approve the posted jobs so that I can protect the app from inappropriate content.

### Agile methodology
This project was developed with the Agile methodology which allowed me to develop the app iteratively and incrementally, and adapt changes with flexibility even in the late stages of development.

_GitHub Issues_ and _Projects_ are used to manage the development process. Each part of the app is divided into _Epics__ which are broken down into _User Stories_ and _Tasks_. An Epic represents a large body of work, such as a feature.

Each Epic is developed in a separate branch and merged to the master branch after testing and debugging and then deployed to the production server on _Heroku_. The _master_ branch is always production-ready and all changes are deployed automatically to the production server. This helps isolate the development of each feature and minimize the risk of breaking the production code. The feature branches merged to the _master_ branch using _Pull Requests_ which allows to review of the code and test the changes before merging.

_GitHub Kanban_ board is used to track the progress of the development process. When _User Story_ is created, it is automatically added to the _Backlog_ column to be prioritized. The product _Backlog_ is never complete, as it is a dynamic document to respond to changes effectively. As new features are identified, they are added to the product _Backlog_. As the product is released, the product _Backlog_ is constantly updated to reflect changes in the product and changes in the market. The Kanban board includes the following columns:
- **Backlog** - the list of all _User _Stories_ that have not yet been scheduled to be completed. As new _User Stories_ are created, they are automatically added to the _Backlog_ column.
- **Sprint Backlog** - the collection of prioritized _User Stories_ that have been selected for the current _Sprint_.
- **Development** - the user stories that are currently being developed.
- **Testing** - user stories that are currently being tested.
- **Done** - all completed and tested _User Stories_.

The _User Stories_ were prioritized using the _MoSCoW_ method and moved to the _Sprint Backlog_ column and added to the _Milestone_. The prioritisation was based on the following criteria:
- **Must Have** - The _User Story_ is crucial and add significant value to the product and must be delivered in the current iteration.
- **Should Have** - The _User Story_ is important but not critical to the success. Simply delivery is not guaranteed within the current iteration.
- **Could Have** - The _User Story_ is desirable and would only be delivered in their entirety in a best-case scenario. When a problem occurs and the deadline is at risk, one or more could-have items are dropped.
- **Won't Have** - The _User Story_ will not be delivered in the current delivery timebox but may be considered for the future.

_Milestones_ were used to group issues into sprints. When the _Sprint_ starts, the _Milestone_ is created and the _User Stories_ are prioritised using the _MoSCoW_ method and added to the _Sprint Backlog_ column. The user story that is currently being developed is moved to the _Development_ column.
Then after the development is completed, the _User Stories_ are moved to the _Testing_ column. When the testing is successfully completed, the _User Stories_ closed using a _commit_ message with reference to the User Story ID.

### Structure
The Get Job platform is based on an intuitive and easy-to-use structure. Every page has a consistent layout and navigation to allow users to easily find the information they need. The app has a responsive design to provide an optimal viewing experience across a wide range of devices.

- The Jobseeker's and Employer's Navbar structures are similar but have different purposes. The Jobseeker can search for jobs and the Employer can search for resumes as well as Jobseeker can create a resume and the Employer can create a job post.
- The index page of the app is a Jobseeker home page which can be toggled to the Employer home page. The Jobseeker and the Employer home page structure is similar. The difference is only in the content of the pages.
- The login page contains an indentical login form for jobseekers and employers but the user has to select the role before login.
- The registration forms are different for jobseekers and employers as they include different fields.
- The List of Resumes and the List of Jobs page structures are identical. The difference is also only in the content of the pages.
- The app also includes separate Detailed pages of the Resume and the Job.
- Jobseekers and Employers have their own Profile pages to manage their accounts and view their resumes and created jobs.


#### Flowchart
The flowchart below shows the structure of the app and the relationships between the pages. The flowchart was created using [Microsoft Visio](https://www.microsoft.com/en-ie/microsoft-365/visio/).
![flowchart]()

### Database Design
The Get Job platform uses a relational database to store and manage data. The RDBMS used for this project is [PostgreSQL](https://www.postgresql.org/) which is hosted on the cloud service [ElephantSQL](https://www.elephantsql.com/).

The ER Diagram below shows the structure of the database and the relationships between the tables. This diagram was created using [Microsoft Visio](https://www.microsoft.com/en-ie/microsoft-365/visio/).
![er_diagram]()


### UI Design
...

#### Wireframes


## Features
Since the User always visits the site for some content and some purpose, the Features of the app are primarily designed to solve the problems of the Jobseekers and Employers and help them to achieve their goals. The UX is designed to create single-use learning and does not distract users' attention from the main goal - to find a job or a candidate.

### Jobseeker's Home page
The Jobseeker's Home page is designed to help Jobseekers to find a job quickly and easily. The page divided into 5 sections: Navbar, Hero, Search panel, Latest Jobs, and Footer.
![jobseeker_home]()

#### Sections:
- #### Navbar
The navigation bar is designed to be simple and intuitive. It includes the app logo, the toggle button to switch between the Jobseeker's and Employer's Home pages, the Sign-Up / Sign-In buttons if the user is not logged in and the Search bar, a Notification icon and the Profile dropdown menu if the user is logged in. The Navbar is fully responsive and the text of the Logo and Sign Up / Sign In buttons as well as the Search bar is hidden on small screens to save space. The Dropdown menu expands to full width on small screens to make it easier to use. In addition, the search bar of the Navbar is moved to the Dropdown menu on small screens to be easily found as it is the main feature of the app.
The Navbar is flexible and always available when the user needs. It hides on scroll down and shows on scroll up.
![navbar]()

- #### Hero
The Hero section contains call-to-action headings and a button to encourage users to create a resume. The image of the section conveys the main message of the app - recruiters are looking for candidates reviewing resumes. When the users are clicking on the `Create Resume` button and if they are logged in, then they are redirected to the Create Resume page, otherwise to the Sign-Up / Sign-In.
![hero]()

- #### Jobseeker's Search bar
One of the important features of the app is the search bar. It is placed in the center of the page to be easily found and allows users to achieve their main goal - to find a job quickly and easily. The functionality of the search bar is the same as the search bar of the Navbar. It takes the user input and searches for the jobs that match the input.
![search_bar]()

- #### Latest Jobs
The Latest Jobs section is a list of the latest vacancies posted by Employers. Each Vacancy represented by a Bootstrap Card component. The Card contains the Job Title, Days ago, the Company Name, the Location, the Salary and the main section of the Job Description. The card title is clickable and redirects the user to the Job Details page. Also a user can save the job to the Favorites or directly Apply for the Job escaping the Job Details page. The section is fully responsive. On small screens, the cards are arranged in one column and on extra large screens in two columns to be easily readable.
![latest_jobs]()

### Job Search page
#### Sections:
- #### Search results
The user can access the Job Search page by using the search bar on the Home page. When the user submits the search query, the app redirects them to the Job Search page and displays the search results.
The search results represented by the Bootstrap Cards, the same as the Latest Jobs section on the Home page. Each card is clickable and redirects the user to the Job Details page.
- #### Search panel
Also, the page contains the full search panel with the search filters including _Job Title_, _Area_, _Job Location_ and _Job Type_. Each filter has a dropdown menu with the list of options. The user can select the options and combine the filters to narrow the search results. The panel is sticky on large screens and always available when the user scrolls the page. On small screens, the search panel is collapsible to save space. The user can expand it by clicking on the `Tap to Expand Search Panel` button. This panel is collapsed by default and also collapsed when user submit the valid search query to leave the more space for the search results. If the user submits the invalid search query, the panel is expanded and the user can see the form validation errors under the input fields.
- #### Number of found jobs and Back to Home button
On the top right side of the page's main container, the user can see the number of found jobs by the search query and return to the Home page by clicking on the arrow icon that is on the left top side of the container.
- #### Pagination
The search results are paginated to improve the UX and make the page more user-friendly. Implemented two types of pagination - with the page numbers and with the Previous and Next buttons to give the user the choice:
- The Previous and Next buttons respresented by the Font Awesome icons. Also the user can jump to the first or the last page by using the appropriate buttons with the double arrows.
- The pagination with the page numbers is implemented as _Elided Pagination_, so the user can see the first and the last page at the start and the end of the pagination bar respectively, the current highlighted page at the center and the previous and the next pages on the left and the right sides of the current page. The other pages are hidden with the ellipsis.

![back_to_top_button]()

### Job Details page

#### Sections:
...

### Apply for the Job
The user can apply for the job by clicking on the `Apply` button on the Job Card on the Home and Job Search pages or on the Job Details page. The button redirects the user to the `Job application` page.

The page contains the form with the two sections:
- First of all, the user must select the resume to apply for the job if there any resumes approved by the app support. If the user has no approved resumes yet, they will be prompted to create a new resume or check the all resumes status on the My Resumes page. If the user has approved resumes, they can select the resume using Radio buttons. Also each resume has the `View` button that allows the user to see the resume details or/and edit the resume. The View page is opened in the new tab to prevent the user from losing the data in the application form.
- The second section of the form is the Cover Letter. The user can enter the cover letter text in the textarea. The text is limited to 1000 characters and is not required. The max lenght validation is on the client-side and on the server-side as well. The client-side validation prevents the user from entering more than 1000 characters and the server-side validation prevents the user from submitting the form with the cover letter text longer than 1000 characters. The validation errors are displayed under the textarea.

The user can submit the application form only if they selected the resume. Is the user tries to submit the form without selecting the resume, the app displays the default browser validation error message `Please select one of these options`. Also if the malicious user tries to submit the form with disabled JavaScript validation, the server-side validation will still prevent the submission and the user will see the appropriate error message under the resume selection section.


### Jobseeker's Profile page
...

- #### Account Deleting
The user can delete(in fact deactivate) their account by clicking on the `Delete` button in the _Delete account_ section of the Profile page. The button redirects the user to the `Confirm Account Delete` page where they must confirm the deletion by entering their password. If the user enters the correct password, the account is deactivated and the app redirects the user to the Home page and displays the message that the account is deactivated and will be deleted in 30 days. So if the user changes their mind, they can contact the app support and reactivate their account. The appropriate message is displayed when the user tries to log in with the deactivated account as well as the app redirects them to the Create Account page.

- #### My Resumes
The user can create multiple resumes and manage them on the My Resumes page. The page contains the table of the current Jobseeker resumes. Each row of the table represents the resume and includes the Resume Title(Ocupation), the Resume Status, the Last Updated date and the Action buttons.
- The **Resume Title** is clickable and redirects the user to the Resume Details page. The title is truncated to 40 characters to fit the table cell and be more readable on small screens. Each word of the title is line-breaked to the new line on small screens, but if the title contains the long word, the table cell is expanded to fit the word until it will be truncated. Then if the table is too wide, the horizontal scrollbar appears.
- The **Resume Status** indicates the current status of the resume. The status can be _In Review_, _Rejected_, _Active_ or _Closed_. The row color depends on the status. The _In Review_ status is yellow, the _Rejected_ status is red, the _Active_ status is green and the _Closed_ status is gray. The _In Review_ status is set by default when the user creates or updates the resume details. Each status has the appropriate tooltip with the description that appears when the user hovers over the icon.
Other statuses can be set by the admin. The _Rejected_ status means that the resume does not meet the requirements or contains the inappropriate content. The _Active_ status means that the resume is approved by the admin and is visible to the Employers. The _Closed_ status means that the resume is closed by the user and is not visible to the Employers.
- The **Last Updated** date converted to the user-friendly format by custom template filter and displayed as time ago. E.g. _2 days ago_ or _1 month ago_.
- The **Control** buttons allow the user to manage the resume. The user can edit the resume details, delete the resume or close the resume. The _Edit_ button redirects the user to the Resume Update page. All resumes except the _Closed_ resumes can be edited. The _Close_ and _Delete_ buttons open the modal window to asks the user to confirm closing/deletion. Once the user has confirmed the action, and the table is updated and an appropriate message shown. The _Close_ button changed to _Open_ and the resume status is changed to _Closed_. The user can reopen the resume, update and display it to the employers again. Once the resume was reopened, it gets the _In Review_ status by default, so the user can update it or/and wait for approval. Only the _Active_ resumes will be shown in the search results and can be viewed by the Employers.
- The **Create New Resume** button redirects the user to the Resume Create page where they can create the new resume. The user can have only up to 5 resumes. If the user tries to create the new resume when they already have 5 resumes, the app redirects them to the My Resumes page and displays the appropriate modal alert. So the user can delete the old resume to create the new one.

- #### My Resume Details
<!-- TODO: Add anchor link to the Resume Details in employer section -->
The Resume Details page is available from the My Resumes list. The page is similar to the Resume Details page of the Employer, but has the different color interface (jobseeker style) and the different functionality. The user can update the resume details, close or delete the resume using the appropriate buttons. These buttons have the same behavior as the buttons on the My Resumes page.


- #### Saved Jobs
The user can save any job to the Favorites by clicking on the `Save` button on the Job Card or on the Job Details page. All saved jobs can be viewed on the Saved Jobs page that is available from the Jobseeker's Dropdown menu only for the authenticated users. The page contains a list of the saved jobs. Each row of the list represents a job and is clickable. So the user can view the job details by clicking on the job title. Also the row contains Action buttons that allow a user to remove the job from the Favorites or directly apply for the job. The removing action does not require the confirmation, as this action is not critical.

### Employer's Home page

#### Sections:
- #### Navbar

- #### Hero

- #### Employer's Search bar

- #### Latest Resumes


##### Card Image
To store the images of the Jobseekers, I used the [Cloudinary](https://cloudinary.com/) service.
The Cloudinary field uses the Cloudinary API to upload the images to the Cloudinary server and store the image URL in the database. The Cloudinary API provides a lot of functionality to manipulate the images.
For the Jobseekers profile avatars, I used the `gravity` AI feature to crop the images to the square shape based on the face detection. Also, I set `public_ids` based on the user email addresses as the unique identifiers of the images. The names generated from the email addresses using the regex pattern to replace the all non-alphanumeric characters with the underscore. The images resized to the 200x200 pixels and changed the format to the WebP to improve the performance of the app and save the Cloudinary storage space.

### Resume Search

#### Sections:
...

- #### Age range selector
As the multiple sliders are not supported by the Bootstrap, I used the [jQuery UI Slider](https://jqueryui.com/slider/) to implement the Age range selector. The user can select the age range by dragging the slider handles or by clicking on the slider bar. The selected range is displayed in the Age range decorative input field. The input field is read-only and disabled. To capture the slider state and insert it into the form I implemented the hidden input fields that are part
of the Django Form. It allows me to validate the inputed by the user age range using server side django validation if the malicious user is trying to force a value change of the hidden input fields or set an invalid value into the search query in the url.


### Resume Details

#### Sections:
...

### Hiring page
...

### Login/Register
The app allows users create an account and have additional features that are not available for the anonymous users. To get on the register or login page, the user can click on the `Sign Up/Sing In` button in the Navbar or they will be redirected automatically to the login page when they are trying to access the page that is available only for the logged in users, e.g. the Apply for the Job page or the Hiring page.

- #### Sign Up form
The Sign Up form is implemented based on the Django Allauth package. The form contains the role, email, password and password confirmation fields and the Sign Up button.
- The role field is a choice field with two options - Jobseeker and Employer. The initial role set automatically and depends where user is coming from. If the user is coming from the page related to Jobseeker, the role is set to Jobseeker. If the user is coming from Employer's page, the role is set to Employer appropriately. But the user can change the role by selecting the appropriate option based on radio buttons. The role field is mandatory and the user can not submit the form without selecting the role, as the role tied to the user account and can not be changed later.
- The email field is a unique identifier of the user and the system does not allow users to register multiple accounts with the same email address. So the Jobseeker and the Employer can not have the same email address.
- The password field as also required and the user can not submit the form without setting the password. The validation of the password is implemented on the client side and on the server side based on the Django Allauth package.

After successful registration, the user is redirected to the Profile page appropriate to the selected role to complete the profile.

Additionaly for the user convenience, the form contains the header with the back to the previous page button that based on the next parameter in the url, and the Sign In link if the user already has an account.

- #### Login form
The Login form is also based on the Django Allauth. The user can login by email and password. The user does not have to select the role to login, as the role is tied to the user account. So the role (Jobseeker or Employer) is set automatically based on the user account.
So the user will be redirected to the appropriate page after successful login based on the next parameter in the url. If the next parameter is not set, the user will be redirected to the Home page appropriate to the role of an account. Although the user will be redirected to next parameter if it is set, the user can only access the page appropriate to the role. So if the unauthenticated user tries to apply for the job, they will be redirected to the Login page. After successful login, the user will be redirected to the Apply for the Job form if the role is Jobseeker, otherwise the user cannot access the Apply for the Job page and get appropriate feedback.
When the user is logged in, the Sign Up/Sign button in the Navbar is replaced by the Profile button. The Profile button contains the dropdown menu. Each role has its own dropdown menu with the appropriate links:
- **Jobseeker**:
My Profile, Search for Jobs, Create Resume, My Applications, Favourite Jobs, Logout
- **Employer**:
My Profile, Search for Resumes, Add a Vacancy, My Jobs, Logout

The authenticated user can have access only to the menu appropriate to the role. So the Jobseeker can not access the options related to the Employer and vice versa. Instead of the Profile button for an authenticated user not associated with his role, the user will see the specific message that the user is logged in as a Jobseeker/Employer and the Logout button.

- #### Logout
The Logout button is available for the authenticated users only and located in the Profile dropdown menu or Sign Up/Sign menu on the page that not associated with current role. When the user clicks on the Logout button, the modal window appears with the confirmation message. The user can confirm the logout by clicking on the Logout button or cancel the logout by clicking on the Dismiss button. After successful logout, the user will be redirected to the Home page.

### Development Features
- #### Django Authentication and Authorization System
The app uses the Django Allauth package that is built on top of the built-in Django Authentication and Authorization System. The system provides a secure way to manage user accounts and allows users to create an account, login, logout, reset password, and update their profile. Also, the package is used to provide additional features such as email verification, social authentication, and password reset.

- #### Role System
To manage the different types of users, I created Custom User Model and implemented a role system.
The app contains two main types of users - Jobseekers and Employers. So the system allows users to create an account as a Jobseeker or an Employer. All the time when we want to create a new user, we have to assign him to a role. The email address is used as a unique identifier of the user and the system does not allow users to register multiple accounts with the same email address. So the Jobseeker and the Employer can not have the same email address.

The role system was implemented by adding a `role` field to the `User` model. The `role` field is a choice field with options `Admin`, `Jobseeker`, and `Employer`. The `role` field also provides access to the appropriate pages, features and content of the app. For example, the Jobseeker can not create a job post and the Employer can not apply for a job.

- #### Branching Strategy
The app was built using the _Feature_ branching strategy. The strategy allows me to create a branch for a specific feature, task or bug without affecting the `master` branch, which keeps the main codebase clean and stable.

I have two main branches - `master` and `develop`. Whenever I want to add a new feature, I create a new branch from the `develop` branch. Then I develop the feature and when it is ready, I create a pull request and merge the `feature` branch into the `develop` branch. Before merging, the code is processed by the Continuous Integration (CI) system to check the code quality and run tests. Then the branch is deployed to the Heroku staging environment for manual testing. When the testing is completed, I pull the latest changes from the remote `develop` branch to the local `develop` branch and merge it into the local `master` branch. Then I push the local `master` branch to the remote `master` branch which triggers the GitHub Actions CI system to run tests. When the CI system successfully completes the checks, the branch is deployed to the Heroku production environment. The strategy allows me to keep the `master` branch clean and stable and test the app before it is deployed to the production environment.

See the [Deployment](#deployment) section for more details about the CI/CD process.

|Branching Strategy|
|:--:|
|![branching_strategy](docs/images/ci-cd-diagram.avif)|

- #### Database
The app uses a relational database service [ElephantSQL](https://www.elephantsql.com/) to store and manage data.

- #### Static Files
The app uses the [Cloudinary](https://cloudinary.com/) cloud service to store static files such as images, CSS, and JavaScript files.

## Technologies Used
- ### Languages
    - [HTML5](https://en.wikipedia.org/wiki/HTML5)
    - [CSS3](https://en.wikipedia.org/wiki/CSS)
    - [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
    - [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
- ### Frameworks, Libraries
    - [Django 4.2](https://docs.djangoproject.com/en/4.2/)
    - [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
    - [jQuery 3.6.4](https://releases.jquery.com/)
    - [jQuery UI 1.13.2](https://jqueryui.com/)
    - [Font Awesome 6.4](https://fontawesome.com/)
    - [Google Fonts](https://fonts.google.com/)
    - [libsass](https://pypi.org/project/libsass/)
    - [coverage](https://coverage.readthedocs.io/en/7.2.7/)

- ### Tools
    - [Git](https://git-scm.com/)
    - [GitHub Actions](https://docs.github.com/en/actions)
    - [Heroku Pipelines](https://devcenter.heroku.com/articles/pipelines)
    - [Microsoft Visio](https://www.microsoft.com/en-ie/microsoft-365/visio/)
    - [Cloudinary](https://cloudinary.com/)
    - [Balsamiq](https://balsamiq.com/)
    - [Sass](https://sass-lang.com/)

- ### Django packages
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [cripsy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5)
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/)
- [django-compressor](https://django-compressor.readthedocs.io/en/stable/)
- [django-sass-processor](https://pypi.org/project/django-sass-processor/)


## Testing
See [TESTING.md]() for an overview of the app testing and debugging.
<!-- TODO Add screenshots of the coverage report -->

## Deployment, CI/CD
The Get Job platform is deployed on the [Heroku](https://www.heroku.com/) cloud platform and can be accessed here https://get-job.live.
The _get-job.live_ domain name uses the [Heroku DNS service](https://devcenter.heroku.com/articles/custom-domains) to point to the Heroku app. Usually Heroku free dyno plan does not support [SSL certificates for custom domains](https://devcenter.heroku.com/articles/ssl#dynos-and-certificate-options). But they provides a free ssl certificate for the _herokuapp.com_ domain. So the dyno is upgraded to the Hobby plan to enable the ssl certificate for the custom domain.

The build, test, and deployment processes of the app are _automated_ using Continuous Integration based on [GitHub Actions](https://docs.github.com/en/actions) and Continuous Deployment based on [Heroku Pipelines](https://devcenter.heroku.com/articles/pipelines).

- #### Continuous Integration
The GitHub repository is configured to use automated _Continuous Integration_ workflows. The workflow is triggered when a pull request is created and merged into the `develop` and/or `master` branches. When the workflow is triggered, it performs the build, lint, and test tasks.

- #### Continuous Deployment
The _Continuous Deployment_ workflow is implemented using [Heroku GitHub Integration](https://devcenter.heroku.com/articles/github-integration). This feature allows me to connect the app to a GitHub repository and deploy the app automatically from the selected branch when a new commit is pushed to the repository. The GitHub integration also supports the option to [wait for CI to pass before deploying](https://devcenter.heroku.com/articles/github-integration#automatic-deploys) the app. So the app is deployed automatically only when the build and test tasks are passed.

[Heroku Pipelines](https://devcenter.heroku.com/articles/pipelines) is used to implement the _Continuous Deployment_ workflow. The pipeline is configured to deploy the app to the two environments - _Staging_ and _Production_:
1. The _Staging_ stage is used to preview code changes and features before being deployed to production. This stage is triggered when a new commit is pushed to the `develop` branch or a pull request is merged into the branch from the feature branches. The app is deployed to the Heroku staging environment automatically when the tests are passed. The staging environment is available here https://get-job-dev.herokuapp.com.
2. The _Production_ stage is a live environment for the app. It is triggered when a new commit is pushed to the `master` branch. It also deploys the app automatically when GitHub Actions CI is passed. The production environment is available by the link https://get-job.herokuapp.com.

## Credits
- ### Code
The Get Job platform is based on my own implementation of code, applying what I have learned from the [Code Institute](https://codeinstitute.net/) Full Stack Software Development course and other educational resources.

- ### Educational Resources
    - Django Multiple User Types, Custom User Model, and email authentication
    https://youtu.be/f0hdXr2MOEA
    https://youtu.be/Z6QMPAcS6E8
    https://medium.com/geekculture/how-to-implement-multiple-user-types-in-django-b72df7a98dc3
    https://medium.com/@royprins/django-custom-user-model-email-authentication-d3e89d36210f
    - CI/CD pipelines
    https://blog.logrocket.com/ci-cd-pipelines-react-github-actions-heroku/


- ### Content
    - Logo Briefcase from https://uxwing.com
    - Hero image of the jobseeker page designed By agny_illustration from https://pngtree.com/freepng/modern-flat-design-concept-of-recruitment-presentation-for-employment-and-recruiting-application-for-employee-hiring-can-used-for-web-banner-infographics-landing-page-flat-vector-illustration_5332898.html?sol=downref&id=bef
    - Hero image of the employer page designed by pikepicture from https://pngtree.com/freepng/recruitment-process-vector-human-resources-choice-of-candidate-employee-office-chair-vacancy-executive-search-recruiting-hiring-hr-isolated-illustration_5190146.html?sol=downref&id=bef?sol=downref&id=bef
    - Branching Strategy diagram is taken from [ci-cd-pipelines-react-github-actions-heroku](https://blog.logrocket.com/ci-cd-pipelines-react-github-actions-heroku/) blog post.
    - Placeholder Company image by <a href="https://pixabay.com/users/ricinator-3282802/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2010880">Ricarda Mölck</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2010880">Pixabay</a>

## Contacts
If you have any questions about the project, or you would like to contact me for any other reason, please feel free to contact me by email or via social media.

[![Gmail Badge](https://img.shields.io/badge/-flashdrag@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:flashdrag@gmail.com)](mailto:flashdrag@gmail.com)

[<img src='https://img.shields.io/badge/Telegram-333333?style=for-the-badge&logo=telegram&logoColor=white&style=plastic&logoWidth=20&labelColor=2CA5E0' alt='Telegram'>](https://t.me/flashdrag) [<img src='https://img.shields.io/badge/LinkedIn-333333?style=for-the-badge&logo=linkedin&logoColor=white&style=plastic&logoWidth=20&labelColor=0077B5' alt='Telegram'>](https://www.linkedin.com/in/pavlo-myskov)
