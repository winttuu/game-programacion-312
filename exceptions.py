class PlayerHasDiedError(Exception):
    pass

class PlayerHasReceivedDamageError(Exception):
    pass

class NotMoreStages(Exception):
    """Excepción lanzada cuando no hay más niveles disponibles."""
    pass