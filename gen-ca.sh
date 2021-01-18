openssl req -newkey rsa:4096 -x509 -keyout ./squid/squid.pem -out ./squid/squid.pem -days 365 -nodes
openssl x509 -in ./squid/squid.pem -outform DER -out ./squid/squid.der

