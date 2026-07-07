import json
import re
import sqlite3

from database import get_connection
from models import ToolError, ToolResponse

def validate_order_id(order_id:str) -> bool:
    if not isinstance(order_id, str):
        return False
    pattern = r"^ORD\d+$"
    return re.match(pattern, order_id) is not None


def validate_product_id(product_id: str) -> bool:
    if not isinstance(product_id, str):
        return False
    pattern = r"^P\d+$"
    return re.match(pattern, product_id) is not None

def validate_email(email: str):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None

ALLOWED_PRIORITIES = {
    "low",
    "medium",
    "high"
}
def validate_priority(priority):
    return priority.lower() in ALLOWED_PRIORITIES


def get_order_status(order_id: str) -> ToolResponse:

    if not validate_order_id(order_id):
        return ToolResponse(
            success=False,
            error=ToolError(
                code = "INVALID_ORDER_ID",
                message = "Invalid Order id format."
            )
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            order_id,
            customer_name,
            product_id,
            status,
            estimated_delivery
        FROM orders
        WHERE order_id=?
        """, (order_id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return ToolResponse(
                success= False,
                error = ToolError(
                    code = "ORDER_NOT_FOUND",
                    message= f"Order with id {order_id} not found."
                )
            )
        
        return ToolResponse(
            success=True,
            data={
                "order_id": row[0],
                "customer_name": row[1],
                "product_id": row[2],
                "status": row[3],
                "estimated_delivery": row[4]
            }
        )
    except sqlite3.Error as e:
        return ToolResponse(
            success= False,
            error = ToolError(
                code = "DATABASE_ERROR",
                message= f"Database error: {str(e)}"
            )
        )
    

def get_product_info(product_id: str) -> ToolResponse:
    if not validate_product_id(product_id):
        return ToolResponse(
            success= False,
            error= ToolError(
                code = "INVALID_PRODUCT_ID",
                message= "Invalid Product id format."
            )
        )
    
    try:
        with open("products.json") as file:
            products = json.load(file)

            for product in products:
                if product["product_id"] == product_id:
                    return ToolResponse(
                        success=True,
                        data=product
                    )
            return ToolResponse(
                success=False,
                error=ToolError(
                    code="PRODUCT_NOT_FOUND",
                    message=f"Product with id {product_id} not found."
                )
            )
    except Exception as e:
        return ToolResponse(
            success=False,
            error=ToolError(
                code="DATABASE_ERROR",
                message=f"Database error: {str(e)}"
            )
        )
    
def create_support_ticket(
        customer_email:str,
        issue_description:str,
        priority:str
) -> ToolResponse:
        if not validate_email(customer_email):
            return ToolResponse(
                success= False,
                error= ToolError(
                    code = "INVALID_EMAIL",
                    message= "Invalid email format."
                )
            )
        
        if len(issue_description.strip()) == 0:
            return ToolResponse(
                success= False,
                error= ToolError(
                    code = "EMPTY_DESCRIPTION",
                    message= "Issue description cannot be empty."
                )
            )
        
        if not validate_priority(priority):
            return ToolResponse(
                success= False,
                error= ToolError(
                    code = "INVALID_PRIORITY",
                    message= "Invalid priority level."
                )
            )
        
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO support_tickets(
                customer_email,
                issue_description,
                priority
            )
            VALUES(?,?,?)
            """, (
                customer_email,
                issue_description,
                priority.lower()
            ))

            conn.commit()

            ticket_id = cursor.lastrowid
            conn.close()
            return ToolResponse(
                success= True,
                data= {
                    "ticket_id": ticket_id,
                    "status": "CREATED"
                }
            )
        except sqlite3.Error as e:  
            return ToolResponse(
                success= False,
                error= ToolError(
                    code = "DATABASE_ERROR",
                    message= f"Database error: {str(e)}"
                )
            )
        
