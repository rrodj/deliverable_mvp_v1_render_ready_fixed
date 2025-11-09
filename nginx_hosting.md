# Nginx Hosting Topologies (Cloud)

Inventory Guardian ships a frontend image that already includes **Nginx** serving the SPA and proxying `/api` to the backend service.

## Recommended (ECS + ALB + TLS termination)
- **ALB** terminates HTTPS (TLS) using **ACM** certificate for `app.<your-domain>`.
- Target group forwards `HTTP :80` to the **frontend** task (container).
- Frontend Nginx proxies `/api/*` to the **backend** service's internal port (via service discovery or internal ALB).

### Sample Nginx (inside frontend image)
`deploy/nginx.conf` (already provided) proxies `/api` → `http://backend:8000/` and serves SPA with history fallback.

**Notes**
- Keep Nginx in **HTTP** when behind an ALB that handles TLS.
- If you use a single VM, terminate TLS at Nginx (see below).

## Single VM (TLS at Nginx using Let's Encrypt)
1. Install `certbot` for Nginx.
2. Server block:
   ```nginx
   server {
     listen 80;
     server_name app.example.com;
     return 301 https://$host$request_uri;
   }
   server {
     listen 443 ssl http2;
     server_name app.example.com;
     ssl_certificate     /etc/letsencrypt/live/app.example.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;

     root /usr/share/nginx/html;
     index index.html;

     location /api/ {
       proxy_pass http://127.0.0.1:8000/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
     }

     location / {
       try_files $uri $uri/ /index.html;
     }
   }
   ```

## Static hosting (optional)
- Serve the compiled SPA from a CDN (e.g., S3 + CloudFront), with the **API** on a separate hostname (`api.<domain>`).
- Adjust `VITE_API_BASE_URL` to the `https://api.<domain>` URL at build time.
