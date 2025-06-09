"""
Data Models and DTOs for API layer
Defines the structure of data exchanged between API and database
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class CompanyInfo:
    """Company Information data model"""
    company_code: str
    company_name: Optional[str] = None
    city_code: Optional[str] = None
    company_address: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    subscription_code: Optional[str] = None
    last_payment: Optional[str] = None
    subscription_duration: Optional[str] = None
    registration_date: Optional[str] = None
    descriptions: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database operations"""
        return {
            'Companyco': self.company_code,
            'Companyna': self.company_name,
            'Cityco': self.city_code,
            'Caddress': self.company_address,
            'Cophoneno': self.phone_number,
            'Username': self.username,
            'Password': self.password,
            'SubscriptionTCode': self.subscription_code,
            'Lastpayment': self.last_payment,
            'Subscriptionduration': self.subscription_duration,
            'Registrationdate': self.registration_date,
            'descriptions': self.descriptions
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompanyInfo':
        """Create instance from database row"""
        return cls(
            company_code=data.get('Companyco', ''),
            company_name=data.get('Companyna'),
            city_code=data.get('Cityco'),
            company_address=data.get('Caddress'),
            phone_number=data.get('Cophoneno'),
            username=data.get('Username'),
            password=data.get('Password'),
            subscription_code=data.get('SubscriptionTCode'),
            last_payment=data.get('Lastpayment'),
            subscription_duration=data.get('Subscriptionduration'),
            registration_date=data.get('Registrationdate'),
            descriptions=data.get('descriptions')
        )


@dataclass
class MainCode:
    """Main Code data model"""
    record_type: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database operations"""
        return {
            'Recty': self.record_type,
            'Code': self.code,
            'Name': self.name,
            'Description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MainCode':
        """Create instance from database row"""
        return cls(
            record_type=data.get('Recty'),
            code=data.get('Code'),
            name=data.get('Name'),
            description=data.get('Description')
        )


@dataclass
class ApiResponse:
    """Standard API response format"""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None
    count: Optional[int] = None

    @classmethod
    def success_response(cls, data: Any = None, message: str = "Operation successful", count: Optional[int] = None) -> 'ApiResponse':
        """Create success response"""
        return cls(success=True, data=data, message=message, count=count)

    @classmethod
    def error_response(cls, error: str, message: str = "Operation failed") -> 'ApiResponse':
        """Create error response"""
        return cls(success=False, error=error, message=message)


# Validation schemas
COMPANY_INFO_REQUIRED_FIELDS = ['company_code']
COMPANY_INFO_OPTIONAL_FIELDS = [
    'company_name', 'city_code', 'company_address', 'phone_number',
    'username', 'password', 'subscription_code', 'last_payment',
    'subscription_duration', 'registration_date', 'descriptions'
]

MAIN_CODE_FIELDS = ['record_type', 'code', 'name', 'description']
