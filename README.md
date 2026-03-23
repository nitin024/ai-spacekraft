# FocusFlow Agent

FocusFlow is an intelligent location discovery application designed to help users find the ideal place based on their current needs, preferences, and context. Leveraging the Google Maps API, the app processes user inputs—such as desired activity type (e.g., quiet workspace, coffee shop, park, or restaurant), proximity constraints, time of day, and personal preferences (e.g., budget, accessibility, or ambiance)—to recommend optimal locations in real-time.

## Key features include:

Personalized Recommendations: Integrates user history and AI-driven analysis to suggest spots that align with individual habits, such as finding a serene study area during work hours or a vibrant social venue for evenings.
Interactive Mapping: Displays results on an interactive Google Maps interface with directions, ratings, reviews, and real-time availability (e.g., open hours, crowd levels via external integrations).
User Input Flexibility: Supports natural language queries (e.g., "Find a quiet place to work near downtown") and filters for dietary needs, accessibility, or environmental factors.
Cross-Platform Support: Available as a web app, mobile app, or API for seamless integration into productivity tools or smart assistants.
FocusFlow aims to enhance daily productivity and well-being by eliminating decision fatigue in location-based choices, making it easier to "flow" into the right environment for focus, relaxation, or connection. The project emphasizes privacy, with all user data processed locally or securely on the cloud, and scalability for global use.

## Create Project
```sh
export PROJECT_ID=$(gcloud projects create your-project-id --name="Your Project Name" --format="value(projectId)")
```

## Activate GCP Services

```sh
gcloud services enable aiplatform.googleapis.com \
    iap.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com --project $PROJECT_ID
```

## MCP Servers

The following MCP servers need to be prepared:

### Google Maps Grounding Lite MCP Server

See offical [documentation](https://developers.google.com/maps/ai/grounding-lite).

```sh
gcloud beta services enable mapstools.googleapis.com --project=$PROJECT_ID
gcloud beta services mcp enable mapstools.googleapis.com --project=$PROJECT_ID
```

Get a Maps API Key and limit it to `mapstools.googleapis.com`.

```sh
gcloud services api-keys create \
    --display-name="FocusFlow Maps MCP" \
    --key-id="focusflow-maps-mcp" \
    --api-target="service=mapstools.googleapis.com" \
    --project $PROJECT_ID
```

Export it as a local variable for local development:

```sh
export MAPS_API_KEY="$(gcloud services api-keys get-key-string "focusflow-maps-mcp" --project $PROJECT_ID --format "value(keyString)")"
```

## Get Started

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt 
```

```sh
adk web ./agents
```

Try a prompt like (with ???):

```txt
???
```

## Deploy to Cloud Run

### Build Permissions

Ensure the default Compute Engine service account (used by Cloud Build for deployment) has permissions to access storage (for source code), write to Artifact Registry, and write logs.

```sh
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/storage.objectUser"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/logging.logWriter"
```

### Create Service Account

Create a dedicated service account for the application:

```sh
SERVICE_ACCOUNT_NAME="focusflow-sa"
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="FocusFlow Agent Service Account" \
    --project=$PROJECT_ID
```

Grant the necessary permissions (Vertex AI User for model access, Logging and Monitoring for observability):

```sh
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/monitoring.metricWriter"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.servicesInvoker"
```

### Setup Maps API Key Secret

Create a secret for the Maps API Key in Secret Manager:

```sh
gcloud secrets create maps-api-key --replication-policy="automatic" --project=$PROJECT_ID
gcloud services api-keys get-key-string "focusflow-maps-mcp" --project $PROJECT_ID --format "value(keyString)" | tr -d '\n' | gcloud secrets versions add maps-api-key --data-file=- --project=$PROJECT_ID
```

Grant the service account access to the secret:

```sh
gcloud secrets add-iam-policy-binding maps-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor" \
    --project=$PROJECT_ID
```

### Deploy Service

Follow the instructions here 

```sh
CLOUD_RUN_REGION=europe-west1
PROJECT_NUMBER="$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')"
# Optional A2A URL
A2A_FOCUSFLOW_TRIP_URL="https://focusflow-trip-${PROJECT_NUMBER}.${CLOUD_RUN_REGION}.run.app/a2a/focusflow_trip"

gcloud run deploy focusflow \
--source . \
--region $CLOUD_RUN_REGION \
--project $PROJECT_ID \
--no-allow-unauthenticated \
--service-account="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
--set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=global,GOOGLE_GENAI_USE_VERTEXAI=true,SERVE_WEB_INTERFACE=true,A2A_FOCUSFLOW_TRIP_URL=$A2A_FOCUSFLOW_TRIP_URL" \
--set-secrets="MAPS_API_KEY=maps-api-key:latest"
```

To access it for testing purposes, create a [Cloud Run IAP](https://docs.cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run) or use the [Cloud Run auth proxy](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/proxy).

```sh
gcloud run services proxy focusflow --region $CLOUD_RUN_REGION --project $PROJECT_ID
```

## IAP 

If you use IAP make sure you deploy your cloud run service with `--iap` and also add the invoker permission to iap.

```sh
gcloud run services add-iam-policy-binding focusflow \
  --region=$CLOUD_RUN_REGION \
  --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-iap.iam.gserviceaccount.com \
  --role=roles/run.invoker \
  --project=$PROJECT_ID

```

## Screenshot

![Screenshot of the running application](img/screenshot.png)

