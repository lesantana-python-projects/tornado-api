from tornado.httpclient import HTTPClientError
from tests.unit.weather import BaseTests
from weather.services.paginator import paginate
import mock


class TestPaginator(BaseTests):

    def test_paginate_page_greater_or_equal_zero(self):
        with self.assertRaises(HTTPClientError) as context:
            paginate('', page=0, page_size=1)
        self.assertEqual(context.exception.message, 'page needs to be >= 1')

    def test_paginate_page_size_greater_or_equal_zero(self):
        with self.assertRaises(HTTPClientError) as context:
            paginate('', page=1, page_size=0)
        self.assertEqual(context.exception.message, 'page_size needs to be >= 1')

    def test_paginate_success_return_value(self):
        mock_param = mock.MagicMock(
            order_by=mock.MagicMock(return_value=mock.MagicMock(count=mock.MagicMock(return_value=300))))
        response = paginate(mock_param, page=2, page_size=10)
        self.assertTrue(hasattr(response, 'has_next'))
        self.assertTrue(hasattr(response, 'has_previous'))
        self.assertTrue(hasattr(response, 'items'))
        self.assertTrue(hasattr(response, 'next_page'))
        self.assertTrue(hasattr(response, 'previous_page'))
        self.assertTrue(hasattr(response, 'total'))
