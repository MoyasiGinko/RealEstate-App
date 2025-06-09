"""
Main Code API
Handles all CRUD operations for the MainCode table
"""

from typing import List, Optional, Dict, Any
from kivy.logger import Logger

from ..core.database import DatabaseManager
from .models import MainCode, ApiResponse


class MainCodeAPI:
    """API for Main Code operations"""

    # Record type descriptions mapping
    RECORD_TYPE_DESCRIPTIONS = {
        '01': 'Countries',
        '02': 'Cities',
        '03': 'Property Types',
        '04': 'Building Types',
        '05': 'Unit Measures',
        '06': 'Offer Types'
    }

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_main_code(self, code_data: Dict[str, Any]) -> ApiResponse:
        """Create a new main code record"""
        try:
            # Create MainCode object
            main_code = MainCode(
                record_type=code_data.get('record_type'),
                code=code_data.get('code'),
                name=code_data.get('name'),
                description=code_data.get('description')
            )

            # Insert into database
            with self.db_manager.get_cursor() as cursor:
                data = main_code.to_dict()
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?' for _ in data])

                query = f"INSERT INTO Maincode ({columns}) VALUES ({placeholders})"
                cursor.execute(query, list(data.values()))

            Logger.info(f"Main code created: {main_code.code}")
            return ApiResponse.success_response(
                data=main_code,
                message="Main code created successfully"
            )

        except Exception as e:
            error_msg = f"Failed to create main code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_main_code(self, code: str, record_type: Optional[str] = None) -> ApiResponse:
        """Get main code by code and optionally by record type"""
        try:
            with self.db_manager.get_cursor() as cursor:
                if record_type:
                    cursor.execute(
                        "SELECT * FROM Maincode WHERE Code = ? AND Recty = ?",
                        (code, record_type)
                    )
                else:
                    cursor.execute("SELECT * FROM Maincode WHERE Code = ?", (code,))

                row = cursor.fetchone()

                if row:
                    # Convert row to dict
                    if hasattr(row, 'keys'):
                        data = dict(row)
                    else:
                        columns = [desc[0] for desc in cursor.description]
                        data = dict(zip(columns, row))

                    main_code = MainCode.from_dict(data)
                    return ApiResponse.success_response(
                        data=main_code,
                        message=f"Main code '{code}' found"
                    )
                else:
                    search_criteria = f"code '{code}'"
                    if record_type:
                        search_criteria += f" and record type '{record_type}'"
                    return ApiResponse.error_response(
                        f"Main code with {search_criteria} not found"
                    )

        except Exception as e:
            error_msg = f"Failed to get main code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_all_main_codes(self, record_type: Optional[str] = None,
                          limit: Optional[int] = None, offset: int = 0) -> ApiResponse:
        """Get all main codes with optional filtering and pagination"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Base query
                query = "SELECT * FROM Maincode"
                params = []

                # Add record type filter
                if record_type:
                    query += " WHERE Recty = ?"
                    params.append(record_type)

                # Add ordering
                query += " ORDER BY Recty, Code"

                # Add pagination
                if limit:
                    query += " LIMIT ? OFFSET ?"
                    params.extend([limit, offset])

                cursor.execute(query, params)
                rows = cursor.fetchall()

                main_codes = []
                for row in rows:
                    if hasattr(row, 'keys'):
                        data = dict(row)
                    else:
                        columns = [desc[0] for desc in cursor.description]
                        data = dict(zip(columns, row))

                    main_codes.append(MainCode.from_dict(data))

                # Get total count
                count_query = "SELECT COUNT(*) FROM Maincode"
                count_params = []
                if record_type:
                    count_query += " WHERE Recty = ?"
                    count_params.append(record_type)

                cursor.execute(count_query, count_params)
                total_count = cursor.fetchone()[0]

                message = f"Retrieved {len(main_codes)} main codes"
                if record_type:
                    message += f" for record type '{record_type}'"

                return ApiResponse.success_response(
                    data=main_codes,
                    message=message,
                    count=total_count
                )

        except Exception as e:
            error_msg = f"Failed to get main codes: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_record_types(self) -> ApiResponse:
        """Get all unique record types"""
        try:
            with self.db_manager.get_cursor() as cursor:
                cursor.execute("SELECT DISTINCT Recty FROM Maincode WHERE Recty IS NOT NULL ORDER BY Recty")
                rows = cursor.fetchall()

                record_types = [row[0] for row in rows if row[0]]

                return ApiResponse.success_response(
                    data=record_types,
                    message=f"Found {len(record_types)} record types",
                    count=len(record_types)
                )

        except Exception as e:
            error_msg = f"Failed to get record types: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def update_main_code(self, original_code: str, update_data: Dict[str, Any],
                        original_record_type: Optional[str] = None) -> ApiResponse:
        """Update a main code record"""
        try:
            # Check if main code exists
            existing_response = self.get_main_code(original_code, original_record_type)
            if not existing_response.success:
                return existing_response

            if not update_data:
                return ApiResponse.error_response("No data provided for update")

            # Build update query
            update_clauses = []
            values = []

            for field, value in update_data.items():
                if field in ['record_type', 'code', 'name', 'description']:
                    db_column = {
                        'record_type': 'Recty',
                        'code': 'Code',
                        'name': 'Name',
                        'description': 'Description'
                    }[field]

                    update_clauses.append(f"{db_column} = ?")
                    values.append(value)

            if not update_clauses:
                return ApiResponse.error_response("No valid fields provided for update")

            # Build WHERE clause
            where_clause = "Code = ?"
            values.append(original_code)

            if original_record_type:
                where_clause += " AND Recty = ?"
                values.append(original_record_type)

            with self.db_manager.get_cursor() as cursor:
                query = f"UPDATE Maincode SET {', '.join(update_clauses)} WHERE {where_clause}"
                cursor.execute(query, values)

                if cursor.rowcount == 0:
                    return ApiResponse.error_response("No rows updated")

            # Return updated main code (use new code if it was updated)
            new_code = update_data.get('code', original_code)
            new_record_type = update_data.get('record_type', original_record_type)
            return self.get_main_code(new_code, new_record_type)

        except Exception as e:
            error_msg = f"Failed to update main code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def delete_main_code(self, code: str, record_type: Optional[str] = None) -> ApiResponse:
        """Delete a main code record"""
        try:
            with self.db_manager.get_cursor() as cursor:
                if record_type:
                    cursor.execute(
                        "DELETE FROM Maincode WHERE Code = ? AND Recty = ?",
                        (code, record_type)
                    )
                else:
                    cursor.execute("DELETE FROM Maincode WHERE Code = ?", (code,))

                if cursor.rowcount == 0:
                    return ApiResponse.error_response("No rows deleted")

            search_criteria = f"code '{code}'"
            if record_type:
                search_criteria += f" and record type '{record_type}'"

            Logger.info(f"Main code deleted: {code}")
            return ApiResponse.success_response(
                message=f"Main code with {search_criteria} deleted successfully"
            )

        except Exception as e:
            error_msg = f"Failed to delete main code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def search_main_codes(self, search_term: str, record_type: Optional[str] = None) -> ApiResponse:
        """Search main codes by term"""
        try:
            search_clauses = [
                "Code LIKE ?",
                "Name LIKE ?",
                "Description LIKE ?"
            ]

            query = f"SELECT * FROM Maincode WHERE ({' OR '.join(search_clauses)})"

            # Parameters for search (add % wildcards)
            search_params = [f"%{search_term}%" for _ in search_clauses]

            # Add record type filter if specified
            if record_type:
                query += " AND Recty = ?"
                search_params.append(record_type)

            query += " ORDER BY Recty, Code"

            with self.db_manager.get_cursor() as cursor:
                cursor.execute(query, search_params)
                rows = cursor.fetchall()

                main_codes = []
                for row in rows:
                    if hasattr(row, 'keys'):
                        data = dict(row)
                    else:
                        columns = [desc[0] for desc in cursor.description]
                        data = dict(zip(columns, row))

                    main_codes.append(MainCode.from_dict(data))

                message = f"Found {len(main_codes)} main codes matching '{search_term}'"
                if record_type:
                    message += f" in record type '{record_type}'"

                return ApiResponse.success_response(
                    data=main_codes,
                    message=message,
                    count=len(main_codes)
                )

        except Exception as e:
            error_msg = f"Failed to search main codes: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def bulk_insert_main_codes(self, main_codes: List[MainCode]) -> ApiResponse:
        """Bulk insert main codes"""
        try:
            with self.db_manager.get_cursor() as cursor:
                query = "INSERT INTO Maincode (Recty, Code, Name, Description) VALUES (?, ?, ?, ?)"
                insert_data = [
                    (mc.record_type, mc.code, mc.name, mc.description)
                    for mc in main_codes
                ]

                cursor.executemany(query, insert_data)

            Logger.info(f"Bulk inserted {len(main_codes)} main codes")
            return ApiResponse.success_response(
                data=main_codes,
                message=f"Successfully inserted {len(main_codes)} main codes",
                count=len(main_codes)
            )

        except Exception as e:
            error_msg = f"Failed to bulk insert main codes: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_record_type_options(self) -> List[Dict[str, str]]:
        """Get list of record type options with descriptions"""
        return [
            {'value': code, 'text': f"{code} - {desc}"}
            for code, desc in self.RECORD_TYPE_DESCRIPTIONS.items()
        ]

    def get_next_available_code(self, record_type: str, country_code: str = None) -> ApiResponse:
        """Generate the next available code for a given record type"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Get the highest existing code for this record type
                cursor.execute(
                    "SELECT MAX(Code) FROM Maincode WHERE Recty = ?",
                    (record_type,)
                )
                result = cursor.fetchone()
                max_code = result[0] if result and result[0] else None

                # Generate next code based on pattern
                if record_type == '01':
                    # Countries: sequential 3-digit codes (001, 002, 003...)
                    if max_code:
                        next_num = int(max_code) + 1
                        next_code = f"{next_num:03d}"
                    else:
                        next_code = "001"

                elif record_type == '02':
                    # Cities: 5-digit codes based on country code
                    if country_code:
                        # Pattern: {country_code}{sequential_2_digits}
                        # For example, if country is 001 (Iraq), cities would be 00101, 00102, etc.
                        country_prefix = country_code  # e.g., "001"

                        # Get highest city code for this specific country
                        cursor.execute(
                            "SELECT MAX(Code) FROM Maincode WHERE Recty = '02' AND Code LIKE ?",
                            (f"{country_prefix}%",)
                        )
                        result = cursor.fetchone()
                        country_max_code = result[0] if result and result[0] else None

                        if country_max_code:
                            # Extract the suffix and increment
                            suffix = country_max_code[len(country_prefix):]
                            next_suffix = int(suffix) + 1
                            next_code = f"{country_prefix}{next_suffix:02d}"
                        else:
                            # First city for this country
                            next_code = f"{country_prefix}01"
                    else:
                        # Fallback: use simple sequential approach
                        if max_code:
                            next_num = int(max_code) + 1
                            next_code = f"{next_num:05d}"
                        else:
                            next_code = "00101"

                else:
                    # Types 03-06: Type prefix + sequential 3-digit codes
                    prefix = record_type
                    if max_code:
                        # Extract the numeric part after the prefix
                        numeric_part = max_code[2:]  # Remove first 2 digits (type prefix)
                        next_num = int(numeric_part) + 1
                        next_code = f"{prefix}{next_num:03d}"
                    else:
                        next_code = f"{prefix}001"

                return ApiResponse.success_response(
                    data={'code': next_code},
                    message=f"Next available code for type {record_type}"
                )

        except Exception as e:
            error_msg = f"Failed to generate next code: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)

    def get_record_type_description(self, record_type: str) -> str:
        """Get description for a record type"""
        return self.RECORD_TYPE_DESCRIPTIONS.get(record_type, f"Type {record_type}")

    def get_countries(self) -> ApiResponse:
        """Get all countries (record type '01') for use in city creation"""
        try:
            with self.db_manager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT Code, Name FROM Maincode WHERE Recty = '01' ORDER BY Name",
                )
                rows = cursor.fetchall()

                countries = []
                for row in rows:
                    countries.append({
                        'code': row[0],
                        'name': row[1],
                        'display': f"{row[0]} - {row[1]}"
                    })

                return ApiResponse.success_response(
                    data=countries,
                    message=f"Retrieved {len(countries)} countries",
                    count=len(countries)
                )

        except Exception as e:
            error_msg = f"Failed to get countries: {str(e)}"
            Logger.error(error_msg)
            return ApiResponse.error_response(error_msg)
