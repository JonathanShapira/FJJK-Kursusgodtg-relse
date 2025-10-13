from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile, Kursus
import json


class KursusTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test kursus
        self.kursus = Kursus.objects.create(
            user=self.user,
            kursus='Test Kursus',
            sted='Test Sted',
            arrangor='Test Arrangør',
            pris=100.00,
            date='2024-01-15'
        )

    def test_kursus_list_view(self):
        """Test that kursus list view returns correct data"""
        response = self.client.get('/api/kursus/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['kursus'], 'Test Kursus')
        self.assertEqual(data[0]['sted'], 'Test Sted')
        self.assertEqual(data[0]['arrangor'], 'Test Arrangør')
        self.assertEqual(float(data[0]['pris']), 100.00)
        self.assertEqual(data[0]['date'], '2024-01-15')

    def test_kursus_create_view_without_file_fails(self):
        """Test creating a new kursus without file fails"""
        kursus_data = {
            'kursus': 'New Kursus',
            'sted': 'New Sted',
            'arrangor': 'New Arrangør',
            'pris': 200.00,
            'date': '2024-02-15'
        }
        
        response = self.client.post(
            '/api/kursus/create/',
            data=json.dumps(kursus_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('file', data)

    def test_kursus_create_with_file(self):
        """Test creating kursus with file upload"""
        test_file = SimpleUploadedFile(
            "test_file.txt",
            b"file content",
            content_type="text/plain"
        )
        
        kursus_data = {
            'kursus': 'Kursus with File',
            'sted': 'File Sted',
            'arrangor': 'File Arrangør',
            'pris': 150.00,
            'date': '2024-03-15',
            'file': test_file
        }
        
        response = self.client.post('/api/kursus/create/', data=kursus_data)
        self.assertEqual(response.status_code, 201)
        
        data = response.json()
        self.assertEqual(data['kursus'], 'Kursus with File')
        self.assertIsNotNone(data['filename'])
        
        # Verify kursus was created in database
        kursus = Kursus.objects.get(kursus='Kursus with File')
        self.assertEqual(kursus.user, self.user)
        self.assertEqual(kursus.sted, 'File Sted')
        self.assertEqual(kursus.arrangor, 'File Arrangør')
        self.assertEqual(float(kursus.pris), 150.00)
        self.assertTrue(kursus.file)

    def test_kursus_update_view(self):
        """Test updating a kursus"""
        update_data = {
            'kursus': 'Updated Kursus',
            'sted': 'Updated Sted',
            'arrangor': 'Updated Arrangør',
            'pris': 300.00,
            'date': '2024-04-15'
        }
        
        response = self.client.patch(
            f'/api/kursus/{self.kursus.id}/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['kursus'], 'Updated Kursus')
        self.assertEqual(data['sted'], 'Updated Sted')

    def test_kursus_delete_view(self):
        """Test deleting a kursus"""
        response = self.client.delete(f'/api/kursus/{self.kursus.id}/delete/')
        self.assertEqual(response.status_code, 204)
        
        # Verify kursus is deleted
        self.assertFalse(Kursus.objects.filter(id=self.kursus.id).exists())

    def test_kursus_page_view(self):
        """Test that kursus page loads correctly"""
        response = self.client.get('/kursus/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kursus Management')

    def test_kursus_page_requires_login(self):
        """Test that kursus page requires authentication"""
        self.client.logout()
        response = self.client.get('/kursus/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_can_only_see_own_kursus(self):
        """Test that users can only see their own kursus records"""
        # Create another user and kursus
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        Kursus.objects.create(
            user=other_user,
            kursus='Other User Kursus',
            sted='Other Sted',
            arrangor='Other Arrangør',
            pris=500.00
        )
        
        # Test that current user only sees their own kursus
        response = self.client.get('/api/kursus/')
        data = response.json()
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['kursus'], 'Test Kursus')
        self.assertNotEqual(data[0]['kursus'], 'Other User Kursus')


class KursusPageTestCase(TestCase):
    def setUp(self):
        """Set up test data for page tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_kursus_page_template(self):
        """Test that kursus page uses correct template"""
        response = self.client.get('/kursus/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/kursus.html')

    def test_kursus_page_contains_form(self):
        """Test that kursus page contains the form"""
        response = self.client.get('/kursus/')
        self.assertContains(response, 'Add New Kursus')
        self.assertContains(response, 'name="kursus"')
        self.assertContains(response, 'name="sted"')
        self.assertContains(response, 'name="arrangor"')
        self.assertContains(response, 'name="pris"')
        self.assertContains(response, 'name="file"')
        self.assertContains(response, 'required')  # File field should be required

    def test_kursus_page_contains_grid(self):
        """Test that kursus page contains grid view"""
        response = self.client.get('/kursus/')
        self.assertContains(response, 'kursus-grid')
        self.assertContains(response, 'grid-item')


class ProfilePageTestCase(TestCase):
    def setUp(self):
        """Set up test data for profile page tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_profile_page_contains_kursus_grid(self):
        """Test that profile page shows kursus grid view"""
        # Create some kursus records
        Kursus.objects.create(
            user=self.user,
            kursus='Test Kursus 1',
            sted='Test Sted 1',
            arrangor='Test Arrangør 1',
            pris=100.00
        )
        Kursus.objects.create(
            user=self.user,
            kursus='Test Kursus 2',
            sted='Test Sted 2',
            arrangor='Test Arrangør 2',
            pris=200.00
        )
        
        response = self.client.get('/profile/profile-page/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'kursus-grid')
        self.assertContains(response, 'Test Kursus 1')
        self.assertContains(response, 'Test Kursus 2')

    def test_profile_page_no_kursus_form(self):
        """Test that profile page doesn't contain kursus form"""
        response = self.client.get('/profile/profile-page/')
        self.assertNotContains(response, 'Add New Kursus')
        self.assertNotContains(response, 'name="kursus"')
