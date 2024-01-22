<h1 align="center">Fund Frontier</h1>

Welcome to Fund Frontier, a NPV Calculator designed to empower users in making informed investment decisions. This program facilitates the evaluation of the Net Present Value (NPV) for up to three projects simultaneously, enabling a comprehensive analysis of their financial viability. The Net Present Value, a crucial financial metric, considers the time value of money to assess the profitability of an investment by calculating the present value of future cash flows.

[This is the link](https://fund-frontier.onrender.com/) to the deployed webpage/URL.

[This is the link](https://github.com/sean-meade/fund-frontier) to the GitHub repository for this project.

<hr>

## Features

### Home Page

- The **home page** is the primary entry point to the Fund Frontier website.
- It prominently features the navigation bar, the NPV calculator interface, and a brief introduction to the tool, allowing users to start evaluating their projects immediately.
- The layout is designed to be intuitive and user-friendly, providing immediate access to the tool's functionalities and essential information.

![Home Page](https://i.imgur.com/PXUyavJ.png)



### Navigation

- The **navigation bar** is a consistent element across all pages of the Fund Frontier site.
- It is designed to be responsive and provides users with easy access to all major sections of the site including the NPV calculator, project comparison, and user account management.
- The navigation bar updates dynamically to reflect the user's authentication status:
  - Authenticated users can access their saved projects, manage their portfolios, and log out.
  - Unauthenticated visitors are presented with options to log in or register.
- On smaller screens, the navigation options are compacted into a hamburger menu to ensure the site remains navigable and user-friendly on any device.


### Project Evaluation Features

1. **Project Comparison**: Evaluate 2 or 3 projects simultaneously, allowing for comprehensive comparison and analysis.
2. **Initial Investment Input**: Users input the initial investment amount, marking the commencement of the project's financial timeline.
3. **Annual Net Cash Flow Calculation**: The tool calculates and presents the annual net cash flow, providing critical insights into the project's profitability over time.
4. **Discount Rate Specification**: Users can set the discount rate, incorporating the time value of money into the project's financial analysis.
5. **NPV and Payback Period**: The system calculates the NPV of cash flows and determines the Payback period, offering a clear financial perspective on each project.
6. **Project Ranking**: Based on NPV values, projects are ranked and flagged accordingly, empowering users with data-driven insights for decision-making.

### Create Evaluation

- **Purpose**: Begin a new project analysis by entering the financial details necessary to evaluate the investment.
- **How to use**:
  - Access the "Create Evaluation" section through the main navigation.
  - Fill in the required fields, such as the name of the evaluation, discount rate, and initial investment.
  - Submit the form to proceed to the "Add Project" phase, where you can input specific project details.

![Create Evaluation](https://i.imgur.com/L13ZXZm.png)
<br>

### Add Project

- **Purpose**: Add individual projects to your evaluation, detailing year-by-year cash flows and other relevant financial data.
- **How to use**:
  - Once an evaluation is created, select the option to "Add Project" within the evaluation.
  - Input the cash flow details for each year and any notes for reference.
  - Use the "Add Another Year" button to input additional years of cash flows.
  - If needed, remove the last entry by clicking the "Delete Last Year" button.
  - Save the project by clicking "Add Next Project" or complete your evaluation with the "Complete Evaluation" button.

![Add Project](https://i.imgur.com/9mud3GF.png)

<br>

### Project Evaluation Features

1. **Project Comparison**: Evaluate 2 or 3 projects simultaneously, allowing for comprehensive comparison and analysis.
2. **Initial Investment Input**: Users input the initial investment amount, marking the commencement of the project's financial timeline.
3. **Annual Net Cash Flow Calculation**: The tool calculates and presents the annual net cash flow, providing critical insights into the project's profitability over time.
4. **Discount Rate Specification**: Users can set the discount rate, incorporating the time value of money into the project's financial analysis.
5. **NPV and Payback Period**: The system calculates the NPV of cash flows and determines the Payback period, offering a clear financial perspective on each project.
6. **Project Ranking**: Based on NPV values, projects are ranked and flagged accordingly, empowering users with data-driven insights for decision-making.
![Evaluation List](https://i.imgur.com/ypLWyk2.png)

<br>

### Register (Sign up) / Login

- Fund Frontier offers a robust user account system.
- Visitors can register for an account to save their project evaluations, manage portfolios, and personalize their experience.
- The registration process requires a unique username and a password, with the password needing confirmation to minimize entry errors.
- Upon successful registration, users are redirected to the login page, allowing them to immediately authenticate and start using their new account.

![Registration Form](https://i.imgur.com/hnCZYo8.png)
![Login Form](https://i.imgur.com/EuIHfbP.png)

<hr>

## User Interaction
1. Evaluate Projects: Users can input details for more than 2 projects, allowing for comprehensive evaluation.
2. View and Save: Project details and evaluation results can be saved for later reference.
3. Modify Values: Users can easily update project parameters as needed for dynamic evaluation.
4. Delete Projects Unwanted projects can be deleted, providing a clean and organized interface.

<hr>

## Value to the user
- This tool helps users decide which projects are the most financially promising. By inputting project details, users can compare their profitability using metrics like net present value and Payback period. The tool also lets users save, view, modify, and delete projects, making it easy to manage and optimize their investment choices. It simplifies decision-making by providing clear insights into the financial performance of different projects.

<hr>

## Technologies Used
- Django
- Python
- HTML
- CSS

<hr>

## Credits and Acknowledgments

#### Contributors:
- [Sean](https://github.com/sean-meade) & [Nate](https://github.com/Redsskull): Took care of the backend models, views, and forms. Addressed and resolved arising issues, ensuring the product's functionality. Also assisted in debugging challenging frontend issues.
- [Bogdan](https://github.com/qburn93): Scrum Master, set up all authentication processes. Collaborated with Nate to delegate tasks during high-stress periods.
- [Johnny](https://github.com/JohnnySonTrinh): Overhauled the original navbar, assisted in styling, and resolved last-minute frontend issues.
- [Marko](https://github.com/markohautala): Designed the styling for all authentication pages (signin, register, signout) and contributed to the documentation content.
- [Andreas](https://github.com/Jelenko76): Focused on documenting the project in the README.

Special Acknowledgments:
- **Sean** and **Nate** for their extensive work on the backend and their invaluable help with the frontend.
- **Bogdan**, the Scrum Master, for efficiently managing the team and the authentication setup.
- **Johnny**, for his significant contributions to the frontend's appearance and functionality.
- **Marko**, for his aesthetic input on the authentication pages and documentation.
- **Andreas**, for his meticulous work on the project's documentation.

![Team](https://i.imgur.com/PbckpH5.png)

## Testing

#### Validator Testing 
- HTML
  - No errors were returned when passing through the official \[W3C validator\](https://validator.w3.org/)

- CSS
  - No errors were found when passing through the official \[Jigsaw validator\](https://jigsaw.w3.org/css-validator/)

- Python
  - No errors were found when passing through the \[CI Python Linter\](https://pep8ci.herokuapp.com/)

#### Lighthouse testing and result

Here is the result from the lighthouse testing:

- Performance: 85%

- Accessibility: 94%

- Best Practices: 85%

- SEO: 92%

#### Browsers and testing

The website has undergone thorough testing and functions seamlessly on different web browsers without encountering any compatibility issues. This guarantees a consistently smooth and reliable user experience for all visitors, regardless of the browser they use.

#### Responsive design

We obtained the image displayed at the top of the README from this website to showcase the responsiveness of our website. It dynamically adjusts its content to suit different screen sizes, including smartphones, tablets, and desktop viewports.

Our commitment to responsive design involves continuous testing and thorough inspection using developer tools. Additionally, the implementation of media queries ensures that the website maintains its responsiveness across various devices, providing an optimal user experience.

<hr>

## Deployment procedure

This site is deployed using GitHub pages.
To deploy the page using GitHub pages:
- Login or signup to GitHub.
- Go to the repository for this project: \[link\](https://github.com/sean-meade/fund-frontier).
- Click the settings button.
- Select pages in the left hand navigation menu.
- From the source dropdown, select main branch and click save.
- The site has now been deployed - it might take a few minutes for it to load successfully.

- To clone the repository, use the following command in your terminal: "git clone https://github.com/sean-meade/fund-frontier"

- To fork the repository, click the "Fork" button on the GitHub repository page. This creates a copy of the project under your GitHub account, allowing you to make changes without affecting the original project.

With these steps, you can not only deploy the site but also have the flexibility to extend and enhance it if you want.

<hr>