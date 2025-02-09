# CDV-Fridge-Compositor

**Fridge Compositor** is a full-stack web application that allows users to manage items in a virtual fridge. It consists of a **Flask backend API**, a **PostgreSQL database**, a **Redis queue** for asynchronous tasks, and an **Nginx web server** for serving the frontend and proxying API requests.

---

## Features

- **Add Items**: Add items to the fridge with a name and quantity.
- **Update Quantities**: Modify the quantity of existing items.
- **Delete Items**: Remove items from the fridge.
- **Real-Time Updates**: Redis ensures smooth communication between the API and database.
- **Scalable Architecture**: Docker Compose makes it easy to deploy and scale the application.

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Queueing**: Redis
- **Web Server**: Nginx
- **Containerization**: Docker Compose

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/agk-code/cdv-fridge-compositor.git
   cd fridge-composer
   ```

2. !!IMPORTANT!! - Change API_URL in frontend/index.html to represent your hostname/IP Adress
    (Have't found a better way to work around that yet :/)


3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: Open `http://localhost:80` in your browser.

---

## Docker Compose Architecture

The application is composed of the following services:

1. **Nginx**:
   - Serves the frontend static files.
   - Proxies API requests to the Flask backend.
   - Port: `80`

2. **Flask Backend**:
   - REST API for managing fridge items.
   - Connects to PostgreSQL and Redis.
   - Port: `5000`

3. **PostgreSQL**:
   - Stores fridge items and their quantities.
   - Port: `5432`

4. **Redis**:
   - Handles queueing and asynchronous tasks between the API and database.
   - Port: `6379`

---

## API Endpoints

| Method | Endpoint               | Description                     |
|--------|------------------------|---------------------------------|
| GET    | `/api/fridge`          | Get all fridge items.           |
| POST   | `/api/fridge`          | Add a new item to the fridge.   |
| PUT    | `/api/fridge/<name>`   | Update the quantity of an item. |
| DELETE | `/api/fridge/<name>`   | Delete an item from the fridge. |

---

## Environment Variables

The following environment variables are used in the `docker-compose.yml` file:

- **PostgreSQL**:
  - `POSTGRES_USER`: Database username.
  - `POSTGRES_PASSWORD`: Database password.
  - `POSTGRES_DB`: Database name.

- **Flask**:
  - `FLASK_ENV`: Environment (e.g., `development` or `production`).
  - `DATABASE_URL`: PostgreSQL connection URL.
  - `REDIS_URL`: Redis connection URL.

---

## Stopping the Application

To stop the application, run:
```bash
docker-compose down
```
---

Enjoy managing your virtual fridge! 🎉