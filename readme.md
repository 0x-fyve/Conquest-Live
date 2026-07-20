# 🏆 Conquest

> **An event-driven leaderboard platform built with Django REST Framework.**

Conquest is a backend API that enables developers to build leaderboards for competitive applications such as games, hackathons, fitness challenges, referral campaigns, and coding competitions.

Instead of storing participant scores directly, Conquest records every scoring action as an immutable event and calculates leaderboards dynamically. This provides a complete audit trail, flexible analytics, and reliable score computation.

---

## ✨ Features

* 🔐 JWT Authentication
* 📁 Multi-project management
* 🏆 Competition management
* 👥 Participant registration
* 📈 Event-based score tracking
* 📊 Dynamic leaderboard generation
* 🔑 API Key management
* 🆔 UUID-based resources
* ⚡ Idempotent score event processing
* 🗂️ Service-layer architecture

---

## 🏗️ Architecture

Conquest follows a layered architecture to separate responsibilities.

```text
                Client
                   │
                   ▼
         Django REST Views
                   │
                   ▼
            Serializers
                   │
                   ▼
        Business Services
                   │
                   ▼
        Django ORM Models
                   │
                   ▼
              Database
```

Business rules are kept inside service classes instead of views, making the application easier to maintain, test, and extend.

---

## 📦 Project Structure

```text
conquest/
│
├── accounts/          # Authentication
├── projects/          # User projects
├── competitions/      # Competitions
├── participants/      # Competition participants
├── scoreevents/       # Event-based scoring
├── api_keys/          # API key management
│
└── config/
```

---

## 🧩 Core Concepts

### 📁 Project

A project represents an application using Conquest.

Examples:

* Mobile Game
* Coding Contest
* Fitness Challenge
* Referral Campaign

Each project can contain multiple competitions.

---

### 🏆 Competition

A competition belongs to a project.

It contains:

* Participants
* Rules
* Score Events
* Leaderboard

---

### 👥 Participant

Represents a competitor inside a competition.

Each participant is uniquely identified within a competition using an external identifier.

---

### 📈 Score Events

Instead of updating a participant's score directly, every score change is stored as an event.

Example:

```text
+100  Completed Challenge
+50   Bonus Points
-20   Penalty

Current Score = 130
```

This approach provides:

* Complete score history
* Easy auditing
* Reliable analytics
* Idempotent event processing

---

### 🏅 Leaderboard

Leaderboards are generated dynamically using Django ORM aggregation.

Each participant's score is calculated by summing all related score events.

Participants are then ranked from highest to lowest score.

---

## ⚙️ Technology Stack

| Technology            | Purpose              |
| --------------------- | -------------------- |
| Python 3              | Programming Language |
| Django                | Web Framework        |
| Django REST Framework | REST API             |
| SQLite                | Development Database |
| Simple JWT            | Authentication       |

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/conquest.git
cd conquest
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Run the server

```bash
python manage.py runserver
```

---

## 🌐 API Overview

### Authentication

```http
POST   /api/register/
POST   /api/login/
POST   /api/token/refresh/
```

### Projects

```http
GET    /api/projects/
POST   /api/projects/
GET    /api/projects/{id}/
PATCH  /api/projects/{id}/
DELETE /api/projects/{id}/
```

### Competitions

```http
GET    /api/competitions/
POST   /api/competitions/
GET    /api/competitions/{id}/
PATCH  /api/competitions/{id}/
DELETE /api/competitions/{id}/
GET    /api/competitions/{id}/leaderboard/
```

### Participants

```http
GET    /api/participants/
POST   /api/participants/
PATCH  /api/participants/{id}/
DELETE /api/participants/{id}/
```

### Score Events

```http
GET    /api/scoreevents/
POST   /api/scoreevents/
```

### API Keys

```http
GET    /api/api-keys/
POST   /api/api-keys/
DELETE /api/api-keys/{id}/
```

---

## 💡 Design Decisions

### Service Layer

Business logic is isolated from views, making the codebase easier to maintain and test.

### UUIDs

All primary resources use UUIDs instead of sequential IDs to improve uniqueness and reduce predictability.

### Event Sourcing

Scores are derived from immutable score events rather than stored directly.

This makes the system more reliable, auditable, and flexible.

### Idempotent Events

Every score event has a globally unique `event_id`, preventing duplicate score submissions.

---

## 📌 Roadmap

* [ ] API Key authentication
* [ ] Swagger / OpenAPI documentation
* [ ] Automated tests
* [ ] Docker support
* [ ] PostgreSQL
* [ ] Redis caching
* [ ] WebSocket live leaderboard
* [ ] CI/CD pipeline

---

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.

Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
