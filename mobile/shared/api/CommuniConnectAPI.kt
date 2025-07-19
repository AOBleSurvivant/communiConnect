package com.communiconnect.app.api

import kotlinx.coroutines.flow.Flow
import retrofit2.http.*
import retrofit2.Response

// MARK: - API Service Interface
interface CommuniConnectAPI {
    
    // MARK: - Authentication
    @POST("auth/login/")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>
    
    @POST("auth/register/")
    suspend fun register(@Body request: RegisterRequest): Response<RegisterResponse>
    
    @POST("auth/logout/")
    suspend fun logout(): Response<Unit>
    
    @POST("auth/refresh/")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<RefreshTokenResponse>
    
    // MARK: - Posts
    @GET("posts/")
    suspend fun getPosts(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20,
        @Query("location") location: String? = null,
        @Query("category") category: String? = null
    ): Response<PostsResponse>
    
    @GET("posts/{postId}/")
    suspend fun getPost(@Path("postId") postId: String): Response<Post>
    
    @POST("posts/")
    suspend fun createPost(@Body request: CreatePostRequest): Response<Post>
    
    @PUT("posts/{postId}/")
    suspend fun updatePost(
        @Path("postId") postId: String,
        @Body request: UpdatePostRequest
    ): Response<Post>
    
    @DELETE("posts/{postId}/")
    suspend fun deletePost(@Path("postId") postId: String): Response<Unit>
    
    @POST("posts/{postId}/like/")
    suspend fun likePost(@Path("postId") postId: String): Response<LikeResponse>
    
    @DELETE("posts/{postId}/like/")
    suspend fun unlikePost(@Path("postId") postId: String): Response<LikeResponse>
    
    @POST("posts/{postId}/comment/")
    suspend fun commentOnPost(
        @Path("postId") postId: String,
        @Body request: CreateCommentRequest
    ): Response<Comment>
    
    @GET("posts/{postId}/comments/")
    suspend fun getPostComments(
        @Path("postId") postId: String,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<CommentsResponse>
    
    // MARK: - Stories
    @GET("stories/")
    suspend fun getStories(): Response<StoriesResponse>
    
    @POST("stories/")
    suspend fun createStory(@Body request: CreateStoryRequest): Response<Story>
    
    // MARK: - Users
    @GET("users/profile/")
    suspend fun getProfile(): Response<Profile>
    
    @PUT("users/profile/")
    suspend fun updateProfile(@Body request: UpdateProfileRequest): Response<Profile>
    
    @GET("users/{userId}/")
    suspend fun getUser(@Path("userId") userId: String): Response<User>
    
    @GET("users/{userId}/posts/")
    suspend fun getUserPosts(
        @Path("userId") userId: String,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<PostsResponse>
    
    @POST("users/{userId}/follow/")
    suspend fun followUser(@Path("userId") userId: String): Response<FollowResponse>
    
    @DELETE("users/{userId}/follow/")
    suspend fun unfollowUser(@Path("userId") userId: String): Response<FollowResponse>
    
    @GET("users/friends/")
    suspend fun getFriends(): Response<FriendsResponse>
    
    @GET("users/suggestions/")
    suspend fun getSuggestedUsers(): Response<SuggestedUsersResponse>
    
    // MARK: - Notifications
    @GET("notifications/")
    suspend fun getNotifications(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<NotificationsResponse>
    
    @PUT("notifications/{notificationId}/read/")
    suspend fun markNotificationAsRead(@Path("notificationId") notificationId: String): Response<Unit>
    
    @PUT("notifications/read-all/")
    suspend fun markAllNotificationsAsRead(): Response<Unit>
    
    // MARK: - Search
    @GET("search/")
    suspend fun search(
        @Query("q") query: String,
        @Query("type") type: String? = null,
        @Query("location") location: String? = null,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<SearchResponse>
    
    // MARK: - Categories
    @GET("categories/")
    suspend fun getCategories(): Response<CategoriesResponse>
    
    @GET("categories/{categoryId}/posts/")
    suspend fun getCategoryPosts(
        @Path("categoryId") categoryId: String,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<PostsResponse>
    
    // MARK: - Analytics
    @GET("analytics/dashboard/")
    suspend fun getAnalyticsDashboard(): Response<AnalyticsDashboard>
    
    @GET("analytics/user/")
    suspend fun getUserAnalytics(): Response<UserAnalytics>
    
    // MARK: - AI Recommendations
    @GET("ai/recommendations/")
    suspend fun getAIRecommendations(): Response<AIRecommendations>
    
    @POST("ai/feedback/")
    suspend fun submitAIFeedback(@Body request: AIFeedbackRequest): Response<Unit>
    
    // MARK: - Security
    @POST("security/audit/")
    suspend fun auditSecurityEvent(@Body request: SecurityAuditRequest): Response<SecurityAudit>
    
    @GET("security/audits/")
    suspend fun getSecurityAudits(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<SecurityAuditsResponse>
    
    @POST("security/detect-fraud/")
    suspend fun detectFraud(@Body request: FraudDetectionRequest): Response<FraudDetection>
    
    @GET("security/dashboard/")
    suspend fun getSecurityDashboard(): Response<SecurityDashboard>
    
    // MARK: - Media Upload
    @Multipart
    @POST("media/upload/")
    suspend fun uploadMedia(
        @Part file: MultipartBody.Part,
        @Part("type") type: RequestBody
    ): Response<MediaUploadResponse>
    
    // MARK: - Location Services
    @GET("geography/quartiers/")
    suspend fun getQuartiers(): Response<QuartiersResponse>
    
    @GET("geography/quartiers/{quartierId}/")
    suspend fun getQuartier(@Path("quartierId") quartierId: String): Response<Quartier>
    
    @GET("geography/quartiers/{quartierId}/posts/")
    suspend fun getQuartierPosts(
        @Path("quartierId") quartierId: String,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<PostsResponse>
}

// MARK: - Request Models
data class LoginRequest(
    val email: String,
    val password: String,
    val device_info: DeviceInfo? = null
)

data class RegisterRequest(
    val email: String,
    val password: String,
    val name: String,
    val phone_number: String? = null,
    val quartier_id: String? = null,
    val device_info: DeviceInfo? = null
)

data class RefreshTokenRequest(
    val refresh_token: String
)

data class CreatePostRequest(
    val content: String,
    val media_url: String? = null,
    val location: String? = null,
    val is_public: Boolean = true,
    val category: String? = null
)

data class UpdatePostRequest(
    val content: String,
    val media_url: String? = null,
    val is_public: Boolean? = null
)

data class CreateCommentRequest(
    val content: String,
    val parent_comment_id: String? = null
)

data class CreateStoryRequest(
    val media_url: String,
    val duration: Int = 24 // hours
)

data class UpdateProfileRequest(
    val name: String? = null,
    val bio: String? = null,
    val avatar_url: String? = null,
    val phone_number: String? = null,
    val quartier_id: String? = null,
    val privacy_settings: PrivacySettings? = null
)

data class AIFeedbackRequest(
    val recommendation_id: String,
    val feedback_type: String, // "like", "dislike", "click", "ignore"
    val feedback_data: Map<String, Any>? = null
)

data class SecurityAuditRequest(
    val event_type: String,
    val description: String,
    val severity: String = "low",
    val metadata: Map<String, Any>? = null
)

data class FraudDetectionRequest(
    val activity_type: String,
    val context: Map<String, Any>? = null
)

data class DeviceInfo(
    val device_type: String,
    val os_version: String,
    val app_version: String,
    val device_id: String? = null
)

// MARK: - Response Models
data class LoginResponse(
    val access_token: String,
    val refresh_token: String,
    val user: User,
    val expires_in: Int
)

data class RegisterResponse(
    val access_token: String,
    val refresh_token: String,
    val user: User,
    val expires_in: Int
)

data class RefreshTokenResponse(
    val access_token: String,
    val expires_in: Int
)

data class PostsResponse(
    val posts: List<Post>,
    val total_count: Int,
    val has_next: Boolean,
    val has_previous: Boolean
)

data class CommentsResponse(
    val comments: List<Comment>,
    val total_count: Int,
    val has_next: Boolean,
    val has_previous: Boolean
)

data class StoriesResponse(
    val stories: List<Story>
)

data class FriendsResponse(
    val friends: List<User>,
    val pending_requests: List<User>,
    val suggested_friends: List<User>
)

data class SuggestedUsersResponse(
    val users: List<User>
)

data class NotificationsResponse(
    val notifications: List<Notification>,
    val total_count: Int,
    val unread_count: Int,
    val has_next: Boolean,
    val has_previous: Boolean
)

data class SearchResponse(
    val posts: List<Post>? = null,
    val users: List<User>? = null,
    val categories: List<Category>? = null,
    val total_count: Int
)

data class CategoriesResponse(
    val categories: List<Category>
)

data class AnalyticsDashboard(
    val global_metrics: GlobalMetrics,
    val user_analytics: UserAnalytics,
    val real_time_insights: RealTimeInsights,
    val security_score: Double
)

data class UserAnalytics(
    val engagement_rate: Double,
    val retention_score: Double,
    val influence_score: Double,
    val growth_rate: Double
)

data class AIRecommendations(
    val personalized_posts: List<Post>,
    val trending_topics: List<TrendingTopic>,
    val user_insights: UserInsights,
    val content_suggestions: List<ContentSuggestion>
)

data class SecurityDashboard(
    val recent_audits: List<SecurityAudit>,
    val fraud_detections: List<FraudDetection>,
    val security_alerts: List<SecurityAlert>,
    val security_score: Double
)

data class MediaUploadResponse(
    val media_id: String,
    val media_url: String,
    val media_type: String,
    val file_size: Long,
    val upload_time: String
)

data class QuartiersResponse(
    val quartiers: List<Quartier>
)

// MARK: - Data Models
data class User(
    val id: String,
    val email: String,
    val name: String,
    val avatar_url: String?,
    val bio: String?,
    val phone_number: String?,
    val quartier: Quartier?,
    val is_verified: Boolean = false,
    val followers_count: Int = 0,
    val following_count: Int = 0,
    val posts_count: Int = 0,
    val created_at: String,
    val last_active: String
)

data class Post(
    val id: String,
    val author: User,
    val content: String,
    val media_url: String?,
    val media_type: String?,
    val location: String?,
    val likes_count: Int = 0,
    val comments_count: Int = 0,
    val shares_count: Int = 0,
    val views_count: Int = 0,
    val is_liked: Boolean = false,
    val is_public: Boolean = true,
    val category: Category?,
    val created_at: String,
    val updated_at: String
)

data class Comment(
    val id: String,
    val author: User,
    val content: String,
    val parent_comment: Comment?,
    val likes_count: Int = 0,
    val is_liked: Boolean = false,
    val created_at: String
)

data class Story(
    val id: String,
    val author: User,
    val media_url: String,
    val duration: Int,
    val views_count: Int = 0,
    val created_at: String,
    val expires_at: String
)

data class Notification(
    val id: String,
    val type: String,
    val title: String,
    val message: String,
    val sender: User?,
    val post: Post?,
    val is_read: Boolean = false,
    val created_at: String
)

data class Category(
    val id: String,
    val name: String,
    val description: String?,
    val icon_url: String?,
    val color: String?,
    val posts_count: Int = 0
)

data class Quartier(
    val id: String,
    val nom: String,
    val commune: Commune,
    val description: String?,
    val posts_count: Int = 0,
    val users_count: Int = 0
)

data class Commune(
    val id: String,
    val nom: String,
    val region: String
)

data class LikeResponse(
    val is_liked: Boolean,
    val likes_count: Int
)

data class FollowResponse(
    val is_following: Boolean,
    val followers_count: Int
)

data class Profile(
    val user: User,
    val privacy_settings: PrivacySettings,
    val analytics: UserAnalytics
)

data class PrivacySettings(
    val profile_visibility: String,
    val share_location: Boolean,
    val share_activity: Boolean,
    val share_posts: Boolean,
    val share_friends: Boolean,
    val email_notifications: Boolean,
    val sms_notifications: Boolean,
    val push_notifications: Boolean
)

data class GlobalMetrics(
    val total_users: Int,
    val total_posts: Int,
    val total_likes: Int,
    val total_comments: Int,
    val new_users_today: Int,
    val new_posts_today: Int
)

data class RealTimeInsights(
    val current_hour: HourlyMetrics,
    val last_24h: DailyMetrics,
    val top_performers: List<User>,
    val trending_content: List<Post>
)

data class HourlyMetrics(
    val new_users: Int,
    val new_posts: Int,
    val new_likes: Int,
    val new_comments: Int
)

data class DailyMetrics(
    val new_users: Int,
    val new_posts: Int,
    val new_likes: Int,
    val new_comments: Int
)

data class TrendingTopic(
    val topic: String,
    val count: Int,
    val trend: String // "up", "down", "stable"
)

data class UserInsights(
    val engagement_level: String,
    val activity_pattern: String,
    val content_preferences: List<String>,
    val growth_trend: String
)

data class ContentSuggestion(
    val type: String,
    val title: String,
    val description: String,
    val confidence_score: Double
)

data class SecurityAudit(
    val audit_id: String,
    val event_type: String,
    val severity: String,
    val description: String,
    val risk_score: Double,
    val timestamp: String,
    val success: Boolean
)

data class FraudDetection(
    val fraud_id: String,
    val fraud_type: String,
    val status: String,
    val confidence_score: Double,
    val risk_level: String,
    val description: String,
    val detection_timestamp: String
)

data class SecurityAlert(
    val alert_id: String,
    val alert_type: String,
    val priority: String,
    val title: String,
    val description: String,
    val is_active: Boolean,
    val created_at: String
)

// MARK: - API Client
class CommuniConnectAPIClient {
    private val retrofit: Retrofit
    private val api: CommuniConnectAPI
    
    init {
        val okHttpClient = OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor())
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .build()
        
        retrofit = Retrofit.Builder()
            .baseUrl("https://api.communiconnect.com/")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        
        api = retrofit.create(CommuniConnectAPI::class.java)
    }
    
    fun getAPI(): CommuniConnectAPI = api
}

// MARK: - Auth Interceptor
class AuthInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        
        // Add auth token if available
        val token = TokenManager.getAccessToken()
        val newRequest = if (token != null) {
            originalRequest.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            originalRequest
        }
        
        val response = chain.proceed(newRequest)
        
        // Handle token refresh if needed
        if (response.code == 401) {
            TokenManager.refreshToken()
        }
        
        return response
    }
}

// MARK: - Token Manager
object TokenManager {
    private const val PREFS_NAME = "CommuniConnectPrefs"
    private const val KEY_ACCESS_TOKEN = "access_token"
    private const val KEY_REFRESH_TOKEN = "refresh_token"
    private const val KEY_TOKEN_EXPIRY = "token_expiry"
    
    private val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    
    fun saveTokens(accessToken: String, refreshToken: String, expiresIn: Int) {
        val expiryTime = System.currentTimeMillis() + (expiresIn * 1000L)
        prefs.edit()
            .putString(KEY_ACCESS_TOKEN, accessToken)
            .putString(KEY_REFRESH_TOKEN, refreshToken)
            .putLong(KEY_TOKEN_EXPIRY, expiryTime)
            .apply()
    }
    
    fun getAccessToken(): String? {
        val token = prefs.getString(KEY_ACCESS_TOKEN, null)
        val expiry = prefs.getLong(KEY_TOKEN_EXPIRY, 0)
        
        return if (token != null && System.currentTimeMillis() < expiry) {
            token
        } else {
            null
        }
    }
    
    fun getRefreshToken(): String? {
        return prefs.getString(KEY_REFRESH_TOKEN, null)
    }
    
    fun clearTokens() {
        prefs.edit()
            .remove(KEY_ACCESS_TOKEN)
            .remove(KEY_REFRESH_TOKEN)
            .remove(KEY_TOKEN_EXPIRY)
            .apply()
    }
    
    fun refreshToken() {
        val refreshToken = getRefreshToken()
        if (refreshToken != null) {
            // Implement token refresh logic
        }
    }
}

// MARK: - Repository Pattern
class CommuniConnectRepository(private val api: CommuniConnectAPI) {
    
    // Authentication
    suspend fun login(email: String, password: String): Result<LoginResponse> {
        return try {
            val response = api.login(LoginRequest(email, password))
            if (response.isSuccessful) {
                response.body()?.let { loginResponse ->
                    TokenManager.saveTokens(
                        loginResponse.access_token,
                        loginResponse.refresh_token,
                        loginResponse.expires_in
                    )
                }
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Login failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun register(request: RegisterRequest): Result<RegisterResponse> {
        return try {
            val response = api.register(request)
            if (response.isSuccessful) {
                response.body()?.let { registerResponse ->
                    TokenManager.saveTokens(
                        registerResponse.access_token,
                        registerResponse.refresh_token,
                        registerResponse.expires_in
                    )
                }
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Registration failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun logout(): Result<Unit> {
        return try {
            val response = api.logout()
            TokenManager.clearTokens()
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Logout failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Posts
    suspend fun getPosts(page: Int = 1, limit: Int = 20): Result<PostsResponse> {
        return try {
            val response = api.getPosts(page, limit)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to load posts"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun createPost(request: CreatePostRequest): Result<Post> {
        return try {
            val response = api.createPost(request)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to create post"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun likePost(postId: String): Result<LikeResponse> {
        return try {
            val response = api.likePost(postId)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to like post"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Notifications
    suspend fun getNotifications(page: Int = 1, limit: Int = 20): Result<NotificationsResponse> {
        return try {
            val response = api.getNotifications(page, limit)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to load notifications"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Analytics
    suspend fun getAnalyticsDashboard(): Result<AnalyticsDashboard> {
        return try {
            val response = api.getAnalyticsDashboard()
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to load analytics"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // AI Recommendations
    suspend fun getAIRecommendations(): Result<AIRecommendations> {
        return try {
            val response = api.getAIRecommendations()
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to load recommendations"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Security
    suspend fun auditSecurityEvent(request: SecurityAuditRequest): Result<SecurityAudit> {
        return try {
            val response = api.auditSecurityEvent(request)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to audit security event"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getSecurityDashboard(): Result<SecurityDashboard> {
        return try {
            val response = api.getSecurityDashboard()
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to load security dashboard"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
} 