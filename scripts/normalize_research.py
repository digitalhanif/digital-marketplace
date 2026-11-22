#!/usr/bin/env python3
"""Normalize research records without inventing missing observations."""


def normalize(item):
    if not isinstance(item, dict):
        raise ValueError("Research record must be an object")
    product = item.get("product")
    if product is not None and not isinstance(product, str):
        raise ValueError("product must be text or null")
    confidence = item.get("confidence", "LOW")
    if confidence not in ("HIGH", "MEDIUM", "LOW"):
        raise ValueError("confidence must be HIGH, MEDIUM or LOW")
    return {
        "product": product.strip() if product is not None else "",
        "source_url": item.get("source_url"),
        "observed_at": item.get("observed_at"),
        "market": item.get("market", "USA"),
        "price_usd": item.get("price_usd"),
        "confidence": confidence,
        "notes": item.get("notes", ""),
    }
