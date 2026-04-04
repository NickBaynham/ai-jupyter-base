# AWS ECS deployment notes

This folder is a **starting point** for running the Jupyter image on Amazon ECS. Treat secrets, networking, and IAM as your own operational responsibility.

## Image build assumptions

- The root `Dockerfile` produces an image that runs **JupyterLab** on port **8888**.
- The default `docker-compose.yml` mounts the repository for local development; **production** images should bake the app (as the `Dockerfile` does before any mount) and avoid bind-mounting source code.
- Push images to **Amazon ECR** (or another registry ECS can pull from). Tag with the git SHA or semver for traceability.

## Environment variables

- **JUPYTER_LAB_TOKEN**: Set a strong random token in ECS task definitions (or use your SSO/proxy in front of Jupyter). Do **not** ship empty-token servers to the public internet.
- **JUPYTER_BASE_*** variables: See `.env.example` for application settings loaded by `jupyter_base.config.load_settings`.
- Prefer **AWS Secrets Manager** or **SSM Parameter Store** for sensitive values, referenced from the task definition.

## Suggested path to ECS

1. Create an **ECR** repository and push the image: `docker build -t your-repo/jupyter-base:latest .` then `docker push ...`.
2. Create a **Fargate** task definition (CPU/memory, port mapping **8888**, log driver to CloudWatch). See `ecs-task-definition.example.json` for a skeletal template—replace ARNs, subnets, and security groups.
3. Run as a **service** behind an **Application Load Balancer** if you need HTTPS and access control, or use **private subnets + VPN** for internal-only notebooks.
4. Attach a **persistent volume** (EFS) if notebooks or data must survive task restarts; map it to `/app/notebooks` or a dedicated data path your jobs use.

## Operational tips

- Scale to zero when idle if cost matters; notebook servers are often interactive and not always suitable for aggressive auto-scaling.
- Restrict security groups so only trusted networks reach port 8888 (or the ALB only).
- Rebuild and redeploy when `pdm.lock` changes to keep dependencies reproducible.
