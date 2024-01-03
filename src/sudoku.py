import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Block:
    def __init__(self, file_name: str = None) -> None:
        self._cells = {}
        self._initialize_cells()
        self._rows = self._get_units(unit_type="rows")
        self._columns = self._get_units(unit_type="columns")
        self._blocks = self._get_units(unit_type="blocks")
        if file_name:
            self._read_input(file_name)
        # print("Evaluating cells...")
        # self._evaluate_units()
        
    def _initialize_cells(self):
        logger.info("initializing cells...")
        for _row in range(9):
            for _column in range(9):
                _block = ((_row+1)//3 + (_column+1)//3) - 1
                _key = str(_row) + '_' + str(_column) + "_" + str(_block)
                _values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self._cells[_key] = {
                    'row': _row,
                    'column': _column,
                    'block': _block,
                    'values': _values,
                    'complete': False
                }
        logger.info("\n")

    def _read_input(self, file_name: str):
        logger.info("Getting input...")
        with open(file_name) as json_file:
            _data = json.load(json_file)
        for k, v in _data.items():
            _row = k
            for _column in range(9):
                _block = (int(_row)+1)//3 + ((_column+1)//3) - 1
                _key = str(_row) + '_' + str(_column)
                if v[_column] != "0":
                    _values = [v[_column]]
                    self._cells[_key] = {
                        'row': _row,
                        'col': _column,
                        'block': _block,
                        'values': _values,
                        'complete': True
                    }
        logger.info("\n")
    
    def _check_completion(self):
        complete = True
        for k, v in self._cells.items():
            if len(v['values']) > 1:
                complete = False

        return complete

    def print_cells(self):
        for _row in range(9):
            _display = ""
            for _column in range(9):
                _block = (int(_row) + 1) // 3 + ((_column + 1) // 3) - 1
                key = str(_row) + '_' + str(_column) + "_" + str(_block)
                _display = _display + str(str(''.join(str(e) for e in self._cells[key]['values'])) + "          ")[:10]
            print(_display, flush=True)
            
    # def _remove_val_from_unit(self, unit, unit_val, search_val):
    #     for k, v in self._cells.items():
    #         if v[unit] == unit_val and len(v['val']) > 1 and search_val in v['val']:
    #             v['val'].remove(search_val)
    #             if len(v['val']) == 1:
    #                 v['complete'] = '1'
    #                 if self._check_completion():
    #                     break
    #                 else:
    #                     self._evaluate_units()

    # def _evaluate_units(self):
    #     for k, v in self._cells.items():
    #         if v['complete'] == '1':
    #             self._remove_val_from_unit('row', v['row'], v['val'][0])
    #             self._remove_val_from_unit('col', v['col'], v['val'][0])
    #             self._remove_val_from_unit('block', v['block'], v['val'][0])

    def _get_units(self, unit_type: str) -> dict:
        if unit_type == "rows":
            digit = 0
        elif unit_type == "columns":
            digit = 2
        else:
            digit = 4

        keys = dict()
        for num in range(9):
            _key = num
            _values = []
            for k, v in self._cells.items():
                if int(k[digit]) == num:
                    _values.append(k)
            keys[_key] = {
                "keys": _values,
                "completed": False
            }
        return keys

    def _evaluate_unit(self, unit):
        return True

    def solve_cells(self):
        _completed = self._check_completion()
        _dirty_bit = True

        while not _completed and _dirty_bit:
            _dirty_bit = False
            _units = 
            for _unit in self._rows:
                _unit_completed = self._evaluate_unit(_unit)
                if not _unit_completed:
                    _unit_dirty_bit = self._solve_unit(_unit)
                    if _unit_dirty_bit:
                        _dirty_bit = True

            for _row in self._rows:
                _completed = self._evaluate_unit(_row)

            for _row in self._rows:
                _completed = self._evaluate_unit(_row)


if __name__ == '__main__':
    block = Block(file_name="cells2.json")
    block.solve_cells()
    # block.print_cells()
