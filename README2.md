Repository Structure

The helm-core-framework repository on GitHub has the following structure:

<pre> ```
.
├── Chart.yaml
├── README.md
├── templates
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress
│   │   ├── ingress-backend-config.yaml
│   │   ├── ingress-frontend-config.yaml
│   │   ├── ingress-iap-secret.yaml
│   │   ├── ingress-managed-cert.yaml
│   │   └── ingress.yaml
│   ├── network-policies
│   │   ├── allow-egress-google-metadata.yaml
│   │   ├── allow-egress-googleapis.yaml
│   │   ├── allow-limited-access.yaml
│   │   └── postgres-cloud-sql.yaml
|   ├── otel-collector.yaml
│   ├── secrets
│   │   ├── secrets.yaml
│   │   ├── store.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   └── tests
│       └── test-connection.yaml
├── values.schema.json
└── values.yaml
``` </pre>

# TEST COMMENT