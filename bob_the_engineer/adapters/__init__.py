"""Adapters for different coding agents."""

from .base import BaseAdapter
from .factory import AdapterFactory

__all__ = ["AdapterFactory", "BaseAdapter"]
