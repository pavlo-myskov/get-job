# Get Job Testing

## Table of Contents
- [Unit Testing](#unit-testing)
    * [Coverage](#coverage)
- [PEP8 - Flake8 Validation](#pep8---flake8-validation)
- [JavaScript Validation](#javascript-validation)
- [HTML Validation](#html-validation)
- [CSS Validation](#css-validation)
- [Lighthouse](#lighthouse)
    * [Desktop](#desktop)
    * [Mobile](#mobile)
- [Compatibility Testing](#compatibility-testing)
    * [Browser Compatibility](#browser-compatibility)
    * [Device Compatibility](#device-compatibility)
- [User Stories Testing](#user-stories-testing)
    * [Jobseeker](#jobseeker)
    * [Employer](#employer)
- [Bugs/Issues](#bugs/issues)

[Back to README.md](https://github.com/FlashDrag/get-job/blob/master/README.md#testing)

## Unit Testing
The unit tests were written using Django's built-in testing framework based on Python's unittest module. The tests can be found in the `tests' directory of each Django app. To run the tests automatically I used CI/CD processes with GitHub Actions. The more detailed information about the CI/CD processes can be found in the [Deployment](https://github.com/FlashDrag/get-job/blob/master/README.md#continuous-integration) section of the file.

*Django Unit Tests GitHub Actions Workflow*
![Unit Tests](images/testing/unit-testing.png)

### Coverage
The coverage report was generated using the [Coverage](https://coverage.readthedocs.io/) tool.
To generate the HTML report I used the following command:
```
$ coverage run manage.py test
$ coverage html
```

![Coverage Report](images/testing/Coverage-report.png)


## PEP8 - Flake8 Validation
The Flake8 validation is used to check the Python code for PEP8 requirements. The validation is configured in the `production.yml` and `development.yml` files in the `.github/workflows` directory. The validation is run automatically with the CI/CD processes.

*Flake8 Validation GitHub Actions Workflow*
![Flake8 Validation](images/testing/flake8.png)

[Back to top](#table-of-contents)

## JavaScript Validation
To validate the JavaScript code I used the [JSHint](https://jshint.com/) tool. As I used single JavaScript file `script.js` for the whole website I pasted the code into the JSHint tool and validated it.

![JSHint Validation](images/testing/JSHint.png)

## HTML Validation
To validate the HTML code I used the [W3C Markup Validation Service](https://validator.w3.org/). The HTML code was validated for each page of the website as the app uses Django's templates to render the HTML code.

| Page | Result |
| :--- | :---: |
| Jobseeker Home | [Jobseeker Home](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2F)
| Job Search | [Job Search](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fjobs%2F)
| Job Details | [Job Details](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fjobs%2F7)
| Employer Home | [Employer Home](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Femployer)
| Resume Search | [Resume Search](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fresumes%2F)
| Resume Details | [Resume Details](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fresume%2F6)


## CSS Validation
To validate the CSS code I used the [Jigsaw](https://jigsaw.w3.org/css-validator/) tool. As I used the SCSS preprocessor to write the CSS code, I validated the compiled `main.css` file that stores all the CSS code an located on the Cloudinary CDN.
<p>
    <a href="http://jigsaw.w3.org/css-validator/validator?lang=en&profile=css3svg&uri=https%3A%2F%2Fres.cloudinary.com%2Fdvj4gdxes%2Fraw%2Fupload%2Fv1%2Fstatic%2Fget-job%2Fcss%2Fmain.css&usermedium=all&vextwarning=&warning=1">
        <img style="border:0;width:88px;height:31px"
            src="https://jigsaw.w3.org/css-validator/images/vcss-blue"
            alt="Valid CSS!" />
    </a>
</p>

![main css validation results](images/testing/CSS-Validator.png)

[Back to top](#table-of-contents)


## Lighthouse
The Google Lighthouse tool was used to check the performance, accessibility, best practices, and SEO of the website. The tests were run on the deployed website.

### Desktop
| Page | Result |
| :--- | :--- |
| Jobseeker Home | ![Jobseeker Home](images/testing/lighthouse/home.png) |
| Job Search | ![Job Search](images/testing/lighthouse/jobs.png) |
| Job Details | ![Job Details](images/testing/lighthouse/job-details.png) |
| Employer Home | ![Employer Home](images/testing/lighthouse/employer-home.png) |
| Resume Search | ![Resume Search](images/testing/lighthouse/resumes.png) |
| Resume Details | ![Resume Details](images/testing/lighthouse/resume-details.png) |

### Mobile
| Page | Result |
| :--- | :--- |
| Jobseeker Home | ![Jobseeker Home](images/testing/lighthouse/home-mobile.png) |
| Job Search | ![Job Search](images/testing/lighthouse/jobs-mobile.png) |
| Job Details | ![Job Details](images/testing/lighthouse/job-details-mobile.png) |
| Employer Home | ![Employer Home](images/testing/lighthouse/employer-home-mobile.png) |
| Resume Search | ![Resume Search](images/testing/lighthouse/resumes-mobile.png) |
| Resume Details | ![Resume Details](images/testing/lighthouse/resume-details-mobile.png) |

[Back to top](#table-of-contents)

## Compatibility Testing
- ### Browser Compatibility
The game was tested on the following browsers:
    - Google Chrome
    - Mozilla Firefox
    - Microsoft Egde
The app worked well across all browsers and discrepancies were not found.

- ### Device Compatability and Responsiveness Testing
The app was tested using Google Chrome Developer Tool - Device Mode Toolbar.

Tested devices:
- iPhone SE
- iPhone 12 Pro
- Pixel 5
- Samsung Galaxy S8+
- Samsung Galaxy S20 Ultra
- iPad Air
- iPad Mini
- Surface Pro 7
- Surface Duo
- Galaxy Fold
- Samsung Galaxy A51
- Nest Hub
- Nest Hub Max
- iPad
- iPadPro

**Some results of the testing on iPhone 12 Pro**:
![Jobseeker Home](images/testing/responsiveness/home.png)
*Jobseeker Home*

![Job Search](images/testing/responsiveness/jobs.png)
*Job Search*

![Job Details](images/testing/responsiveness/job-details.png)
*Job Details*

![Employer Home](images/testing/responsiveness/employer-home.png)
*Employer Home*

![Resume Search](images/testing/responsiveness/resumes.png)
*Resume Search*

![Resume Details](images/testing/responsiveness/resume-details.png)
*Resume Details*

[Back to top](#table-of-contents)

## Manual Testing
#### User Stories Testing
- ##### Jobseeker
- [x] As a visitor, I easily understand the purpose of the website.
- [x] As a visitor, I can use search functionality to find a job.
- [x] As a visitor, I can view the details of a job.
- [x] As an unauthenticated visitor, I can press the "Apply" button on the job details page and get redirected to the login page.
- [x] As an unregisterd user, I switch to the register tab on the login page and register an account.
- [x] As a Jobseeker, I successfully register an account and get email confirmation.
- [x] The email confirmation link redirects me to the Edit Profile page to complete my profile. It also automatically logs me in.
- [x] As a Jobseeker, I can upload my profile picture and complete my profile.
- [x] The app redirects me to the Create Resume page after I complete my profile.
- [x] As a Jobseeker, I can create a new resume.
- [x] As a Jobseeker, I can view the details of my resume. The resume status is set to "IN REVIEW" by default.
- [x] As a Jobseeker, I can view the list of my resumes on the My Resumes page.
- [x] I can edit, close and delete my resumes.
- [x] As a Jobseeker, I can save a job to my Favourites for later review.
- [x] As a Jobseeker, I can view the list of my Favourites on the My Favourites page.
- [x] As a logged in Jobseeker, I can apply for a job by pressing the "Apply" button on the job details page.
- [x] I can view the the Employer's contact details and list of my approved resumes on the Job Application page.
- [x] I can click on my Resume to check the details. It opens in a new tab, so my Cover Letter is not lost.
- [x] As a Jobseeker, I can submit the application with my Cover Letter and selected Resume.
- [x] As a Jobseeker, I can view the list of my applications on the My Applications page.
- [x] I can view the details of my application including Vacancy and Resume snapshots that saved at the stage of application, except for personal details.
- [x] As a Jobseeker, I receive an email notification with a Job Offer for my other resume that I did not use for the application.
- [x] As a Jobseeker, I can view the details of the Job Offer on the Notifications and Job Offers page.
- [x] As a Jobseeker, I edit my profile and resumes.
- [x] As a Jobseeker, I change my password.
- [x] As a Jobseeker, I can disable the email notifications.
- [x] As a Jobseeker, I can delete my account.
- [x] As a Jobseeker, I can log out.
- [x] As a user, I see the flash messages on the top of the page after I perform an action.

## Bugs/Issues
- On the mobile devices, when the user returns to the search results page from the job details page, auto scroll to the same position on the page does not work. The user is returned to the top of the page. The auto scroll uses the anchor tag with the id of the job that passes to the name parameter of the anchor tag.
The issue is not present on the desktop version of the website.

Possible solution: change the name parameter to the id parameter of the anchor tag.

[Back to top](#table-of-contents)

[Back to README.md](https://github.com/FlashDrag/get-job/blob/master/README.md)