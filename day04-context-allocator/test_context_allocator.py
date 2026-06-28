import unittest

from context_allocator import (
    ContextAllocator,
    RetrievedChunk,
    BudgetError,
)


class ContextAllocatorTests(unittest.TestCase):

    def setUp(self):
        self.alloc = ContextAllocator()

    def test_normal_case(self):

        conversation = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]

        docs = [
            RetrievedChunk("Important document", 0.9),
            RetrievedChunk("Another document", 0.7),
        ]

        messages = self.alloc.allocate(
            system_prompt="You are helpful.",
            conversation=conversation,
            retrieved_chunks=docs,
            max_tokens=300,
            response_reservation=50,
        )

        self.assertGreater(len(messages), 0)

    def test_budget_too_small_for_system_prompt(self):

        with self.assertRaises(BudgetError):

            self.alloc.allocate(
                system_prompt="A" * 10000,
                conversation=[],
                retrieved_chunks=[],
                max_tokens=50,
                response_reservation=10,
            )

    def test_budget_too_small_for_chunks(self):

        docs = [
            RetrievedChunk("A" * 10000, 1.0)
        ]

        messages = self.alloc.allocate(
            system_prompt="System",
            conversation=[],
            retrieved_chunks=docs,
            max_tokens=100,
            response_reservation=20,
        )

        self.assertEqual(len(messages), 1)

    def test_history_truncated(self):

        history = []

        for i in range(20):
            history.append({
                "role": "user",
                "content": "hello " * 100
            })

        docs = [
            RetrievedChunk("important", 1.0)
        ]

        messages = self.alloc.allocate(
            system_prompt="System",
            conversation=history,
            retrieved_chunks=docs,
            max_tokens=300,
            response_reservation=50,
        )

        self.assertLess(len(messages), len(history) + 2)

    def test_chunks_sorted_by_score(self):

        docs = [
            RetrievedChunk("low", 0.1),
            RetrievedChunk("high", 0.9),
            RetrievedChunk("medium", 0.5),
        ]

        messages = self.alloc.allocate(
            system_prompt="System",
            conversation=[],
            retrieved_chunks=docs,
            max_tokens=200,
            response_reservation=50,
        )

        retrieved = [
            m["content"] for m in messages
            if "Retrieved Context" in m["content"]
        ]

        if len(retrieved) >= 2:
            self.assertTrue(
                retrieved[0].endswith("high")
            )

    def test_zero_available_budget(self):

        with self.assertRaises(BudgetError):

            self.alloc.allocate(
                system_prompt="System",
                conversation=[],
                retrieved_chunks=[],
                max_tokens=100,
                response_reservation=100,
            )


if __name__ == "__main__":
    unittest.main()