"""
Company Information API
Handles all CRUD operations for the CompanyInfo table
"""

from typing import List, Optional, Dict, Any
from kivy.logger import Logger

from ..core.database import DatabaseManager
from .models import CompanyInfo, ApiResponse


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_required_string(value: Any, field_name: str) -> str:
    """Validate required string field"""
    if not value or not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} is required and must be a non-empty string")
    return value.strip()


def validate_optional_string(value: Any) -> Optional[str]:
    """Validate optional string field"""
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() if value.strip() else None
    return str(value).strip() if str(value).strip() else None


class CompanyInfoAPI:
    """API for Company Information operations"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_company(self, company_data: Dict[str, Any]) -> ApiResponse:
        """Create a new company record"""
        try:
            # Validate required fields
            if not company_data.get('company_code'):
                return ApiResponse.error_response("Company code is required")

            # Create CompanyInfo object
            company = CompanyInfo(
                company_code=company_data['company_code'],
                company_name=company_data.get('company_name'),
                city_code=company_data.get('city_code'),
                company_address=company_data.get('company_address'),
                phone_number=company_data.get('phone_number'),
                username=company_data.get('username'),
                password=company_data.get('password'),
                subscription_code=company_data.get('subscription_code'),
                last_payment=company_data.get('last_payment'),
                subscription_duration=company_data.get('subscription_duration'),
                registration_date=company_data.get('registration_date'),
                descriptions=company_data.get('descriptions')
            )

            # Insert into database
            with self.db_manager.get_cursor() as cursor:
                data = company.to_dict()
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?' for _ in data])

                query = f"INSERT INTO Companyinfo ({columns}) VALUES ({placeholders})"
                cursor.execute(query, list(data.values()))

            Logger.info(f"Company created: {company.company_code}")
            return ApiResponse.success_response(
                data=company,
                message=f"Company '{company.company_code}' created successfully"
            )

        except Exception as e:
            error_msg = f"Failed to create company: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_company(self, company_code: str) -> ApiResponse:
        """Get a company by code"""
        try:
            with self.db_manager.get_cursor() as cursor:
                cursor.execute("SELECT * FROM Companyinfo WHERE Companyco = ?", (company_code,))
                row = cursor.fetchone()

                if row:
                    # Convert row to dict (works with both sqlite3.Row and regular tuples)
                    if hasattr(row, 'keys'):
                        data = dict(row)
                    else:
                        # Fallback for regular tuples
                        columns = [desc[0] for desc in cursor.description]
                        data = dict(zip(columns, row))

                    company = CompanyInfo.from_dict(data)
                    return ApiResponse.success_response(
                        data=company,
                        message=f"Company '{company_code}' found"
                    )
                else:
                    return ApiResponse.error_response(
                        f"Company '{company_code}' not found"
                    )

        except Exception as e:
            error_msg = f"Failed to get company: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_all_companies(self, limit: Optional[int] = None, offset: int = 0) -> ApiResponse:
        """Get all companies with optional pagination"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Base query
                query = "SELECT * FROM Companyinfo"
                params = []

                # Add pagination
                if limit:
                    query += " LIMIT ? OFFSET ?"
                    params.extend([limit, offset])

                cursor.execute(query, params)
                rows = cursor.fetchall()

                companies = []
                for row in rows:
                    if hasattr(row, 'keys'):
                        data = dict(row)
                    else:
                        columns = [desc[0] for desc in cursor.description]
                        data = dict(zip(columns, row))

                    companies.append(CompanyInfo.from_dict(data))

                # Get total count
                cursor.execute("SELECT COUNT(*) FROM Companyinfo")
                total_count = cursor.fetchone()[0]

                return ApiResponse.success_response(
                    data=companies,
                    message=f"Retrieved {len(companies)} companies",
                    count=total_count
                )

        except Exception as e:
            error_msg = f"Failed to get companies: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def update_company(self, company_code: str, update_data: Dict[str, Any]) -> ApiResponse:
        """Update a company record"""
        try:
            # Check if company exists
            existing_response = self.get_company(company_code)
            if not existing_response.success:
                return existing_response

            # Prepare update data
            if 'company_code' in update_data:
                del update_data['company_code']  # Don't allow changing primary key

            if not update_data:
                return ApiResponse.error_response("No data provided for update")

            # Map field names to database column names
            field_mapping = {
                'company_name': 'Companyna',
                'city_code': 'Cityco',
                'company_address': 'Caddress',
                'phone_number': 'Cophoneno',
                'username': 'Username',
                'password': 'Password',
                'subscription_code': 'SubscriptionTCode',
                'last_payment': 'Lastpayment',
                'subscription_duration': 'Subscriptionduration',
                'registration_date': 'Registrationdate',
                'descriptions': 'descriptions'
            }

            # Build update query
            update_clauses = []
            values = []

            for field, value in update_data.items():
                db_column = field_mapping.get(field, field)
                update_clauses.append(f"{db_column} = ?")
                values.append(value)

            values.append(company_code)  # For WHERE clause

            with self.db_manager.get_cursor() as cursor:
                query = f"UPDATE Companyinfo SET {', '.join(update_clauses)} WHERE Companyco = ?"
                cursor.execute(query, values)

                if cursor.rowcount == 0:
                    return ApiResponse.error_response("No rows updated")

            # Return updated company
            return self.get_company(company_code)

        except Exception as e:
            error_msg = f"Failed to update company: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def delete_company(self, company_code: str) -> ApiResponse:
        """Delete a company record"""
        try:
            # Check if company exists
            existing_response = self.get_company(company_code)
            if not existing_response.success:
                return existing_response

            with self.db_manager.get_cursor() as cursor:
                cursor.execute("DELETE FROM Companyinfo WHERE Companyco = ?", (company_code,))

                if cursor.rowcount == 0:
                    return ApiResponse.error_response("No rows deleted")

            Logger.info(f"Company deleted: {company_code}")
            return ApiResponse.success_response(
                message=f"Company '{company_code}' deleted successfully"
            )

        except Exception as e:
            error_msg = f"Failed to delete company: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def search_companies(self, search_term: str, fields: List[str] = None) -> ApiResponse:
        """Search companies by term in specified fields"""
        try:
            if not fields:
                fields = ['Companyna', 'Cityco', 'Caddress', 'Username']

            # Build search query
            search_clauses = [f"{field} LIKE ?" for field in fields]
            query = f"SELECT * FROM Companyinfo WHERE {' OR '.join(search_clauses)}"

            # Parameters for search (add % wildcards)
            search_params = [f"%{search_term}%" for _ in fields]

            with self.db_manager.get_cursor() as cursor:
                cursor.execute(query, search_params)
                rows = cursor.fetchall()

                companies = []
                for row in rows:
                    if hasattr(row, 'keys'):
                        data = dict(row)
                    else:
                        columns = [desc[0] for desc in cursor.description]
                        data = dict(zip(columns, row))

                    companies.append(CompanyInfo.from_dict(data))

                return ApiResponse.success_response(
                    data=companies,
                    message=f"Found {len(companies)} companies matching '{search_term}'",
                    count=len(companies)
                )

        except Exception as e:
            error_msg = f"Failed to search companies: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_next_company_code(self) -> ApiResponse:
        """Generate the next available company code"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Get the highest existing company code
                cursor.execute("SELECT MAX(Companyco) FROM Companyinfo")
                result = cursor.fetchone()
                max_code = result[0] if result and result[0] else None

                if max_code:
                    # Extract numeric part (assuming format like E001, E002, etc.)
                    if max_code.startswith('E'):
                        try:
                            num_part = int(max_code[1:])
                            next_num = num_part + 1
                            next_code = f"E{next_num:03d}"
                        except ValueError:
                            # Fallback if format is unexpected
                            next_code = "E001"
                    else:
                        next_code = "E001"
                else:
                    next_code = "E001"

                return ApiResponse.success_response(
                    data={'code': next_code},
                    message=f"Next available company code: {next_code}"
                )

        except Exception as e:
            error_msg = f"Failed to generate company code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_next_subscription_code(self) -> ApiResponse:
        """Generate the next available subscription code"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Get the highest existing subscription code
                cursor.execute("SELECT MAX(SubscriptionTCode) FROM Companyinfo")
                result = cursor.fetchone()
                max_code = result[0] if result and result[0] else None

                if max_code:
                    try:
                        next_num = int(max_code) + 1
                        next_code = str(next_num)
                    except ValueError:
                        next_code = "1"
                else:
                    next_code = "1"

                return ApiResponse.success_response(
                    data={'code': next_code},
                    message=f"Next available subscription code: {next_code}"
                )

        except Exception as e:
            error_msg = f"Failed to generate subscription code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_cities(self) -> ApiResponse:
        """Get all cities (record type '02') from MainCode for dropdown"""
        try:
            with self.db_manager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT Code, Name FROM Maincode WHERE Recty = '02' ORDER BY Name",
                )
                rows = cursor.fetchall()

                cities = []
                for row in rows:
                    cities.append({
                        'code': row[0],
                        'name': row[1],
                        'display': f"{row[0]} - {row[1]}"
                    })

                return ApiResponse.success_response(
                    data=cities,
                    message=f"Retrieved {len(cities)} cities",
                    count=len(cities)
                )

        except Exception as e:
            error_msg = f"Failed to get cities: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)
