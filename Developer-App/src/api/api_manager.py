"""
API Manager - Central API access point
Provides unified access to all API operations
"""

from typing import Optional
from kivy.logger import Logger

from ..core.database import DatabaseManager
from .company_api import CompanyInfoAPI
from .maincode_api import MainCodeAPI
from .models import ApiResponse


class APIManager:
    """Central API Manager for all database operations"""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager()
        self._company_api = None
        self._maincode_api = None
        self._initialized = False

    def initialize(self) -> ApiResponse:
        """Initialize API manager and database connection"""
        try:
            if not self.db_manager.is_connected():
                if not self.db_manager.connect():
                    return ApiResponse.error_response("Failed to connect to database")

            # Initialize API instances
            self._company_api = CompanyInfoAPI(self.db_manager)
            self._maincode_api = MainCodeAPI(self.db_manager)

            self._initialized = True
            Logger.info("API Manager initialized successfully")

            return ApiResponse.success_response(
                message="API Manager initialized successfully"
            )

        except Exception as e:
            error_msg = f"Failed to initialize API Manager: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    @property
    def company(self) -> CompanyInfoAPI:
        """Get Company API instance"""
        if not self._initialized:
            raise RuntimeError("API Manager not initialized. Call initialize() first.")
        return self._company_api

    @property
    def maincode(self) -> MainCodeAPI:
        """Get MainCode API instance"""
        if not self._initialized:
            raise RuntimeError("API Manager not initialized. Call initialize() first.")
        return self._maincode_api

    def is_initialized(self) -> bool:
        """Check if API manager is initialized"""
        return self._initialized

    def test_connection(self) -> ApiResponse:
        """Test database connection"""
        try:
            if not self._initialized:
                return ApiResponse.error_response("API Manager not initialized")

            if self.db_manager.test_connection():
                return ApiResponse.success_response(
                    message="Database connection is healthy"
                )
            else:
                return ApiResponse.error_response("Database connection failed")

        except Exception as e:
            error_msg = f"Connection test failed: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_database_info(self) -> ApiResponse:
        """Get database information"""
        try:
            if not self._initialized:
                return ApiResponse.error_response("API Manager not initialized")

            db_info = self.db_manager.get_db_info()
            return ApiResponse.success_response(
                data=db_info,
                message="Database information retrieved"
            )

        except Exception as e:
            error_msg = f"Failed to get database info: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def reconnect(self) -> ApiResponse:
        """Reconnect to database"""
        try:
            if self.db_manager.reconnect():
                # Reinitialize API instances
                self._company_api = CompanyInfoAPI(self.db_manager)
                self._maincode_api = MainCodeAPI(self.db_manager)

                return ApiResponse.success_response(
                    message="Database reconnected successfully"
                )
            else:
                return ApiResponse.error_response("Failed to reconnect to database")

        except Exception as e:
            error_msg = f"Reconnection failed: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def close(self):
        """Close database connection and cleanup"""
        try:
            if self.db_manager:
                self.db_manager.close()

            self._company_api = None
            self._maincode_api = None
            self._initialized = False

            Logger.info("API Manager closed")

        except Exception as e:
            Logger.error(f"Error closing API Manager: {str(e)}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Global API manager instance (optional - for convenience)
_global_api_manager = None


def get_api_manager() -> APIManager:
    """Get global API manager instance (creates if needed)"""
    global _global_api_manager

    if _global_api_manager is None:
        _global_api_manager = APIManager()

    return _global_api_manager


def initialize_global_api() -> ApiResponse:
    """Initialize global API manager"""
    api_manager = get_api_manager()
    return api_manager.initialize()


def close_global_api():
    """Close global API manager"""
    global _global_api_manager

    if _global_api_manager:
        _global_api_manager.close()
        _global_api_manager = None
