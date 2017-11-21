import pytest
from stock_synchronizer.core.models.product import Product


class TestProductModel:

    @pytest.fixture
    def product(self):
        return Product(
            id=1,
            parent_id=None,
            stock=10
        )

    def test_update_stock(self, product):
        old_stock = product.stock
        new_stock = old_stock+1
        product.update_stock(new_stock)
        assert product.stock != old_stock

    def test_deactivate(self, product):
        assert product.is_active is True
        product.deactivate()
        assert product.is_active is False
