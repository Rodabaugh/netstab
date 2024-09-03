UI_WIDTH=800
UI_HEIGHT=1000
UI_FONT_SIZE = 18
UI_FONT = "Georgia"
UI_Y_PADDING = 3
UI_X_PADDING = 3
UI_REPORT_WIDTH = 80
UI_REPORT_HEIGHT = 40

DEFAULT_HOST = "1.1.1.1"
DEFAULT_NUM_PACKETS = "4"

STATUS_PINGING_TEXT = "We're pinging!"
STATUS_NOT_PINGING_TEXT = "We're not pinging..."
STATUS_STOP_PINGING_TEXT = "We're stopping!"

HELP_MESSAGE = 'At least one is required.\nThe rest can be blank.\n\nIf Number of Packets is 0, it will ping until you click "STOP!"'

ERROR_NO_HOSTS = "No hosts were provided. Please provide a host."
ERROR_PING_IN_PROGRESS = "A ping is in progress. Please stop the ping, or wait for it to finish."
ERROR_NO_LOG_FILE = "No log file is open.\nPlease create a new one or open an existing one."

FILE_HEADING = "Time Sent,Host,Latency,TTL,Dropped\n"

REPORT_HEADING = "NetStab Report"
REPORT_SEPARATOR = "\n---------------------------\n"
REPORT_LOWEST_LATENCY = "\nLowest Latency" + REPORT_SEPARATOR
REPORT_AVERAGE_HEADING = "\nAverage Latency" + REPORT_SEPARATOR
REPORT_HIGHEST_LATENCY = "\nHighest Latency" + REPORT_SEPARATOR
REPORT_DROPPED_HEADING = "\nDropped Packets" + REPORT_SEPARATOR
REPORT_HIGHEST_SEQUENTIAL_DROPPED = "\nHighest Sequential Dropped" + REPORT_SEPARATOR
REPORT_NOT_PROCESSED = 'No data has been processed yet. Click "Process!" to generate a report.'
REPORT_WORKING = "Processing... Please wait for the report to be created."
REPORT_ERROR = "We failed to create the report. If you know your data to be good, please open a GitHub issue and include your NetStab log file."