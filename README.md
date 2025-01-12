# Rewards Portal

The Rewards Portal is a user-friendly Q&A platform, inspired by the concept of StackOverflow, where users can ask questions, view answers, and manage their profiles. It provides a seamless experience for managing personal information, posting queries, and rewarding user engagement. This project is built using Python, Flask, Bootstrap, and JSON.

---

## Features

### User Authentication
- Secure signup and login system.
- Session-based access management.

### Query Management
- Post questions and view answers.
- Search for specific queries through an intuitive search feature.
- Query-specific details displayed in a user-friendly format.

### Personalized Dashboard
- Update and manage personal details.
- Track user queries and activity.

### Rewards System
- Reward users for their active contributions on the platform.

---

## Project Structure

```plaintext
RewardsPortal/
│
├── templates/
│   ├── SearchResults.html       # Displays query search results.
│   ├── dashboard.html           # User dashboard.
│   ├── homepage.html            # Application homepage.
│   ├── index.html               # Landing page.
│   ├── login.html               # Login form.
│   ├── main.html                # Main page structure.
│   ├── personal_details.html    # User personal details page.
│   ├── query_details.html       # Query-specific page.
│   └── signup.html              # Signup form.
│
├── app.py                       # Main Flask application logic.
├── call_json_server.py          # Script for handling JSON data server.
├── rewards_portal_db.json       # Database file for storing user and query data.
├── pyvenv.cfg                   # Python virtual environment configuration.
├── README.md                    # Project documentation.
├── project.zip                  # Compressed project files.
└── bin/                         # Executable binaries (if any).
```
## Tech Stack
- Backend: Python (Flask Framework)
- Frontend: HTML5, CSS3, Bootstrap
- Database: JSON (Lightweight data storage)
- Environment: Python Virtual Environment

## Installation and Setup
### Prerequisites

- Python 3.6+ installed
- Flask installed (via pip)

### Steps
#### Clone the Repository
```plaintext
git clone <repository-url>
cd RewardsPortal
```
### Set Up a Virtual Environment
```plaintext
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### Install Dependencies
```plaintext
pip install -r requirements.txt
```
### Run the Application
```plaintext
python app.py
```
The application will run on http://127.0.0.1:5000.

## Usage
### Homepage
- Start at the homepage to sign up or log in.
### Dashboard
- Access your personal dashboard to manage your account and track queries.
### Query System
- Post a new query.
- Search for existing queries or view query details.
### Personal Details
- Update your account information via the personal details page.
### Future Enhancements
- Database Integration
- Transition from JSON to a database solution (e.g., MySQL, PostgreSQL).
- Improved Authentication
- Add multi-factor authentication or OAuth integration.
- Enhanced Reward System
- Introduce badges, rankings, and leaderboards for user engagement.
- Mobile Compatibility
- Optimize the portal for mobile responsiveness.

## Contribution
We welcome contributions to improve this project! Follow these steps:

#### Fork the repository.
#### Create a new branch:
```plaintext
git checkout -b feature-name
```
#### Commit your changes:
```plaintext
git commit -m "Add feature-name"
```
#### Push the branch:
```plaintext
git push origin feature-name
```
#### Submit a pull request for review.

## Acknowledgements
- Thanks to the open-source community for inspiration and resources.
- Inspired by platforms like StackOverflow for the Q&A design.



