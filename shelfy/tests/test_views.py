import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
import json

# Import from shelfy app instead of media
from shelfy.views import MediaAPI


class MediaAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = MediaAPI.as_view()
        
    @patch('shelfy.views.requests.get')
    def test_search_all_media_types(self, mock_get):
        """Test searching across all media types."""
        # Mock responses for each media type
        mock_responses = {
            'https://www.googleapis.com/books/v1/volumes': {
                'items': [{
                    'id': 'book123',
                    'volumeInfo': {
                        'title': 'Test Book',
                        'description': 'A test book',
                        'publishedDate': '2020-01-01',
                        'categories': ['Fiction'],
                        'authors': ['Author Name'],
                        'imageLinks': {'thumbnail': 'http://example.com/book.jpg'}
                    }
                }]
            },
            'https://api.themoviedb.org/3/search/movie': {
                'results': [{
                    'id': 456,
                    'title': 'Test Movie',
                    'overview': 'A test movie',
                    'release_date': '2020-02-02',
                    'poster_path': '/poster.jpg'
                }]
            },
            'https://api.rawg.io/api/games': {
                'results': [{
                    'id': 789,
                    'name': 'Test Game',
                    'background_image': 'http://example.com/game.jpg',
                    'released': '2020-03-03'
                }]
            }
        }
        
        # Configure the mock to return different responses for different URLs
        def side_effect(url, params=None):
            mock_response = MagicMock()
            mock_response.status_code = 200
            if url in mock_responses:
                mock_response.json.return_value = mock_responses[url]
            else:
                mock_response.json.return_value = {}
            return mock_response
            
        mock_get.side_effect = side_effect
        
        # Make the request
        request = self.factory.get('/api/media/search?q=test')
        response = self.view(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('results', content)
        
        # Verify we have results from all media types
        results = content['results']
        self.assertEqual(len(results), 3)
        
        # Check if we have one of each media type
        media_types = [item['media_type'] for item in results]
        self.assertIn('book', media_types)
        self.assertIn('movie', media_types)
        self.assertIn('game', media_types)
        
    @patch('shelfy.views.requests.get')
    def test_search_specific_media_type(self, mock_get):
        """Test searching for a specific media type."""
        # Mock book response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [{
                'id': 'book123',
                'volumeInfo': {
                    'title': 'Test Book',
                    'description': 'A test book',
                    'publishedDate': '2020-01-01',
                    'categories': ['Fiction'],
                    'authors': ['Author Name'],
                    'imageLinks': {'thumbnail': 'http://example.com/book.jpg'}
                }
            }]
        }
        mock_get.return_value = mock_response
        
        # Make the request
        request = self.factory.get('/api/media/book?q=test')
        response = self.view(request, media_type='book')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('results', content)
        
        # Verify we only have book results
        results = content['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['media_type'], 'book')
        self.assertEqual(results[0]['title'], 'Test Book')
        
    @patch('shelfy.views.requests.get')
    def test_get_media_details(self, mock_get):
        """Test getting details for a specific media item."""
        # Mock movie details response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 456,
            'title': 'Test Movie',
            'overview': 'A test movie',
            'release_date': '2020-02-02',
            'poster_path': '/poster.jpg',
            'genres': [{'id': 1, 'name': 'Action'}, {'id': 2, 'name': 'Drama'}],
            'credits': {
                'crew': [{'name': 'Director Name', 'job': 'Director'}]
            }
        }
        mock_get.return_value = mock_response
        
        # Make the request
        request = self.factory.get('/api/media/movie/456')
        response = self.view(request, media_type='movie', external_id='456')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        
        # Verify the details
        self.assertEqual(content['title'], 'Test Movie')
        self.assertEqual(content['release_year'], '2020')
        self.assertEqual(content['genre'], 'Action, Drama')
        self.assertEqual(content['director'], 'Director Name')
        
    @patch('shelfy.views.requests.get')
    def test_media_details_not_found(self, mock_get):
        """Test getting details for a non-existent media item."""
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Make the request
        request = self.factory.get('/api/media/book/nonexistent')
        response = self.view(request, media_type='book', external_id='nonexistent')
        
        # Check response
        self.assertEqual(response.status_code, 200)  # The view returns 200 with error message
        content = json.loads(response.content)
        self.assertIn('error', content)
        self.assertEqual(content['error'], 'Book not found')
        
    def test_search_without_query(self):
        """Test search without providing a query parameter."""
        request = self.factory.get('/api/media/search')
        response = self.view(request)
        
        # Check response
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertIn('error', content)
        self.assertEqual(content['error'], "Query parameter 'q' is required.")
        
    def test_invalid_media_type(self):
        """Test getting details with an invalid media type."""
        request = self.factory.get('/api/media/invalid/123')
        response = self.view(request, media_type='invalid', external_id='123')
        
        # Check response
        self.assertEqual(response.status_code, 200)  # The view returns 200 with error message
        content = json.loads(response.content)
        self.assertIn('error', content)
        self.assertEqual(content['error'], 'Invalid media type')


if __name__ == '__main__':
    unittest.main()