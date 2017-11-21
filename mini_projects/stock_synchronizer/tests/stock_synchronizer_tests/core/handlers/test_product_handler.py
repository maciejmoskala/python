import pytest
from unittest import mock
from stock_synchronizer.core.handlers.product_handler import ProductHandler


class TestProductHandler:

    default_stock = 10

    @pytest.fixture
    def product_handler(self):
        return ProductHandler()

    @pytest.fixture
    def parent_id(self):
        return 1

    @pytest.yield_fixture
    def mocked_send_output_message(self):
        function_directory = (
            'stock_synchronizer.core.handlers.'
            'product_handler.ProductHandler._send_output_message')
        with mock.patch(function_directory):
            yield

    def test_create_product(self, product_handler, parent_id):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        assert product_handler.products[parent_id] is not None

    def test_create_for_existing_product(self, product_handler, parent_id):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        with pytest.raises(Exception):
            product_handler.create_product(
                id=parent_id,
                parent_id=None,
                stock=self.default_stock,
            )

    def test_create_product_with_parent(self, product_handler, parent_id):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        child_id = parent_id+1
        product_handler.create_product(
            id=child_id,
            parent_id=parent_id,
            stock=self.default_stock,
        )
        assert product_handler.products[parent_id] is not None
        assert product_handler.products[child_id] is not None

    def test_create_product_with_not_existing_parent(
            self, product_handler, parent_id):
        wrong_parent_id = parent_id+1
        with pytest.raises(Exception):
            product_handler.create_product(
                id=parent_id,
                parent_id=wrong_parent_id,
                stock=self.default_stock,
            )

    def test_end_product(self, product_handler, parent_id):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        assert product_handler.products[parent_id].is_active is True
        product_handler.end_product(
            id=parent_id,
        )
        assert product_handler.products[parent_id].is_active is False

    def test_end_parent_product(
            self, product_handler, parent_id, mocked_send_output_message):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        child_id = parent_id+1
        product_handler.create_product(
            id=child_id,
            parent_id=parent_id,
            stock=self.default_stock,
        )
        product_handler.end_product(
            id=parent_id,
        )
        assert product_handler.products[parent_id].is_active is False
        assert product_handler.products[child_id].is_active is False

    def test_end_child_product(self, product_handler, parent_id):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        child_id = parent_id+1
        product_handler.create_product(
            id=child_id,
            parent_id=parent_id,
            stock=self.default_stock,
        )
        product_handler.end_product(
            id=child_id,
        )
        assert product_handler.products[parent_id].is_active is True
        assert product_handler.products[child_id].is_active is False

    def test_update_product(self, product_handler, parent_id):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        new_stock = self.default_stock-1
        product_handler.update_product(
            id=parent_id,
            stock=new_stock,
        )
        assert product_handler.products[parent_id].stock == new_stock

    def test_update_children_product(
            self, product_handler, parent_id, mocked_send_output_message):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        child_id = parent_id+1
        product_handler.create_product(
            id=child_id,
            parent_id=parent_id,
            stock=self.default_stock,
        )

        new_stock = self.default_stock-1
        product_handler.update_product(
            id=child_id,
            stock=new_stock,
        )
        assert product_handler.products[parent_id].stock == new_stock
        assert product_handler.products[child_id].stock == new_stock

    def test_update_parent_end_child_product(
            self, product_handler, parent_id, mocked_send_output_message):
        product_handler.create_product(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )
        child_id = parent_id+1
        product_handler.create_product(
            id=child_id,
            parent_id=parent_id,
            stock=self.default_stock,
        )

        new_stock = 0
        product_handler.update_product(
            id=parent_id,
            stock=new_stock,
        )
        assert product_handler.products[parent_id].stock == new_stock
        assert product_handler.products[child_id].stock != new_stock
        assert product_handler.products[child_id].is_active is False
