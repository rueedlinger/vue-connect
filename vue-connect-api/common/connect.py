import requests
from common import config

request_timeout_sec = config.get_request_timeout()
poll_intervall_sec = config.get_poll_intervall()


def load_state():
    state = []
    r = requests.get(
        config.get_connect_url() + "/connectors?expand=info&expand=status",
        timeout=request_timeout_sec,
    )
    connectors = r.json()
    for name in connectors:
        connector = connectors[name]
        connector_state = connector["status"]

        if "trace" in connector_state["connector"]:
            trace_short_connector = connector_state["connector"]["trace"].split("\n")
            if len(trace_short_connector) > 0:
                connector_state["connector"]["traceShort"] = trace_short_connector[0]

                short_task_connectors = trace_short_connector[0].split(":")

                if len(short_task_connectors) > 1:
                    connector_state["connector"][
                        "traceException"
                    ] = short_task_connectors[0].strip()
                    connector_state["connector"][
                        "traceMessage"
                    ] = short_task_connectors[1].strip()

        for task in connector_state["tasks"]:
            if "trace" in task:
                trace_short_task = task["trace"].split("\n")
                if len(trace_short_task) > 0:
                    task["traceShort"] = trace_short_task[0]

                    short_task_parts = trace_short_task[0].split(":")

                    if len(short_task_parts) > 1:
                        task["traceException"] = short_task_parts[0].strip()
                        task["traceMessage"] = short_task_parts[1].strip()

        state.append(connector_state)
    return state
