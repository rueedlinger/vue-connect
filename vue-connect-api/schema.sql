DROP TABLE IF EXISTS VC_CLUSTER_CACHE;

CREATE TABLE VC_CLUSTER_CACHE(
    CLUSTER_ID INT PRIMARY KEY,
    CLUSTTER_URL  VARCHAR(250) NOT NULL, 
    RUNNING INTEGER NOT NULL DEFAULT 0 CHECK(RUNNING IN (0,1)),
    CLUSTER_STATE JSON DEFAULT NULL,
    ERROR_MESSAGE TEXT DEFAULT NULL,
    LAST_RUNNING_TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
    CREATED_TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP
);
