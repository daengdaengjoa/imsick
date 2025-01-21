

# 🩺 Project: imsick
#### Health Management Platform with AI-based Diagnosis and Recommendations
http://43.201.49.32/
<br>

## 🚀 Project Introduction
imsick is a health management platform that leverages AI for diagnosis and health recommendations. It provides users with AI-based diagnostics based on symptoms and offers a range of health-related information to help manage their well-being.

<br>

## ⏱️ Development Timeline
- 2024.09 - 2024.11
  - **Project Planning and Ideation**: Define the overall direction of the project tailored to user needs, outlining required features and documenting them.
  - **Frontend and Backend Development**: Develop frontend and backend modules tailored to user interactions and set up a demo environment to integrate project modules.


<br>

## 🧑‍🤝‍🧑 Development Team: Team-8 
- **김도연** : 간단한 프론트엔드 및 현재위치 기반 병원안내
- **김환호** : 간단한 프론트엔드 및 현재위치 기반 병원안내
- **김준수** : 백엔드 - Accounts(회원가입, 로그인, 탈퇴, 수정)
- Articles(전체CRUD, Openai-API, Deepl api ,프롬프팅)
- 프론트엔드 - 전체 페이지
- 배포
- **홍순호** : 백엔드- Articles(게시물, 댓글, 좋아요CRUD)


# ImSick Project Description

<br>

## 💻 Development Environment
- **Programming Language**: Python 3.x
- **Web Framework**: Django
- **Template Engine**: Django Template Language (DTL)
- **Database**: SQLite (for development and testing), PostgreSQL (for deployment)
- **IDE**: Visual Studio Code, PyCharm
- **Version Control**: Git, GitHub

<br>

## ⚙️ Technology Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django
- **Database ORM**: Django ORM
- **Idea Brainstorming Tools and Environments**: Slack, Zep, Notion, Figma

<br>

## 📝 Project Architecture
![image](https://github.com/daengdaengjoa/12-final/assets/156053546/f53e307e-3a3c-45fb-8bdd-91105e146cb3)
![image](https://github.com/daengdaengjoa/12-final/assets/156053546/52652a3a-813c-43d9-a90d-2646a4e8cb95)
![image](https://github.com/daengdaengjoa/12-final/assets/156053546/fa7d39e2-e8b3-4826-b775-c39a190d166d)


- **Demo Video**: [Watch the Demo](https://www.youtube.com/watch?v=mLu8_DXl94U&t=6s)

<br>

## 📌 Key Features

### 1. Post CRUD
- Users can create new posts and view all posts.
- Posts can be edited or deleted on the post detail view page.

### 2. Comment CRUD
- All comments on the post are displayed at the bottom of the post detail view page.
- Users can create, view, edit, and delete comments on the post detail page.

### 3. AI Diagnosis and Recommendations
- Users can directly get AI-based diagnoses and hospital recommendations based on their symptoms.
- AI-generated diagnoses and recommendations are displayed within the page.
- **Cost Efficiency**: By integrating DeepL for certain translations, we've reduced OpenAI token usage costs by more than 30%, making our AI services more sustainable and cost-effective.
- ![image](https://github.com/daengdaengjoa/12-final/assets/156053546/3c967626-721f-4e1d-a37f-f56589ff2a1a)
- ![image](https://github.com/daengdaengjoa/12-final/assets/156053546/2ff57dd9-edbc-496d-be0e-7a8005276ee4)


### 4. Sign Up, Log In
- Membership registration is mandatory for first-time users, enabling them to log in and access the site's features.
- Only logged-in users can create posts, while both logged-in and anonymous users can view posts and comments.

### 5. Search Functionality
- Users can search for posts by symptoms, post titles, authors, and content using the post search box.
- Clicking on search results directs users to the detailed page of the respective post.

### 6. Map Service Integration
- Users can search for nearby hospitals based on their current location and view them on the map.
- Hospital information is retrieved from an external API.

### 7. Like Feature
- Users can like posts on the post details view page.
- The 'Like' button toggles to 'Dislike' upon clicking and can be undone, allowing users to like a post only once.

### 8. Administrator Permissions
- Administrators with the ID "admin_imsick" have the authority to edit or delete posts and comments, regardless of the author.

<br>

## ✒️ API Endpoints

| Endpoint                     | Method | Request Body Data                   | Response Code                                     |
|------------------------------|--------|-------------------------------------|--------------------------------------------------|
| /api/signup                  | POST   | username, password, email           | 200 OK, 400 Bad Request, 409 Conflict            |
| /api/login                   | POST   | username, password                  | 200 OK, 400 Bad Request, 401 Unauthorized        |
| /api/logout                  | GET    | -                                   | 200 OK                                           |
| /api/posts/                  | POST   | title, content, is_published        | 201 Created, 400 Bad Request, 401 Unauthorized   |
| /api/posts/<post_id>/        | GET    | -                                   | 200 OK, 404 Not Found                            |
| /api/posts/<post_id>/        | PUT    | title, content, is_published        | 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found |
| /api/posts/<post_id>/        | DELETE | -                                   | 200 OK, 401 Unauthorized, 404 Not Found          |
| /api/comments/<post_id>/     | POST   | content                             | 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found |
| /api/comments/<comment_id>/  | PUT    | content                             | 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found |
| /api/comments/<comment_id>/  | DELETE | -                                   | 200 OK, 401 Unauthorized, 404 Not Found          |
| /api/diagnosis/              | POST   | symptoms, history                   | 200 OK, 400 Bad Request                          |
| /api/recommend-hospitals     | POST   | location                            | 200 OK, 400 Bad Request                          |

<br>

## 💡 Project Structure
```text
imsick/
├── api/
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── models.py
├── templates/
│   ├── base.html
│   ├── post_list.html
│   ├── post_detail.html
│   ├── profile.html
│   ├── ...
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
├── manage.py
├── requirements.txt
├── README.md

