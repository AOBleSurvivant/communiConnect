// Test de l'API depuis le frontend
const API_BASE_URL = 'http://localhost:8000/api';

// Fonction pour récupérer le token
async function getToken() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.error('❌ Aucun token trouvé');
        return null;
    }
    return token;
}

// Fonction pour tester l'API posts
async function testPostsAPI() {
    console.log('🔍 TEST API POSTS');
    console.log('=' * 60);
    
    const token = await getToken();
    if (!token) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/posts/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ API Posts accessible');
            console.log('📊 Données reçues:', data);
            
            if (data.results && Array.isArray(data.results)) {
                console.log(`📝 Nombre de posts: ${data.results.length}`);
                
                data.results.slice(0, 3).forEach((post, index) => {
                    console.log(`\n${index + 1}. Post ID: ${post.id}`);
                    console.log(`   Auteur: ${post.author?.username || 'Inconnu'}`);
                    console.log(`   Contenu: ${post.content?.substring(0, 50)}...`);
                    console.log(`   Médias: ${post.media_files?.length || 0}`);
                    console.log(`   Date: ${post.created_at}`);
                });
            } else {
                console.log('⚠️ Structure de données inattendue:', data);
            }
        } else {
            console.error(`❌ Erreur API: ${response.status}`);
            const errorText = await response.text();
            console.error('Réponse:', errorText);
        }
    } catch (error) {
        console.error('❌ Exception:', error);
    }
}

// Fonction pour tester la création d'un post
async function testCreatePost() {
    console.log('\n📝 TEST CRÉATION POST');
    console.log('=' * 60);
    
    const token = await getToken();
    if (!token) return;
    
    const postData = {
        content: "Test de post depuis le frontend - Vérification ! 🔍",
        post_type: "info",
        is_anonymous: false
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/posts/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Post créé avec succès');
            console.log('📊 Données du post:', data);
            return data.id;
        } else {
            console.error(`❌ Erreur création post: ${response.status}`);
            const errorText = await response.text();
            console.error('Réponse:', errorText);
        }
    } catch (error) {
        console.error('❌ Exception:', error);
    }
}

// Fonction pour tester l'authentification
async function testAuth() {
    console.log('🔐 TEST AUTHENTIFICATION');
    console.log('=' * 60);
    
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    console.log('Token présent:', !!token);
    console.log('Utilisateur présent:', !!user);
    
    if (user) {
        try {
            const userData = JSON.parse(user);
            console.log('Utilisateur:', userData);
        } catch (e) {
            console.log('Erreur parsing utilisateur');
        }
    }
}

// Fonction pour tester les headers
async function testHeaders() {
    console.log('\n📋 TEST HEADERS');
    console.log('=' * 60);
    
    const token = await getToken();
    if (!token) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/posts/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Headers de la requête:');
        console.log('Authorization:', `Bearer ${token.substring(0, 20)}...`);
        console.log('Content-Type:', 'application/json');
        
        console.log('\nHeaders de la réponse:');
        response.headers.forEach((value, key) => {
            console.log(`${key}: ${value}`);
        });
        
    } catch (error) {
        console.error('❌ Exception:', error);
    }
}

// Fonction principale
async function main() {
    console.log('🔍 TEST COMPLET FRONTEND API');
    console.log('=' * 60);
    
    // Test authentification
    await testAuth();
    
    // Test headers
    await testHeaders();
    
    // Test API posts
    await testPostsAPI();
    
    // Test création post
    const postId = await testCreatePost();
    
    // Vérifier à nouveau les posts
    if (postId) {
        console.log('\n🔄 VÉRIFICATION FINALE');
        console.log('=' * 60);
        await testPostsAPI();
    }
    
    console.log('\n📊 RÉSUMÉ:');
    console.log('=' * 60);
    console.log('✅ Tests terminés');
    console.log('💡 Vérifiez la console pour les détails');
}

// Exécuter les tests
main().catch(console.error);

// Exporter les fonctions pour utilisation dans la console
window.testPostsAPI = testPostsAPI;
window.testCreatePost = testCreatePost;
window.testAuth = testAuth;
window.testHeaders = testHeaders; 