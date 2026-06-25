import tiktoken

class ContextWindowManager:
    MODEL_ENCODINGS ={
        "gpt-4": "cl100k_base",
        "gpt-4o": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base"
    }

    TOKENS_PER_MESSAGE = 4
    TOKENS_PER_NAME = 1
    REPLY_PRIMING_TOKENS = 3

    def __init__(
            self,
            model_name:str,
            max_token_budget:int
    ):
        self.mode_name = model_name
        self.max_token_budget = max_token_budget

        encoding_name = self.MODEL_ENCODINGS.get(
            model_name,
            "cl100k_base"
        )

        self.encoding = tiktoken.get_encoding(
            encoding_name
        )

    
    def count_message_tokens(
            self,
            message
    ):
        tokens = self.TOKENS_PER_MESSAGE
        tokens += len(
            self.encoding.encode(
                message["content"]
            )
        )

        if "name" in message:
            tokens += self.TOKENS_PER_NAME
        
        return tokens
    

    
    def count_messages_tokens(
            self, 
            messages
    ):
        total = self.REPLY_PRIMING_TOKENS
        for message in messages:
            total += self.count_message_tokens(
                message
            )
        return total
    

    def fit_messages(
            self,
            system_prompt,
            conversation_messages
    ):
        fitted_messages = [
            {
                "role": "system",
                "content" : system_prompt
            }
        ]

        current_tokens = self.count_messages_tokens(
            fitted_messages
        )

        reverse_messages = list(
            reversed(conversation_messages)
        )

        selected = []

        for message in reverse_messages:
            message_tokens = (
                self.count_message_tokens(
                    message
                )
            )

            if(
                current_tokens + message_tokens
                <= self.max_token_budget
            ):
                selected.append(message)
                current_tokens += (
                    message_tokens
                )
            else:
                break

        
        selected.reverse()
        fitted_messages.extend(selected)

        return fitted_messages
    


