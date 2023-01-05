import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Block:
    def __init__(self) -> None:
        self.cells = {}
        self._initialize_cells()
        self._get_input() 
        print("Evaluating cells...")
        self._evaluate_units() 
        print("")
        
    def _initialize_cells(self):
        print("Initializing cells...")
        for row in range(9):
            for col in range (9):
                key = str(row) + '_' + str(col)
                block = (2 * (row//3)) + row//3 + col//3
                vals = ['1','2','3','4','5','6','7','8','9']
                self.cells[key] = {
                        'row': str(row), 
                        'col': str(col), 
                        'block': str(block), 
                        'val': vals, 
                        'complete': '0'
                        }
        self._print_cells()
        print("")

    def _get_input(self):
        print("Getting input...")
        with open('cells.json') as json_file:
            data = json.load(json_file)
        for k, v in data.items():
            row = k
            for col, cell in enumerate(v):
                if str(cell).lower() != "x":
                    key = row + '_' + str(col)
                    block = (2 * (int(row)//3)) + int(row)//3 + int(col)//3
                    self.cells[key] = {'row': row, 'col': col, 'block': str(block), 'val': [str(cell)], 'complete': '1'}
        self._print_cells()
        print("")
    
    def _check_completion(self):
        complete = True
        for k, v in self.cells.items():
            if len(v['val']) > 1:
                complete = False

        if complete:
            print("Complete!")
            self._print_cells()
        
        return complete

    def _print_cells(self):
        for row in range(9):
            disp = ""
            for col in range (9):
                key = str(row) + '_' + str(col)
                disp = disp + str(str(''.join(str(e) for e in self.cells[key]['val'])) + "          ")[:10]
            print(disp, flush=True)
        
    def _remove_val_from_col(self, col, search_val):
        dirty = False
        for row in range(9):
            key = str(row) + '_' + str(col)
            val = self.cells[key]['val']
            # print(f"Row: {row}")
            if len(val) > 1 and search_val in val:
                print(f"Using value {search_val} in column {col}, removing value from {row}, {col}")
                self.cells[key]['val'].remove(search_val)
                if len(self.cells[key]['val']) == 1:
                    self.cells[key]['complete'] = '1'
                self._print_cells()
                print("")
                dirty = True
        return dirty
                    
    def _remove_val_from_row(self, row, search_val):
        dirty = False
        for col in range(9):
            key = str(row) + '_' + str(col)
            val = self.cells[key]['val']
            # print(f"Col: {col}")
            if len(val) > 1 and search_val in val:
                print(f"Using value {search_val} in row {row}, removing value from {row}, {col}")
                self.cells[key]['val'].remove(search_val)
                if len(self.cells[key]['val']) == 1:
                    self.cells[key]['complete'] = '1'
                self._print_cells()
                print("")
                dirty = True
        return dirty
    
    def _remove_val_from_block(self, block, search_val):
        dirty = False
        for row in range(9):
            for col in range(9):
                block_val = str((2 * (row//3)) + row//3 + col//3)
                if block_val == str(block):
                    key = str(row) + '_' + str(col)
                    val = self.cells[key]['val']
                    # print(f"Block: {block}")
                    if len(val) > 1 and search_val in val:
                        print(f"Using value {search_val} in block {block}, removing value from {row}, {col}")
                        self.cells[key]['val'].remove(search_val)
                        if len(self.cells[key]['val']) == 1:
                            self.cells[key]['complete'] = '1'
                        self._print_cells()
                        print("")
                        dirty = True
        return dirty
    
    def _evaluate_units(self):
        dirty = True
        while dirty:
            dirty = False
            for k, v in self.cells.items():
                if v['complete'] == '1':
                    dirty_row = self._remove_val_from_col(v['col'], v['val'][0])
            for k, v in self.cells.items():
                if v['complete'] == '1':
                    dirty_col = self._remove_val_from_row(v['row'], v['val'][0])
            for k, v in self.cells.items():
                if v['complete'] == '1':
                    dirty_block = self._remove_val_from_block(v['block'], v['val'][0])
            if dirty_row or dirty_col or dirty_block:
                dirty = True
        
        self._print_cells()
                
if __name__ == '__main__':
    block = Block()
