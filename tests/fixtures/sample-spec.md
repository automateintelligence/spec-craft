# Spec: URL Shortener

Build a service that maps a long URL to a short code and redirects.

- `POST /shorten {url}` returns a short code.
- `GET /<code>` redirects (HTTP 302) to the original URL.
- Codes are 7 characters, alphanumeric.
- Unknown codes return 404.
