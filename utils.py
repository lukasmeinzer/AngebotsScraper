import datetime
import toml
    

def table_name() -> str:
    current_year = datetime.datetime.now().isocalendar()[0]
    current_week = datetime.datetime.now().isocalendar()[1]
    
    table_name = str(current_year) + "_" + str(current_week)
    return table_name

def readToml(section, key) -> str:
    data = toml.load("Config_scraping.toml")
    return data[section][key]

def DbConnectionString(db_name: str) -> str:
    connection_string = (
        "mysql+mysqlconnector://"
        + readToml("MySQL_Server", "User")
        + ":"
        + readToml("MySQL_Server", "Pwd")
        + "@"
        + readToml("MySQL_Server", "Host")
        + "/"
        + db_name
        + "?auth_plugin=mysql_native_password"
    ) 
    return connection_string