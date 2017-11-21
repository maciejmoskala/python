import pytest
from unittest import mock

class TestProductRpc:

    default_stock = 10

    @pytest.fixture
    def parent_id(self):
        return 1

    @pytest.yield_fixture
    def mocked_send_output_message(self):
        with mock.patch('stock_synchronizer.core.rpc.product.PRODUCT_HANDLER'):
            yield

    def test_product_created_with_none_parent_id(self, parent_id, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductCreated

        ProductCreated(
            id=parent_id,
            parent_id=None,
            stock=self.default_stock,
        )

    def test_product_created_with_none_id(self, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductCreated

        with pytest.raises(Exception):
            ProductCreated(
                id=None,
                parent_id=None,
                stock=self.default_stock,
            )

    def test_product_created_with_none_stock(self, parent_id, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductCreated

        with pytest.raises(Exception):
            ProductCreated(
                id=parent_id,
                parent_id=None,
                stock=None,
            )

    def test_product_updated(self, parent_id, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductUpdated

        ProductUpdated(
            id=parent_id,
            stock=self.default_stock,
        )

    def test_product_updated_with_none_id(self, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductUpdated

        with pytest.raises(Exception):
            ProductUpdated(
                id=None,
                stock=self.default_stock,
            )

    def test_product_updated_with_none_stock(self, parent_id, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductUpdated

        with pytest.raises(Exception):
            ProductUpdated(
                id=parent_id,
                stock=None,
            )

    def test_product_ended(self, parent_id, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductEnded

        ProductEnded(
            id=parent_id,
        )

    def test_product_ended_with_none_id(self, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import ProductEnded

        with pytest.raises(Exception):
            ProductEnded(
                id=None,
            )

    def test_summary(self, parent_id, mocked_send_output_message):
        from stock_synchronizer.core.rpc.product import Summary

        Summary()
