# Flask Guestbook Application

A simple, modern guestbook application built with Flask and SQLite, featuring a clean UI using Tailwind CSS. Users can post messages that are stored persistently and displayed in reverse chronological order.

## Features

- Clean, modern UI using Tailwind CSS
- Persistent storage using SQLite
- Responsive design that works on all devices
- Real-time message posting and display
- Chronological message ordering
- Local development environment support

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.11 or higher
- Google Cloud SDK (for deploying to Google App Engine)
- pip (Python package installer)

## Project Structure

```
guestbook/
├── main.py              # Main application file
├── app.yaml             # App Engine configuration
├── requirements.txt     # Python dependencies
├── schema.sql          # Database schema
├── guestbook.db        # SQLite database (created automatically)
└── templates/          # Jinja2 templates
    ├── base.html       # Base template
    └── index.html      # Main page template
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/guestbook.git
cd guestbook
```

2. Create and activate a virtual environment:
```bash
# On macOS and Linux:
python -m venv env
source env/bin/activate

# On Windows:
python -m venv env
.\env\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Verify the contents of `requirements.txt`:
```
Flask==2.0.1
Werkzeug==2.0.1
Jinja2==3.0.1
MarkupSafe==2.0.1
gunicorn==20.1.0
```

2. Ensure `app.yaml` is configured:
```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT main:app

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto

env_variables:
  GOOGLE_CLOUD_PROJECT: "your-project-id"
```

## Running Locally

1. Initialize the database (done automatically on first run):
```bash
python main.py
```

2. Start the development server:
```bash
dev_appserver.py app.yaml
```

3. Visit http://localhost:8080 in your web browser

Alternative method (without App Engine):
```bash
python main.py
```
This will start the Flask development server directly.

## Development

### Database Schema

The application uses a simple SQLite database with the following schema:

```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);
```

### Making Changes

1. Templates are in the `templates/` directory:
   - `base.html`: Contains the base layout
   - `index.html`: Contains the guestbook form and message display

2. Static files (if any) should be placed in the `static/` directory

3. Database operations are handled in `main.py`

## Acknowledgments

- Flask framework
- Tailwind CSS for styling
- Google App Engine for deployment capabilities
