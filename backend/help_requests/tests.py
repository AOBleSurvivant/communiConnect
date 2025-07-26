from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import HelpRequest, HelpResponse, HelpRequestCategory

User = get_user_model()


class HelpRequestModelTest(TestCase):
    """Tests pour le modèle HelpRequest"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = HelpRequestCategory.objects.create(
            name='Test Category',
            icon='🤝',
            color='blue',
            description='Test category description'
        )
    
    def test_create_help_request(self):
        """Test de création d'une demande d'aide"""
        help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Test Help Request',
            description='This is a test help request',
            latitude=Decimal('9.5370'),
            longitude=Decimal('-13.6785'),
            city='Conakry',
            duration_type='this_week'
        )
        
        self.assertEqual(help_request.title, 'Test Help Request')
        self.assertEqual(help_request.author, self.user)
        self.assertEqual(help_request.status, 'open')
        self.assertFalse(help_request.is_urgent)
        self.assertIsNotNone(help_request.id)
    
    def test_help_request_str(self):
        """Test de la méthode __str__"""
        help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Test Help Request',
            description='This is a test help request',
            duration_type='this_week'
        )
        
        expected_str = f"Demande d'aide - Test Help Request (testuser)"
        self.assertEqual(str(help_request), expected_str)
    
    def test_help_request_properties(self):
        """Test des propriétés du modèle"""
        help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Test Help Request',
            description='This is a test help request',
            latitude=Decimal('9.5370'),
            longitude=Decimal('-13.6785'),
            address='123 Test Street',
            city='Conakry',
            duration_type='this_week'
        )
        
        # Test location_display
        self.assertEqual(help_request.location_display, '123 Test Street')
        
        # Test time_ago
        self.assertIn('à l\'instant', help_request.time_ago)
        
        # Test duration_display
        self.assertEqual(help_request.duration_display, 'Cette semaine')
        
        # Test is_expired (non expirée)
        self.assertFalse(help_request.is_expired)
        
        # Test is_expired (expirée)
        help_request.expires_at = timezone.now() - timedelta(days=1)
        help_request.save()
        self.assertTrue(help_request.is_expired)
    
    def test_help_request_increment_views(self):
        """Test de l'incrémentation des vues"""
        help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Test Help Request',
            description='This is a test help request',
            duration_type='this_week'
        )
        
        initial_views = help_request.views_count
        help_request.increment_views()
        help_request.refresh_from_db()
        
        self.assertEqual(help_request.views_count, initial_views + 1)
    
    def test_help_request_increment_responses(self):
        """Test de l'incrémentation des réponses"""
        help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Test Help Request',
            description='This is a test help request',
            duration_type='this_week'
        )
        
        initial_responses = help_request.responses_count
        help_request.increment_responses()
        help_request.refresh_from_db()
        
        self.assertEqual(help_request.responses_count, initial_responses + 1)


class HelpResponseModelTest(TestCase):
    """Tests pour le modèle HelpResponse"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.helper_user = User.objects.create_user(
            username='helperuser',
            email='helper@example.com',
            password='testpass123'
        )
        
        self.help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Test Help Request',
            description='This is a test help request',
            duration_type='this_week'
        )
    
    def test_create_help_response(self):
        """Test de création d'une réponse"""
        response = HelpResponse.objects.create(
            help_request=self.help_request,
            author=self.helper_user,
            response_type='offer_help',
            message='I can help you with this'
        )
        
        self.assertEqual(response.help_request, self.help_request)
        self.assertEqual(response.author, self.helper_user)
        self.assertEqual(response.response_type, 'offer_help')
        self.assertFalse(response.is_accepted)
        self.assertFalse(response.is_rejected)
    
    def test_help_response_str(self):
        """Test de la méthode __str__"""
        response = HelpResponse.objects.create(
            help_request=self.help_request,
            author=self.helper_user,
            response_type='offer_help',
            message='I can help you with this'
        )
        
        expected_str = f"Réponse de helperuser à Test Help Request"
        self.assertEqual(str(response), expected_str)
    
    def test_help_response_accept(self):
        """Test de l'acceptation d'une réponse"""
        response = HelpResponse.objects.create(
            help_request=self.help_request,
            author=self.helper_user,
            response_type='offer_help',
            message='I can help you with this'
        )
        
        initial_responses_count = self.help_request.responses_count
        
        response.accept()
        response.refresh_from_db()
        self.help_request.refresh_from_db()
        
        self.assertTrue(response.is_accepted)
        self.assertFalse(response.is_rejected)
        self.assertEqual(self.help_request.responses_count, initial_responses_count + 1)
    
    def test_help_response_reject(self):
        """Test du rejet d'une réponse"""
        response = HelpResponse.objects.create(
            help_request=self.help_request,
            author=self.helper_user,
            response_type='offer_help',
            message='I can help you with this'
        )
        
        response.reject()
        response.refresh_from_db()
        
        self.assertTrue(response.is_rejected)
        self.assertFalse(response.is_accepted)


class HelpRequestCategoryModelTest(TestCase):
    """Tests pour le modèle HelpRequestCategory"""
    
    def test_create_category(self):
        """Test de création d'une catégorie"""
        category = HelpRequestCategory.objects.create(
            name='Test Category',
            icon='🤝',
            color='blue',
            description='Test category description',
            order=1
        )
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.icon, '🤝')
        self.assertEqual(category.color, 'blue')
        self.assertTrue(category.is_active)
        self.assertEqual(category.order, 1)
    
    def test_category_str(self):
        """Test de la méthode __str__"""
        category = HelpRequestCategory.objects.create(
            name='Test Category',
            icon='🤝',
            color='blue'
        )
        
        self.assertEqual(str(category), 'Test Category')


class HelpRequestIntegrationTest(TestCase):
    """Tests d'intégration pour les demandes d'aide"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.helper_user = User.objects.create_user(
            username='helperuser',
            email='helper@example.com',
            password='testpass123'
        )
    
    def test_complete_help_request_flow(self):
        """Test du flux complet d'une demande d'aide"""
        # 1. Créer une demande d'aide
        help_request = HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Need help moving furniture',
            description='I need help moving some furniture this weekend',
            latitude=Decimal('9.5370'),
            longitude=Decimal('-13.6785'),
            city='Conakry',
            duration_type='this_week',
            estimated_hours=2
        )
        
        self.assertEqual(help_request.status, 'open')
        self.assertEqual(help_request.responses_count, 0)
        
        # 2. Quelqu'un répond à la demande
        response = HelpResponse.objects.create(
            help_request=help_request,
            author=self.helper_user,
            response_type='offer_help',
            message='I can help you move the furniture on Saturday'
        )
        
        # 3. L'auteur accepte la réponse
        response.accept()
        response.refresh_from_db()
        help_request.refresh_from_db()
        
        self.assertTrue(response.is_accepted)
        self.assertEqual(help_request.responses_count, 1)
        
        # 4. Marquer la demande comme terminée
        help_request.status = 'completed'
        help_request.save()
        
        self.assertEqual(help_request.status, 'completed')
    
    def test_help_request_filtering(self):
        """Test du filtrage des demandes d'aide"""
        # Créer plusieurs demandes avec différents types
        HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='material',
            for_who='myself',
            title='Need tools',
            description='I need to borrow some tools',
            duration_type='immediate'
        )
        
        HelpRequest.objects.create(
            author=self.user,
            request_type='offer',
            need_type='transport',
            for_who='community',
            title='Can provide transport',
            description='I can provide transport for community events',
            duration_type='ongoing'
        )
        
        HelpRequest.objects.create(
            author=self.user,
            request_type='request',
            need_type='technical',
            for_who='myself',
            title='Need computer help',
            description='I need help with my computer',
            duration_type='this_month',
            is_urgent=True
        )
        
        # Test filtrage par type de demande
        requests = HelpRequest.objects.filter(request_type='request')
        self.assertEqual(requests.count(), 2)
        
        offers = HelpRequest.objects.filter(request_type='offer')
        self.assertEqual(offers.count(), 1)
        
        # Test filtrage par urgence
        urgent_requests = HelpRequest.objects.filter(is_urgent=True)
        self.assertEqual(urgent_requests.count(), 1)
        
        # Test filtrage par type de besoin
        material_requests = HelpRequest.objects.filter(need_type='material')
        self.assertEqual(material_requests.count(), 1)
        
        # Test filtrage par durée
        immediate_requests = HelpRequest.objects.filter(duration_type='immediate')
        self.assertEqual(immediate_requests.count(), 1) 