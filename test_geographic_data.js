// Script de test pour diagnostiquer le problème des données géographiques
const axios = require('axios');

// Configuration
const API_BASE_URL = 'http://localhost:8000/api';
const FRONTEND_API_URL = 'https://communiconnect-backend.onrender.com/api';

async function testGeographicData() {
  console.log('🔍 Test des données géographiques...\n');

  // Test 1: API locale
  console.log('1️⃣ Test API locale (localhost:8000):');
  try {
    const localResponse = await axios.get(`${API_BASE_URL}/users/geographic-data/`);
    console.log('✅ API locale fonctionne');
    console.log(`📊 Données reçues: ${localResponse.data.regions?.length || 0} régions`);
    console.log(`📊 Premier quartier: ${localResponse.data.regions?.[0]?.prefectures?.[0]?.communes?.[0]?.quartiers?.[0]?.nom || 'Aucun'}`);
  } catch (error) {
    console.log('❌ Erreur API locale:', error.message);
  }

  console.log('\n2️⃣ Test API de production (Render):');
  try {
    const prodResponse = await axios.get(`${FRONTEND_API_URL}/users/geographic-data/`);
    console.log('✅ API de production fonctionne');
    console.log(`📊 Données reçues: ${prodResponse.data.regions?.length || 0} régions`);
  } catch (error) {
    console.log('❌ Erreur API de production:', error.message);
  }

  // Test 3: Configuration frontend
  console.log('\n3️⃣ Test configuration frontend:');
  console.log(`🔗 URL API configurée: ${process.env.REACT_APP_API_URL || 'Non définie'}`);
  console.log(`🔗 URL par défaut: ${FRONTEND_API_URL}`);

  // Test 4: Simulation du composant GeographicSelector
  console.log('\n4️⃣ Test simulation GeographicSelector:');
  try {
    const testData = await axios.get(`${API_BASE_URL}/users/geographic-data/`);
    const regions = testData.data.regions;
    
    if (regions && regions.length > 0) {
      const firstRegion = regions[0];
      const firstPrefecture = firstRegion.prefectures?.[0];
      const firstCommune = firstPrefecture?.communes?.[0];
      const firstQuartier = firstCommune?.quartiers?.[0];
      
      console.log('✅ Données disponibles:');
      console.log(`   Région: ${firstRegion.nom}`);
      console.log(`   Préfecture: ${firstPrefecture?.nom}`);
      console.log(`   Commune: ${firstCommune?.nom}`);
      console.log(`   Quartier: ${firstQuartier?.nom}`);
      
      // Test de sélection
      const selection = {
        region_id: firstRegion.id,
        prefecture_id: firstPrefecture?.id,
        commune_id: firstCommune?.id,
        quartier_id: firstQuartier?.id
      };
      
      console.log('\n📝 Sélection testée:', selection);
    } else {
      console.log('❌ Aucune donnée géographique disponible');
    }
  } catch (error) {
    console.log('❌ Erreur lors du test de sélection:', error.message);
  }

  // Test 5: Vérification des CORS
  console.log('\n5️⃣ Test CORS:');
  try {
    const corsResponse = await axios.options(`${API_BASE_URL}/users/geographic-data/`);
    console.log('✅ CORS configuré correctement');
    console.log('📋 Headers CORS:', corsResponse.headers);
  } catch (error) {
    console.log('❌ Problème CORS:', error.message);
  }

  console.log('\n🎯 Recommandations:');
  console.log('1. Vérifiez que le backend est démarré sur le port 8000');
  console.log('2. Vérifiez la configuration CORS dans Django');
  console.log('3. Vérifiez les variables d\'environnement du frontend');
  console.log('4. Testez l\'API directement dans le navigateur');
}

// Exécution du test
testGeographicData().catch(console.error); 