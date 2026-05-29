# Claim Pilot Frontend

Next.js (React) frontend for the Claim Pilot insurance coverage analysis platform.

## Architecture

![Claim Pilot platform architecture](docs/arch.png)

This app corresponds to the **Users & Frontend** layer (web UI). In local development it calls the FastAPI backend on port 9010; in AWS the diagram shows S3/CloudFront for static hosting and traffic flowing to the application tier.

## Pages

- `/` — Landing page
- `/coverage-check` — Coverage check form with results display

## Local Development

```bash
npm install
npm run dev     # Frontend on port 4000
npm run lint    # Run ESLint
npm run build   # Production build
```

Requires `claim-pilot-backend` running on port 9010.

## Configuration

Copy `.env.example` to `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:9010
```

## Docker

```bash
docker build -t claim-pilot-frontend .
docker run -p 4000:4000 -e PORT=4000 claim-pilot-frontend
```

## Stack

- Next.js 15 with App Router
- TypeScript
- Tailwind CSS

## Maintainer

**Martins Ajibade**

This repository is maintained for the **Claim Pilot** platform (Blue Lambda University).

- **Email:** [martinsajibade3@gmail.com]

For professional inquiries, security-sensitive reports, or questions about this component, please reach out via the address above.
