/**
 * Script de test pour diagnostiquer les problèmes de posts avec médias côté frontend
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';
const TEST_IMAGE_URL = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';

// Classe de test pour le frontend
class FrontendMediaTest {
    constructor() {
        this.testResults = {};
        this.authToken = null;
    }

    // Logger avec timestamp
    log(message, type = 'info') {
        const timestamp = new Date().toISOString();
        const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️';
        console.log(`${prefix} [${timestamp}] ${message}`);
    }

    // Test de connexion à l'API
    async testApiConnection() {
        this.log('=== Test de connexion à l\'API ===');
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/posts/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            this.log(`Status: ${response.status}`);
            this.log(`Headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}`);
            
            if (response.ok) {
                const data = await response.json();
                this.log(`Données reçues: ${JSON.stringify(data, null, 2)}`);
                return true;
            } else {
                this.log(`Erreur HTTP: ${response.status} ${response.statusText}`, 'error');
                return false;
            }
        } catch (error) {
            this.log(`Erreur de connexion: ${error.message}`, 'error');
            return false;
        }
    }

    // Test d'authentification
    async testAuthentication() {
        this.log('=== Test d\'authentification ===');
        
        try {
            const loginData = {
                username: 'testuser',
                password: 'testpass123'
            };
            
            const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData)
            });
            
            if (response.ok) {
                const data = await response.json();
                this.authToken = data.access;
                this.log('Authentification réussie');
                this.log(`Token: ${this.authToken.substring(0, 20)}...`);
                return true;
            } else {
                this.log(`Échec d'authentification: ${response.status}`, 'error');
                return false;
            }
        } catch (error) {
            this.log(`Erreur d'authentification: ${error.message}`, 'error');
            return false;
        }
    }

    // Test de création d'image de test
    createTestImage() {
        this.log('=== Création d\'image de test ===');
        
        try {
            // Créer une image à partir de base64
            const img = new Image();
            img.src = TEST_IMAGE_URL;
            
            // Créer un canvas pour convertir en blob
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = 1;
            canvas.height = 1;
            
            return new Promise((resolve, reject) => {
                img.onload = () => {
                    ctx.drawImage(img, 0, 0);
                    canvas.toBlob((blob) => {
                        const file = new File([blob], 'test_image.png', {
                            type: 'image/png',
                            lastModified: Date.now()
                        });
                        this.log(`Image de test créée: ${file.name} (${file.size} bytes)`);
                        resolve(file);
                    }, 'image/png');
                };
                img.onerror = () => reject(new Error('Impossible de charger l\'image de test'));
            });
        } catch (error) {
            this.log(`Erreur création image: ${error.message}`, 'error');
            return null;
        }
    }

    // Test d'upload de média
    async testMediaUpload() {
        this.log('=== Test d\'upload de média ===');
        
        if (!this.authToken) {
            this.log('Token d\'authentification manquant', 'error');
            return false;
        }
        
        try {
            const testFile = await this.createTestImage();
            if (!testFile) {
                return false;
            }
            
            const formData = new FormData();
            formData.append('file', testFile);
            formData.append('title', 'Test Image');
            formData.append('description', 'Image de test pour diagnostic');
            
            const response = await fetch(`${API_BASE_URL}/api/posts/media/upload/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.authToken}`,
                },
                body: formData
            });
            
            this.log(`Status upload: ${response.status}`);
            
            if (response.ok) {
                const data = await response.json();
                this.log(`Upload réussi: ${JSON.stringify(data, null, 2)}`);
                return data.id; // Retourner l'ID du média créé
            } else {
                const errorData = await response.json();
                this.log(`Erreur upload: ${JSON.stringify(errorData, null, 2)}`, 'error');
                return false;
            }
        } catch (error) {
            this.log(`Erreur upload: ${error.message}`, 'error');
            return false;
        }
    }

    // Test de création de post avec média
    async testPostCreation(mediaId) {
        this.log('=== Test de création de post avec média ===');
        
        if (!this.authToken) {
            this.log('Token d\'authentification manquant', 'error');
            return false;
        }
        
        try {
            const postData = {
                content: 'Test post avec média via frontend',
                post_type: 'info',
                is_anonymous: false,
                media_files: mediaId ? [mediaId] : []
            };
            
            const response = await fetch(`${API_BASE_URL}/api/posts/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`,
                },
                body: JSON.stringify(postData)
            });
            
            this.log(`Status création post: ${response.status}`);
            
            if (response.ok) {
                const data = await response.json();
                this.log(`Post créé avec succès: ${JSON.stringify(data, null, 2)}`);
                return true;
            } else {
                const errorData = await response.json();
                this.log(`Erreur création post: ${JSON.stringify(errorData, null, 2)}`, 'error');
                return false;
            }
        } catch (error) {
            this.log(`Erreur création post: ${error.message}`, 'error');
            return false;
        }
    }

    // Test des composants React
    testReactComponents() {
        this.log('=== Test des composants React ===');
        
        try {
            // Vérifier si React est disponible
            if (typeof React === 'undefined') {
                this.log('React n\'est pas disponible dans ce contexte', 'error');
                return false;
            }
            
            // Vérifier les dépendances
            const requiredDependencies = [
                'axios',
                'react-router-dom',
                'react-hook-form',
                'react-hot-toast',
                'lucide-react'
            ];
            
            let allDependenciesAvailable = true;
            requiredDependencies.forEach(dep => {
                try {
                    require(dep);
                    this.log(`✅ ${dep} disponible`);
                } catch (error) {
                    this.log(`❌ ${dep} manquant`, 'error');
                    allDependenciesAvailable = false;
                }
            });
            
            return allDependenciesAvailable;
        } catch (error) {
            this.log(`Erreur test composants: ${error.message}`, 'error');
            return false;
        }
    }

    // Test de validation des fichiers
    testFileValidation() {
        this.log('=== Test de validation des fichiers ===');
        
        try {
            // Créer différents types de fichiers de test
            const testFiles = [
                new File(['test'], 'test.txt', { type: 'text/plain' }),
                new File(['test'], 'test.jpg', { type: 'image/jpeg' }),
                new File(['test'], 'test.mp4', { type: 'video/mp4' })
            ];
            
            const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
            const allowedVideoTypes = ['video/mp4', 'video/webm', 'video/quicktime', 'video/avi'];
            const maxImageSize = 10 * 1024 * 1024; // 10MB
            const maxVideoSize = 50 * 1024 * 1024; // 50MB
            
            testFiles.forEach(file => {
                this.log(`Test fichier: ${file.name} (${file.type}, ${file.size} bytes)`);
                
                // Test type
                if (file.type.startsWith('image/')) {
                    if (allowedImageTypes.includes(file.type)) {
                        this.log(`✅ Type d'image valide: ${file.type}`);
                    } else {
                        this.log(`❌ Type d'image invalide: ${file.type}`, 'error');
                    }
                    
                    // Test taille
                    if (file.size <= maxImageSize) {
                        this.log(`✅ Taille d'image valide: ${file.size} bytes`);
                    } else {
                        this.log(`❌ Taille d'image trop grande: ${file.size} bytes`, 'error');
                    }
                } else if (file.type.startsWith('video/')) {
                    if (allowedVideoTypes.includes(file.type)) {
                        this.log(`✅ Type de vidéo valide: ${file.type}`);
                    } else {
                        this.log(`❌ Type de vidéo invalide: ${file.type}`, 'error');
                    }
                    
                    // Test taille
                    if (file.size <= maxVideoSize) {
                        this.log(`✅ Taille de vidéo valide: ${file.size} bytes`);
                    } else {
                        this.log(`❌ Taille de vidéo trop grande: ${file.size} bytes`, 'error');
                    }
                } else {
                    this.log(`❌ Type de fichier non supporté: ${file.type}`, 'error');
                }
            });
            
            return true;
        } catch (error) {
            this.log(`Erreur validation fichiers: ${error.message}`, 'error');
            return false;
        }
    }

    // Exécuter tous les tests
    async runAllTests() {
        this.log('🚀 Démarrage des tests frontend pour posts et médias');
        
        this.testResults = {
            apiConnection: await this.testApiConnection(),
            authentication: await this.testAuthentication(),
            reactComponents: this.testReactComponents(),
            fileValidation: this.testFileValidation(),
            mediaUpload: await this.testMediaUpload(),
            postCreation: await this.testPostCreation()
        };
        
        // Si l'upload de média a réussi, tester la création de post avec ce média
        if (this.testResults.mediaUpload) {
            this.testResults.postCreationWithMedia = await this.testPostCreation(this.testResults.mediaUpload);
        }
        
        this.log('\n📊 Résultats des tests:');
        Object.entries(this.testResults).forEach(([testName, result]) => {
            const status = result ? '✅ SUCCÈS' : '❌ ÉCHEC';
            this.log(`${testName}: ${status}`);
        });
        
        const successCount = Object.values(this.testResults).filter(Boolean).length;
        const totalCount = Object.keys(this.testResults).length;
        
        this.log(`\n🎯 Résumé: ${successCount}/${totalCount} tests réussis`);
        
        if (successCount === totalCount) {
            this.log('🎉 Tous les tests sont passés!');
        } else {
            this.log('⚠️ Certains tests ont échoué. Vérifiez les logs ci-dessus.', 'error');
        }
        
        return this.testResults;
    }
}

// Fonction d'export pour utilisation dans le navigateur
if (typeof window !== 'undefined') {
    window.FrontendMediaTest = FrontendMediaTest;
}

// Fonction d'export pour Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FrontendMediaTest;
}

// Auto-exécution si dans le navigateur
if (typeof window !== 'undefined') {
    const tester = new FrontendMediaTest();
    tester.runAllTests().then(results => {
        console.log('Tests terminés:', results);
    });
} 