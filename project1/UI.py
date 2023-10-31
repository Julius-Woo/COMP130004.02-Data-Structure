import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from rb_tree import RedBlackTree
from b_tree import BTree

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.tree_type = None
        self.tree = None
        self.style = ttk.Style(self.root)
        self.init_ui()
        

    def init_ui(self):
        self.root.title("Chinese-English Dictionary")
        self.root.geometry("680x400+400+300")
        self.root.minsize(400, 200)
        self.root.maxsize(900, 800)
        # 左侧部分
        left_frame = ttk.LabelFrame(self.root, text="Manage", width=300, height=500)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        import_frame = ttk.Frame(left_frame)
        import_frame.pack(pady=5, fill=tk.X)
        self.file_name_entry = ttk.Entry(left_frame)
        self.file_name_entry.pack(pady=5, fill=tk.X, padx=10)

        self.import_btn = ttk.Button(left_frame, text="Import")
        self.import_btn.pack(pady=5)

        spacer_frame = ttk.Frame(left_frame, height=20)
        spacer_frame.pack(fill=tk.X)

        english_label = ttk.Label(left_frame, text="English:")
        english_label.pack(pady=7)
        self.english_entry = ttk.Entry(left_frame)
        self.english_entry.pack(pady=7, fill=tk.X, padx=10)

        chinese_label = ttk.Label(left_frame, text="Chinese:")
        chinese_label.pack(pady=7)
        self.chinese_entry = ttk.Entry(left_frame)
        self.chinese_entry.pack(pady=7, fill=tk.X, padx=10)

        self.add_btn = ttk.Button(left_frame, text="Add")
        self.add_btn.pack(pady=5, side=tk.LEFT, padx=10)
        self.delete_btn = ttk.Button(left_frame, text="Delete")
        self.delete_btn.pack(pady=5, side=tk.RIGHT, padx=10)

        # 右侧部分
        right_frame = ttk.LabelFrame(self.root, text="Choice & Lookup", width=320, height=500)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 初始化按钮的样式
        self.style.configure('TButton', padding=6)
        self.style.map('Active.TButton', background=[('active', 'lightblue')])

        # 树选择按钮
        self.rbt_button = ttk.Button(right_frame, text="Red-black Tree", command=lambda: self.select_tree("RBT"))
        self.rbt_button.grid(row=0, column=0, padx=0, pady=5, sticky=tk.E)

        self.bt_button = ttk.Button(right_frame, text="B Tree", command=lambda: self.select_tree("BT"))
        self.bt_button.grid(row=0, column=1, padx=0, pady=5, sticky=tk.W)

        self.translate_entry = ttk.Entry(right_frame, width=12)
        self.translate_entry.grid(row=1, column=0, padx=7, pady=5, sticky=tk.E)

        # Translate 功能
        self.translate_button = ttk.Button(right_frame, text="Translate", width=8, command=self.translate)
        self.translate_button.grid(row=1, column=1, padx=7, pady=5, sticky=tk.W)

        search_label = ttk.Label(right_frame, text="Search from")
        search_label.grid(row=2, column=0, padx=1, pady=2, sticky=tk.E)

        self.search_entry1 = ttk.Entry(right_frame, width=10)
        self.search_entry1.grid(row=2, column=1, padx=1, pady=2)

        to_label = ttk.Label(right_frame, text="to")
        to_label.grid(row=2, column=2, padx=1, pady=2)

        self.search_entry2 = ttk.Entry(right_frame, width=10)
        self.search_entry2.grid(row=2, column=3, padx=1, pady=2)

        self.search_btn = ttk.Button(right_frame, text="Submit", width=6)
        self.search_btn.grid(row=2, column=4, padx=10, pady=20)

        output_label = ttk.Label(right_frame, text="Output:")
        output_label.grid(row=3, column=0, padx=7, pady=2, sticky=tk.W)

        self.output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=10)
        self.output_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        # 绑定事件
        self.import_btn.config(command=self.import_file)
        self.add_btn.config(command=self.add_word)
        self.delete_btn.config(command=self.delete_word)
        self.translate_button.config(command=self.single_search)
        self.search_btn.config(command=self.range_search)
        self.rbt_button.config(command=lambda: self.select_tree("RBT"))
        self.bt_button.config(command=lambda: self.select_tree("BT"))

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        file_name = file_path.split("/")[-1]
        self.file_name_entry.delete(0, tk.END)
        self.file_name_entry.insert(0, file_name)

        if self.tree is None:
            if self.tree_type == "RBT":
                self.tree = RedBlackTree()
            elif self.tree_type == "BT":
                self.tree = BTree(t=10)
            else:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, "Error: No initialization. Please choose a tree type and import a file.\n")
                return

        try:
            result = self.tree.initialize(file_path)
            # if result == []:
            #     raise Exception("Initialization failed: No data was inserted.")
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Succeed initialization!\n")
        except Exception as e:
            try:
                if self.tree_type == "RBT":
                    result = self.tree.batch_op(file_path)
                elif self.tree_type == "BT":
                    result = self.tree.batch_op(file_path)
                if result == []:
                    raise Exception("Initialization failed: No data was inserted.")
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, "Succeed insertion/deletion!\n")
            except Exception as e:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    
    def add_word(self):
        en = self.english_entry.get()
        cn = self.chinese_entry.get()
        
        if not en or not cn:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: Please enter both English and Chinese words.\n")
            return
        
        if self.tree is None:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: No initialization. Please choose a tree type and import a file.\n")
            return
        
        try:
            result = self.tree.insert_word(en, cn)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, result + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def delete_word(self):
        en = self.english_entry.get()
        
        if not en:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: Please enter an English word to delete.\n")
            return
        
        if self.tree is None:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: No initialization. Please choose a tree type and import a file.\n")
            return
        
        try:
            result = self.tree.delete_word(en)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, result + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def translate(self):
        en = self.translate_entry.get()
        
        if not en:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: Please enter an English word to translate.\n")
            return
        
        if self.tree is None:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: No initialization. Please choose a tree type and import a file.\n")
            return
        
        try:
            result = self.tree.singlesearch(en)
            if result is None:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, "Error: Word not found in the tree.\n")
            else:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, result + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def single_search(self):
        word = self.translate_entry.get()
        if not word:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Please enter a word to search.\n")
            return
        
        if self.tree is None:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: No initialization. Please choose a tree type and import a file.\n")
            return

        try:
            result = self.tree.singlesearch(word)
            if result is None:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, "Error: Word not found in the tree.\n")
            else:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, result + "\n")
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def range_search(self):
        low = self.search_entry1.get()
        high = self.search_entry2.get()
        
        if not low or not high:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: Please enter both range start and end.\n")
            return
        
        if self.tree is None:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "Error: No initialization. Please choose a tree type and import a file.\n")
            return
        
        try:
            result = self.tree.rangesearch(low, high)
            if not result:
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, "Error: No words found in the specified range.\n")
            else:
                self.output_text.delete('1.0', tk.END)
                for word, meaning in result:
                    self.output_text.insert(tk.END, f'{word}: {meaning}\n')
        except Exception as e:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def select_tree(self, tree_type):
        self.tree_type = tree_type
        if tree_type == "RBT":
            self.style.configure('RBT.TButton', background='lightblue')
            self.rbt_button.config(style='RBT.TButton')
            self.style.configure('BT.TButton', background='SystemButtonFace')
            self.bt_button.config(style='BT.TButton')
        elif tree_type == "BT":
            self.style.configure('BT.TButton', background='lightblue')
            self.bt_button.config(style='BT.TButton')
            self.style.configure('RBT.TButton', background='SystemButtonFace')
            self.rbt_button.config(style='RBT.TButton')
        self.tree = None

def main():
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()