#!/bin/bash

# Generate self-signed SSL certificates for local development
# ==========================================================

set -e

SSL_DIR="./nginx/ssl"
DOMAIN="industrace.local"

echo "🔐 Generating self-signed SSL certificates for $DOMAIN..."

# Create SSL directory if it doesn't exist
mkdir -p "$SSL_DIR"

# Generate private key
echo "📝 Generating private key..."
openssl genrsa -out "$SSL_DIR/key.pem" 2048

# Generate certificate signing request
echo "📝 Generating certificate signing request..."
openssl req -new -key "$SSL_DIR/key.pem" -out "$SSL_DIR/cert.csr" -subj "/C=IT/ST=Italy/L=Milan/O=Industrace/OU=IT/CN=$DOMAIN"

# Generate self-signed certificate with proper key usage
echo "📝 Generating self-signed certificate..."
openssl x509 -req -days 365 -in "$SSL_DIR/cert.csr" -signkey "$SSL_DIR/key.pem" -out "$SSL_DIR/cert.pem" -extensions v3_req -extfile <(
cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = IT
ST = Italy
L = Milan
O = Industrace
OU = IT
CN = $DOMAIN

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = localhost
DNS.3 = *.industrace.local
IP.1 = 127.0.0.1
IP.2 = ::1
EOF
)

# Clean up CSR file
rm "$SSL_DIR/cert.csr"

# Set proper permissions
chmod 600 "$SSL_DIR/key.pem"
chmod 644 "$SSL_DIR/cert.pem"

echo "✅ SSL certificates generated successfully!"
echo "📁 Certificate: $SSL_DIR/cert.pem"
echo "🔑 Private key: $SSL_DIR/key.pem"
echo ""
echo "⚠️  IMPORTANT: These are self-signed certificates for local development only."
echo "   Your browser will show a security warning - this is normal."
echo "   Click 'Advanced' and 'Proceed to $DOMAIN (unsafe)' to continue."
echo ""
echo "🌐 Add to your /etc/hosts file:"
echo "   127.0.0.1 $DOMAIN"
echo ""
echo "🚀 You can now start the production environment with: make prod"
