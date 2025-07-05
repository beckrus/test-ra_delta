from src.repository.utils import get_missing_fk


def test_get_missing_fk():
    error = """(pymysql.err.IntegrityError) (1452, 'Cannot add or update a child row: a foreign key constraint fails (`post`.`parcels`, CONSTRAINT `parcels_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`))')
    [SQL: INSERT INTO parcels (name, weight, cost_usd, session_id, type_id) VALUES (%s, %s, %s, %s, %s)]
    [parameters: ('Nexus Phone', 190.0, 500.0, UUID('8c6f3b8a-c02d-4933-a06e-cdaa215637f3'), 15)]
    (Background on this error at: https://sqlalche.me/e/20/gkpj)""
    """
    assert get_missing_fk(error) == "type_id"
