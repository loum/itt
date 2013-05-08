from django.test import TransactionTestCase

from itt.control.common.models import CommonModel


class TestCommonModel(TransactionTestCase):

    def test_init(self):
        """Test initialisation of the CommonModel model.
        """
        cm = CommonModel()
        msg = 'Object is not a CommonModel'
        self.assertIsInstance(cm, CommonModel, msg)

    def test_get_fields_at_the_base_level(self):
        """Test the get_fields method at the base class level.
        """
        cm = CommonModel()
        msg = 'get_fields at base level should return empty dictionary'
        self.assertEqual(cm.get_fields(), {}, msg)
