# TODO: Replace render.yaml with Docker Setup

- [ ] Create docker-compose.yml with web (Django app) and db (PostgreSQL) services
- [ ] Create .env file with environment variables (SECRET_KEY, DEBUG, etc.)
- [ ] Modify Dockerfile to remove collectstatic command (move to entrypoint or docker-compose)
- [ ] Ensure migrations run in the container (add entrypoint script if needed)
- [ ] Test the Docker setup locally with docker-compose up --build
- [ ] Remove render.yaml file
- [ ] Update documentation or notes on deployment
