# Super, Coderbyte Take Home Project
# Callum Takasaka
# January 23, 2023
# Code uses only base Python3.10.x as I was unsure if numpy / pandas was allowed
# Thank you for your understanding!

# I use a regular expression for part of the cleaning process
# (I believe this to be more standard than using Python's specific regexp-like syntax)
import re

def separate_cols(columns):
    return columns.split(';')

def flightcode_to_int(flightcode):
    return int(float(flightcode))

def clean_airline_code(airline_code):

    # remove any non-alphanumeric characters, leaving spaces
    clean_airline_code = re.sub("[^a-zA-Z\s]", "", airline_code)

    # also, ensure any trailing or leading spaces are removed
    clean_airline_code = re.sub("^\s+", "", clean_airline_code)
    clean_airline_code = re.sub("\s$", "", clean_airline_code)

    return clean_airline_code

def stringify_row(first_part, second_part):

    stringified_row = ";".join([str(attr) for attr in first_part]) + ";"
    stringified_row += ";".join(second_part)

    return stringified_row

def stringify_headers(headers):
    return ";".join(headers) + '\\n'

def clean_stringified_table(table):

    cleaned_rows = []
    # before working with the data, let us separate it for ease of access
    rows = table.split("\n")

    # isolate the headers from the data, and further split them into individuals
    headers = separate_cols(rows[0])
    # now, let's fix that To_From header!
    fixed_headers = headers[0:-1] + headers[-1].split("_")

    # moving onto the actual data now
    prev_flightcode = 0
    for i in range(1, len(rows)):    # ignore the first "row" as it is the headers

        # separating out the attributes of each row
        attrs = separate_cols(rows[i])

        # if we find an empty / corrupted row, we have reached the end of the table
        if len(attrs) == len(headers):
            clean_row = ""
            
            # check if the flightcode exists, if not, update it based on our index and/or the initial flight code
            flightcode = attrs[2]
            if flightcode == '':
                attrs[2] = prev_flightcode + 10
                prev_flightcode = attrs[2]
            else:
                # need to first convert the string to a float, then to an integer
                prev_flightcode = flightcode_to_int(flightcode)
                # we want to ensure the flightcode column contains only integer values
                attrs[2] = prev_flightcode

            # we want to split the To_From column
            to_from = attrs[-1].split("_")
            # also, capital case these columns
            to_from = [place.title() for place in to_from]

            # now, clean the airline code
            attrs[0] = clean_airline_code(attrs[0])

            # finally, rebuild the row to be stringified again
            stringified_row = stringify_row(attrs[0:-1], to_from)

            cleaned_rows.append(stringified_row)

    # complete the re-stringification, adding line breaks between rows
    restringified_headers = stringify_headers(fixed_headers)
    
    # also, make sure to include the final newline terminator (not the scary robot kind)
    return (restringified_headers + '\\n'.join(cleaned_rows) + '\\n')


# initial stringified table we are given,
string_table = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'

ans = clean_stringified_table(string_table)
print(ans)