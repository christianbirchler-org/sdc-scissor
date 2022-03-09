#
#
#
#
import click
import importlib
import traceback
import time
import os
import sys
import errno
import logging as log
import csv

from code_pipeline.visualization import RoadTestVisualizer
from code_pipeline.tests_generation import TestGenerationStatistic
from code_pipeline.test_generation_utils import register_exit_fun

from code_pipeline.tests_evaluation import OOBAnalyzer

OUTPUT_RESULTS_TO = 'results'
# Sentinel values
ANY = object()
ANY_NOT_NONE = object()
DEFAULT = object()

# Probably this could be simplified with HO functions?
def check_command_with_complex_conditions(
        check_option_is_defined_when_another_is_defined = {},
        at_least_one_must_be_defined = [],
        mutually_exclusive = []
):

    class CommandOptionRequiredClass(click.Command):

        def _get_real_names(self, parameter_list):
            # Retrieve the name users use to set this option
            parameter_list_names = []
            for param_object in parameter_list:
                option_name = None
                for param in self.params:
                    if param.name == param_object:
                        option_name = param.opts[0]
                        break
                parameter_list_names.append(option_name)
            return parameter_list_names

        def _is_option_defined(self, ctx, option):
            return option in ctx.params and ctx.params[option] is not None

        def invoke(self, ctx):
            # cannot_be_defined_at_the_same_time
            for option1, option2 in mutually_exclusive:
                a = self._is_option_defined(ctx, option1)
                b = self._is_option_defined(ctx, option2)
                # They cannot be active at the same time
                if a and b:
                    # Show the error message
                    raise click.ClickException(
                        f"Only one of those options must be defined {self._get_real_names([option1, option2])}")

            # at_least_one_must_be_defined
            for list_of_options in at_least_one_must_be_defined:
                at_least_one_defined = False
                for option in list_of_options:
                    if option in ctx.params and ctx.params[option] is not None:
                        at_least_one_defined = True
                if not at_least_one_defined:
                    # Show the error message
                    raise click.ClickException(f"At least one of those options must be defined {self._get_real_names(list_of_options)}")

            # check_option_is_defined_when_another_is_defined
            for requiring_tuple, required_parameters in check_option_is_defined_when_another_is_defined.items():
                # Check if the requiring parameter is set
                if requiring_tuple[0] in ctx.params:
                    # Check if the value of the requiring parameter is the expected one
                    if requiring_tuple[0] == str(ANY) or (ctx.params[requiring_tuple[0]] is not None and requiring_tuple[0] == str(ANY_NOT_NONE)) or ctx.params[requiring_tuple[0]] == requiring_tuple[1]:
                        # In this case, all the required parameters must be declared. Note we do not check their value.
                        # Note each parameter is validated by a callback, so at this point we assume that if their value
                        #   is given, it is correct
                        for required_parameter in required_parameters:
                            if ctx.params[required_parameter] is None:
                                option_name = self._get_real_names([required_parameter])[0]
                                # Show the error message
                                raise click.ClickException(f"If {requiring_tuple[0]} is set to {requiring_tuple[1]}"
                                                           f" the option {option_name} must be specified")


            super(CommandOptionRequiredClass, self).invoke(ctx)

    return CommandOptionRequiredClass


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def validate_speed_limit(ctx, param, value):
    """
    The speed limit must be a positive integer greater than 10 km/h (lower values might trigger the
    car-not-moving oracle
    """
    if int(value) < 10:
        raise click.BadParameter(
            'The provided value for ' + str(param) + ' is invalid. Choose a value greater than 10')
    else:
        return int(value)


def validate_oob_tolerance(ctx, param, value):
    """
    OOB tolerance must be a value between 0.0 and 1.0
    """
    if value < 0.0 or value > 1.0:
        raise click.BadParameter(
            'The provided value for ' + str(param) + ' is invalid. Choose a value between 0.0 and 1.0')
    else:
        return value


def validate_map_size(ctx, param, value):
    """
    The size of the map is defined by its edge. The edge can be any (integer) value between 100 and 1000
    """
    if int(value) < 100 or int(value) > 1000:
        raise click.BadParameter(
            'The provided value for ' + str(param) + ' is invalid. Choose an integer between 100 and 1000')
    else:
        return int(value)


def validate_optional_time_budget(ctx, param, value):
    """
    A valid time budget is a positive integer of 'seconds' or it should not be set, i.e., set to str(DEFAULT).
    Note we need str(DEFAULT) because click works only with strings
    """
    if value != str(DEFAULT) and int(value) < 1:
        raise click.BadParameter('The provided value for ' + str(param) + ' is invalid. Choose any positive integer')

    # Transform the default value to None after checking the condition
    return int(value) if value != str(DEFAULT) else None


def create_experiment_description(result_folder, params_dict):
    log.info("Creating Experiment Description")
    experiment_description_file = os.path.join(result_folder, "experiment_description.csv")
    csv_columns = params_dict.keys()
    try:
        with open(experiment_description_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(params_dict)
            log.info("Experiment Description available: %s", experiment_description_file)
    except IOError:
        log.error("I/O error. Cannot write Experiment Description")


def create_summary(result_folder, raw_data):
    log.info("Creating Reports")

    # Refactor this
    if type(raw_data) is TestGenerationStatistic:
        log.info("Creating Test Statistics Report:")
        summary_file = os.path.join(result_folder, "generation_stats.csv")
        csv_content = raw_data.as_csv()
        with open(summary_file, 'w') as output_file:
            output_file.write(csv_content)
        log.info("Test Statistics Report available: %s", summary_file)

    log.info("Creating OOB Report")
    oobAnalyzer = OOBAnalyzer(result_folder)
    oob_summary_file = os.path.join(result_folder, "oob_stats.csv")
    csv_content = oobAnalyzer.create_summary()
    with open(oob_summary_file, 'w') as output_file:
        output_file.write(csv_content)

    log.info("OOB  Report available: %s", oob_summary_file)


def post_process(ctx, result_folder, the_executor):
    """
        This method is invoked once the test generation is over.
    """
    # Plot the stats on the console
    log.info("Test Generation Statistics:")
    log.info(the_executor.get_stats())

    # Generate the actual summary files
    create_experiment_description(result_folder, ctx.params)

    # Generate the other reports
    create_summary(result_folder, the_executor.get_stats())


def create_post_processing_hook(ctx, result_folder, executor):
    """
        Uses HighOrder functions to setup the post processing hooks that will be trigger ONLY AND ONLY IF the
        test generation has been killed by us, i.e., this will not trigger if the user presses Ctrl-C

    :param result_folder:
    :param executor:
    :return:
    """

    def _f():
        if executor.is_force_timeout():
            # The process killed itself because a timeout, so we need to ensure the post_process function
            # is called
            post_process(ctx, result_folder, executor)

    return _f


def setup_logging(log_to, debug):
    def log_exception(extype, value, trace):
        log.exception('Uncaught exception:', exc_info=(extype, value, trace))

    # Disable annoyng messages from matplot lib.
    # See: https://stackoverflow.com/questions/56618739/matplotlib-throws-warning-message-because-of-findfont-python
    log.getLogger('matplotlib.font_manager').disabled = True

    term_handler = log.StreamHandler()
    log_handlers = [term_handler]
    start_msg = "Started test generation"

    if log_to is not None:
        file_handler = log.FileHandler(log_to, 'a', 'utf-8')
        log_handlers.append(file_handler)
        start_msg += " ".join(["writing to file: ", str(log_to)])

    log_level = log.DEBUG if debug else log.INFO

    log.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=log_level, handlers=log_handlers)

    sys.excepthook = log_exception

    log.info(start_msg)

# Pay attention that here we use the names of Python parameters, so we use dave2_model instead of dave2-model
@click.command(cls=check_command_with_complex_conditions(
    # Conditionally check one option if others are set
    check_option_is_defined_when_another_is_defined = {
        # If executor is dave2 then the dave2_model becomes mandatory
        ('executor', 'dave2'): ['dave2_model'],
        # If generation_budget is given then the execution_budget must be given as well
        ('generation_budget', ANY_NOT_NONE ): ['execution_budget'],
        # If execution_budget is given then the generation_budget must be given as well
        ('execution_budget', ANY_NOT_NONE ): ['generation_budget'],
    },
    # Conditionally check that at least one option among the defined is set
    at_least_one_must_be_defined = [ ['time_budget', 'generation_budget', 'execution_budget'] ],
    mutually_exclusive = [('time_budget', 'generation_budget'), ('time_budget', 'execution_budget')]

))
@click.option('--executor', type=click.Choice(['mock', 'beamng', 'dave2'], case_sensitive=False), default="mock",
              show_default='Mock Executor (meant for debugging)',
              help="The name of the executor to use. Currently we have 'mock', 'beamng' or 'dave2'.")
@click.option('--dave2-model', required=False, type=click.Path(exists=True),
              help="Path of the pre-trained Dave2 driving AI model (in .h5 format). Mandatory if the executor is dave2")
@click.option('--beamng-home', required=False, default=None, type=click.Path(exists=True),
              show_default='None',
              help="Customize BeamNG executor by specifying the home of the simulator.")
@click.option('--beamng-user', required=False, default=None, type=click.Path(exists=True),
              show_default='Currently Active User (~/BeamNG.tech/)',
              help="Customize BeamNG executor by specifying the location of the folder "
                   "where levels, props, and other BeamNG-related data will be copied."
                   "** Use this to avoid spaces in URL/PATHS! **")
# Budgeting options
@click.option('--generation-budget', required=False, default=DEFAULT, callback=validate_optional_time_budget,
              help="Time budget for the test generation. Expressed in 'real-time' seconds.")
@click.option('--execution-budget', required=False, default=DEFAULT, callback=validate_optional_time_budget,
              help="Time budget for the test execution. Expressed in 'simulated-time' seconds.")
@click.option('--time-budget', required=False, default=DEFAULT, callback=validate_optional_time_budget,
              help="Overall budget for the generation and execution. Expressed in 'real-time'"
                   "seconds. This option is here to be back-ward compatible and will take "
                   "precedence over generation-budget and execution-budget")

@click.option('--map-size', type=int, default=200, callback=validate_map_size,
              show_default='200m, which leads to a 200x200m^2 squared map',
              help="The lenght of the size of the squared map where the road must fit."
                   "Expressed in meters.")
@click.option('--oob-tolerance', type=float, default=0.95, callback=validate_oob_tolerance,
              show_default='0.95',
              help="The tolerance value that defines how much of the vehicle should be outside the lane to "
                   "trigger a failed test. Must be a value between 0.0 (all oob) and 1.0 (no oob)")
@click.option('--speed-limit', type=int, default=70, callback=validate_speed_limit,
              show_default='70 Km/h',
              help="The max speed of the ego-vehicle"
                   "Expressed in Kilometers per hours")
@click.option('--module-name', required=True, type=str,
              help="Name of the module where your test generator is located.")
@click.option('--module-path', required=False, type=click.Path(exists=True),
              help="Path of the module where your test generator is located.")
@click.option('--class-name', required=True, type=str,
              help="Name of the class implementing your test generator.")
# Visual Debugging
@click.option('--visualize-tests', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Visualize the last generated test, i.e., the test sent for the execution. "
                   "Invalid tests are also visualized.")
# Logging options
@click.option('--log-to', required=False, type=click.Path(exists=False),
              help="Location of the log file. If not specified logs appear on the console")
@click.option('--debug', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Activate debugging (results in more logging)")
@click.pass_context
def generate(ctx, executor, dave2_model, beamng_home, beamng_user,
             generation_budget, execution_budget, time_budget,
             map_size, oob_tolerance, speed_limit,
             module_name, module_path, class_name,
             visualize_tests, log_to, debug):

    ctx.ensure_object(dict)

    # TODO Refactor by adding a create summary command and forwarding the output of this run to that command

    # Setup logging
    setup_logging(log_to, debug)

    # Setup test generator by dynamically loading it
    if module_path:
        log.info(f"Loading module from {module_path}")
        sys.path.append(module_path)
        
    log.info(f"Try to import {class_name} from {module_name}")
    module = importlib.import_module(module_name)
    the_class = getattr(module, class_name)

    road_visualizer = None
    # Setup visualization
    if visualize_tests:
        road_visualizer = RoadTestVisualizer(map_size=map_size)

    # Setup folder structure by ensuring that the basic folder structure is there.
    default_output_folder = os.path.join(get_script_path(), OUTPUT_RESULTS_TO)
    try:
        os.makedirs(default_output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Create the unique folder that will host the results of this execution using the test generator data and
    # a timestamp as id
    # TODO Allow to specify a location for this folder and the run id
    timestamp_id = time.time() * 100000000 // 1000000
    result_folder = os.path.join(default_output_folder,
                                 "_".join([str(module_name), str(class_name), str(timestamp_id)]))

    try:
        os.makedirs(result_folder)
    except OSError:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)

    log.info("Outputting results to " + result_folder)

    # Setup executor. All the executor must output the execution data into the result_folder
    if executor == "mock":
        from code_pipeline.executors import MockExecutor
        the_executor = MockExecutor(result_folder, map_size,
                                    generation_budget=generation_budget, execution_budget=execution_budget,
                                    time_budget=time_budget,
                                    road_visualizer=road_visualizer)
    elif executor == "beamng":
        from code_pipeline.beamng_executor import BeamngExecutor
        the_executor = BeamngExecutor(result_folder, map_size,
                                      generation_budget=generation_budget, execution_budget=execution_budget,
                                      time_budget=time_budget,
                                      oob_tolerance=oob_tolerance, max_speed_in_kmh=speed_limit,
                                      beamng_home=beamng_home, beamng_user=beamng_user,
                                      road_visualizer=road_visualizer)

    #     def __init__(self, result_folder, map_size, dave2_model,
    elif executor == "dave2":
        from code_pipeline.dave2_executor import Dave2Executor
        the_executor = Dave2Executor(result_folder, map_size, dave2_model,
                                     generation_budget=generation_budget, execution_budget=execution_budget,
                                     time_budget=time_budget,
                                     oob_tolerance=oob_tolerance, max_speed=speed_limit,
                                     beamng_home=beamng_home, beamng_user=beamng_user,
                                     road_visualizer=road_visualizer)

    # Register the shutdown hook for post processing results
    register_exit_fun(create_post_processing_hook(ctx, result_folder, the_executor))

    try:
        # Instantiate the test generator
        test_generator = the_class(executor=the_executor, map_size=map_size)
        # Start the generation
        test_generator.start()
    except Exception:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)
    finally:
        # Ensure the executor is stopped no matter what.
        # TODO Consider using a ContextManager: With executor ... do
        the_executor.close()

    # We still need this here to post process the results if the execution takes the regular flow
    post_process(ctx, result_folder, the_executor)


if __name__ == '__main__':
    generate()
