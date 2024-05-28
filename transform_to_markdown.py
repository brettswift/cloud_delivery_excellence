import csv
from typing import List
import pandas as pd
import argparse
import os

#  Using this script.
# 1. Save the CSV file to the same directory as this script, with the name that matches the file being read below.
# 2. Run this script using the command `python transform_to_markdown.py`
# 3. The output will be printed to the console. You can redirect the output to a file using `python transform_to_markdown.py > cloud_delivery_excellence.md`
# 4. when editing markdown tables, a vscode extension called "Markdown Table" will take care of formatting for you.

OUTPUT_DIR = 'output'
# Read the CSV data
with open('ServiceExcellence.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    data = list(reader)

# csv headers: Id,Name,Shape Library,Page ID,Contained By,Group,Line Source,Line Destination,Source Arrow,Destination Arrow,Status,Text Area 1,Comments,Id,ParentId,property 1,Text
class Node:
    def __init__(self, name, id, parent_id):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.children = []
    
    def add(self, node):
        self.children.append(node)

    @staticmethod
    def parse_csv_to_nodes(data):
        nodes = []
        for row in data:
            if row[16]:
                nodes.append(Node(row[16], row[13], row[14]))

        return nodes

def find_root_node(nodes: List[Node]):
    for n in nodes:
        if not n.parent_id:
            return n
    raise Exception("No root node found")

all_nodes = Node.parse_csv_to_nodes(data)
root_node = find_root_node(all_nodes)


def add_children(node: Node, nodes: List[Node]):
    for n in nodes:
        if n.parent_id == node.id:
            node.add(n)
            add_children(n, nodes)

add_children(root_node, all_nodes)
def get_max_width(node: Node, indent: int = 0) -> int:
    max_width = len(node.name) + indent
    for child in node.children:
        child_width = get_max_width(child, indent + 2)
        if child_width > max_width:
            max_width = child_width
    return max_width

def print_markdown_nodes(node: Node, indent: int = 0, file=None):
    max_width = get_max_width(node, indent)
    file.write(" " * indent + f"| {'Item'.ljust(max_width)} | {'Comments'.ljust(80)} |\n")
    file.write(" " * indent + "|".ljust(max_width + 3, '-') + "|" + "-" * 82 + "|\n")
    for child in node.children:
        print_markdown_node(child, indent, max_width, file)

def print_markdown_node(node: Node, indent: int, max_width: int, file):
    file.write(f"| {(' ' * indent) + node.name.ljust(max_width - indent)} | {''.ljust(80)} |\n")
    for child in node.children:
        print_markdown_node(child, indent + 2, max_width, file)

def print_markdown(file_name):
    with open(file_name, 'w') as f:
        f.write("# Cloud Delivery Excellence Analysis for <company_name_here>\n")
        f.write("\n")
        f.write("Items in this table map to the Cloud Delivery Excellence mind map.\n")
        f.write("\n")
        print_markdown_nodes(root_node, file=f)

def print_csv(file_name):
    with open(file_name, 'w') as f:
        f.write("Name,Comments\n")
        print_csv_nodes(root_node, file=f)

def print_csv_nodes(node: Node, indent: int = 0, file=None):
    print_csv_node(node, indent, file)
    for child in node.children:
        print_csv_node(child, indent + 2, file)

def print_csv_node(node: Node, indent: int, file):
    file.write(f"{' ' * indent}{node.name},\n")
    for child in node.children:
        print_csv_node(child, indent + 2, file)

def get_indent_color(indent: int) -> str:
    if indent <= 2:
        return "#D3D3D3"  # Medium Grey
    elif indent <= 4:
        return "#F0F0F0"  # Light Grey
    else:
        return '#FFFFFF'  # White

def print_excel_nodes(node: Node, indent: int = 0, data=None):
    if data is None:
        data = []
    data.append({'Item': (' ' * indent) + node.name, 'Comments': ''})
    for child in node.children:
        print_excel_nodes(child, indent + 2, data)
    return data

def print_excel(file_name):
    data = print_excel_nodes(root_node)
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name="Scorecard")
    workbook  = writer.book
    worksheet = writer.sheets['Scorecard']
    for i, row in enumerate(data):
        color = get_indent_color(len(row['Item']) - len(row['Item'].lstrip()))
        format = workbook.add_format({'bg_color': color, 'border': 1})
        worksheet.write(i+1, 0, row['Item'], format)
        worksheet.write(i+1, 1, row['Comments'], format)
    worksheet.set_column('A:A', 30)  # Set width of column A
    comments_format = workbook.add_format({'text_wrap': True})
    worksheet.set_column('B:B', 80, comments_format)  # Set width of column B and wrap text
    writer.close()

def main():
    parser = argparse.ArgumentParser(description='Transform nodes to specified format.')
    parser.add_argument('--format', type=str, required=True, choices=['markdown', 'csv', 'excel'],
                        help='The format to print the nodes in.')
    args = parser.parse_args()

    # force creating the output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = f"{OUTPUT_DIR}/cloud_delivery_excellence.{args.format}"
    if args.format == 'markdown':
        print_markdown(file_name=filename.replace('markdown', 'md'))
    elif args.format == 'csv':
        print_csv(file_name=filename)
    elif args.format == 'excel':
        print_excel(file_name=filename.replace('excel', 'xlsx'))

if __name__ == '__main__':
    main()
