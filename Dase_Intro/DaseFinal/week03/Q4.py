# 创建结点类
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        return

# 检查值是否存在-->查
    def has_value(self, value):
        if self.data == value:
            return True
        else:
            return False


# 构建单链表类
class SingleLinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        return

    def isEmpty(self):
        if self.length == 0:
            return True
        else:
            return False

    def add_node(self, item):
        if not isinstance(item, Node):
            item = Node(item)
            # 如果item不是一个结点类，利用item形成一个结点类
        if self.head is None:
            self.head = item
            self.tail = item
        else:
            self.tail.next = item
            self.tail = item
            # 这里不选择使用头插法，因为会逆序排列我们增加的元素
            # item.next = self.head
            # self.head = item
        self.length += 1
        return

    def insert_node(self, index, data):
        if self.isEmpty():
            print("Empty LinkList!")
            return
        if index < 1 or index > self.length + 1:
            print("index error: out of range!")
            return
        item = Node(data)
        if index == 1:
            item.next = self.head
            self.head = item
            self.length += 1
            return
        j = 1
        noDe = self.head
        prev = self.head
        while noDe.next and j < index:
            prev = noDe
            noDe = noDe.next
            j += 1
        if j == index:
            item.next = noDe
            prev.next = item
            self.length += 1
            return
        if noDe.next is None:
            self.add_node(item)

    def delete_node(self, index):
        if self.isEmpty():
            print("Empty LinkList")
            return
        if index < 1 or self.length < index:
            print("index error: out of range")
            return
        pos = 1
        current_node = self.head
        prev_node = None
        while current_node is not None:
            if pos == index:
                if prev_node is not None:
                    prev_node.next = current_node.next
                    return
                else:
                    self.head = current_node.next
                    return
            prev_node = current_node
            current_node = current_node.next
            pos += 1
        self.length -= 1
        return

    def find_node(self, value):
        current_node = self.head
        pos = 1
        result = []
        while current_node is not None:
            if current_node.has_value(value):
                result.append(pos)
            current_node = current_node.next
            pos += 1
        return result

    def change_node_by_pos(self, value, data):
        current_node = self.head
        if value < 1 or value > self.length:
            print("index error: out of range")
            return
        pos = 1
        while pos < value:
            current_node = current_node.next
            pos += 1
        current_node.data = data
        return

    def change_node_by_item(self, value, data):
        current_node = self.head
        while current_node is not None:
            if current_node.data == value:
                current_node.data = data
            current_node = current_node.next
        return

    def print_link(self):
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        return


# 创建三个节点
Node1 = Node('a')
Node2 = Node('b')
Node3 = Node('c')

# 定义一个空链表
link = SingleLinkList()

# 判断是否是空链表
print(link.isEmpty())

# 尾部添加结点
for node in [Node1, Node2, Node3]:
    link.add_node(node)

link.print_link()

# 在链表中插入几个元素
link.insert_node(2, 'e')
link.insert_node(3, 'f')
link.insert_node(3, 'f')
link.insert_node(8, 'h')  # 无法插入

link.print_link()
print('*****************')

# 删除元素
link.delete_node(3)
link.print_link()

print('*****************')
# 查找元素
node_ids = link.find_node('f')  # 查询元素位置
if len(node_ids) == 0:
    print('链表中无此元素')
else:
    print(node_ids)

link.change_node_by_pos(2, 'ss')
link.change_node_by_item('f', 'd')
link.print_link()
