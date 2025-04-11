from collections import deque
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'D'],
    'C': ['B', 'D'],
    'D': ['A', 'B', 'C']
}
def what_letter(letter):
    return letter == 'D'
def search(name):
    search_queue = deque()
    search_queue +=graph[name]
    searched = []
    while search_queue:
        person = search_queue.popleft()
        if not person in searched:
            if what_letter(person):
                print(person)
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False

search('A')
