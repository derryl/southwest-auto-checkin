import requests


class ResponseStatus:
    def __init__(self, code, search_string):
        self.code = code
        self.search_string = search_string


RESPONSE_STATUS_SUCCESS = ResponseStatus(1, "success")
RESPONSE_STATUS_TOO_EARLY = ResponseStatus(0, "Boarding Pass is more than 24 hours")
RESPONSE_STATUS_INVALID = ResponseStatus(-1, "The confirmation number entered is invalid.")
RESPONSE_STATUS_RES_NOT_FOUND = ResponseStatus(-2, "we were unable to retrieve your reservation from our database")
RESPONSE_STATUS_UNKNOWN_FAILURE = ResponseStatus(-100, None)


class CheckIn:
    def __init__(self, confirmation_num, first_name, last_name):
        self.last_name = last_name
        self.first_name = first_name
        self.confirmation_num = confirmation_num

    def post_to_sw(self):
        payload = {
            'confirmationNumber': self.confirmation_num,
            'firstName': self.first_name,
            'lastName': self.last_name
        }
        response = requests.post('http://www.southwest.com/flight/retrieveCheckinDoc.html', data=payload)

        # todo: try post on save and fail if not success or more than 24 hour status
        if response.status_code is 200:
            if response.content.find(RESPONSE_STATUS_SUCCESS.search_string) is not -1:
                print 'Success for reservation ' + self.confirmation_num
                return RESPONSE_STATUS_SUCCESS.code
            elif response.content.find(RESPONSE_STATUS_TOO_EARLY.search_string) is not -1:
                # more than 24 hours before
                print 'Checking in too early for reservation ' + self.confirmation_num
                return RESPONSE_STATUS_TOO_EARLY.code
            elif response.content.find(RESPONSE_STATUS_INVALID.search_string) is not -1:
                # invalid format
                print 'Invalid confirmation number ' + self.confirmation_num
                return RESPONSE_STATUS_INVALID.code
            elif response.content.find(RESPONSE_STATUS_RES_NOT_FOUND.search_string) is not -1:
                # incorrect name or confirmation number
                print "Can't find reservation in data base " + self.confirmation_num
                return RESPONSE_STATUS_RES_NOT_FOUND.code
            else:
                print response.content
                print 'WTF: ' + self.reservation.__str__()
                return RESPONSE_STATUS_UNKNOWN_FAILURE.code

        print 'received status other then 200 for ' + self.confirmation_num
        print response.content
        return RESPONSE_STATUS_UNKNOWN_FAILURE.code
