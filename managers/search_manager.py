from typing import List, Any, Optional

class SearchManager:
    @staticmethod
    def search(array: List[dict], key: str, target: Any) -> Optional[int]:
        left, right = 0, len(array) - 1

        while left <= right:
            mid = (left + right) // 2
            if array[mid][key] == target:
                return mid
            elif array[mid][key] < target:
                left = mid + 1
            else:
                right = mid - 1

        return None