# simple curl test of 2 endpoints assuming default port for Flask, adjust as needed
#!/bin/bash

# Envoyer des données CSV à l'API /transactions
curl -X POST -F "file=@data.csv" http://localhost:5000/transactions

# Récupérer le rapport à partir de l'API /report
curl http://localhost:5000/report