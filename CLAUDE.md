# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
ArchPortal is an internal web-based management system for small-to-medium architecture firms, focusing on project tracking, architect allocation, and billing operations.

## Tech Stack
- **Backend**: FastAPI (Asynchronous Python 3.11+)
- **Database & Auth**: Supabase (PostgreSQL + GoTrue Auth)
- **Frontend**: Jinja2 Templates + Tailwind CSS + Flowbite + Chart.js (via CDN)
- **Environment**: `python-decouple` or `pydantic-settings` for `.env` management
- **Deployment**: Dockerized, targetting Railway/Fly.io

## Common Development Commands
### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn supabase jinja2 python-multipart pydantic-settings
```

### Running the Application
```bash
uvicorn app.main:app --reload
```

## High-Level Architecture
The project follows a modular FastAPI structure:
- `app/api/`: Route handlers for each module (accounts, projects, employees, billing).
- `app/core/`: Global configuration, RBAC security logic, and Supabase client.
- `app/models/`: Pydantic schemas for request/response validation.
- `app/services/`: Business logic wrappers around the Supabase client.
- `app/static/`: CSS, JS, and images.
- `app/templates/`: Jinja2 HTML templates.

### Core Modules
- `accounts`: User profiles, authentication via Supabase, and role-based access (Admin, Architect, Accountant).
- `projects`: Project lifecycle management from Schematic Design (SD) to Project Closeout.
- `employees`: Team directory, skill tracking, and project assignments.
- `billing`: Invoice generation, payment status, and overdue tracking.
