#!/usr/bin/env python3
"""Illustrative per-order profit model; verify actual Etsy and payment fees."""
import math

def profit(price, production=0, shipping=0, packaging=0, listing_fee=0.20,
           transaction_rate=0.065, payment_rate=0, payment_fixed=0,
           ads=0, refund_reserve=0, other=0):
    values = locals()
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number")
        if value < 0:
            raise ValueError(f"{name} cannot be negative")
    if price == 0:
        raise ValueError("price must be positive")
    if transaction_rate > 1 or payment_rate > 1:
        raise ValueError("Rates must be fractions between 0 and 1")
    costs = production + shipping + packaging + listing_fee + price * (transaction_rate + payment_rate) + payment_fixed + ads + refund_reserve + other
    net_raw = price - costs
    margin_raw = net_raw / price * 100
    if not all(math.isfinite(x) for x in (costs, net_raw, margin_raw)):
        raise ValueError("Calculated amounts exceed the supported numeric range")
    return {"net_profit": round(net_raw, 2), "margin_percent": round(margin_raw, 2), "total_cost": round(costs, 2)}
