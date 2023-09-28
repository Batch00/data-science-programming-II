# project: p3
# submitter: cmbatchelor
# partner: none
# hours: 8

import os
from collections import deque
import pandas as pd
import time
import requests
import shutil
from IPython.core.display import Image, display


class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []
        
        self.finder_parent = None
        self.children = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.visited = set()
        self.order.clear()
        self.dfs_visit(node)
    
    def bfs_search(self, node):
        self.order.clear()
        self.bfs_visit(node)
        
    def dfs_visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)
        self.order.append(node)
        children = self.go(node)
        for c in children:
            self.dfs_visit(c)
            
    def bfs_visit(self, node):
        todo = [node] # tasks to complete (a node to visit) -- start from beginning
        added = set([node])
        self.order.append(node)
        
        while len(todo) > 0:
            curr_node = todo.pop(0)
            #print("CURR:", curr_node)
            
            children = self.go(curr_node)
            
            for child in children:
                if child not in added:
                    todo.append(child)
                    added.add(child)
                    self.order.append(child)
            #print("TODO:", todo)
        return None
              
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def go(self, node):
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for n, has_edge in self.df.loc[node].items():
            if has_edge:
                children.append(n)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__() # call constructor method of parent class
        
    def go(self, file):
        self.file = file
        for txt_file in os.listdir("file_nodes"):
            if self.file == txt_file:
                path = os.path.join("file_nodes", txt_file)
                f = open(path)
                read = f.read().split()
                child_list = read[1].split(',')
                self.file = child_list
                self.order.append(read[0])
        return self.file
    
    def message(self):
        message = []
        for val in self.order:
            if "txt" not in val:
                message.append(val)
        return "".join(message)
    
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
    def go(self, start_url):
        self.node = start_url
        nodes_to_visit = deque([start_url])
        added = {start_url}
        
        while len(nodes_to_visit) > 0:
            curr_node = nodes_to_visit.popleft() # .pop(0)
            #print(curr_node)
            self.driver.get(curr_node)            
            
            links = self.driver.find_elements(by="tag name", value="a")
            for link in links: # each link is a child
                child_url = link.get_attribute("href")
         
                if not child_url in added:
                    nodes_to_visit.append(child_url)
                    added.add(child_url)

            return list(nodes_to_visit)
                
    def table(self):
        self.df_list = []
        for url in self.order:
            self.df_list.append(pd.read_html(url, 
                                             attrs = {'id': 'locations-table'})[0])
        df = pd.concat(self.df_list).reset_index(drop=True)
        return df
def show(driver):
    driver.set_window_size(1000, 600)
    driver.save_screenshot("screen.png")
    display(Image("screen.png"))
    
def reveal_secrets(driver, url, travellog):
    driver.get(url)
    
    passw = []
    for clue in travellog['clue']:
        passw.append(str(clue))
    
    password = ''.join(passw)
    #print(password)
    
    pass_box = driver.find_element(value = "password")
    button = driver.find_element(value = "attempt-button")
    
    pass_box.send_keys(password)
    button.click()
    time.sleep(5)
 
    view_button = driver.find_element(value = "securityBtn")
    view_button.click()
    time.sleep(5)
    
    image = driver.find_element(by = "id", value = "image")
    img_link = image.get_attribute("src")
    
    r = requests.get(img_link, stream = True)
    
    with open('Current_Location.jpg', "wb") as f:
        shutil.copyfileobj(r.raw, f)
        
    curr_location = driver.find_element(by = "tag name", value = 'p')
    return curr_location.text
    
    
    