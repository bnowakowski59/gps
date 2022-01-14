def formatDate(dateImportString):
    """
    Change Date/time string from YYYYMMDDhhmmss
    to YYYY-MM-DD hh:mm:ss received from GPRS measurement.
    """

    errorDate = '0'*14
    newDate = ''

    if len(dateImportString) == 14:
        date = dateImportString[:len(dateImportString)-6]
        time = dateImportString[len(date):]

        for i in range(1):
            newDate = f'{newDate}{date[i:i+4]}'

            for j in range(0,4,2):
                newDate = f'{newDate}-{date[j+4:j+6]}'

        newTime = '-'.join(time[i:i+2] for i in range(0, len(time), 2))

        newDateString = f'{newDate}-{newTime}'

        return newDateString


    return errorDate