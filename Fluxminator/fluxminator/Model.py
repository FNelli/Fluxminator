import os
import math
import numpy as np
import xlrd

from fluxminator.Constants import *


class Range:

    def __init__(self, min_=0, max_=0, step=0):

        self.min = min_
        self.max = max_
        self.step = step
        self.numberOfSteps = 0

        self._calculate_steps()

    ''' Getters & Setters: '''

    def get_min(self):
        return self.min

    def set_min(self, v):
        self.min = v
        self._calculate_steps()

    def get_max(self):
        return self.max

    def set_max(self, v):
        self.max = v
        self._calculate_steps()

    def get_step(self):
        return self.step

    def set_step(self, v):
        self.step = v
        self._calculate_steps()

    def get_numberOfSteps(self):
        return self.numberOfSteps

    ''' Functions for querying the parameter set:'''

    def get_all_values(self):
        """ Retrieve all the values within the range """
        value_list = []

        if self.is_valid_range():
            if self.step != 0:                                              # np.arange only works if step != 0
                for value in np.arange(self.min, self.max, self.step):
                    value_list.append(value)
            value_list.append(self.max)

        return value_list

    def is_valid_range(self):
        """ Verify if the range is valid based on the parameters """
        if (self.min > self.max
                or self.min == self.max and self.step != 0
                or self.step > (self.max - self.min)
                or self.step == 0 and self.min != self.max):
            return False
        return True

    def is_value_in_range(self, value):
        """ Verify if the given value is within the range """
        if value != self.min and value != self.max:
            if self.step == 0:                          # np.arange only works if step != 0
                return False
            else:
                return np.arange(self.min, self.max, self.step).__contains__(value)
        return True

    def print_range(self):
        """ Return the range parameters in string format """
        return (str(self.min) + " " + str(self.max) + " " + str(self.step)).replace(',', '.')

    # PRIVATE FUNCTIONS:

    def _calculate_steps(self):
        """ Set the numberOfSteps parameter after modifying the other Range parameters """
        if self.is_valid_range():
            if self.min == self.max:
                self.numberOfSteps = 1
            else:
                self.numberOfSteps = math.ceil((self.max - self.min) / self.step) + 1
        else:
            self.numberOfSteps = 0


class Parameter:

    def __init__(self, type_=None, name=None, desc=None, range_=None):

        self.type = type_
        self.name = name
        self.desc = desc
        self.range = range_                         # Range object

    ''' Getters & Setters: '''

    def get_type(self): return self.type
    def set_type(self, t): self.type = t
    def get_name(self): return self.name
    def set_name(self, n): self.name = n
    def get_desc(self): return self.desc
    def set_desc(self, d): self.name = d
    def get_range(self): return self.range
    def set_range(self, r): self.range = r


class Motor:

    def __init__(self, slot=0, pole=0, params=[]):

        self.numberSlot = slot
        self.numberPole = pole

        self.parameters = params                    # list of Parameter objects
        self.specialParameterCombinations = {}              # key=parameter_name; value=[values...]
        self.specialRowNumber = 0

        self.parameterSetExcelPath = ""

    ''' Getters & Setters: '''
    
    def get_numberSlot(self) -> int:
        return self.numberSlot

    def set_numberSlot(self, v) -> None:
        self.numberSlot = v

    def get_numberPole(self) -> int:
        return self.numberPole

    def set_numberPole(self, v) -> None:
        self.numberPole = v

    def get_parameters(self) -> list:
        return self.parameters

    def get_specialParameterSets(self) -> dict:
        return self.specialParameterCombinations

    def get_specialRowNumber(self) -> int:
        return self.specialRowNumber

    def get_parameterSetExcelPath(self) -> str:
        return self.parameterSetExcelPath

    def set_parameterSetExcelPath(self, p) -> None:
        self.parameterSetExcelPath = p

    ''' Functions for modifying and querying the parameter set:  '''

    def add_parameter(self, p) -> None:
        """ Add a new parameter to the parameter list """
        self.parameters.append(p)

    def update_parameter(self, orig_name, new_parameter) -> None:
        """ Update a parameter in the parameter list based on its original name """
        for i in range(len(self.parameters)):
            if self.parameters[i].get_name() == orig_name:
                self.parameters[i] = new_parameter
                break

    def delete_parameter(self, p) -> None:
        """ Delete parameter from the parameter list """
        self.parameters.remove(p)

    def is_existing_parameter(self, parameter_name) -> bool:
        """ Check whether a parameter is in the parameter list based on its name """
        for p in self.parameters:
            if p.get_name() == parameter_name:
                return True
        return False

    def get_parameter_by_name(self, parameter_name):
        """ Return a parameter based on its name if it exists """
        for p in self.parameters:
            if p.get_name() == parameter_name:
                return p

    def add_special_parameter_combination(self, parameter_names, parameter_values) -> None:
        """ Add a new parameter combination to the dictionary & update special row number """

        if self.specialParameterCombinations == {}:
            for i in range(len(parameter_names)):
                self.specialParameterCombinations[parameter_names[i]] = [parameter_values[i]]
        else:
            for i in range(len(parameter_names)):
                self.specialParameterCombinations[parameter_names[i]].append(parameter_values[i])

        self.specialRowNumber += 1

    def update_special_parameter_set(self, action, orig_name=None, new_name=None, default_value=None) -> None:
        """ Update the special parameter combination dictionary after changes in the parameter set """

        if self.specialParameterCombinations == {}:
            return

        if action == "Add":
            self.specialParameterCombinations[new_name] = [default_value for _ in range(self.specialRowNumber)]

        elif action == "Edit":
            if orig_name != new_name:
                self.specialParameterCombinations[new_name] = self.specialParameterCombinations.pop(orig_name)

        elif action == "Delete":
            del self.specialParameterCombinations[orig_name]
            if len(self.parameters) == 0:
                self.specialRowNumber = 0

    def clear_parameter_set(self) -> None:
        """ Reset all variables related to the parameter table """
        self.parameters = []
        self.specialParameterCombinations = {}
        self.specialRowNumber = 0

        self.parameterSetExcelPath = ""

    ''' Functions for creating the parameter table and the excel file for the simulations '''

    def create_final_parameter_set(self) -> list:
        """ Generate the parameter table with all parameter combinations, including special sets """

        row_number = 1                                      # initialization - number of rows in the parameter table
        list_of_parameter_sets = []                         # lists in list (EXAMPLE: [[A1, A2], [B1], [C1, C2, C3]])

        for parameter in self.parameters:

            parameter_set = parameter.range.get_all_values()
            list_of_parameter_sets.append(parameter_set)

            row_number *= len(parameter_set)                # refresh row number - without special combinations!

        # PARAMETER TABLE: Descartes-product of the parameter values (at this point: without special combinations)

        parameter_table = [[] for _ in range(row_number)]

        iteration_size = 1                                  # number of consecutive identical values in the table column

        ''' EXAMPLE '''
        # Parameter       Iteration size
        # A[1,2]          IT_A = 1 (default)
        # B[1]            IT_B = IT_A * len(A) = 2
        # C[1,2,3]        IT_C = IT_B * len(B) = 2

        #################
        #   A   B   C   #
        #   1   1   1   #
        #   2   1   1   #
        #   1   1   2   #
        #   2   1   2   #
        #   1   1   3   #
        #   2   1   3   #
        #################

        for p_set in list_of_parameter_sets:

            row_index = 0                                               # start from 0 for all columns in the table
            for big_step in range(int(row_number/iteration_size)):      # steps between iterations
                for small_step in range(iteration_size):                # steps within an iteration
                    p_index = big_step % len(p_set)
                    parameter_table[row_index].append(p_set[p_index])   # add the upcoming value in the column
                    row_index += 1

            iteration_size *= len(p_set)                                # set next iteration size (see EXAMPLE above)

        # ADD THE CUSTOMIZED COMBINATIONS TO THE PARAMETER TABLE (only if they are unique!):

        ''' EXAMPLE '''
        # specialParameterSets dictionary (specialRowNumber = 3):
        # specialParameterSets[A] = [1, 10, 100]
        # specialParameterSets[B] = [1, 5, 1]
        # specialParameterSets[C] = [1, 0.5, 0.1]
        # The custom combination A[0], B[0], C[0] is not unique; it already exists in the table (see EXAMPLE above).

        for spec_row_index in range(self.specialRowNumber):             # check all the custom combinations

            unique = False                                  # ensure that the custom combination (row) is unique
            spec_param_combination = []                     # list for the custom combination (row)

            for parameter in self.parameters:               # access the custom values based on the parameter names

                parameter_name = parameter.get_name()
                spec_parameter_value = self.specialParameterCombinations[parameter_name][spec_row_index]

                if not unique:                              # one unique value is enough for a unique combination (row)
                    unique = not parameter.range.is_value_in_range(spec_parameter_value)

                spec_param_combination.append(spec_parameter_value)

            if unique:
                parameter_table.append(spec_param_combination)

        # self.create_parameter_set_excel_file(parameter_table)
        return parameter_table

    def create_parameter_table_excel(self, parameter_table, model_path):
        """ Create excel file (Sets.xlsx) for the simulations with the parameter combinations """

        wb = Workbook()                 # excel file
        ws = wb.active                  # active sheet

        # HEADER:

        type_row = ["Geom / Physical Param"]
        name_row = ["Parameters to FLUX"]
        desc_row = ["Description"]

        for parameter in self.parameters:
            type_row.append(parameter.get_type())
            name_row.append(parameter.get_name())
            desc_row.append(parameter.get_desc())

        ws.append(type_row)
        ws.append(name_row)
        ws.append(desc_row)

        # DATA:

        row_number = len(parameter_table)
        parameter_number = len(self.parameters)

        for i in range(row_number):
            new_row = ["No-%04d" % (i + 1)]
            new_row.extend(parameter_table[i])
            ws.append(new_row)

        # FORMAT:

        ws.column_dimensions['A'].width = 25

        for row in range(1, row_number + 4):                            # header rows + data rows
            for col in range(1, parameter_number + 2):

                if col == 1 or row < 4:                                 # parameter combination (simulation) ID / header
                    if col != 1 and row == 3:
                        ws.cell(row=row, column=col).font = Font(color="FFFFFF")
                    else:
                        ws.cell(row=row, column=col).font = Font(bold=True, color="FFFFFF")
                    ws.cell(row=row, column=col).fill = THYSSEN_FILL

                if row < 4:                                                     # header
                    ws.cell(row=row, column=col).border = DEFAULT_BORDER
                elif row == row_number + 3:                                     # last row in the sheet
                    ws.cell(row=row, column=col).border = BOTTOM_BORDER
                else:
                    ws.cell(row=row, column=col).border = VERTICAL_BORDER

                if col > 1 or row > 3:
                    ws.cell(row=row, column=col).alignment = Alignment(horizontal='center')

        rule = ColorScaleRule(start_type='percentile', start_value=10,          # color scale for data
                              start_color='DAEEF3', end_type='percentile',
                              end_value=90, end_color='00749E')

        for col in range(2, parameter_number + 2):
            col_letter = get_column_letter(col)
            rule_range = '{0}4:{0}{1}'.format(col_letter, row_number + 4)
            ws.conditional_formatting.add(rule_range, rule)

        # SAVE:

        path = model_path + "/Results"
        if not os.path.exists(path):
            os.makedirs(path)
        path += "/Sets.xlsx"

        try:
            wb.save(path)
            self.parameterSetExcelPath = path
        except IOError:
            raise


class FluxModel:

    def __init__(self):

        self.modelPath = None
        self.modelName = None

        self.motor = Motor()

        # Measurement points:
        self.positionCogging = Range()
        self.positionRipple = Range()
        self.rangeCurrent = Range()
        self.rangeGamma = Range()

        # Parameters for the simulation:
        self.nameGamma = "GAMMA"
        self.nameCurrent = "IMAX"
        self.nameCurrentSource = "IPH_U"
        
        # self.multiCurrent = False
        # self.multiGamma = False

        # Parameters for the report files:
        self.gammasFor2Stack = None
        self.gammasFor3Stack = None

    ''' Getters & Setters: '''
    
    def get_modelPath(self): return self.modelPath
    def set_modelPath(self, p): self.modelPath = p
        
    def get_modelName(self): return self.modelName
    def set_modelName(self, p): self.modelName = p

    def get_positionCogging(self): return self.positionCogging

    def get_positionRipple(self): return self.positionRipple

    def get_rangeCurrent(self): return self.rangeCurrent

    def get_rangeGamma(self): return self.rangeGamma

    def get_nameGamma(self): return self.nameGamma
    def set_nameGamma(self, n): self.nameGamma = n

    def get_nameCurrent(self): return self.nameCurrent
    def set_nameCurrent(self, n): self.nameCurrent = n

    def get_nameCurrentSource(self): return self.nameCurrentSource
    def set_nameCurrentSource(self, n): self.nameCurrentSource = n
    
    def get_gammasFor2Stack(self): return self.gammasFor2Stack
    def set_gammasFor2Stack(self, g): self.gammasFor2Stack = g
    
    def get_gammasFor3Stack(self): return self.gammasFor3Stack
    def set_gammasFor3Stack(self, g): self.gammasFor3Stack = g

    ''' Other functions '''

    def read_skewing_file(self):
        """ Retrieve 2Stack / 3Stack data from the Skewing Excel file if possible """
        # Import the skewing file from any location TODO FUTURE DEVELOPMENT
        # TODO openpyxl
        try:
            wb = xlrd.open_workbook("Skewing.xlsx")  # file with possible 2/3 Stack data
            ws = wb.sheet_by_index(0)

            row_number = ws.nrows
            for i in range(1, row_number):
                slot_num = ws.cell_value(rowx=i, colx=0)

                if self.motor.get_numberSlot() == slot_num:
                    pole_num = ws.cell_value(rowx=i, colx=1)

                    if self.motor.get_numberPole() == pole_num:
                        self.gammasFor2Stack = [ws.cell_value(rowx=i, colx=2), ws.cell_value(rowx=i, colx=3)]
                        self.gammasFor3Stack = [ws.cell_value(rowx=i, colx=4), ws.cell_value(rowx=i, colx=5),
                                                ws.cell_value(rowx=i, colx=6)]
                        break

            wb.release_resources()
        except IOError:
            raise


class Model:
    """ MVP - Model class """

    def __init__(self):

        self.sessionNew = True
        self.sessionOld = False
        self.sessionSummary = False

        self.deleteScenarioSolutions = True
        self.priceCalculation = False   # future development

        self.scenarioCogging = True
        self.scenarioRipple = True
        self.depLoad = False           # multi I
        self.depGamma = False          # multi G

        self.fluxModel = FluxModel()

        self.projectInfoFilePath = ""

        # Current state:

        self.scenarioID = "3"

        self.executionInProgress = False
        self.simulationID = 1               # defines the upcoming parameter combination row in Sets.xlsx
        self.channelData = ""

        self.progressState = 0
        self.simulationTimes = []

        self.summarySavingProblem = False

    ''' Getters & Setters: '''

    # Session parameters:
    def is_sessionNew(self): return self.sessionNew
    def set_sessionNew(self, b): self.sessionNew = b

    def is_sessionOld(self): return self.sessionOld
    def set_sessionOld(self, b): self.sessionOld = b

    def is_sessionSummary(self): return self.sessionSummary
    def set_sessionSummary(self, b): self.sessionSummary = b

    def get_deleteScenarioSolutions(self): return self.deleteScenarioSolutions
    def set_deleteScenarioSolutions(self, b): self.deleteScenarioSolutions = b

    # Scenario parameters:
    def is_scenarioCogging(self): return self.scenarioCogging

    def is_scenarioRipple(self): return self.scenarioRipple

    def set_scenarioCogging(self, b):
        self.scenarioCogging = b
        self._set_scenario_id()

    def set_scenarioRipple(self, b):
        self.scenarioRipple = b
        self._set_scenario_id()

    def get_scenarioID(self): return self.scenarioID

    def is_dependencyLoad(self): return self.depLoad
    def set_dependencyLoad(self, b): self.depLoad = b

    def is_dependencyGamma(self): return self.depGamma
    def set_dependencyGamma(self, b): self.depGamma = b

    def get_projectInfoFilePath(self): return self.projectInfoFilePath
    def set_projectInfoFilePath(self, p): self.projectInfoFilePath = p

    # Current state:
    def get_executionInProgress(self): return self.executionInProgress
    def set_executionInProgress(self, b): self.executionInProgress = b

    def get_simulationID(self): return self.simulationID
    def set_simulationID(self, i): self.simulationID = i

    def get_channelData(self): return self.channelData
    def set_channelData(self, d): self.channelData = d

    def get_progressState(self): return self.progressState
    def set_progressState(self, s): self.progressState = s
    
    def get_simulationTimes(self): return self.simulationTimes
    def set_simulationTimes(self, t): self.simulationTimes = t
    def extend_simulationTimes(self, t): self.simulationTimes.append(t)

    def get_summarySavingProblem(self): return self.summarySavingProblem
    def set_summarySavingProblem(self, b): self.summarySavingProblem = b

    ''' Collect data for the project and the simulations: '''

    def create_info_files(self):
        """ Create project info file & and the channel data template , without the specific parameter combination ID
        and values, which are always filled out before the upcoming simulation starts """

        # Cogging related data:
        if self.scenarioCogging:
            project_info_cogging_data = self.fluxModel.positionCogging.print_range()
            channel_data_cogging = project_info_cogging_data + "\n"
        else:
            project_info_cogging_data = '-'
            channel_data_cogging = "0.0 0.0 0.0\n"

        # Ripple related data:
        if self.scenarioRipple:
            project_info_ripple_data = self.fluxModel.positionRipple.print_range()
            channel_data_ripple = project_info_ripple_data + "\n"

            project_info_current_data = self.fluxModel.rangeCurrent.print_range()
            channel_data_current = self.fluxModel.get_nameCurrent() + " " + project_info_current_data + "\n"

            project_info_gamma_data = self.fluxModel.rangeGamma.print_range()
            channel_data_gamma = self.fluxModel.get_nameGamma() + " " + project_info_gamma_data + "\n"

            if self.fluxModel.rangeCurrent.get_numberOfSteps() == 1:
                project_info_ripple_type = "MONO_I_"
                channel_data_ripple_type = "MONO_I_"
            else:
                project_info_ripple_type = "MULTI_I_"
                channel_data_ripple_type = "MULTI_I_"
            if self.fluxModel.rangeGamma.get_numberOfSteps() == 1:
                project_info_ripple_type += "MONO_G"
                channel_data_ripple_type += "MONO_G"
            else:
                project_info_ripple_type += "MULTI_G"
                channel_data_ripple_type += "MULTI_G"

        else:
            project_info_ripple_type = "-"
            project_info_ripple_data = "-"
            project_info_gamma_data = "-"
            project_info_current_data = "-"

            channel_data_ripple_type = "None"
            channel_data_ripple = "0.0 0.0 0.0\n"
            channel_data_current = self.fluxModel.get_nameCurrent() + " 0.0 0.0 0.0\n"
            channel_data_gamma = self.fluxModel.get_nameGamma() + " 0.0 0.0 0.0\n"

        # Price calculation dependent data: TODO FUTURE DEVELOPMENT
        data_for_price_calculation = "Tooth\nRotor\nMagnet\nNone\n"

        # CREATE PROJECT_INFO.XLSX
        wb = Workbook()
        ws = wb.active

        ws.append(["Project Name", self.fluxModel.get_modelName()])
        ws.append(["Slot Number", self.fluxModel.motor.get_numberSlot()])
        ws.append(["Pole Number", self.fluxModel.motor.get_numberPole()])
        ws.append(["Scenarios", self.scenarioID])                       # 1 cogging, 2 ripple, 3 both
        ws.append(["Cogging Rotation", project_info_cogging_data])
        ws.append(["Ripple Rotation", project_info_ripple_data])
        ws.append(["Ripple Type", project_info_ripple_type])
        ws.append(["Current Variation", project_info_current_data])
        ws.append(["Gamma Variation", project_info_gamma_data])
        ws.append(["Gamma vs Ripple", self.depGamma])
        ws.append(["Load vs Ripple", self.depLoad])
        ws.append(["Gamma name", self.fluxModel.get_nameGamma()])
        ws.append(["Current name", self.fluxModel.get_nameCurrent()])
        ws.append(["Current source name", self.fluxModel.get_nameCurrentSource()])
        ws.append(["Delete results", self.deleteScenarioSolutions])

        # MAIN DATA FOR CHANNEL.TXT
        # placeholders: {id} -> No-000X; {params} -> values for current No-000X

        data_model_path = self.fluxModel.get_modelPath().replace('/', '\\\\') + "\n"
        data_model_name = self.fluxModel.get_modelName()[:-4] + "\n"
        data_simulation_id = "{id}\n"                                   # exact value later for every simulation
        data_scenario = self.scenarioID + "\n"
        data_ripple_type = channel_data_ripple_type + "\n"
        data_cogging = channel_data_cogging
        data_ripple = channel_data_ripple
        data_current = channel_data_current
        data_gamma = channel_data_gamma
        data_parameters = "{params}\n"                                  # exact values later for every simulation
        data_delete_results = str(self.deleteScenarioSolutions) + "\n"
        data_current_source = self.fluxModel.get_nameCurrentSource() + "\n"

        self.channelData = data_model_path + data_model_name \
            + data_simulation_id + data_scenario + data_ripple_type \
            + data_cogging + data_ripple + data_current + data_gamma \
            + data_parameters + data_delete_results + data_current_source \
            + data_for_price_calculation

        path = self.fluxModel.get_modelPath() + "/Results"

        if not os.path.exists(path):
            os.makedirs(path)
        try:
            wb.save(path + "/Project_Info.xlsx")
            self.projectInfoFilePath = path + "/Project_Info.xlsx"
        except IOError:
            raise

    # Private functions:

    def _set_scenario_id(self):
        """ Set the scenarioID parameter after modifying the scenario parameters """
        if self.is_scenarioCogging() and not self.is_scenarioRipple():
            self.scenarioID = "1"
        elif not self.is_scenarioCogging() and self.is_scenarioRipple():
            self.scenarioID = "2"
        elif self.is_scenarioCogging() and self.is_scenarioRipple():
            self.scenarioID = "3"
        else:
            self.scenarioID = "0"

