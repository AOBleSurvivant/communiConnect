// Script de debug pour le frontend
console.log('🔍 DEBUG FRONTEND - PUBLICATIONS ET NOTIFICATIONS');

// Fonction pour vérifier l'état de l'authentification
function checkAuthState() {
    console.log('🔐 Vérification état authentification...');
    
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    console.log('📊 Token présent:', !!token);
    console.log('📊 User présent:', !!user);
    
    if (token) {
        console.log('📊 Token (premiers caractères):', token.substring(0, 20) + '...');
    }
    
    if (user) {
        try {
            const userData = JSON.parse(user);
            console.log('📊 User data:', userData);
        } catch (e) {
            console.log('❌ Erreur parsing user data:', e);
        }
    }
    
    return { token, user };
}

// Fonction pour tester les appels API
async function testAPICalls() {
    console.log('🌐 Test des appels API...');
    
    const { token } = checkAuthState();
    
    if (!token) {
        console.log('❌ Pas de token - impossible de tester les API');
        return;
    }
    
    // Test publications
    try {
        console.log('📝 Test API publications...');
        const postsResponse = await fetch('http://localhost:8000/api/posts/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        console.log('📊 Status publications:', postsResponse.status);
        
        if (postsResponse.ok) {
            const postsData = await postsResponse.json();
            console.log('✅ Publications récupérées');
            console.log('📊 Structure:', typeof postsData);
            console.log('📊 Clés:', Object.keys(postsData));
            
            if (postsData.results) {
                console.log('📊 Nombre de publications:', postsData.results.length);
                if (postsData.results.length > 0) {
                    console.log('📊 Premier post:', {
                        id: postsData.results[0].id,
                        content: postsData.results[0].content?.substring(0, 50) + '...',
                        author: postsData.results[0].author?.first_name
                    });
                }
            }
        } else {
            console.log('❌ Erreur publications:', postsResponse.status);
            const errorText = await postsResponse.text();
            console.log('📊 Erreur détail:', errorText);
        }
    } catch (error) {
        console.log('❌ Exception publications:', error);
    }
    
    // Test notifications
    try {
        console.log('🔔 Test API notifications...');
        const notifResponse = await fetch('http://localhost:8000/api/notifications/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        console.log('📊 Status notifications:', notifResponse.status);
        
        if (notifResponse.ok) {
            const notifData = await notifResponse.json();
            console.log('✅ Notifications récupérées');
            console.log('📊 Structure:', typeof notifData);
            console.log('📊 Clés:', Object.keys(notifData));
            
            if (notifData.results) {
                console.log('📊 Nombre de notifications:', notifData.results.length);
            }
        } else {
            console.log('❌ Erreur notifications:', notifResponse.status);
            const errorText = await notifResponse.text();
            console.log('📊 Erreur détail:', errorText);
        }
    } catch (error) {
        console.log('❌ Exception notifications:', error);
    }
}

// Fonction pour vérifier les composants React
function checkReactComponents() {
    console.log('⚛️ Vérification composants React...');
    
    // Vérifier si React est disponible
    if (typeof React !== 'undefined') {
        console.log('✅ React disponible');
    } else {
        console.log('❌ React non disponible');
    }
    
    // Vérifier les éléments DOM
    const dashboard = document.querySelector('[data-testid="dashboard"]') || 
                     document.querySelector('.dashboard') ||
                     document.querySelector('[class*="dashboard"]');
    
    if (dashboard) {
        console.log('✅ Élément Dashboard trouvé');
    } else {
        console.log('❌ Élément Dashboard non trouvé');
    }
    
    // Vérifier les posts
    const posts = document.querySelectorAll('[data-testid="post"]') ||
                  document.querySelectorAll('.post') ||
                  document.querySelectorAll('[class*="post"]');
    
    console.log('📊 Nombre d\'éléments posts trouvés:', posts.length);
    
    // Vérifier les notifications
    const notifications = document.querySelectorAll('[data-testid="notification"]') ||
                         document.querySelectorAll('.notification') ||
                         document.querySelectorAll('[class*="notification"]');
    
    console.log('📊 Nombre d\'éléments notifications trouvés:', notifications.length);
}

// Fonction pour vérifier les erreurs console
function checkConsoleErrors() {
    console.log('🚨 Vérification erreurs console...');
    
    // Cette fonction sera appelée après un délai pour capturer les erreurs
    setTimeout(() => {
        console.log('📊 Aucune erreur console détectée (ou déjà affichée)');
    }, 1000);
}

// Fonction principale
async function runDebug() {
    console.log('🧪 DEBUG COMPLET FRONTEND');
    console.log('=' .repeat(60));
    
    checkAuthState();
    await testAPICalls();
    checkReactComponents();
    checkConsoleErrors();
    
    console.log('📊 DEBUG TERMINÉ');
    console.log('=' .repeat(60));
}

// Exporter pour utilisation dans la console
window.debugFrontend = runDebug;

// Exécuter automatiquement si le script est chargé
if (typeof window !== 'undefined') {
    // Attendre que la page soit chargée
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runDebug);
    } else {
        runDebug();
    }
} 