from ollama import chat

from decorators import track_llm_metrics


class LLMClient:

    def __init__(self, model):

        self.model = model

    @track_llm_metrics
    def generate(self, prompt):

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]