#!/bin/bash
# Build the Docker image for the FastAPI application


docker run -p 8005:8000 -v /Users/pengliu/Code/fastPipeline/source:/app/source -v /Users/pengliu/Code/fastPipeline/logs:/app/logs --name my_fast_pipeline_server fast_pipeline_server
