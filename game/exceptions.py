class TurnWarsException(Exception):
    
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)

class InvalidGameCreation(TurnWarsException):

    def __init__(self, message):
        TurnWarsException.__init__(self, message)


class InvalidUnit(TurnWarsException):

    def __init__(self, message):
        TurnWarsTurnWarsException.__init__(self, message)

class BadCoordinateCreation(TurnWarsException):
    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class BadFactoryData(TurnWarsException):

    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class BadFactoryRequest(TurnWarsException):

    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class BadWeaponRequest(TurnWarsException):

    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class BadWeaponCreation(TurnWarsException):

    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class BadMoveRequest(TurnWarsException):
    def __init__(self, message=""):
        TurnWarsException.__init__(self, message)

class UnitDoubleMoveRequest(TurnWarsException):
    def __init__(self, message=""):
        TurnWarsException.__init__(self, message)

class InvalidArmyRequest(TurnWarsException):

    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class InvalidBoardDimensions(TurnWarsException):
    def __init__(self, message):
        TurnWarsException.__init__(self, message)

class BadTransportRequest(TurnWarsException):
    def __init__(self, message):
        TurnWarsException.__init__(self, message)


class BadTransportCreation(TurnWarsException):
    def __init__(self, message):
        Exception.__init__(self, message)

class NoPathFound(TurnWarsException):

    def __init__(self, message):
        Exception.__init__(self, message)
class BuildInvalid(TurnWarsException):
    def __init__(self, message=''):
        super(BuildInvalid, self).__init__(message)

class BadScenarioData(TurnWarsException):
    def __init__(self, message):
        super(BadScenarioData, self).__init__(message)

class BadArmorCreation(TurnWarsException):
    def __init__(self, message):
        Exception.__init__(self, message)
