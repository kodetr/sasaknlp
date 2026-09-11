"""Prefix Trie data structure for fast prefix searching and morphological lookup."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class TrieNode:
    """A single node within the Prefix Trie."""

    __slots__ = ("children", "is_terminal", "values")

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_terminal: bool = False
        self.values: List[str] = []


class PrefixTrie:
    """Fast prefix trie supporting O(L) insertion, exact lookup, and prefix queries."""

    def __init__(self) -> None:
        self.root = TrieNode()
        self._size = 0

    def insert(self, word: str, value: Optional[str] = None) -> None:
        """Insert a word and optional associated payload value into the trie."""
        if not word:
            return
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_terminal:
            self._size += 1
            node.is_terminal = True
        if value is not None:
            node.values.append(value)

    def contains(self, word: str) -> bool:
        """Check if exact word exists in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_terminal

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Traverse to node matching prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def find_longest_prefix(self, text: str) -> Tuple[str, Optional[TrieNode]]:
        """Find the longest prefix in the trie that matches the beginning of text."""
        node = self.root
        longest_prefix = ""
        current_str = []
        last_terminal_node: Optional[TrieNode] = None

        for char in text:
            if char not in node.children:
                break
            node = node.children[char]
            current_str.append(char)
            if node.is_terminal:
                longest_prefix = "".join(current_str)
                last_terminal_node = node

        return longest_prefix, last_terminal_node

    def search_by_prefix(self, prefix: str, limit: int = 20) -> List[str]:
        """Find all words starting with given prefix up to limit."""
        node = self._find_node(prefix)
        if not node:
            return []

        results: List[str] = []

        def _dfs(curr_node: TrieNode, path: List[str]) -> None:
            if len(results) >= limit:
                return
            if curr_node.is_terminal:
                results.append(prefix + "".join(path))
            for char, child in sorted(curr_node.children.items()):
                path.append(char)
                _dfs(child, path)
                path.pop()

        _dfs(node, [])
        return results

    def __len__(self) -> int:
        return self._size
