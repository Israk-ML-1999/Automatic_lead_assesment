# AI Sales Campaign CRM - MVP (Groq)

This project is a Minimum Viable Product (MVP) for an AI-powered Sales Campaign CRM, leveraging the Groq platform for lead enrichment and automation. It automates the process of generating personalized sales emails, sending them, and tracking lead responses.

## Features

-   **Lead Enrichment:** Uses the Groq LLM to enrich lead data with personalized personas, priority scores, email subjects, and email bodies.
-   **Email Automation:** Sends personalized emails to leads using SMTP (supports MailHog, Gmail, Outlook).
-   **Response Tracking:**  Classifies lead responses (currently a stub).
-   **Reporting:** Generates Markdown and PDF reports summarizing campaign performance.
-   **Dockerized:**  Easy to deploy and run using Docker and Docker Compose.

## Architecture

The application consists of the following main components:

-   **`app/main.py`**: FastAPI application with endpoints for running the pipeline and accessing reports.
-   **`app/pipeline.py`**: Orchestrates the end-to-end flow of the sales campaign, including reading leads, enriching them, sending emails, and generating reports.
-   **`app/agents/`**: Contains agents responsible for specific tasks:
    -   **`enrichment.py`**: Enriches lead data using the Groq LLM.
    -   **`email_writer.py`**: Finalizes email drafts (stub).
    -   **`reporting.py`**: Generates campaign summary reports in Markdown and PDF formats.
    -   **`response_classifier.py`**: Predicts the category of lead responses (stub).
    -   **`scoring.py`**: Rescores leads (stub).
-   **`app/services/`**: Provides reusable services:
    -   **`csv_io.py`**: Reads and writes lead data to CSV files.
    -   **`emailer.py`**: Sends emails using SMTP.
    -   **`llm.py`**:  Interfaces with the Groq LLM.
-   **`data/`**: Contains lead data (CSV).
-   **`reports/`**: Stores generated reports (Markdown and PDF).

## Getting Started

### Prerequisites

-   Docker
-   Docker Compose
-   Groq API Key (set in `.env`)

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd crm-mvp
    ```

2.  Configure environment variables:

    Create a `.env` file in the root directory and set the following variables:

    ```
    GROQ_API_KEY=your_groq_api_key
    GROQ_MODEL=llama-3.3-70b-versatile
    SMTP_HOST=mailhog
    SMTP_PORT=1025
    SMTP_USER=
    SMTP_PASSWORD=
    SMTP_FROM="Sales Team <sales@example.com>"
    SMTP_USE_TLS=false
    LEADS_CSV=data/leads.csv
    CAMPAIGN_NAME=September Launch
    COMPANY_NAME=Acme Corp
    PRODUCT_PITCH="A lightweight automation platform that saves teams 6-10 hrs/week."
    BATCH_SIZE=10
    MAX_CONCURRENT_BATCHES=5
    ```

    **Note:**
    -   For MailHog, leave `SMTP_USER` and `SMTP_PASSWORD` blank.
    -   For Gmail/Outlook, configure `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, and `SMTP_USE_TLS` accordingly.

3.  Run with Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This will build and start the `api`, `worker`, and `mailhog` services.

### Usage

1.  **Access the API:**

    The API is accessible at `http://localhost:8000`.

2.  **Run the pipeline:**

    Send a POST request to the `/run` endpoint to start the sales campaign pipeline.  You can specify the lead CSV file, batch size, and maximum concurrent batches as query parameters:

    ```bash
    curl -X POST "http://localhost:8000/run?file=data/leads.csv&batch_size=10&max_concurrent_batches=5"
    ```

3.  **View the latest report:**

    Access the latest generated report in Markdown format at:

    ```
    http://localhost:8000/report/latest
    ```

4.  **MailHog Web UI:**

    Access the MailHog web UI at `http://localhost:8025` to view sent emails.

## Development

### Running Locally (without Docker)

1.  Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2.  Set environment variables (as described in the Installation section).

3.  Run the pipeline directly:

    ```bash
    python -m app.pipeline --file data/leads.csv --batch-size 10 --max-concurrent-batches 5
    ```

4.  Run the FastAPI application:

    ```bash
    uvicorn app.main:app --reload
    ```

### Key Files

-   **`app/pipeline.py`**: Main application logic.
-   **`app/agents/enrichment.py`**: Lead enrichment using Groq.
-   **`app/services/llm.py`**: Groq API client.
-   **`data/leads.csv`**: Sample lead data.
-   **`reports/`**: Output reports.

## Scalability

-   The pipeline uses concurrent futures to process lead batches in parallel, improving throughput.
-   The `MAX_CONCURRENT_BATCHES` environment variable controls the level of parallelism.

# For output check Image Folder

Swager UI 

## License

![My Project Workflow](https://github.com/Israk-ML-1999/Automatic_lead_assesment/blob/main/image.png?raw=true)
