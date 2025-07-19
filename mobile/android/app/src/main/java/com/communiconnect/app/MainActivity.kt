package com.communiconnect.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.communiconnect.app.ui.screens.*
import com.communiconnect.app.ui.theme.CommuniConnectTheme
import com.communiconnect.app.viewmodels.AuthViewModel
import com.communiconnect.app.viewmodels.HomeViewModel
import com.communiconnect.app.viewmodels.ProfileViewModel
import com.communiconnect.app.viewmodels.NotificationsViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CommuniConnectTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    CommuniConnectApp()
                }
            }
        }
    }
}

@Composable
fun CommuniConnectApp() {
    val navController = rememberNavController()
    val authViewModel = AuthViewModel()
    
    NavHost(navController = navController, startDestination = "auth") {
        composable("auth") {
            AuthenticationScreen(
                authViewModel = authViewModel,
                onNavigateToMain = {
                    navController.navigate("main") {
                        popUpTo("auth") { inclusive = true }
                    }
                }
            )
        }
        
        composable("main") {
            MainScreen(
                onNavigateToProfile = { navController.navigate("profile") },
                onNavigateToNotifications = { navController.navigate("notifications") },
                onNavigateToCreatePost = { navController.navigate("create_post") }
            )
        }
        
        composable("profile") {
            ProfileScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        
        composable("notifications") {
            NotificationsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        
        composable("create_post") {
            CreatePostScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}

// MARK: - Authentication Screen
@Composable
fun AuthenticationScreen(
    authViewModel: AuthViewModel,
    onNavigateToMain: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var showRegister by remember { mutableStateOf(false) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // Logo
        Icon(
            imageVector = Icons.Default.Globe,
            contentDescription = "Logo",
            modifier = Modifier.size(80.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "CommuniConnect",
            style = MaterialTheme.typography.headlineLarge,
            fontWeight = FontWeight.Bold
        )
        
        Text(
            text = "Connectez-vous avec votre communauté locale",
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Login Form
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            )
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Mot de passe") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done
            )
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Button(
            onClick = {
                isLoading = true
                // Simulate login
                LaunchedEffect(Unit) {
                    delay(1000)
                    isLoading = false
                    onNavigateToMain()
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = email.isNotEmpty() && password.isNotEmpty() && !isLoading
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Text("Se connecter")
            }
        }
        
        if (error != null) {
            Text(
                text = error!!,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        TextButton(
            onClick = { showRegister = true }
        ) {
            Text("Créer un compte")
        }
    }
    
    if (showRegister) {
        RegisterDialog(
            onDismiss = { showRegister = false },
            onRegister = { /* Register implementation */ }
        )
    }
}

// MARK: - Main Screen
@Composable
fun MainScreen(
    onNavigateToProfile: () -> Unit,
    onNavigateToNotifications: () -> Unit,
    onNavigateToCreatePost: () -> Unit
) {
    var selectedTab by remember { mutableStateOf(0) }
    val homeViewModel = HomeViewModel()
    
    Scaffold(
        bottomBar = {
            BottomNavigation {
                BottomNavigationItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = "Accueil") },
                    label = { Text("Accueil") },
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 }
                )
                BottomNavigationItem(
                    icon = { Icon(Icons.Default.Search, contentDescription = "Explorer") },
                    label = { Text("Explorer") },
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 }
                )
                BottomNavigationItem(
                    icon = { Icon(Icons.Default.Add, contentDescription = "Créer") },
                    label = { Text("Créer") },
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 }
                )
                BottomNavigationItem(
                    icon = { Icon(Icons.Default.Notifications, contentDescription = "Notifications") },
                    label = { Text("Notifications") },
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 }
                )
                BottomNavigationItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profil") },
                    label = { Text("Profil") },
                    selected = selectedTab == 4,
                    onClick = { selectedTab = 4 }
                )
            }
        }
    ) { paddingValues ->
        when (selectedTab) {
            0 -> HomeScreen(
                homeViewModel = homeViewModel,
                modifier = Modifier.padding(paddingValues)
            )
            1 -> ExploreScreen(modifier = Modifier.padding(paddingValues))
            2 -> CreatePostScreen(
                onNavigateBack = { selectedTab = 0 },
                modifier = Modifier.padding(paddingValues)
            )
            3 -> NotificationsScreen(
                onNavigateBack = { selectedTab = 0 },
                modifier = Modifier.padding(paddingValues)
            )
            4 -> ProfileScreen(
                onNavigateBack = { selectedTab = 0 },
                modifier = Modifier.padding(paddingValues)
            )
        }
    }
}

// MARK: - Home Screen
@Composable
fun HomeScreen(
    homeViewModel: HomeViewModel,
    modifier: Modifier = Modifier
) {
    val posts by homeViewModel.posts.collectAsState()
    val stories by homeViewModel.stories.collectAsState()
    
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 8.dp)
    ) {
        item {
            // Stories
            StoriesSection(stories = stories)
        }
        
        items(posts) { post ->
            PostCard(
                post = post,
                onLike = { homeViewModel.toggleLike(post.id) },
                onComment = { /* Navigate to comments */ },
                onShare = { /* Share post */ }
            )
        }
    }
}

@Composable
fun StoriesSection(stories: List<Story>) {
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(stories) { story ->
            StoryCard(story = story)
        }
    }
}

@Composable
fun StoryCard(story: Story) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.width(80.dp)
    ) {
        AsyncImage(
            model = story.userAvatar,
            contentDescription = "Avatar",
            modifier = Modifier
                .size(60.dp)
                .clip(CircleShape)
                .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape),
            contentScale = ContentScale.Crop
        )
        
        Spacer(modifier = Modifier.height(4.dp))
        
        Text(
            text = story.userName,
            style = MaterialTheme.typography.bodySmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun PostCard(
    post: Post,
    onLike: () -> Unit,
    onComment: () -> Unit,
    onShare: () -> Unit
) {
    var isLiked by remember { mutableStateOf(false) }
    
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            // Header
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                AsyncImage(
                    model = post.authorAvatar,
                    contentDescription = "Avatar",
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape),
                    contentScale = ContentScale.Crop
                )
                
                Spacer(modifier = Modifier.width(12.dp))
                
                Column {
                    Text(
                        text = post.authorName,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Semibold
                    )
                    Text(
                        text = post.location,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Spacer(modifier = Modifier.weight(1f))
                
                IconButton(onClick = { /* Show options */ }) {
                    Icon(
                        imageVector = Icons.Default.MoreVert,
                        contentDescription = "Options"
                    )
                }
            }
            
            // Content
            if (post.content.isNotEmpty()) {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = post.content,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            
            // Media
            post.mediaURL?.let { mediaURL ->
                Spacer(modifier = Modifier.height(12.dp))
                AsyncImage(
                    model = mediaURL,
                    contentDescription = "Media",
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .clip(RoundedCornerShape(12.dp)),
                    contentScale = ContentScale.Crop
                )
            }
            
            // Actions
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(
                    onClick = {
                        isLiked = !isLiked
                        onLike()
                    }
                ) {
                    Icon(
                        imageVector = if (isLiked) Icons.Filled.Favorite else Icons.Default.FavoriteBorder,
                        contentDescription = "Like",
                        tint = if (isLiked) Color.Red else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Text(
                    text = "${post.likesCount}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.width(16.dp))
                
                IconButton(onClick = onComment) {
                    Icon(
                        imageVector = Icons.Default.ChatBubbleOutline,
                        contentDescription = "Comment"
                    )
                }
                
                Text(
                    text = "${post.commentsCount}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.width(16.dp))
                
                IconButton(onClick = onShare) {
                    Icon(
                        imageVector = Icons.Default.Share,
                        contentDescription = "Share"
                    )
                }
                
                Text(
                    text = "${post.sharesCount}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.weight(1f))
                
                Text(
                    text = post.timeAgo,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

// MARK: - Explore Screen
@Composable
fun ExploreScreen(modifier: Modifier = Modifier) {
    var searchQuery by remember { mutableStateOf("") }
    val categories by remember { mutableStateOf(listOf<Category>()) }
    val trendingPosts by remember { mutableStateOf(listOf<Post>()) }
    
    Column(modifier = modifier.fillMaxSize()) {
        // Search Bar
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            placeholder = { Text("Rechercher...") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            singleLine = true
        )
        
        // Categories
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(categories) { category ->
                CategoryCard(category = category)
            }
        }
        
        // Trending Posts
        LazyColumn(
            contentPadding = PaddingValues(vertical = 8.dp)
        ) {
            items(trendingPosts) { post ->
                PostCard(
                    post = post,
                    onLike = { /* Like post */ },
                    onComment = { /* Comment on post */ },
                    onShare = { /* Share post */ }
                )
            }
        }
    }
}

@Composable
fun CategoryCard(category: Category) {
    Card(
        modifier = Modifier.width(100.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.padding(12.dp)
        ) {
            AsyncImage(
                model = category.iconURL,
                contentDescription = "Category icon",
                modifier = Modifier
                    .size(50.dp)
                    .clip(CircleShape),
                contentScale = ContentScale.Crop
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = category.name,
                style = MaterialTheme.typography.bodySmall,
                fontWeight = FontWeight.Medium,
                textAlign = TextAlign.Center
            )
        }
    }
}

// MARK: - Create Post Screen
@Composable
fun CreatePostScreen(
    onNavigateBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    var content by remember { mutableStateOf("") }
    var selectedImage by remember { mutableStateOf<Uri?>(null) }
    
    Column(modifier = modifier.fillMaxSize()) {
        // Top Bar
        TopAppBar(
            title = { Text("Nouveau Post") },
            navigationIcon = {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                }
            },
            actions = {
                TextButton(
                    onClick = { /* Create post */ },
                    enabled = content.isNotEmpty()
                ) {
                    Text("Publier")
                }
            }
        )
        
        // Content
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
        ) {
            // Text Input
            OutlinedTextField(
                value = content,
                onValueChange = { content = it },
                placeholder = { Text("Que se passe-t-il dans votre communauté ?") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                textStyle = MaterialTheme.typography.bodyLarge
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Media Preview
            selectedImage?.let { uri ->
                AsyncImage(
                    model = uri,
                    contentDescription = "Selected image",
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .clip(RoundedCornerShape(12.dp)),
                    contentScale = ContentScale.Crop
                )
                
                Spacer(modifier = Modifier.height(16.dp))
            }
            
            // Action Buttons
            Row(
                horizontalArrangement = Arrangement.SpaceEvenly,
                modifier = Modifier.fillMaxWidth()
            ) {
                IconButton(onClick = { /* Select image */ }) {
                    Icon(Icons.Default.Photo, contentDescription = "Photo")
                }
                
                IconButton(onClick = { /* Select video */ }) {
                    Icon(Icons.Default.VideoLibrary, contentDescription = "Video")
                }
                
                IconButton(onClick = { /* Select location */ }) {
                    Icon(Icons.Default.LocationOn, contentDescription = "Location")
                }
            }
        }
    }
}

// MARK: - Notifications Screen
@Composable
fun NotificationsScreen(
    onNavigateBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    val notifications by remember { mutableStateOf(listOf<Notification>()) }
    
    Column(modifier = modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text("Notifications") },
            navigationIcon = {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                }
            }
        )
        
        LazyColumn {
            items(notifications) { notification ->
                NotificationItem(notification = notification)
            }
        }
    }
}

@Composable
fun NotificationItem(notification: Notification) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        AsyncImage(
            model = notification.senderAvatar,
            contentDescription = "Avatar",
            modifier = Modifier
                .size(40.dp)
                .clip(CircleShape),
            contentScale = ContentScale.Crop
        )
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(
            modifier = Modifier.weight(1f)
        ) {
            Text(
                text = notification.message,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            
            Text(
                text = notification.timeAgo,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        if (!notification.isRead) {
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .background(
                        color = MaterialTheme.colorScheme.primary,
                        shape = CircleShape
                    )
            )
        }
    }
}

// MARK: - Profile Screen
@Composable
fun ProfileScreen(
    onNavigateBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    val profileViewModel = ProfileViewModel()
    val profile by profileViewModel.profile.collectAsState()
    val stats by profileViewModel.stats.collectAsState()
    val posts by profileViewModel.posts.collectAsState()
    
    Column(modifier = modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text("Profil") },
            navigationIcon = {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                }
            },
            actions = {
                IconButton(onClick = { /* Settings */ }) {
                    Icon(Icons.Default.Settings, contentDescription = "Settings")
                }
            }
        )
        
        LazyColumn {
            item {
                // Profile Header
                ProfileHeader(profile = profile)
                
                // Stats
                StatsSection(stats = stats)
            }
            
            // Posts Grid
            items(posts.chunked(3)) { rowPosts ->
                PostsGridRow(posts = rowPosts)
            }
        }
    }
}

@Composable
fun ProfileHeader(profile: Profile?) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(16.dp)
    ) {
        AsyncImage(
            model = profile?.avatarURL,
            contentDescription = "Profile avatar",
            modifier = Modifier
                .size(100.dp)
                .clip(CircleShape),
            contentScale = ContentScale.Crop
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = profile?.name ?: "",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
        
        Text(
            text = profile?.bio ?: "",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
        
        Text(
            text = profile?.location ?: "",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            OutlinedButton(onClick = { /* Edit profile */ }) {
                Text("Modifier")
            }
            
            OutlinedButton(onClick = { /* Share profile */ }) {
                Text("Partager")
            }
        }
    }
}

@Composable
fun StatsSection(stats: ProfileStats?) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
    ) {
        StatItem(
            title = "Posts",
            value = "${stats?.postsCount ?: 0}",
            modifier = Modifier.weight(1f)
        )
        
        StatItem(
            title = "Abonnés",
            value = "${stats?.followersCount ?: 0}",
            modifier = Modifier.weight(1f)
        )
        
        StatItem(
            title = "Abonnements",
            value = "${stats?.followingCount ?: 0}",
            modifier = Modifier.weight(1f)
        )
    }
}

@Composable
fun StatItem(
    title: String,
    value: String,
    modifier: Modifier = Modifier
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = modifier.padding(vertical = 12.dp)
    ) {
        Text(
            text = value,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold
        )
        
        Text(
            text = title,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun PostsGridRow(posts: List<Post>) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        posts.forEach { post ->
            AsyncImage(
                model = post.mediaURL,
                contentDescription = "Post media",
                modifier = Modifier
                    .weight(1f)
                    .height(120.dp),
                contentScale = ContentScale.Crop
            )
        }
        
        // Fill remaining space with empty boxes
        repeat(3 - posts.size) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .height(120.dp)
                    .background(Color.Gray.copy(alpha = 0.3f))
            )
        }
    }
}

// MARK: - Register Dialog
@Composable
fun RegisterDialog(
    onDismiss: () -> Unit,
    onRegister: () -> Unit
) {
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Créer un compte") },
        text = {
            Column {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Nom complet") },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                OutlinedTextField(
                    value = email,
                    onValueChange = { email = it },
                    label = { Text("Email") },
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    label = { Text("Mot de passe") },
                    modifier = Modifier.fillMaxWidth(),
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                OutlinedTextField(
                    value = confirmPassword,
                    onValueChange = { confirmPassword = it },
                    label = { Text("Confirmer le mot de passe") },
                    modifier = Modifier.fillMaxWidth(),
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
                )
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    onRegister()
                    onDismiss()
                },
                enabled = name.isNotEmpty() && email.isNotEmpty() && 
                         password.isNotEmpty() && password == confirmPassword
            ) {
                Text("Créer")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Annuler")
            }
        }
    )
}

// MARK: - Data Models
data class Post(
    val id: String,
    val authorName: String,
    val authorAvatar: String,
    val content: String,
    val mediaURL: String?,
    val location: String,
    val likesCount: Int,
    val commentsCount: Int,
    val sharesCount: Int,
    val timeAgo: String
)

data class Story(
    val id: String,
    val userName: String,
    val userAvatar: String
)

data class Category(
    val id: String,
    val name: String,
    val iconURL: String
)

data class Notification(
    val id: String,
    val message: String,
    val senderAvatar: String,
    val timeAgo: String,
    val isRead: Boolean
)

data class Profile(
    val name: String,
    val bio: String,
    val avatarURL: String,
    val location: String
)

data class ProfileStats(
    val postsCount: Int,
    val followersCount: Int,
    val followingCount: Int
)

// MARK: - View Models
class AuthViewModel : ViewModel() {
    private val _isAuthenticated = MutableStateFlow(false)
    val isAuthenticated: StateFlow<Boolean> = _isAuthenticated.asStateFlow()
    
    fun login(email: String, password: String) {
        // Login implementation
        _isAuthenticated.value = true
    }
    
    fun logout() {
        _isAuthenticated.value = false
    }
}

class HomeViewModel : ViewModel() {
    private val _posts = MutableStateFlow<List<Post>>(emptyList())
    val posts: StateFlow<List<Post>> = _posts.asStateFlow()
    
    private val _stories = MutableStateFlow<List<Story>>(emptyList())
    val stories: StateFlow<List<Story>> = _stories.asStateFlow()
    
    fun loadPosts() {
        // Load posts from API
    }
    
    fun toggleLike(postId: String) {
        // Toggle like implementation
    }
}

class ProfileViewModel : ViewModel() {
    private val _profile = MutableStateFlow<Profile?>(null)
    val profile: StateFlow<Profile?> = _profile.asStateFlow()
    
    private val _stats = MutableStateFlow<ProfileStats?>(null)
    val stats: StateFlow<ProfileStats?> = _stats.asStateFlow()
    
    private val _posts = MutableStateFlow<List<Post>>(emptyList())
    val posts: StateFlow<List<Post>> = _posts.asStateFlow()
    
    fun loadProfile() {
        // Load profile data
    }
}

class NotificationsViewModel : ViewModel() {
    private val _notifications = MutableStateFlow<List<Notification>>(emptyList())
    val notifications: StateFlow<List<Notification>> = _notifications.asStateFlow()
    
    fun loadNotifications() {
        // Load notifications
    }
} 