from models import ToolResponse


class ResponseFormatter:
    """
    Converts a ToolResponse into a user-friendly message.
    """

    def format(self, response: ToolResponse) -> str:

        if not response.success:
            return f"Error: {response.error.message}"

        data = response.data

        if (
            isinstance(data, dict)
            and "order_id" in data
            and "status" in data
        ):
            return (
                f"Order ID: {data['order_id']}\n"
                f"Customer: {data['customer_name']}\n"
                f"Product ID: {data['product_id']}\n"
                f"Status: {data['status']}\n"
                f"Estimated Delivery: {data['estimated_delivery']}"
            )


        if (
            isinstance(data, dict)
            and "product_id" in data
            and "price" in data
        ):
            return (
                f"Product ID: {data['product_id']}\n"
                f"Name: {data['name']}\n"
                f"Description: {data['description']}\n"
                f"Price: ${data['price']}\n"
                f"Stock: {data['stock']}"
            )

        if (
            isinstance(data, dict)
            and "ticket_id" in data
        ):
            return (
                f"Support ticket #{data['ticket_id']} "
                f"created successfully."
            )

        return str(data)