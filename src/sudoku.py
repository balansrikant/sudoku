import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Block:
    def __init__(self, file_name: str = None) -> None:
        self._cells = {}
        self._completed_cells = 0
        self._completed_status = False
        self._initialize_cells()

        if file_name:
            self._read_input(file_name)
        
    def _initialize_cells(self):
        logger.info("initializing cells...")
        for _row in range(9):
            for _column in range(9):
                _block = (3 * (_row//3)) + (_column//3)
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
            _row = int(k)
            for _column in range(9):
                _block = (3 * (_row//3)) + (_column//3)
                _key = str(_row) + '_' + str(_column) + "_" + str(_block)
                if v[_column] != "0":
                    _values = [v[_column]]
                    self._cells[_key] = {
                        'row': _row,
                        'col': _column,
                        'block': _block,
                        'values': _values,
                        'complete': True
                    }
                    self._completed_cells += 1

        logger.info("\n")
    
    def _check_completion(self):
        self._completed_status = True if self._completed_cells == 81 else False
        return self._completed_status

    def print_cells(self):
        for _row in range(9):
            _display = ""
            if _row in [0, 3, 6]:
                for _ in range(90):
                    _display += "-"
                _display += "\n"

            for _column in range(9):
                _block = (3 * (_row//3)) + (_column//3)
                key = str(_row) + '_' + str(_column) + "_" + str(_block)
                _display = _display + str(str(''.join(str(e) for e in self._cells[key]['values'])) + "          ")[:10]
            print(_display, flush=True)
            
    def _get_units(self) -> list:
        """get units of 9 i.e. rows, columns, blocks"""
        units = []

        # loop through rows, columns and blocks
        for digit in [0, 2, 4]:
            # loop through (row/column/block) 0-9
            for num in range(9):
                keys = []
                for k in self._cells:
                    if int(k[digit]) == num:
                        keys.append(k)
                units.append(keys)
        return units

    def _evaluate_unit(self, unit):
        status = False
        # solve singleton
        _singleton_status = self._solve_singleton(unit)

        # solve sole option
        _sole_option_status = self._solve_sole_option(unit)

        if _singleton_status or _sole_option_status:
            status = True

        return status

    def _solve_singleton(self, unit):
        """remove num from other cells if already present as single in some other cell"""
        status = False
        solved_numbers = []
        for key in unit:
            if len(self._cells[key]["values"]) == 1:
                solved_numbers.append(int(self._cells[key]["values"][0]))
        logger.debug(f"solved numbers: {solved_numbers}")

        for key in unit:
            if len(self._cells[key]["values"]) > 1:
                for num in solved_numbers:
                    if num in self._cells[key]["values"]:
                        self._cells[key]["values"].remove(num)
                        status = True
                        if len(self._cells[key]["values"]) == 1:
                            self._completed_cells += 1
                            self._cells[key]["complete"] = True
        return status

    def _solve_sole_option(self, unit):
        """assign single number to cell when it is the only option possible"""
        status = False
        solved_numbers = []
        unsolved_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for key in unit:
            if len(self._cells[key]["values"]) == 1:
                solved_numbers.append(int(self._cells[key]["values"][0]))
        for num in solved_numbers:
            unsolved_numbers.remove(num)
        logger.debug(f"unsolved numbers: {unsolved_numbers}")

        for num in unsolved_numbers:
            key_options = []
            for key in unit:
                if len(self._cells[key]["values"]) > 1 and num in self._cells[key]["values"]:
                    key_options.append(key)

            if len(key_options) == 1:
                key = key_options[0]
                self._cells[key]["values"] = [num]
                status = True
                self._completed_cells += 1
                self._cells[key]["complete"] = True
        return status

    def solve_cells(self):
        _completed = self._check_completion()
        _dirty_bit = True

        # repeat loop until at least one cell is modified or grid is solved
        while not self._check_completion() and _dirty_bit:
            logger.info("entering loop ...")
            _dirty_bit = False
            _units = self._get_units()
            for _unit in _units:
                _status = self._evaluate_unit(_unit)
                if _status:
                    _dirty_bit = True


if __name__ == '__main__':
    block = Block(file_name="cells2.json")
    block.solve_cells()
    block.print_cells()
