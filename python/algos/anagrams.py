    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sortedGroups = {}
        for s in strs:
            s_sorted = tuple(sorted(s))
            if s_sorted not in sortedGroups:
                sortedGroups[s_sorted] = []
            sortedGroups[s_sorted].append(s)
        return sortedGroups.values()
