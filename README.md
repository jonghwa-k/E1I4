## Tress
Tress is an API server that provides the latest hair news with a project created by Team 2 of Sparta

---

## Introduction
TRESS is a hair news website where you can catch the latest trends at a glance.

The word "Tress" means a lock of hair or braided hair, often used to describe hair in a more elegant and delicate way.

On the Tress website, you can find a trendy hair news board and a free board where members can interact. Members can write posts, and engage with each other through comments and likes on the posts.

---

## Development Period
- Start Date: 2024.08.20
- End Date: 2024.08.28

---
## Team Roles and Responsibilities
| Team Member      | Responsibilities                                                                                           |
|:-----------------|:----------------------------------------------------------------------------------------------------------|
| 이종화(Leader) | - Initial Setup<br>- Profile Features ( edit profile, view my posts/comments, view posts/comments I liked)                |
| 김상아           | - Wireframe Design<br>- Posting Features (like posts, like comments, write comments, edit comments, delete comments) |
| 김석환          | - ERD Design<br>- Member Features (sign up, login, logout, view profile, change password, deactivate account)<br>- Posting Features (create posts, view post list) |
| 유정원           | - Member Features (sign up, login, logout, view profile, edit profile, change password, deactivate account)<br>- Posting Features (categories, search, scoring system) |
| 윤율             | - API Documentation<br>- SA (System Architecture) Document<br>- Posting Features (view post details, edit posts, delete posts) |


---

## Full Technology Stack Overview
- Programming Language: python 3.10
- Web Framework: Django 4.2
- Database: SQLite
- IDE: PyCharm, Vs code
- Version Control: Git, Github
- Communication: Zep, Notion, Slack
- Technical stack
  - Backend: Python, Django
  - Frontend: 
  - Database: Django ORM, SQLite

---

## Key Features

- **User Management:**
  - Sign up, log in, log out, change password, and deactivate account.

- **Posting System:**
  - Full CRUD (Create, Read, Update, Delete) for posts.
  - View post lists, add comments, and use the like feature.
  - Categories for news and free discussion boards.
  - Search functionality.
  - A scoring system based on comments and likes.

- **Profile Features:**
  - View and edit profile.
  - View posts and comments made by the user.
  - Display posts and comments liked by the user.

---

### Folder Structure
```
📦 ProjectName
│
├── accounts/           # App handling user authentication and permissions
├── articles/           # App managing articles and related content
├── hairnews/           # Project-specific settings and configurations
├── manage.py           # Django management command file
├── requirements.txt    # List of dependencies for the project
└── .gitignore          # Files and directories to be ignored by Git
```
---
