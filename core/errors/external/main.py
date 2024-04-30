from core.errors.main import CustomErrorSerializer

database_error = CustomErrorSerializer(50001, 'Database Error', 'Database Error', 500)

all_external_errors = {
    database_error
}