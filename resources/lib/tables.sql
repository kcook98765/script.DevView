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
CREATE TABLE IF NOT EXISTS results (
    code_type TEXT,
    base_code TEXT,
    code_run TEXT,
    results TEXT,
    PRIMARY KEY(code_type,base_code,code_run)
);