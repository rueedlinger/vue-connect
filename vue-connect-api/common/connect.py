from datetime import datetime

import requests

from common import config

request_timeout_sec = config.get_request_timeout()
poll_intervall_sec = config.get_poll_intervall()


def load_state(cluster_id):

    cluster = config.get_connect_clusters()[cluster_id]
    url = cluster["url"]

    state = []
    r = requests.get(
        url + "/connectors?expand=info&expand=status",
        timeout=request_timeout_sec,
    )
    connectors = r.json()

    if connectors is None:
        return state

    for name in connectors:
        connector = connectors[name]

        if "status" not in connector:
            continue

        connector_state = connector["status"]

        if "connector" in connector_state and "trace" in connector_state["connector"]:
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

            connector_state["connector"]["downtime"] = str(datetime.now().isoformat())

        if "tasks" in connector_state:
            for task in connector_state["tasks"]:
                if "trace" in task:
                    trace_short_task = task["trace"].split("\n")
                    if len(trace_short_task) > 0:
                        task["traceShort"] = trace_short_task[0]

                        short_task_parts = trace_short_task[0].split(":")

                        if len(short_task_parts) > 1:
                            task["traceException"] = short_task_parts[0].strip()
                            task["traceMessage"] = short_task_parts[1].strip()

                    task["downtime"] = str(datetime.now().isoformat())

        if len(connector_state) > 0:
            connector_state["cluster"] = cluster
            state.append(connector_state)
    return state
