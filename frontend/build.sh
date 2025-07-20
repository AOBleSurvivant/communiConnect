#!/bin/bash

# Script de build pour le frontend CommuniConnect
echo "🚀 Building CommuniConnect Frontend..."

# Installer les dépendances
npm install

# Build de production
npm run build

echo "✅ Build terminé !"
echo "📁 Fichiers générés dans le dossier 'build'" 