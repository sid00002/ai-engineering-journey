from dataclasses import dataclass
from typing import List, Dict
import copy
import tiktoken



class BudgetError(Exception):
    pass

@dataclass
class RetrivedChunk:
    text:str
    score:float


class TokenCounter:
    def __init__(
            self, model:str = "gpt-4o"
    ):
        self.model = model
        if tiktoken:
            try:
                self.encoding = tiktoken.encoding_for_model(model)
            except KeyError:
                self.encoding = tiktoken.get_encoding("cl100k_base")
        else:
            self.encoding = None

        
    def count_text(self, text:str) -> int:
        if self.encoding:
            return len(self.encoding.encode(text))
        return max(1, len(text)//4)
    
    def count_message(self, message: Dict) -> int:
        tokens = 4
        tokens += self.count_text(message["content"])

        if "content" in message:
            tokens += self.count_text(message["content"])
        
        return tokens
    
    def count_messages(self, messages: List[Dict]) -> int:
        return sum(self.count_message(m) for m in messages) + 2



class ContextAllocator:

    RETRIEVED_ROLE = "system"

    def __init__(self, model="gpt-4o"):
        self.counter = TokenCounter(model)

    def allocate(
        self,
        system_prompt: str,
        conversation: List[Dict],
        retrieved_chunks: List[RetrievedChunk],
        max_tokens: int,
        response_reservation: int,
    ) -> List[Dict]:

        available_budget = max_tokens - response_reservation

        if available_budget <= 0:
            raise BudgetError("Response reservation exceeds token budget.")

        system_msg = {
            "role": "system",
            "content": system_prompt,
        }

        system_tokens = self.counter.count_messages([system_msg])

        if system_tokens > available_budget:
            raise BudgetError("System prompt alone exceeds token budget.")

        remaining = available_budget - system_tokens

        conversation = copy.deepcopy(conversation)

        conversation_tokens = self.counter.count_messages(conversation)

        remaining -= conversation_tokens

        while remaining < 0 and conversation:
            conversation.pop(0)

            conversation_tokens = self.counter.count_messages(conversation)
            remaining = available_budget - system_tokens - conversation_tokens

        if remaining < 0:
            raise BudgetError("Conversation cannot fit even after truncation.")


        retrieved_chunks = sorted(
            retrieved_chunks,
            key=lambda x: x.score,
            reverse=True,
        )

        retrieved_messages = []

        for chunk in retrieved_chunks:

            msg = {
                "role": self.RETRIEVED_ROLE,
                "content": f"Retrieved Context:\n{chunk.text}",
            }

            tokens = self.counter.count_messages([msg])

            if tokens <= remaining:
                retrieved_messages.append(msg)
                remaining -= tokens

        return [system_msg] + retrieved_messages + conversation

    