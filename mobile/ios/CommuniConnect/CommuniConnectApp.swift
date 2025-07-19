import SwiftUI
import Combine
import CoreData
import UserNotifications

@main
struct CommuniConnectApp: App {
    @StateObject private var authManager = AuthenticationManager()
    @StateObject private var networkManager = NetworkManager()
    @StateObject private var notificationManager = NotificationManager()
    @StateObject private var locationManager = LocationManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .environmentObject(networkManager)
                .environmentObject(notificationManager)
                .environmentObject(locationManager)
                .onAppear {
                    setupApp()
                }
        }
    }
    
    private func setupApp() {
        // Configuration initiale de l'app
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if granted {
                DispatchQueue.main.async {
                    UIApplication.shared.registerForRemoteNotifications()
                }
            }
        }
        
        // Configuration du réseau
        networkManager.configure()
        
        // Configuration des notifications
        notificationManager.configure()
        
        // Configuration de la localisation
        locationManager.requestLocationPermission()
    }
}

struct ContentView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @State private var selectedTab = 0
    
    var body: some View {
        Group {
            if authManager.isAuthenticated {
                MainTabView(selectedTab: $selectedTab)
            } else {
                AuthenticationView()
            }
        }
        .animation(.easeInOut, value: authManager.isAuthenticated)
    }
}

struct MainTabView: View {
    @Binding var selectedTab: Int
    @EnvironmentObject var notificationManager: NotificationManager
    
    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Image(systemName: "house.fill")
                    Text("Accueil")
                }
                .tag(0)
            
            ExploreView()
                .tabItem {
                    Image(systemName: "magnifyingglass")
                    Text("Explorer")
                }
                .tag(1)
            
            CreatePostView()
                .tabItem {
                    Image(systemName: "plus.circle.fill")
                    Text("Créer")
                }
                .tag(2)
            
            NotificationsView()
                .tabItem {
                    Image(systemName: "bell.fill")
                    Text("Notifications")
                }
                .badge(notificationManager.unreadCount)
                .tag(3)
            
            ProfileView()
                .tabItem {
                    Image(systemName: "person.fill")
                    Text("Profil")
                }
                .tag(4)
        }
        .accentColor(.purple)
    }
}

// MARK: - Home View
struct HomeView: View {
    @StateObject private var viewModel = HomeViewModel()
    @EnvironmentObject var authManager: AuthenticationManager
    
    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 16) {
                    // Stories
                    StoriesView()
                    
                    // Posts
                    ForEach(viewModel.posts) { post in
                        PostCardView(post: post)
                            .padding(.horizontal)
                    }
                }
                .padding(.top)
            }
            .navigationTitle("CommuniConnect")
            .navigationBarTitleDisplayMode(.large)
            .refreshable {
                await viewModel.loadPosts()
            }
            .onAppear {
                viewModel.loadPosts()
            }
        }
    }
}

// MARK: - Stories View
struct StoriesView: View {
    @StateObject private var viewModel = StoriesViewModel()
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            LazyHStack(spacing: 12) {
                ForEach(viewModel.stories) { story in
                    StoryCardView(story: story)
                }
            }
            .padding(.horizontal)
        }
        .frame(height: 100)
    }
}

struct StoryCardView: View {
    let story: Story
    
    var body: some View {
        VStack {
            AsyncImage(url: URL(string: story.userAvatar)) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Circle()
                    .fill(Color.gray.opacity(0.3))
            }
            .frame(width: 60, height: 60)
            .clipShape(Circle())
            .overlay(
                Circle()
                    .stroke(Color.purple, lineWidth: 2)
            )
            
            Text(story.userName)
                .font(.caption)
                .lineLimit(1)
        }
    }
}

// MARK: - Post Card View
struct PostCardView: View {
    let post: Post
    @StateObject private var viewModel = PostCardViewModel()
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Header
            HStack {
                AsyncImage(url: URL(string: post.authorAvatar)) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Circle()
                        .fill(Color.gray.opacity(0.3))
                }
                .frame(width: 40, height: 40)
                .clipShape(Circle())
                
                VStack(alignment: .leading) {
                    Text(post.authorName)
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    Text(post.location)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                Button(action: {
                    viewModel.showOptions = true
                }) {
                    Image(systemName: "ellipsis")
                        .foregroundColor(.secondary)
                }
            }
            
            // Content
            if !post.content.isEmpty {
                Text(post.content)
                    .font(.body)
                    .lineLimit(nil)
            }
            
            // Media
            if let mediaURL = post.mediaURL {
                AsyncImage(url: URL(string: mediaURL)) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .cornerRadius(12)
                } placeholder: {
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                        .cornerRadius(12)
                        .frame(height: 200)
                }
            }
            
            // Actions
            HStack(spacing: 20) {
                Button(action: {
                    viewModel.toggleLike()
                }) {
                    HStack(spacing: 4) {
                        Image(systemName: viewModel.isLiked ? "heart.fill" : "heart")
                            .foregroundColor(viewModel.isLiked ? .red : .secondary)
                        Text("\(post.likesCount)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                Button(action: {
                    viewModel.showComments = true
                }) {
                    HStack(spacing: 4) {
                        Image(systemName: "bubble.left")
                            .foregroundColor(.secondary)
                        Text("\(post.commentsCount)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                Button(action: {
                    viewModel.sharePost()
                }) {
                    HStack(spacing: 4) {
                        Image(systemName: "square.and.arrow.up")
                            .foregroundColor(.secondary)
                        Text("\(post.sharesCount)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                Spacer()
                
                Text(post.timeAgo)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
        .sheet(isPresented: $viewModel.showComments) {
            CommentsView(post: post)
        }
        .actionSheet(isPresented: $viewModel.showOptions) {
            ActionSheet(
                title: Text("Options"),
                buttons: [
                    .default(Text("Signaler")) { viewModel.reportPost() },
                    .destructive(Text("Supprimer")) { viewModel.deletePost() },
                    .cancel()
                ]
            )
        }
    }
}

// MARK: - Explore View
struct ExploreView: View {
    @StateObject private var viewModel = ExploreViewModel()
    @State private var searchText = ""
    
    var body: some View {
        NavigationView {
            VStack {
                // Search Bar
                SearchBar(text: $searchText)
                    .padding()
                
                // Categories
                ScrollView(.horizontal, showsIndicators: false) {
                    LazyHStack(spacing: 12) {
                        ForEach(viewModel.categories) { category in
                            CategoryCardView(category: category)
                        }
                    }
                    .padding(.horizontal)
                }
                
                // Trending Posts
                ScrollView {
                    LazyVStack(spacing: 16) {
                        ForEach(viewModel.trendingPosts) { post in
                            PostCardView(post: post)
                                .padding(.horizontal)
                        }
                    }
                }
            }
            .navigationTitle("Explorer")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

struct SearchBar: View {
    @Binding var text: String
    
    var body: some View {
        HStack {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.secondary)
            
            TextField("Rechercher...", text: $text)
                .textFieldStyle(PlainTextFieldStyle())
            
            if !text.isEmpty {
                Button(action: {
                    text = ""
                }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(10)
    }
}

struct CategoryCardView: View {
    let category: Category
    
    var body: some View {
        VStack {
            AsyncImage(url: URL(string: category.iconURL)) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            } placeholder: {
                Circle()
                    .fill(Color.purple.opacity(0.3))
            }
            .frame(width: 50, height: 50)
            .clipShape(Circle())
            
            Text(category.name)
                .font(.caption)
                .fontWeight(.medium)
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 12)
        .background(Color.purple.opacity(0.1))
        .cornerRadius(20)
    }
}

// MARK: - Create Post View
struct CreatePostView: View {
    @StateObject private var viewModel = CreatePostViewModel()
    @EnvironmentObject var locationManager: LocationManager
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        NavigationView {
            VStack {
                // Content Input
                TextEditor(text: $viewModel.content)
                    .padding()
                    .frame(minHeight: 100)
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                    .padding()
                
                // Media Selection
                if let selectedImage = viewModel.selectedImage {
                    Image(uiImage: selectedImage)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(maxHeight: 200)
                        .cornerRadius(12)
                        .padding(.horizontal)
                }
                
                // Action Buttons
                HStack(spacing: 20) {
                    Button(action: {
                        viewModel.selectImage()
                    }) {
                        HStack {
                            Image(systemName: "photo")
                            Text("Photo")
                        }
                        .foregroundColor(.purple)
                    }
                    
                    Button(action: {
                        viewModel.selectVideo()
                    }) {
                        HStack {
                            Image(systemName: "video")
                            Text("Vidéo")
                        }
                        .foregroundColor(.purple)
                    }
                    
                    Button(action: {
                        viewModel.selectLocation()
                    }) {
                        HStack {
                            Image(systemName: "location")
                            Text("Localisation")
                        }
                        .foregroundColor(.purple)
                    }
                    
                    Spacer()
                }
                .padding()
                
                Spacer()
            }
            .navigationTitle("Nouveau Post")
            .navigationBarTitleDisplayMode(.inline)
            .navigationBarItems(
                leading: Button("Annuler") {
                    presentationMode.wrappedValue.dismiss()
                },
                trailing: Button("Publier") {
                    Task {
                        await viewModel.createPost()
                        presentationMode.wrappedValue.dismiss()
                    }
                }
                .disabled(viewModel.content.isEmpty)
            )
        }
    }
}

// MARK: - Notifications View
struct NotificationsView: View {
    @StateObject private var viewModel = NotificationsViewModel()
    @EnvironmentObject var notificationManager: NotificationManager
    
    var body: some View {
        NavigationView {
            List {
                ForEach(viewModel.notifications) { notification in
                    NotificationRowView(notification: notification)
                }
            }
            .navigationTitle("Notifications")
            .navigationBarTitleDisplayMode(.large)
            .refreshable {
                await viewModel.loadNotifications()
            }
            .onAppear {
                viewModel.loadNotifications()
            }
        }
    }
}

struct NotificationRowView: View {
    let notification: Notification
    
    var body: some View {
        HStack(spacing: 12) {
            AsyncImage(url: URL(string: notification.senderAvatar)) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Circle()
                    .fill(Color.gray.opacity(0.3))
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 4) {
                Text(notification.message)
                    .font(.body)
                    .lineLimit(2)
                
                Text(notification.timeAgo)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            if !notification.isRead {
                Circle()
                    .fill(Color.purple)
                    .frame(width: 8, height: 8)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Profile View
struct ProfileView: View {
    @StateObject private var viewModel = ProfileViewModel()
    @EnvironmentObject var authManager: AuthenticationManager
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Profile Header
                    ProfileHeaderView(profile: viewModel.profile)
                    
                    // Stats
                    StatsView(stats: viewModel.stats)
                    
                    // Posts Grid
                    PostsGridView(posts: viewModel.posts)
                }
            }
            .navigationTitle("Profil")
            .navigationBarTitleDisplayMode(.large)
            .navigationBarItems(trailing: Button("Paramètres") {
                viewModel.showSettings = true
            })
            .sheet(isPresented: $viewModel.showSettings) {
                SettingsView()
            }
            .onAppear {
                viewModel.loadProfile()
            }
        }
    }
}

struct ProfileHeaderView: View {
    let profile: Profile
    
    var body: some View {
        VStack(spacing: 16) {
            AsyncImage(url: URL(string: profile.avatarURL)) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Circle()
                    .fill(Color.gray.opacity(0.3))
            }
            .frame(width: 100, height: 100)
            .clipShape(Circle())
            
            VStack(spacing: 8) {
                Text(profile.name)
                    .font(.title2)
                    .fontWeight(.bold)
                
                Text(profile.bio)
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                
                Text(profile.location)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            HStack(spacing: 20) {
                Button("Modifier") {
                    // Edit profile action
                }
                .foregroundColor(.purple)
                
                Button("Partager") {
                    // Share profile action
                }
                .foregroundColor(.purple)
            }
        }
        .padding()
    }
}

struct StatsView: View {
    let stats: ProfileStats
    
    var body: some View {
        HStack(spacing: 0) {
            StatItemView(title: "Posts", value: "\(stats.postsCount)")
            StatItemView(title: "Abonnés", value: "\(stats.followersCount)")
            StatItemView(title: "Abonnements", value: "\(stats.followingCount)")
        }
        .background(Color(.systemGray6))
        .cornerRadius(12)
        .padding(.horizontal)
    }
}

struct StatItemView: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack(spacing: 4) {
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 12)
    }
}

struct PostsGridView: View {
    let posts: [Post]
    let columns = Array(repeating: GridItem(.flexible(), spacing: 2), count: 3)
    
    var body: some View {
        LazyVGrid(columns: columns, spacing: 2) {
            ForEach(posts) { post in
                AsyncImage(url: URL(string: post.mediaURL ?? "")) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                }
                .frame(height: 120)
                .clipped()
            }
        }
        .padding(.horizontal)
    }
}

// MARK: - Authentication View
struct AuthenticationView: View {
    @StateObject private var viewModel = AuthenticationViewModel()
    @EnvironmentObject var authManager: AuthenticationManager
    
    var body: some View {
        NavigationView {
            VStack(spacing: 30) {
                // Logo
                VStack(spacing: 16) {
                    Image(systemName: "globe")
                        .font(.system(size: 80))
                        .foregroundColor(.purple)
                    
                    Text("CommuniConnect")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Text("Connectez-vous avec votre communauté locale")
                        .font(.body)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                
                // Login Form
                VStack(spacing: 16) {
                    TextField("Email", text: $viewModel.email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                    
                    SecureField("Mot de passe", text: $viewModel.password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    Button(action: {
                        Task {
                            await viewModel.login()
                        }
                    }) {
                        Text("Se connecter")
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.purple)
                            .cornerRadius(10)
                    }
                    .disabled(viewModel.isLoading)
                    
                    if viewModel.isLoading {
                        ProgressView()
                    }
                    
                    if let error = viewModel.error {
                        Text(error)
                            .font(.caption)
                            .foregroundColor(.red)
                    }
                }
                .padding(.horizontal)
                
                // Register Link
                Button("Créer un compte") {
                    viewModel.showRegister = true
                }
                .foregroundColor(.purple)
                
                Spacer()
            }
            .padding()
            .sheet(isPresented: $viewModel.showRegister) {
                RegisterView()
            }
        }
    }
}

// MARK: - Data Models
struct Post: Identifiable, Codable {
    let id: String
    let authorName: String
    let authorAvatar: String
    let content: String
    let mediaURL: String?
    let location: String
    let likesCount: Int
    let commentsCount: Int
    let sharesCount: Int
    let timeAgo: String
}

struct Story: Identifiable, Codable {
    let id: String
    let userName: String
    let userAvatar: String
}

struct Category: Identifiable, Codable {
    let id: String
    let name: String
    let iconURL: String
}

struct Notification: Identifiable, Codable {
    let id: String
    let message: String
    let senderAvatar: String
    let timeAgo: String
    let isRead: Bool
}

struct Profile: Codable {
    let name: String
    let bio: String
    let avatarURL: String
    let location: String
}

struct ProfileStats: Codable {
    let postsCount: Int
    let followersCount: Int
    let followingCount: Int
}

// MARK: - View Models
class HomeViewModel: ObservableObject {
    @Published var posts: [Post] = []
    
    func loadPosts() {
        // Load posts from API
    }
}

class StoriesViewModel: ObservableObject {
    @Published var stories: [Story] = []
}

class PostCardViewModel: ObservableObject {
    @Published var isLiked = false
    @Published var showComments = false
    @Published var showOptions = false
    
    func toggleLike() {
        isLiked.toggle()
    }
    
    func showComments() {
        showComments = true
    }
    
    func sharePost() {
        // Share post implementation
    }
    
    func reportPost() {
        // Report post implementation
    }
    
    func deletePost() {
        // Delete post implementation
    }
}

class ExploreViewModel: ObservableObject {
    @Published var categories: [Category] = []
    @Published var trendingPosts: [Post] = []
    
    func loadData() {
        // Load explore data
    }
}

class CreatePostViewModel: ObservableObject {
    @Published var content = ""
    @Published var selectedImage: UIImage?
    @Published var isLoading = false
    
    func selectImage() {
        // Image picker implementation
    }
    
    func selectVideo() {
        // Video picker implementation
    }
    
    func selectLocation() {
        // Location picker implementation
    }
    
    func createPost() async {
        // Create post implementation
    }
}

class NotificationsViewModel: ObservableObject {
    @Published var notifications: [Notification] = []
    
    func loadNotifications() async {
        // Load notifications
    }
}

class ProfileViewModel: ObservableObject {
    @Published var profile: Profile?
    @Published var stats: ProfileStats?
    @Published var posts: [Post] = []
    @Published var showSettings = false
    
    func loadProfile() {
        // Load profile data
    }
}

class AuthenticationViewModel: ObservableObject {
    @Published var email = ""
    @Published var password = ""
    @Published var isLoading = false
    @Published var error: String?
    @Published var showRegister = false
    
    func login() async {
        // Login implementation
    }
}

// MARK: - Managers
class AuthenticationManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    
    func login(email: String, password: String) async {
        // Login implementation
    }
    
    func logout() {
        // Logout implementation
    }
}

class NetworkManager: ObservableObject {
    func configure() {
        // Network configuration
    }
}

class NotificationManager: ObservableObject {
    @Published var unreadCount = 0
    
    func configure() {
        // Notification configuration
    }
}

class LocationManager: ObservableObject {
    func requestLocationPermission() {
        // Location permission request
    }
}

// MARK: - Additional Views
struct CommentsView: View {
    let post: Post
    @State private var commentText = ""
    
    var body: some View {
        NavigationView {
            VStack {
                List {
                    // Comments list
                }
                
                HStack {
                    TextField("Ajouter un commentaire...", text: $commentText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    Button("Envoyer") {
                        // Send comment
                    }
                    .disabled(commentText.isEmpty)
                }
                .padding()
            }
            .navigationTitle("Commentaires")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

struct SettingsView: View {
    var body: some View {
        NavigationView {
            List {
                Section("Compte") {
                    NavigationLink("Modifier le profil") {
                        Text("Modifier le profil")
                    }
                    NavigationLink("Sécurité") {
                        Text("Sécurité")
                    }
                    NavigationLink("Confidentialité") {
                        Text("Confidentialité")
                    }
                }
                
                Section("Application") {
                    NavigationLink("Notifications") {
                        Text("Notifications")
                    }
                    NavigationLink("Langue") {
                        Text("Langue")
                    }
                    NavigationLink("Thème") {
                        Text("Thème")
                    }
                }
                
                Section("Support") {
                    NavigationLink("Aide") {
                        Text("Aide")
                    }
                    NavigationLink("À propos") {
                        Text("À propos")
                    }
                }
            }
            .navigationTitle("Paramètres")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

struct RegisterView: View {
    @Environment(\.presentationMode) var presentationMode
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var name = ""
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("Créer un compte")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                VStack(spacing: 16) {
                    TextField("Nom complet", text: $name)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    TextField("Email", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                    
                    SecureField("Mot de passe", text: $password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    SecureField("Confirmer le mot de passe", text: $confirmPassword)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                Button("Créer le compte") {
                    // Register implementation
                }
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.purple)
                .cornerRadius(10)
                
                Spacer()
            }
            .padding()
            .navigationBarItems(leading: Button("Annuler") {
                presentationMode.wrappedValue.dismiss()
            })
        }
    }
} 