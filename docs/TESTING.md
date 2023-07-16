# Get Job Testing

## Table of Contents
...

## Unit Testing
The unit tests were written using Django's built-in testing framework based on Python's unittest module. The tests can be found in the `tests' directory of each app. To run the tests, use the following command: `python manage.py test`. To run the tests automatically I used CI/CD processes with GitHub Actions. The more detailed information about the CI/CD processes can be found in the **Deployment** section of the [README.md](https://github.com/FlashDrag/get-job/blob/master/README.md) file.

*Django Unit Tests GitHub Actions Workflow*
![Unit Tests](images/testing/unit-testing.png)

### Coverage
The coverage report was generated using the [Coverage](https://coverage.readthedocs.io/en/coverage-5.5/) tool. The report can be found in the `htmlcov` directory.
<!-- TODO Add screenshots of the coverage report -->

## PEP8 - Flake8 Validation
The Flake8 validation is used to check the Python code for PEP8 requirements. The validation is configured in the `production.yml` and `development.yml` files in the `.github/workflows` directory. The validation is run automatically with the CI/CD processes.

*Flake8 Validation GitHub Actions Workflow*
![Flake8 Validation](images/testing/flake8.png)


## JavaScript Validation
<!-- TODO -->

## HTML Validation
To validate the HTML code I used the [W3C Markup Validation Service](https://validator.w3.org/). The HTML code was validated for each page of the website as the app uses Django's templates to render the HTML code.

| Page | Result |
| :--- | :---: |
| Jobseeker Home | ![Jobseeker Home](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2F)
| Job Search | ![Job Search](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fjobs%2F)
| Job Details | ![Job Details](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fjobs%2F7)
| Employer Home | ![Employer Home](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Femployer)
| Resume Search | ![Resume Search](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fresumes%2F)
| Resume Details | ![Resume Details](https://validator.w3.org/nu/?doc=https%3A%2F%2Fget-job.live%2Fresume%2F6)



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

## Responsiveness
<!-- TODO -->

## Lighthouse
The Google Lighthouse tool was used to check the performance, accessibility, best practices, and SEO of the website. The tests were run on the deployed website.

### Desktop
| Page | Result |
| :--- | :--- |
| Jobseeker Home | ![Jobseeker Home](images/testing/lighthouse/jobseeker-home.png) |
<!-- TODO -->

### Mobile
| Page | Result |
| :--- | :--- |
| Jobseeker Home | ![Jobseeker Home](images/testing/lighthouse/jobseeker-home-mobile.png) |
<!-- TODO -->
...

## Manual Testing
<!-- TODO -->

## User Stories Testing
<!-- TODO -->

## Bugs
<!-- TODO -->