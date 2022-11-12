CREATE TABLE IF NOT EXISTS infotag (
    function_name TEXT ,
    data_type TEXT,
    keys TEXT,
    return_type TEXT,
    notes TEXT,
    V19 TEXT,
    V20 TEXT,
    PRIMARY KEY(function_name,data_type,V19,V20)
);
CREATE TABLE IF NOT EXISTS listitem (
    listitem TEXT,
    notes TEXT,
    PRIMARY KEY(listitem)
);
