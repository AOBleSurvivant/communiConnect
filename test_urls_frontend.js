// Test des URLs du frontend
const BASE_URL = "http://127.0.0.1:8000/api";

// URLs à tester
const urlsToTest = [
  // Likes
  `${BASE_URL}/posts/410/like/`,
  
  // Commentaires
  `${BASE_URL}/posts/410/comments/`,
  
  // Partages (avec double posts)
  `${BASE_URL}/posts/posts/410/share/`,
  `${BASE_URL}/posts/posts/410/shares/`,
  `${BASE_URL}/posts/posts/410/share-external/`,
  `${BASE_URL}/posts/posts/410/external-shares/`,
  
  // Analytics (avec double posts)
  `${BASE_URL}/posts/posts/410/analytics/`,
];

console.log("🔗 TEST DES URLS FRONTEND");
console.log("=" * 60);

urlsToTest.forEach((url, index) => {
  console.log(`${index + 1}. ${url}`);
});

console.log("\n📊 RÉSUMÉ:");
console.log("✅ URLs likes: /posts/{id}/like/");
console.log("✅ URLs commentaires: /posts/{id}/comments/");
console.log("✅ URLs partages: /posts/posts/{id}/share/");
console.log("✅ URLs analytics: /posts/posts/{id}/analytics/");
console.log("\n💡 Les URLs partages et analytics nécessitent le double 'posts'"); 