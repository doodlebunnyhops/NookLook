"""UI components for the ACNH bot

This package organizes Discord UI views by functionality:
- base: Foundation classes with shared behavior (user restrictions, timeouts, refresh logic)
- common: Shared UI components (refresh buttons, Nookipedia views, utilities)
- item_views: Item variant selection interfaces
- detail_views: Entity detail views (villagers, critters)
- search_views: Search result display and navigation
- pagination: Paginated browsing views for items and critters
"""

# Base classes
from .base import (
    UserRestrictedView,
    MessageTrackingMixin,
    TimeoutPreservingView,
    RefreshableView
)

# Common components
from .common import (
    RefreshImagesButton,
    RefreshableStaticView,
    NookipediaView,
    get_nookipedia_view,
    get_combined_view
)

# Item variant views
from .item_views import (
    VariantSelectView,
    VariantSelect,
    ColorSelect,
    PatternSelect
)

# Detail views
from .detail_views import (
    VillagerDetailsView,
    CritterAvailabilityView
)

# Search result views
from .search_views import (
    SearchResultsView,
    PaginatedResultView
)

# Pagination views
from .pagination import (
    PaginationView,
    ItemsPaginationView,
    CrittersPaginationView
)

__all__ = [
    # Base classes
    'UserRestrictedView',
    'MessageTrackingMixin',
    'TimeoutPreservingView',
    'RefreshableView',
    
    # Common components
    'RefreshImagesButton',
    'RefreshableStaticView',
    'NookipediaView',
    'get_nookipedia_view',
    'get_combined_view',
    
    # Item variant views
    'VariantSelectView',
    'VariantSelect',
    'ColorSelect',
    'PatternSelect',
    
    # Detail views
    'VillagerDetailsView',
    'CritterAvailabilityView',
    
    # Search result views
    'SearchResultsView',
    'PaginatedResultView',
    
    # Pagination views
    'PaginationView',
    'ItemsPaginationView',
    'CrittersPaginationView'
]
