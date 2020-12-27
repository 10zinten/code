from datetime import date, timedelta

import pytest

from model import Batch, OrderLine, OutOfStock, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_perfers_current_stocke_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    sku = "MINIMALIST-SPOON"
    earliest = Batch("speedy-batch", sku, 100, eta=today)
    medium = Batch("normal-batch", sku, 100, eta=tomorrow)
    latest = Batch("speedy-batch", sku, 100, eta=later)
    line = OrderLine("order1", sku, 10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_returns_allocated_batch_ref():
    sku = "HIGHBROW-POSTER"
    in_stock_batch = Batch("in-stock-batch-ref", sku, 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", sku, 100, eta=tomorrow)
    line = OrderLine("oref", sku, 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference

def test_raise_out_of_stock_exception_if_cannot_allocate():
    sku = "SMALL-FORK"
    batch = Batch("batch1", sku, 10, eta=today)
    line = OrderLine("order1", sku, 10)
    allocate(line, [batch])

    with pytest.raises(OutOfStock, match=sku):
        line = OrderLine("order1", sku, 1)
        allocate(line, [batch])

