StatusOk = 0

# arguments err, code from 1000 to 2000
SourceUrlIllegal = 1000
SourceURLNotExist = 1001
DstUrlIllegal = 1002

# server err, code from 200 to 3000
ServerUnknownError = 2000

messages = {
    StatusOk: "OK",
    SourceUrlIllegal: "source url illegal",
    SourceURLNotExist: "source url not exist",
    DstUrlIllegal: "dsl url illegal",
    ServerUnknownError: "Server unknown error"
}


def code2msg(code):
    if code not in messages:
        raise ValueError('code illegal')

    return messages[code]
